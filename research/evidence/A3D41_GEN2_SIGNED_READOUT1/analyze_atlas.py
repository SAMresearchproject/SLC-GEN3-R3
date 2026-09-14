"""Native exact response differences, inverse fibers and probe information.

Data indexing/selection are orchestration; GEN2 computes every difference,
fiber, entropy and entropy comparison. Fractions below are used only in the
explicit independent arithmetic check.
"""
from pathlib import Path
import json
import sys
from itertools import combinations
from fractions import Fraction
ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT))
from SAM_PROJECT.session import DomainSession
from SAM_PROJECT.receipt_storage import read_record
HERE = Path(__file__).resolve().parent
SESSION = ROOT / 'SAM_REVIEW/campaigns/PROJECT_DOMAIN_SESSIONS1/sessions/ATOM3D_c51c939ff7ce489196cfb2aa0bcbfc43'
def load(name): return json.loads((HERE/name).read_text())
def save(name, value): (HERE/name).write_text(json.dumps(value, indent=2, sort_keys=True)+'\n')

def main():
    atlas, words = load('ATLAS.json'), load('WORDS.json')
    session = DomainSession(SESSION)
    known = set((SESSION/'calls').iterdir())
    calls=load('ANALYSIS_CALLS.json') if (HERE/'ANALYSIS_CALLS.json').exists() else []
    replay={(c['operation'],c['purpose']):c for c in calls}
    def execute(op, payload, purpose):
        nonlocal known
        if (op,purpose) in replay:
            prior=replay[op,purpose]
            directory=ROOT/prior['directory']
            request=json.loads(read_record(directory/'INPUT.json','gzip'))
            assert request['payload']==payload, 'Saved native call input differs'
            # Move the reused receipt to the current end so callers cite it.
            calls.remove(prior); calls.append(prior)
            return json.loads(read_record(directory/'OUTPUT.json','gzip'))
        result = session.execute(op, payload, purpose=purpose)
        current=set((SESSION/'calls').iterdir()); added=current-known
        assert len(added)==1
        calls.append({'operation':op,'purpose':purpose,'directory':str(added.pop().relative_to(ROOT))})
        known=current; save('ANALYSIS_CALLS.json', calls)
        return result
    rows = {(r['configuration']['state'],r['configuration']['cover'],r['configuration']['assignment']):r for r in atlas}
    states = sorted({w['before'] for w in words})
    probes = [(e,s) for e in range(9) for s in (1,-1)]
    wordmap = {(w['before'],w['edge'],w['sign']):w for w in words}
    # Exact native arithmetic on new perturbation outputs. All input leaves bind
    # the construction receipt that computed them; the prior graph survives.
    deltas=[]; checks=[]
    for cover in (3,4):
        for assignment in range(6):
            nodes=[]
            for state in sorted({r['configuration']['state'] for r in atlas}):
                r=rows[state,cover,assignment]
                nodes.append({'id':f's{state}','op':'VALUE','value':r['observed'], 'source': {'receipt':r['receipt'],'quantity':'EXTERIOR:observed','unit':'CANDIDATE_SOURCE_ACTION'}})
            for w in words:
                nodes.append({'id':f"d{w['before']}_{w['edge']}_{w['sign']}",'op':'SUBTRACT','left':f"s{w['after']}",'right':f"s{w['before']}"})
            result=execute('GEN2_SIGNED_LOG',{'representation':'RATIONAL','nodes':nodes},f'Calculate all 288 signed one-Write source-action changes natively, cover {cover}, placement {assignment}.')
            lookup={n['id']:n for n in result['nodes']}
            for w in words:
                delta=lookup[f"d{w['before']}_{w['edge']}_{w['sign']}"]['value']
                checks.append(Fraction(delta)==Fraction(rows[w['after'],cover,assignment]['observed'])-Fraction(rows[w['before'],cover,assignment]['observed']))
                deltas.append({'state':w['before'],'cover':cover,'assignment':assignment,'edge':w['edge'],'sign':w['sign'],'delta':delta,'receipt':calls[-1]['directory']})
            save(f'ARITHMETIC_C{cover}_A{assignment}_CHECKPOINT.json',result['checkpoint'])
            print(f'Native signed differences complete: cover {cover}, placement {assignment}',flush=True)
    save('DELTAS.json',deltas)
    dmap={(d['state'],d['cover'],d['assignment'],d['edge'],d['sign']):d['delta'] for d in deltas}
    all_sources=[{'state':s,'cover':c,'assignment':a} for s in states for c in (3,4) for a in range(6)]
    contracts={}; profiles={}
    def contract(roster, selected, extra_sites=False):
        records=[]
        for src in roster:
            s,c,a=src['state'],src['cover'],src['assignment']
            visible=[dmap[s,c,a,e,sign] for e,sign in selected]
            if extra_sites: visible.append(rows[s,c,a]['sites'])
            records.append({'source':src,'visible':visible})
        return {'records':records,'target':'ORIGINAL_LI6_STATE_COVER_PLACEMENT','known_information':{'rho':1,'selected_minimum_family':'H000976','known_initial_state':roster[0]['state'] if len({r['state'] for r in roster})==1 else None,'probes':[list(p) for p in selected],'signed_sites_observed':extra_sites},
                'source_contract':{'campaign':'A3D41_GEN2_SIGNED_READOUT1','native_atlas_receipts':sorted({r['receipt'] for r in atlas}),'transition_receipts':'WORDS.json','response_arithmetic_receipts':'DELTAS.json'}}
    def profile(label, roster, selected, extra_sites=False):
        spec=contract(roster,selected,extra_sites)
        result=execute('GEN2_CUSTODY',{'contract':spec,'action':'profile'},f'Native exact inverse partition and information for {label}; all source alternatives and ties retained.')
        profiles[label]={'profile':result['native_profile'],'receipt':calls[-1]['directory'],'probes':[list(p) for p in selected]}
        contracts[label]=spec
        save('PROFILES.json',profiles)
        p=result['native_profile']
        print(label,p['visible_output_count'],p['expected_hidden_information']['exact_nats'],flush=True)
        return p
    known_sources=[r for r in all_sources if r['state']==14336]
    for label,roster in [('KNOWN_STATE',known_sources),('UNKNOWN_STATE',all_sources)]:
        profile(label+'_BASE',roster,[])
        profile(label+'_ALL18',roster,probes)
        for edge,sign in probes:
            profile(f'{label}_E{edge}_{sign}',roster,[(edge,sign)])
    # Native exact logarithmic comparison ranks single probes without rounding.
    def terms(p): return [[x['prime'],x['coefficient']] for x in p['expected_hidden_information']['prime_log_coefficients']]
    rankings={}
    for mode in ('KNOWN_STATE','UNKNOWN_STATE'):
        best=[]; bestp=None
        for edge,sign in probes:
            label=f'{mode}_E{edge}_{sign}'; p=profiles[label]['profile']
            if bestp is None: best=[label];bestp=p;continue
            result=execute('GEN2_FORMAL_LOG',{'terms':terms(p),'compare_terms':terms(bestp)},f'Exact native entropy comparison for {label} against current best probe; minimize unresolved information.')
            if result['exact_comparison']<0: best=[label];bestp=p
            elif result['exact_comparison']==0: best.append(label)
        rankings[mode]={'best_single_probes_all_ties':best,'remaining_information':bestp['expected_hidden_information']}
    save('RANKINGS.json',rankings)
    # Search all unordered positive-orientation two-probe choices, plus signed
    # site data on the full transcript. This is a declared bounded probe roster.
    for e,f in combinations(range(9),2):
        profile(f'KNOWN_STATE_PAIR_{e}_{f}',known_sources,[(e,1),(f,1)])
        profile(f'UNKNOWN_STATE_PAIR_{e}_{f}',all_sources,[(e,1),(f,1)])
    profile('UNKNOWN_STATE_ALL18_AND_SITES',all_sources,probes,True)
    # Observation-only exact inverses are queried for each distinct complete
    # transcript; supplied custody is not treated as measured information.
    fibers=[]
    for label in ('KNOWN_STATE_ALL18','UNKNOWN_STATE_ALL18','UNKNOWN_STATE_ALL18_AND_SITES'):
        spec=contracts[label]; values={json.dumps(r['visible'],sort_keys=True):r['visible'] for r in spec['records']}
        groups=[]
        for visible in values.values():
            members=execute('GEN2_CUSTODY',{'contract':spec,'action':'fiber','visible':visible},f'Compute complete observation-only inverse fiber for {label}.')
            groups.append({'visible':visible,'members':members,'receipt':calls[-1]['directory']})
        fibers.append({'label':label,'groups':groups})
    save('FIBERS.json',fibers)
    save('CHECKS.json',{'independent_exact_subtractions':len(checks),'passed':sum(checks),'all_passed':all(checks),
        'baseline_observed_actions':sorted({str(rows[s,c,a]['observed']) for s in states for c in (3,4) for a in range(6)}),
        'source_configurations':len(all_sources),'perturbation_contexts':len(deltas),
        'notes':'Independent Python Fraction subtraction verifies native arithmetic. Native construction/information outputs are the research calculations.'})
    save('ANALYSIS_RUN.json',{'status':'RETURNED','native_calls':len(calls),'profiles':len(profiles)})
    session.close()

if __name__=='__main__':main()
