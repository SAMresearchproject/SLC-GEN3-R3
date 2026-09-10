"""Quick rerun to verify H-1 fix; writes to v2 filenames to avoid lock conflict."""
import sys
from pathlib import Path

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE))

import sob126_ledger as ldgr

ldgr.OUT_CSV  = HERE / "SOB126_ledger_v2.csv"
ldgr.OUT_XLSX = HERE / "SOB126_ledger_v2.xlsx"

rows = [ldgr.build_row(Z) for Z in range(1, 127)]
ldgr.write_csv(rows)
ldgr.write_xlsx(rows)

print(f"Wrote: {ldgr.OUT_CSV}")
print(f"Wrote: {ldgr.OUT_XLSX}")
print()

h1 = next(r for r in rows if r["Z"] == 1)
print("H-1 row after fix:")
for k in ["Z", "symbol", "N_sob", "A_sob", "observed_isotope", "N_observed", "A_observed",
         "delta_N", "delta_A", "B_u_u", "B_u_MeV", "B_smooth_MeV", "binding_residual_MeV"]:
    print(f"  {k:>22s} = {h1[k]}")
