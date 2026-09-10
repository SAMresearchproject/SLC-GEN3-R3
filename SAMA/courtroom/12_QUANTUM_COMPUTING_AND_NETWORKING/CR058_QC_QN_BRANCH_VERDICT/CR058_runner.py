import json, csv, hashlib
from pathlib import Path
ROOT=Path(__file__).resolve().parent
BRANCH=ROOT.parent
def load(rel): return json.loads((BRANCH/rel).read_text(encoding="utf-8"))
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
    paths=[
        ("CR050","CR050_QP_CARRIER_SUPPORT/CR050_summary.json"),
        ("CR051","CR051_QC_CARRIER_ENVELOPE_GATE_READOUT/CR051_summary.json"),
        ("CR052","CR052_QC_MATERIAL_ISOTOPE_SUPPORT/CR052_summary.json"),
        ("CR053","CR053_QN_NETWORK_GRAMMAR_LINK_RELAY_ROUTING/CR053_summary.json"),
        ("CR054","CR054_QN_BORN_SURFACE_AND_LETTER_SAFE_CORRECTION/CR054_summary.json"),
        ("CR055","CR055_QN_EARTH_A_AND_SEALED_BENCHMARK_MANIFEST/CR055_summary.json"),
        ("CR056","CR056_QN_EXTERNAL_BENCHMARK_AND_EXPERIMENTAL_PROTOCOL/CR056_summary.json"),
        ("CR057","CR057_QN_LIVE_SCORECARD_AND_INGESTION_PROTOCOL/CR057_summary.json"),
    ]
    comps=[(k,load(p)) for k,p in paths]
    rows=[{"component":k,"verdict":v["verdict"],"scientific_verdict":v["scientific_verdict"],"claim_tier":v["claim_tier"]} for k,v in comps]
    csvwrite(ROOT/"CR058_component_verdicts.csv", rows)
    ok = (
        comps[0][1]["scientific_verdict"]=="PASS" and
        comps[1][1]["scientific_verdict"]=="PASS" and
        comps[2][1]["scientific_verdict"]=="PASS" and
        comps[3][1]["scientific_verdict"]=="PASS" and
        comps[4][1]["scientific_verdict"]=="PASS" and
        comps[5][1]["scientific_verdict"]=="PASS" and
        comps[6][1]["scientific_verdict"]=="BOUNDARY_PASS" and
        comps[7][1]["scientific_verdict"]=="BOUNDARY_PASS"
    )
    verdict="CR058_BOUNDARY_PASS_QUANTUM_COMPUTING_AND_NETWORKING_BRANCH" if ok else "CR058_FAIL_QUANTUM_COMPUTING_AND_NETWORKING_BRANCH"
    export_claim=("SAM's private QC/QN branch produces a coherent particle-informed quantum computing and networking protocol stack: "
                  "carrier/envelope/sensor selection, native gates, Paul Revere readout/routing, no-clone relay rules, network Born surface, "
                  "letter-safe error correction, Earth-A deployment surface, sealed benchmark/comparator schema, external benchmark alignment, "
                  "experimental protocol translation, live scorecard package, and ingestion/scoring protocol. The branch remains scoped as protocol "
                  "and lab-handoff readiness, not hardware demonstration or externally validated self-correcting network operation.")
    summary={
        "test_id":"CR058_QC_QN_BRANCH_VERDICT",
        "verdict":verdict,
        "execution_status":"CLEAN",
        "scientific_verdict":"BOUNDARY_PASS" if ok else "FAIL",
        "triage_bin":"B" if ok else "C",
        "claim_tier":"QC_QN_PROTOCOL_AND_SCORING_STACK_LAB_HANDOFF_READY_NOT_HARDWARE_VALIDATED" if ok else "FAILED_QC_QN_BRANCH",
        "export_claim":export_claim,
        "scope_boundaries":[
            "not demonstrated quantum hardware",
            "not live external trial success",
            "not proven self-correcting network operation",
            "not full fault-tolerant architecture proof",
            "not a claim of automatic endorsement by any external platform"
        ],
        "component_verdicts":rows,
    }
    (ROOT/"CR058_summary.json").write_text(json.dumps(summary,indent=2)+"\n",encoding="utf-8")
    lines=["# CR058 QC/QN Branch Verdict","","## Verdict","","```text",verdict,"```","","## Component Verdicts","","| component | verdict | scientific verdict | claim tier |","|---|---|---|---|"]
    for r in rows: lines.append(f"| {r['component']} | {r['verdict']} | {r['scientific_verdict']} | {r['claim_tier']} |")
    lines.extend(["","## Export Claim","","```text",export_claim,"```","","## Scope Boundaries","","```text"])
    lines.extend(summary["scope_boundaries"])
    lines.append("```")
    (ROOT/"CR058_result.md").write_text("\n".join(lines)+"\n",encoding="utf-8")
    hashwrite([ROOT/"CR058_declared_premises.json",ROOT/"CR058_PRECOMMIT.md",ROOT/"CR058_runner.py",ROOT/"CR058_component_verdicts.csv",ROOT/"CR058_result.md",ROOT/"CR058_summary.json"])
    print(json.dumps(summary,indent=2))
if __name__=="__main__": main()
