"""
Scratch pad: apply new session rules (CR266-CR273) to CR261 residuals
and attempt to reduce RMS below 5 MeV target.

Session rules to try:
  1. Tensor-Theta knockout: for nuclei where 3Z = Theta-multiple,
     add corrective term
  2. GKS Z-fold shell correction: components = gcd-structure
  3. Substrate-noble-Z (CR272): Z in {2, 18, 36, 54, 72, 108, 126}
  4. Doubly-magic signature (CR270 Pb-208 finding): both Z, N even
     with shared factor structure

Reads CR261_bw_fit_per_row.csv, applies corrections, reports new RMS.
"""

import csv
import math
import os
from functools import reduce

HERE = os.path.dirname(os.path.abspath(__file__))
FIT_CSV = os.path.join(HERE, "CR261_bw_fit_per_row.csv")

# Substrate atoms
H_HAT = 2
D_HAT = 3
THETA = H_HAT * D_HAT ** 2  # 18
M = 126

# Nuclear magic numbers (conventional shell model)
MAGIC = {2, 8, 20, 28, 50, 82, 126}

# Substrate-noble-cipher Z values (CR272/CR273)
SUBSTRATE_NOBLE_Z = {2, 18, 36, 54, 72, 108, 126}


def gcd_of(a, b):
    return math.gcd(a, b)


def gks_components_q3(u, d, e):
    """Number of disconnected components in q=3 source-count measure."""
    def lcm(a, b):
        return a * b // math.gcd(a, b)
    H_total = u * d * e
    K = lcm(u, d) * lcm(d, e) * lcm(e, u) // reduce(lcm, [u, d, e])
    return H_total // K


def theta_multiplicity(n):
    """Return k if n = k*Theta (k integer), else 0."""
    if n % THETA == 0:
        return n // THETA
    return 0


def load_data():
    rows = []
    with open(FIT_CSV, "r") as f:
        reader = csv.DictReader(f)
        for row in reader:
            row["Z"] = int(row["Z"])
            row["N"] = int(row["N"])
            row["A"] = int(row["A"])
            row["B_u_obs"] = float(row["B_u_obs_MeV"])
            row["B_u_pred_CR261"] = float(row["B_u_pred_MeV"])
            row["residual_CR261"] = float(row["residual_MeV"])
            # Compute source counts
            row["u"] = 2 * row["Z"] + row["N"]
            row["d"] = row["Z"] + 2 * row["N"]
            row["e"] = row["Z"]
            # Compute components
            row["components"] = gks_components_q3(row["u"], row["d"], row["e"])
            # Magic number check
            row["Z_magic"] = row["Z"] in MAGIC
            row["N_magic"] = row["N"] in MAGIC
            row["magic_count"] = int(row["Z_magic"]) + int(row["N_magic"])
            # Substrate noble Z check
            row["Z_substrate_noble"] = row["Z"] in SUBSTRATE_NOBLE_Z
            row["N_substrate_noble"] = row["N"] in SUBSTRATE_NOBLE_Z
            # Theta multiplicity of main = 3Z
            row["main_theta_mult"] = theta_multiplicity(3 * row["Z"])
            row["e_theta_mult"] = theta_multiplicity(row["Z"])
            rows.append(row)
    return rows


def rms(residuals):
    if not residuals:
        return 0.0
    return math.sqrt(sum(r * r for r in residuals) / len(residuals))


def report_baseline(rows):
    """Report CR261 baseline RMS."""
    train_res = [r["residual_CR261"] for r in rows if r["set"] == "train"]
    test_res = [r["residual_CR261"] for r in rows if r["set"] == "test"]
    print("CR261 baseline:")
    print(f"  train RMS = {rms(train_res):.3f} MeV ({len(train_res)} rows)")
    print(f"  test  RMS = {rms(test_res):.3f} MeV ({len(test_res)} rows)")
    print()


def try_shell_correction(rows, gamma_Z=5.0, gamma_N=5.0):
    """Add magic-shell correction: nuclei with magic Z or N get extra
    binding proportional to gamma."""
    print(f"TRIAL: shell correction (gamma_Z={gamma_Z}, gamma_N={gamma_N})")
    print(f"  (positive gamma = more binding at magic numbers)")
    train_res = []
    test_res = []
    for r in rows:
        correction = 0.0
        if r["Z_magic"]:
            correction += gamma_Z
        if r["N_magic"]:
            correction += gamma_N
        # CR261 residual = pred - obs
        # New residual = (pred + correction) - obs = old_residual + correction
        # But correction is expected to ADD binding, so pred should INCREASE
        # If correction represents extra binding beyond CR261 prediction,
        # pred_new = pred_old + correction (assuming positive gamma means added binding)
        new_residual = r["residual_CR261"] + correction
        if r["set"] == "train":
            train_res.append(new_residual)
        else:
            test_res.append(new_residual)
    print(f"  train RMS = {rms(train_res):.3f} MeV")
    print(f"  test  RMS = {rms(test_res):.3f} MeV")
    print()
    return rms(train_res), rms(test_res)


