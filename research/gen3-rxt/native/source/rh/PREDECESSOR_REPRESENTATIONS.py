"""Open RH exploration frontier: native competing routes and retained exact feedback.

The controller proposes source-bound mutations; GEN3 evaluates and certifies
route priorities, executes representations, and retains the acquired search history.
"""
from fractions import Fraction as Q
from math import isqrt
import json,hashlib
from CURRENT_REVISION.domains.RH.growth import Graph,project_graph
FAMILIES=('WEIGHTED','QUARTIC','COFACTOR','HARMONIC')
OBJECTIVE='Explore available RH representations and combinations to find a route to the original uniform signed-growth bound. Follow new structure, generate follow-up cases, and preserve useful failures.'

def candidate(family,s,t,parent=None,reason=None):
 return dict(id=f'{family.lower()}_s{s}_t{t}',family=family,s=s,t=t,scope='AUXILIARY_UNIFORM_BOUND',
             parent=parent,question=reason or OBJECTIVE)

def choose(engine,pool,answers):
 """Novelty, signed cancellation feedback and underexplored branches compete."""
 done={a['question_id'] for a in answers};pending=[c for c in pool if c['id'] not in done]
 if not pending:return None,None
 visits={f:sum(a.get('family')==f for a in answers) for f in FAMILIES}
 # Every third choice lets an underexplored representation take the lead.
 if len(answers)%3==0:
  least=min(visits[f] for f in FAMILIES if any(c['family']==f for c in pending))
  pending=[c for c in pending if visits[c['family']]==least]
 g=Graph();refs=[]
 for c in pending:
  history=[a for a in answers if a.get('family')==c['family']]
  feedback=history[-1].get('feedback','0') if history else '0'
  unseen=not any(a['s']==c['s'] and a.get('family')==c['family'] for a in answers)
  inherited=next((a.get('feedback','0') for a in reversed(answers) if a['question_id']==c.get('parent')),'0')
  reward=g.add(g.value(1+int(unseen)),g.add(g.value(feedback),g.value(inherited)))
  refs.append(g.div(reward,g.value(1+visits[c['family']])))
 values,native=engine.graph(g);maximum=max(Q(values[r]) for r in refs);ties=[i for i,r in enumerate(refs) if Q(values[r])==maximum]
 cert=Graph();rr=[cert.sub(cert.value(maximum),cert.value(values[r])) for r in refs];cv,cn=engine.graph(cert)
 assert all(Q(cv[r])>=0 for r in rr)
 return pending[ties[0]],dict(native=native,certificate=cn,candidates=[c['id'] for c in pending],ties=ties,policy='Native exact feedback priority; every third selection favors a less explored representation. This is a search policy, not a theorem condition.')

