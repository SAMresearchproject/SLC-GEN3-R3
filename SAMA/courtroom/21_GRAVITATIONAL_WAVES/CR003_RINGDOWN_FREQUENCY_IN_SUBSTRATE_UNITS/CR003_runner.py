"""
CR003 -- Ringdown Frequency in Substrate Units

Exhaustive small-form enumeration over substrate atoms (h, d, S, V, F,
R, R2, Theta, L, M, pi). For each candidate expression, compute the
relative error against the Schwarzschild l=m=2 n=0 QNM dimensionless
real and imaginary parts:

  target_R = 0.37367168
  target_I = 0.08896232

PASS gate: best candidate within 0.5% on each part independently.

precommit : ec90b9924a12ae760bd3cefb550ad602be442114b8a26c36b0fb9c37f5998cd3
"""

import csv
import hashlib
import json
import math
import os

HERE = os.path.dirname(os.path.abspath(__file__))
PRECOMMIT_PATH = os.path.join(HERE, "CR003_PRECOMMIT.md")
PRECOMMIT_HASH = "ec90b9924a12ae760bd3cefb550ad602be442114b8a26c36b0fb9c37f5998cd3"

# Target QNM dimensionless complex frequency, Schwarzschild l=m=2 n=0.
# Source: Berti, Cardoso, Starinets 2009, Living Rev. Rel. 12, 2.
TARGET_R = 0.37367168
TARGET_I = 0.08896232

GATE_PASS = 0.5        # percent
GATE_BOUNDARY = 5.0    # percent

# Substrate atoms (CR258 sealed)
h, d = 2, 3
S = h**d              # 8
V = d**d              # 27
F = d**(d+1)          # 81
R = h**2 * d          # 12
R2 = R*R              # 144
Theta = h * d**2      # 18
L = h * F             # 162
M = R2 - Theta        # 126
PI = math.pi

ATOMS = {
    "h": h, "d": d, "S": S, "V": V, "F": F,
    "R": R, "R2": R2, "Theta": Theta, "L": L, "M": M, "PI": PI,
}


def file_sha256(p):
    with open(p, "rb") as f:
        return hashlib.sha256(f.read()).hexdigest()


def verify_precommit():
    h_ = file_sha256(PRECOMMIT_PATH)
    if h_ != PRECOMMIT_HASH:
        raise SystemExit(f"precommit hash mismatch: got {h_} want {PRECOMMIT_HASH}")


def enumerate_candidates():
    """Generate (expression_string, numeric_value) pairs for the
    declared forms in the precommit."""
    names = list(ATOMS.keys())
    out = []
    for a in names:
        for b in names:
            # a/b
            try:
                v = ATOMS[a] / ATOMS[b]
                out.append((f"{a}/{b}", v))
            except ZeroDivisionError:
                pass
    for a in names:
        for b in names:
            for c in names:
                # a/(b+c), a/(b-c)
                for sym, fn in [("+", lambda x, y: x+y), ("-", lambda x, y: x-y)]:
                    den = fn(ATOMS[b], ATOMS[c])
                    if abs(den) < 1e-9:
                        continue
                    out.append((f"{a}/({b}{sym}{c})", ATOMS[a] / den))
                # (a+b)/c, (a-b)/c
                if ATOMS[c] != 0:
                    out.append((f"({a}+{b})/{c}", (ATOMS[a] + ATOMS[b]) / ATOMS[c]))
                    out.append((f"({a}-{b})/{c}", (ATOMS[a] - ATOMS[b]) / ATOMS[c]))
                # (a*b)/c
                if ATOMS[c] != 0:
                    out.append((f"({a}*{b})/{c}", (ATOMS[a] * ATOMS[b]) / ATOMS[c]))
                # a/(b*c)
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


def top_matches(candidates, target, top=15):
    scored = []
    for expr, v in candidates:
        if not math.isfinite(v):
            continue
        if v <= 0:
            continue   # frequencies are positive
        err_pct = abs(v - target) / target * 100
        scored.append((err_pct, expr, v))
    scored.sort()
    # dedupe by value (keep shortest expression for each unique value bin)
    seen = {}
    for err, expr, v in scored:
        key = round(v, 10)
        if key not in seen or len(expr) < len(seen[key][1]):
            seen[key] = (err, expr, v)
    deduped = sorted(seen.values())
    return deduped[:top]


