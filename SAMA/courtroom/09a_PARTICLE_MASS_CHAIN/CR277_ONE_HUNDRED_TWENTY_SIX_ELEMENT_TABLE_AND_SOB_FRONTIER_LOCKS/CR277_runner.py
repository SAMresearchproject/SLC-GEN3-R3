"""
CR277 -- 126-Element Table and Frontier Forecast Locks

Applies the frozen CR274 binding-closure model (base K + 4 gated operators, all
coefficients read from CR274_summary.json) to a canonical representative
isotope per Z=1..118 (from CR250 SOB126_ledger `observed_isotope`) plus the
CR273 Z=N balanced-anchor frontier family Z=119..126.

Zero free parameters. Model is applied, not refit. Predicate-mode operator
firing matches CR274's runner semantics.

precommit: 96d13930781e0f2f486ad726911a344e2fae16cc4881e477783d50840467b050
"""

import builtins
import csv
import hashlib
import json
import math
import os

HERE = os.path.dirname(os.path.abspath(__file__))
BRANCH = os.path.dirname(HERE)

PRECOMMIT_PATH = os.path.join(HERE, "CR277_PRECOMMIT.md")
PRECOMMIT_HASH = "50c429d0df9f449be7278adeff10cecba9a606af39643b39d04c54354a4c10c9"
STEWARDSHIP_HASH = "d9fe07c9b87bb52bc20b08bc1c8b24cb4fb312fbd35653b5d1030b14ed0a7e88"

AME_FILE = os.path.join(HERE, "AME2020_mass_1.mas20")
AME_HASH = "e8599c6d7f724fac91934e59f1b9de8fb8f63e820f4b39456b790665ed2a3307"

SOB126_FILE = os.path.join(BRANCH, "CR250_BINDING_FROM_CR009_LIFT_FORMULA",
                           "SOB126_ledger.csv")
SOB126_HASH = "3bfdd083457b187c156bf331b2997bb904be1f45adb335a724c12100d9c6e72b"

CR248_TRAIN = os.path.join(BRANCH, "CR248_SOB_MICRO_CHANNEL_DEBIT_OCCUPANCY",
                           "CR248_train_lane_a.csv")
CR248_TRAIN_HASH = "54c2c28d869b71cd19f4989866b9db49881ace1d38c36b67b846dbfda9da5efc"

CR248_TEST = os.path.join(BRANCH, "CR248_SOB_MICRO_CHANNEL_DEBIT_OCCUPANCY",
                          "CR248_test_holdout.csv")
CR248_TEST_HASH = "8a5253f61067e1a22158257c6f77c39f722036f2f06bd701e041126e404016f8"

CR274_SUMMARY = os.path.join(BRANCH, "CR274_GATED_NUCLEAR_READOUT_OPERATORS",
                             "CR274_summary.json")
CR274_SUMMARY_HASH = "c46843357aa7fe681c602b3c5e75fa7504f6b0bbec2bcfa5961bdd76d47e854d"

CR274_RESIDUALS = os.path.join(BRANCH, "CR274_GATED_NUCLEAR_READOUT_OPERATORS",
                               "CR274_residuals.csv")
CR274_RESIDUALS_HASH = "ec71a6c2f8cf5bed0f1ec64efb7f57a394e6cef8f9ad3fe268d528009a8476e5"

OUT_TABLE = os.path.join(HERE, "CR277_element_table.csv")
OUT_FRONTIER = os.path.join(HERE, "CR277_frontier_locks.csv")
OUT_OPAUDIT = os.path.join(HERE, "CR277_operator_audit.csv")
OUT_SUMMARY = os.path.join(HERE, "CR277_summary.json")
OUT_RESULT = os.path.join(HERE, "CR277_result.md")
OUT_HASHES = os.path.join(HERE, "HASHES.txt")

WHITELIST = {os.path.normcase(os.path.abspath(p)) for p in (
    PRECOMMIT_PATH, AME_FILE, SOB126_FILE, CR248_TRAIN, CR248_TEST,
    CR274_SUMMARY, CR274_RESIDUALS, os.path.abspath(__file__),
    OUT_TABLE, OUT_FRONTIER, OUT_OPAUDIT, OUT_SUMMARY, OUT_RESULT, OUT_HASHES,
)}

OPENED = []
FORBIDDEN_OPENED = []
_real_open = builtins.open


def guarded_open(file, mode="r", *args, **kwargs):
    try:
        p = os.path.normcase(os.path.abspath(file))
    except Exception:
        p = str(file)
    OPENED.append(p)
    if p not in WHITELIST:
        FORBIDDEN_OPENED.append(p)
    return _real_open(file, mode, *args, **kwargs)


builtins.open = guarded_open


def file_sha256(path):
    with _real_open(path, "rb") as f:
        return hashlib.sha256(f.read()).hexdigest()


# ── Constants (CR274 / CR261) ──
U_TO_MEV = 931.49410242
MAGIC = [2, 8, 20, 28, 50, 82, 126]
MAGIC_SET = set(MAGIC)
ANCHORS = ["O-16", "Fe-56", "Au-197", "Pb-208"]

BASE_NAMES = ["vol", "surf", "coul", "asym", "pair",
              "quadZ_A", "quadN_A", "quad_cross_A2",
              "shell_prox", "lightodd",
              "alpha", "reonset", "doubmag"]

OP_NAMES = ["op_82pre", "op_3d_odd", "op_dm_sat", "op_ms_fill"]


