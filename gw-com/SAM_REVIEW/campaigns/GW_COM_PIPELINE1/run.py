"""Run the declared five-layer C4 experiment with complete retained evidence."""
import argparse
from fractions import Fraction as F
import hashlib
import json
from pathlib import Path
import shutil
import sys

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[2]
sys.path.insert(0,str(ROOT))
from SAM_PROJECT.session import DomainSession
from GW_COM.runtime.native import Native
from GW_COM.runtime.modulation import source, wave_library, observe
from GW_COM.runtime.carrier import fit
from GW_COM.runtime.residual import extract
from GW_COM.runtime.information import symbolize, tests
from GW_COM.runtime.evidence import Store, encode
from GW_COM.runtime.decoder import admission, decode


def strings(value):
    if isinstance(value,F):return str(value)
    if isinstance(value,dict):return {k:strings(v) for k,v in value.items()}
    if isinstance(value,(list,tuple)):return [strings(v) for v in value]
    return value


def summary_key(symbols):
    return sorted(tuple(g['bins']) for g in symbols['repetition_groups'] if len(g['frame_indices'])>=2)


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--run',default='run001')
    args=parser.parse_args()
    if not args.run.isalnum():raise ValueError('Use an alphanumeric run name')
    directory=HERE/args.run
    directory.mkdir(exist_ok=False)
    # Snapshot implementation/contract before any measurements; corrections
    # may create another run without invalidating this run's original sources.
    snapshots=directory/'code';snapshots.mkdir()
    code=[*sorted((ROOT/'GW_COM/runtime').glob('*.py')),Path(__file__).resolve(),HERE/'CONTRACT.json',
          ROOT/'SAM_HISTORY/entries/H000733_2026-08-28_RH_Q3RHV2_SPIN_ORBIT_WAVE_THETA_STATE_HISTORY.md']
    refs=[]
    for i,path in enumerate(code):
        target=snapshots/(str(i)+'_'+path.name)
        shutil.copyfile(path,target)
        refs.append({'path':str(target.relative_to(ROOT)),'sha256':hashlib.sha256(target.read_bytes()).hexdigest()})
    method=directory/'METHOD.json'
    method.write_bytes(encode({'schema':'GW_COM_METHOD_V1','refs':refs,'contract':'CONTRACT.json in code snapshot'}))
    store=Store(ROOT,directory/'records',method)
    primary=[2,5,7,11,13,17]
    alternate=[4,6,8,10,12,14]
    definitions={
        'prime_clean':{'message':primary,'active':True},
        'prime_noisy':{'message':primary,'active':True,'gain':F(1,2),'offset':F(1,5),'noise':F(1,100),'seed':81},
        'alternate_clean':{'message':alternate,'active':True,'gain':F(2)},
        'unmodulated_clean':{'message':primary,'active':False},
        'unmodulated_noisy':{'message':primary,'active':False,'noise':F(1,100),'seed':82},
        'drift_only':{'message':primary,'active':False,'drift':F(1,400),'offset':F(1,5)}}
    sources={name:source(d['message'],d['active']) for name,d in definitions.items()}
    results={}
    with DomainSession.start('STARBREAKER',objective='GW-COM five-layer C4 successor: carrier fits, signed residuals, controlled symbol search and gated decoding',
                             output_root=directory/'sessions',receipt_storage='gzip') as session:
        print(session.announcement(),flush=True)
        native=Native(session)
        library,source_receipt=wave_library(native,sources)
        modulation_ref=store.record('modulation','modulation_model',{
            'family':'equal radial perturbations, interval modulation',
            'profile_numerator':[0,1,3,6,8,6,3,1,0],'profile_denominator':128,
            'unit_weight_antipodal_bodies':True,'motion':'prescribed C4',
            'wave':'second difference of Qxx-Qyy','unique_native_stencils':len(library),
            'known_protocol':'4 synchronization markers then 6 intervals',
            'unassigned':['continuous actuation','SI strain','polarization/chirp/precession']},execution=[source_receipt])
        for name,config in definitions.items():
            print('Processing '+name,flush=True)
            s=sources[name]
            wave=[library[stencil] for stencil in s['stencils']]
            options={k:v for k,v in config.items() if k not in ('message','active')}
            raw,channel_receipt=observe(native,wave,**options)
            # Truth is retained separately and passed only to post-decode evaluation.
            store.write(name+'.transmitter_truth',strings(s['truth']))
            source_ref=store.record(name+'.source','source_history',{
                'positions':strings(s['positions']),'signed_source_wave':strings(wave)},
                parents=[modulation_ref],execution=[source_receipt])
            raw_ref=store.record(name+'.raw','raw_waveform',{'samples':strings(raw),
                'sample_indices':list(range(len(raw))),'first_arrival_tick':37,'tick_step':1,
                'valid_mask':[True]*len(raw),'known_quiet_calibration':[0,128],
                'known_quiet_holdout':[128,192],'noise_bound':str(options.get('noise',0)),
                'channel':'single signed projected component','phase_convention':'C4 basis alternates every tick'},
                parents=[source_ref],execution=[channel_receipt])
            models,fit_receipt=fit(native,raw)
            alternatives=[]
            bound=max(F(1,10**12),3*options.get('noise',F(0)))
            for index,model in enumerate(models):
                prediction,residual,res_receipt=extract(native,raw,model)
                error=max(abs(v) for v in residual[128:192])
                adequate=error<=bound
                fit_ref=store.record(name+'.fit'+str(index),'source_fit',strings({**model,
                    'selection_criterion':'lowest parameter count among heldout-adequate models',
                    'predicted_samples':prediction,'holdout_max_absolute_error':error,
                    'declared_acceptance_bound':bound,'adequate':adequate,
                    'uncertainty':'bounded-noise holdout diagnostic; no parameter confidence interval assigned'}),
                    parents=[raw_ref],execution=[fit_receipt,res_receipt])
                residual_ref=store.record(name+'.residual'+str(index),'residual_history',{
                    'signed_samples':strings(residual),'raw_sample_indices':list(range(len(raw))),
                    'valid_mask':[True]*len(raw),'transforms':[],
                    'identity':'raw = prediction + residual, independently checked exactly'},
                    parents=[raw_ref,fit_ref],execution=[res_receipt])
                symbol_data=symbolize(residual,model['coefficients'][0])
                symbol_ref=store.record(name+'.symbols'+str(index),'candidate_symbolization',symbol_data,
                    parents=[residual_ref,modulation_ref])
                alternatives.append({'model':model['name'],'adequate':adequate,
                    'fit':fit_ref,'residual':residual_ref,'symbols':symbol_ref,'symbol_data':symbol_data})
            adequate=[a for a in alternatives if a['adequate']]
            selected=adequate[0] if adequate else alternatives[0]
            info,info_receipt=tests(native,selected['symbol_data'])
            info_ref=store.record(name+'.information','information_tests',info,
                parents=[selected['symbols'],selected['residual']],execution=[info_receipt])
            refs={'raw_waveform':raw_ref,'source_fit':selected['fit'],'residual_history':selected['residual'],
                  'candidate_symbolization':selected['symbols'],'information_tests':info_ref}
            results[name]={'lineage':refs,'adequate':bool(adequate),'alternatives':alternatives,
                'selected':selected['model'],'info':info,'symbol_data':selected['symbol_data']}
        null_cases=('unmodulated_clean','unmodulated_noisy','drift_only')
        nulls_clean=all(results[n]['symbol_data']['repetition_count']==0 for n in null_cases)
        null_evidence=store.record('unmodulated_control_suite','control_suite',{
            'cases':[{'case':n,'selected_model':results[n]['selected'],
                      'repetition_count':results[n]['symbol_data']['repetition_count'],
                      'information_tests':results[n]['lineage']['information_tests']} for n in null_cases],
            'all_zero_repeated_candidates':nulls_clean},
            parents=[results[n]['lineage']['information_tests'] for n in null_cases])
        summary={}
        for name,item in results.items():
            matching=all(summary_key(a['symbol_data'])==summary_key(item['symbol_data'])
                         for a in item['alternatives'] if a['adequate'])
            physical=[{'name':'quiet_holdout','status':'PASS' if item['adequate'] else 'FAIL',
                       'evidence':item['lineage']['source_fit']},
                      {'name':'adequate_fit_alternatives','status':'PASS' if matching else 'FAIL',
                       'evidence':[{'fit':a['fit'],'symbols':a['symbols']} for a in item['alternatives']]},
                      {'name':'unmodulated_and_drift_controls','status':'PASS' if nulls_clean else 'FAIL','evidence':null_evidence}]
            statistical=[{'name':'disjoint_repetition','status':'PASS' if item['info']['observed_repetition']>=2 else 'FAIL',
                          'evidence':item['lineage']['information_tests']},
                         {'name':'permutation_rank','status':'PASS' if F(item['info']['permutation_p'])<=F(1,20) else 'FAIL',
                          'evidence':item['lineage']['information_tests']}]
            # Individual control evidence also gets explicit artifact references
            # in a retained manifest so decoder verification checks its content.
            control_refs=[null_evidence,*[a[k] for a in item['alternatives'] for k in ('fit','symbols')]]
            control_manifest=directory/(name+'.control_evidence.json')
            control_manifest.write_bytes(encode({'schema':'GW_COM_METHOD_V1','refs':control_refs}))
            controls=store.record(name+'.controls','control_results',{
                'physical_controls':physical,'statistical_controls':statistical,
                'scope':'declared dimensionless C4 carrier/readout family','contract':store.method},
                parents=list(item['lineage'].values()),execution=[control_manifest])
            gate=admission(store,name+'.admission',item['lineage'],controls)
            admitted=store.payload(gate)['eligible']
            decoded_ref=None
            evaluation=None
            if admitted:
                decoded_ref=decode(store,name+'.decoded',gate)
                hypotheses=store.payload(decoded_ref)['hypotheses']
                evaluation={'expected_message':definitions[name]['message'],
                    'exact_message_present':any(h['interval_integers']==definitions[name]['message'] for h in hypotheses)}
                store.record(name+'.evaluation','post_decode_evaluation',evaluation,parents=[decoded_ref])
            else:
                try:
                    decode(store,name+'.must_not_decode',gate)
                except ValueError:
                    pass
                else:
                    raise AssertionError('Nonadmitted decoder executed')
            summary[name]={'selected_carrier':item['selected'],
                'adequate_models':[a['model'] for a in item['alternatives'] if a['adequate']],
                'repeat_count':item['info']['observed_repetition'],'permutation_p':item['info']['permutation_p'],
                'admitted':admitted,'admission':gate,'decoded_hypothesis':decoded_ref,
                'post_decode_evaluation':evaluation}
            print(name+': '+json.dumps({k:v for k,v in summary[name].items() if k in ('selected_carrier','repeat_count','permutation_p','admitted')}),flush=True)
        for path in store.directory.glob('*.json'):
            if not path.name.endswith('.data.json') and '.transmitter_truth.' not in path.name:
                store.verify(store.ref(path))
        output={'scope':'Dimensionless C4 five-layer execution; no physical astrophysical inference',
                'session':str(session.directory.relative_to(ROOT)), 'cases':summary,
                'native_calls':native.calls,'native_call_count':len(native.calls),
                'native_nodes':sum(c['nodes'] for c in native.calls),
                'independent_checks':'every native source stencil and every prediction/residual sample checked exactly',
                'unmodulated_controls_clear':nulls_clean}
        store.write('RUN_RESULT',output)
    print('Run preserved at '+str(directory),flush=True)


if __name__=='__main__':main()
