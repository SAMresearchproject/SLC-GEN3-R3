"""Candidate decoding requires explicit, matching physical/statistical evidence."""
from fractions import Fraction as F


LINEAGE = ('raw_waveform','source_fit','residual_history','candidate_symbolization','information_tests')


def verify_control_evidence(store, value):
    if isinstance(value,dict) and {'path','sha256'}<=value.keys():
        store.verify(value)
        return 1
    if isinstance(value,dict):
        return sum(verify_control_evidence(store,v) for v in value.values())
    if isinstance(value,list):
        return sum(verify_control_evidence(store,v) for v in value)
    return 0


def parents_by_kind(store, ref):
    pairs = [(store.read(p)['kind'],p) for p in store.read(ref)['parent_refs']]
    if len({k for k,_ in pairs}) != len(pairs):
        raise ValueError('Ambiguous same-kind parents')
    return dict(pairs)


def check_lineage(store, refs, controls):
    if set(refs)!=set(LINEAGE):
        raise ValueError('Incomplete lineage')
    for kind,ref in refs.items():
        store.verify(ref)
        if store.read(ref)['kind']!=kind or store.read(ref)['status']!='COMPLETE':
            raise ValueError('Incorrect or incomplete stage')
    expected = {'source_fit':['raw_waveform'],
                'residual_history':['raw_waveform','source_fit'],
                'candidate_symbolization':['residual_history'],
                'information_tests':['candidate_symbolization','residual_history']}
    for kind, dependencies in expected.items():
        parents=parents_by_kind(store,refs[kind])
        if any(parents.get(d)!=refs[d] for d in dependencies):
            raise ValueError('Lineage changed: '+kind)
    store.verify(controls)
    if store.read(controls)['kind']!='control_results' or store.read(controls)['status']!='COMPLETE':
        raise ValueError('Missing or incomplete control results')
    if parents_by_kind(store,controls)!=refs:
        raise ValueError('Controls refer to another candidate lineage')
    data=store.payload(controls)
    for family in ('physical_controls','statistical_controls'):
        for row in data.get(family,[]):
            if not verify_control_evidence(store,row.get('evidence')):
                raise ValueError('Individual control evidence is missing')


def admission(store, name, refs, controls):
    check_lineage(store,refs,controls)
    results = store.payload(controls)
    dispositions = {}
    for family in ('physical_controls','statistical_controls'):
        rows = results.get(family,[])
        dispositions[family] = 'PASS' if rows and all(r.get('status')=='PASS' for r in rows) else 'FAIL'
    eligible = all(v=='PASS' for v in dispositions.values())
    # Recheck the declared statistical criterion from retained test values.
    test = store.payload(refs['information_tests'])
    if test.get('observed_repetition',0)<2 or F(test.get('permutation_p','1'))>F(1,20):
        eligible=False
        dispositions['statistical_controls']='FAIL'
    return store.record(name,'decoder_admission',{'eligible':eligible,'dispositions':dispositions,
        'lineage':refs,'controls':controls,'criteria':'CONTRACT.json via method_ref'},
        parents=[*refs.values(),controls])


def decode(store, name, admitted):
    store.verify(admitted)
    if store.read(admitted)['kind']!='decoder_admission' or store.read(admitted)['status']!='COMPLETE':
        raise ValueError('Decoder admission record required')
    gate=store.payload(admitted)
    if not gate['eligible'] or any(gate['dispositions'].get(k)!='PASS'
                                  for k in ('physical_controls','statistical_controls')):
        raise ValueError('Candidate is not admitted for decoding')
    refs,controls=gate['lineage'],gate['controls']
    check_lineage(store,refs,controls)
    control_data=store.payload(controls)
    for family in ('physical_controls','statistical_controls'):
        rows=control_data.get(family,[])
        if not rows or any(r.get('status')!='PASS' for r in rows):
            raise ValueError('Unpassed control evidence')
    tests=store.payload(refs['information_tests'])
    if tests['observed_repetition']<2 or F(tests['permutation_p'])>F(1,20):
        raise ValueError('Statistical criteria not met')
    symbols=store.payload(refs['candidate_symbolization'])
    hypotheses=[]
    for group in symbols['repetition_groups']:
        if len(group['frame_indices'])<2:
            continue
        frames=[symbols['frames'][i] for i in group['frame_indices']]
        hypotheses.append({'interval_integers':group['bins'], 'frame_indices':group['frame_indices'],
            'support':[{'raw_sample_spans':f['sample_spans'],'unit_samples':f['unit_samples'],
                        'symbols':f['symbols']} for f in frames],
            'interpretation':'integers encoded as timing intervals; intent not assigned',
            'corrections':[],'unresolved_symbols':[]})
    return store.record(name,'decoded_hypothesis',{'hypotheses':hypotheses,
        'all_frame_alternatives':symbols['frames'],'grammar':'integer timing intervals after four synchronization markers',
        'raw_waveform_ref':refs['raw_waveform']},parents=[admitted,refs['candidate_symbolization']])
