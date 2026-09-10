# CR090 Coverage Map

```text
artifact: CR090_coverage_map.md
inventory: CR090_candidate_anchor_inventory.csv
status: DRAFT (citation_verification_status across all rows = PENDING)
```

## Live Candidates Per Target CR

```text
CR091 precision electroweak          11 rows (EW001..EW011)
CR092 Higgs sector                   15 rows (H001..H015)
CR093 heavy flavour                   9 rows (HF001..HF009)
CR094 exotic spectroscopy             8 rows (EXO001..EXO008)
CR095 lepton universality             7 rows (LU001..LU007)
                                  --------
total live candidates                50 rows
```

All five anchor-class CRs exceed the CR090 declared-premises minimum
of 5 live candidates per target CR.

## Honest-Negative Candidates (CR096)

```text
HN001 CLASS_B  CDF II W mass (Tevatron not CERN)
HN002 CLASS_D  Fermilab muon g-2 (Fermilab not CERN)
HN003 CLASS_C  Belle R(D*) (B-factory not CERN)
HN004 CLASS_E  KamLAND theta_12 (reactor neutrino not CERN)
HN005 CLASS_F  PDG world-average W mass used as anchor
HN006 CLASS_A  Withdrawn early Run-1 ATLAS Higgs mass
HN007 CLASS_G  Perturbed CMS Higgs mass (synthetic)
                                  --------
total honest-negatives                7 rows (one per class A..G)
```

The CR090 minimum (7 honest-negatives covering classes A..G) is met
exactly. CR096 may add more class-A through class-G rows if the
curator identifies additional withdrawn or non-CERN measurements
during verification.

## Multi-Experiment Cross-Source Coverage (Pillar 3)

Observables with two or more independent CERN measurements feeding
the same SAM prediction:

```text
W boson mass            EW001 ATLAS  EW002 CMS  EW003 LHCb
W boson decay width     EW005 ATLAS  EW006 LEP combined
top quark mass          EW007 ATLAS  EW008 CMS
sin^2 theta_W eff       EW009 ATLAS  EW010 CMS  EW011 LHCb
Higgs mass              H001 ATLAS  H002 CMS  H003 ATLAS+CMS combined
H -> gamma gamma mu     H004 ATLAS  H005 CMS
H -> ZZ* -> 4l mu       H006 ATLAS  H007 CMS
H -> WW* mu             H008 ATLAS  H009 CMS
H -> tau tau mu         H010 ATLAS  H011 CMS
H -> bb mu (VH)         H012 ATLAS  H013 CMS
H -> mu mu evidence     H014 CMS   H015 ATLAS
B_s -> mu mu BR         HF001 LHCb  HF002 CMS
W lepton universality   LU006 W->e/mu  LU007 W->tau/mu (ATLAS, same paper)
                                  --------
observables with multi-experiment cover    13
```

The CR090 declared-premises minimum (3 observables with multi-
experiment cross-source) is exceeded by a wide margin. Pillar 3
defense is strong on the W mass and Higgs sector in particular.

## Single-Experiment-Only (Pillar 3 not claimed for these rows)

```text
Z boson mass                       LEP combined        EW004
B^0 -> mu mu upper limit           LHCb only           HF003
Delta m_s                          LHCb dominant       HF004
Delta m_d                          LHCb dominant       HF005
sin 2 beta                         LHCb dominant       HF006
gamma CKM                          LHCb dominant       HF007
phi_s                              LHCb dominant       HF008
B -> K* mu mu P5'                  LHCb dominant       HF009
X(3872) mass / width               LHCb precision      EXO001 EXO002
Tcc+(3875)                         LHCb discovery      EXO003
Pc(4312/4440/4457) trio            LHCb discovery      EXO004 EXO005 EXO006
Pcs(4459)0                         LHCb discovery      EXO007
Xi_cc++                            LHCb discovery      EXO008
R(D), R(D*), R(J/psi)              LHCb dominant       LU003 LU004 LU005
R_K, R_K*                          LHCb dominant       LU001 LU002
```

For these rows, `cross_source_status = SINGLE` is recorded. Pillar 3
is not claimed; only Pillars 1, 2, and 4 apply. This is honest
disclosure: where only LHCb has measured the observable to date, we
cannot triangulate. The branch verdict reflects this asymmetry.

## SAM Prediction Source Coverage

```text
09a/CR062a row13 W boson           EW001 EW002 EW003 EW005 EW006 HN001 HN005
09a/CR062a row14 Z boson           EW004
09a/CR062a row6+row16 top quark    EW007 EW008
09a/CR062a row15 Higgs             H001 H002 H003 HN006 HN007
QP075 electroweak mixing operator  EW009 EW010 EW011
QP075 H decay role operator        H004..H015
QP075 rare-decay role operator     HF001 HF002 HF003 HF009
QP075 B mixing operator            HF004 HF005
QP075 CKM angle operator           HF006 HF007
QP075 CP violation operator        HF008
QP075 / V4.1 composite partition   EXO001 EXO002 EXO003
QP075 / V4.1 5q partition          EXO004 EXO005 EXO006 EXO007
QP075 / V4.1 ccq partition         EXO008
QP075 charged-lepton operator      LU001..LU007 HN002 HN003
QP075 neutrino mixing operator     HN004
```

Every live candidate names a sam_prediction_source. No row is
prediction-source-orphaned.

## Pre-CR091 Verification Punch List

Before CR091 builds its anchor envelope, the curator must:

```text
1. promote citation_verification_status from PENDING to
   VERIFIED_BY_CURATOR for every EW001..EW011 row in CR091 scope by
   confirming arXiv id, journal reference, publication date, and
   measurement value against the cited source
2. write CR091_cern_anchor_envelope.json with the eleven EW rows,
   each carrying central value + stat unc + sys unc + units +
   publication reference + date
3. write CR091_cern_anchor_envelope.json.sha256.txt sibling and lock
4. only then invoke the CR091 runner (which follows the four-pillar
   blindness protocol)
```

The same verification pattern applies for CR092..CR095 against their
respective inventory slices.

## What CR090 Did Not Do

```text
- CR090 did NOT open any anchor envelope
- CR090 did NOT compute any residual
- CR090 did NOT declare per-class tolerance bands (those live in
  each target CR's own precommit)
- CR090 did NOT promote any citation_verification_status; all rows
  remain PENDING until curator review
- CR090 did NOT exercise Pillars 1 or 2 directly; those bite at
  CR091..CR095 runner time
```
