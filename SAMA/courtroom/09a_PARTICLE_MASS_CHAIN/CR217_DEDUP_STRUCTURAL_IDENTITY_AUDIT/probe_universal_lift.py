"""
Probe: does m(p) = p +/- p^2/R^2 fire on every row of the CR214 195-row complement?

User hypothesis: it works on every row; rows with positive_debit need the
flipped form m(p) = p - p^2/R^2.

This is an exploration script, not a sealed CR. It tries every reasonable
encoding of p against every reasonable target column, both signs, and
reports the hit rate per encoding. Tolerance set to 1e-10.
"""
from __future__ import annotations

import csv
from collections import Counter
from decimal import Decimal, getcontext
from fractions import Fraction
from pathlib import Path


getcontext().prec = 60

ROOT = Path(__file__).resolve().parents[2]
INPUT = (
    ROOT / "09a_PARTICLE_MASS_CHAIN"
    / "CR214_CR119_PARTICLE_COMPLEMENT_PATTERN_AUDIT"
    / "CR214_particle_complement_195.csv"
)

R = 12
R2 = R * R  # 144
EPS = Decimal("1e-10")


def to_decimal(s: str) -> Decimal:
    s = s.strip()
    if not s:
        return Decimal(0)
    return Decimal(s)


def parse_partition(s: str) -> list[int]:
    """Parse '1+1+2' into [1,1,2]. Single integers like '8' into [8]."""
    s = s.strip()
    if not s:
        return []
    try:
        return [int(part.strip()) for part in s.split("+")]
    except ValueError:
        return []


def expected_lift(p: int, sign: str) -> Decimal:
    """Return p + p^2/144 or p - p^2/144 as exact Decimal."""
    p_dec = Decimal(p)
    lift = Decimal(p * p) / Decimal(R2)
    return p_dec + lift if sign == "+" else p_dec - lift


def candidate_p_values(partition_components: list[int]) -> dict[str, int]:
    if not partition_components:
        return {}
    p_sum = sum(partition_components)
    p_prod = 1
    for x in partition_components:
        p_prod *= x
    p_max = max(partition_components)
    p_min = min(partition_components)
    out = {
        "sum": p_sum,
        "product": p_prod,
        "max": p_max,
        "min": p_min,
    }
    if len(partition_components) == 1:
        out["single"] = partition_components[0]
    return out


def main() -> None:
    with INPUT.open("r", encoding="utf-8-sig", newline="") as handle:
        rows = list(csv.DictReader(handle))

    print(f"Loaded {len(rows)} rows from CR214 195-row complement.")
    print(f"Testing m(p) = p +/- p^2/R^2 with R^2 = {R2}.")
    print(f"Tolerance: {EPS}.")
    print()

    target_columns = ["M_native", "M_observed_candidate", "S_debit_or_credit"]
    sign_options = ["+", "-"]

    # Per-row hit map: for each row, which (p_encoding, target, sign) combos fire?
    hit_combo_counter: Counter[tuple[str, str, str]] = Counter()
    rows_with_any_hit = 0
    rows_with_zero_hit = []
    per_row_hits: list[list[tuple[str, str, str]]] = []

    # Per-bin tally
    bin_total: Counter[str] = Counter()
    bin_any_hit: Counter[str] = Counter()
    bin_hidden_source_p_plus = 0

    for row in rows:
        bin_name = row.get("bin", "")
        bin_total[bin_name] += 1
        partition_components = parse_partition(row.get("partition_signature", ""))
        p_candidates = candidate_p_values(partition_components)
        if not p_candidates:
            rows_with_zero_hit.append((row.get("candidate_id", ""), bin_name, "no_partition"))
            per_row_hits.append([])
            continue

        target_values = {col: to_decimal(row.get(col, "0")) for col in target_columns}

        this_row_hits = []
        for p_name, p_val in p_candidates.items():
            for sign in sign_options:
                expected = expected_lift(p_val, sign)
                for col_name, target_val in target_values.items():
                    if abs(target_val - expected) < EPS:
                        combo = (p_name, col_name, sign)
                        this_row_hits.append(combo)
                        hit_combo_counter[combo] += 1
        per_row_hits.append(this_row_hits)
        if this_row_hits:
            rows_with_any_hit += 1
            bin_any_hit[bin_name] += 1
        else:
            rows_with_zero_hit.append(
                (
                    row.get("candidate_id", ""),
                    bin_name,
                    f"M_native={row.get('M_native', '')[:30]} | S={row.get('S_debit_or_credit', '')[:30]}",
                )
            )

    print("=" * 78)
    print("HIT MAP -- combinations (p_encoding, target_column, sign) that hit any row")
    print("=" * 78)
    if not hit_combo_counter:
        print("NO COMBINATION OF (p_encoding, target, sign) FIRES ON ANY ROW.")
    else:
        for combo, count in sorted(hit_combo_counter.items(), key=lambda x: -x[1]):
            print(f"  {combo[0]:>10s} -> {combo[1]:>22s}  sign {combo[2]}   hits: {count}/{len(rows)}")
    print()

    print("=" * 78)
    print("PER-BIN COVERAGE -- rows with at least one (encoding, target, sign) hit")
    print("=" * 78)
    for bin_name in sorted(bin_total):
        hit = bin_any_hit.get(bin_name, 0)
        total = bin_total[bin_name]
        print(f"  {bin_name:>34s}: {hit:3d}/{total:3d}  ({100.0*hit/total:.0f}%)")
    print()

    print("=" * 78)
    print(f"OVERALL: {rows_with_any_hit}/{len(rows)} rows have at least one hit")
    print(f"OVERALL: {len(rows_with_zero_hit)}/{len(rows)} rows have ZERO hits")
    print("=" * 78)
    print()

    print("=" * 78)
    print("FIRST 12 ROWS WITH ZERO HITS (sample)")
    print("=" * 78)
    for entry in rows_with_zero_hit[:12]:
        cid, bin_name, detail = entry
        print(f"  {cid}  [{bin_name}]  {detail}")
    print()

    # Bonus: dump a sample of rows from each bin showing what M_native, S, etc. look like
    print("=" * 78)
    print("SAMPLE PER BIN (first row of each bin)")
    print("=" * 78)
    seen = set()
    for row in rows:
        b = row.get("bin", "")
        if b in seen:
            continue
        seen.add(b)
        print(f"  bin={b}")
        print(f"    candidate_id={row.get('candidate_id')}")
        print(f"    partition_signature={row.get('partition_signature')}")
        print(f"    closure_depth={row.get('closure_depth')}")
        print(f"    surface_sign={row.get('surface_sign')}")
        print(f"    M_native={row.get('M_native','')[:40]}")
        print(f"    S_debit_or_credit={row.get('S_debit_or_credit','')[:40]}")
        print(f"    M_observed_candidate={row.get('M_observed_candidate','')[:40]}")
        print()


if __name__ == "__main__":
    main()
