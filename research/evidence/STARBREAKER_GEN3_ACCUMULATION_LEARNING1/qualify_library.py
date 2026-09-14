"""Verify all acquired targets and unchanged primary models after library expansion."""
from pathlib import Path
from fractions import Fraction as F
import hashlib,json,sys,subprocess
import numpy as np
P=Path(__file__).resolve().parent;ROOT=P.parents[2];sys.path.insert(0,str(ROOT))
from SAM_PROJECT.session import DomainSession
from CURRENT_REVISION.runtime import verify

def read(p):return json.loads(Path(p).read_text())
def save(p,v):Path(p).write_text(json.dumps(v,indent=2,sort_keys=True)+'\n')

def main():
    out=P/'library_extension';pkg=read(ROOT/'CURRENT_REVISION/domains/STARBREAKER/POLICY.json');old=read(out/'before/POLICY.json')
    for target in old['models']:
        assert old['models'][target]['model']==pkg['models'][target]['model']
        assert old['models'][target]['sha256']==pkg['models'][target]['sha256']
    assert old['feature_table']==pkg['feature_table'] and old['inventory_counts']==pkg['inventory_counts']
    assert read(out/'before/SOURCE_BINDING.json')['sources']==read(ROOT/'CURRENT_REVISION/domains/STARBREAKER/SOURCE_BINDING.json')['sources']
    data=np.load(ROOT/'SAM_REVIEW/campaigns/GEN3_ATOM3D_CONSTRUCTION_LEARNING1/dataset.npz');idx=np.linspace(0,len(data['ids'])-1,256,dtype=int);ids=data['ids'][idx];features=np.column_stack([data['x'][idx],np.array(pkg['feature_table'])[data['patterns'][idx]]])
    s=DomainSession.start('STARBREAKER',objective='Installed adoption of all45 source-bound construction targets, exact signed log integration and source-selected primary model preservation.',output_root=out/'sessions',receipt_storage='gzip')
    print(s.announcement(),flush=True);save(out/'SESSION_BINDING.json',{'path':str(s.directory),'manifest':s.manifest})
    status=s.execute('SB_STATUS',{},purpose='Verify all45 acquired targets are available through the installed Starbreaker domain.')
    assert len(status['learned_targets'])==45
    result=s.execute('SB_CONSTRUCTION_POLICY',{'family_ids':ids.tolist(),'source_contract':pkg['source_contract'],'targets':status['learned_targets']},purpose='Apply all45 acquired construction policies to256 source families with preserved feature semantics and exact branch probabilities.')
    checked=0
    for i,row in enumerate(result['rows']):
        for target,package in pkg['models'].items():
            model=package['model'];node=model['tree']
            while node['split'] and node['depth']<model['selected_depth']:
                c=node['split'];node=node['left' if features[i,model['columns'][c['feature']]]<=c['threshold'] else 'right']
            assert node['probability']==row['predictions'][target]['probability'] and node['path']==row['predictions'][target]['decision_path'];checked+=1
    assert checked==11520
    request={'account':'all45_recovery','relation':'N100_EDGE_002','direction':'FORWARD','rho':1,'incoming_address':1,'receiver_family_ids':[203898,0]}
    first=s.execute('SB_J4_ACCUMULATE',request,purpose='Verify the final installed full-library engine computes the same native source action and exact cyclic logarithmic history.')
    expected=read(P/'CANDIDATE_SMOKE.json');assert first['actions_per_cycle']==expected['actions_per_cycle']
    for k in ['U','D','V','L','M']:assert first['accumulation']['summary'][k]==expected['accumulation']['summary'][k]
    path=s.directory;s.close();s=DomainSession(path)
    got=s.execute('SB_READOUT',{'account':request['account']},purpose='Recover the exact accumulator from the same native root as the full45-target learned library.')
    assert got==first['accumulation']
    second=s.execute('SB_J4_ACCUMULATE',{k:v for k,v in request.items() if k!='receiver_family_ids'},purpose='Append a cycle after full-library recovery while reusing the acquired native response action.')
    assert second['action_arithmetic_reused'] and second['accumulation']['edge_count']==8
    assert F(second['accumulation']['summary']['V']['argument'])==F(got['summary']['V']['argument'])**2
    final_status=s.status();s.close();assert not final_status['failed_calls'] and not final_status['incomplete_calls']
    # Actual current CE CLI adoption, inheriting this managed resource budget.
    empty=out/'EMPTY.json';save(empty,{})
    cli=subprocess.run([str(ROOT/'CE-run'),'--domain','STARBREAKER','--operation','SB_STATUS','--payload',str(empty)],cwd=ROOT,text=True,capture_output=True)
    save(out/'CLI.json',{'returncode':cli.returncode,'stdout':cli.stdout,'stderr':cli.stderr});assert cli.returncode==0 and 'SB-GEN3-ACCUMULATION-R1' in cli.stdout
    result={'status':'PASS','acquired_models':45,'exact_policy_applications':checked,'primary_models_and_features_unchanged':True,'native_response_source_unchanged':True,'same_exact_log_arguments':True,'fresh_full_library_recovery':True,'incremental_append':True,'ce_cli_adoption':True,'managed_receipts':len(final_status['returned_calls']),'registry':verify()}
    save(out/'QUALIFICATION.json',result);print(json.dumps(result),flush=True)

if __name__=='__main__':main()
