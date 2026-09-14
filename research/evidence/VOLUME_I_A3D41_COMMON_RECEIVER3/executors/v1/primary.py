#!/usr/bin/env python3
"""Common receiver census using managed native T18 source events."""
import argparse
from collections import defaultdict
from itertools import permutations, product
import importlib.util
import sys

from custody import CAMPAIGN, PROJECT, fail, ledger, manifest, preflight, read, run_directory, save, sha, utc
from reception import (CHANNELS, LANES, PHASE, RELATIONS, SLOTS, VIEWS, CurrentReception,
                       Frame, common_reception, contact, difference, encode, inverse,
                       phase_path, recovered, require, signature, source_lift)

STATES = tuple(product(range(4), repeat=3))
WORDS = tuple(permutations(range(3)))


def templates_by_rho():
    rows = {}
    for line in (CAMPAIGN/'inputs/J4_PRE_GRAM_RESPONSE_HISTORIES.jsonl').read_text().splitlines():
        import json
        r = json.loads(line)
        if r['relation_id'] in RELATIONS:
            key = (r['rho'], r['relation_id'])
            require(key not in rows and r['selected_packet_relation'] is True, 'Invalid J4 relation')
            rows[key] = {c: r[c] for c in CHANNELS}
    require(set(rows) == set(product(range(1, 129), RELATIONS)), 'Incomplete J4 calibration')
    return rows


def native_sources(folder):
    sys.path.insert(0, str(PROJECT))
    from CURRENT_REVISION import open_domain
    from CURRENT_REVISION.domains.ATOM3D.native_contact import lift
    domain = open_domain('ATOM3D')
    packet = domain.build_campaign()
    require(packet['domain_revision'] == 'A3D41-T18-CONTACT-R2', 'Wrong current contact source')
    require(packet['contact_contract_sha256'] == sha(CAMPAIGN/'inputs/A3D41_CONTACT_CONTRACT.json'),
            'Current contact contract differs from frozen source')
    h_by_q = {}
    for q in STATES:
        h = tuple(lift(encode(q), 'NATIVE_SIGNED_PHASE'))
        require(h == source_lift(q), 'Signed lift correspondence failed')
        require(tuple(map(abs, h)) == tuple(lift(encode(q), 'UNSIGNED_OCCUPANCY')), 'Occupancy lift differs')
        h_by_q[q] = h
    raw = read(CAMPAIGN/'inputs/A3D41_R2_INSTALLED_RESULT.json')
    families = defaultdict(dict)
    count = 0
    with ledger(folder/'NATIVE_WORD_RECEIPTS.jsonl.gz') as write:
        for row in raw['history_results']:
            q, d, word = tuple(row['initial_phases']), row['orientation'], tuple(row['order'])
            require(q in STATES and d in (-1, 1) and word in WORDS, 'Invalid source family')
            require(word not in families[(q, d)], 'Duplicate source order')
            receipt = domain.execute('T18_WORD', {'address': row['trajectory'][0],
                'writes': [[SLOTS[j], d] for j in word], 'source_endpoint': 'SOURCE_EVENT_PORT',
                'target_endpoint': 'RECEPTION_EVENT_PORT', 'shell_state': 0})
            # Endpoint names denote algebraic ports, not physical site coordinates.
            require(receipt['trajectory'] == row['trajectory'], 'Current native source correspondence failed')
            states = phase_path(q, d, word)
            require([encode(p) for p in states] == receipt['trajectory'], 'Phase/address correspondence failed')
            rec = recovered(q, d, word)
            truth = row['readouts']['NATIVE_SIGNED_PHASE']
            require(rec['barrier'] == truth['barrier'] and
                    [v-rec['contact_profile'][0] for v in rec['contact_profile']] == truth['prefix_deltas'],
                    'Inherited contact correspondence differs')
            families[(q, d)][word] = row
            write({'source_id': row['id'], 'receipt': receipt})
            count += 1
    require(count == 768 and len(families) == 128 and all(set(v) == set(WORDS) for v in families.values()),
            'Incomplete native source roster')
    save(folder/'NATIVE_BINDING.json', {'source_revision': packet['domain_revision'],
        'native_words_executed': count, 'native_writes_executed': 3*count,
        'signed_and_occupancy_lift_states': len(h_by_q),
        'entrypoint': 'CURRENT_REVISION.open_domain(ATOM3D).execute(T18_WORD)',
        'source_endpoint_and_target_endpoint': 'distinct algebraic ports; physical sites unassigned',
        'current_policy': domain.policy, 'packet_contact_contract_sha256': packet['contact_contract_sha256'],
        'current_t18_sha256': sha(PROJECT/'CURRENT_REVISION/engines/SLC/native/t18.py'),
        'current_ce_sha256': sha(PROJECT/'CURRENT_REVISION/engines/CE/cev1_hfm5_current.py'),
        'current_lift_sha256': sha(PROJECT/'CURRENT_REVISION/domains/ATOM3D/native_contact.py'),
        'prior_gpu_source_reused': True, 'new_gpu_contact_run': False})
    return families, h_by_q


