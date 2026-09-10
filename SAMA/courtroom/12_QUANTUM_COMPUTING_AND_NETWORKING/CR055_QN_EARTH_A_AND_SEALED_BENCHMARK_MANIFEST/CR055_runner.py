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
    summaries={k: load(f"../_source_artifacts/summaries/{k}_summary.json") for k in ['QN007', 'QN008', 'QN009']}

    q7,q8,q9=[summaries[k] for k in ["QN007","QN008","QN009"]]
    pass_conditions={
        "QN007_no_external_data":q7["external_quantum_network_data_used"] is False,
        "QN008_no_external_data":q8["external_quantum_network_data_used"] is False,
        "QN009_no_external_data":q9["external_quantum_network_data_used"] is False,
        "free_parameters_zero":all(summaries[k]["free_parameters_introduced"]==0 for k in ["QN007","QN008","QN009"]),
        "all_checks_pass":all(summaries[k]["check_passes"]==summaries[k]["check_total"] for k in ["QN007","QN008","QN009"]),
        "all_wrong_controls_pass":all(summaries[k]["wrong_control_passes"]==summaries[k]["wrong_control_total"] for k in ["QN007","QN008","QN009"]),
        "sealed_hashes_present":q9["sealed_hashes_present"] is True,
        "all_qn008_inputs_external_frozen":q9["all_qn008_inputs_external_frozen"] is True,
    }
    rows=[
        {"source":"QN007","result_class":q7["result_class"],"earth_surface_A":q7["earth_surface_A"],"earth_fraction_of_A_SIDE":q7["earth_fraction_of_A_SIDE"],"earth_fraction_of_A_SHARE":q7["earth_fraction_of_A_SHARE"]},
        {"source":"QN008","result_class":q8["result_class"],"benchmark_manifest_rows":q8["benchmark_manifest_rows"],"formula_freeze_rows":q8["formula_freeze_rows"],"sealed_hash_rows":q8["sealed_hash_rows"]},
        {"source":"QN009","result_class":q9["result_class"],"scoring_rule_rows":q9["scoring_rule_rows"],"forbidden_leakage_screen_rows":q9["forbidden_leakage_screen_rows"],"comparator_output_schema_rows":q9["comparator_output_schema_rows"]},
    ]
    extra_summary={"earth_surface_A":q7["earth_surface_A"],"benchmark_manifest_rows":q8["benchmark_manifest_rows"],"scoring_rule_rows":q9["scoring_rule_rows"]}
    
    verdict_pass=all(pass_conditions.values())
    verdict="CR055_PASS_QN_EARTH_A_AND_SEALED_BENCHMARK_MANIFEST" if verdict_pass else "CR055_FAIL_QN_EARTH_A_AND_SEALED_BENCHMARK_MANIFEST"
    sci="PASS" if verdict_pass else "FAIL"
    triage="B" if "PASS"=="BOUNDARY_PASS" else "A"
    if not verdict_pass: triage="C"
    csvwrite(ROOT/"CR055_rows.csv", rows)
    summary={
        "test_id":"CR055_QN_EARTH_A_AND_SEALED_BENCHMARK_MANIFEST",
        "verdict":verdict,
        "execution_status":"CLEAN",
        "scientific_verdict":sci,
        "triage_bin":triage,
        "claim_tier":"QN_DEPLOYMENT_SURFACE_SEALED_BENCHMARK_COMPARATOR_SCHEMA" if verdict_pass else "FAILED_QN_DEPLOYMENT_SURFACE_SEALED_BENCHMARK_COMPARATOR_SCHEMA",
        "source_keys":['QN007', 'QN008', 'QN009'],
        "pass_conditions":pass_conditions,
        **extra_summary
    }
    (ROOT/"CR055_summary.json").write_text(json.dumps(summary,indent=2)+"\n",encoding="utf-8")
    lines=["# CR055 QN Earth-A and Sealed Benchmark Manifest","","## Verdict","","```text",verdict,"```","","## Scope Boundary","","```text","Benchmark readiness only. This is not external benchmark success.","```","","## Key Rows","","See `CR055_rows.csv`.","","## Pass Conditions","","| condition | pass |","|---|---:|"]
    for k,v in pass_conditions.items(): lines.append(f"| {k} | {str(v).lower()} |")
    (ROOT/"CR055_result.md").write_text("\n".join(lines)+"\n",encoding="utf-8")
    hashwrite([ROOT/"CR055_declared_premises.json",ROOT/"CR055_PRECOMMIT.md",ROOT/"CR055_runner.py",ROOT/"CR055_rows.csv",ROOT/"CR055_result.md",ROOT/"CR055_summary.json"])
    print(json.dumps(summary,indent=2))
if __name__=="__main__": main()
