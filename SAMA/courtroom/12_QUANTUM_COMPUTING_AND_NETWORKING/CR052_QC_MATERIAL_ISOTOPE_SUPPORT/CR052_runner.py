import json, csv, hashlib
from pathlib import Path
ROOT=Path(__file__).resolve().parent
BRANCH=ROOT.parent
def load(rel): return json.loads((ROOT/rel).resolve().read_text(encoding="utf-8"))
def sha256(p):
    h=hashlib.sha256(); h.update(Path(p).read_bytes()); return h.hexdigest()
def csvwrite(p,rows):
    fields=[]
    for r in rows:
        for k in r:
            if k not in fields: fields.append(k)
    with Path(p).open("w",newline="",encoding="utf-8") as f:
        w=csv.DictWriter(f,fieldnames=fields); w.writeheader(); w.writerows(rows)
def hashwrite(paths):
    rows=[]
    for p in sorted(paths,key=lambda p:str(p).lower()):
        if p.name!="HASHES.txt": rows.append(f"{sha256(p)}  {p.relative_to(BRANCH)}")
    (ROOT/"HASHES.txt").write_text("\n".join(rows)+"\n",encoding="utf-8")
def main():
    summaries={k: load(f"../_source_artifacts/summaries/{k}_summary.json") for k in ['QC005']}

    q=summaries["QC005"]
    pass_conditions={
        "free_parameters_zero":q["free_parameters_introduced"]==0,
        "sealed_isotope_comparison_inherited":q["inherited_sealed_isotope_comparison_used"] is True,
        "no_new_external_source_intake":q["new_external_source_intake"] is False,
        "selected_filters_positive":q["selected_filters"]>0,
        "checks_pass":q["check_passes"]==q["check_total"],
        "wrong_controls_pass":q["wrong_control_passes"]==q["wrong_control_total"],
    }
    rows=[{"source":"QC005","result_class":q["result_class"],"support_filters":q["support_filters"],"selected_filters":q["selected_filters"],"excluded_filters":q["excluded_filters"],"lane_score_rows":q["lane_score_rows"],"application_rule_rows":q["application_rule_rows"]}]
    extra_summary={"selected_filters":q["selected_filters"],"excluded_filters":q["excluded_filters"]}
    
    verdict_pass=all(pass_conditions.values())
    verdict="CR052_PASS_QC_MATERIAL_ISOTOPE_SUPPORT" if verdict_pass else "CR052_FAIL_QC_MATERIAL_ISOTOPE_SUPPORT"
    sci="PASS" if verdict_pass else "FAIL"
    triage="B" if "PASS"=="BOUNDARY_PASS" else "A"
    if not verdict_pass: triage="C"
    csvwrite(ROOT/"CR052_rows.csv", rows)
    summary={
        "test_id":"CR052_QC_MATERIAL_ISOTOPE_SUPPORT",
        "verdict":verdict,
        "execution_status":"CLEAN",
        "scientific_verdict":sci,
        "triage_bin":triage,
        "claim_tier":"QC_MATERIAL_ISOTOPE_SUPPORT_FILTER" if verdict_pass else "FAILED_QC_MATERIAL_ISOTOPE_SUPPORT_FILTER",
        "source_keys":['QC005'],
        "pass_conditions":pass_conditions,
        **extra_summary
    }
    (ROOT/"CR052_summary.json").write_text(json.dumps(summary,indent=2)+"\n",encoding="utf-8")
    lines=["# CR052 QC Material / Isotope Support","","## Verdict","","```text",verdict,"```","","## Scope Boundary","","```text","Support filter only. This does not prove device material performance.","```","","## Key Rows","","See `CR052_rows.csv`.","","## Pass Conditions","","| condition | pass |","|---|---:|"]
    for k,v in pass_conditions.items(): lines.append(f"| {k} | {str(v).lower()} |")
    (ROOT/"CR052_result.md").write_text("\n".join(lines)+"\n",encoding="utf-8")
    hashwrite([ROOT/"CR052_declared_premises.json",ROOT/"CR052_PRECOMMIT.md",ROOT/"CR052_runner.py",ROOT/"CR052_rows.csv",ROOT/"CR052_result.md",ROOT/"CR052_summary.json"])
    print(json.dumps(summary,indent=2))
if __name__=="__main__": main()
