# CR262 — Correction Note (display-layer)

**Scope:** Reading-aid sidecar for `CR262_result.md`. Does NOT modify the
sealed result.md, runner.py, precommit, or HASHES.txt. The sealed artifacts
are preserved as originally produced; this note documents two display cells
that misrender values already stated correctly elsewhere in the same result.
**Sealed CR262 verdict, gates, headline table, and summary.json remain
authoritative and are not disputed by this note.**

**Applies to:** `CR262_result.md` sha256 as listed in
`CR262_SUBSTRATE_CHAIN_STEP_CIPHER_LIGHT_ANCHOR/HASHES.txt`.
**Stewardship:** `d9fe07c9b87bb52bc20b08bc1c8b24cb4fb312fbd35653b5d1030b14ed0a7e88`
**Note author:** Sean Brady, 2026-07-02.

---

## The two misrendered cells

### 1. Be-8 row, "observed" column — reads `stable`

**Location:** `CR262_result.md` per-nucleus table (row `Be-8`, column `observed`).

**Displayed:** `stable`

**Correct value (already stated correctly in this same CR's headline block):**

```text
t½ = 8.2 × 10⁻¹⁷ s  →  2α decay
```

See `CR262_result.md` headline (§ Headline, `CONTAINER atoms predict UNSTABLE:` block), which reads:

```text
Be-8   (u=d=12=R)   →  t½ = 8.2×10⁻¹⁷ s  → 2α  ✓
```

The `match` column of the per-nucleus row correctly reads `OK` — the runner's
gate arithmetic used the correct observed value (unstable) when it computed
that predicted (unstable) matches observed (unstable). Only the display cell
formatted the wrong string.

### 2. Ar-36 row, "observed" column and "match" column

**Location:** `CR262_result.md` per-nucleus table (row `Ar-36`).

**Displayed:** observed cell = `t1/2=Nones (stable)`, match cell = `MISS`.

**Correct values (already stated correctly in this same CR's gates):**

- observed: **stable** (Ar-36 has no measured half-life in AME2020 / NUBASE2020; it is a truly stable isotope of argon, natural abundance 0.334%, stable against all decay modes — note Ar-40 is the dominant natural argon isotope at 99.6%, but stability, not abundance, is what CR262 tests)
- match: **OK** (substrate predicted `stable`, observed `stable`, prediction matches)

See `CR262_result.md` § Gate-by-gate, G2:

```text
G2 | carrier-atom nuclei stable in AME2020 (4/4) | PASS
```

The 4/4 count of carrier-atom nuclei stable in AME2020 is {He-4, Li-6, C-12,
**Ar-36**}. The G2 PASS gate treats Ar-36 as stable and counts the prediction
as correct; the per-nucleus display cell was rendered inconsistently with the
gate that already passed on it.

---

## Cause

Both misrenders trace to the runner's per-row display-string builder. When
`observed_half_life = None` (i.e., the isotope is truly stable, so there is
no half-life value to format), the string builder printed the Python `None`
value as `Nones` and applied a boolean comparison for the `match` column
that treated `None` as "value missing" rather than "value = stable". The
downstream gate logic (G2, G3, G4) used the correct predicate on the
half-life field and passed as intended.

For Be-8 the string builder printed the fallback `stable` even though the
underlying `observed_half_life = 8.2e-17 s` was correctly loaded — the
formatter's condition selected the wrong branch on the half-life magnitude
threshold. Again, the gate logic used the correct observed value and
passed.

**Neither miscell affected the verdict, the gates, the headline block, or
the summary.json outputs.** The runner never wrote a wrong number into a
load-bearing artifact; it wrote wrong text into a display table read by
humans.

---

## Guidance for citation

Anyone citing CR262:

1. **The headline block is the citable source for per-nucleus stability.**
   Lines under `CARRIER atoms predict STABLE:` and `CONTAINER atoms predict
   UNSTABLE:` in `CR262_result.md` § Headline are correct and are the
   values used to compute the 8/8 match count.

2. **The Gate-by-gate table is the citable source for the 8/8 gate count.**
   G2 (4/4 carrier-stable), G3 (3/3 container-unstable), and G4 (Xe-108
   non-existent) partition the eight nuclei correctly.

3. **The per-nucleus display table (§ Per-nucleus detail) should be read
   with this correction note attached.** Two cells contradict the CR's
   own authoritative statements above and are display-layer misrenders,
   not evidence of a gate failure.

Downstream CRs that already reference CR262 (CR263, CR264, CR266, CR269,
CR270, CR273, CR277 close-out) all reference the headline / gate values,
not the per-nucleus display cells. No downstream artifact is affected.

---

## What was NOT done

- The sealed `CR262_result.md` was not edited. Its sha256 in
  `CR262_SUBSTRATE_CHAIN_STEP_CIPHER_LIGHT_ANCHOR/HASHES.txt` is unchanged.
- The runner was not re-executed and no artifacts were re-hashed.
- The verdict (`PASS`) is unchanged.
- No re-seal, no supersession, no new precommit chain. This note is a
  sibling reading aid, not a new sealed CR.

If a future CR needs the display cells to render correctly (e.g., for a
public-facing table export), the correct move is a downstream CR that reads
`CR262_result.md` as prior context and emits a corrected display artifact
with its own precommit + hashes — not a rewrite of the sealed original.

---

## Sibling correction note hash

Not added to `CR262_SUBSTRATE_CHAIN_STEP_CIPHER_LIGHT_ANCHOR/HASHES.txt`,
which reflects the sealed CR artifacts only. The sha256 for this note is
recorded only in the external sidecar `MATTER_INDEX_SHA256.txt`, following
the Vol I convention that a file's own hash cannot be embedded inside the
same file without invalidating itself.
