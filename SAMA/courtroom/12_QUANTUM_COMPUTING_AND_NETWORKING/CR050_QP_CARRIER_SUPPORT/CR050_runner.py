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
    summaries={k: load(f"../_source_artifacts/summaries/{k}_summary.json") for k in ['QP010', 'QP043']}

    q10=summaries["QP010"]; q43=summaries["QP043"]
    pass_conditions={
        "QP010_free_parameters_zero": q10["free_parameters_introduced"]==0,
        "QP010_qubit_rows_positive": q10["qubit_rows"]>0,
        "QP010_result_built": "BUILT" in q10["result_class"],
        "QP043_free_parameters_zero": q43["free_parameters_introduced"]==0,
        "QP043_unknown_modes_present": q43["unknown_mode_rows"]>0,
        "QP043_at_least_one_assigned": q43["assigned_existing_carrier_rows"]>=1,
    }
    rows=[
        {"source":"QP010","result_class":q10["result_class"],"qubit_rows":q10["qubit_rows"],"top_protected_route":q10.get("top_protected_route"),"top_ticks_to_A_SIDE":q10.get("top_ticks_to_A_SIDE"),"top_ticks_to_A_SHARE":q10.get("top_ticks_to_A_SHARE")},
        {"source":"QP043","result_class":q43["result_class"],"unknown_mode_rows":q43["unknown_mode_rows"],"assigned_existing_carrier_rows":q43["assigned_existing_carrier_rows"],"candidate_composite_carrier_rows":q43["candidate_composite_carrier_rows"],"unassigned_boundary_rows":q43["unassigned_boundary_rows"]},
    ]
    extra_summary={"QP010_result_class":q10["result_class"],"QP043_result_class":q43["result_class"]}
    
    verdict_pass=all(pass_conditions.values())
    verdict="CR050_PASS_QP_CARRIER_SUPPORT" if verdict_pass else "CR050_FAIL_QP_CARRIER_SUPPORT"
    sci="PASS" if verdict_pass else "FAIL"
    triage="B" if "PASS"=="BOUNDARY_PASS" else "A"
    if not verdict_pass: triage="C"
    csvwrite(ROOT/"CR050_rows.csv", rows)
    summary={
        "test_id":"CR050_QP_CARRIER_SUPPORT",
        "verdict":verdict,
        "execution_status":"CLEAN",
        "scientific_verdict":sci,
        "triage_bin":triage,
        "claim_tier":"QUANTUM_PHASE_CARRIER_SUPPORT" if verdict_pass else "FAILED_QUANTUM_PHASE_CARRIER_SUPPORT",
        "source_keys":['QP010', 'QP043'],
        "pass_conditions":pass_conditions,
        **extra_summary
    }
    (ROOT/"CR050_summary.json").write_text(json.dumps(summary,indent=2)+"\n",encoding="utf-8")
    lines=["# CR050 QP Carrier Support","","## Verdict","","```text",verdict,"```","","## Scope Boundary","","```text","Support artifact only. This does not prove a quantum computer or network.","```","","## Key Rows","","See `CR050_rows.csv`.","","## Pass Conditions","","| condition | pass |","|---|---:|"]
    for k,v in pass_conditions.items(): lines.append(f"| {k} | {str(v).lower()} |")
    (ROOT/"CR050_result.md").write_text("\n".join(lines)+"\n",encoding="utf-8")
    hashwrite([ROOT/"CR050_declared_premises.json",ROOT/"CR050_PRECOMMIT.md",ROOT/"CR050_runner.py",ROOT/"CR050_rows.csv",ROOT/"CR050_result.md",ROOT/"CR050_summary.json"])
    print(json.dumps(summary,indent=2))
if __name__=="__main__": main()
