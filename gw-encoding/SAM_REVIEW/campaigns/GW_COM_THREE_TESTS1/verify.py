"""Arithmetic/custody verification of the three saved experiments; no new simulations."""
from pathlib import Path
from fractions import Fraction as F
import json,math,random,sys
import numpy as np
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[2];sys.path.insert(0,str(ROOT))
from GW_COM.runtime.evidence import Store,encode
from GW_COM.runtime.information import framing,max_repetition

def main():
 run=HERE/'run001';directory=run/'records';store=Store(ROOT,directory,run/'METHOD.json');load=lambda n:json.loads((directory/(n+'.json')).read_text())
 result=load('RUN_RESULT');assert result['test_count']==3 and len(result['test1'])==12 and len(result['test3'])==2
 records=0;seen=set()
 for p in directory.glob('*.json'):
  d=json.loads(p.read_text())
  if d.get('schema')=='GW_COM_EVIDENCE_V1':store.verify(store.ref(p),seen);records+=1
 predecessor=ROOT/'SAM_REVIEW/campaigns/GW_COM_CONTINUOUS1/run001/records'
 source={k:json.loads((predecessor/f'continuous_{k}.source.data.json').read_text()) for k in ('prime','unmodulated')}
 trigs=[tuple(map(F,row)) for row in source['prime']['trig_inputs']]
 count=0;raw_checked=0;normal_equations=0;statistical_checks=0
 cases=list(result['test1'])+['test3.'+k for k in result['test3']]
 for name in cases:
  raw=load(name+'.raw.data');wave=[tuple(map(F,row)) for row in raw['samples']]
  if name.startswith('noise_'):
   d=load(name+'.noise.data');rng=random.Random(d['seed']);sigma=F(d['sigma']);kind=name.rsplit('_',1)[1];base=source[kind]['waveform']
   for i,pair in enumerate(d['standard_normal_samples']):
    for j in (0,1):
     x=F(format(rng.gauss(0,1),'.12g'));assert x==F(pair[j]);assert wave[i][j]==F(base[i][j])+sigma*x;raw_checked+=1
  else:
   src=load(name+'.source.data');kind=name.split('.')[-1]
   for i,pair in enumerate(wave):
    vals=list(map(F,src['declared_constants'][i]))
    if kind=='slow_chirp':a,c,s=vals;expected=(a*c,a*s)
    else:
     ci,c,s,cp,sp=vals;hp=-4*(1+ci*ci)*c;hx=-8*ci*s;expected=(cp*hp-sp*hx,sp*hp+cp*hx)
    assert pair==expected;raw_checked+=2
  for size in (2,4):
   fit=load(name+'.fit'+str(size)+'.data');res=load(name+'.residual'+str(size)+'.data');coeff=list(map(F,fit['coefficients']));normal=[F(0)]*size
   for i,(p,row) in enumerate(zip(fit['predicted_samples'],res['signed_samples'])):
    c,s=trigs[i];bases=([c,-s,F(1),F(0)][:size],[s,c,F(0),F(1)][:size]);rr=list(map(F,row))
    for j in (0,1):
     forecast=sum(a*b for a,b in zip(coeff,bases[j]));assert forecast==F(p[j]);assert wave[i][j]-forecast==rr[j];count+=1
     if i<128:
      for k,b in enumerate(bases[j]):normal[k]+=b*rr[j]
    assert sum(v*v for v in rr)==F(res['norm_squared'][i])
   assert all(v==0 for v in normal);normal_equations+=size
   error=max(abs(F(v)) for row in res['signed_samples'][128:192] for v in row);assert error==F(fit['holdout_error']);assert fit['adequate']==(error<=F(fit['tolerance']))
  info=load(name+'.information.data');null=info['permutations'];observed=info['observed_repetition']
  for surrogate in null:
   markers=[0]
   for gap in surrogate['gap_order']:markers.append(markers[-1]+gap)
   frames=framing(markers,7) if surrogate['gap_order'] else []
   assert max_repetition(frames)[0]==surrogate['repetition_count']
  expected=F(1+sum(row['repetition_count']>=observed for row in null),len(null)+1)
  assert expected==F(info['permutation_p']);assert info['pass']==(observed>=2 and expected<=F(1,20));statistical_checks+=1
  gate=load(name+'.admission.data');control=store.payload(gate['controls']);eligible=all(rows and all(row['status']=='PASS' for row in rows) for rows in (control['physical_controls'],control['statistical_controls'])) and info['pass'];assert gate['eligible']==eligible
  if not eligible:assert not (directory/(name+'.decoded.json')).exists()
 scaled=load('test2.scaling.data');G=6.67430e-11;c=299792458;pc=3.085677581491367e16
 for name,row in result['test2'].items():
  m=row['mass_each_kg'];r=row['radius_each_m'];w=math.sqrt(G*m/(4*r**3));assert math.isclose(w,row['omega_rad_s'],rel_tol=1e-14)
  for dist in row['distances']:
   h=2*G*G*m*m/(c**4*r*dist['distance_pc']*pc);assert math.isclose(h,dist['h_carrier'],rel_tol=1e-13)
  ds=row['distances'];assert math.isclose(ds[0]['h_carrier']/ds[-1]['h_carrier'],1e6,rel_tol=1e-13)
  assert math.isclose(row['circular_GW_power_W'],32/5*G**4*(m/2)**2*(2*m)**3/(c**5*(2*r)**5),rel_tol=1e-13)
  assert math.isclose(row['circular_merger_time_s'],5*c**5*(2*r)**4/(256*G**3*(m/2)*(2*m)**2),rel_tol=1e-13)
  sp=load('test2.'+name+'.spectral_inputs.data');dt=sp['dt_s'];df=sp['df_Hz'];psd=np.array(sp['ASD_per_sqrt_Hz'])**2
  for kind,key in [('modulation','rho_known_modulation'),('carrier_hann','rho_carrier_hann')]:
   norm=4*df*dt*dt*np.sum(np.array(sp['FFT_magnitude_squared'][kind])/psd)
   for j,dist in enumerate(row['distances']):
    k=float(F(scaled[name]['distances'][j]['prefactor']));rho=math.sqrt(norm)*k;assert math.isclose(rho,dist[key],rel_tol=1e-12)
 report={'status':'PASS','scientific_experiments':3,'new_scientific_runs_during_verification':0,'evidence_records':records,'raw_channel_samples_checked':raw_checked,'exact_prediction_and_residual_channel_samples_checked':count,'normal_equations_checked':normal_equations,'full_search_permutation_rank_results_checked':statistical_checks,'physical_scalings_checked':2,'distance_rows_checked':6,'scope':'Hashes, serialization, source addition/projection, exact algebra, statistical ranks and SI/SNR arithmetic; no new grid points'}
 with (run/'VALIDATION.json').open('xb') as f:f.write(encode(report))
 print(json.dumps(report,indent=2))

if __name__=='__main__':main()
