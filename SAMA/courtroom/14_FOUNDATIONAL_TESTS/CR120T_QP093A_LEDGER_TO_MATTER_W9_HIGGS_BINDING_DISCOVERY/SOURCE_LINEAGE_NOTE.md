# CR120T Source Lineage Note

Recorded from the project steward before frozen validation execution:

- the first QP093A generator output contained 321 rows;
- the 126-row promotion is one selection pass over that original output;
- the CR253 80-row promotion is a separate selection pass;
- the two updated workbooks are a third look at the original QP093A output;
- the proposed 81-row roster must not be merged with either the 126-row or
  80-row promoted set merely because all three descend from QP093A.

CR120T consequence: the frozen F81 candidate is explicitly a rule learned on
the first updated workbook's 126-row `count=1` promoted lane and tested as a
126-to-81 projection attempt. It is not presented as a rule independently
learned over the original 321-row universe. Typed values are reconciled by
candidate ID to the frozen corrected 299-row canonical catalog; that
canonicalization does not erase the workbook lineage above.

