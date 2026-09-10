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
    G330=load('../_source_artifacts/summaries/G330_output.json'); G331=load('../_source_artifacts/summaries/G331_output.json'); G332=load('../_source_artifacts/summaries/G332_output.json')
    pass_conditions={
      'G330_predictions_all_pass': G330['prediction_pass_count']==G330['prediction_total'],
      'G330_wrong_controls_all_pass': G330['wrong_control_pass_count']==G330['wrong_control_total'],
      'G331_predictions_all_pass': G331['prediction_pass_count']==G331['prediction_total'],
      'G331_wrong_controls_all_pass': G331['wrong_control_pass_count']==G331['wrong_control_total'],
      'G332_predictions_all_pass': G332['prediction_pass_count']==G332['prediction_total'],
      'G332_wrong_controls_all_pass': G332['wrong_control_pass_count']==G332['wrong_control_total'],
      'G330_not_theorem_grade': 'not CMB theorem' in G330['grade'],
      'G331_not_theorem_grade': 'not CMB theorem' in G331['grade'],
      'G332_not_theorem_grade': 'not theorem-grade' in G332['grade'],
    }
    verdict_pass=all(pass_conditions.values())
    verdict='CR020_BOUNDARY_PASS_CMB_BOUNDARY_AND_ACOUSTIC_CONCEPT_CHAIN' if verdict_pass else 'CR020_FAIL_CMB_BOUNDARY_AND_ACOUSTIC_CONCEPT_CHAIN'
    rows=[{'test':'G330','verdict':G330['verdict'],'grade':G330['grade']},{'test':'G331','verdict':G331['verdict'],'grade':G331['grade']},{'test':'G332','verdict':G332['verdict'],'grade':G332['grade']}]
    csvwrite(ROOT/'CR020_cmb_concept_rows.csv',rows)
    summary={'test_id':'CR020_CMB_BOUNDARY_AND_ACOUSTIC_CONCEPT_CHAIN','verdict':verdict,'execution_status':'CLEAN','scientific_verdict':'BOUNDARY_PASS' if verdict_pass else 'FAIL','triage_bin':'B' if verdict_pass else 'C','claim_tier':'CMB_BOUNDARY_ACOUSTIC_CONCEPT_CHAIN_NOT_FULL_CMB_THEOREM','pass_conditions':pass_conditions,'source_verdicts':rows}
    (ROOT/'CR020_summary.json').write_text(json.dumps(summary,indent=2)+'\n',encoding='utf-8')
    lines=['# CR020 CMB Boundary and Acoustic Concept Chain','','## Verdict','','```text',verdict,'```','','## Source Tests','','```text','G330 — PBH initial A inventory / transparency boundary.','G331 — escaped baryon write decoupling.','G332 — corrected CMB acoustic branch.','```','','## Scope Boundary','','```text','This branch establishes CMB boundary/acoustic concept and consistency; it is not theorem-grade full CMB closure.','```','','## Pass Conditions','','| condition | pass |','|---|---:|']
    for k,v in pass_conditions.items(): lines.append(f'| {k} | {str(v).lower()} |')
    (ROOT/'CR020_result.md').write_text('\n'.join(lines)+'\n',encoding='utf-8')
    hashwrite([ROOT/'CR020_declared_premises.json',ROOT/'CR020_PRECOMMIT.md',ROOT/'CR020_runner.py',ROOT/'CR020_cmb_concept_rows.csv',ROOT/'CR020_result.md',ROOT/'CR020_summary.json'])
    print(json.dumps(summary,indent=2))
if __name__=='__main__': main()
