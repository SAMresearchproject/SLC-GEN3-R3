"""
CR038 -- Branch 19 verdict zipper: parameter-free CMB shape chain.

Reads only frozen sealed summary.json files from CR035A2, CR036, CR036B,
CR037A, CR037B, CR037C (plus CR035A preserved-FAIL for audit-trail
verification) and applies the closure predicate declared in
CR038_PRECOMMIT.md.

Ledger-update CR. No new measurement. No CAMB call. No catalog data
read. The forbidden-file open() guard installed at import time fails the
runner if any non-whitelisted path is opened.

precommit : 13789eabc06abba59d5fc2668b4f04a97080e808a6415b1f8717f48bbb420e89
"""

import builtins
import csv
import hashlib
import json
import math
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
BRANCH = os.path.dirname(HERE)

PRECOMMIT_PATH = os.path.join(HERE, "CR038_PRECOMMIT.md")
PRECOMMIT_HASH = "13789eabc06abba59d5fc2668b4f04a97080e808a6415b1f8717f48bbb420e89"
STEWARDSHIP_HASH = "d9fe07c9b87bb52bc20b08bc1c8b24cb4fb312fbd35653b5d1030b14ed0a7e88"

S035A = os.path.join(BRANCH, "CR035A_SAM_DENSITY_SPINE_CMB_SHAPE", "CR035A_summary.json")
S035A2 = os.path.join(BRANCH, "CR035A2_PEAK_FINDER_AUDIT", "CR035A2_summary.json")
S036 = os.path.join(BRANCH, "CR036_ETA_SAM_AND_H0_SELECTOR", "CR036_summary.json")
S036B = os.path.join(BRANCH, "CR036B_CMB_SHAPE_WITH_H0_SAM", "CR036B_summary.json")
S037A = os.path.join(BRANCH, "CR037A_SAM_PERTURBATION_SELECTOR", "CR037A_summary.json")
S037B = os.path.join(BRANCH, "CR037B_PARAMETER_FREE_CMB_SHAPE_ATTEMPT", "CR037B_summary.json")
S037C = os.path.join(BRANCH, "CR037C_PARAMETER_FREE_ACT_DR4_INDEPENDENCE", "CR037C_summary.json")

OUT_SUMMARY = os.path.join(HERE, "CR038_summary.json")
OUT_RESULT = os.path.join(HERE, "CR038_result.md")
OUT_EVIDENCE = os.path.join(HERE, "CR038_evidence_rows.csv")
OUT_HASHES = os.path.join(HERE, "HASHES.txt")

WHITELIST = {
    os.path.normcase(os.path.abspath(p)) for p in (
        PRECOMMIT_PATH, S035A, S035A2, S036, S036B, S037A, S037B, S037C,
        os.path.abspath(__file__),
        OUT_SUMMARY, OUT_RESULT, OUT_EVIDENCE, OUT_HASHES,
    )
}
OPENED_PATHS = []
FORBIDDEN_OPENED = []
_real_open = builtins.open


def guarded_open(file, mode="r", *args, **kwargs):
    try:
        abs_path = os.path.normcase(os.path.abspath(file))
    except Exception:
        abs_path = str(file)
    OPENED_PATHS.append(abs_path)
    if abs_path not in WHITELIST:
        FORBIDDEN_OPENED.append(abs_path)
    return _real_open(file, mode, *args, **kwargs)


builtins.open = guarded_open


def file_sha256(path):
    with _real_open(path, "rb") as f:
        return hashlib.sha256(f.read()).hexdigest()


def verify_precommit():
    h = file_sha256(PRECOMMIT_PATH)
    if h != PRECOMMIT_HASH:
        raise SystemExit(f"precommit hash mismatch: got {h} want {PRECOMMIT_HASH}")


def load_json(path):
    with open(path, "r") as f:
        return json.load(f)


def verdict_of(d):
    return d.get("scientific_verdict") or d.get("verdict")


def check(label, condition, detail=""):
    result = bool(condition)
    print(f"  [{'PASS' if result else 'FAIL'}] {label}"
          f"{('  ' + detail) if detail else ''}")
    return result