def predecessor_reference():
    p = CAMPAIGN/'inputs/PREDECESSOR_MAP.py'
    spec = importlib.util.spec_from_file_location('frozen_predecessor_map', p)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def multiply(a, b):
    return (a[0]*b[0]-a[1]*b[1], a[0]*b[1]+a[1]*b[0])


def certificate(rho, t, table):
    a, b, c = (t[r] for r in RELATIONS)
    require(all(c[ch][k] == [-v for v in b[ch][k]] for ch in CHANNELS for k in range(4)),
            'Opposite-template identity failed')
    ab = multiply(a[CHANNELS[0]][0], b[CHANNELS[1]][0])
    ba = multiply(b[CHANNELS[0]][0], a[CHANNELS[1]][0])
    det = [ab[j]-ba[j] for j in (0, 1)]
    distinct = 0
    for q in STATES:
        for d in (-1, 1):
            changes = [difference(table[phase_path(q, d, (j,))[-1]], table[q]) for j in range(3)]
            distinct += len(set(changes)) == 3
    return {'rho': rho, 'opposite_template_equalities': 16, 'minor_rows': ['forward:0', 'reverse:0'],
            'complex_minor': det, 'minor_nonzero': det != [0, 0],
            'state_direction_cases': 128, 'three_distinct_next_writes': distinct}


def metrics():
    return {v: {'classes': 0, 'singleton_orders': 0, 'ambiguous_orders': 0,
                'barrier_resolved_orders': 0, 'mixed_barrier_classes': 0} for v in VIEWS}


def add_metrics(target, groups, models):
    target['classes'] += len(groups)
    for members in groups.values():
        n = len(members)
        target['singleton_orders' if n == 1 else 'ambiguous_orders'] += n
        bs = {models[i]['barrier'] for i in members}
        if len(bs) == 1:
            target['barrier_resolved_orders'] += n
        else:
            target['mixed_barrier_classes'] += 1


