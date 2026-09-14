"""Use GEN2 finite inverse algorithms to find a compact source readout."""
from pathlib import Path
from itertools import combinations
import json, sys
ROOT=Path(__file__).resolve().parents[3];sys.path.insert(0,str(ROOT))
from SAM_PROJECT.session import DomainSession
HERE=Path(__file__).resolve().parent
SESSION=ROOT/'SAM_REVIEW/campaigns/PROJECT_DOMAIN_SESSIONS1/sessions/ATOM3D_c51c939ff7ce489196cfb2aa0bcbfc43'
def load(n):return json.loads((HERE/n).read_text())
def save(n,v):(HERE/n).write_text(json.dumps(v,indent=2,sort_keys=True)+'\n')

def main():
    ds=load('DELTAS.json'); atlas=load('ATLAS.json'); old=load('PROFILES.json')
    d={(r['state'],r['cover'],r['assignment'],r['edge'],r['sign']):r['delta'] for r in ds}
    states=sorted({r['state'] for r in ds})
    sources=[{'state':s,'cover':c,'assignment':a} for s in states for c in (3,4) for a in range(6)]
    session=DomainSession(SESSION);known=set((SESSION/'calls').iterdir());calls=[]
    def execute(op,payload,purpose):
        nonlocal known
        r=session.execute(op,payload,purpose=purpose)
        now=set((SESSION/'calls').iterdir()); added=now-known; assert len(added)==1
        calls.append({'operation':op,'purpose':purpose,'directory':str(added.pop().relative_to(ROOT))});known=now
        save('COMPACT_CALLS.json',calls);return r
    # The one additional scalar is an actual native polynomial readout of the
    # signed N01 site current in its existing phase plane. No spatial axis is assigned.
    bits={}
    for state in states:
        row=next(r for r in atlas if r['configuration']=={'state':state,'cover':3,'assignment':0,'rho':1})
        result=execute('GEN2_READOUT',{'strategy':'polynomial','source':{'linear':[1,1],'output_unit':'SIGNED_NATIVE_SITE_CURRENT','input_unit':'NATIVE_Z4_CURRENT','normalization':'REAL_PLUS_IMAGINARY_N01_PHASE_PLANE'},'after':[row['sites'][0][5],row['sites'][1][5]]},f'Compute signed N01 site readout Re(alpha)+Im(alpha) for retained history {state}.')
        bits[state]=result['value']
    save('SIGNED_SITE_READOUT.json',{str(k):v for k,v in bits.items()})
    def spec(probes,with_bit=False):
        records=[]
        for r in sources:
            s,c,a=r['state'],r['cover'],r['assignment']
            visible=[d[s,c,a,e,sign] for e,sign in probes]
            if with_bit:visible.append(bits[s])
            records.append({'source':r,'visible':visible})
        return {'records':records,'target':'ORIGINAL_LI6_STATE_COVER_PLACEMENT','known_information':{'rho':1,'starting_history':'UNKNOWN_WITHIN_RETAINED_SIXTEEN','probe_protocol':'INDEPENDENT_SINGLE_WRITES_EACH_FROM_THE_SAME_RESTORED_INITIAL_CONFIGURATION','probes':probes,'signed_N01_readout':with_bit},'source_contract':{'source':'H000976','native_transition_receipts':'WORDS.json','native_construction_receipts':'ATLAS_CALLS.json','native_response_differences':'DELTAS.json','signed_site_readout_receipts':'COMPACT_CALLS.json'}}
    profiles=[]
    def profile(probes):
        if len(probes)==2 and all(s==1 for e,s in probes):
            e,f=[x[0] for x in probes]; prior=old[f'UNKNOWN_STATE_PAIR_{e}_{f}']
            r={'profile':prior['profile'],'receipt':prior['receipt'],'probes':probes}
        else:
            result=execute('GEN2_CUSTODY',{'contract':spec(probes),'action':'profile'},f'Native inverse partition for independent probe tuple {probes}.')
            r={'profile':result['native_profile'],'receipt':calls[-1]['directory'],'probes':probes}
        profiles.append(r);save('COMPACT_PROFILES.json',profiles)
        return r
    probes=[(e,s) for e in range(9) for s in (1,-1)]
    winners=[]
    for pair in combinations(probes,2):
        r=profile(pair)
        if r['profile']['visible_output_count']==96:winners.append(r)
    searched='ALL_153_SIGNED_PAIRS'
    if not winners:
        for triple in combinations([(e,1) for e in range(9)],3):
            r=profile(triple)
            if r['profile']['visible_output_count']==96:winners.append(r)
        searched+=';ALL_84_POSITIVE_TRIPLES'
    if not winners:
        save('COMPACT_RESULT.json',{'status':'NO_COMPACT_MATCH','search':searched});session.close();return
    chosen=winners[0]['probes']; contract=spec(chosen,True)
    result=execute('GEN2_CUSTODY',{'contract':contract,'action':'profile'},'Compute exact information of compact response probes plus one signed site-current bit.')
    save('DECODER_CONTRACT.json',contract)
    save('DECODER_PROFILE.json',result)
    # Query every source observation through the native inverse. This checks the
    # usable decoder, including every retained history, cover and center placement.
    inverses=[]
    for record in contract['records']:
        recovered=execute('GEN2_CUSTODY',{'contract':contract,'action':'fiber','visible':record['visible']},'Decode compact observation '+json.dumps(record['source'],sort_keys=True))
        inverses.append({'source':record['source'],'visible':record['visible'],'members':recovered,'matches':recovered==[record['source']],'receipt':calls[-1]['directory']})
    save('COMPACT_INVERSES.json',inverses)
    save('COMPACT_RESULT.json',{'status':'PASS' if all(r['matches'] for r in inverses) else 'FAIL','search':searched,'minimum_scalar_action_probes':len(chosen),'chosen_probes':chosen,'all_matching_tuples_in_searched_roster':[r['probes'] for r in winners],'with_signed_site_bit':True,'decoded_configurations':len(inverses),'profile':result['native_profile'],'native_calls':len(calls)})
    print(json.dumps(load('COMPACT_RESULT.json'),indent=2),flush=True)
    session.close()
if __name__=='__main__':main()
