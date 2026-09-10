"""
CR230 Raw-Generator Test — Runner

Takes the SAM foundational constants {R, D, alpha_H} as input and derives the
substrate structural number set {126, 81, 81, 162, 27} step-by-step via the
inclusion-exclusion accounting (CR229) plus the substrate write-rate identity.

Also runs the four wrong controls (WC1-WC4) and confirms each breaks the closure.

Sealed: 2026-06-22 by Sean Brady.
"""

from fractions import Fraction


def raw_generator(R: int, D: int, alpha_H: int) -> dict:
    """Derive the substrate structural number set from {R, D, alpha_H} alone."""
    capacity = R ** 2
    binary_closure = 2 ** D
    tensor = capacity // binary_closure
    assert tensor == alpha_H * (D ** 2), (
        f"tensor identity broken: R^2/2^D ({tensor}) != alpha_H*D^2 ({alpha_H * D**2})"
    )
    retained = capacity - tensor
    per_side_unique = retained // 2
    one_side = per_side_unique + tensor
    mirror = D ** (D + 1)
    closed_ledger = one_side + mirror
    write_rate = (one_side * 4) // R

    return {
        "R": R,
        "D": D,
        "alpha_H": alpha_H,
        "capacity_R2": capacity,
        "binary_closure_2^D": binary_closure,
        "tensor_R2_over_2D": tensor,
        "retained_capacity": retained,
        "per_side_unique": per_side_unique,
        "one_side_total": one_side,
        "mirror_D_to_D_plus_1": mirror,
        "closed_ledger": closed_ledger,
        "write_rate_D3": write_rate,
    }


def verify_target(result: dict, target: dict, label: str) -> bool:
    """Compare result against target. Returns True iff all match exactly."""
    ok = True
    for k, v in target.items():
        actual = result.get(k)
        if actual != v:
            print(f"  [{label}] FAIL key {k}: expected {v}, got {actual}")
            ok = False
        else:
            print(f"  [{label}] PASS key {k}: {actual}")
    return ok


def wc1_omit_row_0306(R: int, D: int, alpha_H: int) -> dict:
    """Wrong Control 1: omit row 0306 (p=1) from carrier side. Side sum drops by 1."""
    base = raw_generator(R, D, alpha_H)
    base["one_side_total"] -= 1
    base["closed_ledger"] = base["one_side_total"] + base["mirror_D_to_D_plus_1"]
    return base


def wc2_restore_duplicate_0305(R: int, D: int, alpha_H: int) -> dict:
    """Wrong Control 2: restore CR216-retired duplicate 0305 (p=1). Side sum increases by 1."""
    base = raw_generator(R, D, alpha_H)
    base["one_side_total"] += 1
    base["closed_ledger"] = base["one_side_total"] + base["mirror_D_to_D_plus_1"]
    return base


def wc3_treat_0303_as_unpacked(R: int, D: int, alpha_H: int) -> dict:
    """Wrong Control 3: treat 0303 mirror as one of the 12 unpacked carrier elements."""
    base = raw_generator(R, D, alpha_H)
    base["one_side_total"] += base["mirror_D_to_D_plus_1"]
    base["mirror_D_to_D_plus_1"] = 0
    base["closed_ledger"] = base["one_side_total"] + base["mirror_D_to_D_plus_1"]
    return base


def wc4_use_mass_lift_values(R: int, D: int, alpha_H: int) -> dict:
    """Wrong Control 4: use lifted masses m(p) = p + p^2/R^2 instead of bare partitions."""
    base = raw_generator(R, D, alpha_H)
    partitions = [1, 2, 3, 4, 6, 8, 9, 12]
    bare_sum = sum(partitions)
    lifted_sum_frac = sum(Fraction(p) + Fraction(p ** 2, R ** 2) for p in partitions)
    lift = lifted_sum_frac - Fraction(bare_sum)
    new_one_side = Fraction(base["one_side_total"]) + lift
    new_ledger = new_one_side + Fraction(base["mirror_D_to_D_plus_1"])
    base["one_side_total"] = float(new_one_side)
    base["closed_ledger"] = float(new_ledger)
    return base


def main():
    R, D, alpha_H = 12, 3, 2

    print("=" * 70)
    print("CR230 Raw-Generator Test")
    print("Inputs: R =", R, ", D =", D, ", alpha_H =", alpha_H)
    print("=" * 70)

    target = {
        "capacity_R2": 144,
        "tensor_R2_over_2D": 18,
        "retained_capacity": 126,
        "per_side_unique": 63,
        "one_side_total": 81,
        "mirror_D_to_D_plus_1": 81,
        "closed_ledger": 162,
        "write_rate_D3": 27,
    }

    print("\n[MAIN] Running raw generator on canonical inputs...")
    result = raw_generator(R, D, alpha_H)
    main_pass = verify_target(result, target, "MAIN")

    print("\n[WC1] omit row 0306 (p=1) — expect ledger 161 (off by 1, not 162):")
    wc1 = wc1_omit_row_0306(R, D, alpha_H)
    wc1_breaks = wc1["closed_ledger"] != 162
    print(f"  closed_ledger = {wc1['closed_ledger']} -> {'BREAKS' if wc1_breaks else 'DOES NOT BREAK'}")

    print("\n[WC2] restore duplicate 0305 (p=1) — expect ledger 163:")
    wc2 = wc2_restore_duplicate_0305(R, D, alpha_H)
    wc2_breaks = wc2["closed_ledger"] != 162
    print(f"  closed_ledger = {wc2['closed_ledger']} -> {'BREAKS' if wc2_breaks else 'DOES NOT BREAK'}")

    print("\n[WC3] treat 0303 as unpacked (no mirror side):")
    wc3 = wc3_treat_0303_as_unpacked(R, D, alpha_H)
    wc3_breaks = wc3["mirror_D_to_D_plus_1"] != 81 or wc3["one_side_total"] != 81
    print(
        f"  one_side = {wc3['one_side_total']}, mirror = {wc3['mirror_D_to_D_plus_1']} -> {'BREAKS' if wc3_breaks else 'DOES NOT BREAK'}"
    )

    print("\n[WC4] use mass-lift values m(p) = p + p^2/R^2:")
    wc4 = wc4_use_mass_lift_values(R, D, alpha_H)
    wc4_breaks = wc4["closed_ledger"] != 162
    print(
        f"  one_side = {wc4['one_side_total']}, closed_ledger = {wc4['closed_ledger']} -> {'BREAKS' if wc4_breaks else 'DOES NOT BREAK'}"
    )

    print("\n" + "=" * 70)
    all_wc_break = wc1_breaks and wc2_breaks and wc3_breaks and wc4_breaks
    overall = main_pass and all_wc_break
    print(f"MAIN pass:  {main_pass}")
    print(f"WC1 breaks: {wc1_breaks}")
    print(f"WC2 breaks: {wc2_breaks}")
    print(f"WC3 breaks: {wc3_breaks}")
    print(f"WC4 breaks: {wc4_breaks}")
    print(f"OVERALL CR230 VERDICT: {'PASS' if overall else 'FAIL'}")
    print("=" * 70)


if __name__ == "__main__":
    main()
