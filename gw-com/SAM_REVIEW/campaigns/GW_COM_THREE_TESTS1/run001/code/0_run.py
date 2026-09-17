"""Three fixed experiments. No adaptive points or decoder changes."""
import argparse, hashlib, importlib.util, json, math, random, shutil, sys
from fractions import Fraction as F
from pathlib import Path
import numpy as np
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[2];sys.path.insert(0,str(ROOT))
from SAM_PROJECT.session import DomainSession
from GW_COM.runtime.native import Native,Graph
from GW_COM.runtime.continuous import fit_and_residual
from GW_COM.runtime.information import tests
from GW_COM.runtime.evidence import Store,encode
from GW_COM.runtime.decoder import admission,decode
PRE=ROOT/'SAM_REVIEW/campaigns/GW_COM_CONTINUOUS1'
spec=importlib.util.spec_from_file_location('continuous_campaign',PRE/'run.py');module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
symbols,pattern,serial=module.symbols,module.pattern,module.serial

def rounded(x):return F(format(float(x),'.16e'))
def read(p):return json.loads(p.read_text())
def prior(store,name):
 ref=store.ref(PRE/'run001/records'/f'{name}.json');store.verify(ref);return ref,store.payload(ref)

def noisy(native,wave,sigma,seed):
 rng=random.Random(seed);draws=[tuple(F(format(rng.gauss(0,1),'.12g')) for _ in range(2)) for row in wave]
 out=[];receipts=[]
 for start in range(0,len(wave),512):
  g=Graph();sn=g.value(sigma,'declared noise sigma per channel');nodes=[]
  for i in range(start,min(start+512,len(wave))):
   pair=[]
   for j in (0,1):pair.append(g.op('ADD',g.value(wave[i][j],{'source_sample':i,'channel':j}),g.op('MULTIPLY',sn,g.value(draws[i][j],{'Gaussian_seed':seed,'sample':i,'channel':j}))))
   nodes.append(pair)
  vals,rec=native.evaluate(g,'Test1: add declared Gaussian receiver noise to continuous source; preserve signed channels')
  receipts.append(rec);out.extend(tuple(vals[n] for n in pair) for pair in nodes)
 return out,draws,receipts

def nuisance(native,kind,length):
 wave=[];inputs=[];receipts=[]
 for start in range(0,length,512):
  g=Graph();nodes=[]
  for i in range(start,min(start+512,length)):
   t=i/8
   if kind=='slow_chirp':
    w=1+.1*t/616;phase=t+.05*t*t/616
    vals=[rounded(-8*w**(2/3)),rounded(math.cos(2*phase)),rounded(math.sin(2*phase))]
    a,c,s=[g.value(x,{'nuisance':kind,'sample':i,'constant':k}) for k,x in enumerate(vals)]
    pair=[g.op('MULTIPLY',a,c),g.op('MULTIPLY',a,s)]
   else:
    inc=.6+.2*math.sin(.03*t);psi=.3*math.sin(.017*t)
    vals=[rounded(math.cos(inc)),rounded(math.cos(2*t)),rounded(math.sin(2*t)),rounded(math.cos(2*psi)),rounded(math.sin(2*psi))]
    ci,c,s,cp,sp=[g.value(x,{'nuisance':kind,'sample':i,'constant':k}) for k,x in enumerate(vals)]
    hp=g.op('MULTIPLY',g.value(-4,'quadrupole inclination factor'),g.op('MULTIPLY',g.op('ADD',g.value(1,'unit'),g.op('MULTIPLY',ci,ci)),c))
    hx=g.op('MULTIPLY',g.value(-8,'quadrupole cross coefficient'),g.op('MULTIPLY',ci,s))
    pair=[g.op('SUBTRACT',g.op('MULTIPLY',cp,hp),g.op('MULTIPLY',sp,hx)),g.op('ADD',g.op('MULTIPLY',sp,hp),g.op('MULTIPLY',cp,hx))]
   inputs.append([str(v) for v in vals]);nodes.append(pair)
  values,rec=native.evaluate(g,'Test3: '+kind+' unmodulated nuisance channels from declared adiabatic phase/projection inputs')
  receipts.append(rec);wave.extend(tuple(values[v] for v in pair) for pair in nodes)
 return wave,inputs,receipts

