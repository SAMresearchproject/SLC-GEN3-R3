"""
SAM-native galaxy halo derivation scratch — branch 08.

Per the galaxy mass derivation PDF (2026-06-27):
  X(r) = V_dark^2(r) / V_bar^2(r)                      (from CR031b)
  f_halo(r) = X(r) / (1 + X(r))                        (saturation coordinate)
  f_halo,inf = X_inf / (1 + X_inf)                     (X_inf = 3.18 from CR025)
  A_halo(rho) = f_halo(rho) / f_halo,inf, rho = r/R_outer
  c_SAM = 1 / rho_{1/2}    where A_halo(rho_{1/2}) = 1/2
  M_halo(<r) = r * X(r) * V_bar^2(r) / G

NOT a sealed CR. Exploratory work to see what the SAM-native halo machinery
looks like when applied to SPARC galaxies. If it lands, it becomes CR032.

X_inf = 3.18 from sealed CR025 outer dark-fraction median.
"""

from __future__ import annotations

from pathlib import Path
import csv
import math
import statistics

UPSILON_DISK = 0.5
UPSILON_BUL  = 0.7

# G in kpc * (km/s)^2 / M_sun  (SPARC workbook convention)
G_KPC_KMS2_PER_MSUN = 4.30091e-6

# Sealed: outer dark fraction X_inf from CR025 SPARC median
X_INF = 3.18
F_HALO_INF = X_INF / (1.0 + X_INF)  # = 0.7608

MRT_PATH = Path(
    r"C:\VS\Stam_model-A-v1.0\data\external_data\SPARC_G392\MassModels_Lelli2016c.mrt"
)


def parse_mrt(path: Path) -> dict[str, list[dict]]:
    galaxies: dict[str, list[dict]] = {}
    with path.open("r") as f:
        lines = f.readlines()
    in_data = False
    sep = 0
    for line in lines:
        if line.startswith("---"):
            sep += 1
            if sep == 3:
                in_data = True
            continue
        if not in_data or not line.strip():
            continue
        gid = line[0:11].strip()
        try:
            R     = float(line[19:25])
            Vobs  = float(line[26:32])
            Vgas  = float(line[39:45])
            Vdisk = float(line[46:52])
            Vbul  = float(line[53:59])
        except ValueError:
            continue
        # V_bar^2 with sign(V_gas)
        vgas_signed = (1.0 if Vgas >= 0 else -1.0) * Vgas * Vgas
        vbar2 = vgas_signed + UPSILON_DISK * Vdisk ** 2 + UPSILON_BUL * Vbul ** 2
        if vbar2 <= 0:
            continue
        vobs2 = Vobs * Vobs
        vdark2 = max(vobs2 - vbar2, 0.0)
        X = vdark2 / vbar2
        f_halo = X / (1.0 + X) if (1.0 + X) > 0 else None
        galaxies.setdefault(gid, []).append(dict(
            R=R, Vobs=Vobs, Vgas=Vgas, Vdisk=Vdisk, Vbul=Vbul,
            Vbar2=vbar2, Vobs2=vobs2, Vdark2=vdark2,
            X=X, f_halo=f_halo,
        ))
    return galaxies


def interpolate_crossing(rho_arr: list[float], a_arr: list[float],
                          target: float) -> float | None:
    """Find first rho where A_halo crosses target (linear interp)."""
    if not rho_arr or not a_arr:
        return None
    # Sort by rho
    pairs = sorted(zip(rho_arr, a_arr))
    rhos = [p[0] for p in pairs]
    aas = [p[1] for p in pairs]
    for i in range(len(pairs) - 1):
        a0, a1 = aas[i], aas[i + 1]
        r0, r1 = rhos[i], rhos[i + 1]
        if a0 <= target <= a1 or a1 <= target <= a0:
            if a1 == a0:
                return r0
            frac = (target - a0) / (a1 - a0)
            return r0 + frac * (r1 - r0)
    # If last point is above target, return last rho
    if aas[-1] >= target:
        return rhos[-1]
    return None


