"""
CR003b -- QNM Higher Modes Strength Test

Same substrate atom set and search space as CR003. Tests whether the
substrate algebra encodes the full ringdown spectrum or only the
fundamental l=m=2 n=0 mode.

precommit : 9ed16b1ebc02c8765db9ff3c307bf71380928ffb7954cb0bfb300a972d2703c5
"""

import csv
import hashlib
import json
import math
import os

HERE = os.path.dirname(os.path.abspath(__file__))
PRECOMMIT_PATH = os.path.join(HERE, "CR003b_PRECOMMIT.md")
PRECOMMIT_HASH = "9ed16b1ebc02c8765db9ff3c307bf71380928ffb7954cb0bfb300a972d2703c5"

GATE_PASS = 0.5         # percent
GATE_BOUNDARY = 5.0     # percent

# Substrate atoms (CR258 sealed, identical to CR003)
h, d = 2, 3
S = h**d
V = d**d
F = d**(d+1)
R = h**2 * d
R2 = R*R
Theta = h * d**2
L = h * F
M = R2 - Theta
PI = math.pi

ATOMS = {
    "h": h, "d": d, "S": S, "V": V, "F": F,
    "R": R, "R2": R2, "Theta": Theta, "L": L, "M": M, "PI": PI,
}

# Higher Schwarzschild QNMs to test, Berti et al. 2009 Table I
MODES = [
    # (label, l, n, omega_R_M, omega_I_M)
    ("l=2 n=1 (overtone)",       2, 1, 0.34671, 0.27391),
    ("l=3 n=0 (fundamental)",    3, 0, 0.59944, 0.09270),
    ("l=3 n=1 (overtone)",       3, 1, 0.58264, 0.28129),
    ("l=4 n=0 (fundamental)",    4, 0, 0.80918, 0.09416),
    ("l=5 n=0 (fundamental)",    5, 0, 1.01229, 0.09487),
]

# CR003 baseline (for forward-prediction extension reporting)
CR003_R_FORM = "d/S"
CR003_R_VALUE = d / S       # 3/8 = 0.375
CR003_I_FORM = "R/(L-V)"
CR003_I_VALUE = R / (L - V) # 4/45 = 0.0888...


def file_sha256(p):
    with open(p, "rb") as f:
        return hashlib.sha256(f.read()).hexdigest()


def verify_precommit():
    h_ = file_sha256(PRECOMMIT_PATH)
    if h_ != PRECOMMIT_HASH:
        raise SystemExit(f"precommit hash mismatch: got {h_} want {PRECOMMIT_HASH}")


def enumerate_candidates():
    names = list(ATOMS.keys())
    out = []
    for a in names:
        for b in names:
            try:
                v = ATOMS[a] / ATOMS[b]
                out.append((f"{a}/{b}", v))
            except ZeroDivisionError:
                pass
    for a in names:
        for b in names:
            for c in names:
                for sym, fn in [("+", lambda x, y: x+y), ("-", lambda x, y: x-y)]:
                    den = fn(ATOMS[b], ATOMS[c])
                    if abs(den) < 1e-9:
                        continue
                    out.append((f"{a}/({b}{sym}{c})", ATOMS[a] / den))
                if ATOMS[c] != 0:
                    out.append((f"({a}+{b})/{c}", (ATOMS[a] + ATOMS[b]) / ATOMS[c]))
                    out.append((f"({a}-{b})/{c}", (ATOMS[a] - ATOMS[b]) / ATOMS[c]))
                    out.append((f"({a}*{b})/{c}", (ATOMS[a] * ATOMS[b]) / ATOMS[c]))
                if ATOMS[b] * ATOMS[c] != 0:
                    out.append((f"{a}/({b}*{c})", ATOMS[a] / (ATOMS[b] * ATOMS[c])))
    for a in names:
        for b in names:
            for c in names:
                for D_ in names:
                    den = ATOMS[c] * ATOMS[D_]
                    if abs(den) < 1e-9:
                        continue
                    out.append((f"({a}*{b})/({c}*{D_})", (ATOMS[a] * ATOMS[b]) / den))
    return out


def best_match(candidates, target, top_k=5):
    scored = []
    for expr, v in candidates:
        if not math.isfinite(v):
            continue
        if v <= 0:
            continue
        err_pct = abs(v - target) / target * 100
        scored.append((err_pct, expr, v))
    scored.sort()
    seen = {}
    for err, expr, v in scored:
        key = round(v, 10)
        if key not in seen or len(expr) < len(seen[key][1]):
            seen[key] = (err, expr, v)
    deduped = sorted(seen.values())
    return deduped[:top_k]


def gate(err_pct):
    if err_pct <= GATE_PASS:
        return "PASS"
    if err_pct <= GATE_BOUNDARY:
        return "BOUNDARY"
    return "FAIL"