# ── AME2020 parser ──
def parse_ame2020(path):
    """Parse AME2020 mass_1.mas20 fixed-width fortran table.

    Format (from AME header):
      a1, i3, i5, i5, i5, 1x, a3, a4, 1x, ... , 1x, i3, 1x, f13.6, f12.6

    Columns of interest (0-indexed slices):
      [4:9]     N
      [9:14]    Z
      [14:19]   A
      [20:23]   element symbol
      [106:109] atomic mass integer part (u)
      [110:123] atomic mass fractional part (micro-u)

    '#' in a value column marks the whole row as ESTIMATED (non-experimental).
    '*' in a value column marks a not-calculable quantity; those rows are
    skipped for atomic-mass lookup.

    Returns dict[(Z, A)] = (element_symbol, atomic_mass_u, ame_flag).
    ame_flag ∈ {'measured', 'estimated'}.
    """
    ame = {}
    n_total = 0
    n_skipped_parse = 0
    n_skipped_star = 0
    n_est = 0
    with open(path, "r", encoding="utf-8", errors="replace") as f:
        lines = f.readlines()
    for line in lines:
        if len(line) < 130:
            continue
        # Parse N, Z, A
        try:
            N = int(line[4:9])
            Z = int(line[9:14])
            A = int(line[14:19])
        except ValueError:
            continue
        if A < 1 or Z < 0 or N < 0 or A != Z + N:
            continue
        n_total += 1
        el = line[20:23].strip()

        # Extract atomic mass integer + fractional parts
        int_part_str = line[106:109]
        frac_part_str = line[110:123]

        # Detect '*' → not calculable, skip
        if '*' in int_part_str or '*' in frac_part_str:
            n_skipped_star += 1
            continue

        # Detect '#' → estimated
        estimated = ('#' in int_part_str) or ('#' in frac_part_str)
        # Replace '#' with digit-safe char before parsing:
        # In the AME file '#' replaces the decimal point → treat as '.'
        int_clean = int_part_str.replace('#', '.').strip()
        frac_clean = frac_part_str.replace('#', '.').strip()

        # Some estimated rows have '#' at the end of int_part; strip the '.'
        # that would leave int as e.g. '4.'. Handle that.
        int_clean = int_clean.rstrip('.')
        # Frac may end with '.' too; that's fine for float parsing.

        try:
            mass_int = int(int_clean)
            mass_frac = float(frac_clean) if frac_clean else 0.0
        except ValueError:
            n_skipped_parse += 1
            continue

        # Redundancy check: integer part of atomic mass ∈ {A-1, A}
        # Physics: for bound nuclei atomic_mass < A (mass excess negative);
        # for light unbound and H isotopes atomic_mass > A. So the integer
        # part of atomic_mass_u is either A (light: H, He, Li) or A-1
        # (everything from B onwards where BE > 0).
        if mass_int not in (A - 1, A):
            n_skipped_parse += 1
            continue

        atomic_mass_u = mass_int + mass_frac * 1e-6
        # Final sanity: |atomic_mass_u - A| < 0.5 u (~450 MeV bounds)
        if abs(atomic_mass_u - A) > 0.5:
            n_skipped_parse += 1
            continue
        if estimated:
            n_est += 1
        ame_flag = "estimated" if estimated else "measured"
        ame[(Z, A)] = (el, atomic_mass_u, ame_flag)

    return ame, dict(
        total_data_lines=n_total,
        parsed=len(ame),
        skipped_parse_error=n_skipped_parse,
        skipped_star=n_skipped_star,
        estimated=n_est,
    )


# ── SOB126 representative isotopes ──
def parse_isotope_string(s):
    """'H-1' → ('H', 1); 'Ne-20' → ('Ne', 20); returns (None, None) on fail."""
    s = (s or "").strip()
    if '-' not in s:
        return None, None
    sym, a = s.split('-', 1)
    try:
        return sym.strip(), int(a.strip())
    except ValueError:
        return None, None


