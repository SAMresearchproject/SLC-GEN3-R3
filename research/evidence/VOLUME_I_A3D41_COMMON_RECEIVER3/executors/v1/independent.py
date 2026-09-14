#!/usr/bin/env python3
"""Independent Gaussian-integer forward model and exhaustive conditional inverse.

Imports custody/serialization only. No primary, reception or predecessor math.
"""
import argparse
from collections import defaultdict
import hashlib
from itertools import permutations, product
import json

from custody import CAMPAIGN, fail, ledger_rows, manifest, preflight, read, run_directory, save, utc, verify_outputs

LABELS = ('N100_EDGE_002', 'N100_EDGE_006', 'N100_EDGE_084')
KINDS = ('SIGNED_PHASE', 'AXIS_OCCUPANCY')
VIEWS = ('JOINT', 'SIGNED', 'OCCUPANCY', 'ENDPOINTS', 'WRONG_POST_ABS')
WORDS = tuple(permutations(range(3)))
PHASES = tuple(product(range(4), repeat=3))
G = ((2, 0, -1), (0, 2, 1), (-1, 1, 2))


def check(ok, message):
    if not ok:
        raise ValueError(message)


def mul(z, w):
    return (z[0]*w[0]-z[1]*w[1], z[0]*w[1]+z[1]*w[0])


def phase(q):
    value = (1, 0)
    for _ in range(q % 4):
        value = mul(value, (0, 1))
    return value