def run(run_id):
    folder = run_directory(run_id)
    save(folder/'START.json', {'started_utc': utc(), 'stage': 'PRIMARY_STARTED'})
    try:
        save(folder/'PREFLIGHT.json', preflight())
        families, lifts = native_sources(folder)
        all_t, reference = templates_by_rho(), predecessor_reference()
        total, per_rho, certificates = metrics(), [], []
        controls = defaultdict(int)
        decoded_exact = 0
        current = CurrentReception()
        count = 0
        with ledger(folder/'RECEPTION_INVERSE.jsonl.gz') as write:
            for rho in range(1, 129):
                t = {r: all_t[(rho, r)] for r in RELATIONS}
                table = {q: common_reception(lifts[q], t) for q in STATES}
                for q, frame in table.items():
                    require(frame.signed == reference.response_at(encode(q), t), 'Signed source map changed')
                    require(frame.occupancy == reference.response_at(encode(q), t, erase_source_sign=True),
                            'Occupancy source map changed')
                    controls['both_source_projections'] += 1
                certificates.append(certificate(rho, t, table))
                local = metrics()
                phase_at_native_address = {encode(q): q for q in STATES}
                for (q, d), source in sorted(families.items()):
                    paths = [tuple(phase_at_native_address[a] for a in source[w]['trajectory']) for w in WORDS]
                    received = []
                    for path in paths:
                        received.append(tuple(current.receive(table[p].payload()) for p in path))
                    models = [recovered(q, d, w) for w in WORDS]
                    groups = {}
                    for view in VIEWS:
                        group = defaultdict(list)
                        for i, frames in enumerate(received):
                            group[signature(frames, view)].append(i)
                        groups[view] = group
                        for target in (local, total):
                            add_metrics(target[view], group, models)
                    for i, frames in enumerate(received):
                        answers = inverse(q, d, frames, table)
                        candidates = {view: [list(WORDS[j]) for j in groups[view][signature(frames, view)]]
                                      for view in VIEWS}
                        require([a['order'] for a in answers] == candidates['JOINT'], 'Stepwise inverse differs from legal words')
                        exact = answers == [models[i]]
                        decoded_exact += exact
                        reversed_answers = inverse(paths[i][-1], -d, tuple(reversed(frames)), table)
                        require(reversed_answers == [recovered(paths[i][-1], -d, tuple(reversed(WORDS[i])))],
                                'Reversed native word did not reconstruct')
                        controls['native_word_reversal'] += 1
                        shifted = tuple(Frame(f.signed, frames[(n+1) % 4].occupancy) for n, f in enumerate(frames))
                        wrong = inverse(q, d, shifted, table)
                        controls['misaligned_total'] += 1
                        controls['misaligned_accepted' if wrong else 'misaligned_rejected'] += 1
                        controls['misaligned_wrong_singleton'] += bool(len(wrong) == 1 and wrong[0]['order'] != list(WORDS[i]))
                        # Source truth is introduced only after reception and decoding.
                        truth = source[WORDS[i]]
                        write({'conditions': {'initial_phases': list(q), 'orientation': d, 'rho': rho},
                               'observations': [f.payload() for f in frames], 'inverse': answers,
                               'view_candidates': candidates,
                               'wrong_alignment_inverse': wrong,
                               'truth': {'id': truth['id'], 'order': list(WORDS[i]),
                                         'barrier': truth['readouts']['NATIVE_SIGNED_PHASE']['barrier']}})
                        count += 1
                per_rho.append({'rho': rho, 'views': local})
                if rho % 32 == 0:
                    print(f'reception rho={rho}/128 histories={count}', flush=True)
        require(count == 98304, 'Incomplete common-reception census')
        if decoded_exact == count:
            classification = 'The test result suggests strong contact with the concept.'
        elif total['JOINT']['classes'] > 16384:
            classification = 'The test result suggests the concept is possible.'
        else:
            classification = 'The test falsifies the concept.'
        summary = {'status': 'COMPLETE', 'classification': classification,
                   'joined_histories': count, 'comparison_families': 16384,
                   'exact_order_and_barrier_inverses': decoded_exact,
                   'common_reception_frames': count*4, 'observed_scalar_values': count*128,
                   'views': total, 'controls': dict(controls),
                   'local_injectivity_state_direction_cases': sum(x['state_direction_cases'] for x in certificates),
                   'local_injectivity_cases_passed': sum(x['three_distinct_next_writes'] for x in certificates),
                   'nonzero_minors': sum(x['minor_nonzero'] for x in certificates),
                   'finished_utc': utc()}
        save(folder/'SUMMARY.json', summary)
        save(folder/'PER_RHO.json', per_rho)
        save(folder/'INJECTIVITY_CERTIFICATE.json', certificates)
        manifest(folder, 'PRIMARY_MANIFEST.json')
        print(classification, flush=True)
    except BaseException as error:
        fail(folder, error, 'PRIMARY_MANIFEST.json')
        raise


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--run-id', required=True)
    run(parser.parse_args().run_id)
