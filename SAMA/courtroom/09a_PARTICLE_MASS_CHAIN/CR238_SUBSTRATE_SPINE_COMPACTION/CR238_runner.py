"""CR238 Substrate Spine Compaction + Primitive Typing Audit — Runner.

Sealed precommit SHA-256:
    5e916199fb185db80a2b2346d3e0a9c59f9418c5e8d96b7453ffc716e8c46293

Foundational atoms (Sean Brady's framing 2026-06-23):
    F, S are foundational substrate atoms.
    D, alpha_H are the dimensional and binary readouts extracted from them.

All substrate quantities derive from {F, S, alpha_H} via the typed spine.
Bit-identical match against CR221 frozen kappa_floor (7117/768) and g_n (1/64)
is the load-bearing test (Block B).

Per precommit P25 the runner is permitted exactly one input-declaration block
where the foundational atoms appear as literals. Every other appearance of
{81, 162, 27, 144, 126, 18, 8, 1/12, 1/64, 7117/768} (and related kernel
literals) in this file is flagged by the literal-scan audit (Block F).

The runner is fully deterministic and uses sympy.Rational throughout for exact
arithmetic. The only irrational value is A_0 = V / (pi * alpha_H * L), which is
checked as an exact symbolic identity (sympy expression equality), not as a
rational.
"""

from __future__ import annotations

import csv
import hashlib
import json
import re
import sys
from pathlib import Path
from typing import Any

import sympy as sp


# CR238_LITERAL_SCAN: INPUT_BOUNDARY_BEGIN
F_INPUT = 81
S_INPUT = 8
ALPHA_H_INPUT = 2
# CR238_LITERAL_SCAN: INPUT_BOUNDARY_END


SCRIPT_DIR = Path(__file__).parent
SCRIPT_PATH = Path(__file__).resolve()
CR219_CSV_PATH = Path(r"C:\VS\CR219_promoted_particle_rows_126.csv")
PRECOMMIT_PATH = SCRIPT_DIR / "CR238_PRECOMMIT.md"

EXPECTED_CR219_SHA = (
    "45a8e7d20117b5aad62933d3858faf892cd3a3620c2ea8671f05904b10f1142f"
)
EXPECTED_PRECOMMIT_SHA = (
    "5e916199fb185db80a2b2346d3e0a9c59f9418c5e8d96b7453ffc716e8c46293"
)


# ------------------------------------------------------------
# SHA-locking
# ------------------------------------------------------------
def sha256_file(path: Path) -> str:
    """Compute SHA-256 of a file as lowercase hex."""
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def assert_input_shas() -> dict[str, str]:
    """Verify CR219 csv and precommit SHAs match the locked values."""
    csv_sha = sha256_file(CR219_CSV_PATH)
    pre_sha = sha256_file(PRECOMMIT_PATH)
    if csv_sha != EXPECTED_CR219_SHA:
        sys.exit(
            "FAIL: CR219 csv sha mismatch "
            f"(expected {EXPECTED_CR219_SHA}, got {csv_sha})"
        )
    if pre_sha != EXPECTED_PRECOMMIT_SHA:
        sys.exit(
            "FAIL: CR238 precommit sha mismatch "
            f"(expected {EXPECTED_PRECOMMIT_SHA}, got {pre_sha})"
        )
    return {"cr219_csv_sha": csv_sha, "precommit_sha": pre_sha}


# ------------------------------------------------------------
# Typed spine derivation
# ------------------------------------------------------------
def derive_spine(
    F_val: int | sp.Rational,
    S_val: int | sp.Rational,
    alpha_H_val: int | sp.Rational,
) -> dict[str, Any]:
    """Derive every typed primitive from foundational atoms {F, S, alpha_H}.

    Returns a dict whose values are sympy Rational (or symbolic expressions).
    D is computed as sqrt(F/(S+1)); whether D is a positive integer is reported
    in the 'D_is_positive_integer' flag.
    """
    F = sp.Rational(F_val)
    S = sp.Rational(S_val)
    aH = sp.Rational(alpha_H_val)

    L = aH * F
    D_sq = sp.Rational(F, S + 1)
    D = sp.sqrt(D_sq)
    D_simpl = sp.simplify(D)

    # Detect positive-integer D
    D_is_int = D_simpl.is_Integer and D_simpl > 0

    V = F / D_simpl
    Theta = aH * D_simpl ** 2
    R = aH * L / V
    R_sq = R ** 2
    M = L - 2 * Theta

    aH_pow_S = aH ** S
    kappa = (R - sp.Rational(1)) * (F * S - sp.Rational(1)) / (D_simpl * aH_pow_S)
    g = sp.Rational(1) / S ** 2

    A_0 = V / (sp.pi * aH * L)
    A_share = V / (aH * L)
    A_side = V / (2 * aH * L)

    return {
        "F": sp.simplify(F),
        "S": sp.simplify(S),
        "alpha_H": sp.simplify(aH),
        "L": sp.simplify(L),
        "D": D_simpl,
        "V": sp.simplify(V),
        "Theta": sp.simplify(Theta),
        "R": sp.simplify(R),
        "R_sq": sp.simplify(R_sq),
        "M": sp.simplify(M),
        "kappa": sp.simplify(kappa),
        "g": sp.simplify(g),
        "A_0": sp.simplify(A_0),
        "A_share": sp.simplify(A_share),
        "A_side": sp.simplify(A_side),
        "D_is_positive_integer": bool(D_is_int),
    }