def decode_address(a):
    return tuple((a // 2**j) % 2 + 2*((a // 2**(j+9)) % 2) for j in (1, 4, 7))


def frame(q, bases):
    coefficients = [phase(x) for x in q]
    result = {}
    for name in KINDS:
        values = []
        for k in range(8):
            terms = [mul(tuple(abs(x) for x in z) if name == KINDS[1] else z, bases[j][k])
                     for j, z in enumerate(coefficients)]
            values.extend(sum(p[axis] for p in terms) for axis in range(2))
        result[name] = values
    return result


def path(initial, direction, word):
    return [tuple((initial[j]+direction*(j in word[:n])) % 4 for j in range(3)) for n in range(4)]


def answer(initial, direction, word):
    states = path(initial, direction, word)
    h = []
    for q in states:
        z = [phase(x) for x in q]
        h.append(sum(G[i][j]*(z[i][0]*z[j][0]+z[i][1]*z[j][1])
                     for i in range(3) for j in range(3)))
    return {'order': list(word), 'phase_path': [list(q) for q in states],
            'contact_profile': h, 'barrier': max(h)-h[0]}


def view(observations, kind):
    s = tuple(v for f in observations for v in f[KINDS[0]])
    u = tuple(v for f in observations for v in f[KINDS[1]])
    if kind == 'SIGNED':
        return s
    if kind == 'OCCUPANCY':
        return u
    if kind == 'ENDPOINTS':
        return tuple(observations[0][KINDS[0]]+observations[0][KINDS[1]]+
                     observations[3][KINDS[0]]+observations[3][KINDS[1]])
    if kind == 'WRONG_POST_ABS':
        return s+tuple(abs(x) for x in s)
    check(kind == 'JOINT', 'Unknown view')
    return s+u


def empty_metrics():
    return {v: dict(classes=0, singleton_orders=0, ambiguous_orders=0,
                    barrier_resolved_orders=0, mixed_barrier_classes=0) for v in VIEWS}


def accumulate(target, keys, models):
    unseen = set(range(6))
    while unseen:
        i = min(unseen)
        same = {j for j in unseen if keys[j] == keys[i]}
        unseen -= same
        target['classes'] += 1
        target['singleton_orders' if len(same) == 1 else 'ambiguous_orders'] += len(same)
        if len({models[j]['barrier'] for j in same}) == 1:
            target['barrier_resolved_orders'] += len(same)
        else:
            target['mixed_barrier_classes'] += 1


def native_check(folder, source):
    seen = set()
    for row in ledger_rows(folder/'NATIVE_WORD_RECEIPTS.jsonl.gz'):
        sid, r = row['source_id'], row['receipt']
        check(sid in source and sid not in seen, 'Wrong native source receipt')
        seen.add(sid)
        body = {k: v for k, v in r.items() if k != 'semantic_sha256'}
        raw = json.dumps(body, sort_keys=True, separators=(',', ':'), ensure_ascii=False, allow_nan=False).encode()+b'\n'
        check(hashlib.sha256(raw).hexdigest() == r['semantic_sha256'], 'Native receipt hash differs')
        truth = source[sid]
        check(r['schema'] == 'SLC_T18_RETAINED_WORD_V1', 'Wrong native schema')
        check(r['source_endpoint'] != r['target_endpoint'], 'Native endpoints merged')
        check(r['trajectory'] == truth['trajectory'], 'Native/source trajectory differs')
        states = path(truth['initial_phases'], truth['orientation'], truth['order'])
        check(list(map(decode_address, r['trajectory'])) == states, 'Native coordinates differ')
        check(len(r['directed_history']) == 3, 'Incomplete native Write word')
        for n, event in enumerate(r['directed_history']):
            check(event == {'record_index': (1, 4, 7)[truth['order'][n]], 'orientation': truth['orientation'],
                            'address_before': r['trajectory'][n], 'address_after': r['trajectory'][n+1],
                            'retained_W8_shell_state': 0}, 'Native Write correspondence differs')
    check(len(seen) == 768, 'Incomplete native receipts')
    return len(seen)


def verify(run_id):
    out = run_directory(run_id, independent=True)
    folder = out.parent
    save(out/'START.json', {'started_utc': utc(), 'stage': 'INDEPENDENT_STARTED'})
    try:
        custody = preflight()
        output_files = verify_outputs(folder, 'PRIMARY_MANIFEST.json')
        src = read(CAMPAIGN/'inputs/A3D41_R2_INSTALLED_RESULT.json')['history_results']
        source = {r['id']: r for r in src}
        truth = {(tuple(r['initial_phases']), r['orientation'], tuple(r['order'])): r for r in src}
        check(len(source) == len(truth) == 768, 'Source roster differs')
        native_count = native_check(folder, source)
        bases = {}
        for line in (CAMPAIGN/'inputs/J4_PRE_GRAM_RESPONSE_HISTORIES.jsonl').read_text().splitlines():
            r = json.loads(line)
            if r['relation_id'] in LABELS:
                bases[(r['rho'], r['relation_id'])] = r['forward_amplitude']+r['reverse_amplitude']
        records = iter(ledger_rows(folder/'RECEPTION_INVERSE.jsonl.gz'))
        total, per_rho, certificates = empty_metrics(), [], []
        controls = defaultdict(int)
        count = exact = 0
        for rho in range(1, 129):
            b = [bases[(rho, name)] for name in LABELS]
            check(all(tuple(b[2][k]) == tuple(-v for v in b[1][k]) for k in range(8)), 'Template sign identity differs')
            table = {q: frame(q, b) for q in PHASES}
            product1, product2 = mul(b[0][0], b[1][4]), mul(b[1][0], b[0][4])
            det = [product1[k]-product2[k] for k in range(2)]
            distinguishable = 0
            for q in PHASES:
                for d in (-1, 1):
                    increments = []
                    for j in range(3):
                        q2 = tuple((v+d*(i == j)) % 4 for i, v in enumerate(q))
                        increments.append(tuple(table[q2][name][k]-table[q][name][k]
                                                for name in KINDS for k in range(16)))
                    distinguishable += all(increments[j] != increments[k] for j in range(3) for k in range(j))
            certificates.append({'rho': rho, 'opposite_template_equalities': 16,
                'minor_rows': ['forward:0', 'reverse:0'], 'complex_minor': det,
                'minor_nonzero': det != [0, 0], 'state_direction_cases': 128,
                'three_distinct_next_writes': distinguishable})
            controls['both_source_projections'] += 64
            local = empty_metrics()
            for q in PHASES:
                for d in (-1, 1):
                    signals = [[table[p] for p in path(q, d, w)] for w in WORDS]
                    keys = {v: [view(sig, v) for sig in signals] for v in VIEWS}
                    models = [answer(q, d, w) for w in WORDS]
                    for v in VIEWS:
                        for target in (local, total):
                            accumulate(target[v], keys[v], models)
                    for i, word in enumerate(WORDS):
                        record = next(records)
                        condition = {'initial_phases': list(q), 'orientation': d, 'rho': rho}
                        check(record['conditions'] == condition, 'Receiver record conditions differ')
                        observations = record['observations']
                        check(len(observations) == 4 and all(set(f) == set(KINDS) and
                            all(len(f[name]) == 16 and all(type(x) is int for x in f[name]) for name in KINDS)
                            for f in observations), 'Receiver observations have extra fields or wrong shape')
                        check(observations == signals[i], 'Independently computed common reception differs')
                        match = {v: [j for j in range(6) if keys[v][j] == view(observations, v)] for v in VIEWS}
                        expected = [models[j] for j in match['JOINT']]
                        check(record['inverse'] == expected, 'Independent exhaustive inverse differs')
                        check(record['view_candidates'] == {v: [list(WORDS[j]) for j in match[v]] for v in VIEWS},
                              'Control inverse differs')
                        exact += expected == [models[i]]
                        t = truth[(q, d, word)]
                        check(record['truth'] == {'id': t['id'], 'order': list(word),
                              'barrier': t['readouts']['NATIVE_SIGNED_PHASE']['barrier']}, 'Source truth differs')
                        check(models[i]['barrier'] == record['truth']['barrier'] and
                              [v-models[i]['contact_profile'][0] for v in models[i]['contact_profile']] ==
                              t['readouts']['NATIVE_SIGNED_PHASE']['prefix_deltas'], 'Contact barrier differs')
                        # Relabeling truth cannot enter this inverse: only observations/conditions were used above.
                        shifted = [{KINDS[0]: f[KINDS[0]], KINDS[1]: observations[(n+1) % 4][KINDS[1]]}
                                   for n, f in enumerate(observations)]
                        wrong = [models[j] for j in range(6) if view(shifted, 'JOINT') == keys['JOINT'][j]]
                        check(wrong == record['wrong_alignment_inverse'], 'Misalignment control differs')
                        controls['misaligned_total'] += 1
                        controls['misaligned_accepted' if wrong else 'misaligned_rejected'] += 1
                        controls['misaligned_wrong_singleton'] += bool(len(wrong) == 1 and wrong[0]['order'] != list(word))
                        q_end = path(q, d, word)[-1]
                        reverse_word = tuple(reversed(word))
                        check([table[p] for p in path(q_end, -d, reverse_word)] == observations[::-1],
                              'Native reverse source word differs')
                        controls['native_word_reversal'] += 1
                        count += 1
            per_rho.append({'rho': rho, 'views': local})
            if rho % 32 == 0:
                print(f'independent rho={rho}/128 histories={count}', flush=True)
        check(next(records, None) is None, 'Extra receiver records')
        check(count == 98304, 'Incomplete independent census')
        summary = read(folder/'SUMMARY.json')
        check(summary['views'] == total and read(folder/'PER_RHO.json') == per_rho, 'Partition metrics differ')
        check(read(folder/'INJECTIVITY_CERTIFICATE.json') == certificates, 'Injectivity certificate differs')
        check(summary['controls'] == dict(controls), 'Control totals differ')
        check(summary['exact_order_and_barrier_inverses'] == exact and
              summary['joined_histories'] == count and summary['common_reception_frames'] == count*4 and
              summary['observed_scalar_values'] == count*128, 'Census totals differ')
        check(summary['local_injectivity_cases_passed'] == sum(x['three_distinct_next_writes'] for x in certificates)
              and summary['nonzero_minors'] == sum(x['minor_nonzero'] for x in certificates), 'Certificate totals differ')
        classification = ('The test result suggests strong contact with the concept.' if exact == count else
                          'The test result suggests the concept is possible.' if total['JOINT']['classes'] > 16384 else
                          'The test falsifies the concept.')
        check(summary['classification'] == classification, 'Classification differs')
        save(out/'VERIFICATION.json', {'status': 'PASS', 'classification': classification, 'finished_utc': utc(),
             'custody': custody, 'primary_output_files_verified': output_files,
             'native_word_receipts_verified': native_count, 'receiver_histories_verified': count,
             'receiver_scalar_values_verified': count*128, 'independent_exact_inverses': exact,
             'per_rho_and_control_metrics': 'MATCH', 'injectivity_certificates': 'MATCH',
             'independent_algorithm': 'Gaussian integer forward law; exhaustive six-word inverse',
             'primary_or_predecessor_mathematics_imported': False})
        manifest(out, 'INDEPENDENT_MANIFEST.json')
        print('Independent reconstruction PASS', flush=True)
    except BaseException as error:
        fail(out, error, 'INDEPENDENT_MANIFEST.json')
        raise


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--run-id', required=True)
    verify(parser.parse_args().run_id)
