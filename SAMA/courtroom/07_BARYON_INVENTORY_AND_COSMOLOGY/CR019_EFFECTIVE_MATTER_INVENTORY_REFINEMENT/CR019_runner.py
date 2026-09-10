import json, csv, hashlib
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
    G310=load('../_source_artifacts/summaries/G310_output.json')
    G312=load('../_source_artifacts/summaries/G312_output.json')
    G313=load('../_source_artifacts/summaries/G313_output.json')
    omega=G313['omega']
    Omega_b=omega['omega_b']; Omega_m=omega['omega_m_derived']; Omega_pbh=Omega_m-Omega_b; Omega_vac=1-Omega_m
    pass_conditions={
        'G310_predictions_passed': G310['overall']['all_predictions_pass'] is True,
        'G310_wrong_controls_passed': G310['overall']['all_wrong_controls_pass'] is True,
        'G312_predictions_passed': G312['overall']['all_predictions_pass'] is True,
        'G312_wrong_controls_passed': G312['overall']['all_wrong_controls_pass'] is True,
        'G313_predictions_passed': G313['overall']['all_predictions_pass'] is True,
        'G313_wrong_controls_passed': G313['overall']['all_wrong_controls_pass'] is True,
        'derived_coeff_is_D': close(G313['derived_coeff'],3.0),
        'omega_m_identity': close(Omega_m,0.3137609155690572),
        'omega_b_unchanged': close(Omega_b,0.049299011266100756),
    }
    verdict_pass=all(pass_conditions.values())
    verdict='CR019_PASS_EFFECTIVE_MATTER_INVENTORY_REFINEMENT' if verdict_pass else 'CR019_FAIL_EFFECTIVE_MATTER_INVENTORY_REFINEMENT'
    rows=[{'quantity':'Omega_b','value':Omega_b},{'quantity':'Omega_m_eff','value':Omega_m},{'quantity':'Omega_BB_PBH_trapped','value':Omega_pbh},{'quantity':'Omega_substrate_vacuum','value':Omega_vac},{'quantity':'derived_coeff','value':G313['derived_coeff']}]
    csvwrite(ROOT/'CR019_inventory_rows.csv',rows)
    summary={'test_id':'CR019_EFFECTIVE_MATTER_INVENTORY_REFINEMENT','verdict':verdict,'execution_status':'CLEAN','scientific_verdict':'PASS' if verdict_pass else 'FAIL','triage_bin':'A' if verdict_pass else 'C','claim_tier':'EFFECTIVE_MATTER_INVENTORY_FROM_D_CHI2_DIRECTIONAL_CUMULANT','Omega_b':Omega_b,'Omega_m_eff':Omega_m,'Omega_BB_PBH_trapped':Omega_pbh,'Omega_substrate_vacuum':Omega_vac,'pass_conditions':pass_conditions}
    (ROOT/'CR019_summary.json').write_text(json.dumps(summary,indent=2)+'\n',encoding='utf-8')
    lines=['# CR019 Effective Matter Inventory Refinement','','## Verdict','','```text',verdict,'```','','## Inventory Packet','','```text',f'Omega_b = {Omega_b:.15f}',f'Omega_m_eff = {Omega_m:.15f}',f'Omega_BB_PBH_trapped = {Omega_pbh:.15f}',f'Omega_substrate_vacuum = {Omega_vac:.15f}',f'derived_coeff = {G313["derived_coeff"]}','```','','## Source Tests','','```text','G310 — residual localized to Ω_m side.','G312 — D·χ² correction candidate.','G313 — directional cumulant trace derives D coefficient.','```','','## Pass Conditions','','| condition | pass |','|---|---:|']
    for k,v in pass_conditions.items(): lines.append(f'| {k} | {str(v).lower()} |')
    (ROOT/'CR019_result.md').write_text('\n'.join(lines)+'\n',encoding='utf-8')
    hashwrite([ROOT/'CR019_declared_premises.json',ROOT/'CR019_PRECOMMIT.md',ROOT/'CR019_runner.py',ROOT/'CR019_inventory_rows.csv',ROOT/'CR019_result.md',ROOT/'CR019_summary.json'])
    print(json.dumps(summary,indent=2))
if __name__=='__main__': main()
