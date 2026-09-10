# CR071 Appeal Channel Documentation

## Permanent Verdict

```text
CR071_BOUNDARY_PRE_REGISTERED_PREDICTION
```

This verdict is PERMANENT and never overwritten.

## Appeal Outcomes (M3 Channel)

```text
APPEAL_FRONTIER_HIT  - a post-2026-06-13 IAEA observation in Z=97..118
                       matches one of CR071's pre-registered ZNA rows.
                       Outcome: append a NEW CR with verdict
                       APPEAL_FRONTIER_HIT.  CR071 itself remains
                       BOUNDARY_PRE_REGISTERED_PREDICTION.

APPEAL_FRONTIER_MISS - a post-2026-06-13 IAEA observation in Z=97..118
                       does NOT match any of CR071's pre-registered ZNA
                       rows.  Outcome: append a NEW CR with verdict
                       APPEAL_FRONTIER_MISS.  CR071 itself remains
                       BOUNDARY_PRE_REGISTERED_PREDICTION.
```

## Invocation Format

```text
1. Cite this CR (CR071) and the sealed frontier map sha256.
2. Cite the post-2026-06-13 IAEA LiveChart artifact with its sha256.
3. Cite the per-row comparison: predicted ZNA vs observed ZNA.
4. Submit as a new courtroom CR appended after CR072 branch verdict.
```

## Sealed Frontier Map Hash

See: `CR071_pre_registered_frontier_map.sha256.txt`
