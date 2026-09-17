"""Independent exact reconstruction and saved-run custody checks."""
from fractions import Fraction as F
import json
from pathlib import Path
import sys

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[2]
sys.path.insert(0,str(ROOT))
from GW_COM.runtime.evidence import Store


def main():
    run=HERE/(sys.argv[1] if len(sys.argv)>1 else 'run001')
    store=Store(ROOT,run/'records',run/'METHOD.json')
    result=json.loads((run/'records/RUN_RESULT.json').read_text())
    reconstructed=0
    normal_equations=0
    records=0
    for path in sorted(store.directory.glob('*.json')):
        record=json.loads(path.read_text())
        if record.get('schema')!='GW_COM_EVIDENCE_V1':continue
        ref=store.ref(path);store.verify(ref);records+=1
        data=store.payload(ref)
        if record['kind']=='source_history':
            xy=[tuple(map(F,p)) for p in data['positions']]
            q=[2*(x*x-y*y) for x,y in xy]
            actual=[F(v) for v in data['signed_source_wave']]
            assert actual==[q[i-1]-2*q[i]+q[i+1] for i in range(1,len(q)-1)]
            reconstructed+=len(actual)
        if record['kind']=='residual_history':
            parents={store.read(r)['kind']:r for r in record['parent_refs']}
            raw=store.payload(parents['raw_waveform'])
            fit=store.payload(parents['source_fit'])
            r=list(map(F,data['signed_samples']))
            y=list(map(F,raw['samples']))
            predicted=list(map(F,fit['predicted_samples']))
            assert all(a-b==c for a,b,c in zip(y,predicted,r))
            coeff=list(map(F,fit['coefficients']))
            xs=[[(F(-1)**i),F(1),F(i,128)*((-1)**i)][:len(coeff)] for i in range(len(y))]
            assert predicted==[sum(c*x for c,x in zip(coeff,row)) for row in xs]
            for j in range(len(coeff)):
                assert sum(xs[i][j]*r[i] for i in range(128))==0
                normal_equations+=1
            assert data['raw_sample_indices']==list(range(len(y)))
            reconstructed+=len(r)
        if record['kind']=='information_tests':
            exceed=sum(row['repetition_count']>=data['observed_repetition'] for row in data['permutations'])
            assert F(data['permutation_p'])==F(1+exceed,1+len(data['permutations']))
            symbols=next(p for p in record['parent_refs'] if store.read(p)['kind']=='candidate_symbolization')
            markers=store.payload(symbols)['markers']
            gaps=sorted(b-a for a,b in zip(markers,markers[1:]))
            assert all(sorted(row['gap_order'])==gaps for row in data['permutations'])
    for name,case in result['cases'].items():
        if case['admitted']:
            assert case['decoded_hypothesis'] is not None
            assert case['post_decode_evaluation']['exact_message_present']
        else:
            assert case['decoded_hypothesis'] is None
            assert not (run/'records'/(name+'.must_not_decode.json')).exists()
    assert result['unmodulated_controls_clear']
    report={'status':'PASS','evidence_records_verified':records,
            'exact_source_and_residual_samples_checked':reconstructed,
            'least_squares_normal_equations_checked':normal_equations,
            'cases':len(result['cases']),'permutation_rank_checks':len(result['cases'])}
    with (run/'VALIDATION.json').open('x') as f:
        json.dump(report,f,indent=2);f.write('\n')
    print(json.dumps(report,indent=2))


if __name__=='__main__':main()