def main():
    verify_precommit()
    print("CR003 -- Ringdown Frequency in Substrate Units (EXPLORATORY)")
    print(f"precommit hash : {PRECOMMIT_HASH}")
    print()
    print("Substrate atoms (CR258 sealed):")
    for k, v in ATOMS.items():
        print(f"  {k:>5s} = {v}")
    print()
    print(f"GR Schwarzschild l=m=2 n=0 QNM dimensionless frequency:")
    print(f"  omega_R * M = {TARGET_R}")
    print(f"  omega_I * M = {TARGET_I}")
    print(f"  Q = omega_R / (2 omega_I) = {TARGET_R/(2*TARGET_I):.6f}")
    print()

    candidates = enumerate_candidates()
    print(f"Enumerated {len(candidates)} candidate expressions")
    print(f"(deduped by numerical value for display only)")
    print()

    # ===== Real part =====
    print(f"=== Top 15 candidates for omega_R * M = {TARGET_R} ===")
    print(f"  {'rank':>4s}  {'err %':>9s}  {'expression':<32s}  {'value':>12s}")
    top_R = top_matches(candidates, TARGET_R, top=15)
    for i, (err, expr, v) in enumerate(top_R, start=1):
        print(f"  {i:>4d}  {err:>9.4f}  {expr:<32s}  {v:>12.7f}")
    best_R = top_R[0]
    print()
    print(f"  BEST omega_R candidate: {best_R[1]} = {best_R[2]:.7f}")
    print(f"  relative error: {best_R[0]:.4f}%")
    cond_R = best_R[0] <= GATE_PASS
    R_status = "PASS" if cond_R else ("BOUNDARY" if best_R[0] <= GATE_BOUNDARY else "FAIL")
    print(f"  gate: {R_status}")
    print()

    # ===== Imag part =====
    print(f"=== Top 15 candidates for omega_I * M = {TARGET_I} ===")
    print(f"  {'rank':>4s}  {'err %':>9s}  {'expression':<32s}  {'value':>12s}")
    top_I = top_matches(candidates, TARGET_I, top=15)
    for i, (err, expr, v) in enumerate(top_I, start=1):
        print(f"  {i:>4d}  {err:>9.4f}  {expr:<32s}  {v:>12.7f}")
    best_I = top_I[0]
    print()
    print(f"  BEST omega_I candidate: {best_I[1]} = {best_I[2]:.7f}")
    print(f"  relative error: {best_I[0]:.4f}%")
    cond_I = best_I[0] <= GATE_PASS
    I_status = "PASS" if cond_I else ("BOUNDARY" if best_I[0] <= GATE_BOUNDARY else "FAIL")
    print(f"  gate: {I_status}")
    print()

    # ===== Quality factor cross-check =====
    Q_sam = best_R[2] / (2 * best_I[2])
    Q_gr = TARGET_R / (2 * TARGET_I)
    Q_err = abs(Q_sam - Q_gr) / Q_gr * 100
    print(f"=== Quality factor cross-check (not gated) ===")
    print(f"  Q_SAM = (BEST R) / (2 * BEST I) = {Q_sam:.6f}")
    print(f"  Q_GR  = {TARGET_R} / (2 * {TARGET_I}) = {Q_gr:.6f}")
    print(f"  relative error: {Q_err:.4f}%")
    print()

    # ===== Joint verdict =====
    if cond_R and cond_I:
        verdict = "PASS"
    elif R_status == "FAIL" or I_status == "FAIL":
        verdict = "FAIL"
    else:
        verdict = "BOUNDARY"

    print(f"CR003 VERDICT: {verdict}")
    print(f"  omega_R gate: {R_status}  ({best_R[0]:.4f}% off)")
    print(f"  omega_I gate: {I_status}  ({best_I[0]:.4f}% off)")
    print()

    # ===== Outputs =====
    csv_path = os.path.join(HERE, "CR003_candidates.csv")
    with open(csv_path, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["part", "rank", "expression", "value", "target", "err_pct"])
        for i, (err, expr, v) in enumerate(top_R, start=1):
            w.writerow(["omega_R", i, expr, v, TARGET_R, err])
        for i, (err, expr, v) in enumerate(top_I, start=1):
            w.writerow(["omega_I", i, expr, v, TARGET_I, err])

    summary = {
        "artifact": "CR003_RINGDOWN_FREQUENCY_IN_SUBSTRATE_UNITS",
        "mode": "EXPLORATORY",
        "verdict": verdict,
        "precommit_hash": PRECOMMIT_HASH,
        "target": {
            "omega_R_times_M": TARGET_R,
            "omega_I_times_M": TARGET_I,
            "Q_GR": Q_gr,
            "source": "Berti, Cardoso, Starinets 2009 Living Rev Rel 12 2",
        },
        "gates": {
            "PASS_pct": GATE_PASS,
            "BOUNDARY_pct": GATE_BOUNDARY,
        },
        "search_space": {
            "candidate_count": len(candidates),
            "forms": ["a/b", "a/(b+c)", "a/(b-c)", "(a+b)/c", "(a-b)/c",
                      "(a*b)/c", "a/(b*c)", "(a*b)/(c*d)"],
            "atoms": list(ATOMS.keys()),
        },
        "best_R": {
            "expression": best_R[1],
            "value": best_R[2],
            "err_pct": best_R[0],
            "status": R_status,
        },
        "best_I": {
            "expression": best_I[1],
            "value": best_I[2],
            "err_pct": best_I[0],
            "status": I_status,
        },
        "Q_cross_check": {
            "Q_SAM": Q_sam,
            "Q_GR": Q_gr,
            "err_pct": Q_err,
        },
    }
    with open(os.path.join(HERE, "CR003_summary.json"), "w",
              encoding="utf-8") as f:
        json.dump(summary, f, indent=2, default=str)

    runner_hash = file_sha256(__file__)
    print(f"runner SHA-256 : {runner_hash}")


if __name__ == "__main__":
    main()
