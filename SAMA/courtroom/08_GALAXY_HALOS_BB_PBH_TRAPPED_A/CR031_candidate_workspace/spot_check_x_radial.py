"""
CR031 Candidate — Option A spot-check.

Tests whether X(r) = V_dark^2 / V_bar^2 has a coherent shape across galaxies
when computed at multiple radii per galaxy from the SPARC mass-model data.

This is exploratory work. NOT a sealed CR. NOT a load-bearing claim.
Per the CR031 candidate note (2026-06-25):
  - confirms or kills the X-as-radial-law reading without sealing anything
  - falsifier: if X(r) profiles do NOT cluster after r-normalization,
    the reading has no independent radial-law content.
"""

from __future__ import annotations

from pathlib import Path
import csv

# SPARC mass-to-light ratios (Lelli et al. 2016c standard values)
UPSILON_DISK = 0.5
UPSILON_BUL  = 0.7

MRT_PATH = Path(
    r"C:\VS\Stam_model-A-v1.0\data\external_data\SPARC_G392\MassModels_Lelli2016c.mrt"
)

# Byte spans per the .mrt header
COL_ID    = (0, 11)
COL_D     = (12, 18)
COL_R     = (19, 25)
COL_VOBS  = (26, 32)
COL_EVOBS = (33, 38)
COL_VGAS  = (39, 45)
COL_VDISK = (46, 52)
COL_VBUL  = (53, 59)


def parse_mrt(path: Path) -> dict[str, list[dict]]:
    galaxies: dict[str, list[dict]] = {}
    with path.open("r") as f:
        lines = f.readlines()

    # Find the data start (line after the second '---' separator)
    in_data = False
    sep_count = 0
    for line in lines:
        if line.startswith("---"):
            sep_count += 1
            if sep_count == 3:
                in_data = True
            continue
        if not in_data:
            continue
        if not line.strip():
            continue

        gid   = line[COL_ID[0]:COL_ID[1]].strip()
        try:
            R     = float(line[COL_R[0]:COL_R[1]])
            Vobs  = float(line[COL_VOBS[0]:COL_VOBS[1]])
            eVobs = float(line[COL_EVOBS[0]:COL_EVOBS[1]])
            Vgas  = float(line[COL_VGAS[0]:COL_VGAS[1]])
            Vdisk = float(line[COL_VDISK[0]:COL_VDISK[1]])
            Vbul  = float(line[COL_VBUL[0]:COL_VBUL[1]])
        except ValueError:
            continue

        # V_bar^2 = sign(Vgas)·Vgas^2 + Y_disk·Vdisk^2 + Y_bul·Vbul^2
        # The sign() is so gas-rich centers (Vgas can be negative in inner radii) carry through
        vgas_signed = (1.0 if Vgas >= 0 else -1.0) * Vgas * Vgas
        vbar2 = vgas_signed + UPSILON_DISK * Vdisk * Vdisk + UPSILON_BUL * Vbul * Vbul
        vbar2 = max(vbar2, 0.0)
        vobs2 = Vobs * Vobs
        vdark2 = max(vobs2 - vbar2, 0.0)

        x = vdark2 / vbar2 if vbar2 > 0 else None

        row = dict(
            galaxy=gid,
            R_kpc=R,
            Vobs_kms=Vobs,
            eVobs_kms=eVobs,
            Vgas_kms=Vgas,
            Vdisk_kms=Vdisk,
            Vbul_kms=Vbul,
            Vbar2=vbar2,
            Vobs2=vobs2,
            Vdark2=vdark2,
            X=x,
        )
        galaxies.setdefault(gid, []).append(row)
    return galaxies


def pick_well_sampled(galaxies, min_points: int = 12) -> list[str]:
    return sorted(
        [g for g, rows in galaxies.items() if len(rows) >= min_points],
        key=lambda g: len(galaxies[g]),
        reverse=True,
    )


