import json,csv,hashlib
from pathlib import Path
ROOT=Path(__file__).resolve().parent; BRANCH=ROOT.parent

def load(rel): return json.loads((BRANCH/rel).read_text(encoding='utf-8'))
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
    paths=[('CR018','CR018_A0_CHI_BARYON_INVENTORY_DERIVATION/CR018_summary.json'),('CR019','CR019_EFFECTIVE_MATTER_INVENTORY_REFINEMENT/CR019_summary.json'),('CR020','CR020_CMB_BOUNDARY_AND_ACOUSTIC_CONCEPT_CHAIN/CR020_summary.json'),('CR021','CR021_PLANCK_LITE_CMB_DENSITY_AND_BBN_CONTACT/CR021_summary.json'),('CR022','CR022_PRECISION_CMB_EXTENSION_FROM_sam_precision_cmb/CR022_summary.json')]
    comps=[(k,load(p)) for k,p in paths]
    rows=[{'component':k,'verdict':v['verdict'],'scientific_verdict':v['scientific_verdict'],'claim_tier':v['claim_tier']} for k,v in comps]
    csvwrite(ROOT/'CR023_component_verdicts.csv',rows)
    ok=(comps[0][1]['scientific_verdict']=='PASS' and comps[1][1]['scientific_verdict']=='PASS' and comps[2][1]['scientific_verdict']=='BOUNDARY_PASS' and comps[3][1]['scientific_verdict']=='BOUNDARY_PASS' and comps[4][1]['scientific_verdict']=='BOUNDARY_PASS')
    verdict='CR023_BOUNDARY_PASS_BARYON_INVENTORY_AND_COSMOLOGY_BRANCH' if ok else 'CR023_FAIL_BARYON_INVENTORY_AND_COSMOLOGY_BRANCH'
    export_claim='SAM derives Ω_b ≈ 0.049299 from native A0/radix structure and horizon quotient χ, then sharpens Ω_m_eff ≈ 0.313761 through the D·χ² directional-cumulant correction. The result feeds scoped CMB-boundary, acoustic, Planck-lite, BBN, and precision-CMB contact branches. Full recombination, perturbation, TT/TE/EE, full Planck likelihood, and theorem-grade CMB closure remain open debts.'
    summary={'test_id':'CR023_BARYON_COSMOLOGY_BRANCH_VERDICT','verdict':verdict,'execution_status':'CLEAN','scientific_verdict':'BOUNDARY_PASS' if ok else 'FAIL','triage_bin':'B' if ok else 'C','claim_tier':'DERIVED_BARYON_INVENTORY_AND_SCOPED_COSMOLOGY_CONTACT_FULL_CMB_BOUNDARIES_PRESERVED','export_claim':export_claim,'scope_boundaries':['not full CMB closure','not full recombination closure','not full perturbation theorem','not full TT/TE/EE theorem closure','not full Planck likelihood','not full distance-triad closure'],'component_verdicts':rows}
    (ROOT/'CR023_summary.json').write_text(json.dumps(summary,indent=2)+'\n',encoding='utf-8')
    lines=['# CR023 Baryon Inventory and Cosmology Branch Verdict','','## Verdict','','```text',verdict,'```','','## Component Verdicts','','| component | verdict | scientific verdict | claim tier |','|---|---|---|---|']
    for r in rows: lines.append(f"| {r['component']} | {r['verdict']} | {r['scientific_verdict']} | {r['claim_tier']} |")
    lines.extend(['','## Export Claim','','```text',export_claim,'```','','## Scope Boundaries','','```text'])
    lines.extend(summary['scope_boundaries']); lines.append('```')
    (ROOT/'CR023_result.md').write_text('\n'.join(lines)+'\n',encoding='utf-8')
    hashwrite([ROOT/'CR023_declared_premises.json',ROOT/'CR023_PRECOMMIT.md',ROOT/'CR023_runner.py',ROOT/'CR023_component_verdicts.csv',ROOT/'CR023_result.md',ROOT/'CR023_summary.json'])
    print(json.dumps(summary,indent=2))
if __name__=='__main__': main()
