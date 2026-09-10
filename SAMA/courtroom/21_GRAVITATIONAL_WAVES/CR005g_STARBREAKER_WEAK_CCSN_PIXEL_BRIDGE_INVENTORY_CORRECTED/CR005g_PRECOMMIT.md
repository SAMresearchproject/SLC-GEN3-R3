# CR005g Ledger-Scaled Carrier Inventory Precommit

CR005f stopped before creating a release because it assumed every Starbreaker
scenario contained 252 carriers. The frozen records instead close exactly on
the ledger-scaled rule:

```text
carrier_count = 18 * ledger_count

ledger_count  : 14   21   33    56
carrier_count : 252  378  594  1008
scenarios     : 24   24   24    24
total carrier occurrences = 53,568
```

This inventory is independently visible in the frozen typed roster, the
scenario decomposition, and the executed CR005d all-carrier rows. No waveform
match or null statistic was opened by CR005f.

CR005g changes only the per-scenario assertion and total carrier gate. The
exact trace projection, waveform population and doors, pixel construction,
observer bank, primary statistic, full-bank null searches, controls, evidence
ladder, and physical-claim ceiling remain frozen from CR005f and CR005e.

The run remains a normalized morphology comparison. It cannot yield physical
strain, luminosity, seconds, hertz, source distance, detector reach, or proof
of a common mechanism.

Same-run repair is prohibited.
