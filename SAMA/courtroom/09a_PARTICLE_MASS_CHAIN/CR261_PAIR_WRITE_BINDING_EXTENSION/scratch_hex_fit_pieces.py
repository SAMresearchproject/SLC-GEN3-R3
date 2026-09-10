"""
Fractured-hexagon fit-pieces test for CR261 binding formula.

For each nucleus (Z, N):
  - Z decomposes into k_Z whole Θ-cells + remainder r_Z = Z mod 18
  - N decomposes into k_N whole Θ-cells + remainder r_N = N mod 18
  - Θ-cells charge 0; remainder charges are Z mod 18 and N mod 18

Add correction terms to CR261 based on (r_Z, r_N) and see if RMS drops
below 5 MeV.
"""

import csv
import math
import os

HERE = os.path.dirname(os.path.abspath(__file__))
FIT_CSV = os.path.join(HERE, "CR261_bw_fit_per_row.csv")

THETA = 18


def load_data():
    rows = []
    with open(FIT_CSV, "r") as f:
        reader = csv.DictReader(f)
        for row in reader:
            Z = int(row["Z"])
            N = int(row["N"])
            A = int(row["A"])
            row.update({
                "Z": Z, "N": N, "A": A,
                "residual_CR261": float(row["residual_MeV"]),
                "r_Z": Z % THETA,       # Z mod Theta
                "r_N": N % THETA,       # N mod Theta
                "k_Z": Z // THETA,      # number of whole Theta cells in Z
                "k_N": N // THETA,      # number of whole Theta cells in N
                "r_A": A % THETA,       # A mod Theta
            })
            rows.append(row)
    return rows


def rms(vals):
    return math.sqrt(sum(v * v for v in vals) / len(vals)) if vals else 0.0


def try_correction(rows, label, correction_fn):
    """Apply correction_fn(row) → MeV correction, report RMS."""
    train_res = []
    test_res = []
    for r in rows:
        correction = correction_fn(r)
        new_residual = r["residual_CR261"] + correction
        if r["set"] == "train":
            train_res.append(new_residual)
        else:
            test_res.append(new_residual)
    trms = rms(train_res)
    tems = rms(test_res)
    marker = " ★" if trms < 5.0 else ""
    print(f"  {label:60s}: train={trms:.3f} test={tems:.3f}{marker}")
    return trms, tems


def optimize_1d(rows, coeff_fn, coeffs, label):
    """Try a range of coefficients."""
    print(f"\n{label}:")
    for c in coeffs:
        try_correction(rows, f"{c:+.2f} · <{label[:20]}>",
                       lambda r, c=c: c * coeff_fn(r))


def optimize_2d(rows, fn1, fn2, label1, label2):
    """Grid search 2 coefficients."""
    print(f"\nGrid search: {label1} + {label2}")
    best = (0, 0, float("inf"))
    for c1 in [-3, -2, -1, -0.5, 0, 0.5, 1, 2, 3]:
        for c2 in [-3, -2, -1, -0.5, 0, 0.5, 1, 2, 3]:
            train_res = []
            for r in rows:
                if r["set"] != "train":
                    continue
                correction = c1 * fn1(r) + c2 * fn2(r)
                train_res.append(r["residual_CR261"] + correction)
            trms = rms(train_res)
            if trms < best[2]:
                best = (c1, c2, trms)
    print(f"  best: {label1}={best[0]}, {label2}={best[1]}: train RMS={best[2]:.3f}")
    # Check test
    test_res = []
    for r in rows:
        if r["set"] != "test":
            continue
        correction = best[0] * fn1(r) + best[1] * fn2(r)
        test_res.append(r["residual_CR261"] + correction)
    print(f"    at best: test RMS = {rms(test_res):.3f}")


def show_r_distribution(rows):
    """Show residuals by (r_Z, r_N) buckets."""
    print("\nResiduals grouped by (r_Z, r_N):")
    for r_Z in [0, 2, 4, 6, 8, 10, 12, 14, 16]:
        matched = [r for r in rows if r["r_Z"] == r_Z]
        if not matched:
            continue
        residuals = [r["residual_CR261"] for r in matched]
        print(f"  r_Z={r_Z}: n={len(matched):>2d} mean={sum(residuals)/len(matched):+.2f} "
              f"RMS={rms(residuals):.2f}")


def main():
    rows = load_data()
    print(f"Loaded {len(rows)} rows")
    print(f"Baseline: train RMS = 5.555 MeV, test RMS = 8.574 MeV\n")

    show_r_distribution(rows)

    print("\n--- Single-term corrections ---")
    print("Try: correction = c · (Z mod 18)")
    optimize_1d(rows, lambda r: r["r_Z"], [-1.0, -0.5, -0.2, -0.1, 0.1, 0.2, 0.5, 1.0], "Z mod 18")

    print("\nTry: correction = c · (N mod 18)")
    optimize_1d(rows, lambda r: r["r_N"], [-1.0, -0.5, -0.2, -0.1, 0.1, 0.2, 0.5, 1.0], "N mod 18")

    print("\nTry: correction = c · (r_Z + r_N)")
    optimize_1d(rows, lambda r: r["r_Z"] + r["r_N"], [-1.0, -0.5, -0.2, -0.1, 0.1, 0.2, 0.5, 1.0], "r_Z + r_N")

    print("\nTry: correction = c · (r_Z · r_N)  [product, favors mid-shell]")
    optimize_1d(rows, lambda r: r["r_Z"] * r["r_N"], [-0.05, -0.02, -0.01, 0.01, 0.02, 0.05], "r_Z · r_N")

    print("\nTry: correction = c · (r_A) [A mod 18]")
    optimize_1d(rows, lambda r: r["r_A"], [-1.0, -0.5, -0.2, -0.1, 0.1, 0.2, 0.5, 1.0], "A mod 18")

    print("\n--- Two-term corrections ---")
    optimize_2d(rows,
                lambda r: r["r_Z"], lambda r: r["r_N"],
                "r_Z", "r_N")

    optimize_2d(rows,
                lambda r: r["r_Z"] + r["r_N"],
                lambda r: r["r_Z"] * r["r_N"] / 18,
                "sum", "prod/18")

    # A quadratic term based on distance from Θ-multiple
    print("\nTry: correction = c · min(r_Z, 18-r_Z)  [distance to nearest Θ]")
    def dist_theta(r):
        d = r["r_Z"]
        return min(d, 18 - d) if d else 0
    optimize_1d(rows, dist_theta,
                [-1.0, -0.5, -0.3, -0.2, 0.2, 0.3, 0.5, 1.0], "dist to Θ")


if __name__ == "__main__":
    main()
