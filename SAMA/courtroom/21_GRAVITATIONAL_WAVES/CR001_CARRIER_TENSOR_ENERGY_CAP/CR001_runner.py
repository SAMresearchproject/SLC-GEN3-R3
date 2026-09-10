"""
CR001 -- Carrier-Tensor Energy Cap

EXPLORATORY first lock on the SAM GW framing. Tests whether every
confirmed LIGO/Virgo binary-merger event satisfies the substrate
cap E_GW/(M_total*c^2) <= Theta/R^2 = 1/8.

precommit : 1e37ca0a35394c2c6a1c36f8a124058c505f4ad9be339bdb1204d9cacf1d0805

Event data hardcoded as in-code literals (per precommit data
discipline). Sources cited in each row's comment field.
"""

import csv
import hashlib
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
PRECOMMIT_PATH = os.path.join(HERE, "CR001_PRECOMMIT.md")
PRECOMMIT_HASH = "1e37ca0a35394c2c6a1c36f8a124058c505f4ad9be339bdb1204d9cacf1d0805"

# Substrate atoms (CR229, CR258)
ALPHA_H = 2
D_HAT = 3
R = ALPHA_H ** 2 * D_HAT          # 12
R_SQ = R * R                      # 144
THETA = ALPHA_H * D_HAT ** 2      # 18
SUBSTRATE_CAP = THETA / R_SQ      # 1/8 = 0.125

# Curated LIGO/Virgo confirmed-event set, source-frame values.
# All values from LIGO/Virgo published catalog papers and event
# discovery papers. Format: (event_id, M_total_msun, E_rad_msun,
# event_class, source_citation)
#
# E_rad here is the radiated energy in units of solar-mass c^2 (so
# E_rad/M_total is dimensionless = E_GW / (M_total * c^2)).
#
# Sources:
#   GWTC-1: Abbott et al. 2019, Phys. Rev. X 9, 031040
#   GWTC-2: Abbott et al. 2021, Phys. Rev. X 11, 021053
#   GWTC-2.1: Abbott et al. 2024, Phys. Rev. D 109, 022001
#   GWTC-3: Abbott et al. 2023, Phys. Rev. X 13, 041039
#   GW170817: Abbott et al. 2017, Phys. Rev. Lett. 119, 161101
#   GW190521: Abbott et al. 2020, Phys. Rev. Lett. 125, 101102
#   GW190814: Abbott et al. 2020, Astrophys. J. Lett. 896, L44
#   GW190412: Abbott et al. 2020, Phys. Rev. D 102, 043015
#   GW200115: Abbott et al. 2021, Astrophys. J. Lett. 915, L5

EVENTS = [
    # event_id,       M_total, E_rad, class,    source
    ("GW150914",      65.3,    3.1,   "BBH",    "Abbott+2016 PRL 116 061102"),
    ("GW151012",      37.2,    1.6,   "BBH",    "GWTC-1"),
    ("GW151226",      21.5,    1.0,   "BBH",    "GWTC-1"),
    ("GW170104",      49.1,    2.2,   "BBH",    "GWTC-1"),
    ("GW170608",      18.6,    0.85,  "BBH",    "GWTC-1"),
    ("GW170729",      80.3,    4.8,   "BBH",    "GWTC-1"),
    ("GW170809",      56.4,    2.7,   "BBH",    "GWTC-1"),
    ("GW170814",      53.2,    2.7,   "BBH",    "GWTC-1"),
    ("GW170817",       2.74,   0.025, "BNS",    "Abbott+2017 PRL 119 161101"),
    ("GW170818",      62.5,    2.7,   "BBH",    "GWTC-1"),
    ("GW170823",      68.9,    3.3,   "BBH",    "GWTC-1"),
    ("GW190412",      37.3,    1.7,   "BBH-asym","Abbott+2020 PRD 102 043015"),
    ("GW190425",       3.4,    0.01,  "BNS",    "Abbott+2020 ApJL 892 L3"),
    ("GW190521",     150.0,    7.6,   "BBH-IMBH","Abbott+2020 PRL 125 101102"),
    ("GW190814",      25.8,    0.8,   "NSBH?",  "Abbott+2020 ApJL 896 L44"),
    ("GW200115",       6.6,    0.025, "NSBH",   "Abbott+2021 ApJL 915 L5"),
]


def file_sha256(p):
    with open(p, "rb") as f:
        return hashlib.sha256(f.read()).hexdigest()


def verify_precommit():
    h = file_sha256(PRECOMMIT_PATH)
    if h != PRECOMMIT_HASH:
        raise SystemExit(f"precommit hash mismatch: got {h} want {PRECOMMIT_HASH}")


