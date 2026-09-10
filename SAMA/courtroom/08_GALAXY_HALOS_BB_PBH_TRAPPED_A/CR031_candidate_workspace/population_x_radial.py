"""
CR031 Candidate — Population test across all SPARC galaxies.

Scales the 6-galaxy spot-check to the full SPARC catalog. Computes per-galaxy
X(r/R_outer) profiles, bins into 5 normalized-radius bins, and reports the
population median X(r) curve plus the cross-galaxy IQR spread.

This is exploratory work. NOT a sealed CR. NOT a load-bearing claim.

Falsifier (per CR031 candidate note 2026-06-25):
  if the population median X(r) curve does NOT track from ~1.0 (inner) to
  ~5.4 (outer; cosmic Omega_PBH/Omega_b), the X-as-radial-law reading has no
  independent radial-law content and CR029's debt remains where it sits.
"""

from __future__ import annotations

from pathlib import Path
import csv
import math

UPSILON_DISK = 0.5
UPSILON_BUL  = 0.7
MIN_POINTS_PER_GALAXY = 5

MRT_PATH = Path(
    r"C:\VS\Stam_model-A-v1.0\data\external_data\SPARC_G392\MassModels_Lelli2016c.mrt"
)
G392_RESIDUALS = Path(
    r"C:\VS\Stam_model-A-v1.0\tests\Substrate\G392_REAL_SPARC_PBH_HALO_INVENTORY_TEST\G392_sparc_galaxy_residuals.csv"
)

# Reference X values from the CR031 candidate note
REF_INNER = 1.000   # per-isotope at N=Z (CR240 forced identity)
REF_MID   = 3.179   # galactic outer median (CR025 SPARC median: 0.7607/0.2393)
REF_COSMIC = 5.364  # cosmological Omega_PBH/Omega_b (sealed CR023)


def parse_mrt(path: Path) -> dict[str, list[dict]]:
    galaxies: dict[str, list[dict]] = {}
    with path.open("r") as f:
        lines = f.readlines()

    in_data = False
    sep_count = 0
    for line in lines:
        if line.startswith("---"):
            sep_count += 1
            if sep_count == 3:
                in_data = True
            continue
        if not in_data or not line.strip():
            continue

        gid = line[0:11].strip()
        try:
            R     = float(line[19:25])
            Vobs  = float(line[26:32])
            eVobs = float(line[33:38])
            Vgas  = float(line[39:45])
            Vdisk = float(line[46:52])
            Vbul  = float(line[53:59])
        except ValueError:
            continue

        vgas_signed = (1.0 if Vgas >= 0 else -1.0) * Vgas * Vgas
        vbar2 = vgas_signed + UPSILON_DISK * Vdisk * Vdisk + UPSILON_BUL * Vbul * Vbul
        vbar2 = max(vbar2, 0.0)
        vobs2 = Vobs * Vobs
        vdark2 = max(vobs2 - vbar2, 0.0)

        x = vdark2 / vbar2 if vbar2 > 0 else None

        galaxies.setdefault(gid, []).append(dict(
            R=R, Vobs=Vobs, eVobs=eVobs,
            Vbar2=vbar2, Vobs2=vobs2, Vdark2=vdark2,
            X=x,
        ))
    return galaxies


def load_quality_map(path: Path) -> dict[str, int]:
    qmap: dict[str, int] = {}
    if not path.exists():
        return qmap
    with path.open("r") as f:
        for row in csv.DictReader(f):
            try:
                qmap[row["galaxy"]] = int(row["quality"])
            except (KeyError, ValueError):
                pass
    return qmap


