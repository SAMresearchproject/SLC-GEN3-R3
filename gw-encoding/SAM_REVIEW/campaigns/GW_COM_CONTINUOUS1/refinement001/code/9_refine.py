"""Refine dynamics verification and re-admit retained candidates without refitting."""
import hashlib
import json
from pathlib import Path
import shutil
import sys

HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[2];sys.path.insert(0,str(ROOT))
from GW_COM.runtime.continuous import integrate_check
from GW_COM.runtime.evidence import Store,encode
from GW_COM.runtime.decoder import admission,decode


def main():
    prior=HERE/'run001';target=HERE/'refinement001';target.mkdir(exist_ok=False)
    snapshot=target/'code';snapshot.mkdir();refs=[]
    for i,path in enumerate([*sorted((ROOT/'GW_COM/runtime').glob('*.py')),Path(__file__).resolve(),HERE/'REFINEMENT_CONTRACT.json']):
        dst=snapshot/(str(i)+'_'+path.name);shutil.copyfile(path,dst)
        refs.append({'path':str(dst.relative_to(ROOT)),'sha256':hashlib.sha256(dst.read_bytes()).hexdigest()})
    method=target/'METHOD.json';method.write_bytes(encode({'schema':'GW_COM_METHOD_V1','refs':refs}))
    store=Store(ROOT,target/'records',method,units={'time':'dimensionless continuous t','scope':'independent refinement of retained Newtonian reference'})
    old=Store(ROOT,prior/'records',prior/'METHOD.json')
    run=json.loads((prior/'records/RUN_RESULT.json').read_text())
    truth=json.loads((prior/'records/transmitter_truth.json').read_text());events=list(map(float,truth['events']));end=events[-1]+4
    result={}
    for name,case in run['cases'].items():
        active=name=='continuous_prime'
        check=integrate_check(events,end,1/64,active)
        previous=old.payload(case['dynamics'])['checks'][-1]
        passed=(check['maximum_state_error']<=1e-5 and check['maximum_wave_error']<=1e-4
                and check['energy_balance_error']<=1e-5 and check['maximum_state_error']<previous['maximum_state_error']
                and check['maximum_wave_error']<previous['maximum_wave_error'])
        dynamics=store.record(name+'.dynamics','integrated_dynamics',{'check':check,'pass':passed,
            'previous_step':previous['step'],'tolerances_unchanged':True},parents=[case['dynamics']])
        old_gate=old.payload(case['admission']);lineage=old_gate['lineage'];controls=old.payload(old_gate['controls'])
        for row in controls['physical_controls']:
            if row['name']=='integrated_dynamics':row.update(status='PASS' if passed else 'FAIL',evidence=dynamics)
        control=store.record(name+'.controls','control_results',controls,parents=list(lineage.values()))
        gate=admission(store,name+'.admission',lineage,control);eligible=store.payload(gate)['eligible'];decoded=None;matches=None
        if eligible:
            decoded=decode(store,name+'.decoded',gate)
            matches=any(h['interval_integers']==truth['payload'] for h in store.payload(decoded)['hypotheses'])
            store.record(name+'.evaluation','post_decode_evaluation',{'expected':truth['payload'],'exact_match':matches},parents=[decoded])
        else:
            try:decode(store,name+'.blocked',gate)
            except ValueError:pass
            else:raise AssertionError('Nonadmitted decode')
        result[name]={'dynamics_pass':passed,'admitted':eligible,'decoded':decoded,'exact_match':matches,
            'admission':gate,'dynamics':dynamics,'state_error':check['maximum_state_error'],
            'wave_error':check['maximum_wave_error'],'energy_balance_error':check['energy_balance_error']}
        store.verify(gate)
        print(name+': '+json.dumps(result[name]),flush=True)
    store.write('RESULT',{'predecessor_result':old.ref(prior/'records/RUN_RESULT.json'),'payload':truth['payload'],
                         'cases':result,'new_native_calls':0,'reason':'Independent numerical refinement, unchanged native research inputs/results'})


if __name__=='__main__':main()