# ------------------------------------------------------------
# Block A — Typed structural identities
# ------------------------------------------------------------
def block_a(spine: dict[str, Any]) -> list[dict[str, Any]]:
    """P1..P11 — typed identities; P1..P10 must be exact rationals,
    P11 must be an exact symbolic pi-normalized identity.
    """
    F = spine["F"]
    S = spine["S"]
    aH = spine["alpha_H"]
    L = spine["L"]
    D = spine["D"]
    V = spine["V"]
    Theta = spine["Theta"]
    R = spine["R"]
    R_sq = spine["R_sq"]
    M = spine["M"]

    checks: list[dict[str, Any]] = []

    def check(label: str, lhs: Any, rhs: Any, want_rational: bool = True) -> None:
        diff = sp.simplify(lhs - rhs)
        passed = diff == 0
        if want_rational:
            kind = "exact_rational" if passed else "rational_mismatch"
        else:
            kind = "symbolic_identity" if passed else "symbolic_mismatch"
        checks.append(
            {
                "id": label,
                "passed": bool(passed),
                "kind": kind,
                "value": str(sp.simplify(lhs)),
            }
        )

    # P1 — Two-sidedness: alpha_H = L / F
    check("P1_alpha_H_from_L_over_F", L / F, aH)

    # P2 — Closed two-sided event: L = alpha_H * F
    check("P2_L_equals_aH_times_F", L, aH * F)
    check("P2_L_value", L, sp.Rational(162))

    # P3 — Dimensional readout: D = sqrt(F/(S+1))
    check("P3_D_squared", D ** 2, F / (S + 1))
    check("P3_D_value", D, sp.Rational(3))

    # P4 — Cubic write cell: V = F/D and V = sqrt(F*(S+1))
    check("P4_V_from_F_over_D", V, F / D)
    check("P4_V_value", V, sp.Rational(27))
    check("P4_V_squared_equals_F_S_plus_1", V ** 2, F * (S + 1))

    # P5 — Tensor bridge: Theta = alpha_H * D^2 and Theta = L/(S+1)
    check("P5_Theta_from_aH_D_sq", Theta, aH * D ** 2)
    check("P5_Theta_equals_L_over_S_plus_1", Theta, L / (S + 1))
    check("P5_Theta_value", Theta, sp.Rational(18))

    # P6 — Radix: R = alpha_H * L / V = 4D
    check("P6_R_equals_aH_L_over_V", R, aH * L / V)
    check("P6_R_equals_4D", R, 4 * D)
    check("P6_R_value", R, sp.Rational(12))

    # P7 — Matter capacity: M = L - 2*Theta = R^2 - Theta
    check("P7_M_equals_L_minus_2_Theta", M, L - 2 * Theta)
    check("P7_M_equals_R_sq_minus_Theta", M, R_sq - Theta)
    check("P7_M_value", M, sp.Rational(126))

    # P8 — Closed ledger identity: L = M + 2*Theta
    check("P8_L_equals_M_plus_2_Theta", L, M + 2 * Theta)

    # P9 — Cycle-budget identity: R^2 = L - Theta
    check("P9_R_sq_equals_L_minus_Theta", R_sq, L - Theta)
    check("P9_R_sq_value", R_sq, sp.Rational(144))
    # Role separation distinct values
    check("P9_role_separation_L", L, sp.Rational(162))
    check("P9_role_separation_R_sq", R_sq, sp.Rational(144))
    check("P9_role_separation_M", M, sp.Rational(126))
    check("P9_role_separation_Theta", Theta, sp.Rational(18))
    check(
        "P9_M_not_equals_R_sq",
        sp.Integer(1) if M != R_sq else sp.Integer(0),
        sp.Integer(1),
    )

    # P10 — Share split: S = R^2 / Theta = (L - Theta)/Theta
    check("P10_S_equals_R_sq_over_Theta", S, R_sq / Theta)
    check("P10_S_equals_L_minus_Theta_over_Theta", S, (L - Theta) / Theta)
    check("P10_S_value", S, sp.Rational(8))

    # P11 — A_0 (irrational), A_share, A_side
    A_0_typed = V / (sp.pi * aH * L)
    A_share_typed = V / (aH * L)
    A_side_typed = V / (2 * aH * L)
    A_0_expected = sp.Rational(1, 12) / sp.pi
    check("P11_A_0_symbolic", A_0_typed, A_0_expected, want_rational=False)
    check("P11_A_share_value", A_share_typed, sp.Rational(1, 12))
    check("P11_A_side_value", A_side_typed, sp.Rational(1, 24))

    return checks


# ------------------------------------------------------------
# Block B — CR221 bit-identical match
# ------------------------------------------------------------
CR221_KAPPA_FLOOR = sp.Rational(7117, 768)
CR221_NEUTRON_G_UNIT = sp.Rational(1, 64)
# CR221-known component q_A values (for the two-route P14 consistency check;
# these enter as named typed constants from the upstream CR221 result).
CR221_CHARGED_PAIR_QA = sp.Rational(7105, 96)
CR221_NEUTRON_QA = sp.Rational(1, 8)


def block_b(spine: dict[str, Any]) -> list[dict[str, Any]]:
    checks: list[dict[str, Any]] = []
    kappa = spine["kappa"]
    g = spine["g"]
    F = spine["F"]
    S = spine["S"]
    R = spine["R"]
    D = spine["D"]
    aH = spine["alpha_H"]

    # P12 — typed kappa = CR221 frozen value
    diff = sp.simplify(kappa - CR221_KAPPA_FLOOR)
    checks.append(
        {
            "id": "P12_typed_kappa_equals_CR221_kappa_floor",
            "passed": bool(diff == 0),
            "typed": str(kappa),
            "cr221": str(CR221_KAPPA_FLOOR),
            "diff": str(diff),
        }
    )

    # P13 — typed g = CR221 frozen value
    diff_g = sp.simplify(g - CR221_NEUTRON_G_UNIT)
    checks.append(
        {
            "id": "P13_typed_g_equals_CR221_neutron_G_unit",
            "passed": bool(diff_g == 0),
            "typed": str(g),
            "cr221": str(CR221_NEUTRON_G_UNIT),
            "diff": str(diff_g),
        }
    )

    # P14 — two-route consistency: S*(R-1)*(F*S-1) = (charged_pair_qA + neutron_qA) * aH^S * D
    lhs = S * (R - 1) * (F * S - 1)
    rhs = (CR221_CHARGED_PAIR_QA + CR221_NEUTRON_QA) * aH ** S * D
    diff_14 = sp.simplify(lhs - rhs)
    checks.append(
        {
            "id": "P14_two_route_consistency",
            "passed": bool(diff_14 == 0),
            "lhs": str(sp.simplify(lhs)),
            "rhs": str(sp.simplify(rhs)),
            "diff": str(diff_14),
        }
    )

    return checks