def classify_galaxy(rho_arr, a_arr, f_halo_inner, f_halo_outer,
                     rho_half, rho_90, slope_outer) -> str:
    """Configuration class per the PDF."""
    if rho_half is None:
        return "disturbed_or_non_closed"
    # Outer plateau-locked? A_halo at outer = ~1
    a_outer = a_arr[-1] if a_arr else None

    if rho_half < 0.3:
        return "early_saturating_halo"
    if rho_half > 0.7:
        return "late_saturating_halo"
    if a_outer is not None and a_outer >= 0.95 and slope_outer is not None and abs(slope_outer) < 0.2:
        return "plateau_locked_halo"
    if slope_outer is not None and slope_outer > 0.5:
        return "rising_edge_halo"
    if f_halo_inner is not None and f_halo_inner < 0.2:
        return "baryon_dominated_inner_closure"
    if f_halo_outer is not None and f_halo_outer > 0.8:
        return "outer_substrate_dominated_closure"
    return "intermediate"


def log10_slope(rho_arr, x_arr, lower=0.6, upper=1.0):
    """Estimate d log10(X) / d log10(rho) in outer region [lower, upper] of rho."""
    pts = [(r, x) for r, x in zip(rho_arr, x_arr)
           if r is not None and x is not None and r > 0 and x > 0
           and lower <= r <= upper]
    if len(pts) < 2:
        return None
    log_rho = [math.log10(p[0]) for p in pts]
    log_x = [math.log10(p[1]) for p in pts]
    n = len(pts)
    mr = sum(log_rho) / n
    mx = sum(log_x) / n
    num = sum((log_rho[i] - mr) * (log_x[i] - mx) for i in range(n))
    den = sum((log_rho[i] - mr) ** 2 for i in range(n))
    if den == 0:
        return None
    return num / den


def analyze_galaxy(gid: str, rows: list[dict]):
    if len(rows) < 3:
        return None
    rows = sorted(rows, key=lambda r: r["R"])
    R_outer = rows[-1]["R"]
    if R_outer <= 0:
        return None

    # rho, f_halo, A_halo per row
    rho_arr = [r["R"] / R_outer for r in rows]
    f_halo_arr = [r["f_halo"] for r in rows]
    x_arr = [r["X"] for r in rows]

    A_halo_arr = [
        (fh / F_HALO_INF) if fh is not None else None
        for fh in f_halo_arr
    ]
    # Drop rows where A_halo is None for crossing analysis
    rho_clean = [r for r, a in zip(rho_arr, A_halo_arr) if a is not None]
    A_clean = [a for a in A_halo_arr if a is not None]

    rho_half = interpolate_crossing(rho_clean, A_clean, 0.5)
    rho_90 = interpolate_crossing(rho_clean, A_clean, 0.9)
    c_SAM = (1.0 / rho_half) if (rho_half is not None and rho_half > 0) else None

    # Inner / outer f_halo
    f_halo_inner = f_halo_arr[0] if f_halo_arr else None
    f_halo_outer = f_halo_arr[-1] if f_halo_arr else None

    # Slope of log10(X) vs log10(rho) in outer half
    slope_outer = log10_slope(rho_arr, x_arr, lower=0.5, upper=1.0)

    # Halo mass at each radius and at outer edge
    M_halo_per_row = []
    for r in rows:
        if r["Vdark2"] > 0:
            M_halo_per_row.append(r["R"] * r["Vdark2"] / G_KPC_KMS2_PER_MSUN)
        else:
            M_halo_per_row.append(0.0)
    M_halo_outer = M_halo_per_row[-1] if M_halo_per_row else None

    # SAM-native: M_halo(<R_outer) = R_outer * X_inf * V_bar^2(R_outer) / G
    # The "predicted halo mass at outer edge if sealed X_inf applies"
    M_halo_sealed = (R_outer * X_INF * rows[-1]["Vbar2"]
                      / G_KPC_KMS2_PER_MSUN)

    config = classify_galaxy(
        rho_clean, A_clean, f_halo_inner, f_halo_outer,
        rho_half, rho_90, slope_outer,
    )

    return dict(
        galaxy=gid,
        n_points=len(rows),
        R_outer_kpc=R_outer,
        rho_half=rho_half,
        rho_90=rho_90,
        c_SAM=c_SAM,
        f_halo_inner=f_halo_inner,
        f_halo_outer=f_halo_outer,
        slope_outer_log_X_log_r=slope_outer,
        M_halo_outer_measured=M_halo_outer,
        M_halo_outer_sealed_X_inf=M_halo_sealed,
        Vbar_outer_kms=math.sqrt(max(rows[-1]["Vbar2"], 0.0)),
        Vobs_outer_kms=math.sqrt(rows[-1]["Vobs2"]),
        config=config,
    )


