"""Diagnostic: find the 7 UNCATEGORIZED rows from CR276."""

import csv
import os

HERE = os.path.dirname(os.path.abspath(__file__))
TABLE = os.path.join(HERE, "CR276_anchoring_table.csv")

with open(TABLE, "r", encoding="utf-8") as f:
    for r in csv.DictReader(f):
        if r["category"] == "UNCATEGORIZED":
            print(f"  {r['candidate_id']}  bin={r['bin']}  route_class={r['route_class']}")
            print(f"      partition={r['partition']}  depth={r['depth']}  sign={r['sign']}  q_abs={r['q_abs']}")
            print(f"      operator_class={r['operator_class']}")
            print(f"      closure_status={r['closure_status']}")
            print()