def representation(engine,proxy,family,s,t,source,binding):
 """Execute an alternative representation, keeping its full signed sum."""
 block=[source[str(n)] for n in range(s,2*s)];g=Graph();v=g.value;checks=[]
 if family in ('QUARTIC','COFACTOR'):
  A=isqrt(isqrt(2*s-1))+1;cutoff=(2*s-1)//(A*A)
  tr=proxy.execute('RH_QUARTIC_TRANSPORT',dict(s=s,t=t,source_binding=binding,anchors=[source[str(n)] for n in range(1,cutoff+1)]))
  assert tr['source']==block
  if family=='QUARTIC':
   names=('original','quadratic','transport');read={name:{k:v(x) for k,x in tr['readouts'][name].items()} for name in names}
   cross=g.sub(g.sub(read['transport']['Qhat'],read['original']['Qhat']),read['quadratic']['Qhat'])
   feature=dict(original_energy=read['original']['Qhat'],quadratic_energy=read['quadratic']['Qhat'],transport_energy=read['transport']['Qhat'],joint_cross=cross,
                transport_mean=read['transport']['M'],original_mean=read['original']['M'])
   total=read['transport']['Qhat'];diagonal=g.add(read['original']['Qhat'],read['quadratic']['Qhat'])
  else:
   # The unique A-smooth cofactor partitions the complete transport source.
   primes=[p for p in range(2,A+1) if all(p%d for d in range(2,isqrt(p)+1))]
   low=[];high=[];mu=[v(x) for x in block]
   f={int(n):v(x) for n,x in tr['f'].items()};c={}
   for a,x in f.items():
    for b,y in f.items():c[a*b]=g.add(c.get(a*b,g.zero),g.mul(x,y))
   for i,n in enumerate(range(s,2*s)):
    m=n
    for p in primes:
     while m%p==0:m//=p
    k=n//m;w=g.sum(x for d,x in c.items() if k%d==0)
    val=g.add(g.mul(v(source[str(k)]),v(source[str(m)])),w)
    checks.append(g.sub(val,v(tr['transport'][i])))
    if k<A:checks.append(g.sub(val,g.mul(v(source[str(k)]),g.add(v(1),v(source[str(m)])))))
    low.append(val if k<A else g.zero);high.append(val if k>=A else g.zero)
   built,coefficient_native=engine.graph(g);assert all(Q(built[x])==0 for x in checks)
   lo_result=proxy.execute('RH_PREFIX_PROJECT',dict(s=s,t=t,source=[built[x] for x in low],source_binding=binding))
   hi_result=proxy.execute('RH_PREFIX_PROJECT',dict(s=s,t=t,source=[built[x] for x in high],source_binding=binding))
   g=Graph();v=g.value;checks=[]
   lo={k:v(x) for k,x in lo_result['readouts'].items()};hi={k:v(x) for k,x in hi_result['readouts'].items()}
   total=v(tr['readouts']['transport']['Qhat']);diagonal=g.add(lo['Qhat'],hi['Qhat']);cross=g.sub(total,diagonal)
   feature=dict(low_energy=lo['Qhat'],complement_energy=hi['Qhat'],transport_energy=total,joint_cross=cross,
                low_mean=lo['M'],complement_mean=hi['M'],transport_mean=v(tr['readouts']['transport']['M']))
 elif family=='HARMONIC':
  u=isqrt(2*s-1);S=g.sum(g.div(v(source[str(a)]),v(a)) for a in range(1,u+1));density=g.sub(g.zero,g.mul(S,S))
  coeff={}
  for a in range(1,u+1):
   for b in range(a,u+1):
    term=g.mul(v(source[str(a)]),v(source[str(b)]))
    if a!=b:term=g.mul(v(2),term)
    coeff[a*b]=g.add(coeff.get(a*b,g.zero),term)
  reconstruction=[g.zero for _ in range(s)]
  for k,c in coeff.items():
   for n in range(((s+k-1)//k)*k,2*s,k):reconstruction[n-s]=g.sub(reconstruction[n-s],c)
  for x,y in zip(reconstruction,block):checks.append(g.sub(x,v(y)))
  drift=[density]*s;discrepancy=[g.sub(x,density) for x in reconstruction]
  built,coefficient_native=engine.graph(g);assert all(Q(built[x])==0 for x in checks)
  harmonic_sum=built[S]
  projected=[proxy.execute('RH_PREFIX_PROJECT',dict(s=s,t=t,source=[built[x] for x in array],source_binding=binding)) for array in (reconstruction,drift,discrepancy)]
  g=Graph();v=g.value;checks=[];S=v(harmonic_sum)
  full,a,b=[{k:v(x) for k,x in result['readouts'].items()} for result in projected]
  total=full['Qhat'];diagonal=g.add(a['Qhat'],b['Qhat']);cross=g.sub(total,diagonal)
  feature=dict(original_energy=total,harmonic_drift_energy=a['Qhat'],signed_discrepancy_energy=b['Qhat'],joint_cross=cross,harmonic_sum=S)
 else:raise ValueError('Unknown exploration representation')
 feature['sum_component_energies']=diagonal;feature['joint_energy']=total
 # Cancellation relative to the component budget; signs stay in joint_cross.
 normalized=g.div(cross,g.add(v(1),diagonal))
 values,native=engine.graph(g);assert all(Q(values[x])==0 for x in checks)
 # Native absolute-value certificate for the feedback used by future choices.
 feedback_graph=Graph();value=feedback_graph.value(values[normalized]);absolute=feedback_graph.sub(feedback_graph.zero,value) if Q(values[normalized])<0 else value
 fv,fn=engine.graph(feedback_graph);assert Q(fv[absolute])>=0
 return dict(family=family,features={k:values[x] for k,x in feature.items()},feedback=fv[absolute],exact_equalities=len(checks),native=native,feedback_native=fn,coefficient_native=locals().get('coefficient_native'),projection_receipts=locals().get('projected',locals().get('lo_result')), 
             interpretation='Exact signed representation and component interaction. A discovered finite relation is retained for the uniform derivation.')

def offspring(row,weighted,scales):
 """Mutate stops, switch representations, cross scales and follow large cells."""
 s,t,family=row['s'],row['t'],row['family'];parent=row['question_id'];result=[]
 for f in FAMILIES:
  if f!=family:result.append(candidate(f,s,t,parent,'Follow an acquired result into another representation and look for shared source structure or a new cancellation relation.'))
 # Search both locally and at a different fraction of the block; preserve phase.
 step=max(1,isqrt(s));stops={max(0,t-step),min(s,t+step),max(0,t-1),min(s,t+1),max(0,t-2),min(s,t+2),t//2,(s+t)//2}
 for v in sorted(stops):
  if v!=t:result.append(candidate(family,s,v,parent,'Explore a nearby or displaced stop from an acquired branch; detect unexpected signed structure rather than following a fixed question list.'))
 for scale in (s//2,s*2):
  if scale in scales:result.append(candidate(family,scale,max(1,min(scale,t*scale//s)),parent,'Lift or descend an acquired source pattern to the neighboring dyadic scale.'))
 for cell in weighted['cells']:
  if cell['cell'] in weighted['largest_cells']:
   for v in (cell['l'],min(s,cell['h']+1)):result.append(candidate(family,s,v,parent,'Follow a large returned weighted cell into its stop boundaries and compare source representations.'))
 return result

def discover(engine,rows):
 """Evolve simple exact finite envelopes across all acquired representations.

Every coefficient is explicitly an observed finite envelope, with earlier
violations preserved; none is promoted into a uniform bound.
"""
 if not rows:return {}
 g=Graph();records=[]
 for row in rows:
  r=row['readouts'];features={'one':'1','mean_plus_one':None,'diagonal_plus_one':None,'active_plus_one':None}
  base={'one':g.value(1),'mean_plus_one':g.add(g.value(1),g.value(r['mean_energy'])),
        'diagonal_plus_one':g.add(g.value(1),g.value(r['D_adm'])),
        'active_plus_one':g.add(g.value(1),g.value(r['active_energy']))}
  harmonic=g.sum(g.div(g.value(1),g.value(k)) for k in range(1,row['s']))
  base['harmonic_plus_one']=g.add(g.value(1),harmonic)
  # The grammar combines source features and geometric factors, retaining provenance.
  for a,b in [('one','one'),('mean_plus_one','one'),('harmonic_plus_one','one'),('mean_plus_one','harmonic_plus_one'),('diagonal_plus_one','harmonic_plus_one'),('active_plus_one','one')]:
   denominator=g.mul(base[a],base[b]);ratio=g.div(g.value(r['Qhat']),denominator)
   records.append(dict(case=row['question_id'],expression=a+'*'+b,node=ratio))
 values,native=engine.graph(g);envelopes={}
 for record in records:
  key=record['expression'];value=Q(values[record['node']])
  if key not in envelopes or value>Q(envelopes[key]['coefficient']):envelopes[key]={'coefficient':str(value),'witness':record['case']}
 cert=Graph();margins=[cert.sub(cert.value(envelopes[r['expression']]['coefficient']),cert.value(values[r['node']])) for r in records]
 cv,cn=engine.graph(cert);assert all(Q(cv[x])>=0 for x in margins)
 return dict(envelopes=envelopes,native=native,certificate=cn,scope='OBSERVED_FINITE_ENVELOPES',uniform_bound_status='OPEN',meaning='Candidate expressions generated and compared across acquired cases; coefficients are finite search observations, not an unbounded estimate.')

def remember(proxy,engine,row):
 """Keep runtime measurements as metadata strings in exact native history."""
 account='RH_SEARCH_'+row['question_id']
 state={**row,'seconds':str(row['seconds'])}
 try:
  old=proxy.execute('GEN3_HISTORY_EXPORT',{'account':account})
  assert old['points'][-1]['state']==state
  return 'RECOVERED'
 except KeyError:pass
 g=Graph();action=g.add(g.value(1),g.value(row['feedback']));values,native=engine.graph(g)
 proxy.execute('GEN3_LOG_OPEN',dict(account=account,
       quantity=dict(kind='RH_EXPLORATION_FEEDBACK_PLUS_ONE',units={},scope='HISTORY',sign_convention='POSITIVE_VALUE',normalization={'shift':'1'},source='RH_EXPLORATORY_BRANCH'),
       source_binding=dict(objective=OBJECTIVE,history_role='EXPLORATION_EVIDENCE',formula_context='RH_V3_COMPLETE_FORMULA_CONTEXT',policy='Native exact feedback and underexplored-route selection; source-scoped search evidence'),
       points=[dict(id='start',state={'phase':'BEFORE_SOURCE_ENCOUNTER'},action='1'),dict(id=row['question_id'],state=state,action=values[action])],
       edges=[dict(id='acquire',before='start',after=row['question_id'],event={'kind':'ACQUIRED_EXACT_SOURCE_BRANCH','family':row['family']})]))
 return 'ACQUIRED'
