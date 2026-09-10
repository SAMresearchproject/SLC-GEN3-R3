import json, csv, math, hashlib
from pathlib import Path
ROOT=Path(__file__).resolve().parent; BRANCH=ROOT.parent

def load(rel): return json.loads((ROOT/rel).resolve().read_text(encoding='utf-8'))
def close(a,b,tol=1e-12): return abs(a-b)<=tol
def sha256(p): h=hashlib.sha256(); h.update(Path(p).read_bytes()); return h.hexdigest()
def csvwrite(p,rows):
    fields=[]
    for r in rows:
        for k in r:
            if k not in fields: fields.append(k)
    with Path(p).open('w',newline='',encoding='utf-8') as f:
        w=csv.DictWriter(f,fieldnames=fields); w.writeheader(); w.writerows(rows)
def hashwrite(paths):
    rows=[]
    for p in sorted(paths,key=lambda p:str(p).lower()):
        if p.name!='HASHES.txt': rows.append(f"{sha256(p)}  {p.relative_to(BRANCH)}")
    (ROOT/'HASHES.txt').write_text('\n'.join(rows)+'\n',encoding='utf-8')
def main():
    prem=load('CR018_declared_premises.json')
    G219=load('../_source_artifacts/summaries/G219_summary.json')
    G219B=load('../_source_artifacts/summaries/G219B_summary.json')
    G219C=load('../_source_artifacts/summaries/G219C_output.json')
    G305=load('../_source_artifacts/summaries/G305_output.json')
    R=prem['sam_inputs']['R']; D=prem['sam_inputs']['D']; exp=prem['expected_values']
    A0=1/(math.pi*R); mu_H=(2**D)/D; chi=mu_H*A0; Omega_b=2*A0*(1-chi)
    pass_conditions={
        'free_parameters_zero': prem['free_parameters_introduced']==0,
        'G219_original_passed_but_reframed': G219.get('all_passed') is True,
        'G219B_corrected_passed': G219B.get('all_passed') is True,
        'G219C_monte_carlo_passed': G219C.get('OVERALL_PASS') is True,
        'G305_predictions_passed': G305['overall']['all_predictions_pass'] is True,
        'G305_wrong_controls_passed': G305['overall']['all_wrong_controls_pass'] is True,
        'A0_identity': close(A0,exp['A0']),
        'mu_H_identity': close(mu_H,exp['mu_H']),
        'chi_identity': close(chi,exp['chi']),
        'Omega_b_identity': close(Omega_b,exp['Omega_b']),
    }
    verdict_pass=all(pass_conditions.values())
    verdict='CR018_PASS_A0_CHI_BARYON_INVENTORY_DERIVATION' if verdict_pass else 'CR018_FAIL_A0_CHI_BARYON_INVENTORY_DERIVATION'
    rows=[{'quantity':'A0','value':A0},{'quantity':'mu_H','value':mu_H},{'quantity':'chi','value':chi},{'quantity':'Omega_b','value':Omega_b}]
    csvwrite(ROOT/'CR018_derived_rows.csv',rows)
    summary={'test_id':prem['test_id'],'verdict':verdict,'execution_status':'CLEAN','scientific_verdict':'PASS' if verdict_pass else 'FAIL','triage_bin':'A' if verdict_pass else 'C','claim_tier':'DERIVED_BARYON_INVENTORY_CANDIDATE','A0':A0,'mu_H':mu_H,'chi':chi,'Omega_b':Omega_b,'pass_conditions':pass_conditions,'source_verdicts':{'G219':G219.get('classification'), 'G219B':G219B.get('classification'), 'G305':G305['overall']['verdict']}}
    (ROOT/'CR018_summary.json').write_text(json.dumps(summary,indent=2)+'\n',encoding='utf-8')
    lines=['# CR018 A0, Chi, and Baryon Inventory Derivation','','## Verdict','','```text',verdict,'```','','## Derived Packet','','```text',f'A0 = {A0:.15f}',f'mu_H = {mu_H:.15f}',f'chi = {chi:.15f}',f'Omega_b = {Omega_b:.15f}','```','','## Source Tests','','```text','G219  — initial chi / matter-budget derivation; retained historical but reframed.','G219B — corrected combinatorial chi derivation.','G219C — Monte Carlo structural confirmation.','G305  — horizon quotient measure under symmetry axioms.','```','','## Pass Conditions','','| condition | pass |','|---|---:|']
    for k,v in pass_conditions.items(): lines.append(f'| {k} | {str(v).lower()} |')
    (ROOT/'CR018_result.md').write_text('\n'.join(lines)+'\n',encoding='utf-8')
    hashwrite([ROOT/'CR018_declared_premises.json',ROOT/'CR018_PRECOMMIT.md',ROOT/'CR018_runner.py',ROOT/'CR018_derived_rows.csv',ROOT/'CR018_result.md',ROOT/'CR018_summary.json'])
    print(json.dumps(summary,indent=2))
if __name__=='__main__': main()