def try_shell_optimize(rows):
    """Find best (gamma_Z, gamma_N) that minimizes train RMS."""
    print("SEARCHING for optimal (gamma_Z, gamma_N) to minimize train RMS")
    best = (0, 0, float("inf"))
    for gz in [-10, -8, -6, -5, -4, -3, -2, -1, 0, 1, 2, 3, 4, 5, 6, 8, 10]:
        for gn in [-10, -8, -6, -5, -4, -3, -2, -1, 0, 1, 2, 3, 4, 5, 6, 8, 10]:
            train_res = []
            for r in rows:
                if r["set"] != "train":
                    continue
                correction = 0.0
                if r["Z_magic"]:
                    correction += gz
                if r["N_magic"]:
                    correction += gn
                new_residual = r["residual_CR261"] + correction
                train_res.append(new_residual)
            train_rms = rms(train_res)
            if train_rms < best[2]:
                best = (gz, gn, train_rms)
    print(f"  best: gamma_Z={best[0]}, gamma_N={best[1]}, train RMS={best[2]:.3f}")
    # Compute test RMS at best
    test_res = []
    for r in rows:
        if r["set"] != "test":
            continue
        correction = 0.0
        if r["Z_magic"]:
            correction += best[0]
        if r["N_magic"]:
            correction += best[1]
        new_residual = r["residual_CR261"] + correction
        test_res.append(new_residual)
    print(f"  at best params: test RMS = {rms(test_res):.3f}")
    print()
    return best


def try_substrate_noble_correction(rows):
    """Test if substrate-noble Z values give a specific correction pattern."""
    print("SUBSTRATE-NOBLE Z check (Z in {2, 18, 36, 54, 72, 108, 126}):")
    for r in rows:
        if r["Z_substrate_noble"] or r["N_substrate_noble"]:
            print(f"  {r['isotope']:8s} Z={r['Z']:>3d} N={r['N']:>3d} "
                  f"resid={r['residual_CR261']:+.3f} MeV  "
                  f"Z_noble={r['Z_substrate_noble']} N_noble={r['N_substrate_noble']}")
    print()


def try_component_scaled_correction(rows, kappa=0.15):
    """Add correction proportional to GKS component count."""
    print(f"TRIAL: components * kappa (kappa={kappa} MeV/component)")
    train_res = []
    test_res = []
    for r in rows:
        correction = kappa * r["components"]
        new_residual = r["residual_CR261"] + correction
        if r["set"] == "train":
            train_res.append(new_residual)
        else:
            test_res.append(new_residual)
    print(f"  train RMS = {rms(train_res):.3f} MeV")
    print(f"  test  RMS = {rms(test_res):.3f} MeV")
    print()


def show_largest_residuals(rows, n=10):
    """Show largest CR261 residuals."""
    print(f"LARGEST |residual| in CR261:")
    sorted_rows = sorted(rows, key=lambda r: abs(r["residual_CR261"]), reverse=True)
    for r in sorted_rows[:n]:
        magic_note = []
        if r["Z_magic"]:
            magic_note.append("Z-magic")
        if r["N_magic"]:
            magic_note.append("N-magic")
        magic_str = " (" + ", ".join(magic_note) + ")" if magic_note else ""
        print(f"  {r['isotope']:8s} Z={r['Z']:>3d} N={r['N']:>3d} A={r['A']:>3d} "
              f"resid={r['residual_CR261']:+7.3f} MeV{magic_str}")
    print()


def main():
    rows = load_data()
    print(f"Loaded {len(rows)} rows from CR261 fit data")
    print(f"  train: {sum(1 for r in rows if r['set']=='train')}")
    print(f"  test:  {sum(1 for r in rows if r['set']=='test')}")
    print()

    report_baseline(rows)
    show_largest_residuals(rows)

    # Try shell correction with initial guess
    try_shell_correction(rows, gamma_Z=5, gamma_N=5)
    try_shell_correction(rows, gamma_Z=-5, gamma_N=-5)

    # Optimize
    best = try_shell_optimize(rows)

    # Substrate noble check
    try_substrate_noble_correction(rows)

    # Component-based correction
    try_component_scaled_correction(rows, kappa=0.1)
    try_component_scaled_correction(rows, kappa=0.15)
    try_component_scaled_correction(rows, kappa=0.2)


if __name__ == "__main__":
    main()