def per_galaxy_bin_medians(galaxies: dict[str, list[dict]],
                            galaxy_filter=None,
                            ) -> tuple[int, list[list[float]]]:
    """Return (n_galaxies_used, bins_with_per_galaxy_medians)."""
    bin_edges = [0.0, 0.2, 0.4, 0.6, 0.8, 1.0001]
    per_bin_galaxies: list[list[float]] = [[] for _ in range(5)]

    n_used = 0
    for gid, rows in galaxies.items():
        if galaxy_filter is not None and not galaxy_filter(gid):
            continue
        rows = [r for r in rows if r["X"] is not None]
        if len(rows) < MIN_POINTS_PER_GALAXY:
            continue
        rows.sort(key=lambda r: r["R"])
        R_outer = rows[-1]["R"]
        if R_outer <= 0:
            continue

        # per-bin per-galaxy median
        galaxy_bin_vals: list[list[float]] = [[] for _ in range(5)]
        for r in rows:
            r_norm = r["R"] / R_outer
            for i in range(5):
                if bin_edges[i] <= r_norm < bin_edges[i + 1]:
                    galaxy_bin_vals[i].append(r["X"])
                    break

        any_used = False
        for i in range(5):
            if galaxy_bin_vals[i]:
                galaxy_bin_vals[i].sort()
                med = galaxy_bin_vals[i][len(galaxy_bin_vals[i]) // 2]
                per_bin_galaxies[i].append(med)
                any_used = True
        if any_used:
            n_used += 1
    return n_used, per_bin_galaxies


def quantile(vals: list[float], q: float) -> float:
    s = sorted(vals)
    if not s:
        return float("nan")
    k = (len(s) - 1) * q
    f = int(k)
    c = min(f + 1, len(s) - 1)
    return s[f] + (s[c] - s[f]) * (k - f)


def report_profile(label: str, n_used: int, per_bin: list[list[float]]) -> None:
    bin_labels = ["0.0-0.2", "0.2-0.4", "0.4-0.6", "0.6-0.8", "0.8-1.0"]
    print(f"\n=== {label} ===")
    print(f"  galaxies contributing to at least one bin: {n_used}")
    print()
    print(f"  {'bin':>9}  {'n_galaxies':>10}  {'med_X':>8}  "
          f"{'Q1':>8}  {'Q3':>8}  {'log10_X_spread':>15}")
    print(f"  {'-' * 9}  {'-' * 10}  {'-' * 8}  {'-' * 8}  {'-' * 8}  {'-' * 15}")
    for i, lbl in enumerate(bin_labels):
        vals = per_bin[i]
        if not vals:
            print(f"  {lbl:>9}  {0:>10}  {'--':>8}  {'--':>8}  {'--':>8}  {'--':>15}")
            continue
        med = quantile(vals, 0.5)
        q1 = quantile(vals, 0.25)
        q3 = quantile(vals, 0.75)
        pos_vals = [v for v in vals if v > 0]
        if len(pos_vals) >= 2:
            logs = [math.log10(v) for v in pos_vals]
            mean_log = sum(logs) / len(logs)
            std_log = (sum((lg - mean_log) ** 2 for lg in logs) / len(logs)) ** 0.5
        else:
            std_log = float("nan")
        print(f"  {lbl:>9}  {len(vals):>10}  {med:>8.3f}  "
              f"{q1:>8.3f}  {q3:>8.3f}  {std_log:>15.3f}")


def reference_comparison(per_bin: list[list[float]]) -> None:
    if not per_bin[0] or not per_bin[2] or not per_bin[4]:
        return
    inner_med = quantile(per_bin[0], 0.5)
    mid_med = quantile(per_bin[2], 0.5)
    outer_med = quantile(per_bin[4], 0.5)
    print("\n  Reference comparison:")
    print(f"    inner  (r/R~0.1) :  data={inner_med:6.3f}   ref={REF_INNER:6.3f}  "
          f"(N=Z baryon-dominated; CR240)   delta={inner_med - REF_INNER:+.3f}")
    print(f"    middle (r/R~0.5) :  data={mid_med:6.3f}   ref={REF_MID:6.3f}  "
          f"(CR025 SPARC median)            delta={mid_med - REF_MID:+.3f}")
    print(f"    outer  (r/R~0.9) :  data={outer_med:6.3f}   ref={REF_COSMIC:6.3f}  "
          f"(Omega_PBH/Omega_b; CR023)      delta={outer_med - REF_COSMIC:+.3f}")
    if REF_COSMIC > 0:
        rel_outer = (outer_med - REF_COSMIC) / REF_COSMIC * 100
        print(f"    outer-edge relative gap from cosmic-X reference: {rel_outer:+.2f}%")


def main() -> None:
    galaxies = parse_mrt(MRT_PATH)
    print(f"Loaded {len(galaxies)} galaxies, "
          f"{sum(len(rs) for rs in galaxies.values())} radial points")

    qmap = load_quality_map(G392_RESIDUALS)
    if qmap:
        n_q1 = sum(1 for v in qmap.values() if v == 1)
        n_q2 = sum(1 for v in qmap.values() if v == 2)
        n_q3 = sum(1 for v in qmap.values() if v == 3)
        print(f"Quality flags from G392: Q1={n_q1}, Q2={n_q2}, Q3={n_q3}")

    # Full population
    n_all, per_bin_all = per_galaxy_bin_medians(galaxies)
    report_profile("Full population (all galaxies with >= 5 valid points)",
                   n_all, per_bin_all)
    reference_comparison(per_bin_all)

    # Quality-1 only
    if qmap:
        q1_filter = lambda g: qmap.get(g, 99) == 1
        n_q1_used, per_bin_q1 = per_galaxy_bin_medians(galaxies, q1_filter)
        report_profile("Quality-1 only (highest-rated SPARC galaxies)",
                       n_q1_used, per_bin_q1)
        reference_comparison(per_bin_q1)

    # Write the full per-galaxy aggregate table
    out_csv = Path(__file__).parent / "x_population_per_galaxy_binned.csv"
    bin_labels = ["bin_0.0-0.2", "bin_0.2-0.4", "bin_0.4-0.6",
                  "bin_0.6-0.8", "bin_0.8-1.0"]
    rows_out: list[dict] = []
    bin_edges = [0.0, 0.2, 0.4, 0.6, 0.8, 1.0001]
    for gid, rows in galaxies.items():
        rows = [r for r in rows if r["X"] is not None]
        if len(rows) < MIN_POINTS_PER_GALAXY:
            continue
        rows.sort(key=lambda r: r["R"])
        R_outer = rows[-1]["R"]
        if R_outer <= 0:
            continue
        gbins: list[list[float]] = [[] for _ in range(5)]
        for r in rows:
            r_norm = r["R"] / R_outer
            for i in range(5):
                if bin_edges[i] <= r_norm < bin_edges[i + 1]:
                    gbins[i].append(r["X"])
                    break
        d = dict(galaxy=gid, n_points=len(rows), R_outer_kpc=round(R_outer, 2))
        for i, lbl in enumerate(bin_labels):
            if gbins[i]:
                d[lbl] = round(quantile(gbins[i], 0.5), 4)
            else:
                d[lbl] = ""
        if qmap:
            d["quality"] = qmap.get(gid, "")
        rows_out.append(d)

    fields = ["galaxy", "n_points", "R_outer_kpc"]
    if qmap:
        fields.append("quality")
    fields += bin_labels
    with out_csv.open("w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader()
        for r in rows_out:
            w.writerow(r)
    print(f"\nWrote {out_csv}  ({len(rows_out)} galaxies)")


if __name__ == "__main__":
    main()
