# CR222d Row Taxonomy Promotion Gate Result

**Result class:** `CR222d_PASS_ROW_TAXONOMY_PROMOTION_GATE__SUPPORT_GRAMMAR_NOT_MATTER`

**Checks:** 18/18

**CR222d_row_taxonomy_theorem.csv SHA-256:** `c0f8918974f660ddb0e51e10e3c37f1d59b8bcf0b98b0d02cec1d81ae2a1320a`

## Verdict

The uploaded CR219 overlay supports the theorem:

```text
native/source support != matter promotion
```

The taxonomy is:

```text
139 = 126 matter allowed + 13 blocked non-matter rows
126 = 63 stable matter + 63 bound composite
13  = 12 unique support roster rows + 1 duplicate mirror row
```

The support roster correction is:

```text
12 unique support rows = 0300+0301+0302+0304+0306..0313 = 81
duplicate mirror row   = QP093A-0303 = 81
closure                = 81 + 81 = 162
```

So QP093A-0303 remains blocked non-matter, but it is not counted as an
independent support mode.

The promotion gate is:

```text
G_matter=0 => M_obs=qA=T=W=0
G_matter=1 => qA=M_obs*(1+|q|/144), T=qA/8, W=7qA/8
```

The source-support surcharge shape is present:

```text
M_native = p + p^2/144
```

but the eight hidden support rows remain blocked, with qA/tensor/write channels
closed. This protects the Paul Revere packet from treating support inventory as
emitted matter.

If `.1` partition displays are present, CR222d treats them only as visual
support-row markers. They are not used as numeric partition inputs.
