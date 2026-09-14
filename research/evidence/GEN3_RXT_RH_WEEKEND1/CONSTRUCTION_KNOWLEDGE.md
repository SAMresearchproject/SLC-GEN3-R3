# Readable construction knowledge from native minima

The first production extraction contains **375 explicit rules from 27 small
selected trees**. The rendering cutoff is 32 leaves per tree. All 45 targets
are indexed; larger trees remain available through `TRAIN_MODEL` and can be
extracted with a larger rendering limit.

The shared-four-state-orbit model has **22 leaves**, each with probability
exactly zero or one in the selected tree. Native extraction records zero
exceptions across **1,111,861 training rows and 239,131 development rows**.
The 239,152 reserved test rows were not used in this extraction. Current
coverage and exceptions appear in each rule; target-definition metadata in
the JSON retains its original source-policy provenance.

One particularly readable positive rule is:

> Exactly one of triad multiplicities 0 and 1 is nonzero, and exactly one of
> triad multiplicities 2 and 3 is nonzero.

Its explicit native conditions are `m0*m1=0`, `m2*m3=0`,
`(m0-m1)^2>0`, and `(m2-m3)^2>0`. The multiplicities are the source integers
0 through 4. This leaf records 129,780 training families and 20,350 development
families, all with the shared four-state orbit target.

Native witness **604364** uses multiplicities `[3,0,3,0]`. Contexts 3 and 11
both minimize at states **43520, 44031, 218112, 218623**, forming the recorded
common quarter-turn orbit. Their source minimum actions are **921/4** and
**157**. Both reference complete minimum set
`00f803a946dc62a414e65909f79a9e74e1398a674df8cbda6e8f1977fe8c3db5`.

The [complete 22-rule sheet](reports/1789232410484/rules/shared_four_state_orbit-24282096d5aa.md)
contains the remaining cases and witnesses. Its model SHA is
`24282096d5aa5ffbd3c4566065ce964feed3ca4aa2ef7257a09cb3f9050f286a`;
native extraction receipt
`392fe2e22db2fb709c17f758be475b89dc82ff6e11d05a6d9b96e2ecb66c27f2`.
Source domain SHA:
`9ef3e988a674812b1c4a02331276dfa1dcb19c7a557282e38f18119c0f714af1`.
The JSON companion retains every witness's source features, all 32 context
minima and the complete minimum-set bitmaps. Each review refreshes these
records when the selected models or their acquired support change.