def analyze(native,store,name,wave,trigs,source,noise,tolerance,execution):
 raw=store.record(name+'.raw','raw_waveform',serial({'samples':wave,'dt':'1/8','sample_indices':list(range(len(wave))),'noise':noise}),parents=[source],execution=execution)
 alternatives=[]
 for size in (2,4):
  coeff,pred,res,norm,receipts=fit_and_residual(native,wave,trigs,size)
  err=max(abs(v) for row in res[128:192] for v in row);adequate=err<=tolerance
  fit=store.record(name+'.fit'+str(size),'source_fit',serial({'coefficients':coeff,'predicted_samples':pred,'model_coefficients':size,'calibration':[0,128],'holdout':[128,192],'holdout_error':err,'tolerance':tolerance,'adequate':adequate}),parents=[raw],execution=receipts)
  residual=store.record(name+'.residual'+str(size),'residual_history',serial({'signed_samples':res,'norm_squared':norm,'raw_sample_indices':list(range(len(wave)))}),parents=[raw,fit],execution=receipts)
  data=symbols(res,norm,coeff);sym=store.record(name+'.symbols'+str(size),'candidate_symbolization',data,parents=[residual])
  alternatives.append({'fit':fit,'residual':residual,'symbols':sym,'data':data,'adequate':adequate,'holdout_error':float(err)})
 good=[a for a in alternatives if a['adequate']];chosen=good[0] if good else alternatives[0]
 info,receipt=tests(native,chosen['data']);ir=store.record(name+'.information','information_tests',info,parents=[chosen['symbols'],chosen['residual']],execution=[receipt])
 lineage={'raw_waveform':raw,'source_fit':chosen['fit'],'residual_history':chosen['residual'],'candidate_symbolization':chosen['symbols'],'information_tests':ir}
 return {'lineage':lineage,'alternatives':alternatives,'chosen':chosen,'info':info,'adequate':bool(good),'stable':bool(good) and all(pattern(a['data'])==pattern(chosen['data']) for a in good)}

def finish(store,name,item,physical):
 physical=[{'name':'quiet_fit','status':'PASS' if item['adequate'] else 'FAIL','evidence':item['lineage']['source_fit']},
 {'name':'fit_alternative_stability','status':'PASS' if item['stable'] else 'FAIL','evidence':[a['symbols'] for a in item['alternatives']]}]+physical
 control=store.record(name+'.controls','control_results',{'physical_controls':physical,'statistical_controls':[{'name':'repetition_permutation','status':'PASS' if item['info']['pass'] else 'FAIL','evidence':item['lineage']['information_tests']}]},parents=list(item['lineage'].values()))
 gate=admission(store,name+'.admission',item['lineage'],control);ok=store.payload(gate)['eligible'];decoded=None;exact=None
 if ok:
  decoded=decode(store,name+'.decoded',gate)
  exact=any(h['interval_integers']==[2,3,5,7,11,13,17] for h in store.payload(decoded)['hypotheses'])
  store.record(name+'.evaluation','post_decode_evaluation',{'exact_seven_prime_payload':exact},parents=[decoded])
 summary={'admission':gate,'admitted':ok,'decoded':decoded,'exact_payload':exact,'fit_adequate':item['adequate'],'fit_alternatives_agree':item['stable'],'markers':len(item['chosen']['data']['markers']),'repeats':item['info']['observed_repetition'],'p':item['info']['permutation_p'],'statistical_pass':item['info']['pass'],'holdout_errors':[a['holdout_error'] for a in item['alternatives']]}
 print(name+': '+json.dumps({k:v for k,v in summary.items() if k not in ('admission','decoded')}),flush=True)
 store.verify(gate);return summary