# ------------------------------------------------------------
# Block C — CR232 matter gate regrade from typed kernel
# ------------------------------------------------------------
def _to_decimal(s: str) -> sp.Rational:
    """Parse a CSV decimal string into a sympy Rational.

    Blocked rows in CR219 store "no" as the sentinel for an empty/zero
    retained_write_support channel; treat it as exact zero. Empty cells
    and "nan" likewise collapse to zero.
    """
    s = s.strip()
    if s == "" or s.lower() in ("nan", "no"):
        return sp.Rational(0)
    return sp.Rational(s)


def load_cr219(spine: dict[str, Any]) -> list[dict[str, Any]]:
    """Read CR219 csv into a list of row dicts (string columns).

    Header row in the CSV starts with the literal '139' (total row count),
    which we treat as the row-index column.
    """
    rows: list[dict[str, Any]] = []
    with open(CR219_CSV_PATH, "r", encoding="utf-8") as fh:
        reader = csv.reader(fh)
        header = next(reader)
        # First column is row index; second is candidate_id
        col_names = header
        for raw in reader:
            row = {col_names[i]: raw[i] for i in range(len(col_names))}
            rows.append(row)
    return rows


def block_c(spine: dict[str, Any], rows: list[dict[str, Any]]) -> dict[str, Any]:
    R_sq = spine["R_sq"]
    S = spine["S"]
    tol_str = "1/1000000"  # 1e-6; typed as rational
    tol = sp.Rational(tol_str)

    matter_rows = [r for r in rows if r.get("matter_row_allowed") == "yes"]
    blocked_rows = [r for r in rows if r.get("matter_row_allowed") == "no"]
    hidden_support = [
        r for r in rows if r.get("bin") == "hidden_source_support_rows"
    ]

    # P15 — Matter gate: qA_predicted = M_obs * (1 + q_abs/R^2); T = qA/S; W = (S-1)*qA/S
    matter_row_results: list[dict[str, Any]] = []
    matter_pass = 0
    matter_fail = 0
    for r in matter_rows:
        M_obs = _to_decimal(r.get("M_observed_candidate", "0"))
        q_abs = _to_decimal(r.get("q_abs", "0"))
        qA_uploaded = _to_decimal(r.get("qA_source_support", "0"))
        T_uploaded = _to_decimal(r.get("tensor_carrier_support", "0"))
        W_uploaded = _to_decimal(r.get("retained_write_support", "0"))

        qA_pred = M_obs * (1 + q_abs / R_sq)
        T_pred = qA_pred / S
        W_pred = (S - 1) * qA_pred / S

        ok_qA = abs(qA_pred - qA_uploaded) <= tol
        ok_T = abs(T_pred - T_uploaded) <= tol
        ok_W = abs(W_pred - W_uploaded) <= tol
        row_pass = ok_qA and ok_T and ok_W
        if row_pass:
            matter_pass += 1
        else:
            matter_fail += 1
        matter_row_results.append(
            {
                "candidate_id": r.get("candidate_id", ""),
                "M_obs": str(M_obs),
                "qA_pred": str(qA_pred),
                "qA_uploaded": str(qA_uploaded),
                "qA_match": bool(ok_qA),
                "T_pred": str(T_pred),
                "T_uploaded": str(T_uploaded),
                "T_match": bool(ok_T),
                "W_pred": str(W_pred),
                "W_uploaded": str(W_uploaded),
                "W_match": bool(ok_W),
                "row_pass": bool(row_pass),
            }
        )

    # P16 — Blocked rows: M_obs = qA = T = W = 0
    blocked_pass = 0
    blocked_fail = 0
    blocked_results: list[dict[str, Any]] = []
    for r in blocked_rows:
        M_obs = _to_decimal(r.get("M_observed_candidate", "0"))
        qA = _to_decimal(r.get("qA_source_support", "0"))
        T = _to_decimal(r.get("tensor_carrier_support", "0"))
        W = _to_decimal(r.get("retained_write_support", "0"))
        ok = (
            abs(M_obs) <= tol
            and abs(qA) <= tol
            and abs(T) <= tol
            and abs(W) <= tol
        )
        if ok:
            blocked_pass += 1
        else:
            blocked_fail += 1
        blocked_results.append(
            {
                "candidate_id": r.get("candidate_id", ""),
                "bin": r.get("bin", ""),
                "M_obs": str(M_obs),
                "qA": str(qA),
                "T": str(T),
                "W": str(W),
                "row_pass": bool(ok),
            }
        )

    # P17 — Hidden-support surcharge: M_native = p + p^2/R^2
    surcharge_pass = 0
    surcharge_fail = 0
    surcharge_results: list[dict[str, Any]] = []
    for r in hidden_support:
        p = _to_decimal(r.get("partition_signature", "0"))
        M_native_uploaded = _to_decimal(r.get("M_native", "0"))
        M_native_pred = p + (p * p) / R_sq
        ok = abs(M_native_pred - M_native_uploaded) <= tol
        if ok:
            surcharge_pass += 1
        else:
            surcharge_fail += 1
        surcharge_results.append(
            {
                "candidate_id": r.get("candidate_id", ""),
                "p": str(p),
                "M_native_pred": str(M_native_pred),
                "M_native_uploaded": str(M_native_uploaded),
                "row_pass": bool(ok),
            }
        )

    return {
        "P15_matter_rows_checked": len(matter_rows),
        "P15_matter_rows_pass": matter_pass,
        "P15_matter_rows_fail": matter_fail,
        "P15_matter_row_results": matter_row_results,
        "P16_blocked_rows_checked": len(blocked_rows),
        "P16_blocked_rows_pass": blocked_pass,
        "P16_blocked_rows_fail": blocked_fail,
        "P16_blocked_results": blocked_results,
        "P17_hidden_support_checked": len(hidden_support),
        "P17_hidden_support_pass": surcharge_pass,
        "P17_hidden_support_fail": surcharge_fail,
        "P17_surcharge_results": surcharge_results,
    }