def main():
    galaxies = parse_mrt(MRT_PATH)
    print(f"Loaded {len(galaxies)} galaxies, "
          f"{sum(len(r) for r in galaxies.values())} valid radial points")
    print(f"Sealed X_inf = {X_INF}  (CR025 outer dark-fraction median)")
    print(f"f_halo,inf   = X_inf/(1+X_inf) = {F_HALO_INF:.6f}")
    print()

    results = []
    for gid, rows in galaxies.items():
        analysis = analyze_galaxy(gid, rows)
        if analysis is not None:
            results.append(analysis)
    print(f"Analyzed {len(results)} galaxies (>= 3 radial points)")

    # Configuration distribution
    print("\n=== Configuration class distribution ===")
    config_counts = {}
    for r in results:
        config_counts[r["config"]] = config_counts.get(r["config"], 0) + 1
    for cfg, n in sorted(config_counts.items(), key=lambda x: -x[1]):
        print(f"  {n:>4}  {cfg}")

    # c_SAM distribution
    c_vals = [r["c_SAM"] for r in results if r["c_SAM"] is not None]
    print(f"\n=== c_SAM distribution (n = {len(c_vals)}) ===")
    if c_vals:
        c_sorted = sorted(c_vals)
        n = len(c_sorted)
        print(f"  min     = {min(c_vals):.3f}")
        print(f"  25%     = {c_sorted[n//4]:.3f}")
        print(f"  median  = {c_sorted[n//2]:.3f}")
        print(f"  75%     = {c_sorted[3*n//4]:.3f}")
        print(f"  max     = {max(c_vals):.3f}")
        print(f"  mean    = {sum(c_vals)/n:.3f}")

    # rho_half distribution
    rh_vals = [r["rho_half"] for r in results if r["rho_half"] is not None]
    print(f"\n=== rho_{{1/2}} distribution (n = {len(rh_vals)}) ===")
    if rh_vals:
        rh_sorted = sorted(rh_vals)
        n = len(rh_sorted)
        print(f"  min     = {rh_sorted[0]:.3f}")
        print(f"  25%     = {rh_sorted[n//4]:.3f}")
        print(f"  median  = {rh_sorted[n//2]:.3f}")
        print(f"  75%     = {rh_sorted[3*n//4]:.3f}")
        print(f"  max     = {rh_sorted[-1]:.3f}")

    # M_halo distribution (sealed X_inf prediction)
    M_vals = [r["M_halo_outer_sealed_X_inf"] for r in results
              if r["M_halo_outer_sealed_X_inf"] is not None and r["M_halo_outer_sealed_X_inf"] > 0]
    print(f"\n=== M_halo(<R_outer) sealed-X_inf prediction (n = {len(M_vals)}) ===")
    if M_vals:
        M_sorted = sorted(M_vals)
        n = len(M_sorted)
        print(f"  min     = {M_sorted[0]:.3e}  M_sun")
        print(f"  25%     = {M_sorted[n//4]:.3e}  M_sun")
        print(f"  median  = {M_sorted[n//2]:.3e}  M_sun")
        print(f"  75%     = {M_sorted[3*n//4]:.3e}  M_sun")
        print(f"  max     = {M_sorted[-1]:.3e}  M_sun")

    # Sealed-vs-measured comparison
    M_pairs = [(r["M_halo_outer_measured"], r["M_halo_outer_sealed_X_inf"])
               for r in results
               if r["M_halo_outer_measured"] is not None
               and r["M_halo_outer_measured"] > 0
               and r["M_halo_outer_sealed_X_inf"] is not None
               and r["M_halo_outer_sealed_X_inf"] > 0]
    print(f"\n=== Sealed-X_inf predicted M_halo vs measured M_halo (n = {len(M_pairs)}) ===")
    if M_pairs:
        ratios = [s / m for m, s in M_pairs]
        ratios_log = [math.log10(r) for r in ratios if r > 0]
        ratios_sorted = sorted(ratios)
        n = len(ratios_sorted)
        print(f"  ratio (sealed/measured) min   = {ratios_sorted[0]:.3f}")
        print(f"  ratio 25%                     = {ratios_sorted[n//4]:.3f}")
        print(f"  ratio median                  = {ratios_sorted[n//2]:.3f}")
        print(f"  ratio 75%                     = {ratios_sorted[3*n//4]:.3f}")
        print(f"  ratio max                     = {ratios_sorted[-1]:.3f}")
        if ratios_log:
            mean_log = sum(ratios_log) / len(ratios_log)
            var_log = sum((lr - mean_log) ** 2 for lr in ratios_log) / len(ratios_log)
            print(f"  log10(ratio) mean             = {mean_log:+.3f}")
            print(f"  log10(ratio) std              = {var_log**0.5:.3f}")

    # Representative galaxies per configuration class
    print("\n=== representative galaxies per configuration class ===")
    by_class: dict[str, list] = {}
    for r in results:
        by_class.setdefault(r["config"], []).append(r)
    for cfg, items in sorted(by_class.items()):
        items_sorted = sorted(items, key=lambda x: -x["n_points"])[:3]
        print(f"\n  {cfg}  (n = {len(items)}):")
        print(f"    {'galaxy':<12} {'n_pts':>5} {'R_outer':>8} {'rho_1/2':>8} "
              f"{'c_SAM':>7} {'f_in':>6} {'f_out':>6} {'slope':>7} {'M_sealed':>10}")
        for r in items_sorted:
            rho_h = f"{r['rho_half']:.3f}" if r['rho_half'] is not None else "  --"
            cs = f"{r['c_SAM']:.2f}" if r['c_SAM'] is not None else "  --"
            slp = f"{r['slope_outer_log_X_log_r']:+.3f}" if r['slope_outer_log_X_log_r'] is not None else "    --"
            ms = f"{r['M_halo_outer_sealed_X_inf']:.2e}" if r['M_halo_outer_sealed_X_inf'] else "    --"
            print(f"    {r['galaxy']:<12} {r['n_points']:>5} "
                  f"{r['R_outer_kpc']:>8.2f} {rho_h:>8} "
                  f"{cs:>7} "
                  f"{r['f_halo_inner']:>6.3f} {r['f_halo_outer']:>6.3f} "
                  f"{slp:>7} {ms:>10}")

    # Write per-galaxy CSV
    out_path = Path(__file__).parent / "galaxy_mass_derivation_per_galaxy.csv"
    fields = ["galaxy", "n_points", "R_outer_kpc", "rho_half", "rho_90", "c_SAM",
              "f_halo_inner", "f_halo_outer", "slope_outer_log_X_log_r",
              "M_halo_outer_measured", "M_halo_outer_sealed_X_inf",
              "Vbar_outer_kms", "Vobs_outer_kms", "config"]
    with out_path.open("w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader()
        for r in results:
            w.writerow({k: r[k] for k in fields})
    print(f"\nWrote {out_path}")


if __name__ == "__main__":
    main()
