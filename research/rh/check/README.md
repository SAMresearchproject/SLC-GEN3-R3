# Check executable retained history

The concrete public test is whether the **short-horizon certificates rebuild from retained prefix state without future Möbius signs**, and whether the **signed transport identity recombines exactly** from the downloadable scale-8192 output. SAMA volumes and the paused Mersenne campaign provide supporting context; neither is a prerequisite.

## Run the check

Python 3.10+ and the standard library suffice for this identified independent check. From the repository root:

```sh
python3 research/rh/check/verify_retained_history.py
curl -L --fail -o COVERAGE_S8192.json.gz https://github.com/SAMresearchproject/SLC-GEN3-R3/releases/download/research-2026-09-14/COVERAGE_S8192.json.gz
python3 research/rh/check/verify_retained_history.py --coverage COVERAGE_S8192.json.gz
```

The [scale-8192 archive](https://github.com/SAMresearchproject/SLC-GEN3-R3/releases/download/research-2026-09-14/COVERAGE_S8192.json.gz) is 95,125,149 bytes and contains all 8,193 prefixes and native source witnesses. SHA-256: `4313557d89fa97e51d8c283fafa0f24eac5f81d11edbc28baddbf33944839ff5`.

The checker reconstructs the three scale-4096 four-admission certificates from [prefix-only packets](PREFIX_CERTIFICATES.json), matching the original exact rational bounds and branch counts. It accepts no future-sign sequence. At each future index, squareful coefficients are zero and squarefree coefficients branch over both signs; the exact signed energy state is propagated down every branch. Squarefree support is determined from the integer index. The expected certificate fields are comparison targets and do not enter the branch calculation. The [original native implementation](original/extensions/forcing_prospective_r1/search.cpp) and [recorded results](original/results/forcing_prospective_r1/EVALUATION_S4096.json) are included for comparison.

With `--coverage`, it authenticates the original archive and recombines seven exact energy, transport, remainder, sum-of-squares and signed-parity identities at every supplied witness. It also independently rebuilds all 8,193 coarse prefix energies, forcing values and excesses in admission order, and fine energies and source hashes at every witness. Signs are computed only for the admission being processed, with no suffix lookup. The certificate calculation remains separate: it never computes actual future signs and instead enumerates the allowed continuations.

The certificate experiment is at scale4096; the complete forcing scan is at scale8192. They are separately identified inputs to the executable-history check. The recovery certificate at t=1130 keeps E below one-half for four admissions; the certificates at t=1071 and t=1077 keep E below one. Uniform renewal through continuing admissions remains the mathematical task.

[Recorded independent verification](VERIFICATION.json): all three certificate bounds match, 24,597 exact source reconstruction comparisons and 21 exact transport checks pass.