def main():
    verify_precommit()
    print("CR001 -- Carrier-Tensor Energy Cap (EXPLORATORY)")
    print(f"precommit hash : {PRECOMMIT_HASH}")
    print()
    print(f"Substrate atoms:")
    print(f"  alpha_H = {ALPHA_H}, D = {D_HAT}")
    print(f"  R = alpha_H^2 * D = {R}")
    print(f"  Theta = alpha_H * D^2 = {THETA}")
    print(f"  R^2 = {R_SQ}")
    print(f"  cap = Theta / R^2 = {THETA}/{R_SQ} = {SUBSTRATE_CAP:.6f}")
    print()

    print(f"  {'event':>11s} {'class':>9s}  {'M_total':>8s}  {'E_rad':>6s}  "
          f"{'f_rad':>9s}  {'cap':>7s}  {'within?':>9s}")
    print(f"  {'-'*11} {'-'*9}  {'-'*8}  {'-'*6}  {'-'*9}  {'-'*7}  {'-'*9}")

    per_event = []
    n_pass = 0
    n_fail = 0
    n_boundary = 0
    max_frac = 0.0
    max_frac_event = None

    for ev_id, m_total, e_rad, ev_class, source in EVENTS:
        f_rad = e_rad / m_total
        within = f_rad <= SUBSTRATE_CAP
        margin = SUBSTRATE_CAP - f_rad
        near_boundary = (within and margin < 0.005)
        if within:
            n_pass += 1
            if near_boundary:
                n_boundary += 1
                status = "BOUND"
            else:
                status = "OK"
        else:
            n_fail += 1
            status = "OVER"
        if f_rad > max_frac:
            max_frac = f_rad
            max_frac_event = ev_id
        print(f"  {ev_id:>11s} {ev_class:>9s}  "
              f"{m_total:>8.2f}  {e_rad:>6.3f}  "
              f"{f_rad:>9.5f}  {SUBSTRATE_CAP:>7.5f}  {status:>9s}")
        per_event.append({
            "event_id": ev_id,
            "class": ev_class,
            "M_total_msun": m_total,
            "E_rad_msun_c2": e_rad,
            "f_rad": f_rad,
            "cap": SUBSTRATE_CAP,
            "margin": margin,
            "within_cap": within,
            "near_boundary_within_0p005": near_boundary,
            "source": source,
        })

    print()
    print(f"Summary:")
    print(f"  events tested        : {len(EVENTS)}")
    print(f"  within cap (PASS)    : {n_pass}")
    print(f"  near boundary (<0.5%): {n_boundary}")
    print(f"  exceeded cap (FAIL)  : {n_fail}")
    print(f"  max f_rad observed   : {max_frac:.5f} ({max_frac_event})")
    print(f"  cap                  : {SUBSTRATE_CAP:.5f}")
    print(f"  headroom to cap      : {SUBSTRATE_CAP - max_frac:.5f}")
    print()

    # Verdict
    if n_fail > 0:
        verdict = "FAIL"
    elif n_boundary > 0:
        verdict = "BOUNDARY"
    else:
        verdict = "PASS"
    print(f"CR001 VERDICT: {verdict}")
    print()

    # Emit outputs
    per_event_csv = os.path.join(HERE, "CR001_per_event.csv")
    with open(per_event_csv, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["event_id", "class", "M_total_msun", "E_rad_msun_c2",
                    "f_rad", "cap", "margin", "within_cap",
                    "near_boundary_within_0p005", "source"])
        for r in per_event:
            w.writerow([r["event_id"], r["class"], r["M_total_msun"],
                        r["E_rad_msun_c2"], r["f_rad"], r["cap"],
                        r["margin"], r["within_cap"],
                        r["near_boundary_within_0p005"], r["source"]])

    summary = {
        "artifact": "CR001_CARRIER_TENSOR_ENERGY_CAP",
        "mode": "EXPLORATORY",
        "verdict": verdict,
        "precommit_hash": PRECOMMIT_HASH,
        "substrate_atoms": {
            "alpha_H": ALPHA_H,
            "D": D_HAT,
            "R": R,
            "R_sq": R_SQ,
            "Theta": THETA,
        },
        "cap": SUBSTRATE_CAP,
        "cap_closed_form": "Theta / R^2 = 18/144 = 1/8 = 0.125",
        "events_tested": len(EVENTS),
        "within_cap": n_pass,
        "near_boundary": n_boundary,
        "exceeded_cap": n_fail,
        "max_f_rad_observed": max_frac,
        "max_f_rad_event": max_frac_event,
        "headroom_to_cap": SUBSTRATE_CAP - max_frac,
    }
    with open(os.path.join(HERE, "CR001_summary.json"), "w", encoding="utf-8") as f:
        json.dump(summary, f, indent=2, default=str)

    runner_hash = file_sha256(__file__)
    print(f"runner SHA-256 : {runner_hash}")


if __name__ == "__main__":
    main()
