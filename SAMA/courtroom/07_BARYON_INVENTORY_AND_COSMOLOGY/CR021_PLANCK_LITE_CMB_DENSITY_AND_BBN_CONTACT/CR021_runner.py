import json,csv,hashlib
from pathlib import Path
ROOT=Path(__file__).resolve().parent; BRANCH=ROOT.parent

def load(rel): return json.loads((ROOT/rel).resolve().read_text(encoding='utf-8'))
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
    G379=load('../_source_artifacts/summaries/G379_output.json'); G380=load('../_source_artifacts/summaries/G380_output.json'); G381=load('../_source_artifacts/summaries/G381_output.json'); G382=load('../_source_artifacts/summaries/G382_output.json'); G383=load('../_source_artifacts/summaries/G383_output.json'); G384=load('../_source_artifacts/summaries/G384_output.json'); G396=load('../_source_artifacts/summaries/G396_output.json')
    d=G381['verdict_details']
    pass_conditions={
      'G379_card_frozen': G379['validation_pass_count']==G379['validation_total'],
      'G380_smoke_passed': 'PASS' in G380['verdict'],
      'G381_planck_lite_passed': G381['verdict']=='G381_PASS_PLANCK_LITE_DIAGONAL_CONTACT',
      'G381_primary_better_than_wrong_control': d['primary_better_than_wrong_control'] is True,
      'G382_residuals_passed': G382['prediction_passes']==G382['prediction_total'] and G382['wrong_control_passes']==G382['wrong_control_total'],
      'G383_wrong_controls_passed': G383['prediction_passes']==G383['prediction_total'] and G383['wrong_control_passes']==G383['wrong_control_total'],
      'G384_claim_lock_passed': G384['check_passes']==G384['check_total'],
      'G396_bbn_scoped_passed': G396['check_passes']==G396['check_total'],
    }
    verdict_pass=all(pass_conditions.values())
    verdict='CR021_BOUNDARY_PASS_PLANCK_LITE_CMB_DENSITY_AND_BBN_CONTACT' if verdict_pass else 'CR021_FAIL_PLANCK_LITE_CMB_DENSITY_AND_BBN_CONTACT'
    rows=[
      {'test':'G379','verdict':G379['verdict']},
      {'test':'G380','verdict':G380['verdict']},
      {'test':'G381','verdict':G381['verdict'],'primary_high_l_delta_chi2_per_point':d['primary_high_l_delta_chi2_per_point'],'wrong_control_high_l_delta_chi2_per_point':d['wrong_control_high_l_delta_chi2_per_point']},
      {'test':'G382','verdict':G382['verdict'],'primary_tt_peak_mean_abs_amp_frac':G382['primary_tt_peak_mean_abs_amp_frac'],'primary_ee_peak_mean_abs_amp_frac':G382['primary_ee_peak_mean_abs_amp_frac']},
      {'test':'G383','verdict':G383['verdict'],'primary_delta_chi2_per_point':G383['primary_delta_chi2_per_point']},
      {'test':'G384','verdict':G384['verdict']},
      {'test':'G396','verdict':G396['verdict'],'omega_b_h2_primary':G396['omega_b_h2_primary'],'eta10_primary':G396['eta10_primary']},
    ]
    csvwrite(ROOT/'CR021_contact_rows.csv',rows)
    summary={'test_id':'CR021_PLANCK_LITE_CMB_DENSITY_AND_BBN_CONTACT','verdict':verdict,'execution_status':'CLEAN','scientific_verdict':'BOUNDARY_PASS' if verdict_pass else 'FAIL','triage_bin':'B' if verdict_pass else 'C','claim_tier':'SCOPED_CMB_DENSITY_BBN_CONTACT_NOT_FULL_CMB_CLOSURE','primary_high_l_delta_chi2_per_point':d['primary_high_l_delta_chi2_per_point'],'wrong_control_high_l_delta_chi2_per_point':d['wrong_control_high_l_delta_chi2_per_point'],'omega_b_h2_primary':G396['omega_b_h2_primary'],'eta10_primary':G396['eta10_primary'],'pass_conditions':pass_conditions}
    (ROOT/'CR021_summary.json').write_text(json.dumps(summary,indent=2)+'\n',encoding='utf-8')
    lines=['# CR021 Planck-Lite CMB Density and BBN Contact','','## Verdict','','```text',verdict,'```','','## Key Packet','','```text',f'G381 primary_high_l_delta_chi2_per_point = {d["primary_high_l_delta_chi2_per_point"]}',f'G381 wrong_control_high_l_delta_chi2_per_point = {d["wrong_control_high_l_delta_chi2_per_point"]}',f'G396 omega_b_h2_primary = {G396["omega_b_h2_primary"]}',f'G396 eta10_primary = {G396["eta10_primary"]}','```','','## Scope Boundary','','```text','Planck-lite / BBN contact only; no full Planck likelihood, recombination, perturbation, TT/TE/EE theorem-grade closure.','```','','## Pass Conditions','','| condition | pass |','|---|---:|']
    for k,v in pass_conditions.items(): lines.append(f'| {k} | {str(v).lower()} |')
    (ROOT/'CR021_result.md').write_text('\n'.join(lines)+'\n',encoding='utf-8')
    hashwrite([ROOT/'CR021_declared_premises.json',ROOT/'CR021_PRECOMMIT.md',ROOT/'CR021_runner.py',ROOT/'CR021_contact_rows.csv',ROOT/'CR021_result.md',ROOT/'CR021_summary.json'])
    print(json.dumps(summary,indent=2))
if __name__=='__main__': main()