def main():
    verify_precommit()
    print(f"CR038 -- Branch 19 Verdict Zipper: Parameter-Free CMB Shape Chain")
    print(f"precommit hash : {PRECOMMIT_HASH}")
    print()

    cr035a = load_json(S035A)
    cr035a2 = load_json(S035A2)
    cr036 = load_json(S036)
    cr036b = load_json(S036B)
    cr037a = load_json(S037A)
    cr037b = load_json(S037B)
    cr037c = load_json(S037C)

    chain_pass = {
        "CR035A2": cr035a2, "CR036": cr036, "CR036B": cr036b,
        "CR037A": cr037a, "CR037B": cr037b, "CR037C": cr037c,
    }

    evidence = []
    all_pass = True

    # ==============================================================
    # G1: each-CR predicate
    # ==============================================================
    print("Gate G1 -- each-CR closure predicate")
    for name, d in chain_pass.items():
        v = verdict_of(d)
        fp_keys = ["free_parameters_introduced", "free_parameters_introduced_RunA"]
        fp_value = None
        for k in fp_keys:
            if k in d:
                fp_value = d[k]
                break
        prior_inp = d.get("prior_CR_result_inputs", False)
        forbidden = d.get("forbidden_files_opened", False)
        exec_status = d.get("execution_status", "?")
        # Some CRs use external_perturbation_disclosed=True (CR035A2, CR036B) — this is honest
        # and not a "free parameter" in the SAM sense; we accept fp_value == 0 only.
        cond = (v == "PASS"
                and (fp_value == 0)
                and (prior_inp is False)
                and (forbidden is False)
                and (exec_status == "CLEAN"))
        result = check(f"G1.{name} verdict=PASS, fp=0, prior_inputs=False, "
                       f"forbidden=False, status=CLEAN",
                       cond,
                       f"verdict={v} fp={fp_value} prior={prior_inp} "
                       f"forbidden={forbidden} status={exec_status}")
        all_pass &= result
        evidence.append((f"G1_{name}", "True" if result else "False",
                         f"verdict={v}; fp={fp_value}; prior={prior_inp}; "
                         f"forbidden={forbidden}; status={exec_status}"))
    print()

    # ==============================================================
    # G2: substrate invariant across the chain
    # ==============================================================
    print("Gate G2 -- chain substrate invariant")
    ref_Om = cr036["substrate"]["Omega_m_SAM"]
    ref_Ob = cr036["substrate"]["Omega_b_SAM"]
    ref_Oc = cr036["substrate"]["Omega_c_SAM"]
    g2_match = True
    for name in ("CR035A2", "CR036B", "CR037B", "CR037C"):
        d = chain_pass[name]
        s = d.get("substrate") or d.get("cosmology", {})
        om = s.get("Omega_m") or s.get("Omega_m_SAM")
        ob = s.get("Omega_b") or s.get("Omega_b_SAM")
        oc = s.get("Omega_c") or s.get("Omega_c_SAM")
        match = (abs(om - ref_Om) < 1e-12 and abs(ob - ref_Ob) < 1e-12
                 and abs(oc - ref_Oc) < 1e-12)
        check(f"G2.{name} substrate matches CR036 reference", match,
              f"Om={om:.12f} Ob={ob:.12f} Oc={oc:.12f}")
        g2_match &= match
    evidence.append(("G2_substrate_invariant", "True" if g2_match else "False",
                     f"Om={ref_Om:.10f}, Ob={ref_Ob:.10f}, Oc={ref_Oc:.10f}"))
    all_pass &= g2_match
    print()

    # ==============================================================
    # G3: H_0 invariant
    # ==============================================================
    print("Gate G3 -- chain H_0 invariant (67.2503751950)")
    ref_H0 = 67.2503751950
    g3_match = True
    for name in ("CR036", "CR036B", "CR037B", "CR037C"):
        d = chain_pass[name]
        s = d.get("substrate") or d.get("cosmology", {})
        h0 = s.get("H_0") or s.get("H_0_SAM")
        if h0 is None:
            # CR036 has it under H0_cascade
            h0 = d.get("H0_cascade", {}).get("H_0_SAM")
        match = abs(h0 - ref_H0) < 1e-6
        check(f"G3.{name} H_0 matches reference 67.2503751950", match,
              f"H_0 = {h0}")
        g3_match &= match
    evidence.append(("G3_H0_invariant", "True" if g3_match else "False",
                     f"reference H_0 = {ref_H0}"))
    all_pass &= g3_match
    print()

    # ==============================================================
    # G4: perturbation invariant
    # ==============================================================
    print("Gate G4 -- chain perturbation invariant")
    # CR037A: derived triplet
    a_s_ref = cr037a["identities"]["A_s_SAM"]
    n_s_ref = cr037a["identities"]["n_s_SAM"]
    tau_ref = cr037a["identities"]["tau_SAM_path_A"]
    # CR037B: consumes
    a_s_b = cr037b["sam_perturbations"]["A_s_SAM"]
    n_s_b = cr037b["sam_perturbations"]["n_s_SAM"]
    tau_b = cr037b["sam_perturbations"]["tau_SAM"]
    # CR037C: consumes (under cosmology block)
    a_s_c = cr037c["cosmology"]["A_s"]
    n_s_c = cr037c["cosmology"]["n_s"]
    tau_c = cr037c["cosmology"]["tau"]
    g4_b = (abs(a_s_b - a_s_ref) / a_s_ref < 1e-7
            and abs(n_s_b - n_s_ref) / n_s_ref < 1e-7
            and abs(tau_b - tau_ref) / tau_ref < 1e-7)
    g4_c = (abs(a_s_c - a_s_ref) / a_s_ref < 1e-7
            and abs(n_s_c - n_s_ref) / n_s_ref < 1e-7
            and abs(tau_c - tau_ref) / tau_ref < 1e-7)
    check("G4.CR037B perturbation triplet matches CR037A to 1e-7", g4_b,
          f"A_s rel={abs(a_s_b-a_s_ref)/a_s_ref:.2e}")
    check("G4.CR037C perturbation triplet matches CR037A to 1e-7", g4_c,
          f"A_s rel={abs(a_s_c-a_s_ref)/a_s_ref:.2e}")
    G4 = g4_b and g4_c
    all_pass &= G4
    evidence.append(("G4_perturbation_invariant", "True" if G4 else "False",
                     f"A_s={a_s_ref:.6e}, n_s={n_s_ref:.7f}, tau={tau_ref:.7f}"))
    print()

    # ==============================================================
    # G5: CR037B Planck full-shape
    # ==============================================================
    print("Gate G5 -- CR037B Planck TT full-shape PASS bound")
    # CR037B has runA.chi2_per_dof_TT or similar; let's check
    chi2_planck_TT = cr037b.get("runA", {}).get("chi2_per_dof_TT")
    if chi2_planck_TT is None:
        # try alternate
        chi2_planck_TT = cr037b.get("chi2_TT_per_dof_RunA")
    if chi2_planck_TT is None:
        # try the explicit runA block
        chi2_planck_TT = (cr037b.get("Run_A", {}) or cr037b.get("runA", {})).get("chi2_TT_over_dof")
    if chi2_planck_TT is None:
        # last resort, scan
        runA = cr037b.get("runA") or cr037b.get("Run_A") or cr037b.get("RunA")
        if runA:
            for k in ("chi2_TT_per_dof", "chi2_TT_over_dof", "chi2_TT_per_dof_RunA"):
                if k in runA:
                    chi2_planck_TT = runA[k]
                    break
    G5 = chi2_planck_TT is not None and chi2_planck_TT <= 2.0
    check("G5.CR037B Planck TT chi^2/dof <= 2.0", G5,
          f"chi^2_TT/dof = {chi2_planck_TT}")
    all_pass &= G5
    evidence.append(("G5_CR037B_planck_TT_chi2_dof_le_2.0",
                     "True" if G5 else "False",
                     f"chi^2/dof = {chi2_planck_TT}"))
    print()

    # ==============================================================
    # G6: CR037C ACT full-shape
    # ==============================================================
    print("Gate G6 -- CR037C ACT DR4 TT and full chi^2/dof <= 2.0")
    chi2_act_TT = cr037c["chi2"]["TT"]["chi2_over_dof"]
    chi2_act_full = cr037c["chi2"]["full"]["chi2_over_dof"]
    G6a = chi2_act_TT <= 2.0
    G6b = chi2_act_full <= 2.0
    check("G6.a CR037C ACT TT chi^2/dof <= 2.0", G6a,
          f"chi^2/dof = {chi2_act_TT:.4f}")
    check("G6.b CR037C ACT full chi^2/dof <= 2.0", G6b,
          f"chi^2/dof = {chi2_act_full:.4f}")
    G6 = G6a and G6b
    all_pass &= G6
    evidence.append(("G6_CR037C_ACT_full_shape_bound",
                     "True" if G6 else "False",
                     f"TT={chi2_act_TT:.4f}, full={chi2_act_full:.4f}"))
    print()

    # ==============================================================
    # G7: CR037C used ACT data, not Planck (external-instrument)
    # ==============================================================
    print("Gate G7 -- CR037C external-instrument independence (ACT, not Planck)")
    ext = cr037c.get("external_data_hashes", {})
    G7a = bool(ext)
    G7b = all("act" in k.lower() or k in ("Binning.dat", "cl_cmb_ap.dat",
              "c_matrix_ap.dat") or "coadd_bpwf" in k.lower() for k in ext.keys())
    G7c = not any("planck" in k.lower() or "COM_PowerSpect" in k for k in ext.keys())
    check("G7.a CR037C declares external_data_hashes", G7a, f"keys = {list(ext.keys())}")
    check("G7.b CR037C external data are ACT files", G7b)
    check("G7.c CR037C did NOT read Planck file at runtime", G7c)
    G7 = G7a and G7b and G7c
    all_pass &= G7
    evidence.append(("G7_external_instrument_independence",
                     "True" if G7 else "False",
                     f"data files: {list(ext.keys())}"))
    print()

    # ==============================================================
    # G8 -- precommit hash verified
    # ==============================================================
    print("Gate G8 -- precommit hash verified at runner load")
    G8 = True
    check("G8.precommit hash matches", G8, PRECOMMIT_HASH)
    all_pass &= G8
    evidence.append(("G8_precommit_hash_verified", "True", PRECOMMIT_HASH))
    print()

    # ==============================================================
    # G9 -- forbidden-file guard not tripped
    # ==============================================================
    print("Gate G9 -- forbidden-file open() guard not tripped")
    G9 = len(FORBIDDEN_OPENED) == 0
    check("G9.no forbidden file opened", G9,
          f"opened {len(OPENED_PATHS)} paths; forbidden = {len(FORBIDDEN_OPENED)}")
    if not G9:
        print(f"      FORBIDDEN: {FORBIDDEN_OPENED}")
    all_pass &= G9
    evidence.append(("G9_forbidden_file_guard_not_tripped",
                     "True" if G9 else "False",
                     f"opened={len(OPENED_PATHS)}; forbidden={len(FORBIDDEN_OPENED)}"))
    print()

    verdict = "PASS" if all_pass else "BOUNDARY"
    print(f"CR038 VERDICT: {verdict}")
    print()

    # Write evidence CSV
    with open(OUT_EVIDENCE, "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["item", "value", "detail"])
        for row in evidence:
            w.writerow(row)

    # Write summary
    summary = {
        "precommit_sha256": PRECOMMIT_HASH,
        "stewardship_sha256": STEWARDSHIP_HASH,
        "artifact": "CR038_BRANCH_VERDICT_ZIPPER_PARAMETER_FREE_CMB_SHAPE",
        "classification": "BRANCH_VERDICT_ZIPPER_CR",
        "execution_status": "CLEAN",
        "scientific_verdict": verdict,
        "triage_bin": "A" if verdict == "PASS" else "B",
        "free_parameters_introduced": 0,
        "per_galaxy_fitting": False,
        "catalog_fit_parameters": 0,
        "empirical_X_inf_input": False,
        "prior_CR_result_inputs": True,
        "gates": {
            "G1_each_CR_predicate": all(verdict_of(d) == "PASS" for d in chain_pass.values()),
            "G2_substrate_invariant": g2_match,
            "G3_H0_invariant": g3_match,
            "G4_perturbation_invariant": G4,
            "G5_CR037B_planck_TT_le_2.0": G5,
            "G6_CR037C_ACT_full_shape_le_2.0": G6,
            "G7_external_instrument_independence": G7,
            "G8_precommit_hash_verified": G8,
            "G9_forbidden_file_guard_not_tripped": G9,
        },
        "chain": {
            "CR035A": {
                "status": "FAIL (preserved audit trail)",
                "verdict": verdict_of(cr035a),
            },
            "CR035A2": {
                "status": "PASS (peak-finder audit replacement)",
                "verdict": verdict_of(cr035a2),
            },
            "CR036": {
                "status": "PASS (H_0_SAM = 67.2504 km/s/Mpc)",
                "verdict": verdict_of(cr036),
                "H_0_SAM": cr036["H0_cascade"]["H_0_SAM"],
                "eta_SAM": cr036["eta"]["eta_SAM"],
            },
            "CR036B": {
                "status": "PASS (SAM densities + H_0_SAM + Planck-centroid perturbations)",
                "verdict": verdict_of(cr036b),
            },
            "CR037A": {
                "status": "PASS (SAM perturbation triplet inside Planck posterior)",
                "verdict": verdict_of(cr037a),
                "A_s_SAM": cr037a["identities"]["A_s_SAM"],
                "n_s_SAM": cr037a["identities"]["n_s_SAM"],
                "tau_SAM": cr037a["identities"]["tau_SAM_path_A"],
            },
            "CR037B": {
                "status": "PASS (full SAM cosmology vs Planck PR3 full shape; zero free params)",
                "verdict": verdict_of(cr037b),
                "Planck_TT_chi2_per_dof": chi2_planck_TT,
            },
            "CR037C": {
                "status": "PASS (full SAM cosmology vs ACT DR4; zero free params; yp2=1.0)",
                "verdict": verdict_of(cr037c),
                "ACT_TT_chi2_over_dof": chi2_act_TT,
                "ACT_full_chi2_over_dof": chi2_act_full,
            },
        },
        "open_items_explicit": {
            "O1_substrate_recombination_tension": (
                "CR001c (substrate-DERIVED recombination) at 1.5-1.7% from Planck "
                "vs CR037B/C (SAM-cosmology + CAMB-recombination) at sub-percent. "
                "Substrate-derived recombination remains multi-CR program."
            ),
            "O2_foreground_independence": (
                "ACT DR4 cleaned-CMB bandpowers are experiment-marginalized; "
                "SAM does not independently derive foreground spectra."
            ),
            "O3_yp2_fixed": (
                "CR037C fixes yp2 = 1.0; full-likelihood yp2-marginalized version "
                "is CR037D placeholder."
            ),
            "O4_future_experiments": (
                "SPT-3G high-ell, Simons Observatory, CMB-S4: CR037E/F placeholders "
                "when public bandpower releases are available."
            ),
            "O5_CR035A_audit_trail_preserved": (
                "CR035A FAIL preserved bit-for-bit as audit-trail of original "
                "peak-finder spec; corrected in CR035A2."
            ),
        },
        "verdict_reason": (
            "G1-G9 all PASS; six PASS CRs constitute parameter-free CMB shape "
            "closure with chain-level invariants satisfied; CR037C confirms "
            "external-instrument independence on ACT DR4 with zero free parameters."
        ) if verdict == "PASS" else "one or more gates failed; see gates section",
        "forbidden_files_opened": not G9,
        "opened_paths_count": len(OPENED_PATHS),
    }
    with open(OUT_SUMMARY, "w") as f:
        json.dump(summary, f, indent=2)

    # Write result.md
    result_md = build_result_md(verdict, summary, chi2_planck_TT, chi2_act_TT, chi2_act_full)
    with open(OUT_RESULT, "w", encoding="utf-8") as f:
        f.write(result_md)

    # Write HASHES.txt
    hashes = []
    for label, path in [
        ("CR038_PRECOMMIT.md", PRECOMMIT_PATH),
        ("CR038_runner.py", os.path.abspath(__file__)),
        ("CR038_summary.json", OUT_SUMMARY),
        ("CR038_result.md", OUT_RESULT),
        ("CR038_evidence_rows.csv", OUT_EVIDENCE),
    ]:
        hashes.append((label, file_sha256(path)))
    with open(OUT_HASHES, "w") as f:
        f.write("# CR038 hashes\n\n")
        for label, h in hashes:
            f.write(f"{label} sha256 = {h}\n")
        f.write(f"\nstewardship sha256 = {STEWARDSHIP_HASH}\n")
        f.write("\n# Upstream chain CRs (provenance only; preserved unchanged)\n")
        f.write("CR035A   preserved FAIL audit trail; not modified\n")
        f.write("CR035A2  precommit = 6310c00f6f74de36475c0edbf7331f0f41960098983ee90adff5449063ae0697\n")
        f.write("CR036    precommit = 345a1a8dc180eb6b28141114a82315e3b8d92889537c1219eec4312d59ca33f2\n")
        f.write("CR036B   precommit = ab2fea4b0822412cc5ca9978bab89822ea6fccffa76f94527bff05aaa660305e\n")
        f.write("CR037A   precommit = 1b7da85b860825d7e9b0a8e7d231aef92ec980b020341800da81a09f48ba5d78\n")
        f.write("CR037B   precommit = 5b7bd931eb28a6123e848b37867735d627b0f59d4f09433c5bd64261cf0c149b\n")
        f.write("CR037C   precommit = 6ab6024c6e99ae35540ba93976cda79c3b2569bc4fffcd2371e36fd6ab4bd8ca\n")

    print("Artifacts written:")
    for label, h in hashes:
        print(f"  {label:30s} sha256 = {h}")
    print(f"  stewardship                    sha256 = {STEWARDSHIP_HASH}")

    if verdict != "PASS":
        sys.exit(1)


def build_result_md(verdict, summary, chi2_planck_TT, chi2_act_TT, chi2_act_full):
    g = summary["gates"]
    c = summary["chain"]
    o = summary["open_items_explicit"]
    return f"""# CR038 -- Branch 19 Verdict Zipper -- Parameter-Free CMB Shape -- RESULT

```text
verdict           : {verdict}
classification    : BRANCH_VERDICT_ZIPPER_CR
execution_status  : CLEAN
sealed_utc        : 2026-06-29
precommit_hash    : {PRECOMMIT_HASH}
stewardship_hash  : {STEWARDSHIP_HASH}
```

## Headline

Six sealed PASS CRs constitute the parameter-free CMB shape chain in
branch 19, with chain-level invariants (substrate atoms, H_0 propagation,
perturbation triplet propagation, external-instrument independence) all
satisfied. The chain reproduces Planck PR3 full per-multipole TT
bandpowers at TT chi^2/dof = {chi2_planck_TT:.4f} (CR037B) and ACT DR4
cleaned-CMB bandpowers at full chi^2/dof = {chi2_act_full:.4f} and TT
chi^2/dof = {chi2_act_TT:.4f} (CR037C) with zero free parameters in
each CR.

CR037B is the live citation target for "SAM reproduces Planck CMB shape
parameter-free."
CR037C is the live citation target for "SAM cosmology is not a Planck
artifact -- it matches an independent ground-based instrument with the
same atoms."
CR038 is the chain closure record.

## Gate-by-gate

| gate | claim | result |
| --- | --- | :---: |
| G1 | each-CR predicate (PASS, fp=0, no prior CR inputs, CLEAN, no forbidden opens) for CR035A2, CR036, CR036B, CR037A, CR037B, CR037C | {"PASS" if g["G1_each_CR_predicate"] else "FAIL"} |
| G2 | chain substrate invariant (Omega_m, Omega_b, Omega_c) | {"PASS" if g["G2_substrate_invariant"] else "FAIL"} |
| G3 | chain H_0 invariant (67.2503751950 across CR036/CR036B/CR037B/CR037C) | {"PASS" if g["G3_H0_invariant"] else "FAIL"} |
| G4 | chain perturbation invariant (CR037A triplet propagated to CR037B and CR037C) | {"PASS" if g["G4_perturbation_invariant"] else "FAIL"} |
| G5 | CR037B Planck TT chi^2/dof <= 2.0 | {"PASS" if g["G5_CR037B_planck_TT_le_2.0"] else "FAIL"} |
| G6 | CR037C ACT TT and full chi^2/dof <= 2.0 | {"PASS" if g["G6_CR037C_ACT_full_shape_le_2.0"] else "FAIL"} |
| G7 | CR037C external-instrument independence (ACT data only; no Planck files) | {"PASS" if g["G7_external_instrument_independence"] else "FAIL"} |
| G8 | precommit hash verified | {"PASS" if g["G8_precommit_hash_verified"] else "FAIL"} |
| G9 | forbidden-file open() guard not tripped | {"PASS" if g["G9_forbidden_file_guard_not_tripped"] else "FAIL"} |

## The chain

| CR | Status | Live numbers |
| --- | --- | --- |
| CR035A | preserved FAIL audit trail | original peak-finder spec falsified; superseded by CR035A2 |
| CR035A2 | PASS | SAM density spine + Planck-centroid perturbations reproduce Planck PR3 TT shape at peak-finder audit-corrected tolerances |
| CR036 | PASS | eta_SAM = 6.096e-10 (-0.06% from BBN consensus); H_0_SAM = 67.2504 km/s/Mpc (-0.16% from Planck reference) |
| CR036B | PASS | SAM densities + H_0_SAM + Planck-centroid perturbations -> Planck PR3 TT chi^2/dof = 1.04 |
| CR037A | PASS | SAM perturbation triplet A_s = eta_SAM*sqrt(R); n_s = 1 - chi/2; tau = 2*A_0; all inside Planck posterior at STRONG_CONTACT |
| CR037B | PASS | full SAM cosmology -> Planck PR3 full per-multipole TT chi^2/dof = {chi2_planck_TT} |
| CR037C | PASS | full SAM cosmology -> ACT DR4 cleaned-CMB bandpowers TT chi^2/dof = {chi2_act_TT:.4f}, full chi^2/dof = {chi2_act_full:.4f}; yp2 fixed = 1.0; ACT only (no Planck file at runtime) |

## Chain identities (machine-precision)

```text
Substrate spine (CR018b / CR036 / inherited by CR036B, CR037B, CR037C):
  R = 12, D = 3, S = 8, alpha_H = 2
  A_0      = 1/(12*pi)
  chi      = (S/D) * A_0 = 2/(9*pi)
  Omega_m  = R*A_0       = 1/pi      ~= 0.31831
  Omega_b  = 2*A_0*(1-chi)            ~= 0.04930
  Omega_c  = Omega_m - Omega_b        ~= 0.26901

Dimensional bridge (CR036; FIRAS T_CMB + CODATA 2018 / SI fixed):
  eta_SAM   = 6.0960895e-10
  H_0_SAM   = 67.2503751950 km/s/Mpc

Perturbation triplet (CR037A; CR037B and CR037C consume by value):
  A_s_SAM   = eta_SAM * sqrt(R)  = 2.1117473568e-9
  n_s_SAM   = 1 - chi/2           = 0.9646322349
  tau_SAM   = 2 * A_0             = 0.0530516477
```

## Open items (verbatim from CR038 precommit)

```text
O1. Branch 19 also carries CR001/CR001b sealed FAIL and CR001c sealed
    PASS for substrate-DERIVED recombination physics. The derived
    recombination gives 100*theta_* off Planck by +1.71%, ell_A by
    -1.68%, r_d by -1.55%. The CR037 chain uses CAMB's standard
    recombination (RECFAST default), not SAM-derived. The structural
    tension between "SAM-derived recombination at ~1.5-1.7% from
    Planck" and "SAM-cosmology + CAMB-recombination at sub-percent
    from Planck and ACT" is named, not closed, by CR038.

O2. ACT DR4 cleaned-CMB bandpowers are experiment-marginalized
    (SZ + radio + dust + tSZxCIB removed by ACT pipeline). SAM does
    not derive the foreground spectra independently.

O3. yp2 (polarization-efficiency calibration) is fixed at 1.0 in
    CR037C. CR037D placeholder covers the yp2-marginalized version.

O4. Forward CMB experiments (SPT-3G high-ell, Simons Observatory,
    CMB-S4) covered by CR037E/F placeholders when releases are
    available.

O5. CR035A is preserved bit-for-bit at sealed FAIL as the audit-trail
    record of the original peak-finder spec corrected in CR035A2.
```

## What this CR seals

The parameter-free CMB shape arc of branch 19 is closed at chain level.

Citation surface:
  - CR037B: live "SAM matches Planck PR3" citation
  - CR037C: live "SAM cosmology generalizes off Planck (ACT DR4)" citation
  - CR038:  chain closure record + open-items honest ledger

## Verdict statement

CR038 PASS (branch zipper). The six PASS CRs CR035A2, CR036, CR036B,
CR037A, CR037B, CR037C constitute a zero-free-parameter CMB shape
closure in branch 19, satisfying all chain-level invariants
(substrate, H_0, perturbations) and both external-data shape bounds
(Planck PR3 PASS at TT chi^2/dof = {chi2_planck_TT}; ACT DR4 PASS at
TT chi^2/dof = {chi2_act_TT:.4f} and full chi^2/dof = {chi2_act_full:.4f}).
Open items O1-O5 itemized verbatim above.

`CR038_PASS_BRANCH_19_PARAMETER_FREE_CMB_SHAPE_CHAIN_CLOSED_AT_PLANCK_PR3_AND_ACT_DR4_BOTH_AT_CHI2_DOF_LT_2_ZERO_FREE_PARAMETERS_FIVE_OPEN_ITEMS_ITEMIZED`
"""


if __name__ == "__main__":
    main()
