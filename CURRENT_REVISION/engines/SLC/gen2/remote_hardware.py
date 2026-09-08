"""Independent Ryzen, actual Rusticl 780M and T500 GEN2 source executor.

Transferred as source to the authorized lilhelper workspace. No project
imports are used. J4 receiver matrices are rebuilt directly from source
templates; CPU and OpenCL evaluate independent transition implementations.
"""
import argparse
from fractions import Fraction
import hashlib
import json
import multiprocessing as mp
import os
from pathlib import Path
import socket
import subprocess
import sys
import time

os.environ.setdefault('OPENBLAS_NUM_THREADS', '1')
os.environ.setdefault('OMP_NUM_THREADS', '1')
os.environ.setdefault('RUSTICL_ENABLE', 'radeonsi')
import numpy as np

KERNEL = r'''
__kernel void native_source(__global const long *rows, __global const long *matrix,
                            __global const int *coordinates, __global long *output,
                            const uint count) {
  uint row=get_global_id(0); if(row>=count) return;
  uint source=(uint)rows[5*row], before=(uint)rows[5*row+1];
  uint axis=(uint)rows[5*row+2]; int delta=(int)rows[5*row+3];
  uint low=(before>>axis)&1u;
  uint after=before^(1u<<axis)^((low^(uint)(delta==-1))<<(axis+9u));
  output[129*row]=(long)after;
  for(uint block=0;block<2;block++) {
    for(uint state=0;state<2;state++) {
      uint address=state ? after : before;
      for(uint lane=0;lane<2;lane++) {
        for(uint channel=0;channel<16;channel++) {
          long sum=0;
          if(coordinates[source*6+3*block]>=0) {
            for(uint j=0;j<3;j++) {
              uint c=(uint)coordinates[source*6+3*block+j];
              uint q=((address>>c)&1u)+2u*((address>>(c+9u))&1u);
              long real=q==0 ? 1 : q==2 ? -1 : 0;
              long imag=q==1 ? 1 : q==3 ? -1 : 0;
              if(lane) { real=real<0 ? -real : real; imag=imag<0 ? -imag : imag; }
              uint m=source*192+block*96+channel*6;
              sum+=matrix[m+j]*real+matrix[m+j+3]*imag;
            }
          }
          output[129*row+1+64*block+32*state+16*lane+channel]=sum;
        }
      }
    }
  }
}
'''
_ROWS = _MATRIX = _COORDINATES = None


def sha(path):
    h = hashlib.sha256()
    with Path(path).open('rb') as stream:
        for block in iter(lambda: stream.read(8 * 1024 * 1024), b''):
            h.update(block)
    return h.hexdigest()


def write(path, data):
    path = Path(path)
    if path.exists():
        raise ValueError('Refusing to overwrite hardware custody: ' + str(path))
    if not isinstance(data, bytes):
        data = (json.dumps(data, sort_keys=True, indent=2, allow_nan=False) + '\n').encode()
    with path.open('xb') as stream:
        stream.write(data); stream.flush(); os.fsync(stream.fileno())
    fd = os.open(path.parent, os.O_RDONLY | os.O_DIRECTORY)
    try: os.fsync(fd)
    finally: os.close(fd)


