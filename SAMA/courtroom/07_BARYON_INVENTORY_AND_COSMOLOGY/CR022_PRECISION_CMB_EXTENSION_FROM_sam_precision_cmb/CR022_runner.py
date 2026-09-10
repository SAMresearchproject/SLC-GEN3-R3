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
    C001=load('../_source_artifacts/summaries/CMBP001_fixed_density.json')
    C010=load('../_source_artifacts/summaries/CMBP010_summary.json'); C011=load('../_source_artifacts/summaries/CMBP011_summary.json'); C012=load('../_source_artifacts/summaries/CMBP012_summary.json'); C013=load('../_source_artifacts/summaries/CMBP013_summary.json'); C014=load('../_source_artifacts/summaries/CMBP014_summary.json'); C015=load('../_source_artifacts/summaries/CMBP015_summary.json'); T1=load('../_source_artifacts/summaries/TRIAD001_summary.json'); T2=load('../_source_artifacts/summaries/TRIAD002_summary.json'); R3=load('../_source_artifacts/summaries/REVEAL003_summary.json'); BAO=load('../_source_artifacts/summaries/BAO002_sound_horizon.json')
    f=C001['fixed_inputs'] if 'fixed_inputs' in C001 else C001
    primary=R3['primary_high_l_TTTEEE']; imp=R3['imported_trio_high_l_TTTEEE']
    pass_conditions={
      'fixed_density_has_Omega_b': abs(f['Omega_b']-0.049299011266101)<1e-12,
      'C010_precomparison_firewall': C010['comparison_performed'] is False and C010['target_data_read'] is False,
      'C011_As_native_precomparison': C011['comparison_performed'] is False and C011['target_data_read'] is False and C011['free_parameters_introduced']==0,
      'C012_ns_native_precomparison': C012['comparison_performed'] is False and C012['target_data_read'] is False and C012['free_parameters_introduced']==0,
      'C013_tau_native_precomparison': C013['comparison_performed'] is False and C013['target_data_read'] is False and C013['free_parameters_introduced']==0,
      'C014_prediction_sealed': C014['comparison_performed'] is False and C014['target_data_read'] is False and C014['prediction_rows']>0,
      'C015_wrong_controls_frozen': C015['wrong_control_count']>0 and C015['no_control_eligible_for_promotion'] is True,
      'TRIAD_lockbox_complete': T1['comparison_performed'] is False and T2['comparison_performed'] is False,
      'REVEAL_no_parameter_fit': R3['checks']['no_parameter_fit'] is True and R3['formula_mutation_performed'] is False and R3['prediction_mutation_performed'] is False,
      'imported_trio_closer_than_primary': imp['delta_chi2_per_point'] < primary['delta_chi2_per_point'],
      'BAO002_recombination_boundary_preserved': BAO['route_status']=='CONDITIONAL_IMPORTED_RECOMBINATION_TRANSPORT_FROZEN',
    }
    verdict_pass=all(pass_conditions.values())
    verdict='CR022_BOUNDARY_PASS_PRECISION_CMB_EXTENSION' if verdict_pass else 'CR022_FAIL_PRECISION_CMB_EXTENSION'
    rows=[
      {'artifact':'CMBP001','Omega_b':f.get('Omega_b'),'Omega_m_eff':f.get('Omega_m_eff')},
      {'artifact':'CMBP011','A_s_native':C011.get('A_s_native')},
      {'artifact':'CMBP012','n_s_native':C012.get('n_s_native')},
      {'artifact':'CMBP013','tau_native':C013.get('tau_native')},
      {'artifact':'REVEAL003_primary','delta_chi2_per_point':primary['delta_chi2_per_point']},
      {'artifact':'REVEAL003_imported_trio','delta_chi2_per_point':imp['delta_chi2_per_point']},
      {'artifact':'BAO002','r_d_Mpc':BAO['r_d_Mpc'],'r_star_Mpc':BAO['r_star_Mpc'],'theta_star_100':BAO['theta_star_100'],'route_status':BAO['route_status']},
    ]
    csvwrite(ROOT/'CR022_precision_cmb_rows.csv',rows)
    summary={'test_id':'CR022_PRECISION_CMB_EXTENSION_FROM_sam_precision_cmb','verdict':verdict,'execution_status':'CLEAN','scientific_verdict':'BOUNDARY_PASS' if verdict_pass else 'FAIL','triage_bin':'B' if verdict_pass else 'C','claim_tier':'SCOPED_PRECISION_CMB_EXTENSION_FULL_CMB_BOUNDARIES_PRESERVED','A_s_native':C011.get('A_s_native'),'n_s_native':C012.get('n_s_native'),'tau_native':C013.get('tau_native'),'primary_high_l_delta_chi2_per_point':primary['delta_chi2_per_point'],'imported_trio_high_l_delta_chi2_per_point':imp['delta_chi2_per_point'],'r_d_Mpc':BAO['r_d_Mpc'],'r_star_Mpc':BAO['r_star_Mpc'],'theta_star_100':BAO['theta_star_100'],'pass_conditions':pass_conditions}
    (ROOT/'CR022_summary.json').write_text(json.dumps(summary,indent=2)+'\n',encoding='utf-8')
    lines=['# CR022 Precision-CMB Extension from sam_precision_cmb','','## Verdict','','```text',verdict,'```','','## Key Packet','','```text',f'A_s_native = {C011.get("A_s_native")}',f'n_s_native = {C012.get("n_s_native")}',f'tau_native = {C013.get("tau_native")}',f'REVEAL003 primary high-l delta = {primary["delta_chi2_per_point"]}',f'REVEAL003 imported-trio high-l delta = {imp["delta_chi2_per_point"]}',f'r_d = {BAO["r_d_Mpc"]} Mpc',f'theta_star_100 = {BAO["theta_star_100"]}',f'route_status = {BAO["route_status"]}','```','','## Scope Boundary','','```text','Scoped precision-CMB extension only. Imported-trio control remains closer to official Planck theory; recombination/acoustic-ruler bridge remains boundary-scoped.','```','','## Pass Conditions','','| condition | pass |','|---|---:|']
    for k,v in pass_conditions.items(): lines.append(f'| {k} | {str(v).lower()} |')
    (ROOT/'CR022_result.md').write_text('\n'.join(lines)+'\n',encoding='utf-8')
    hashwrite([ROOT/'CR022_declared_premises.json',ROOT/'CR022_PRECOMMIT.md',ROOT/'CR022_runner.py',ROOT/'CR022_precision_cmb_rows.csv',ROOT/'CR022_result.md',ROOT/'CR022_summary.json'])
    print(json.dumps(summary,indent=2))
if __name__=='__main__': main()