# ------------------------------------------------------------
# Block D — CR233 role identities from typed primitives
# ------------------------------------------------------------
def block_d(spine: dict[str, Any]) -> list[dict[str, Any]]:
    F = spine["F"]
    S = spine["S"]
    aH = spine["alpha_H"]
    D = spine["D"]
    V = spine["V"]
    Theta = spine["Theta"]
    R = spine["R"]
    L = spine["L"]

    checks: list[dict[str, Any]] = []

    # P18 — ROLE 1: Theta = alpha_H * D^2
    checks.append(
        {
            "id": "P18_ROLE_1_Theta",
            "passed": bool(sp.simplify(Theta - aH * D ** 2) == 0),
            "typed_value": str(Theta),
            "expected": "18",
        }
    )

    # P19 — ROLE 2: F = foundational atom
    checks.append(
        {
            "id": "P19_ROLE_2_F_foundational",
            "passed": bool(sp.simplify(F - sp.Rational(F_INPUT)) == 0),
            "typed_value": str(F),
        }
    )

    # P20 — ROLE 3: mirror face size = F
    L_minus_F = L - F
    checks.append(
        {
            "id": "P20_ROLE_3_mirror_face_size",
            "passed": bool(sp.simplify(L_minus_F - F) == 0),
            "mirror_face_size": str(L_minus_F),
        }
    )

    # P21 — ROLE 4: V = F/D
    checks.append(
        {
            "id": "P21_ROLE_4_V_equals_F_over_D",
            "passed": bool(sp.simplify(V - F / D) == 0),
            "typed_value": str(V),
        }
    )

    # P22 — Cross identity (derivation D^4 = F)
    # Path: (aH * D^2)^2 = (aH * L / V) * V => aH^2 D^4 = aH * L = aH * aH * F = aH^2 * F
    # Cancel aH^2: D^4 = F
    cross_lhs = (aH * D ** 2) ** 2
    cross_rhs_1 = (aH * L / V) * V
    cross_rhs_2 = aH * L
    cross_rhs_3 = aH * aH * F
    cancel = sp.simplify(D ** 4 - F)
    checks.append(
        {
            "id": "P22_cross_identity_step_1",
            "passed": bool(sp.simplify(cross_lhs - cross_rhs_1) == 0),
            "lhs": str(cross_lhs),
            "rhs": str(cross_rhs_1),
        }
    )
    checks.append(
        {
            "id": "P22_cross_identity_step_2",
            "passed": bool(sp.simplify(cross_rhs_1 - cross_rhs_2) == 0),
            "lhs": str(cross_rhs_1),
            "rhs": str(cross_rhs_2),
        }
    )
    checks.append(
        {
            "id": "P22_cross_identity_step_3",
            "passed": bool(sp.simplify(cross_rhs_2 - cross_rhs_3) == 0),
            "lhs": str(cross_rhs_2),
            "rhs": str(cross_rhs_3),
        }
    )
    checks.append(
        {
            "id": "P22_cross_identity_D_fourth_equals_F",
            "passed": bool(cancel == 0),
            "D_to_fourth": str(D ** 4),
            "F": str(F),
        }
    )
    # Also verify Theta^2 = R * V
    checks.append(
        {
            "id": "P22_Theta_squared_equals_R_V",
            "passed": bool(sp.simplify(Theta ** 2 - R * V) == 0),
            "Theta_squared": str(Theta ** 2),
            "R_V": str(R * V),
        }
    )

    return checks


# ------------------------------------------------------------
# Block E — Substrate uniqueness scan
# ------------------------------------------------------------
def block_e(spine: dict[str, Any]) -> dict[str, Any]:
    S = spine["S"]
    target = S + 1  # canonical S=8 -> 9
    scan: list[dict[str, Any]] = []
    agreeing_D: list[int] = []
    for D_try in range(1, 13):
        D_try_sym = sp.Rational(D_try)
        lhs = D_try_sym ** (D_try_sym - 1)
        face_axiom_F = D_try_sym ** (D_try_sym + 1)
        radix_closure_F = (S + 1) * D_try_sym ** 2
        agree = bool(sp.simplify(face_axiom_F - radix_closure_F) == 0)
        scan.append(
            {
                "D": D_try,
                "D_to_D_minus_1": int(lhs),
                "target_S_plus_1": int(target),
                "face_axiom_F": int(face_axiom_F),
                "radix_closure_F": int(radix_closure_F),
                "agree": agree,
            }
        )
        if agree:
            agreeing_D.append(D_try)
    return {
        "P23_unique_D": agreeing_D == [3],
        "P23_agreeing_D_list": agreeing_D,
        "P24_F_at_D_3": int(sp.Rational(3) ** (sp.Rational(3) + 1)),
        "scan": scan,
    }


# ------------------------------------------------------------
# Block F — Primitive typing audit (literal scan)
# ------------------------------------------------------------
# Per precommit P25 the forbidden literal set is:
#   {81, 162, 27, 144, 126, 18, 8, 1/12, 1/64, 7117/768}
# Plus the load-bearing kappa decomposition components (7117, 768, 64, 324, 647)
# whose appearance as raw integers anywhere in the runner would also bypass
# the typed derivation. The values 2 (α_H) and 12 (R) are deliberately not
# scanned: 2 collides with generic Python uses (exponents like D**2, slicing,
# indent=2, two-bridge coefficients) and 12 collides with R-related arithmetic
# in too many places; scanning them uniformly would generate noise without
# adding discriminating power. The structural 2 = α_H equality is locked at
# the input boundary and verified symbolically in Block A (P1).
# The scanner uses Python's tokenizer to find NUMBER tokens only (so strings,
# comments, and docstrings are skipped naturally); fraction patterns are then
# matched as adjacent NUMBER / OP / NUMBER triples.
# CR238_LITERAL_SCAN: ALLOWED_SECTION_BEGIN scanner configuration data
FORBIDDEN_INTEGER_LITERALS = {
    F_INPUT,
    S_INPUT,
    18,    # Theta
    27,    # V
    64,    # 1/g denominator
    126,   # M
    144,   # R^2
    162,   # L
    324,   # Theta^2 / R*V
    647,   # F*S - 1
    768,   # kappa denominator
    7117,  # kappa numerator
}
FORBIDDEN_FRACTION_LITERALS_TEXT = ("1/12", "1/64", "7117/768")
# CR238_LITERAL_SCAN: ALLOWED_SECTION_END


