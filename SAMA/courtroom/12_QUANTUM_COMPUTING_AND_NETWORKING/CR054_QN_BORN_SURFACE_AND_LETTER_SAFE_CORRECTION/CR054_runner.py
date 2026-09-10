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
    summaries={k: load(f"../_source_artifacts/summaries/{k}_summary.json") for k in ['QN005', 'QN006']}

    q5,q6=summaries["QN005"],summaries["QN006"]
    pass_conditions={
        "QN005_no_external_data":q5["external_quantum_network_data_used"] is False,
        "QN006_no_external_data":q6["external_quantum_network_data_used"] is False,
        "free_parameters_zero":q5["free_parameters_introduced"]==0 and q6["free_parameters_introduced"]==0,
        "checks_pass":q5["check_passes"]==q5["check_total"] and q6["check_passes"]==q6["check_total"],
        "wrong_controls_pass":q5["wrong_control_passes"]==q5["wrong_control_total"] and q6["wrong_control_passes"]==q6["wrong_control_total"],
        "forbidden_fields_false":q5["forbidden_fields_used"] is False and q6["forbidden_fields_used"] is False,
    }
    rows=[
        {"source":"QN005","result_class":q5["result_class"],"top_open_route":q5["top_open_route"],"top_open_probability":q5["top_open_probability"],"network_available_routes":q5["network_available_routes"]},
        {"source":"QN006","result_class":q6["result_class"],"syndrome_rows":q6["syndrome_rows"],"correction_rules":q6["correction_rules"],"correction_decision_rows":q6["correction_decision_rows"],"correction_classes":q6["correction_classes"]},
    ]
    extra_summary={"top_open_route":q5["top_open_route"],"top_open_probability":q5["top_open_probability"],"correction_classes":q6["correction_classes"]}
    
    verdict_pass=all(pass_conditions.values())
    verdict="CR054_PASS_QN_BORN_SURFACE_AND_LETTER_SAFE_CORRECTION" if verdict_pass else "CR054_FAIL_QN_BORN_SURFACE_AND_LETTER_SAFE_CORRECTION"
    sci="PASS" if verdict_pass else "FAIL"
    triage="B" if "PASS"=="BOUNDARY_PASS" else "A"
    if not verdict_pass: triage="C"
    csvwrite(ROOT/"CR054_rows.csv", rows)
    summary={
        "test_id":"CR054_QN_BORN_SURFACE_AND_LETTER_SAFE_CORRECTION",
        "verdict":verdict,
        "execution_status":"CLEAN",
        "scientific_verdict":sci,
        "triage_bin":triage,
        "claim_tier":"QN_BORN_SURFACE_LETTER_SAFE_CORRECTION_PROTOCOL" if verdict_pass else "FAILED_QN_BORN_SURFACE_LETTER_SAFE_CORRECTION_PROTOCOL",
        "source_keys":['QN005', 'QN006'],
        "pass_conditions":pass_conditions,
        **extra_summary
    }
    (ROOT/"CR054_summary.json").write_text(json.dumps(summary,indent=2)+"\n",encoding="utf-8")
    lines=["# CR054 QN Born Surface and Letter-Safe Correction","","## Verdict","","```text",verdict,"```","","## Scope Boundary","","```text","Correction protocol only. This is not hardware-demonstrated error correction.","```","","## Key Rows","","See `CR054_rows.csv`.","","## Pass Conditions","","| condition | pass |","|---|---:|"]
    for k,v in pass_conditions.items(): lines.append(f"| {k} | {str(v).lower()} |")
    (ROOT/"CR054_result.md").write_text("\n".join(lines)+"\n",encoding="utf-8")
    hashwrite([ROOT/"CR054_declared_premises.json",ROOT/"CR054_PRECOMMIT.md",ROOT/"CR054_runner.py",ROOT/"CR054_rows.csv",ROOT/"CR054_result.md",ROOT/"CR054_summary.json"])
    print(json.dumps(summary,indent=2))
if __name__=="__main__": main()
