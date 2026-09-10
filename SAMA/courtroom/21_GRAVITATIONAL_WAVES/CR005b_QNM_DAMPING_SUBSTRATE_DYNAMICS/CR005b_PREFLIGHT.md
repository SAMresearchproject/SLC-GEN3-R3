# CR005b Preflight

Branch: 21_GRAVITATIONAL_WAVES
CR: CR005b_QNM_DAMPING_SUBSTRATE_DYNAMICS
Task title: CR005b QNM damping substrate dynamics

Firewall metadata:

```text
sam_language_v0_3_consulted_during_development = false
sam_language_v0_3_candidate_hash_known_to_research_agent = false
```

## Exact scientific question

Can SAM promote the CR003 exploratory match for the Schwarzschild fundamental
QNM damping coefficient into a source-role derivation:

```text
omega_I*M = R/(L - V) = R/(R^2 - d_hat^2) = 4/45
```

where `L - V` is the unresolved damping shell, without search, fitting, or
external-target construction?

## Claim tested

The fundamental Schwarzschild QNM imaginary component is the route-radix leak
rate across the unresolved ledger shell:

```text
damping_shell = L - V
omega_I*M     = R / damping_shell
              = 12 / (162 - 27)
              = 4/45
```

## Source authority

1. SAM V4.2 master/action engine for current radix-route grammar.
2. Branch 21 README and GW substrate framing for carrier-tensor context.
3. CR003 for the exploratory QNM expression and Berti comparator.
4. CR005 for the sealed real-frequency derivation and explicit damping open
   boundary.
5. QNM study notes for the CR005b damping frontier.

## Calculation/operator path

1. Build substrate atoms from exact integers:
   `h_hat=2`, `d_hat=3`, `S=8`, `V=27`, `F=81`, `R=12`, `R^2=144`,
   `Theta=18`, `L=162`, `M=126`.
2. Compute the unresolved damping shell:
   `L - V = 135`.
3. Verify the equivalent shell form:
   `L - V = R^2 - d_hat^2 = (R - d_hat)(R + d_hat) = 135`.
4. Compute:
   `omega_I*M = R/(L - V) = 4/45`.
5. Compare reveal-only to Berti 2009:
   `omega_I*M = 0.08896232`.
6. Run wrong controls.

## Output type and units

- Output: dimensionless QNM coefficient `omega_I*M`.
- Units: dimensionless.
- Radix basis: mixed with explicit conversion. SAM atoms are native structural
  integers; the comparator is external decimal.

## External data

External comparator only:

```text
omega_I_M_Berti_2009 = 0.08896232
```

No external target is used to choose a formula. No external dataset is opened.

## Free parameters

```text
free_parameter_count = 0
```

## Forbidden inputs

The runner must not read or import any forbidden language, holdout, forecast,
contract, or executable-language path. It must not read another test result at
runtime except the precommitted source files listed in the source manifest. It
must not use the Berti comparator to select, tune, or repair the formula.

## Controls

- WC1: `R/R^2`
- WC2: `R/L`
- WC3: `R/M`
- WC4: `d_hat/(L - V)`
- WC5: `Theta/(L - V)`
- WC6: `(pi + S)/M` as a non-sourced pi-neighbor from CR003

## Stopping conditions

- Stop as FAIL if the precommit hash does not match.
- Stop as FAIL if a source hash does not match the manifest.
- Stop as FAIL if any forbidden file guard trips.
- Stop as FAIL if exact arithmetic identities do not hold.
- Stop as BOUNDARY if the derivation identities hold but comparator separation
  or wrong-control separation is not strong enough for PASS.

## Permitted verdicts

Exactly one of:

```text
PASS
BOUNDARY
FAIL
```

## Falsification condition

Rule-9 falsification sentence:

```text
One exact source-identity failure, one source-hash mismatch, one forbidden-file
guard trip, one hidden fitted parameter, or an external comparator gap greater
than the precommitted PASS/BOUNDARY bands falsifies this CR's PASS claim.
```