def rebuild(plan, source):
    wanted = ('N100_EDGE_002', 'N100_EDGE_006', 'N100_EDGE_084')
    templates = {}
    with source.open() as stream:
        for line in stream:
            row = json.loads(line)
            if row['relation_id'] in wanted:
                templates[(row['rho'], row['relation_id'])] = row
    matrix = np.zeros((len(plan['sections']), 2, 16, 6), np.int64)
    coordinates = np.full((len(plan['sections']), 2, 3), -1, np.int32)
    for k, section in enumerate(plan['sections']):
        spec = section['contract']; rho = int(spec['source_binding'].split(':rho=')[1])
        expected_hash = spec['source_binding'].split(':')[1]
        if sha(source) != expected_hash:
            raise ValueError('J4 source hash differs from source contract')
        for block, receiver in enumerate(spec['receivers']):
            coordinates[k, block] = receiver['coordinates']
            for channel, name in enumerate(('forward_amplitude', 'reverse_amplitude')):
                for step in range(4):
                    for j, relation in enumerate(wanted):
                        x, y = templates[(rho, relation)][name][step]
                        offset = 8 * channel + 2 * step
                        matrix[k, block, offset, j] = x
                        matrix[k, block, offset, j + 3] = -y
                        matrix[k, block, offset + 1, j] = y
                        matrix[k, block, offset + 1, j + 3] = x
            supplied = np.array([[int(Fraction(v)) for v in row] for row in receiver['matrix']], np.int64)
            if not np.array_equal(supplied, matrix[k, block]):
                raise ValueError('Independent template contraction differs from compiled receiver')
    bound = max(int(sum(abs(int(v)) for v in row)) for row in matrix.reshape(-1, 6))
    if bound > np.iinfo(np.int64).max:
        raise OverflowError('J4 contraction exceeds signed int64')
    return matrix, coordinates, bound


def pin(queue):
    os.sched_setaffinity(0, [queue.get()])


def cpu_chunk(bounds):
    start, stop = bounds; rows = _ROWS[start:stop]
    output = np.zeros((len(rows), 129), np.int64)
    address, axis, direction = rows[:, 1], rows[:, 2], rows[:, 3]
    q = ((address >> axis) & 1) + 2 * ((address >> (axis + 9)) & 1)
    changed = (q + direction) % 4
    mask = (np.int64(1) << axis) | (np.int64(1) << (axis + 9))
    after = (address & ~mask) | ((changed & 1) << axis) | ((changed >> 1) << (axis + 9))
    output[:, 0] = after
    phase = np.array(((1, 0), (0, 1), (-1, 0), (0, -1)), np.int64)
    for source in range(len(_MATRIX)):
        selected = np.flatnonzero(rows[:, 0] == source)
        if not len(selected): continue
        for block, coordinates in enumerate(_COORDINATES[source]):
            if coordinates[0] < 0: continue
            for step, values in enumerate((address[selected], after[selected])):
                q = ((values[:, None] >> coordinates) & 1) + 2 * ((values[:, None] >> (coordinates + 9)) & 1)
                lift = phase[q]
                signed = np.concatenate((lift[:, :, 0], lift[:, :, 1]), axis=1)
                for lane, h in enumerate((signed, np.abs(signed))):
                    begin = 1 + 64 * block + 32 * step + 16 * lane
                    output[selected, begin:begin + 16] = h @ _MATRIX[source, block].T
    return start, output, {'pid': os.getpid(), 'affinity': sorted(os.sched_getaffinity(0)), 'rows': len(rows)}


def cpu_run(rows, matrix, coordinates, workers):
    global _ROWS, _MATRIX, _COORDINATES
    _ROWS, _MATRIX, _COORDINATES = rows, matrix, coordinates
    cpus = sorted(os.sched_getaffinity(0))[:workers]
    if len(cpus) != workers: raise ValueError('Ryzen profile unavailable')
    context = mp.get_context('fork'); queue = context.Queue()
    for cpu in cpus: queue.put(cpu)
    bounds = np.linspace(0, len(rows), workers + 1, dtype=int)
    started = time.perf_counter()
    with context.Pool(workers, initializer=pin, initargs=(queue,)) as pool:
        parts = pool.map(cpu_chunk, [(int(a), int(b)) for a, b in zip(bounds[:-1], bounds[1:])], chunksize=1)
    output = np.empty((len(rows), 129), np.int64)
    for begin, part, _ in parts: output[begin:begin + len(part)] = part
    return output, {'workers': workers, 'cpus': cpus, 'seconds': time.perf_counter() - started,
                    'worker_processes': [p[2] for p in parts]}


