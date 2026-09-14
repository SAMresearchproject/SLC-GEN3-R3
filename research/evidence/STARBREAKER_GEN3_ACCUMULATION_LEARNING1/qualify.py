"""Installed Starbreaker integration execution and independent wiring checks."""
from pathlib import Path
from fractions import Fraction as F
from collections import Counter
import hashlib,json,sys,time
import numpy as np
P=Path(__file__).resolve().parent;ROOT=P.parents[2];sys.path.insert(0,str(ROOT))
from SAM_PROJECT.session import DomainSession
from CURRENT_REVISION.runtime import verify

def save(p,v):Path(p).write_text(json.dumps(v,indent=2,sort_keys=True)+'\n')
def arg(summary,name):return F(summary[name]['argument'])

def main():
    started=time.monotonic();checks=Counter();registry=verify();save(P/'REGISTRY_VERIFICATION.json',registry)
    s=DomainSession.start('STARBREAKER',objective='Installed Starbreaker GEN3 source-action/log accumulation and acquired ATOM3D construction-policy integration.',output_root=P/'sessions',receipt_storage='gzip')
    print(s.announcement(),flush=True);print('Session: '+str(s.directory),flush=True);save(P/'SESSION_BINDING.json',{'path':str(s.directory),'manifest':s.manifest})
    s.execute('SB_STATUS',{},purpose='Verify installed first-class Starbreaker native operations and source profile.')
    observed=[]
    for relation in ['N100_EDGE_002','N100_EDGE_006','N100_EDGE_084']:
        for direction in ['FORWARD','REVERSE']:
            for rho in range(1,129):
                account=f'{relation}_{direction}_{rho}'
                result=s.execute('SB_J4_ACCUMULATE',{'account':account,'relation':relation,'direction':direction,'rho':rho,'incoming_address':1},purpose=f'Compute actual J4 signed response norm and exact logarithmic accumulation for {relation}/{direction}/rho{rho}; retain source phase and ancestry.')
                summary=result['accumulation']['summary'];energy=list(map(F,result['actions_per_cycle']));signed=result['signed_receiver_history']
                assert result['accumulation']['status']=='DEFINED'
                assert [sum(F(v)**2 for v in row) for row in signed]==energy+[energy[0]]
                up=down=F(1);maximum=F(1);ties=[0]
                values=energy+[energy[0]]
                for k,(a,b) in enumerate(zip(values,values[1:]),1):
                    ratio=b/a
                    if ratio>1:up*=ratio
                    elif ratio<1:down/=ratio
                    net=b/values[0]
                    if net>maximum:maximum=net;ties=[k]
                    elif net==maximum:ties.append(k)
                assert arg(summary,'U')==up and arg(summary,'D')==down and arg(summary,'V')==up*down and arg(summary,'L')==1 and arg(summary,'M')==maximum
                assert summary['maximizing_points']==[account+'/shell/'+str(k) for k in ties]
                assert result['propagation']['closed'] and result['propagation']['inverse_recovered']
                checks['native_complete_source_histories']+=1;checks['native_shell_steps']+=4
                checks['positive_total_variation_closed_cycles']+=int(up*down>1);checks['stationary_norm_cycles']+=int(up*down==1)
                observed.append({'account':account,'actions':result['actions_per_cycle'],'summary':summary})
            print(json.dumps({'completed_histories':checks['native_complete_source_histories'],'last_family':relation+'/'+direction}),flush=True)
    save(P/'NATIVE_CYCLE_RESULTS.json',observed)
    request={'account':'append_recovery','relation':'N100_EDGE_002','direction':'FORWARD','rho':1,'incoming_address':1,'receiver_family_ids':[203898,0,4799999]}
    first=s.execute('SB_J4_ACCUMULATE',request,purpose='Exercise integrated signed history, exact accumulation and learned receiver construction proposals in one Starbreaker call.')
    initial=first['accumulation'];session_path=s.directory;s.close();s=DomainSession(session_path)
    resumed=s.execute('SB_READOUT',{'account':'append_recovery'},purpose='Read exact Starbreaker accumulation after complete runtime restart.')
    assert resumed==initial;checks['fresh_exact_account_recovery']+=1
    second=s.execute('SB_J4_ACCUMULATE',{k:v for k,v in request.items() if k!='receiver_family_ids'},purpose='Append one actual phase cycle to the recovered account without replaying prior accumulation.')
    a=initial['summary'];b=second['accumulation']['summary'];assert arg(b,'U')==arg(a,'U')**2 and arg(b,'D')==arg(a,'D')**2 and arg(b,'V')==arg(a,'V')**2 and arg(b,'L')==1
    assert second['action_arithmetic_reused'] and second['accumulation']['edge_count']==8;checks['incremental_append_after_restart']+=1
    history=s.execute('SB_HISTORY',{'account':'append_recovery'},purpose='Recover complete ordered signed amplitudes and packet ancestry behind the exact log account.')
    save(P/'RECOVERED_HISTORY.json',history);save(P/'INTEGRATED_EXAMPLE.json',second)
    before=s.execute('SB_READOUT',{'account':'append_recovery'},purpose='Pin the account before a source-mismatch rejection check.')
    try:s.execute('SB_J4_ACCUMULATE',{**request,'rho':2},purpose='Verify that a different source cannot append to an existing Starbreaker source account.')
    except ValueError:checks['source_mismatch_rejected']+=1
    else:raise AssertionError('Mixed-source append accepted')
    assert s.execute('SB_READOUT',{'account':'append_recovery'},purpose='Verify rejected source append left the acquired history unchanged.')==before
    try:s.execute('SB_CONSTRUCTION_POLICY',{'family_ids':[203898],'source_contract':'UNRELATED_GRAPH'},purpose='Verify learned receiver policy admission retains its actual source grammar.')
    except ValueError:checks['wrong_training_contract_rejected']+=1
    else:raise AssertionError('Cross-domain features accepted')
    # The two source-selected models were pinned before this comparison. This
    # evaluation is part of integration qualification; it does not resume or
    # alter the paused curriculum or change either selected model.
    data=np.load(ROOT/'SAM_REVIEW/campaigns/GEN3_ATOM3D_CONSTRUCTION_LEARNING1/dataset.npz');test=data['split']==2;ids=data['ids'][test];truth=data['y'][test]
    names=['shared_four_state_orbit','channel_minimum_sets_agree'];counts=[Counter(),Counter()];prediction_columns=[[],[]];first_policy=None
    for start in range(0,len(ids),2048):
        result=s.execute('SB_CONSTRUCTION_POLICY',{'family_ids':ids[start:start+2048].tolist(),'source_contract':'A3D41_TYPED_CONSTRUCTION_CAMPAIGN_V1'},purpose='Apply the pinned construction policies through installed Starbreaker to reused held-out pattern families; no fitting or model selection.')
        if first_policy is None:first_policy=result
        for offset,row in enumerate(result['rows']):
            assert row['family_id']==int(ids[start+offset])
            for t,target in enumerate(names):
                predicted=F(row['predictions'][target]['probability'])>=F(1,2);actual=bool(truth[start+offset,t]);label='tp' if predicted and actual else 'fp' if predicted else 'fn' if actual else 'tn'
                counts[t][label]+=1;prediction_columns[t].append(int(predicted))
        if start%16384==0:print(json.dumps({'test_policy_families':min(start+2048,len(ids))}),flush=True)
    np.savez_compressed(P/'TEST_PREDICTIONS.npz',family_ids=ids,predictions=np.array(prediction_columns).T)
    # Report ratios with native exact arithmetic, keeping contingency counting
    # as the explicitly identified source-record orchestration step.
    reports={}
    for t,target in enumerate(names):
        c=counts[t];nodes=[]
        def node(op,**fields):name='m'+str(len(nodes));nodes.append({'id':name,'op':op,**fields});return name
        def value(n):return node('VALUE',value=str(n),source={'dataset':'cb7a5ae5299a5cd60574b6019da7f093ee41e86d526b397709dbc912df25d5d0','target':target,'scope':'reused test patterns; models frozen before evaluation'})
        def ratio(a,b):return node('DIVIDE',left=value(a),right=value(b))
        refs={'accuracy':ratio(c['tp']+c['tn'],len(ids)),'precision':ratio(c['tp'],c['tp']+c['fp']),'recall':ratio(c['tp'],c['tp']+c['fn']),'specificity':ratio(c['tn'],c['tn']+c['fp'])}
        refs['balanced_accuracy']=node('DIVIDE',left=node('ADD',left=refs['recall'],right=refs['specificity']),right=value(2))
        result=s.execute('GEN2_SIGNED_LOG',{'nodes':nodes,'representation':'RATIONAL'},purpose='Compute exact integration test metrics for the pinned '+target+' model through Starbreaker GEN3.')
        values={n['id']:n['value'] for n in result['nodes']};reports[target]={'families':len(ids),**dict(c),**{k:str(values[v]) for k,v in refs.items()}}
    # Policy knowledge is durable in the same R3 origin root as log accounts.
    probe=s.execute('SB_CONSTRUCTION_POLICY',{'family_ids':[203898,0,4799999],'source_contract':'A3D41_TYPED_CONSTRUCTION_CAMPAIGN_V1'},purpose='Pin acquired policy execution before a second complete process-level consumer recovery.')
    s.close();s=DomainSession(session_path)
    repeat=s.execute('SB_CONSTRUCTION_POLICY',{'family_ids':[203898,0,4799999],'source_contract':'A3D41_TYPED_CONSTRUCTION_CAMPAIGN_V1'},purpose='Replay the same acquired receiver policy after fresh recovery without fitting.')
    assert repeat==probe;checks['fresh_exact_policy_recovery']+=1
    status=s.status();s.close();assert status['incomplete_calls']==0 and status['failed_calls']==2
    checks['authenticated_returned_receipts']=len(status['returned_calls']);checks['expected_admission_rejections']=status['failed_calls']
    with DomainSession.start('MATTER_SEARCH',objective='Verify Starbreaker operation domain admission.',output_root=P/'admission_sessions',receipt_storage='gzip') as other:
        try:other.execute('SB_STATUS',{},purpose='Verify a Starbreaker domain operation rejects on another domain.')
        except ValueError:checks['wrong_operation_domain_rejected']+=1
        else:raise AssertionError('Starbreaker operation accepted by another domain')
    result={'status':'PASS','domain_version':'SB-GEN3-ACCUMULATION-R1','checks':dict(checks),'test_results':reports,'test_scope':'Reused 94-pattern holdout, 81406 families. No training resumed; both source-selected models pinned before this evaluation.','seconds':time.monotonic()-started,'registry':registry,'training_pause_preserved':(ROOT/'SAM_REVIEW/campaigns/GEN3_ATOM3D_CONSTRUCTION_CURRICULUM1/STOP').exists()}
    save(P/'RESULT.json',result);print(json.dumps(result),flush=True)

if __name__=='__main__':main()
