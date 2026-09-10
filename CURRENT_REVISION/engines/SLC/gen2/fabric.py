"""Reusable GEN2 native batch execution on H14F, Ryzen, 780M and T500."""
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import shlex
import shutil
import subprocess
import sys
import time

os.environ.setdefault('OPENBLAS_NUM_THREADS', '1')
os.environ.setdefault('OMP_NUM_THREADS', '1')
import numpy as np

HERE = Path(__file__).resolve().parent
ROOT = next(p for p in HERE.parents if (p / 'CURRENT_REVISION/REGISTRY.json').is_file())
from .hardware import plan_batch, evaluate_primary

SSH = ['ssh', '-o', 'BatchMode=yes', '-o', 'ConnectTimeout=10', '-o', 'StrictHostKeyChecking=yes', 'lilhelper@10.77.0.2']
SCP = ['scp', '-q', '-o', 'BatchMode=yes', '-o', 'ConnectTimeout=10', '-o', 'StrictHostKeyChecking=yes']


def sha(path):
    h = hashlib.sha256()
    with Path(path).open('rb') as stream:
        for block in iter(lambda: stream.read(8 * 1024 * 1024), b''): h.update(block)
    return h.hexdigest()


def write(path, value):
    data = value if isinstance(value, bytes) else (json.dumps(value, sort_keys=True, indent=2, allow_nan=False) + '\n').encode()
    if path.exists(): raise ValueError('Hardware evidence path already exists: ' + str(path))
    with path.open('xb') as stream:
        stream.write(data); stream.flush(); os.fsync(stream.fileno())
    fd = os.open(path.parent, os.O_RDONLY | os.O_DIRECTORY)
    try: os.fsync(fd)
    finally: os.close(fd)


def remote(command, **kwargs):
    return subprocess.run(SSH + [shlex.join(command)], check=True, capture_output=True, **kwargs)