def gpu_run(context, queue, program, rows, matrix, coordinates, batch):
    import pyopencl as cl
    mf = cl.mem_flags
    started = time.perf_counter()
    m = cl.Buffer(context, mf.READ_ONLY | mf.COPY_HOST_PTR, hostbuf=matrix)
    c = cl.Buffer(context, mf.READ_ONLY | mf.COPY_HOST_PTR, hostbuf=coordinates)
    output = np.empty((len(rows), 129), np.int64)
    kernel = cl.Kernel(program, 'native_source'); kernels, transfers = [], []
    for begin in range(0, len(rows), batch):
        count = min(batch, len(rows) - begin)
        x = cl.Buffer(context, mf.READ_ONLY | mf.COPY_HOST_PTR, hostbuf=rows[begin:begin + count])
        y = cl.Buffer(context, mf.WRITE_ONLY, count * 129 * 8)
        event = kernel(queue, (count,), None, x, m, c, y, np.uint32(count))
        transfer = cl.enqueue_copy(queue, output[begin:begin + count], y)
        transfer.wait(); kernels.append((event.profile.end - event.profile.start) * 1e-9)
        transfers.append((transfer.profile.end - transfer.profile.start) * 1e-9)
    queue.finish()
    return output, {'batch_size': batch, 'batches': len(kernels), 'seconds': time.perf_counter() - started,
                    'kernel_seconds': sum(kernels), 'device_to_host_seconds': sum(transfers)}


def readback(directory):
    manifest = json.loads((directory / 'MANIFEST.json').read_text())
    count, size = 0, 0
    for name, item in manifest['files'].items():
        path = directory / name
        if path.stat().st_size != item['bytes'] or sha(path) != item['sha256']:
            raise ValueError('T500 full readback differs: ' + name)
        count += 1; size += path.stat().st_size
    return {'status': 'PASS', 'files': count, 'bytes': size, 'pid': os.getpid(),
            'manifest_sha256': sha(directory / 'MANIFEST.json')}


