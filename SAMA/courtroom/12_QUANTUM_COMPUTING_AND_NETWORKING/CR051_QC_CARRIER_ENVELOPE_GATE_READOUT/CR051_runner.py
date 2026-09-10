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
    summaries={k: load(f"../_source_artifacts/summaries/{k}_summary.json") for k in ['QC001', 'QC002', 'QC003', 'QC004']}

    q1,q2,q3,q4=[summaries[k] for k in ["QC001","QC002","QC003","QC004"]]
    pass_conditions={
        "QC001_free_parameters_zero":q1["free_parameters_introduced"]==0,
        "QC001_no_external_hardware":q1["external_quantum_hardware_data_used"] is False,
        "QC002_checks_pass":q2["check_passes"]==q2["check_total"],
        "QC002_wrong_controls_pass":q2["wrong_control_passes"]==q2["wrong_control_total"],
        "QC003_native_gates_positive":q3["native_gates"]==5,
        "QC003_checks_pass":q3["check_passes"]==q3["check_total"],
        "QC004_paul_revere_selected":"PAUL_REVERE" in q4["result_class"],
        "QC004_checks_pass":q4["check_passes"]==q4["check_total"],
        "all_free_parameters_zero":all(summaries[k]["free_parameters_introduced"]==0 for k in ["QC001","QC002","QC003","QC004"]),
    }
    rows=[
        {"source":"QC001","result_class":q1["result_class"],"primary_letter_carrier":q1["primary_letter_carrier"],"control_envelope":q1["control_envelope"],"boundary_stress_sensor":q1["boundary_stress_sensor"],"lead_ticks":q1["primary_max_lead_to_A_SHARE_ticks"]},
        {"source":"QC002","result_class":q2["result_class"],"carrier_route":q2["carrier_route"],"control_envelope_route":q2["control_envelope_route"],"boundary_sensor_route":q2["boundary_sensor_route"],"carrier_to_envelope_lead_ratio":q2["carrier_to_envelope_lead_ratio"]},
        {"source":"QC003","result_class":q3["result_class"],"native_gates":q3["native_gates"]},
        {"source":"QC004","result_class":q4["result_class"],"allowed_pre_write_observables":q4.get("allowed_pre_write_observables"),"blocked_pre_write_observables":q4.get("blocked_pre_write_observables")}
    ]
    extra_summary={"primary_carrier":q1["primary_letter_carrier"],"control_envelope":q1["control_envelope"],"boundary_sensor":q1["boundary_stress_sensor"],"native_gates":q3["native_gates"],"carrier_to_envelope_lead_ratio":q2["carrier_to_envelope_lead_ratio"]}
    
    verdict_pass=all(pass_conditions.values())
    verdict="CR051_PASS_QC_CARRIER_ENVELOPE_GATE_READOUT" if verdict_pass else "CR051_FAIL_QC_CARRIER_ENVELOPE_GATE_READOUT"
    sci="PASS" if verdict_pass else "FAIL"
    triage="B" if "PASS"=="BOUNDARY_PASS" else "A"
    if not verdict_pass: triage="C"
    csvwrite(ROOT/"CR051_rows.csv", rows)
    summary={
        "test_id":"CR051_QC_CARRIER_ENVELOPE_GATE_READOUT",
        "verdict":verdict,
        "execution_status":"CLEAN",
        "scientific_verdict":sci,
        "triage_bin":triage,
        "claim_tier":"QC_CARRIER_ENVELOPE_GATE_READOUT_PROTOCOL" if verdict_pass else "FAILED_QC_CARRIER_ENVELOPE_GATE_READOUT_PROTOCOL",
        "source_keys":['QC001', 'QC002', 'QC003', 'QC004'],
        "pass_conditions":pass_conditions,
        **extra_summary
    }
    (ROOT/"CR051_summary.json").write_text(json.dumps(summary,indent=2)+"\n",encoding="utf-8")
    lines=["# CR051 QC Carrier / Envelope / Gate / Readout","","## Verdict","","```text",verdict,"```","","## Scope Boundary","","```text","Protocol construction only. This does not prove hardware implementation.","```","","## Key Rows","","See `CR051_rows.csv`.","","## Pass Conditions","","| condition | pass |","|---|---:|"]
    for k,v in pass_conditions.items(): lines.append(f"| {k} | {str(v).lower()} |")
    (ROOT/"CR051_result.md").write_text("\n".join(lines)+"\n",encoding="utf-8")
    hashwrite([ROOT/"CR051_declared_premises.json",ROOT/"CR051_PRECOMMIT.md",ROOT/"CR051_runner.py",ROOT/"CR051_rows.csv",ROOT/"CR051_result.md",ROOT/"CR051_summary.json"])
    print(json.dumps(summary,indent=2))
if __name__=="__main__": main()
