#!/usr/bin/env python3
"""Check the short exact derivation against the retained sixteen histories."""
from fractions import Fraction as F
import json
from pathlib import Path
import numpy as np

HERE = Path(__file__).resolve().parent


def main():
    geometry = json.loads((HERE / 'GEOMETRY.json').read_text())
    bits = np.load(HERE / 'MINIMUM_BITSETS.npz')['sets']
    selected = np.flatnonzero(np.unpackbits(bits[43], bitorder='little')[:262144])
    rows = []
    for state in selected:
        q = np.array([((int(state) >> e) & 1) + 2 * ((int(state) >> (e + 9)) & 1)
                      for e in range(9)])
        z = np.array([1, 1j, -1, -1j])[q]
        t, alpha = z[0], z[8]
        assert np.array_equal(z, [t, t, -t, -t, -t, t, t, t, alpha])
        j = np.array(geometry['site_incidence']) @ z
        assert np.array_equal(j, [0, 0, 0, 0, -alpha, alpha])
        cycle_norms = (np.abs(np.array(geometry['cycle_incidence']) @ z) ** 2).astype(int)
        assert cycle_norms.tolist() == [9, 9, 1, 1, 4]
        exposure = [int(abs(j[u] - j[v]) ** 2) for u, v in geometry['endpoints']]
        assert sum(exposure) == 8
        for cover in geometry['covers'][3:]:
            pair_sum = sum(exposure[e] for e in cover['pair_edges'])
            assert pair_sum == 2
            triad = F(int(cycle_norms[cover['triads'][0]]), 3)
            lift = F(9, 16) * F(int(cycle_norms[4]), 4)
            assert F(43, 4) * pair_sum + 72 * triad + lift == F(737, 16)
            assert 12 * pair_sum + 108 * triad + lift == F(969, 16)
        rows.append({'state': int(state), 'common_phase': int(q[0]), 'exterior_phase': int(q[8])})
    assert len(rows) == 16
    assert len({(r['common_phase'], r['exterior_phase']) for r in rows}) == 16
    result = {'status': 'PASS', 'states': rows,
              'selection': 'four common phases times four exterior phases',
              'observed_source_action': '737/16', 'native_source_action': '969/16',
              'hidden_lift_action': '9/16', 'source_unit': 'CANDIDATE_SOURCE_ACTION'}
    (HERE / 'SELECTION_DERIVATION.json').write_text(json.dumps(result, sort_keys=True, indent=2) + '\n')
    print(json.dumps({'status': 'PASS', 'exact_selected_histories': len(rows)}))


if __name__ == '__main__':
    main()
