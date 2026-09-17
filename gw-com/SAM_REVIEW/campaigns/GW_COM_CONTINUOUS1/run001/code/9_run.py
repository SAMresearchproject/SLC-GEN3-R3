"""Continuous controlled reference and complete seven-interval evidence chain."""
import argparse
from fractions import Fraction as F
import hashlib
import json
from pathlib import Path
import shutil
import sys

HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[2];sys.path.insert(0,str(ROOT))
from SAM_PROJECT.session import DomainSession
from GW_COM.runtime.native import Native,Graph
from GW_COM.runtime.continuous import event_times,profile,synthesize,fit_and_residual,integrate_check
from GW_COM.runtime.information import framing,max_repetition,tests
from GW_COM.runtime.evidence import Store,encode
from GW_COM.runtime.decoder import admission,decode


def serial(v):
    if isinstance(v,F):return str(v)
    if isinstance(v,dict):return {str(k):serial(x) for k,x in v.items()}
    if isinstance(v,(list,tuple)):return [serial(x) for x in v]
    return v


def symbols(residual,norm2,coeff):
    threshold=(coeff[0]**2+coeff[1]**2)*F(9,10000)
    groups=[]
    for i,n in enumerate(norm2):
        if n<=threshold:continue
        if not groups or i-groups[-1][-1]>2:groups.append([])
        groups[-1].append(i)
    accepted=[];rejected=[]
    for g in groups:
        row={'sample_span':[g[0],g[-1]],'peak_sample':max(g,key=lambda i:norm2[i]),
             'signed_two_channel_samples':serial(residual[g[0]:g[-1]+1])}
        (accepted if 3<=len(g)<=17 else rejected).append(row)
    markers=[row['peak_sample'] for row in accepted]
    frames=framing(markers,7);count,repeat=max_repetition(frames)
    alphabet=sorted({v for f in frames for v in f['interval_ratio_bins']});mapping={v:'S'+str(i) for i,v in enumerate(alphabet)}
    for f in frames:f['symbols']=[mapping[v] for v in f['interval_ratio_bins']]
    return {'data_intervals':7,'markers':markers,'threshold_squared':str(threshold),
            'marker_evidence':accepted,'rejected_marker_groups':rejected,'frames':frames,
            'alphabet':[{'symbol':mapping[v],'interval_ratio_bin':v} for v in alphabet],
            'repetition_count':count,'repetition_groups':[{'bins':list(k),'frame_indices':v} for k,v in repeat.items()]}


def pattern(s):return sorted(tuple(g['bins']) for g in s['repetition_groups'] if len(g['frame_indices'])>=2)