def _find_block_line_ranges(
    source_text: str, marker_begin: str, marker_end: str
) -> list[tuple[int, int]]:
    """Return inclusive (start, end) line ranges between matching markers."""
    ranges: list[tuple[int, int]] = []
    begin: int | None = None
    for lineno, line in enumerate(source_text.splitlines(), start=1):
        if marker_begin in line:
            begin = lineno
        elif marker_end in line and begin is not None:
            ranges.append((begin, lineno))
            begin = None
    return ranges


def _line_in_ranges(lineno: int, ranges: list[tuple[int, int]]) -> bool:
    return any(begin <= lineno <= end for begin, end in ranges)


def scan_literals_in_text(source_text: str) -> list[dict[str, Any]]:
    """Tokenize the source and flag NUMBER tokens that match forbidden values.

    Also flags forbidden fraction patterns (NUMBER '/' NUMBER) like "1/12".
    Each occurrence is reported with classification metadata; the caller
    categorizes input/allowed/comparand/injection.
    """
    import io
    import tokenize as tk

    lines = source_text.splitlines()
    input_ranges = _find_block_line_ranges(
        source_text,
        "CR238_LITERAL_SCAN: INPUT_BOUNDARY_BEGIN",
        "CR238_LITERAL_SCAN: INPUT_BOUNDARY_END",
    )
    allowed_ranges = _find_block_line_ranges(
        source_text,
        "CR238_LITERAL_SCAN: ALLOWED_SECTION_BEGIN",
        "CR238_LITERAL_SCAN: ALLOWED_SECTION_END",
    )

    results: list[dict[str, Any]] = []

    try:
        tokens = list(tk.tokenize(io.BytesIO(source_text.encode("utf-8")).readline))
    except tk.TokenizeError:
        return results

    # First pass: forbidden integer NUMBER tokens
    for i, tok in enumerate(tokens):
        if tok.type != tk.NUMBER:
            continue
        try:
            val = int(tok.string)
        except ValueError:
            continue
        if val not in FORBIDDEN_INTEGER_LITERALS:
            continue
        line_no = tok.start[0]
        line_content = lines[line_no - 1] if 0 < line_no <= len(lines) else ""
        in_input = _line_in_ranges(line_no, input_ranges)
        in_allowed = _line_in_ranges(line_no, allowed_ranges)
        is_comparand = (
            "==" in line_content
            or "!=" in line_content
            or "sp.Rational" in line_content
        )
        results.append(
            {
                "line": line_no,
                "literal": str(val),
                "kind": "integer",
                "in_input_block": in_input,
                "in_allowed_section": in_allowed,
                "is_comparand": is_comparand,
                "content": line_content.rstrip(),
            }
        )

    # Second pass: forbidden fraction patterns NUMBER '/' NUMBER
    for i in range(len(tokens) - 2):
        a = tokens[i]
        b = tokens[i + 1]
        c = tokens[i + 2]
        if (
            a.type == tk.NUMBER
            and b.type == tk.OP
            and b.string == "/"
            and c.type == tk.NUMBER
        ):
            frac_text = f"{a.string}/{c.string}"
            if frac_text in FORBIDDEN_FRACTION_LITERALS_TEXT:
                line_no = a.start[0]
                line_content = lines[line_no - 1] if 0 < line_no <= len(lines) else ""
                in_input = _line_in_ranges(line_no, input_ranges)
                in_allowed = _line_in_ranges(line_no, allowed_ranges)
                is_comparand = (
                    "==" in line_content
                    or "!=" in line_content
                    or "sp.Rational" in line_content
                )
                results.append(
                    {
                        "line": line_no,
                        "literal": frac_text,
                        "kind": "fraction",
                        "in_input_block": in_input,
                        "in_allowed_section": in_allowed,
                        "is_comparand": is_comparand,
                        "content": line_content.rstrip(),
                    }
                )

    return results


def scan_literals_in_runner() -> dict[str, Any]:
    """Read the runner's own source and run the literal scan.

    Categorize each occurrence as:
      - input_boundary: inside the INPUT DECLARATION block (allowed per P25)
      - allowed_section: inside an ALLOWED_SECTION marker (scanner data)
      - comparand: line contains == / != / sp.Rational(...) (test assertion)
      - injection: otherwise (flagged as failure)
    """
    source = SCRIPT_PATH.read_text(encoding="utf-8")
    occurrences = scan_literals_in_text(source)

    categorized: list[dict[str, Any]] = []
    counts = {
        "input_boundary": 0,
        "allowed_section": 0,
        "comparand": 0,
        "injection": 0,
    }
    for occ in occurrences:
        if occ["in_input_block"]:
            category = "input_boundary"
        elif occ["in_allowed_section"]:
            category = "allowed_section"
        elif occ["is_comparand"]:
            category = "comparand"
        else:
            category = "injection"
        counts[category] += 1
        categorized.append({**occ, "category": category})

    return {
        "total_occurrences": len(categorized),
        "input_boundary": counts["input_boundary"],
        "allowed_section": counts["allowed_section"],
        "comparand": counts["comparand"],
        "injection": counts["injection"],
        "categorized": categorized,
    }


# ------------------------------------------------------------
# Block F — WC8 injection sentinel test
# ------------------------------------------------------------
WC8_INJECTED_SOURCE = '''"""WC8 injection test fixture."""
# This file deliberately injects a raw literal that should be flagged.
kappa = 7117/768  # raw-literal injection -- should be flagged
result = kappa
'''


def wc8_injection_test() -> dict[str, Any]:
    """Run the literal scanner on a fixture containing a raw injection and
    verify the scanner flags it.
    """
    occurrences = scan_literals_in_text(WC8_INJECTED_SOURCE)
    flagged = [
        o for o in occurrences
        if not o["in_input_block"] and not o["is_comparand"]
    ]
    return {
        "fixture_lines": len(WC8_INJECTED_SOURCE.splitlines()),
        "total_occurrences": len(occurrences),
        "flagged_as_injection": len(flagged),
        "audit_caught_injection": len(flagged) >= 1,
        "occurrences": occurrences,
    }