def scaling(native,store,prime,null,source_refs,contract):
 g=Graph()
 def v(x,label):return g.value(F(str(x)),label)
 def mul(a,b):return g.op('MULTIPLY',a,b)
 def div(a,b):return g.op('DIVIDE',a,b)
 def power(a,n):
  out=v(1,'multiplicative identity')
  for _ in range(n):out=mul(out,a)
  return out
 G=v(contract['constants']['G_SI'],'SI gravitational constant');c=v(contract['constants']['c_m_s'],'exact speed of light');pc=v(contract['constants']['parsec_m'],'parsec in metres')
 out={}
 for s in contract['sources']:
  m=v(s['mass_each_kg'],'body mass kg');r=v(s['radius_each_m'],'individual orbital radius m')
  w2=div(mul(G,m),mul(v(4,'equal mass Kepler factor'),power(r,3)))
  eu=mul(m,mul(power(r,2),w2));fu=mul(m,mul(r,w2))
  luminosity=div(mul(v(F(2,5),'equal-mass circular quadrupole luminosity factor'),mul(power(G,4),power(m,5))),mul(power(c,5),power(r,5)))
  tc=div(mul(v(F(5,32),'equal-mass Newtonian merger-time coefficient'),mul(power(c,5),power(r,4))),mul(power(G,3),power(m,3)))
  rows=[]
  for distance in contract['distances_pc']:
   R=mul(pc,v(distance,'distance pc'));k=div(mul(G,eu),mul(power(c,4),R))
   rows.append({'distance_pc':distance,'prefactor':k,'carrier_amplitude':mul(v(8,'dimensionless face-on carrier amplitude'),k)})
  out[s['name']]={'omega_squared':w2,'energy_unit_J':eu,'force_unit_N':fu,'positive_work_marker_J':mul(eu,v(F(1073,4352),'retained exact dimensionless positive work')),'positive_work_22markers_J':mul(eu,v(F(11803,2176),'retained full reference work')),'sampled_peak_force_squared_N2':mul(power(fu,2),v(F(9790641,21381376),'retained sampled dimensionless force squared')),'circular_GW_power_W':luminosity,'circular_merger_time_s':tc,'distances':rows}
 vals,receipt=native.evaluate(g,'Test2: dimensional Kepler constraint, strain prefactor, force/work scales, circular GW luminosity and inspiral timescale')
 converted={}
 for name,d in out.items():
  converted[name]={k:str(vals[node]) for k,node in d.items() if k!='distances'}
  converted[name]['distances']=[{'distance_pc':row['distance_pc'],**{k:str(vals[n]) for k,n in row.items() if k!='distance_pc'}} for row in d['distances']]
 ref=store.record('test2.scaling','dimensional_source',converted,parents=source_refs,execution=[receipt])
 asd=np.loadtxt(HERE/'sources/aLIGODesign.txt');hp=np.array([float(row[0]) for row in prime]);base=np.array([float(row[0]) for row in null]);delta=hp-base;N=len(hp)
 output={};spectrum_refs=[]
 for model in contract['sources']:
  name=model['name'];d=converted[name];omega=math.sqrt(float(F(d['omega_squared'])));dt=1/(8*omega);df=1/(N*dt)
  freq=np.fft.rfftfreq(N,dt);valid=(freq>=asd[0,0])&(freq<=asd[-1,0]);freq=freq[valid];curve=np.exp(np.interp(np.log(freq),np.log(asd[:,0]),np.log(asd[:,1])))
  arrays={'carrier_hann':base*np.hanning(N),'modulation':delta};spectra={key:np.abs(np.fft.rfft(a)[valid])**2 for key,a in arrays.items()}
  inp=store.record('test2.'+name+'.spectral_inputs','spectral_inputs',{'frequency_Hz':freq.tolist(),'ASD_per_sqrt_Hz':curve.tolist(),'FFT_magnitude_squared':{k:a.tolist() for k,a in spectra.items()},'dt_s':dt,'df_Hz':df,'convention':contract['spectrum']},parents=[ref])
  g=Graph();nodes={}
  for key,a in spectra.items():
   terms=[g.op('DIVIDE',g.value(rounded(p),{'FFT_power':key,'bin':i}),g.value(rounded(n*n),{'interpolated_PSD_bin':i})) for i,(p,n) in enumerate(zip(a,curve))]
   total=g.op('MULTIPLY',g.value(rounded(4*df*dt*dt),'one-sided Fourier normalization'),g.sum(terms))
   nodes[key]=[]
   for row in d['distances']:
    k=g.value(F(row['prefactor']),'native dimensional strain prefactor')
    nodes[key].append(g.op('MULTIPLY',total,g.op('MULTIPLY',k,k)))
  values,rec=native.evaluate(g,'Test2: single-detector one-sided design-PSD weighted spectral norms for carrier and known modulation residual, each distance')
  snrs={k:[math.sqrt(float(values[n])) for n in ns] for k,ns in nodes.items()}
  duration=616/omega;energy=float(F(d['energy_unit_J']));power_gw=float(F(d['circular_GW_power_W']))
  result={'mass_each_kg':float(model['mass_each_kg']),'radius_each_m':model['radius_each_m'],'omega_rad_s':omega,'GW_frequency_Hz':omega/math.pi,'duration_s':duration,'v_over_c':omega*model['radius_each_m']/299792458,'circular_GW_power_W':power_gw,'circular_merger_time_s':float(F(d['circular_merger_time_s'])),'baseline_radiated_energy_over_binding':power_gw*duration/energy,'positive_work_marker_J':float(F(d['positive_work_marker_J'])),'positive_work_22markers_J':float(F(d['positive_work_22markers_J'])),'sampled_peak_force_N':math.sqrt(float(F(d['sampled_peak_force_squared_N2']))),'distances':[]}
  for j,row in enumerate(d['distances']):
   k=float(F(row['prefactor']));R=row['distance_pc']*float(contract['constants']['parsec_m']);result['distances'].append({'distance_pc':row['distance_pc'],'h_carrier':float(F(row['carrier_amplitude'])),'h_modulation_peak_plus':float(np.max(np.abs(delta)))*k,'h_modulation_rms_plus':float(np.sqrt(np.mean(delta**2)))*k,'rho_carrier_hann':snrs['carrier_hann'][j],'rho_known_modulation':snrs['modulation'][j],'distance_over_wavelength':R/(299792458/(omega/math.pi))})
  result['rho8_reference_distance_pc']=result['distances'][1]['rho_known_modulation']*1000/8
  sr=store.record('test2.'+name+'.detectability','detectability',result,parents=[ref,inp],execution=[rec]);output[name]={'evidence':sr,**result};spectrum_refs.append(sr)
 store.write('TEST2_RESULT',output);print('TEST2 COMPLETE '+json.dumps(output),flush=True);return output

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--run',default='run001');args=ap.parse_args();assert args.run.isalnum()
 run=HERE/args.run;run.mkdir(exist_ok=False);snap=run/'code';snap.mkdir();refs=[]
 paths=[Path(__file__),HERE/'CONTRACT.json',HERE/'sources/aLIGODesign.txt',PRE/'run.py',*sorted((ROOT/'GW_COM/runtime').glob('*.py'))]
 for i,p in enumerate(paths):
  dest=snap/(str(i)+'_'+p.name);shutil.copyfile(p,dest);refs.append({'path':str(dest.relative_to(ROOT)),'sha256':hashlib.sha256(dest.read_bytes()).hexdigest()})
 method=run/'METHOD.json';method.write_bytes(encode({'schema':'GW_COM_METHOD_V1','refs':refs}));store=Store(ROOT,run/'records',method,units={'waveform':'dimensionless two-channel continuous source until explicit SI scaling','time':'dt=1/8 dimensionless; SI conversion explicit in Test2'})
 contract=read(HERE/'CONTRACT.json');sources={};waves={}
 for kind in ('prime','unmodulated'):
  sources[kind],data=prior(store,'continuous_'+kind+'.source');waves[kind]=[tuple(map(F,row)) for row in data['waveform']]
 trigs=[tuple(map(F,row)) for row in data['trig_inputs']]
 dynamics={kind:store.ref(PRE/'refinement001/records'/f'continuous_{kind}.dynamics.json') for kind in waves}
 for ref in dynamics.values():store.verify(ref);assert store.payload(ref)['pass']
 with DomainSession.start('STARBREAKER',objective='Exactly three GW-COM tests: continuous Gaussian SNR sweep, SI detectability, natural-carrier false positives; fixed contract and no expansion',output_root=run/'sessions',receipt_storage='gzip') as session:
  print(session.announcement(),flush=True);native=Native(session);result={}
  # Test 1: use native source-bound squared energy for disclosed SNR definitions.
  g=Graph();energy=[];carrier=[]
  for i,(p,b) in enumerate(zip(waves['prime'],waves['unmodulated'])):
   for j in (0,1):
    a=g.value(p[j],{'prime_sample':i,'channel':j});n=g.value(b[j],{'null_sample':i,'channel':j});d=g.op('SUBTRACT',a,n);energy.append(g.op('MULTIPLY',d,d));carrier.append(g.op('MULTIPLY',n,n))
  en=g.sum(energy);bn=g.sum(carrier);values,rec=native.evaluate(g,'Test1: exact noiseless continuous modulation energy and carrier energy defining RMS and coherent SNR')
  energy_ref=store.record('test1.snr_definition','snr_definition',{'modulation_sum_squares':str(values[en]),'carrier_sum_squares':str(values[bn]),'channel_samples':2*len(trigs)},parents=list(sources.values()),execution=[rec])
  t1={}
  for sigma_text in contract['test_1']['sigma_per_channel']:
   sigma=F(sigma_text)
   for seed in contract['test_1']['seeds']:
    prefix='noise_s'+str(sigma.denominator)+'_'+str(seed);items={}
    for kind in ('prime','unmodulated'):
     name=prefix+'_'+kind;print('START '+name,flush=True)
     wave,draws,receipts=noisy(native,waves[kind],sigma,seed)
     noise=store.record(name+'.noise','noise_realization',{'standard_normal_samples':serial(draws),'sigma':str(sigma),'seed':seed})
     items[kind]=analyze(native,store,name,wave,trigs,sources[kind],noise,6*sigma+F(1,10**10),receipts)
    null_ok=items['unmodulated']['info']['observed_repetition']==0
    for kind,item in items.items():
     name=prefix+'_'+kind;summary=finish(store,name,item,[{'name':'source_dynamics','status':'PASS','evidence':dynamics[kind]}, {'name':'matched_unmodulated','status':'PASS' if null_ok else 'FAIL','evidence':items['unmodulated']['lineage']['information_tests']}])
     summary.update(sigma=float(sigma),seed=seed,kind=kind,modulation_rms_snr=math.sqrt(float(values[en])/(2*len(trigs)))/float(sigma),optimal_two_channel_modulation_snr=math.sqrt(float(values[en]))/float(sigma),carrier_rms_snr=math.sqrt(float(values[bn])/(2*len(trigs)))/float(sigma));t1[name]=summary
  store.write('TEST1_RESULT',t1);result['test1']=t1;print('TEST1 COMPLETE',flush=True)
  result['test2']=scaling(native,store,waves['prime'],waves['unmodulated'],list(sources.values()),contract['test_2'])
  t3={}
  for kind in contract['test_3']['cases']:
   print('START nuisance '+kind,flush=True);wave,inputs,receipts=nuisance(native,kind,len(trigs))
   source=store.record('test3.'+kind+'.source','source_history',serial({'samples':wave,'declared_constants':inputs,'definition':contract['test_3'][kind],'dt':'1/8','intentional_modulation':False}),execution=receipts)
   item=analyze(native,store,'test3.'+kind,wave,trigs,source,'none',F(1,10**10),[])
   summary=finish(store,'test3.'+kind,item,[]);summary['false_positive_statistical']=item['info']['pass'];summary['any_repeated_packet']=item['info']['observed_repetition']>=2;t3[kind]=summary
  store.write('TEST3_RESULT',t3);result['test3']=t3
  result.update(test_count=3,session=str(session.directory.relative_to(ROOT)),native_call_count=len(native.calls),native_nodes=sum(c['nodes'] for c in native.calls),native_calls=native.calls)
  store.write('RUN_RESULT',result);print('ALL THREE TESTS COMPLETE; '+str(len(native.calls))+' native calls',flush=True)

if __name__=='__main__':main()
