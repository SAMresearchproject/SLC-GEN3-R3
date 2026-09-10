"""Build inputs/external_nuclide_table.csv from the locked QP061 observed roster.

QP061 is the sealed external NUBASE-style isotope dataset already present in this
repo's upstream (used in CR226 reveal phase). We normalize its columns into the
Test 8 schema.
"""
import csv
import hashlib
from pathlib import Path

ROOT = Path(__file__).resolve().parent
QP061 = Path(r"C:\VS\quantum_phase\artifacts\qp061\qp061_observed_roster_normalized.csv")
OUT = ROOT / "inputs" / "external_nuclide_table.csv"


def sha256_file(p: Path) -> str:
    h = hashlib.sha256()
    with p.open("rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def main():
    qp061_sha = sha256_file(QP061)
    print(f"QP061 source: {QP061}")
    print(f"QP061 sha256: {qp061_sha}")

    with QP061.open("r", encoding="utf-8-sig", newline="") as f:
        src = list(csv.DictReader(f))
    print(f"QP061 rows: {len(src)}")

    out_fields = ["Z", "N", "A", "symbol", "half_life", "half_life_sec",
                  "is_stable", "isomer_flag", "isomer_status_unknown", "source"]
    out_rows = []
    for r in src:
        Z = int(r["observed_Z"])
        N = int(r["observed_N"])
        A_raw = (r.get("observed_A") or "").strip()
        A = int(A_raw) if A_raw else Z + N
        symbol = r.get("observed_symbol", "")
        half_life = r.get("half_life", "")
        hl_sec_raw = (r.get("half_life_sec") or "").strip()
        is_stable_raw = (r.get("is_stable_or_long_lived") or "").strip().lower()
        is_stable = is_stable_raw == "true"
        # If is_stable AND half_life_sec missing, set to inf
        if is_stable and not hl_sec_raw:
            hl_sec = "inf"
        elif hl_sec_raw:
            hl_sec = hl_sec_raw
        else:
            hl_sec = ""
        out_rows.append({
            "Z": Z,
            "N": N,
            "A": A,
            "symbol": symbol,
            "half_life": half_life,
            "half_life_sec": hl_sec,
            "is_stable": is_stable,
            "isomer_flag": "",  # QP061 does not distinguish; mark unknown
            "isomer_status_unknown": True,
            "source": "QP061_OBSERVED_ROSTER_NORMALIZED",
        })

    with OUT.open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=out_fields, lineterminator="\n")
        w.writeheader()
        for row in out_rows:
            w.writerow(row)

    out_sha = sha256_file(OUT)
    print(f"\nWrote {OUT.name}: {len(out_rows)} rows, sha {out_sha}")
    return qp061_sha, out_sha


if __name__ == "__main__":
    main()
