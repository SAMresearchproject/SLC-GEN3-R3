"""Source-specific R4 operation for the retained exact dense N72 kernel."""
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
import time


def dispatch(payload, *, generation, foundation):
    here = Path(__file__).resolve().parent
    root = next(p for p in here.parents if (p / 'CURRENT_REVISION').is_dir())
    binding = json.loads((here / 'DENSE_N72_BINDING.json').read_text())
    if set(payload) != {'source_instance'} or payload['source_instance'] != binding['source_instance']:
        raise ValueError('GEN2_DENSE_N72 requires its exact frozen source-instance identity')
    from CURRENT_REVISION.runtime import require_generation
    require_generation(generation)
    for row in binding['files']:
        if hashlib.sha256((root / row['path']).read_bytes()).hexdigest() != row['sha256']:
            raise ValueError('Dense N72 bound source differs: ' + row['path'])
    campaign = root / binding['campaign']
    if (campaign / 'execution').exists():
        raise ValueError('Preserve the completed or failed N72 execution; use a successor for another run')
    env = dict(os.environ, OPENBLAS_NUM_THREADS='1', OMP_NUM_THREADS='1', MKL_NUM_THREADS='1')
    started = time.perf_counter()
    with (campaign / 'NATIVE_STDOUT.txt').open('x') as out, (campaign / 'NATIVE_STDERR.txt').open('x') as err:
        run = subprocess.run([sys.executable, str(root / binding['runner']), '--run-id', 'R01'],
                             cwd=root, env=env, stdout=out, stderr=err)
    if run.returncode:
        raise RuntimeError('Dense N72 execution failed; preserved logs in ' + str(campaign))
    require_generation(generation)
    result_path = campaign / 'execution/release/FULL_N72_R01_RESULT.json'
    recovery_path = campaign / 'execution/work/R01/N72_RECOVERY.json'
    result = json.loads(result_path.read_text())
    recovered = json.loads(recovery_path.read_text())
    count = recovered['observed_configuration_count']
    hd = foundation.serialize_hd(count, source_provenance='GEN2_DENSE_N72:sum of reconstructed density-of-states coefficients')
    return {'schema': 'GEN2_R4_DENSE_N72_RESULT_V1', 'generation': generation,
            'source_instance': binding['source_instance'], 'kernel': binding['dense_kernel'],
            'native_result': {'path': str(result_path.relative_to(root)),
                              'sha256': hashlib.sha256(result_path.read_bytes()).hexdigest()},
            'recovery': {'path': str(recovery_path.relative_to(root)),
                         'sha256': hashlib.sha256(recovery_path.read_bytes()).hexdigest()},
            'configuration_count': count, 'configuration_count_hd_log': hd,
            'metrics': result['metrics'], 'operation_seconds': time.perf_counter() - started,
            'minimum_energy': recovered['minimum_energy'], 'maximum_energy': recovered['maximum_energy'],
            'occupied_energy_bins': recovered['occupied_energy_bins'],
            'fixed_coefficient_sha256': recovered['fixed_coefficient_sha256'],
            'classification': result['result_classification'],
            'R4_role': 'Current native operation dispatch, source binding, execution receipts and exact logarithmic count readout',
            'dense_arithmetic': 'Retained H14F kernel; no new logarithmic dense-solver algorithm is assigned'}