def main():
    verify_precommit()
    print("CR003b -- QNM Higher Modes Strength Test")
    print(f"precommit hash : {PRECOMMIT_HASH}")
    print()
    print("Substrate atoms (CR258 sealed, identical to CR003):")
    for k, v in ATOMS.items():
        print(f"  {k:>5s} = {v}")
    print()
    print(f"CR003 baseline (l=2 n=0):")
    print(f"  omega_R: {CR003_R_FORM} = {CR003_R_VALUE:.6f}")
    print(f"  omega_I: {CR003_I_FORM} = {CR003_I_VALUE:.6f}")
    print()

    candidates = enumerate_candidates()
    print(f"Enumerated {len(candidates)} candidate expressions")
    print()

    n_pass = 0
    n_boundary = 0
    n_fail = 0
    per_mode_results = []

    for label, ll, nn, tR, tI in MODES:
        print(f"=== {label}  GR: omega_R*M={tR:.5f}, omega_I*M={tI:.5f} ===")

        # Real part
        top_R = best_match(candidates, tR, top_k=5)
        best_R = top_R[0]
        R_status = gate(best_R[0])
        print(f"  REAL part top candidates:")
        for i, (err, expr, v) in enumerate(top_R, start=1):
            tag = " <-- BEST" if i == 1 else ""
            print(f"    {i}. err={err:7.4f}%  {expr:30s} = {v:.6f}{tag}")
        print(f"    gate: {R_status} ({best_R[0]:.4f}%)")

        # Imag part
        top_I = best_match(candidates, tI, top_k=5)
        best_I = top_I[0]
        I_status = gate(best_I[0])
        print(f"  IMAG part top candidates:")
        for i, (err, expr, v) in enumerate(top_I, start=1):
            tag = " <-- BEST" if i == 1 else ""
            print(f"    {i}. err={err:7.4f}%  {expr:30s} = {v:.6f}{tag}")
        print(f"    gate: {I_status} ({best_I[0]:.4f}%)")
        print()

        for status in (R_status, I_status):
            if status == "PASS":
                n_pass += 1
            elif status == "BOUNDARY":
                n_boundary += 1
            else:
                n_fail += 1

        per_mode_results.append({
            "label": label,
            "l": ll,
            "n": nn,
            "target_R": tR,
            "target_I": tI,
            "best_R_expr": best_R[1],
            "best_R_value": best_R[2],
            "best_R_err_pct": best_R[0],
            "best_R_status": R_status,
            "best_I_expr": best_I[1],
            "best_I_value": best_I[2],
            "best_I_err_pct": best_I[0],
            "best_I_status": I_status,
        })

    # ===== Verdict =====
    n_total = len(MODES) * 2
    print(f"=== Aggregate (across {n_total} coefficients) ===")
    print(f"  PASS     (within 0.5%) : {n_pass}/{n_total}")
    print(f"  BOUNDARY (within 5%)   : {n_boundary}/{n_total}")
    print(f"  FAIL     (>5% off)     : {n_fail}/{n_total}")
    print()

    if n_pass >= 9:
        verdict = "STRONG_PASS"
    elif n_pass >= 7:
        verdict = "PASS"
    elif n_pass >= 5 or (n_pass + n_boundary) >= 7:
        verdict = "BOUNDARY"
    else:
        verdict = "FAIL"

    print(f"CR003b VERDICT: {verdict}")
    print()

    # ===== Reported extension hypotheses (not gated) =====
    print(f"=== Reported H1/H2 extension hypotheses (not gated) ===")
    print(f"H1: ω_R extension hypothesis -- does CR003 form predict higher l?")
    for r in per_mode_results:
        if r["n"] == 0:
            # for n=0 modes, see if CR003 form * (l-1) works
            pred_h1 = CR003_R_VALUE * (r["l"] - 1)
            err = abs(pred_h1 - r["target_R"]) / r["target_R"] * 100
            print(f"  {r['label']:>30s}: H1 (d/S * (l-1)) = {pred_h1:.5f}, "
                  f"target {r['target_R']:.5f}, err {err:.2f}%")
    print(f"H2: ω_I overtone hypothesis -- does R/(L-V) * (2n+1) work?")
    for r in per_mode_results:
        pred_h2 = CR003_I_VALUE * (2 * r["n"] + 1)
        err = abs(pred_h2 - r["target_I"]) / r["target_I"] * 100
        print(f"  {r['label']:>30s}: H2 (R/(L-V) * (2n+1)) = {pred_h2:.5f}, "
              f"target {r['target_I']:.5f}, err {err:.2f}%")
    print()

    # ===== Emit outputs =====
    csv_path = os.path.join(HERE, "CR003b_per_mode.csv")
    with open(csv_path, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["mode", "l", "n",
                    "target_R", "best_R_expr", "best_R_value", "best_R_err_pct", "best_R_status",
                    "target_I", "best_I_expr", "best_I_value", "best_I_err_pct", "best_I_status"])
        for r in per_mode_results:
            w.writerow([r["label"], r["l"], r["n"],
                        r["target_R"], r["best_R_expr"], r["best_R_value"],
                        r["best_R_err_pct"], r["best_R_status"],
                        r["target_I"], r["best_I_expr"], r["best_I_value"],
                        r["best_I_err_pct"], r["best_I_status"]])

    summary = {
        "artifact": "CR003b_QNM_HIGHER_MODES",
        "mode": "EXPLORATORY",
        "verdict": verdict,
        "precommit_hash": PRECOMMIT_HASH,
        "search_space_size": len(candidates),
        "coefficients_tested": n_total,
        "passed_within_0p5pct": n_pass,
        "boundary_within_5pct": n_boundary,
        "failed": n_fail,
        "per_mode": per_mode_results,
        "cr003_baseline": {
            "omega_R_form": CR003_R_FORM,
            "omega_R_value": CR003_R_VALUE,
            "omega_I_form": CR003_I_FORM,
            "omega_I_value": CR003_I_VALUE,
        },
    }
    with open(os.path.join(HERE, "CR003b_summary.json"), "w",
              encoding="utf-8") as f:
        json.dump(summary, f, indent=2, default=str)

    runner_hash = file_sha256(__file__)
    print(f"runner SHA-256 : {runner_hash}")


if __name__ == "__main__":
    main()
