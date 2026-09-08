"""Reusable exact full-block moment compiler and signed admission stream.

H000958: H uses all nodes even when the admitted prefix ends within the block.
One rational LDL factorization serves all admissions; no absolute-value
replacement of signed feedback is made.
"""
from __future__ import annotations

from fractions import Fraction as F

from .exact import ExactError, dot, fraction, integer, seal


class MomentBlock:
    def __init__(self, scale: int, degree: int):
        self.scale = integer(scale, minimum=1)
        self.degree = integer(degree, minimum=0)
        if self.degree >= self.scale:
            raise ExactError("full-block degree must be smaller than its node count")
        self.nodes = tuple(range(scale, 2*scale))
        self.rows = tuple(tuple(F(n, scale)**k for k in range(degree+1)) for n in self.nodes)
        size = degree+1
        self.gram = tuple(tuple(sum((row[i]*row[j]/n for n, row in zip(self.nodes, self.rows)), F())
                                for j in range(size)) for i in range(size))
        lower = [[F(int(i == j)) for j in range(size)] for i in range(size)]
        diagonal = []
        for i in range(size):
            pivot = self.gram[i][i]-sum(lower[i][k]**2*diagonal[k] for k in range(i))
            if pivot <= 0:
                raise ExactError("weighted Gram factorization has a nonpositive pivot")
            diagonal.append(pivot)
            for j in range(i+1, size):
                lower[j][i] = (self.gram[j][i]-sum(lower[j][k]*lower[i][k]*diagonal[k]
                                                for k in range(i)))/pivot
        self.lower = tuple(tuple(row) for row in lower)
        self.diagonal = tuple(diagonal)
        self.factorization_count = 1
        self.dual_rows = tuple(self.solve(row) for row in self.rows)

    def solve(self, rhs):
        rhs = tuple(fraction(value) for value in rhs)
        size = self.degree+1
        if len(rhs) != size:
            raise ExactError("moment right-hand side dimension differs")
        forward = []
        for i in range(size):
            forward.append(rhs[i]-sum(self.lower[i][j]*forward[j] for j in range(i)))
        result = [value/pivot for value, pivot in zip(forward, self.diagonal)]
        for i in reversed(range(size)):
            result[i] -= sum(self.lower[j][i]*result[j] for j in range(i+1, size))
        return tuple(result)

    def project(self, signed_prefix, *, retain_admissions: bool = True) -> dict:
        """Prefix starts at scale; its missing suffix is exactly zero.

        The unit-source rank budget is reported only for |c_n| <= 1.
        Arbitrary signed rational inputs retain their exact decomposition.
        """
        coefficients = tuple(fraction(value) for value in signed_prefix)
        if len(coefficients) > self.scale:
            raise ExactError("prefix exceeds this complete block")
        beta = (F(),)*(self.degree+1)
        diagonal, correlation, raw_bound = F(), F(), F()
        admissions = []
        for n, c, row, dual in zip(self.nodes, coefficients, self.rows, self.dual_rows):
            step = c/n
            injection = self.scale*step*step*dot(row, dual)
            feedback = 2*self.scale*step*dot(dual, beta)
            beta = tuple(a+step*b for a, b in zip(beta, row))
            diagonal += injection
            correlation += feedback
            raw_bound += self.scale*c*c/n
            if retain_admissions:
                admissions.append({"node": n, "signed_coefficient": c,
                                   "diagonal_injection": injection, "signed_feedback": feedback,
                                   "prefix_scaled_norm": diagonal+correlation})
        fitted = self.solve(beta)
        norm = self.scale*dot(beta, fitted)
        trace = sum((dot(row, dual)/n for n, row, dual in zip(self.nodes, self.rows, self.dual_rows)), F())
        if norm != diagonal+correlation or not 0 <= norm <= raw_bound or trace != self.degree+1:
            raise ExactError("exact moment projection reconstruction differs")
        return seal("Q3_EXACT_SIGNED_MOMENT_BLOCK_V1", scale=self.scale, degree=self.degree,
                    full_block=(self.scale, 2*self.scale-1), admitted_count=len(coefficients),
                    zero_extended_count=self.scale-len(coefficients), beta=beta, fitted=fitted,
                    scaled_norm=norm, diagonal=diagonal, signed_correlation=correlation,
                    positive_correlation=max(correlation, F()), raw_bessel_bound=raw_bound,
                    weighted_trace=trace,
                    unit_source_rank_bound=self.degree+1 if all(abs(c) <= 1 for c in coefficients) else None,
                    factorization_count=self.factorization_count, admissions=admissions)
