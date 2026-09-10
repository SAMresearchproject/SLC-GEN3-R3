"""
Scratch: apply Θ-channel knockout directly to CR261 residuals.

For each nucleus, count how many of the (u, d, e) source counts are
Θ-multiples. The "Θ doesn't charge" rule from Sean's feedback memory
suggests these channels contribute 0 to binding.

Test whether nuclei with Θ-multiple channels show systematically
different residuals than those without.
"""

import csv
import math
import os

HERE = os.path.dirname(os.path.abspath(__file__))
FIT_CSV = os.path.join(HERE, "CR261_bw_fit_per_row.csv")

H_HAT = 2
D_HAT = 3
THETA = 18


def load_data():
    rows = []
    with open(FIT_CSV, "r") as f:
        reader = csv.DictReader(f)
        for row in reader:
            Z = int(row["Z"])
            N = int(row["N"])
            A = int(row["A"])
            u = 2 * Z + N
            d = Z + 2 * N
            e = Z
            row.update({
                "Z": Z, "N": N, "A": A,
                "u": u, "d": d, "e": e,
                "B_u_obs": float(row["B_u_obs_MeV"]),
                "B_u_pred_CR261": float(row["B_u_pred_MeV"]),
                "residual_CR261": float(row["residual_MeV"]),
                "u_is_theta_mult": u % THETA == 0,
                "d_is_theta_mult": d % THETA == 0,
                "e_is_theta_mult": e % THETA == 0,
            })
            row["theta_channel_count"] = (
                int(row["u_is_theta_mult"])
                + int(row["d_is_theta_mult"])
                + int(row["e_is_theta_mult"])
            )
            rows.append(row)
    return rows


def rms(vals):
    if not vals:
        return 0.0
    return math.sqrt(sum(v * v for v in vals) / len(vals))


def show_by_theta_count(rows):
    """Group nuclei by theta_channel_count and show residuals."""
    print("Residuals grouped by number of Θ-multiple channels:")
    for tc in range(4):
        subset = [r for r in rows if r["theta_channel_count"] == tc]
        if not subset:
            continue
        residuals = [r["residual_CR261"] for r in subset]
        print(f"\n  {tc} Θ-channels ({len(subset)} nuclei):")
        print(f"    mean residual  = {sum(residuals)/len(residuals):+.3f} MeV")
        print(f"    RMS residual   = {rms(residuals):.3f} MeV")
        for r in subset:
            channels = []
            if r["u_is_theta_mult"]:
                channels.append(f"u={r['u']}")
            if r["d_is_theta_mult"]:
                channels.append(f"d={r['d']}")
            if r["e_is_theta_mult"]:
                channels.append(f"e={r['e']}")
            channel_str = ",".join(channels) if channels else "none"
            print(f"      {r['isotope']:8s} Z={r['Z']:>3d} N={r['N']:>3d}: "
                  f"resid={r['residual_CR261']:+7.3f}  Θ-channels: {channel_str}")


def try_theta_channel_correction(rows, alpha=0.0):
    """Add correction proportional to number of Θ-channels."""
    print(f"\nTRIAL: correction = alpha * theta_channel_count, alpha={alpha}")
    train_res = []
    test_res = []
    for r in rows:
        correction = alpha * r["theta_channel_count"]
        new_residual = r["residual_CR261"] + correction
        if r["set"] == "train":
            train_res.append(new_residual)
        else:
            test_res.append(new_residual)
    print(f"  train RMS = {rms(train_res):.3f} MeV")
    print(f"  test  RMS = {rms(test_res):.3f} MeV")
    return rms(train_res), rms(test_res)


def optimize_theta_correction(rows):
    """Find optimal alpha for theta-channel correction."""
    print("\nSearching for optimal alpha:")
    best = (0, float("inf"))
    for alpha in [-10, -8, -6, -5, -4, -3, -2, -1, 0, 1, 2, 3, 4, 5, 6, 8, 10]:
        train_res = []
        for r in rows:
            if r["set"] != "train":
                continue
            correction = alpha * r["theta_channel_count"]
            train_res.append(r["residual_CR261"] + correction)
        train_rms = rms(train_res)
        if train_rms < best[1]:
            best = (alpha, train_rms)
    print(f"  best alpha = {best[0]}, train RMS = {best[1]:.3f}")


def main():
    rows = load_data()
    print(f"Loaded {len(rows)} rows\n")

    show_by_theta_count(rows)
    try_theta_channel_correction(rows, alpha=0)  # baseline
    optimize_theta_correction(rows)


if __name__ == "__main__":
    main()