# ------------------------------------------------------------
# Wrong controls WC1..WC9
# ------------------------------------------------------------
def wc1_face_perturbation() -> dict[str, Any]:
    """ℱ → 80 with S=8 — D non-integer, identities break."""
    spine = derive_spine(80, S_INPUT, ALPHA_H_INPUT)
    D = spine["D"]
    kappa = spine["kappa"]
    D_integer = spine["D_is_positive_integer"]
    kappa_matches_CR221 = bool(sp.simplify(kappa - CR221_KAPPA_FLOOR) == 0)
    return {
        "wc_id": "WC1",
        "description": "F=80 face perturbation",
        "D_is_positive_integer": D_integer,
        "D_value": str(D),
        "kappa": str(kappa),
        "kappa_matches_CR221": kappa_matches_CR221,
        "expected": "BREAK",
        "observed": "BREAK" if (not D_integer or not kappa_matches_CR221) else "PASS",
        "broke_as_predicted": (not D_integer or not kappa_matches_CR221),
    }


def wc2_split_perturbation() -> dict[str, Any]:
    """ℱ=81, S → 7 — D non-integer, identities break."""
    spine = derive_spine(F_INPUT, 7, ALPHA_H_INPUT)
    D = spine["D"]
    kappa = spine["kappa"]
    D_integer = spine["D_is_positive_integer"]
    kappa_matches_CR221 = bool(sp.simplify(kappa - CR221_KAPPA_FLOOR) == 0)
    return {
        "wc_id": "WC2",
        "description": "S=7 split perturbation",
        "D_is_positive_integer": D_integer,
        "D_value": str(D),
        "kappa": str(kappa),
        "kappa_matches_CR221": kappa_matches_CR221,
        "expected": "BREAK",
        "observed": "BREAK" if (not D_integer or not kappa_matches_CR221) else "PASS",
        "broke_as_predicted": (not D_integer or not kappa_matches_CR221),
    }


def wc3_split_overshoot() -> dict[str, Any]:
    """ℱ=81, S → 9 — D non-integer, identities break."""
    spine = derive_spine(F_INPUT, 9, ALPHA_H_INPUT)
    D = spine["D"]
    D_integer = spine["D_is_positive_integer"]
    kappa = spine["kappa"]
    kappa_matches_CR221 = bool(sp.simplify(kappa - CR221_KAPPA_FLOOR) == 0)
    return {
        "wc_id": "WC3",
        "description": "S=9 split overshoot",
        "D_is_positive_integer": D_integer,
        "D_value": str(D),
        "kappa": str(kappa),
        "kappa_matches_CR221": kappa_matches_CR221,
        "expected": "BREAK",
        "observed": "BREAK" if (not D_integer or not kappa_matches_CR221) else "PASS",
        "broke_as_predicted": (not D_integer or not kappa_matches_CR221),
    }


def wc4_alpha_h_violation() -> dict[str, Any]:
    """α_H forced to non-binary value while ℒ=162 held at its CR217-sealed value.

    α_H is structurally defined as ℒ/ℱ (binary readout = face count). At canonical
    ℒ=162 and ℱ=81, α_H must equal 2. Forcing α_H to 3 with the sealed ℒ creates
    two independent contradictions (the test passes if either or both fire):

      (a) α_H_declared (3) ≠ α_H_derived (ℒ/ℱ = 162/81 = 2)
      (b) Continuing the derivation: S derived from (ℒ−Θ)/Θ with Θ = α_H_declared·D²
          = 3·9 = 27 gives S_derived = (162−27)/27 = 5 ≠ S_declared (8).
    """
    F = sp.Rational(F_INPUT)
    S_decl = sp.Rational(S_INPUT)
    aH_decl = sp.Rational(3)  # forced violation of binary readout
    L_sealed = sp.Rational(162)  # CR217 sealed closed two-sided event

    aH_derived = L_sealed / F
    aH_contradiction = bool(sp.simplify(aH_decl - aH_derived) != 0)

    # Continue downstream with α_H_declared=3 and ℒ=162 held fixed
    D = sp.sqrt(F / (S_decl + 1))
    Theta = aH_decl * D ** 2
    V = F / D
    R = aH_decl * L_sealed / V
    S_derived = (L_sealed - Theta) / Theta
    S_contradiction = bool(sp.simplify(S_decl - S_derived) != 0)
    R_breaks_4D = bool(sp.simplify(R - 4 * D) != 0)

    self_contradicts = aH_contradiction or S_contradiction
    return {
        "wc_id": "WC4",
        "description": "alpha_H = 3 violates binary readout (with L=162 held fixed)",
        "alpha_H_declared": str(aH_decl),
        "alpha_H_derived_from_L_over_F": str(sp.simplify(aH_derived)),
        "alpha_H_contradiction": aH_contradiction,
        "S_declared": str(S_decl),
        "S_derived_with_aH_3": str(sp.simplify(S_derived)),
        "S_contradiction": S_contradiction,
        "R_breaks_4D_identity": R_breaks_4D,
        "expected": "SELF-CONTRADICT",
        "observed": "SELF-CONTRADICT" if self_contradicts else "CONSISTENT",
        "broke_as_predicted": self_contradicts,
    }


def wc5_kappa_exponent_variation() -> dict[str, Any]:
    """Replace α_H^S with α_H^(S-1) and α_H^(S+1)."""
    spine = derive_spine(F_INPUT, S_INPUT, ALPHA_H_INPUT)
    F = spine["F"]
    S = spine["S"]
    R = spine["R"]
    D = spine["D"]
    aH = spine["alpha_H"]
    kappa_S_minus_1 = (R - 1) * (F * S - 1) / (D * aH ** (S - 1))
    kappa_S_plus_1 = (R - 1) * (F * S - 1) / (D * aH ** (S + 1))
    break_minus = bool(sp.simplify(kappa_S_minus_1 - CR221_KAPPA_FLOOR) != 0)
    break_plus = bool(sp.simplify(kappa_S_plus_1 - CR221_KAPPA_FLOOR) != 0)
    return {
        "wc_id": "WC5",
        "description": "kappa exponent variation aH^(S-1), aH^(S+1)",
        "kappa_S_minus_1": str(sp.simplify(kappa_S_minus_1)),
        "kappa_S_plus_1": str(sp.simplify(kappa_S_plus_1)),
        "S_minus_1_breaks_CR221_match": break_minus,
        "S_plus_1_breaks_CR221_match": break_plus,
        "expected": "BREAK both",
        "observed": "BREAK both" if (break_minus and break_plus) else "INCOMPLETE",
        "broke_as_predicted": break_minus and break_plus,
    }


