# Why the two channels admit a local inverse

Let A=X_002 and B=X_006 be vectors of eight Gaussian integers, with direction
and carrier sample as separate coordinates. H000970 gives X_084=-B. Therefore

    S = z0 A + (z1-z2) B
    U = a0 A + (a1-a2) B.

Both are projections of one F(q)=(S,U). The six real source coordinates h and
their unsigned occupancy |h| are existing native readouts. Forming (h,|h|)
before applying diag(T,T) supplies the common algebraic reception mechanism.
Reception overwrites the current local frame. The list of observations is
separately retained by the experiment and is the inverse's ordered input.

For direction d in {+1,-1}, a Write on relation j contributes

    delta_j F = ((i^d-1) z_j X_j, (i-1)(-1)^q_j X_j).

Every signed factor is nonzero. If A and B are complex-linearly independent,
a Write on relation 0 cannot equal one on relation 1 or 2. For relations 1
and 2, equal signed increments require z1=-z2, hence q1=q2+2 mod 4: their
parities agree. Equal occupancy increments, because X_084=-B, require opposite
parities. The requirements are incompatible. Thus all three possible next
Writes have different two-lane increments at every q and either direction.

One nonzero complex 2x2 minor of A and B certifies their independence. The
executor checks the fixed minor using the first forward and first reverse
carrier sample separately at each declared rho. It retains all 128 exact
Gaussian-integer determinants. This certifies the declared finite family;
no unbounded-rho extrapolation is used.

Starting with the declared initial q, each observed change identifies its
Write uniquely. Induction reconstructs the word and every phase prefix. The
primary implementation retains all matches so a coding or data deviation
cannot be hidden by choosing the first one. The independent implementation
enumerates lawful words without using this stepwise algorithm.

This also explains the original collision: opposite phases have the same
axis occupancy. Their signed changes cancel against opposite templates, but
their occupancy changes have opposite receiver signs and reveal which relation
changed. Conversely, the occupancy map forgets the phase sign that the signed
channel retains. The two channels stay distinct throughout reception.

The formula gives a local statement for arbitrary sequences of unit Writes
on these three relations, provided their direction and chronological
increments are known and the two template conditions hold. The executed
comparison remains the declared three-Write, six-order census. Longer words,
unknown initial phase/direction, moving geometry and physical readout are not
silently added to that census.
