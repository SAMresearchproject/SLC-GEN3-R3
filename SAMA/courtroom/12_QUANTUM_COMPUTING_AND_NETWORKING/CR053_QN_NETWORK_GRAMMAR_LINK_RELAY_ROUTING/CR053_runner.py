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
    summaries={k: load(f"../_source_artifacts/summaries/{k}_summary.json") for k in ['QN001', 'QN002', 'QN003', 'QN004']}

    q1,q2,q3,q4=[summaries[k] for k in ["QN001","QN002","QN003","QN004"]]
    pass_conditions={
        "all_no_external_network_data": all(summaries[k]["external_quantum_network_data_used"] is False for k in ["QN001","QN002","QN003","QN004"]),
        "all_free_parameters_zero": all(summaries[k]["free_parameters_introduced"]==0 for k in ["QN001","QN002","QN003","QN004"]),
        "all_checks_pass": all(summaries[k]["check_passes"]==summaries[k]["check_total"] for k in ["QN001","QN002","QN003","QN004"]),
        "all_wrong_controls_pass": all(summaries[k]["wrong_control_passes"]==summaries[k]["wrong_control_total"] for k in ["QN001","QN002","QN003","QN004"]),
        "QN004_paul_revere_routing": "PAUL_REVERE" in q4["result_class"],
        "QN004_forbidden_fields_false": q4["forbidden_fields_used"] is False,
    }
    rows=[
        {"source":"QN001","result_class":q1["result_class"],"network_objects":q1["network_objects"],"primary_carrier":q1["primary_carrier"],"control_envelope":q1["control_envelope"],"boundary_sensor":q1["boundary_sensor"]},
        {"source":"QN002","result_class":q2["result_class"],"selected_link_object":q2["selected_link_object"],"selected_link_route":q2["selected_link_route"],"selected_link_viability_score":q2["selected_link_viability_score"]},
        {"source":"QN003","result_class":q3["result_class"],"selected_relay_surface":q3["selected_relay_surface"],"relay_viability_score":q3["relay_viability_score"]},
        {"source":"QN004","result_class":q4["result_class"],"selected_route":q4["selected_route"],"top_selected_routing_score":q4["top_selected_routing_score"]},
    ]
    extra_summary={"selected_route":q4["selected_route"],"top_selected_routing_score":q4["top_selected_routing_score"]}
    
    verdict_pass=all(pass_conditions.values())
    verdict="CR053_PASS_QN_NETWORK_GRAMMAR_LINK_RELAY_ROUTING" if verdict_pass else "CR053_FAIL_QN_NETWORK_GRAMMAR_LINK_RELAY_ROUTING"
    sci="PASS" if verdict_pass else "FAIL"
    triage="B" if "PASS"=="BOUNDARY_PASS" else "A"
    if not verdict_pass: triage="C"
    csvwrite(ROOT/"CR053_rows.csv", rows)
    summary={
        "test_id":"CR053_QN_NETWORK_GRAMMAR_LINK_RELAY_ROUTING",
        "verdict":verdict,
        "execution_status":"CLEAN",
        "scientific_verdict":sci,
        "triage_bin":triage,
        "claim_tier":"QN_NETWORK_GRAMMAR_LINK_RELAY_ROUTING_PROTOCOL" if verdict_pass else "FAILED_QN_NETWORK_GRAMMAR_LINK_RELAY_ROUTING_PROTOCOL",
        "source_keys":['QN001', 'QN002', 'QN003', 'QN004'],
        "pass_conditions":pass_conditions,
        **extra_summary
    }
    (ROOT/"CR053_summary.json").write_text(json.dumps(summary,indent=2)+"\n",encoding="utf-8")
    lines=["# CR053 QN Network Grammar / Link / Relay / Routing","","## Verdict","","```text",verdict,"```","","## Scope Boundary","","```text","Protocol grammar/routing only. This is not live network validation.","```","","## Key Rows","","See `CR053_rows.csv`.","","## Pass Conditions","","| condition | pass |","|---|---:|"]
    for k,v in pass_conditions.items(): lines.append(f"| {k} | {str(v).lower()} |")
    (ROOT/"CR053_result.md").write_text("\n".join(lines)+"\n",encoding="utf-8")
    hashwrite([ROOT/"CR053_declared_premises.json",ROOT/"CR053_PRECOMMIT.md",ROOT/"CR053_runner.py",ROOT/"CR053_rows.csv",ROOT/"CR053_result.md",ROOT/"CR053_summary.json"])
    print(json.dumps(summary,indent=2))
if __name__=="__main__": main()
