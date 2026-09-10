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
    summaries={k: load(f"../_source_artifacts/summaries/{k}_summary.json") for k in ['QN012', 'QN013']}

    q12,q13=summaries["QN012"],summaries["QN013"]
    pass_conditions={
        "QN012_external_data_allowed":q12["external_quantum_network_data_used"] is True and "QN010" in q12["external_data_allowed_by"],
        "QN013_external_data_allowed":q13["external_quantum_network_data_used"] is True and "QN010" in q13["external_data_allowed_by"],
        "QN012_no_new_external_intake":q12["new_external_source_intake"] is False,
        "QN013_no_new_external_intake":q13["new_external_source_intake"] is False,
        "QN013_demo_data_only":q13["demo_data_only"] is True,
        "free_parameters_zero":q12["free_parameters_introduced"]==0 and q13["free_parameters_introduced"]==0,
        "checks_pass":q12["check_passes"]==q12["check_total"] and q13["check_passes"]==q13["check_total"],
        "wrong_controls_pass":q12["wrong_control_passes"]==q12["wrong_control_total"] and q13["wrong_control_passes"]==q13["wrong_control_total"],
        "forbidden_fields_false":q12["forbidden_fields_used"] is False and q13["forbidden_fields_used"] is False,
    }
    rows=[
        {"source":"QN012","result_class":q12["result_class"],"selected_candidate":q12["selected_candidate"],"data_package_files":q12["data_package_files"],"paul_revere_letter_rows":q12["paul_revere_letter_rows"],"scorecard_rows":q12["scorecard_rows"],"leakage_firewall_rows":q12["leakage_firewall_rows"]},
        {"source":"QN013","result_class":q13["result_class"],"demo_data_only":q13["demo_data_only"],"demo_trials":q13["demo_trials"],"pass_trials":q13["pass_trials"],"partial_trials":q13["partial_trials"],"blocker_trials":q13["blocker_trials"],"ingestion_schema_rows":q13["ingestion_schema_rows"],"score_rule_rows":q13["score_rule_rows"]},
    ]
    extra_summary={"demo_data_only":q13["demo_data_only"],"demo_trials":q13["demo_trials"],"pass_trials":q13["pass_trials"],"partial_trials":q13["partial_trials"],"blocker_trials":q13["blocker_trials"],"next_frontier":q13["next_frontier"]}
    
    verdict_pass=all(pass_conditions.values())
    verdict="CR057_PASS_QN_LIVE_SCORECARD_AND_INGESTION_PROTOCOL" if verdict_pass else "CR057_FAIL_QN_LIVE_SCORECARD_AND_INGESTION_PROTOCOL"
    sci="BOUNDARY_PASS" if verdict_pass else "FAIL"
    triage="B" if "BOUNDARY_PASS"=="BOUNDARY_PASS" else "A"
    if not verdict_pass: triage="C"
    csvwrite(ROOT/"CR057_rows.csv", rows)
    summary={
        "test_id":"CR057_QN_LIVE_SCORECARD_AND_INGESTION_PROTOCOL",
        "verdict":verdict,
        "execution_status":"CLEAN",
        "scientific_verdict":sci,
        "triage_bin":triage,
        "claim_tier":"QN_LIVE_SCORECARD_INGESTION_PROTOCOL_DEMO_DATA_ONLY" if verdict_pass else "FAILED_QN_LIVE_SCORECARD_INGESTION_PROTOCOL_DEMO_DATA_ONLY",
        "source_keys":['QN012', 'QN013'],
        "pass_conditions":pass_conditions,
        **extra_summary
    }
    (ROOT/"CR057_summary.json").write_text(json.dumps(summary,indent=2)+"\n",encoding="utf-8")
    lines=["# CR057 QN Live Scorecard and Ingestion Protocol","","## Verdict","","```text",verdict,"```","","## Scope Boundary","","```text","Live-data scoring protocol only. QN013 demo data only; not external live lab validation.","```","","## Key Rows","","See `CR057_rows.csv`.","","## Pass Conditions","","| condition | pass |","|---|---:|"]
    for k,v in pass_conditions.items(): lines.append(f"| {k} | {str(v).lower()} |")
    (ROOT/"CR057_result.md").write_text("\n".join(lines)+"\n",encoding="utf-8")
    hashwrite([ROOT/"CR057_declared_premises.json",ROOT/"CR057_PRECOMMIT.md",ROOT/"CR057_runner.py",ROOT/"CR057_rows.csv",ROOT/"CR057_result.md",ROOT/"CR057_summary.json"])
    print(json.dumps(summary,indent=2))
if __name__=="__main__": main()
