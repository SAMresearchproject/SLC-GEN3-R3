"""Build the external reveal reference CSV from the CR226 sealed reveal comparison.

The CR226 reveal comparison already sources from QP061 (atomic mass) and CR119
(known symbols/names) AFTER the prediction seal — it is the canonical downstream
reveal source. We re-shape it into the column layout this test's reveal mode expects.
"""
from __future__ import annotations
import csv
import hashlib
from pathlib import Path

ROOT = Path(__file__).resolve().parent
CR226_REVEAL = Path(r"C:\VS\The_Courtroom\09a_PARTICLE_MASS_CHAIN\CR226_VAULTED_SOB_CARD_GENERATION_FREEZE_REVEAL\vault\03_reveal\CR226_reveal_comparison_126.csv")
OUT = ROOT / "reveal_reference.csv"


def sha256_file(p: Path) -> str:
    h = hashlib.sha256()
    with p.open("rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def main():
    with CR226_REVEAL.open("r", encoding="utf-8-sig", newline="") as f:
        src = list(csv.DictReader(f))
    print(f"Source CR226_reveal_comparison_126.csv: {len(src)} rows")
    print(f"Source SHA-256: {sha256_file(CR226_REVEAL)}")

    out_rows = []
    for r in src:
        out_rows.append({
            "Z": r["Z"],
            "symbol": r.get("known_symbol", ""),
            "name": r.get("known_name", ""),
            "external_anchor_A": r.get("A", ""),
            "external_anchor_N": r.get("N", ""),
            "external_stability_label": r.get("reference_clock", ""),
            "measured_mass_u": r.get("atomic_mass_u_reveal", ""),
        })

    fields = ["Z", "symbol", "name", "external_anchor_A", "external_anchor_N",
              "external_stability_label", "measured_mass_u"]
    with OUT.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fields, lineterminator="\n")
        writer.writeheader()
        for row in out_rows:
            writer.writerow(row)
    print(f"Wrote: {OUT.name}  ({len(out_rows)} rows)  sha={sha256_file(OUT)}")


if __name__ == "__main__":
    main()