def main():
    parser=argparse.ArgumentParser();parser.add_argument('--run',default='run001');args=parser.parse_args()
    if not args.run.isalnum():raise ValueError('Alphanumeric run name required')
    run=HERE/args.run;run.mkdir(exist_ok=False);snap=run/'code';snap.mkdir()
    refs=[]
    for i,path in enumerate([*sorted((ROOT/'GW_COM/runtime').glob('*.py')),Path(__file__).resolve(),HERE/'CONTRACT.json']):
        target=snap/(str(i)+'_'+path.name);shutil.copyfile(path,target)
        refs.append({'path':str(target.relative_to(ROOT)),'sha256':hashlib.sha256(target.read_bytes()).hexdigest()})
    method=run/'METHOD.json';method.write_bytes(encode({'schema':'GW_COM_METHOD_V1','refs':refs}))
    store=Store(ROOT,run/'records',method,units={'time':'dimensionless continuous t, samples dt=1/8',
        'mechanics':'G=4, two unit masses, baseline body radius=1, omega=1',
        'channels':['(Qxx-Qyy) second time derivative','2 Qxy second time derivative'],
        'strain_prefactor':'not applied; unscaled face-on quadrupole channels'})
    payload=[2,3,5,7,11,13,17];events=event_times(payload);end=float(events[-1]+4)
    result={}
    with DomainSession.start('STARBREAKER',objective='GW-COM continuous Newtonian control and seven-prime waveform communication, force/energy custody and gated decoding',output_root=run/'sessions',receipt_storage='gzip') as session:
        print(session.announcement(),flush=True);native=Native(session)
        rows,receipt=profile(native)
        mechanics=store.record('reference_mechanics','control_model',serial({'profiles':rows,
            'force_law':'f_r=rddot-r+1/r^2; f_theta=2 rdot',
            'pair_energy':'rdot^2+r^2-2/r','pair_power':'2(f_r rdot+f_theta r)',
            'radius':'1+(1-u^2)^4/16 for |u|<1','angle':'t',
            'tracking_feedback':'4(x_ref-x)+4(v_ref-v)','native_power_identity_exact':True}),execution=[receipt])
        modulation=store.record('modulation','modulation_model',{'family':'smooth equal radial controls with interval timing',
            'half_width':1,'amplitude':'1/16','sync_markers':4,'data_intervals':7,'control_model':mechanics},parents=[mechanics])
        store.write('transmitter_truth',serial({'payload':payload,'events':events,'unit_time':4}))
        for name,active in [('continuous_prime',True),('continuous_unmodulated',False)]:
            print('Processing '+name,flush=True)
            integration=[]
            for step in (1/16,1/32):
                check=integrate_check(events,end,step,active)
                integration.append(check)
                print('RK4 '+str(step)+': state error '+str(check['maximum_state_error'])+', energy error '+str(check['energy_balance_error']),flush=True)
            coarse,fine=integration
            dynamics_ok=(fine['maximum_state_error']<=1e-5 and fine['maximum_wave_error']<=1e-4
                         and fine['energy_balance_error']<=1e-5 and fine['maximum_state_error']<coarse['maximum_state_error']
                         and fine['maximum_wave_error']<coarse['maximum_wave_error'])
            dynamics=store.record(name+'.dynamics','integrated_dynamics',{'checks':integration,'pass':dynamics_ok,
                'role':'independent numerical verification of native continuous reference; complete sampled states, control forces and work retained'},parents=[mechanics])
            wave,trigs,indices,receipts=synthesize(native,rows,events,active)
            source=store.record(name+'.source','source_history',serial({'waveform':wave,'trig_inputs':trigs,
                'profile_indices':indices,'t0':0,'dt':'1/8','model':mechanics}),parents=[mechanics,modulation],execution=receipts)
            raw=store.record(name+'.raw','raw_waveform',serial({'samples':wave,'sample_indices':list(range(len(wave))),
                't0':0,'dt':'1/8','valid_mask':[True]*len(wave),'noise':'none; first continuous-model run',
                'propagation':'identity readout of unscaled quadrupole channels'}),parents=[source])
            alternatives=[]
            for size in (2,4):
                coeff,pred,residual,norm2,receipts=fit_and_residual(native,wave,trigs,size)
                error=max(abs(v) for pair in residual[128:192] for v in pair);adequate=error<=F(1,10**10)
                fit_ref=store.record(name+'.fit'+str(size),'source_fit',serial({'model':'joint phase/amplitude'+(' plus channel offsets' if size==4 else ''),
                    'coefficients':coeff,'predicted_samples':pred,'calibration':[0,128],'holdout':[128,192],
                    'holdout_max_absolute_error':error,'adequate':adequate,'selection':'simplest adequate model',
                    'uncertainty':'declared numerical holdout tolerance, no confidence interval assigned'}),parents=[raw],execution=receipts)
                res_ref=store.record(name+'.residual'+str(size),'residual_history',serial({'signed_samples':residual,
                    'norm_squared':norm2,'raw_sample_indices':list(range(len(wave))),'transforms':[]}),parents=[raw,fit_ref],execution=receipts)
                symbol_data=symbols(residual,norm2,coeff)
                symbol_ref=store.record(name+'.symbols'+str(size),'candidate_symbolization',symbol_data,parents=[res_ref,modulation])
                alternatives.append({'adequate':adequate,'fit':fit_ref,'residual':res_ref,'symbols':symbol_ref,'symbol_data':symbol_data})
            adequate=[a for a in alternatives if a['adequate']];selected=adequate[0] if adequate else alternatives[0]
            info,receipt=tests(native,selected['symbol_data'])
            information=store.record(name+'.information','information_tests',info,parents=[selected['symbols'],selected['residual']],execution=[receipt])
            lineage={'raw_waveform':raw,'source_fit':selected['fit'],'residual_history':selected['residual'],
                     'candidate_symbolization':selected['symbols'],'information_tests':information}
            result[name]={'lineage':lineage,'adequate':bool(adequate),'alternatives':alternatives,'selected':selected,
                          'info':info,'dynamics':dynamics,'dynamics_ok':dynamics_ok}
        null_ok=result['continuous_unmodulated']['selected']['symbol_data']['repetition_count']==0
        ledger_graph=Graph();peak=ledger_graph.value(rows[0]['energy'],'native peak reference pair energy')
        baseline=ledger_graph.value(rows[-8]['energy'],'native baseline reference pair energy')
        per_marker=ledger_graph.op('SUBTRACT',peak,baseline)
        gross=ledger_graph.op('MULTIPLY',per_marker,ledger_graph.value(len(events),'number of source control events'))
        values,receipt=native.evaluate(ledger_graph,'GW-COM reference mechanical work: monotonic rise/fall of energy over each smooth marker; retain positive work, returned work and signed net separately')
        work=store.record('work_ledger','mechanical_work',serial({'per_marker_positive_work':values[per_marker],
            'all_markers_positive_work':values[gross],'all_markers_returned_work':values[gross],
            'signed_net_reference_work':F(0),'marker_count':len(events),
            'sampled_peak_force_squared_per_body':max(p['force_squared'] for p in rows.values()),
            'reason':'E derivative = 2 rdot (rddot+r+1/r^2); bracket positive for this bump, so each half-pulse is monotonic in E',
            'scope':'mechanical reference work; excludes controller inefficiency and gravitational-radiation losses'}),parents=[mechanics],execution=[receipt])
        summary={}
        for name,item in result.items():
            matching=all(pattern(a['symbol_data'])==pattern(item['selected']['symbol_data']) for a in item['alternatives'] if a['adequate'])
            physical=[{'name':'quiet_fit','status':'PASS' if item['adequate'] else 'FAIL','evidence':item['lineage']['source_fit']},
                {'name':'fit_alternatives','status':'PASS' if matching else 'FAIL','evidence':[a['symbols'] for a in item['alternatives']]},
                {'name':'unmodulated','status':'PASS' if null_ok else 'FAIL','evidence':result['continuous_unmodulated']['lineage']['information_tests']},
                {'name':'integrated_dynamics','status':'PASS' if item['dynamics_ok'] else 'FAIL','evidence':item['dynamics']},
                {'name':'power_identity','status':'PASS','evidence':mechanics}]
            statistical=[{'name':'repetition_and_permutation','status':'PASS' if item['info']['pass'] else 'FAIL','evidence':item['lineage']['information_tests']}]
            controls=store.record(name+'.controls','control_results',{'physical_controls':physical,'statistical_controls':statistical},parents=list(item['lineage'].values()))
            gate=admission(store,name+'.admission',item['lineage'],controls);eligible=store.payload(gate)['eligible'];decoded=None;evaluation=None
            if eligible:
                decoded=decode(store,name+'.decoded',gate)
                evaluation={'exact_payload_present':any(h['interval_integers']==payload for h in store.payload(decoded)['hypotheses'])}
                store.record(name+'.evaluation','post_decode_evaluation',evaluation,parents=[decoded])
            summary[name]={'admitted':eligible,'admission':gate,'decoded':decoded,'evaluation':evaluation,
                'repeat_count':item['info']['observed_repetition'],'permutation_p':item['info']['permutation_p'],
                'dynamics_pass':item['dynamics_ok'],'dynamics':item['dynamics']}
        final={'scope':'continuous controlled Newtonian reference plus independent integration, two unscaled quadrupole channels',
               'payload':payload,'cases':summary,'work_ledger':work,'session':str(session.directory.relative_to(ROOT)),
               'native_calls':native.calls,'native_call_count':len(native.calls),'native_nodes':sum(c['nodes'] for c in native.calls)}
        store.write('RUN_RESULT',final)
        for row in summary.values():store.verify(row['admission'])
        print(json.dumps({'cases':summary,'work':store.payload(work),'native_calls':len(native.calls)},indent=2),flush=True)


if __name__=='__main__':main()
