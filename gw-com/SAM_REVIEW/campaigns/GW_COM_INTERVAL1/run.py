"""Source-bound interval communication successor to H000733's discrete orbit wave.

Python constructs prescribed source positions and orchestrates decoding/checks.
SLC computes the quadrupole and second differences from those positions.
"""
import csv
from fractions import Fraction as F
import hashlib
import json
from pathlib import Path
import random
import sys

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
sys.path.insert(0, str(ROOT))
from SAM_PROJECT.session import DomainSession
from receiver import decode

MESSAGE = [2, 5, 7, 11, 13, 17]
UNIT = 16
PROFILE = [0, 1, 3, 6, 8, 6, 3, 1, 0]
SOURCE = 'SAM_HISTORY/entries/H000733_2026-08-28_RH_Q3RHV2_SPIN_ORBIT_WAVE_THETA_STATE_HISTORY.md'


def write(path, value):
    path.write_text(json.dumps(value, indent=2) + '\n')


def positions(message, controlled=True):
    events = []
    start = 32
    for _ in range(2):
        packet = [start + UNIT * i for i in range(4)]
        for n in message:
            packet.append(packet[-1] + UNIT * n)
        events.extend(packet)
        start = packet[-1] + 23 * UNIT
    radii = [F(1) for _ in range(events[-1] + 33)]
    if controlled:
        for center in events:
            for offset, value in enumerate(PROFILE):
                radii[center + offset - 4] += F(value, 128)
    axes = [(1, 0), (0, 1), (-1, 0), (0, -1)]
    xy = [(r * axes[k % 4][0], r * axes[k % 4][1]) for k, r in enumerate(radii)]
    return xy, events, radii


def independent(stencil):
    # Independent exact contraction: trace cancels in Qxx-Qyy.
    projected = [2 * (x*x - y*y) for x, y in stencil]
    return projected[0] - 2 * projected[1] + projected[2]


def native_stencils(session, stencils, source_hash):
    values = {}
    unique = sorted(set(stencils))
    nodes = []
    def node(op, **fields):
        key = 'n' + str(len(nodes))
        nodes.append({'id': key, 'op': op, **fields})
        return key
    def val(v, **source):
        return node('VALUE', value=str(v), source={'authority_sha256': source_hash, **source})
    two, three = val(2, role='pair multiplicity'), val(3, role='trace dimension')
    outputs = []
    for index, stencil in enumerate(unique):
        q = []
        for offset, (x, y) in enumerate(stencil):
            xx = val(x, stencil=index, offset=offset, coordinate='x_plus')
            yy = val(y, stencil=index, offset=offset, coordinate='y_plus')
            x2 = node('MULTIPLY', left=xx, right=xx)
            y2 = node('MULTIPLY', left=yy, right=yy)
            r2 = node('ADD', left=x2, right=y2)
            trace = node('DIVIDE', left=r2, right=three)
            qxx = node('MULTIPLY', left=two, right=node('SUBTRACT', left=x2, right=trace))
            qyy = node('MULTIPLY', left=two, right=node('SUBTRACT', left=y2, right=trace))
            q.append(node('SUBTRACT', left=qxx, right=qyy))
        center = node('MULTIPLY', left=two, right=q[1])
        out = node('SUBTRACT', left=node('ADD', left=q[0], right=q[2]), right=center)
        outputs.append((stencil, out))
    result = session.execute('GEN2_SIGNED_LOG', {'nodes': nodes, 'representation': 'RATIONAL'},
        purpose='GW-COM source adapter: H000733 antipodal-pair trace-free quadrupole and signed second difference for every distinct controlled-orbit stencil; exact reuse across repeated source positions.')
    assert result['complete']
    lookup = {row['id']: F(row['value']) for row in result['nodes']}
    for stencil, key in outputs:
        values[stencil] = lookup[key]
        assert values[stencil] == independent(stencil), 'Independent quadrupole reconstruction mismatch'
    return values, {'operation': 'GEN2_SIGNED_LOG', 'unique_stencils': len(unique),
                    'native_nodes': len(nodes), 'checkpoint_sha256': result['checkpoint']['sha256']}