def vflat_estimate(rows: list[dict]) -> float:
    # Median of outer-third Vobs as a rough vflat proxy
    if len(rows) < 6:
        return 0.0
    sorted_rows = sorted(rows, key=lambda r: r["R_kpc"])
    outer_third = sorted_rows[-len(sorted_rows) // 3:]
    vals = sorted([r["Vobs_kms"] for r in outer_third])
    return vals[len(vals) // 2]


def main() -> None:
    out_dir = Path(__file__).parent
    out_dir.mkdir(parents=True, exist_ok=True)

    galaxies = parse_mrt(MRT_PATH)
    print(f"Loaded {len(galaxies)} galaxies, "
          f"{sum(len(rs) for rs in galaxies.values())} radial points")

    # Select 6 galaxies spanning the mass / vflat range
    well_sampled = pick_well_sampled(galaxies, min_points=12)
    by_vflat = sorted(
        [(g, vflat_estimate(galaxies[g])) for g in well_sampled],
        key=lambda x: x[1],
    )
    by_vflat = [x for x in by_vflat if x[1] > 0]

    n = len(by_vflat)
    if n >= 6:
        picks = [by_vflat[i] for i in (0, n // 5, 2 * n // 5, 3 * n // 5, 4 * n // 5, n - 1)]
    else:
        picks = by_vflat

    print("\n=== selected galaxies (spanning vflat range) ===")
    for g, v in picks:
        rows = galaxies[g]
        print(f"  {g:12s}  vflat~{v:6.1f} km/s   n_points={len(rows):3d}   "
              f"R_range=[{min(r['R_kpc'] for r in rows):5.2f}, "
              f"{max(r['R_kpc'] for r in rows):6.2f}] kpc")

    # Write per-radius X table
    per_radius_csv = out_dir / "x_radial_per_galaxy.csv"
    with per_radius_csv.open("w", newline="") as f:
        w = csv.writer(f)
        w.writerow([
            "galaxy", "R_kpc", "R_norm",
            "Vobs_kms", "Vbar_kms", "Vdark_kms",
            "X_substrate_over_matter", "dark_fraction_v2",
        ])
        for g, _ in picks:
            rows = sorted(galaxies[g], key=lambda r: r["R_kpc"])
            R_outer = rows[-1]["R_kpc"]
            for r in rows:
                if r["X"] is None:
                    continue
                vbar = r["Vbar2"] ** 0.5
                vdark = r["Vdark2"] ** 0.5
                dark_frac = r["Vdark2"] / r["Vobs2"] if r["Vobs2"] > 0 else 0.0
                w.writerow([
                    r["galaxy"],
                    f"{r['R_kpc']:.3f}",
                    f"{r['R_kpc']/R_outer:.4f}",
                    f"{r['Vobs_kms']:.2f}",
                    f"{vbar:.2f}",
                    f"{vdark:.2f}",
                    f"{r['X']:.4f}",
                    f"{dark_frac:.4f}",
                ])

    print(f"\nWrote {per_radius_csv}")

    # Compute X at five normalized-radius bins: 0.0-0.2, 0.2-0.4, 0.4-0.6, 0.6-0.8, 0.8-1.0
    print("\n=== X(r/R_outer) per galaxy at normalized-radius bins ===")
    bin_edges = [0.0, 0.2, 0.4, 0.6, 0.8, 1.0001]
    bin_labels = ["0.0-0.2", "0.2-0.4", "0.4-0.6", "0.6-0.8", "0.8-1.0"]
    header = "  " + " " * 14 + " | " + " | ".join(f"{lbl:>9}" for lbl in bin_labels)
    print(header)
    print("  " + "-" * (len(header) - 2))

    per_galaxy_binned: list[dict] = []
    for g, _ in picks:
        rows = sorted(galaxies[g], key=lambda r: r["R_kpc"])
        R_outer = rows[-1]["R_kpc"]
        bins: list[list[float]] = [[] for _ in range(5)]
        for r in rows:
            if r["X"] is None:
                continue
            r_norm = r["R_kpc"] / R_outer
            for i in range(5):
                if bin_edges[i] <= r_norm < bin_edges[i + 1]:
                    bins[i].append(r["X"])
                    break

        med_per_bin = []
        for b in bins:
            if not b:
                med_per_bin.append(None)
            else:
                bsorted = sorted(b)
                med_per_bin.append(bsorted[len(bsorted) // 2])
        per_galaxy_binned.append({"galaxy": g, "bins": med_per_bin})

        cells = []
        for x in med_per_bin:
            cells.append("       --" if x is None else f"{x:9.3f}")
        print(f"  {g:14s}  | " + " | ".join(cells))

    # Aggregate across galaxies: median X per normalized-radius bin
    print()
    print("  " + "-" * (len(header) - 2))
    agg = []
    for i in range(5):
        vals = [pgb["bins"][i] for pgb in per_galaxy_binned if pgb["bins"][i] is not None]
        if vals:
            vals.sort()
            agg.append(vals[len(vals) // 2])
        else:
            agg.append(None)
    cells = ["       --" if x is None else f"{x:9.3f}" for x in agg]
    print(f"  {'AGGREGATE (med)':14s}  | " + " | ".join(cells))

    # Summary statistics
    print("\n=== shape coherence test ===")
    valid_galaxies = sum(
        1 for pgb in per_galaxy_binned if all(b is not None for b in pgb["bins"])
    )
    print(f"  galaxies with X defined in all 5 r/R_outer bins: {valid_galaxies}/{len(picks)}")
    if valid_galaxies >= 3:
        # For each bin, compute std-dev across galaxies of log(X)
        import math
        print("\n  Cross-galaxy spread per bin (log10 X):")
        print("    bin       median_X    log10_X_spread (lower = more coherent)")
        for i in range(5):
            vals = [pgb["bins"][i] for pgb in per_galaxy_binned
                    if pgb["bins"][i] is not None and pgb["bins"][i] > 0]
            if len(vals) >= 2:
                logs = [math.log10(v) for v in vals]
                mean_log = sum(logs) / len(logs)
                std_log = (sum((lg - mean_log) ** 2 for lg in logs) / len(logs)) ** 0.5
                vals_sorted = sorted(vals)
                med = vals_sorted[len(vals_sorted) // 2]
                print(f"    {bin_labels[i]:>9}  {med:9.3f}    {std_log:6.3f}")

    # Reference X values from CR031 candidate note
    print("\n=== Reference X values from CR031 candidate note ===")
    print(f"  per-isotope at N=Z:      1.000  (CR240 forced identity)")
    print(f"  galactic outer median:   3.179  (CR025 SPARC median: 0.7607/0.2393)")
    print(f"  cosmological:            5.364  (CR023 Omega_PBH/Omega_b)")
    print(f"\n  predicted X(r/R_outer) profile if X = Q_sub/Q_matter is the radial law:")
    print(f"    inner bulge ~  1.0  (baryon-dominated)")
    print(f"    outer halo  ~  3.2  (median SPARC)")
    print(f"    cosmic      ~  5.4  (universe-average)")


if __name__ == "__main__":
    main()