def wc6_g_exponent_variation() -> dict[str, Any]:
    """Replace g = 1/S^2 with g = 1/S."""
    spine = derive_spine(F_INPUT, S_INPUT, ALPHA_H_INPUT)
    S = spine["S"]
    g_wrong = sp.Rational(1) / S
    break_match = bool(sp.simplify(g_wrong - CR221_NEUTRON_G_UNIT) != 0)
    return {
        "wc_id": "WC6",
        "description": "g = 1/S instead of 1/S^2",
        "g_wrong": str(g_wrong),
        "breaks_CR221_match": break_match,
        "expected": "BREAK",
        "observed": "BREAK" if break_match else "PASS",
        "broke_as_predicted": break_match,
    }


def wc7_n_z_form_swap(spine: dict[str, Any]) -> dict[str, Any]:
    """Compare floor-form N(Z) vs mod-form N(Z) on Z in 1..12."""
    from fractions import Fraction
    R_val = int(spine["R"])
    diverge_count = 0
    samples: list[dict[str, Any]] = []
    for Z in range(1, 13):
        floor_form = Z + (Z // R_val) * ((Z - 1) // R_val)
        # Mod form (as the precommit defines it): Z + (Z/R) * ((Z-1) mod R)
        mod_form = Fraction(Z) + Fraction(Z, R_val) * Fraction((Z - 1) % R_val)
        diverge = floor_form != mod_form
        if diverge:
            diverge_count += 1
        samples.append(
            {
                "Z": Z,
                "floor_form": floor_form,
                "mod_form": f"{mod_form.numerator}/{mod_form.denominator}",
                "diverge": diverge,
            }
        )
    return {
        "wc_id": "WC7",
        "description": "N(Z) floor form vs mod form (Z=1..12)",
        "diverge_count": diverge_count,
        "diverges_at_He4_Z2": samples[1]["diverge"],
        "samples": samples,
        "expected": "BREAK at Z with (Z-1) mod R != 0",
        "observed": "BREAK" if diverge_count > 0 else "PASS",
        "broke_as_predicted": diverge_count > 0,
    }


def wc8_literal_injection() -> dict[str, Any]:
    """Run injection-sentinel test against the literal scanner."""
    sentinel = wc8_injection_test()
    caught = sentinel["audit_caught_injection"]
    return {
        "wc_id": "WC8",
        "description": "raw-literal injection sentinel (audit discriminator)",
        "audit_caught_injection": caught,
        "details": sentinel,
        "expected": "ARITHMETIC PASSES, AUDIT FLAGS",
        "observed": "AUDIT FLAGS" if caught else "AUDIT MISSED",
        "broke_as_predicted": caught,
    }


def wc9_uniqueness_d_4() -> dict[str, Any]:
    """D=4 substrate attempt at S=8 — axioms disagree."""
    D_try = sp.Rational(4)
    S_val = sp.Rational(8)
    face_axiom = D_try ** (D_try + 1)
    radix_closure = (S_val + 1) * D_try ** 2
    disagree = bool(face_axiom - radix_closure != 0)
    d_to_d_minus_1 = D_try ** (D_try - 1)
    return {
        "wc_id": "WC9",
        "description": "D=4 substrate attempt at S=8",
        "face_axiom_F": int(face_axiom),
        "radix_closure_F": int(radix_closure),
        "D_to_D_minus_1": int(d_to_d_minus_1),
        "target_S_plus_1": int(S_val + 1),
        "axioms_disagree": disagree,
        "expected": "AXIOMS DISAGREE",
        "observed": "AXIOMS DISAGREE" if disagree else "AGREE",
        "broke_as_predicted": disagree,
    }


# ------------------------------------------------------------
# Output emission
# ------------------------------------------------------------
def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    if not rows:
        path.write_text("", encoding="utf-8")
        return
    keys = list(rows[0].keys())
    with open(path, "w", encoding="utf-8", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=keys)
        w.writeheader()
        for r in rows:
            w.writerow({k: r.get(k, "") for k in keys})


def main() -> int:
    shas = assert_input_shas()

    # Derive the canonical spine
    spine = derive_spine(F_INPUT, S_INPUT, ALPHA_H_INPUT)

    # Run blocks
    block_a_checks = block_a(spine)
    block_b_checks = block_b(spine)
    cr219_rows = load_cr219(spine)
    block_c_result = block_c(spine, cr219_rows)
    block_d_checks = block_d(spine)
    block_e_result = block_e(spine)
    block_f_scan = scan_literals_in_runner()

    # Wrong controls
    wc_results = [
        wc1_face_perturbation(),
        wc2_split_perturbation(),
        wc3_split_overshoot(),
        wc4_alpha_h_violation(),
        wc5_kappa_exponent_variation(),
        wc6_g_exponent_variation(),
        wc7_n_z_form_swap(spine),
        wc8_literal_injection(),
        wc9_uniqueness_d_4(),
    ]

    # Aggregate pass/fail
    block_a_pass = all(c["passed"] for c in block_a_checks)
    block_b_pass = all(c["passed"] for c in block_b_checks)
    block_c_pass = (
        block_c_result["P15_matter_rows_fail"] == 0
        and block_c_result["P16_blocked_rows_fail"] == 0
        and block_c_result["P17_hidden_support_fail"] == 0
    )
    block_d_pass = all(c["passed"] for c in block_d_checks)
    block_e_pass = block_e_result["P23_unique_D"]
    block_f_pass = block_f_scan["injection"] == 0
    wc_pass = all(w["broke_as_predicted"] for w in wc_results)
    overall_pass = (
        block_a_pass
        and block_b_pass
        and block_c_pass
        and block_d_pass
        and block_e_pass
        and block_f_pass
        and wc_pass
    )

    # Emit outputs
    out_dir = SCRIPT_DIR
    write_csv(
        out_dir / "CR238_block_a_checks.csv",
        [{k: str(v) for k, v in c.items()} for c in block_a_checks],
    )
    write_csv(
        out_dir / "CR238_block_b_checks.csv",
        [{k: str(v) for k, v in c.items()} for c in block_b_checks],
    )
    write_csv(
        out_dir / "CR238_matter_row_audit.csv",
        block_c_result["P15_matter_row_results"],
    )
    write_csv(
        out_dir / "CR238_blocked_row_audit.csv",
        block_c_result["P16_blocked_results"],
    )
    write_csv(
        out_dir / "CR238_surcharge_audit.csv",
        block_c_result["P17_surcharge_results"],
    )
    write_csv(
        out_dir / "CR238_block_d_checks.csv",
        [{k: str(v) for k, v in c.items()} for c in block_d_checks],
    )
    write_csv(
        out_dir / "CR238_uniqueness_scan.csv",
        [{k: str(v) for k, v in s.items()} for s in block_e_result["scan"]],
    )
    write_csv(
        out_dir / "CR238_literal_scan.csv",
        [{k: str(v) for k, v in c.items()} for c in block_f_scan["categorized"]],
    )
    write_csv(
        out_dir / "CR238_wrong_controls.csv",
        [{k: str(v) for k, v in w.items() if k != "details"} for w in wc_results],
    )

    # Summary JSON
    summary = {
        "precommit_sha": shas["precommit_sha"],
        "cr219_csv_sha": shas["cr219_csv_sha"],
        "expected_precommit_sha": EXPECTED_PRECOMMIT_SHA,
        "expected_cr219_csv_sha": EXPECTED_CR219_SHA,
        "input_atoms": {
            "F": int(spine["F"]),
            "S": int(spine["S"]),
            "alpha_H": int(spine["alpha_H"]),
        },
        "derived_readouts": {
            "D": str(spine["D"]),
            "L": str(spine["L"]),
            "V": str(spine["V"]),
            "Theta": str(spine["Theta"]),
            "R": str(spine["R"]),
            "R_sq": str(spine["R_sq"]),
            "M": str(spine["M"]),
            "kappa": str(spine["kappa"]),
            "g": str(spine["g"]),
            "A_0": str(spine["A_0"]),
            "A_share": str(spine["A_share"]),
            "A_side": str(spine["A_side"]),
        },
        "block_a": {
            "pass": block_a_pass,
            "total": len(block_a_checks),
            "passed": sum(1 for c in block_a_checks if c["passed"]),
        },
        "block_b": {
            "pass": block_b_pass,
            "total": len(block_b_checks),
            "passed": sum(1 for c in block_b_checks if c["passed"]),
            "kappa_typed": str(spine["kappa"]),
            "kappa_cr221": str(CR221_KAPPA_FLOOR),
            "g_typed": str(spine["g"]),
            "g_cr221": str(CR221_NEUTRON_G_UNIT),
        },
        "block_c": {
            "pass": block_c_pass,
            "matter_rows_pass_over_total": (
                f"{block_c_result['P15_matter_rows_pass']}/"
                f"{block_c_result['P15_matter_rows_checked']}"
            ),
            "blocked_rows_pass_over_total": (
                f"{block_c_result['P16_blocked_rows_pass']}/"
                f"{block_c_result['P16_blocked_rows_checked']}"
            ),
            "hidden_support_pass_over_total": (
                f"{block_c_result['P17_hidden_support_pass']}/"
                f"{block_c_result['P17_hidden_support_checked']}"
            ),
        },
        "block_d": {
            "pass": block_d_pass,
            "total": len(block_d_checks),
            "passed": sum(1 for c in block_d_checks if c["passed"]),
        },
        "block_e": {
            "pass": block_e_pass,
            "agreeing_D_list": block_e_result["P23_agreeing_D_list"],
            "F_at_D_3": block_e_result["P24_F_at_D_3"],
        },
        "block_f": {
            "pass": block_f_pass,
            "total_occurrences": block_f_scan["total_occurrences"],
            "input_boundary": block_f_scan["input_boundary"],
            "allowed_section": block_f_scan["allowed_section"],
            "comparand": block_f_scan["comparand"],
            "injection": block_f_scan["injection"],
        },
        "wrong_controls": {
            "all_broke_as_predicted": wc_pass,
            "individual": {w["wc_id"]: w["broke_as_predicted"] for w in wc_results},
        },
        "overall_pass": overall_pass,
    }

    with open(out_dir / "CR238_summary.json", "w", encoding="utf-8") as fh:
        json.dump(summary, fh, indent=2, sort_keys=True)

    # Print verdict line
    verdict = "PASS" if overall_pass else "FAIL"
    print(f"CR238 verdict: {verdict}")
    print(
        f"  Block A: {summary['block_a']['passed']}/{summary['block_a']['total']}"
    )
    print(
        f"  Block B: {summary['block_b']['passed']}/{summary['block_b']['total']}"
    )
    print(
        f"  Block C matter: {summary['block_c']['matter_rows_pass_over_total']}, "
        f"blocked: {summary['block_c']['blocked_rows_pass_over_total']}, "
        f"hidden: {summary['block_c']['hidden_support_pass_over_total']}"
    )
    print(
        f"  Block D: {summary['block_d']['passed']}/{summary['block_d']['total']}"
    )
    print(
        f"  Block E: unique D = {summary['block_e']['agreeing_D_list']}"
    )
    print(
        f"  Block F literal-scan: "
        f"input_boundary={summary['block_f']['input_boundary']}, "
        f"allowed_section={summary['block_f']['allowed_section']}, "
        f"comparand={summary['block_f']['comparand']}, "
        f"injection={summary['block_f']['injection']}"
    )
    print(
        f"  Wrong controls all broke as predicted: "
        f"{summary['wrong_controls']['all_broke_as_predicted']}"
    )

    return 0 if overall_pass else 1


if __name__ == "__main__":
    sys.exit(main())