def channel(wave, delay=37, gain=1., noise=0., seed=1):
    rng = random.Random(seed)
    # Carrier-only lead-in; no start timestamps travel to the receiver.
    lead = [8. * (-1)**i for i in range(delay)]
    return [gain * (v + rng.gauss(0, noise)) for v in lead + [float(x) for x in wave]]


def main():
    release = HERE / 'release'
    release.mkdir(exist_ok=False)
    source_hash = hashlib.sha256((ROOT / SOURCE).read_bytes()).hexdigest()
    cases = {'prime': (MESSAGE, True), 'unmodulated': (MESSAGE, False),
             'alternate': ([4, 6, 8, 10, 12, 14], True)}
    sources = {name: positions(message, active) for name, (message, active) in cases.items()}
    stencils = {name: [tuple(xy[i-1:i+2]) for i in range(1, len(xy)-1)]
                for name, (xy, _, _) in sources.items()}
    with DomainSession.start('STARBREAKER', objective='GW-COM interval-only orbit-wave transmission and waveform-only decoding',
                             output_root=HERE/'sessions', receipt_storage='gzip') as session:
        print(session.announcement(), flush=True)
        values, native = native_stencils(session, [s for seq in stencils.values() for s in seq], source_hash)
        session_path = str(session.directory.relative_to(ROOT))
    waves = {name: [values[s] for s in seq] for name, seq in stencils.items()}
    decoded = {}
    for name, wave in waves.items():
        samples = channel(wave)
        write(release / (name + '_receiver_input.json'), {'wave_samples': samples})
        decoded[name] = decode(samples)
    assert [p['intervals'] for p in decoded['prime']['packets']] == [MESSAGE, MESSAGE]
    assert decoded['unmodulated']['packets'] == []
    alternate = cases['alternate'][0]
    assert [p['intervals'] for p in decoded['alternate']['packets']] == [alternate, alternate]
    trials = []
    for seed in range(20):
        delay = 7 + seed * 3
        gain = (.25, 1., 4.)[seed % 3]
        samples = channel(waves['prime'], delay, gain, .04, seed)
        recovery = decode(samples)
        recovered = [p['intervals'] for p in recovery['packets']]
        trials.append({'seed': seed, 'delay_samples': delay, 'gain': gain,
                       'noise_sigma_before_gain': .04, 'recovered': recovered,
                       'exact_two_packet_recovery': recovered == [MESSAGE, MESSAGE]})
    # Each output row binds sampled positions to the reused native stencil.
    with (release/'source_wave.csv').open('w', newline='') as f:
        out = csv.writer(f)
        out.writerow(['sample','x_plus','y_plus','radius','signed_quadrupole_second_difference'])
        xy, events, radii = sources['prime']
        for i, v in enumerate(waves['prime'], 1):
            out.writerow([i, str(xy[i][0]), str(xy[i][1]), str(radii[i]), str(v)])
    write(release/'transmitter.json', {'message': MESSAGE, 'unit_ticks': UNIT,
        'marker_centers': sources['prime'][1], 'radial_profile_over_128': PROFILE,
        'antipodal_unit_weight_bodies': True, 'prescribed_motion': True})
    result = {'classification': 'The test result suggests the concept is possible.',
        'scope': 'Dimensionless sampled C4 antipodal orbit with prescribed equal radial markers and ideal delayed scalar readout; no SI strain, actuator dynamics or physical propagation calibration.',
        'session': session_path, 'native': native, 'source': SOURCE, 'source_sha256': source_hash,
        'decoded': decoded, 'noise_trials': trials,
        'noise_trials_recovered': sum(t['exact_two_packet_recovery'] for t in trials),
        'noise_trials_total': len(trials), 'independent_exact_stencil_checks': native['unique_stencils']}
    write(release/'RESULT.json', result)
    manifest = {str(p.relative_to(ROOT)): hashlib.sha256(p.read_bytes()).hexdigest()
                for p in [HERE/'run.py', HERE/'receiver.py', ROOT/SOURCE, *sorted(release.iterdir())] if p.is_file()}
    write(release/'MANIFEST.json', manifest)
    print(json.dumps({'session': session_path, 'native': native, 'prime_recovered': decoded['prime'],
                      'noise_recovered': result['noise_trials_recovered'], 'noise_total': len(trials)}, indent=2))


if __name__ == '__main__':
    main()
