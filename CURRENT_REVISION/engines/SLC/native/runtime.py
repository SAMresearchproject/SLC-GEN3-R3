"""One native Q3 context for shared exact operations and frozen quality inference."""
from __future__ import annotations

from collections import OrderedDict
from contextlib import ExitStack
import importlib.util
from pathlib import Path
import sys

from .exact import ExactError, integer
from .history import ConnectorHistory, response_partition
from .moments import MomentBlock
from .quadratic import quadratic_change, reciprocal_receiver
from .formula import compile_formulas
from .algebra import execute as execute_integer




class Q3Runtime:
    """Native operators and bounded source-keyed caches, scoped to one session.

    The existing learned Q3 model is an authenticated compatibility component.
    New exact history/receiver/moment/formula operations execute in this package.
    """
    def __init__(self, model=None, *, cache_size: int = 128):
        self.cache_size = integer(cache_size, minimum=1)
        self.model = model
        self._blocks = OrderedDict()
        self._scores = OrderedDict()
        self._stack = ExitStack()
        self._quality = None
        self.quality_module = None
        self.score_evaluations = 0
        self.factorizations = 0
        self._closed = False

    def __enter__(self):
        if self._closed:
            raise ExactError("Q3 session is closed")
        return self

    def __exit__(self, *args):
        self._closed = True
        self._blocks.clear()
        self._scores.clear()
        return self._stack.__exit__(*args)

    def _active(self):
        if self._closed:
            raise ExactError("Q3 session is closed")

    def _remember(self, cache, key, value):
        cache[key] = value
        cache.move_to_end(key)
        if len(cache) > self.cache_size:
            cache.popitem(last=False)
        return value

    def moment_block(self, scale, degree) -> MomentBlock:
        self._active()
        key = (integer(scale, minimum=1), integer(degree, minimum=0))
        if key not in self._blocks:
            self.factorizations += 1
            return self._remember(self._blocks, key, MomentBlock(*key))
        self._blocks.move_to_end(key)
        return self._blocks[key]

    def quality(self):
        self._active()
        if self._quality is None:
            from .. import slcq3_rz_current as module
            self._quality = self._stack.enter_context(module.open_runtime(self.model))
            self.quality_module = module
        return self._quality

    def derive_r3_graph(self, query, candidate):
        return self.quality().derive_r3_graph(query, candidate)

    @property
    def _foundation(self):
        return self.quality()._foundation

    def score(self, query, candidate):
        runtime = self.quality()
        if not isinstance(query, self.quality_module.SourceVisibleChoice) or \
           not isinstance(candidate, self.quality_module.CandidateGroupInput):
            raise ExactError("quality input types differ from the frozen Q3 interface")
        candidate._validated_roster()
        # SourceVisibleChoice and its tuple roster are frozen native values.
        # Keeping the full tuple preserves orientation and multiplicity.
        key = (query, candidate.visible_records)
        if key not in self._scores:
            self.score_evaluations += 1
            return self._remember(self._scores, key, runtime.score(query, candidate))
        self._scores.move_to_end(key)
        return self._scores[key]

    def rank(self, query, candidates):
        roster = tuple(candidates)
        if not roster:
            raise ExactError("quality candidate roster is empty")
        scores = tuple(self.score(query, candidate) for candidate in roster)
        ordered = tuple(sorted(range(len(roster)), key=lambda i: (scores[i], -i), reverse=True))
        top = tuple(i for i in ordered if scores[i] == scores[ordered[0]])
        return self.quality_module.RankOutcome(
            "SELECTED_UNIQUE" if len(top) == 1 else "AMBIGUOUS_TOP_SCORE", ordered, top, scores)

    def direction_fiber(self, address, writes, **custody):
        self._active()
        from .t18 import word
        return word(address, writes, **custody)

    def history_quotient(self, left, right):
        self._active()
        from .t18 import history_quotient
        return history_quotient(left, right)

    def graph_spectrum(self, instance, ports=(), **execution):
        self._active()
        from .structure import retained_spectrum
        return retained_spectrum(instance, ports, **execution)

    def connector(self, operands):
        self._active()
        return ConnectorHistory(tuple(operands)).receipt()

    def integer_operation(self, operation, payload):
        self._active()
        return execute_integer(operation,payload)

    def exact_information(self):
        """Return the authenticated V6/ICF1 component within this Q3 session."""
        return self.quality()._foundation

    def partition(self, histories, actions):
        self._active()
        return response_partition(histories, actions)

    def receiver(self, before, after, matrix, **units):
        self._active()
        return quadratic_change(before, after, matrix, **units)

    def reciprocal(self, left, right, current, matrix, **units):
        self._active()
        return reciprocal_receiver(left, right, current, matrix, **units)

    def formulas(self, operands, formulas):
        self._active()
        return compile_formulas(operands, formulas)