def run(directory):
    import pyopencl as cl
    started = time.perf_counter()
    binding = json.loads((directory / 'SOURCE_BINDING.json').read_text())
    if sha(directory / 'ROWS.npy') != binding['source_rows_sha256'] or sha(directory / 'PLAN.json') != binding['plan_sha256']:
        raise ValueError('Transferred source batch or plan differs from primary binding')
    executor_hashes = [value for name, value in binding['files'].items() if Path(name).name == 'remote_hardware.py']
    if executor_hashes != [sha(Path(__file__))]:
        raise ValueError('Transferred independent executor source differs')
    plan = json.loads((directory / 'PLAN.json').read_text())
    rows = np.load(directory / 'ROWS.npy', allow_pickle=False)
    matrix, coordinates, bound = rebuild(plan, directory / 'J4_RESPONSES.jsonl')
    cpu_calibration, expected = [], None
    for workers in (4, 16):
        output, timing = cpu_run(rows, matrix, coordinates, workers)
        if expected is None: expected = output
        elif not np.array_equal(expected, output): raise ValueError('Ryzen schedules disagree')
        cpu_calibration.append(timing)
    selected_cpu = min(cpu_calibration, key=lambda r: r['seconds'])['workers']
    cpu, cpu_selected = cpu_run(rows, matrix, coordinates, selected_cpu)
    if not np.array_equal(cpu, expected): raise ValueError('Selected Ryzen rerun differs')
    devices = [d for p in cl.get_platforms() for d in p.get_devices() if '780m' in d.name.lower()]
    if len(devices) != 1: raise ValueError('Actual Radeon 780M device not uniquely available')
    device = devices[0]; context = cl.Context([device])
    queue = cl.CommandQueue(context, properties=cl.command_queue_properties.PROFILING_ENABLE)
    compile_started = time.perf_counter(); program = cl.Program(context, KERNEL).build()
    compile_seconds = time.perf_counter() - compile_started
    calibration = []
    for batch in (512, 4096, 16384, len(rows)):
        gpu, timing = gpu_run(context, queue, program, rows, matrix, coordinates, batch)
        if not np.array_equal(gpu, cpu): raise ValueError('Actual GEN2 GPU source output differs from independent Ryzen')
        calibration.append(timing)
    selected_batch = min(calibration, key=lambda r: r['seconds'])['batch_size']
    gpu, selected = gpu_run(context, queue, program, rows, matrix, coordinates, selected_batch)
    if not np.array_equal(gpu, cpu): raise ValueError('Selected GPU rerun differs')
    write(directory / 'GEN2_NATIVE_SOURCE.cl', KERNEL.encode())
    write(directory / 'CPU_OUTPUT.i64le', cpu.astype('<i8', copy=False).tobytes())
    write(directory / 'GPU_OUTPUT.i64le', gpu.astype('<i8', copy=False).tobytes())
    write(directory / 'MATRIX.i64le', matrix.astype('<i8', copy=False).tobytes())
    write(directory / 'COORDINATES.i32le', coordinates.astype('<i4', copy=False).tobytes())
    result = {'status': 'PASS', 'host': socket.gethostname(), 'rows': len(rows), 'values': int(cpu.size),
              'CPU_GPU_all_values_equal': True, 'maximum_absolute_receiver_bound': bound,
              'source_templates_reconstructed_independently': True,
              'cpu_calibration': cpu_calibration, 'selected_cpu': dict(cpu_selected, executed_after_calibration=True),
              'gpu': {'name': device.name, 'platform': device.platform.name, 'driver': device.driver_version,
                      'global_memory_bytes': device.global_mem_size, 'maximum_allocation_bytes': device.max_mem_alloc_size,
                      'compile_seconds': compile_seconds, 'calibration': calibration,
                      'selected_schedule': dict(selected, executed_after_calibration=True),
                      'scope': 'Packed T18 transition and source signed/occupancy before/after contractions only'},
              'output_sha256': sha(directory / 'GPU_OUTPUT.i64le'),
              'complete_compute_and_write_seconds': time.perf_counter() - started,
              'source_sha256': sha(Path(__file__)), 'kernel_sha256': sha(directory / 'GEN2_NATIVE_SOURCE.cl')}
    result['storage_mount'] = json.loads(subprocess.run(['findmnt', '-J', '-T', str(directory), '-o', 'SOURCE,TARGET,FSTYPE'], check=True, capture_output=True, text=True).stdout)
    result['storage_devices'] = json.loads(subprocess.run(['lsblk', '-J', '-o', 'NAME,MODEL,SIZE,TYPE,MOUNTPOINTS'], check=True, capture_output=True, text=True).stdout)
    write(directory / 'COMPUTATION.json', result)
    manifest = {'files': {p.name: {'sha256': sha(p), 'bytes': p.stat().st_size} for p in sorted(directory.iterdir()) if p.is_file()}}
    write(directory / 'MANIFEST.json', manifest)
    fresh = subprocess.run([sys.executable, str(Path(__file__).resolve()), 'readback', str(directory)], check=True, capture_output=True, text=True)
    result['T500_full_independent_readback'] = json.loads(fresh.stdout)
    write(directory / 'RESULT.json', result)
    return result


def main():
    p = argparse.ArgumentParser(); p.add_argument('mode', choices=('run', 'readback', 'resume')); p.add_argument('directory', type=Path)
    args = p.parse_args(); directory = args.directory.resolve()
    if args.mode == 'run': result = run(directory)
    elif args.mode == 'readback': result = readback(directory)
    else:
        start = time.perf_counter(); result = readback(directory)
        original = json.loads((directory / 'COMPUTATION.json').read_text())
        cpu, gpu = directory / 'CPU_OUTPUT.i64le', directory / 'GPU_OUTPUT.i64le'
        if sha(cpu) != sha(gpu) or sha(gpu) != original['output_sha256']:
            raise ValueError('Resumed complete output differs')
        result.update(resumed=True, output_sha256=sha(gpu), source_recomputed=False, seconds=time.perf_counter() - start)
    print(json.dumps(result, sort_keys=True, indent=2))


if __name__ == '__main__': main()
