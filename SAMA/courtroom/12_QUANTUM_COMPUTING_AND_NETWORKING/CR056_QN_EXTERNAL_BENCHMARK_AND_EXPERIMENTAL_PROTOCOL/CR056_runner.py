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
    summaries={k: load(f"../_source_artifacts/summaries/{k}_summary.json") for k in ['QN010', 'QN011']}

    q10,q11=summaries["QN010"],summaries["QN011"]
    pass_conditions={
        "QN010_external_data_allowed":q10["external_quantum_network_data_used"] is True and "QN009" in q10["external_data_allowed_by"],
        "QN011_external_data_allowed":q11["external_quantum_network_data_used"] is True and "QN010" in q11["external_data_allowed_by"],
        "QN011_no_new_external_intake":q11["new_external_source_intake"] is False,
        "free_parameters_zero":q10["free_parameters_introduced"]==0 and q11["free_parameters_introduced"]==0,
        "checks_pass":q10["check_passes"]==q10["check_total"] and q11["check_passes"]==q11["check_total"],
        "wrong_controls_pass":q10["wrong_control_passes"]==q10["wrong_control_total"] and q11["wrong_control_passes"]==q11["wrong_control_total"],
        "forbidden_fields_false":q10["forbidden_fields_used"] is False and q11["forbidden_fields_used"] is False,
        "selected_candidate_consistent":q10["strongest_candidate"]==q11["selected_candidate"],
    }
    rows=[
        {"source":"QN010","result_class":q10["result_class"],"candidate_platforms":q10["candidate_platforms"],"external_sources_used":q10["external_sources_used"],"comparison_rows":q10["comparison_rows"],"strongest_candidate":q10["strongest_candidate"],"match_count":q10["strongest_candidate_match_count"],"partial_count":q10["strongest_candidate_partial_count"],"blocker_count":q10["strongest_candidate_blocker_count"]},
        {"source":"QN011","result_class":q11["result_class"],"selected_candidate":q11["selected_candidate"],"selected_candidate_alignment_class":q11["selected_candidate_alignment_class"],"protocol_requirement_rows":q11["protocol_requirement_rows"],"experimental_step_rows":q11["experimental_step_rows"],"observable_rows":q11["observable_rows"],"success_criteria_rows":q11["success_criteria_rows"]},
    ]
    extra_summary={"strongest_candidate":q10["strongest_candidate"],"match_count":q10["strongest_candidate_match_count"],"partial_count":q10["strongest_candidate_partial_count"],"blocker_count":q10["strongest_candidate_blocker_count"]}
    
    verdict_pass=all(pass_conditions.values())
    verdict="CR056_PASS_QN_EXTERNAL_BENCHMARK_AND_EXPERIMENTAL_PROTOCOL" if verdict_pass else "CR056_FAIL_QN_EXTERNAL_BENCHMARK_AND_EXPERIMENTAL_PROTOCOL"
    sci="BOUNDARY_PASS" if verdict_pass else "FAIL"
    triage="B" if "BOUNDARY_PASS"=="BOUNDARY_PASS" else "A"
    if not verdict_pass: triage="C"
    csvwrite(ROOT/"CR056_rows.csv", rows)
    summary={
        "test_id":"CR056_QN_EXTERNAL_BENCHMARK_AND_EXPERIMENTAL_PROTOCOL",
        "verdict":verdict,
        "execution_status":"CLEAN",
        "scientific_verdict":sci,
        "triage_bin":triage,
        "claim_tier":"QN_EXTERNAL_BENCHMARK_PROTOCOL_TRANSLATION" if verdict_pass else "FAILED_QN_EXTERNAL_BENCHMARK_PROTOCOL_TRANSLATION",
        "source_keys":['QN010', 'QN011'],
        "pass_conditions":pass_conditions,
        **extra_summary
    }
    (ROOT/"CR056_summary.json").write_text(json.dumps(summary,indent=2)+"\n",encoding="utf-8")
    lines=["# CR056 QN External Benchmark and Experimental Protocol","","## Verdict","","```text",verdict,"```","","## Scope Boundary","","```text","External comparison/protocol translation only. This is not live trial success.","```","","## Key Rows","","See `CR056_rows.csv`.","","## Pass Conditions","","| condition | pass |","|---|---:|"]
    for k,v in pass_conditions.items(): lines.append(f"| {k} | {str(v).lower()} |")
    (ROOT/"CR056_result.md").write_text("\n".join(lines)+"\n",encoding="utf-8")
    hashwrite([ROOT/"CR056_declared_premises.json",ROOT/"CR056_PRECOMMIT.md",ROOT/"CR056_runner.py",ROOT/"CR056_rows.csv",ROOT/"CR056_result.md",ROOT/"CR056_summary.json"])
    print(json.dumps(summary,indent=2))
if __name__=="__main__": main()