def execute(payload=None):
    payload = {} if payload is None else payload
    if not isinstance(payload, dict) or set(payload) - {'output_root', 'contracts'}:
        raise ValueError('GEN2 source batch accepts output_root and optional native source contracts')
    started = time.perf_counter()
    root = Path(payload.get('output_root') or ROOT / 'SAM_RUNTIME/R3/hardware')
    root.mkdir(parents=True, exist_ok=True)
    stamp = datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%S%fZ')
    run = root / ('GEN2_' + stamp); run.mkdir()
    destination = '/home/lilhelper/SAM_Research_Project/GEN2_BUILD1/' + run.name
    plan, rows, blocks = plan_batch(payload.get('contracts'))
    if not payload.get('contracts') and (len(rows) != 62976 or [s['rows'] for s in plan['sections']] != [384, 384, 384, 384, 49152, 12288]):
        raise ValueError('GEN2 hardware source roster differs')
    write(run / 'PLAN.json', plan)
    with (run / 'ROWS.npy').open('xb') as stream:
        np.save(stream, rows, allow_pickle=False); stream.flush(); os.fsync(stream.fileno())
    write(run / 'SOURCE_BINDING.json', {'files': {str(p.resolve()): sha(p) for p in
           [HERE / 'hardware.py', HERE / 'native.py', HERE / 'compiler.py', HERE / 'contracts.py',
            HERE / 'exact.py', HERE / 'dependencies/common_reception.py',
            HERE / 'dependencies/native/t18.py', HERE / 'remote_hardware.py', Path(__file__).resolve()]},
           'source_rows_sha256': sha(run / 'ROWS.npy'), 'plan_sha256': sha(run / 'PLAN.json'),
           'remote_directory': destination})
    calibration, reference = [], None
    worker_limit = len(os.environ['SAM_R3_CPU_ORDER'].split(',')) if 'SAM_R3_CPU_ORDER' in os.environ else 14
    for workers in dict.fromkeys((min(4,worker_limit),worker_limit)):
        value, receipt = evaluate_primary(rows, blocks, workers)
        if reference is None: reference = value
        elif not np.array_equal(reference, value): raise ValueError('H14F source schedules disagree')
        calibration.append(receipt)
    selected_workers = min(calibration, key=lambda r: r['seconds'])['workers']
    primary, selected = evaluate_primary(rows, blocks, selected_workers)
    if not np.array_equal(primary, reference): raise ValueError('H14F selected rerun differs')
    selected['executed_after_calibration'] = True
    write(run / 'H14F_OUTPUT.i64le', primary.astype('<i8', copy=False).tobytes())
    write(run / 'H14F.json', {'calibration': calibration, 'selected_schedule': selected, 'compile_seconds': plan['compile_seconds']})
    remote(['python3', '-c', 'import pathlib,sys; pathlib.Path(sys.argv[1]).mkdir(parents=True,exist_ok=False)', destination])
    source_paths = [run / 'PLAN.json', run / 'ROWS.npy', run / 'SOURCE_BINDING.json',
                    HERE / 'dependencies/J4_RESPONSES.jsonl', HERE / 'remote_hardware.py',
                    HERE.parent / 'gen3/resources.py', HERE.parent / 'gen3/RESOURCE_PROFILE.json']
    subprocess.run(SCP + [str(p) for p in source_paths] + ['lilhelper@10.77.0.2:' + destination + '/'], check=True)
    # fsync every received input before starting scientific execution.
    sync_script = 'import os,pathlib,sys; p=pathlib.Path(sys.argv[1]); [(lambda f:(os.fsync(f.fileno()),f.close()))(x.open("rb")) for x in p.iterdir() if x.is_file()]; f=os.open(p,os.O_RDONLY|os.O_DIRECTORY); os.fsync(f); os.close(f)'
    remote(['python3', '-c', sync_script, destination])
    execution = remote(['python3', destination + '/resources.py', 'run', '--role', 'cpu',
                        '--name', 'native-' + stamp.lower(), '--', 'flock', '--exclusive',
                        '/home/lilhelper/SAM_Research_Project/SAM_TRAINING/780m.lock',
                        'env', 'RUSTICL_ENABLE=radeonsi', 'OPENBLAS_NUM_THREADS=1', 'OMP_NUM_THREADS=1',
                        'python3', destination + '/remote_hardware.py', 'run', destination], text=True)
    write(run / 'REMOTE_STDOUT.txt', execution.stdout.encode()); write(run / 'REMOTE_STDERR.txt', execution.stderr.encode())
    result = json.loads(execution.stdout)
    write(run / 'REMOTE_RESULT.json', result)
    for name in ('GPU_OUTPUT.i64le', 'CPU_OUTPUT.i64le', 'MATRIX.i64le', 'COORDINATES.i32le', 'GEN2_NATIVE_SOURCE.cl', 'MANIFEST.json', 'COMPUTATION.json'):
        subprocess.run(SCP + ['lilhelper@10.77.0.2:' + destination + '/' + name, str(run / name)], check=True)
    cpu = np.memmap(run / 'CPU_OUTPUT.i64le', mode='r', dtype='<i8', shape=primary.shape)
    gpu = np.memmap(run / 'GPU_OUTPUT.i64le', mode='r', dtype='<i8', shape=primary.shape)
    if not np.array_equal(primary, cpu) or not np.array_equal(primary, gpu):
        raise ValueError('H14F compiled source and independent CPU/GPU outputs differ')
    resumed = remote(['python3', destination + '/remote_hardware.py', 'resume', destination], text=True)
    resume = json.loads(resumed.stdout)
    if resume['output_sha256'] != sha(run / 'H14F_OUTPUT.i64le'):
        raise ValueError('T500 complete resumed result differs from primary source')
    write(run / 'RESUMPTION.json', resume)
    source_views = []
    for section in plan['sections']:
        a = section['start']; b = a + section['rows']; view = primary[a:b]
        two = len(section['contract']['receivers']) == 2
        row = {'name': section['name'], 'rows': len(view), 'contract_id': section['contract_id'],
               'all_values_match': True, 'port_frames_retained': two,
               'source_event_label_count': len(section['events'])}
        if two:
            summed = view[:, 1:65] + view[:, 65:129]
            row['mixed_equal_coefficient_view_sha256'] = hashlib.sha256(summed.astype('<i8', copy=False).tobytes()).hexdigest()
            row['mixed_view_note'] = 'Exact sum of two separately retained source blocks; no independent extra observation asserted'
        source_views.append(row)
    final = {'status': 'PASS', 'schema': 'GEN2_HARDWARE_QUALIFICATION_V1', 'run': str(run.resolve()),
             'rows': len(rows), 'values': int(primary.size), 'all_H14F_Ryzen_780M_values_equal': True,
             'source_sections': source_views, 'H14F': {'calibration': calibration, 'selected_schedule': selected},
             'remote': result, 'resume': resume, 'remote_directory': destination,
             'primary_output_sha256': sha(run / 'H14F_OUTPUT.i64le'), 'complete_seconds': time.perf_counter() - started,
             'scope': 'Exact finite native source transitions and two-lane source contractions; inverse graph and learned readouts are not GPU claims',
             'input_rows_sha256': sha(run / 'ROWS.npy'), 'plan_sha256': sha(run / 'PLAN.json'),
             'source_binding_sha256': sha(run / 'SOURCE_BINDING.json')}
    write(run / 'RESULT.json', final)
    write(root / ('RESULT_' + stamp + '.json'), {'result_path': str((run / 'RESULT.json').resolve()), 'sha256': sha(run / 'RESULT.json')})
    return {'status': final['status'], 'result_path': str((run / 'RESULT.json').resolve()),
            'result_sha256': sha(run / 'RESULT.json'), 'rows': final['rows'], 'values': final['values'],
            'all_H14F_Ryzen_780M_values_equal': True, 'remote_directory': destination,
            'output_sha256': final['primary_output_sha256'], 'complete_seconds': final['complete_seconds'],
            'source_sections': final['source_sections'], 'installed_entrypoint': str(HERE.resolve()).startswith(str(ROOT / 'CURRENT_REVISION') + '/')}