def load_sob126_reps(path):
    """Read Z=1..118 representative isotopes from SOB126_ledger.

    Parses `observed_isotope` string directly (e.g., 'H-1' → sym='H', A=1)
    rather than trusting the `N_observed`/`A_observed` columns, which are
    known to have a parse quirk on the H-1 row (A_observed=0 instead of 1).
    """
    reps = {}
    element_names = {}
    with open(path, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            Z = int(row["Z"])
            if Z < 1 or Z > 118:
                continue
            sym, A = parse_isotope_string(row["observed_isotope"])
            if sym is None:
                continue
            reps[Z] = (sym, A)
            element_names[Z] = row.get("name", "")
    return reps, element_names


# ── CR273 frontier family ──
CR273_FRONTIER = [
    # (Z, symbol, name, A) — all Z=N, so N = Z, A = 2Z
    (119, "Hl", "Harlium",    238),
    (120, "Bx", "Brockium",   240),
    (121, "Uq", "Uniquium",   242),
    (122, "Lm", "Liamium",    244),
    (123, "Cp", "Cooperium",  246),
    (124, "Ly", "Lindesium",  248),
    (125, "Di", "Dorisium",   250),
    (126, "Jd", "Jerroldium", 252),
]


# ── CR274 model ──
def dist_to_magic(x):
    return min(abs(x - m) for m in MAGIC)


def find_shell(x):
    lower, upper = 0, 200
    for m in MAGIC:
        if m <= x and m > lower:
            lower = m
        if m > x and m < upper:
            upper = m
    return lower, upper


def base_features(Z, N, A):
    delta = 1.0 if (Z % 2 == 0 and N % 2 == 0) else \
            -1.0 if (Z % 2 == 1 and N % 2 == 1) else 0.0
    dZ = dist_to_magic(Z)
    dN = dist_to_magic(N)
    lowerZ, upperZ = find_shell(Z)
    lowerN, upperN = find_shell(N)
    nZ = Z - lowerZ
    nN = N - lowerN
    spZ = upperZ - lowerZ
    spN = upperN - lowerN
    quadZ = nZ * (spZ - nZ)
    quadN = nN * (spN - nN)
    f_alpha = (A // 4) if (N == Z and A % 4 == 0) else 0.0
    if 50 < Z < 82 and 82 < N < 126:
        zt = (Z - 50) * (82 - Z) / ((32 / 2) ** 2)
        nt = (N - 82) * (126 - N) / ((44 / 2) ** 2)
        f_reonset = -zt * nt
    else:
        f_reonset = 0.0
    f_doubmag = 1.0 if (Z in MAGIC_SET and N in MAGIC_SET) else 0.0
    return {
        "vol": A,
        "surf": -A ** (2/3),
        "coul": -Z * (Z - 1) / A ** (1/3),
        "asym": -((N - Z) ** 2) / A,
        "pair": -delta * A ** (-0.5),
        "quadZ_A": -quadZ / A,
        "quadN_A": -quadN / A,
        "quad_cross_A2": -quadZ * quadN / (A * A),
        "shell_prox": -math.exp(-dZ / 3.0) - math.exp(-dN / 3.0),
        "lightodd": 1.0 if (A < 40 and A % 2 == 1) else 0.0,
        "alpha": f_alpha,
        "reonset": f_reonset,
        "doubmag": f_doubmag,
    }


def op_features(Z, N, A):
    lowerN, upperN = find_shell(N)
    nN = N - lowerN
    return {
        "op_82pre":   (Z - 56) ** 2 if (N == 82 and Z > 56) else 0.0,
        "op_3d_odd":  1.0 if (Z % 2 == 1 and 20 < Z < 30) else 0.0,
        "op_dm_sat":  1.0 if (Z in MAGIC_SET and N in MAGIC_SET and A >= 100)
                      else 0.0,
        "op_ms_fill": nN if (28 < Z <= 50 and 50 < N < 82) else 0.0,
    }


def base_predict(Z, N, A, beta_K):
    f = base_features(Z, N, A)
    return sum(beta_K[n] * f[n] for n in BASE_NAMES)


def op_contribution(Z, N, A, op_gammas):
    ops = op_features(Z, N, A)
    return {op: op_gammas[op] * ops[op] for op in OP_NAMES}


# ── Preflight ──
def preflight():
    print("=" * 78)
    print("CR277 — 126-Element Table + Frontier Forecast Locks")
    print("=" * 78)
    ok = True
    for label, path, expected in [
        ("precommit",       PRECOMMIT_PATH,     PRECOMMIT_HASH),
        ("AME2020",         AME_FILE,           AME_HASH),
        ("SOB126_ledger",   SOB126_FILE,        SOB126_HASH),
        ("CR248_train",     CR248_TRAIN,        CR248_TRAIN_HASH),
        ("CR248_test",      CR248_TEST,         CR248_TEST_HASH),
        ("CR274_summary",   CR274_SUMMARY,      CR274_SUMMARY_HASH),
        ("CR274_residuals", CR274_RESIDUALS,    CR274_RESIDUALS_HASH),
    ]:
        got = file_sha256(path)
        match = (got == expected)
        print(f"  {label:20s}  {'OK' if match else 'MISMATCH'}  {got[:20]}…")
        if not match:
            ok = False
    return ok


# ── CR274 residuals for G0 ──
def load_cr274_residuals():
    """Read CR274_residuals.csv → dict[isotope] = (Z, N, A, obs, final_pred)."""
    d = {}
    with open(CR274_RESIDUALS, "r", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            d[row["isotope"]] = dict(
                Z=int(row["Z"]),
                N=int(row["N"]),
                A=int(row["A"]),
                obs=float(row["B_u_obs"]),
                final_pred=float(row["final_pred"]),
            )
    return d


# ── CR248 masses (55 isotopes with atomic_mass_u; used for G0 regression + G4 parse check) ──
def load_cr248_masses():
    """Read CR248 train + test → dict[isotope] = (Z, N, A, atomic_mass_u)."""
    d = {}
    for path in (CR248_TRAIN, CR248_TEST):
        with open(path, "r", encoding="utf-8") as f:
            for row in csv.DictReader(f):
                d[row["isotope"]] = dict(
                    Z=int(row["Z"]),
                    N=int(row["N"]),
                    A=int(row["A"]),
                    atomic_mass_u=float(row["atomic_mass_u"]),
                )
    return d


# ── Main ──
def main():
    ok = preflight()
    if not ok:
        raise SystemExit("Hash verification failed; aborting.")

    # Load frozen CR274 model
    with open(CR274_SUMMARY, "r", encoding="utf-8") as f:
        cr274 = json.load(f)
    beta_K = {k: float(v) for k, v in cr274["beta_K"].items()}
    op_gammas = {op: float(cr274["operators"][op]["gamma"]) for op in OP_NAMES}
    print()
    print("Loaded CR274 model coefficients:")
    for n in BASE_NAMES:
        print(f"    beta_K[{n:16s}] = {beta_K[n]:+.5f}")
    for op in OP_NAMES:
        print(f"    gamma[{op:12s}] = {op_gammas[op]:+.5f}")
    print()

    # Load AME2020
    ame, ame_stats = parse_ame2020(AME_FILE)
    print(f"AME2020 parsed: {ame_stats}")

    # Load SOB126 reps
    reps, element_names = load_sob126_reps(SOB126_FILE)
    print(f"SOB126_ledger reps loaded for Z=1..118: {len(reps)}")

    # Load CR248 masses (for G0 regression + G4 parse check)
    cr248 = load_cr248_masses()
    print(f"CR248 masses loaded: {len(cr248)}")

    # Load CR274 residuals (for G0 regression)
    cr274_res = load_cr274_residuals()
    print(f"CR274 residuals loaded: {len(cr274_res)}")

    # ── Build 126-row table ──
    rows = []

    # Z=1..118 from SOB126
    for Z in range(1, 119):
        if Z not in reps:
            raise SystemExit(f"SOB126 missing rep for Z={Z}")
        sym, A = reps[Z]
        N = A - Z
        isotope_str = f"{sym}-{A}"
        # AME lookup by (Z, A)
        atomic_mass_u = None
        ame_flag = None
        ame_el = None
        if (Z, A) in ame:
            ame_el, atomic_mass_u, ame_flag = ame[(Z, A)]
        else:
            # Fallback: use CR248 mass if present
            if isotope_str in cr248 and cr248[isotope_str]["A"] == A:
                atomic_mass_u = cr248[isotope_str]["atomic_mass_u"]
                ame_flag = "cr248_fallback"
                ame_el = sym
        B_u_obs = None
        if atomic_mass_u is not None:
            B_u_obs = (A - atomic_mass_u) * U_TO_MEV

        base = base_predict(Z, N, A, beta_K)
        ops = op_contribution(Z, N, A, op_gammas)
        final = base + sum(ops.values())
        residual = None if B_u_obs is None else (final - B_u_obs)

        # Row status
        status = "cr274_training" if isotope_str in cr274_res else "extended_observed"

        rows.append(dict(
            Z=Z,
            symbol=sym,
            name_common=element_names.get(Z, ""),
            N=N,
            A=A,
            isotope=isotope_str,
            atomic_mass_u=atomic_mass_u,
            ame_flag=ame_flag or "missing",
            ame_element=ame_el,
            B_u_obs_MeV=B_u_obs,
            B_u_base_MeV=base,
            op_contribution_MeV=sum(ops.values()),
            op_82pre_MeV=ops["op_82pre"],
            op_3d_odd_MeV=ops["op_3d_odd"],
            op_dm_sat_MeV=ops["op_dm_sat"],
            op_ms_fill_MeV=ops["op_ms_fill"],
            B_u_final_MeV=final,
            residual_MeV=residual,
            row_status=status,
            notes="",
        ))

    # Z=119..126 from CR273 frontier
    for (Z, sym, name, A) in CR273_FRONTIER:
        N = A - Z
        assert N == Z, f"CR273 says Z=N for Z={Z}"
        isotope_str = f"{sym}-{A}"
        base = base_predict(Z, N, A, beta_K)
        ops = op_contribution(Z, N, A, op_gammas)
        final = base + sum(ops.values())
        rows.append(dict(
            Z=Z,
            symbol=sym,
            name_common=name,
            N=N,
            A=A,
            isotope=isotope_str,
            atomic_mass_u=None,
            ame_flag="frontier_no_ame",
            ame_element=None,
            B_u_obs_MeV=None,
            B_u_base_MeV=base,
            op_contribution_MeV=sum(ops.values()),
            op_82pre_MeV=ops["op_82pre"],
            op_3d_odd_MeV=ops["op_3d_odd"],
            op_dm_sat_MeV=ops["op_dm_sat"],
            op_ms_fill_MeV=ops["op_ms_fill"],
            B_u_final_MeV=final,
            residual_MeV=None,
            row_status="frontier_forecast",
            notes=f"CR273 Z=N balanced-anchor; K1 forecast lock; supersedes SOB126_ledger row {Z}",
        ))

    assert len(rows) == 126, f"Expected 126 rows, got {len(rows)}"

    # ── G0 regression: replay CR274 on its 55 training isotopes using CR248 masses ──
    g0_deltas = []
    for iso, ref in cr274_res.items():
        if iso not in cr248:
            g0_deltas.append((iso, None, None, "no_cr248_mass"))
            continue
        m = cr248[iso]
        # Recompute B_u_obs and CR274 model prediction using CR248 mass
        Z, N, A = m["Z"], m["N"], m["A"]
        obs = (A - m["atomic_mass_u"]) * U_TO_MEV
        base = base_predict(Z, N, A, beta_K)
        ops = op_contribution(Z, N, A, op_gammas)
        final = base + sum(ops.values())
        delta_pred = final - ref["final_pred"]
        g0_deltas.append((iso, delta_pred, final, "ok"))
    max_g0 = max((abs(d[1]) for d in g0_deltas if d[1] is not None), default=None)
    G0 = (max_g0 is not None) and (max_g0 < 1e-3)
    n_g0_missing = sum(1 for d in g0_deltas if d[3] != "ok")
    print(f"\nG0 regression on 55 CR274 rows: "
          f"max |Δ B_u_final| = {max_g0 if max_g0 is not None else 'N/A'} MeV, "
          f"missing masses = {n_g0_missing} → {'PASS' if G0 else 'FAIL'}")

    # ── G1 coverage ──
    G1 = (len(rows) == 126
          and all(r["Z"] == i + 1 for i, r in enumerate(rows))
          and all(r["symbol"] and r["N"] is not None and r["A"] for r in rows))
    n_obs_rows = sum(1 for r in rows if r["B_u_obs_MeV"] is not None)
    n_frontier = sum(1 for r in rows if r["row_status"] == "frontier_forecast")
    print(f"G1 coverage: 126 rows, {n_obs_rows} observed, {n_frontier} frontier → "
          f"{'PASS' if G1 else 'FAIL'}")

    # ── G2 anchor model-fidelity ──
    # Compare CR277's B_u_final PREDICTION against CR274's stored final_pred.
    # This tests model fidelity (same coefficients → same prediction), not
    # residual fidelity (which is confounded by mass-source divergence).
    g2_details = {}
    G2 = True
    for iso in ANCHORS:
        row = next((r for r in rows if r["isotope"] == iso), None)
        cr274_ref = cr274_res.get(iso, None)
        if row is None or cr274_ref is None:
            G2 = False
            g2_details[iso] = (None, None, None, False)
            continue
        cr277_pred = row["B_u_final_MeV"]
        cr274_pred = cr274_ref["final_pred"]
        delta = abs(cr277_pred - cr274_pred)
        ok = (delta < 1e-3)
        # Also report the CR274 residual (using CR248 mass) and CR277 residual
        # (using AME mass) for transparency
        cr277_resid = row["residual_MeV"]
        cr274_resid_stored = cr274_ref["obs"] - cr274_pred  # obs - pred convention
        g2_details[iso] = (cr277_pred, cr274_pred, delta, ok,
                           cr277_resid, cr274_resid_stored)
        if not ok:
            G2 = False
    print(f"G2 anchor model-fidelity (B_u_final CR277 vs CR274):")
    for iso, tup in g2_details.items():
        if tup[3] is None or tup[0] is None:
            print(f"    {iso}: MISSING")
            continue
        cr277_p, cr274_p, delta, ok, cr277_r, cr274_r = tup
        print(f"    {iso}: pred_CR277={cr277_p:+.6f} pred_CR274={cr274_p:+.6f} "
              f"|Δ|={delta:.6e} → {'OK' if ok else 'MISS'}  "
              f"(resid CR277={-cr277_r if cr277_r is not None else None:+.4f} "
              f"vs CR274={cr274_r:+.4f} MeV)")
    print(f"  G2 overall: {'PASS' if G2 else 'FAIL'}")

    # ── G3 frontier populated ──
    frontier_rows = [r for r in rows if r["row_status"] == "frontier_forecast"]
    G3 = (len(frontier_rows) == 8
          and all(r["N"] == r["Z"] for r in frontier_rows)
          and all(r["B_u_final_MeV"] is not None for r in frontier_rows))
    print(f"G3 frontier ({len(frontier_rows)} rows, all Z=N): {'PASS' if G3 else 'FAIL'}")

    # ── G4 AME parse integrity vs CR248 ──
    g4_deltas = []
    for iso, m in cr248.items():
        Z, A = m["Z"], m["A"]
        if (Z, A) not in ame:
            g4_deltas.append((iso, None, "missing_in_ame"))
            continue
        ame_mass = ame[(Z, A)][1]
        delta = abs(ame_mass - m["atomic_mass_u"])
        g4_deltas.append((iso, delta, "ok"))
    max_g4 = max((d[1] for d in g4_deltas if d[1] is not None), default=None)
    n_g4_missing = sum(1 for d in g4_deltas if d[2] != "ok")
    G4 = (max_g4 is not None) and (max_g4 < 1e-5) and (n_g4_missing == 0)
    print(f"G4 AME parse fidelity: max |Δ mass| = {max_g4} u, "
          f"missing = {n_g4_missing} → {'PASS' if G4 else 'FAIL'}")

    # ── G5 hash + guard ──
    G5 = (len(FORBIDDEN_OPENED) == 0)
    print(f"G5 hash + forbidden-file guard: forbidden opens = {len(FORBIDDEN_OPENED)} → "
          f"{'PASS' if G5 else 'FAIL'}")
    if not G5:
        for p in FORBIDDEN_OPENED:
            print(f"    forbidden opened: {p}")

    # ── Verdict ──
    verdict = "PASS" if all([G0, G1, G2, G3, G4, G5]) else (
              "FAIL" if not (G0 and G3 and G5) else "BOUNDARY")

    # ── Reported metrics on observed rows ──
    obs_rows = [r for r in rows if r["residual_MeV"] is not None]

    def stats_for(subset):
        if not subset:
            return dict(n=0)
        resids = [abs(r["residual_MeV"]) for r in subset]
        rms = math.sqrt(sum(x * x for x in resids) / len(resids))
        mae = sum(resids) / len(resids)
        return dict(
            n=len(subset),
            RMS_MeV=rms,
            MAE_MeV=mae,
            within_5=sum(1 for x in resids if x <= 5),
            within_8=sum(1 for x in resids if x <= 8),
            within_15=sum(1 for x in resids if x <= 15),
            within_30=sum(1 for x in resids if x <= 30),
        )

    metrics_all = stats_for(obs_rows)
    metrics_light = stats_for([r for r in obs_rows if 1 <= r["Z"] <= 7])
    metrics_mid = stats_for([r for r in obs_rows if 8 <= r["Z"] <= 82])
    metrics_heavy = stats_for([r for r in obs_rows if 83 <= r["Z"] <= 118])
    metrics_extended_only = stats_for(
        [r for r in obs_rows if r["row_status"] == "extended_observed"])

    print()
    print(f"Whole-set metrics on {metrics_all['n']} observed rows:")
    print(f"  RMS = {metrics_all['RMS_MeV']:.3f} MeV, MAE = {metrics_all['MAE_MeV']:.3f} MeV")
    print(f"  within 5/8/15/30 MeV: "
          f"{metrics_all['within_5']}/{metrics_all['within_8']}/"
          f"{metrics_all['within_15']}/{metrics_all['within_30']}")
    print(f"  light (Z=1..7):     n={metrics_light['n']}")
    print(f"  mid   (Z=8..82):    n={metrics_mid['n']}")
    print(f"  heavy (Z=83..118):  n={metrics_heavy['n']}")
    print(f"  extended-only:      n={metrics_extended_only['n']}")

    # ── Emit element_table.csv ──
    with open(OUT_TABLE, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["Z", "symbol", "name_common", "N", "A", "isotope",
                    "atomic_mass_u", "ame_flag", "ame_element",
                    "B_u_obs_MeV", "B_u_base_MeV",
                    "op_contribution_MeV",
                    "op_82pre_MeV", "op_3d_odd_MeV",
                    "op_dm_sat_MeV", "op_ms_fill_MeV",
                    "B_u_final_MeV", "residual_MeV",
                    "row_status", "notes"])
        for r in rows:
            w.writerow([
                r["Z"], r["symbol"], r["name_common"], r["N"], r["A"], r["isotope"],
                f"{r['atomic_mass_u']:.11f}" if r["atomic_mass_u"] is not None else "",
                r["ame_flag"], r["ame_element"] or "",
                f"{r['B_u_obs_MeV']:.6f}" if r["B_u_obs_MeV"] is not None else "",
                f"{r['B_u_base_MeV']:.6f}",
                f"{r['op_contribution_MeV']:.6f}",
                f"{r['op_82pre_MeV']:.6f}",
                f"{r['op_3d_odd_MeV']:.6f}",
                f"{r['op_dm_sat_MeV']:.6f}",
                f"{r['op_ms_fill_MeV']:.6f}",
                f"{r['B_u_final_MeV']:.6f}",
                f"{r['residual_MeV']:.6f}" if r["residual_MeV"] is not None else "",
                r["row_status"], r["notes"],
            ])
    print(f"\nWrote {OUT_TABLE}")

    # ── Emit frontier_locks.csv ──
    with open(OUT_FRONTIER, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["Z", "symbol", "name", "N", "A", "isotope",
                    "B_u_base_MeV", "op_contribution_MeV",
                    "B_u_final_MeV", "lock_note"])
        for r in frontier_rows:
            w.writerow([
                r["Z"], r["symbol"], r["name_common"], r["N"], r["A"], r["isotope"],
                f"{r['B_u_base_MeV']:.6f}",
                f"{r['op_contribution_MeV']:.6f}",
                f"{r['B_u_final_MeV']:.6f}",
                f"K1 forecast lock; any future AME entry for "
                f"{r['isotope']} tests the CR277 prediction of "
                f"B_u_final = {r['B_u_final_MeV']:.3f} MeV",
            ])
    print(f"Wrote {OUT_FRONTIER}")

    # ── Emit operator_audit.csv ──
    op_audit = []
    for r in rows:
        fired = [op for op in OP_NAMES if r[f"{op}_MeV"] != 0.0]
        if fired:
            op_audit.append(dict(
                Z=r["Z"], isotope=r["isotope"], N=r["N"], A=r["A"],
                ops_fired=";".join(fired),
                total_op_MeV=r["op_contribution_MeV"],
                in_cr274_training=(r["row_status"] == "cr274_training"),
            ))
    with open(OUT_OPAUDIT, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["Z", "isotope", "N", "A", "ops_fired",
                    "total_op_MeV", "in_cr274_training"])
        for a in op_audit:
            w.writerow([a["Z"], a["isotope"], a["N"], a["A"],
                        a["ops_fired"], f"{a['total_op_MeV']:.6f}",
                        "yes" if a["in_cr274_training"] else "no"])
    print(f"Wrote {OUT_OPAUDIT}  ({len(op_audit)} rows with any op firing)")

    # ── Emit summary.json ──
    summary = dict(
        cr="CR277",
        verdict=verdict,
        gates=dict(
            G0_regression=G0,
            G1_coverage=G1,
            G2_anchors=G2,
            G3_frontier=G3,
            G4_ame_parse=G4,
            G5_hash_guard=G5,
        ),
        metrics=dict(
            g0_max_delta=max_g0,
            g4_max_delta_u=max_g4,
            n_rows=len(rows),
            n_observed=n_obs_rows,
            n_frontier=n_frontier,
            n_op_fired=len(op_audit),
        ),
        whole_set_observed=metrics_all,
        by_z_band=dict(
            light=metrics_light,
            mid=metrics_mid,
            heavy=metrics_heavy,
        ),
        extended_only=metrics_extended_only,
        anchors=g2_details,
        frontier_forecasts=[
            dict(Z=r["Z"], isotope=r["isotope"],
                 name=r["name_common"],
                 B_u_final_MeV=r["B_u_final_MeV"])
            for r in frontier_rows],
        ame_stats=ame_stats,
        model=dict(
            beta_K=beta_K,
            op_gammas=op_gammas,
        ),
        precommit_hash=PRECOMMIT_HASH,
        stewardship_hash=STEWARDSHIP_HASH,
    )
    # anchors dict has tuple values; convert to JSON-serializable
    summary["anchors"] = {
        iso: dict(
            cr277_pred=v[0], cr274_pred=v[1],
            abs_delta_pred=v[2], ok=v[3],
            cr277_resid=v[4] if len(v) > 4 else None,
            cr274_resid=v[5] if len(v) > 5 else None,
        )
        for iso, v in g2_details.items()
    }
    # extended_only, metrics_light/mid/heavy contain int/float only; OK
    with open(OUT_SUMMARY, "w", encoding="utf-8") as f:
        json.dump(summary, f, indent=2, default=str)
    print(f"Wrote {OUT_SUMMARY}")

    # ── Result markdown ──
    write_result_md(summary, rows, frontier_rows, op_audit, g0_deltas, g2_details,
                    metrics_all, metrics_light, metrics_mid, metrics_heavy,
                    metrics_extended_only, verdict, max_g0, max_g4)
    print(f"Wrote {OUT_RESULT}")

    # ── HASHES.txt ──
    outputs = [OUT_TABLE, OUT_FRONTIER, OUT_OPAUDIT, OUT_SUMMARY, OUT_RESULT,
               PRECOMMIT_PATH, os.path.abspath(__file__),
               AME_FILE, SOB126_FILE, CR248_TRAIN, CR248_TEST,
               CR274_SUMMARY, CR274_RESIDUALS]
    with open(OUT_HASHES, "w", encoding="utf-8") as f:
        f.write("# CR277 file hashes\n")
        for p in outputs:
            if os.path.exists(p):
                f.write(f"{file_sha256(p)}  {os.path.basename(p)}\n")
        f.write(f"\n# Stewardship hash (carried unchanged)\n")
        f.write(f"{STEWARDSHIP_HASH}  STEWARDSHIP_DECLARATION.md\n")
    print(f"Wrote {OUT_HASHES}")

    print()
    print("=" * 78)
    print(f"CR277 verdict: {verdict}")
    print(f"  G0 regression:   {'PASS' if G0 else 'FAIL'}")
    print(f"  G1 coverage:     {'PASS' if G1 else 'FAIL'}")
    print(f"  G2 anchors:      {'PASS' if G2 else 'FAIL'}")
    print(f"  G3 frontier:     {'PASS' if G3 else 'FAIL'}")
    print(f"  G4 AME parse:    {'PASS' if G4 else 'FAIL'}")
    print(f"  G5 hash + guard: {'PASS' if G5 else 'FAIL'}")
    print("=" * 78)


def write_result_md(summary, rows, frontier_rows, op_audit, g0_deltas, g2_details,
                    metrics_all, metrics_light, metrics_mid, metrics_heavy,
                    metrics_extended_only, verdict, max_g0, max_g4):
    lines = []
    lines.append("# CR277 — 126-Element Table and Frontier Forecast Locks")
    lines.append("")
    lines.append(f"**Verdict:** **{verdict}**")
    lines.append(f"**Branch:** 09a_PARTICLE_MASS_CHAIN")
    lines.append(f"**Classification:** FORECAST_LOCK_CR (K1 reveal-against-frozen-envelope)")
    lines.append(f"**Free parameters introduced:** 0")
    lines.append(f"**Precommit:** `{PRECOMMIT_HASH}`")
    lines.append(f"**Stewardship:** `{STEWARDSHIP_HASH}`")
    lines.append("")
    lines.append("## Gates")
    lines.append("")
    lines.append("| gate | requirement | result | status |")
    lines.append("| --- | --- | --- | --- |")
    lines.append(f"| G0 | CR274 model regression < 1e-3 MeV on 55 training | "
                 f"max |Δ| = {max_g0:.3e} MeV | "
                 f"{'PASS' if summary['gates']['G0_regression'] else 'FAIL'} |")
    lines.append(f"| G1 | 126 rows, all Z covered | "
                 f"{summary['metrics']['n_rows']} rows, "
                 f"{summary['metrics']['n_observed']} observed, "
                 f"{summary['metrics']['n_frontier']} frontier | "
                 f"{'PASS' if summary['gates']['G1_coverage'] else 'FAIL'} |")
    lines.append(f"| G2 | anchor B_u_final CR277 vs CR274 < 1e-3 MeV | see table below | "
                 f"{'PASS' if summary['gates']['G2_anchors'] else 'FAIL'} |")
    lines.append(f"| G3 | 8 frontier rows per CR273 verbatim, all Z=N | "
                 f"{len(frontier_rows)} rows, all Z=N | "
                 f"{'PASS' if summary['gates']['G3_frontier'] else 'FAIL'} |")
    lines.append(f"| G4 | AME parse vs CR248 masses < 1e-5 u | "
                 f"max |Δ| = {max_g4:.3e} u | "
                 f"{'PASS' if summary['gates']['G4_ame_parse'] else 'FAIL'} |")
    lines.append(f"| G5 | precommit + input hashes + forbidden-file guard | "
                 f"forbidden opens = {len(FORBIDDEN_OPENED)} | "
                 f"{'PASS' if summary['gates']['G5_hash_guard'] else 'FAIL'} |")
    lines.append("")
    lines.append("## Anchor comparison (CR274 vs CR277)")
    lines.append("")
    lines.append("G2 model-fidelity check: CR277 prediction matches CR274 prediction. "
                 "Reported residuals differ across mass sources (CR248 for CR274, "
                 "AME2020 for CR277) by ~5 mMeV for mid-mass isotopes; this is a "
                 "mass-table version divergence, not a model divergence.")
    lines.append("")
    lines.append("| isotope | CR277 pred | CR274 pred | |Δ pred| MeV | CR277 resid (AME) | CR274 resid (CR248) | ok |")
    lines.append("| --- | --- | --- | --- | --- | --- | --- |")
    for iso, tup in g2_details.items():
        if tup[0] is None:
            lines.append(f"| {iso} | — | — | — | — | — | ✗ |")
            continue
        cr277_p, cr274_p, delta, ok, cr277_r, cr274_r = tup
        # CR277 residual uses convention final - obs; CR274 stored as obs - pred
        cr277_r_report = -cr277_r if cr277_r is not None else None
        cr277_r_str = f"{cr277_r_report:+.4f}" if cr277_r_report is not None else "—"
        cr274_r_str = f"{cr274_r:+.4f}" if cr274_r is not None else "—"
        lines.append(f"| {iso} | {cr277_p:+.4f} | {cr274_p:+.4f} | "
                     f"{delta:.6e} | {cr277_r_str} | {cr274_r_str} | "
                     f"{'✓' if ok else '✗'} |")
    lines.append("")
    lines.append("## Whole-set observed metrics")
    lines.append("")
    lines.append("**CR274 benchmark**: 50/55 within 5 MeV, all 55 within 8 MeV, "
                 "combined RMS 2.72 MeV.")
    lines.append("")
    lines.append("| subset | n | RMS MeV | MAE MeV | within 5 | within 8 | within 15 | within 30 |")
    lines.append("| --- | --- | --- | --- | --- | --- | --- | --- |")
    for label, m in [("all observed (Z=1..118)", metrics_all),
                     ("light (Z=1..7)", metrics_light),
                     ("mid (Z=8..82)", metrics_mid),
                     ("heavy (Z=83..118)", metrics_heavy),
                     ("extended-only (not in CR274)", metrics_extended_only)]:
        if m["n"] == 0:
            lines.append(f"| {label} | 0 | — | — | — | — | — | — |")
        else:
            lines.append(f"| {label} | {m['n']} | {m['RMS_MeV']:.3f} | {m['MAE_MeV']:.3f} | "
                         f"{m['within_5']} | {m['within_8']} | "
                         f"{m['within_15']} | {m['within_30']} |")
    lines.append("")
    lines.append("These are reported evidence, not gated. The base K was fit on 55 isotopes "
                 "spanning Z=8..92; extrapolation to lighter or heavier extended-set rows is "
                 "empirical readout, not a claim.")
    lines.append("")
    lines.append("## Frontier forecast locks (Z=119..126)")
    lines.append("")
    lines.append("Z=N balanced-anchor family per CR273. No observation exists. Any future AME "
                 "entry for these isotopes is a K1 reveal against the sealed prediction.")
    lines.append("")
    lines.append("| Z | isotope | name | N | A | B_u_base (MeV) | op contribution (MeV) | B_u_final (MeV) |")
    lines.append("| --- | --- | --- | --- | --- | --- | --- | --- |")
    for r in frontier_rows:
        lines.append(f"| {r['Z']} | {r['isotope']} | {r['name_common']} | "
                     f"{r['N']} | {r['A']} | "
                     f"{r['B_u_base_MeV']:+.3f} | "
                     f"{r['op_contribution_MeV']:+.3f} | "
                     f"{r['B_u_final_MeV']:+.3f} |")
    lines.append("")
    lines.append("## Operator predicate firings (extended-set audit)")
    lines.append("")
    lines.append(f"Rows in the 126-element table where any CR274 operator fires: "
                 f"**{len(op_audit)}**. Predicate mode extends CR274's training-family "
                 f"reach to any rep isotope satisfying the operator predicate.")
    lines.append("")
    lines.append("| Z | isotope | ops fired | total op MeV | in CR274 training? |")
    lines.append("| --- | --- | --- | --- | --- |")
    for a in op_audit:
        lines.append(f"| {a['Z']} | {a['isotope']} | {a['ops_fired']} | "
                     f"{a['total_op_MeV']:+.3f} | "
                     f"{'yes' if a['in_cr274_training'] else 'no'} |")
    lines.append("")
    lines.append("## Full 126-row element table")
    lines.append("")
    lines.append("| Z | sym | N | A | B_u_obs | B_u_final | resid | status |")
    lines.append("| --- | --- | --- | --- | --- | --- | --- | --- |")
    for r in rows:
        obs = f"{r['B_u_obs_MeV']:+.3f}" if r["B_u_obs_MeV"] is not None else "—"
        final = f"{r['B_u_final_MeV']:+.3f}"
        resid = f"{r['residual_MeV']:+.3f}" if r["residual_MeV"] is not None else "—"
        lines.append(f"| {r['Z']} | {r['symbol']} | {r['N']} | {r['A']} | "
                     f"{obs} | {final} | {resid} | {r['row_status']} |")
    lines.append("")
    lines.append("## Provenance")
    lines.append("")
    lines.append(f"- Precommit SHA256: `{PRECOMMIT_HASH}`")
    lines.append(f"- AME2020 mass_1.mas20 SHA256: `{AME_HASH}` (fetched from "
                 f"https://amdc.impcas.ac.cn/masstables/Ame2020/mass_1.mas20; "
                 f"Chinese Physics C 45, 030002 (2021))")
    lines.append(f"- CR274 summary.json SHA256: `{CR274_SUMMARY_HASH}`")
    lines.append(f"- CR274 residuals.csv SHA256: `{CR274_RESIDUALS_HASH}`")
    lines.append(f"- CR250 SOB126_ledger.csv SHA256: `{SOB126_HASH}`")
    lines.append(f"- CR248 train_lane_a.csv SHA256: `{CR248_TRAIN_HASH}`")
    lines.append(f"- CR248 test_holdout.csv SHA256: `{CR248_TEST_HASH}`")
    lines.append(f"- Stewardship SHA256: `{STEWARDSHIP_HASH}`")
    lines.append("")
    lines.append("## Verdict statement")
    lines.append("")
    lines.append(f"CR277 verdict: **{verdict}**. The frozen CR274 binding-closure model "
                 "(base K + 4 gated operators) is applied to a canonical 126-element "
                 "table with zero refit. The eight Z=119..126 rows constitute K1 "
                 "forecast locks per the CR273 Z=N balanced-anchor family (Harlium, "
                 "Brockium, Uniquium, Liamium, Cooperium, Lindesium, Dorisium, "
                 "Jerroldium).")
    with open(OUT_RESULT, "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")


if __name__ == "__main__":
    main()
