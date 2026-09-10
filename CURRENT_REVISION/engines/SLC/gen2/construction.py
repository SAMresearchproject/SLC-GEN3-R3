"""Typed instances, incidence pullbacks and retained Li-6 construction views.

Source accounts belong to instances; an instance may have several responses.
This allows the hidden packet to supply its center and depth-loop responses
without adding a second copy of its source amount.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from fractions import Fraction
from functools import lru_cache
from pathlib import Path
import json
import struct

from .exact import rational, canonical, digest
from .readouts import vec, matrix, dot, matvec, matmul, transpose, quadratic_value

DEPENDENCIES = Path(__file__).parent / "dependencies"


def hidden_lift(partition):
    p = rational(partition)
    if p < 0:
        raise ValueError("source partition must be nonnegative")
    return p + p * p / 144


def activation_value(rule, context):
    """A small declarative activation language; no Python evaluation or hidden state."""
    if type(rule) is bool:
        return Fraction(int(rule))
    if isinstance(rule, (int, str, Fraction)):
        return rational(rule)
    if not isinstance(rule, dict) or len(rule) != 1:
        raise ValueError("activation requires an exact value or one declared operator")
    if "flag" in rule:
        key = rule["flag"]
        if key not in context or type(context[key]) is not bool:
            raise ValueError("activation flag is absent or not boolean: " + str(key))
        return Fraction(int(context[key]))
    if "equals" in rule:
        key, value = rule["equals"]
        if key not in context:
            raise ValueError("activation context is absent: " + str(key))
        return Fraction(int(canonical(context[key]) == canonical(value)))
    if "all" in rule:
        values = [activation_value(item, context) for item in rule["all"]]
        if any(value not in (0, 1) for value in values):
            raise ValueError("all activation operands must be boolean values")
        return Fraction(int(all(values)))
    if "product" in rule:
        value = Fraction(1)
        for item in rule["product"]:
            value *= activation_value(item, context)
        return value
    raise ValueError("unregistered activation operator")


@dataclass(frozen=True)
class SourceAccount:
    name: str
    amount: Fraction
    unit: str
    formula: dict | None = None
    provenance: dict = field(default_factory=dict)

    @classmethod
    def from_dict(cls, item):
        name, unit = item["name"], item["unit"]
        if not isinstance(name, str) or not name or not isinstance(unit, str) or not unit:
            raise ValueError("source account requires name and unit")
        formula = item.get("formula")
        amount = rational(item["amount"]) if "amount" in item else None
        if formula is not None:
            if formula.get("operation") != "hidden_lift":
                raise ValueError("unregistered source account formula")
            calculated = hidden_lift(formula["partition"])
            if amount is not None and amount != calculated:
                raise ValueError("source account amount differs from its native formula")
            amount = calculated
        if amount is None:
            raise ValueError("source account has no exact amount")
        return cls(name, amount, unit, formula, item.get("provenance", {}))

    def to_dict(self):
        return canonical({"name": self.name, "amount": self.amount, "unit": self.unit,
                          "formula": self.formula, "provenance": self.provenance})


@dataclass(frozen=True)
class SourceAction:
    action_id: str
    pullback: tuple
    form: tuple
    coefficients: dict
    activation: object = True
    metadata: dict = field(default_factory=dict)

    @classmethod
    def from_dict(cls, item, dimension):
        pull = matrix(item["pullback"], columns=dimension)
        if not pull:
            raise ValueError("action pullback cannot be empty")
        form = matrix(item["form"], len(pull), len(pull), True)
        coefficients = {name: rational(value) for name, value in item.get("coefficients", {"native": 1}).items()}
        if not coefficients or any(not isinstance(name, str) or not name for name in coefficients):
            raise ValueError("an action requires named output accounts")
        return cls(item.get("action_id", "response"), pull, form, coefficients,
                   item.get("activation", True), item.get("metadata", {}))

    def to_dict(self):
        return canonical({"action_id": self.action_id, "pullback": self.pullback, "form": self.form,
                          "coefficients": self.coefficients, "activation": self.activation, "metadata": self.metadata})


@dataclass(frozen=True)
class TypedInstance:
    instance_id: str
    kind: str
    multiplicity: int
    actions: tuple
    accounts: tuple
    activation: object = True
    context: dict = field(default_factory=dict)

    @classmethod
    def from_dict(cls, item, dimension):
        multiplicity = item.get("multiplicity", 1)
        if type(multiplicity) is not int or multiplicity < 1:
            raise ValueError("instance multiplicity must be a positive integer")
        # In the compact single-action spelling, activation belongs to the
        # instance. Nested actions may independently declare their own factor.
        shorthand = {key: value for key, value in item.items() if key != "activation"}
        actions = item.get("actions", [shorthand] if "pullback" in item else [])
        instance_id, kind = item["instance_id"], item["kind"]
        if not isinstance(instance_id, str) or not instance_id or not isinstance(kind, str) or not kind:
            raise ValueError("an instance requires a stable id and type")
        parsed = tuple(SourceAction.from_dict(action, dimension) for action in actions)
        if len({action.action_id for action in parsed}) != len(parsed):
            raise ValueError("duplicate action id on the same instance")
        accounts = tuple(SourceAccount.from_dict(account) for account in item.get("accounts", []))
        if len({account.name for account in accounts}) != len(accounts):
            raise ValueError("duplicate account name on the same instance")
        return cls(instance_id, kind, multiplicity, parsed, accounts, item.get("activation", True), item.get("context", {}))

    def to_dict(self):
        return canonical({"instance_id": self.instance_id, "kind": self.kind, "multiplicity": self.multiplicity,
                          "actions": [action.to_dict() for action in self.actions],
                          "accounts": [account.to_dict() for account in self.accounts],
                          "activation": self.activation, "context": self.context})


@dataclass(frozen=True)
class ConstructionSpec:
    construction_id: str
    coordinates: tuple
    instances: tuple
    output_units: dict
    alternatives: dict = field(default_factory=dict)
    metadata: dict = field(default_factory=dict)

    @classmethod
    def from_dict(cls, item):
        coordinates = tuple(item["coordinates"])
        if not coordinates or any(not isinstance(x, str) or not x for x in coordinates) or len(set(coordinates)) != len(coordinates):
            raise ValueError("construction coordinates must be nonempty unique names")
        instances = tuple(TypedInstance.from_dict(instance, len(coordinates)) for instance in item["instances"])
        if len({instance.instance_id for instance in instances}) != len(instances):
            raise ValueError("source instance counted more than once")
        units = dict(item.get("output_units", {"native": "NATIVE_SOURCE_ACTION"}))
        if any(not isinstance(value, str) or not value for value in units.values()):
            raise ValueError("output account units must be explicit")
        if any(name not in units for instance in instances for action in instance.actions for name in action.coefficients):
            raise ValueError("action output account lacks declared units")
        return cls(item["construction_id"], coordinates, instances, units, item.get("alternatives", {}), item.get("metadata", {}))

    def to_dict(self):
        return canonical({"construction_id": self.construction_id, "coordinates": self.coordinates,
                          "instances": [instance.to_dict() for instance in self.instances],
                          "output_units": self.output_units, "alternatives": self.alternatives, "metadata": self.metadata})

    def compile(self, context=None):
        context = {} if context is None else context
        n = len(self.coordinates)
        forms = {name: [[Fraction() for _ in range(n)] for _ in range(n)] for name in self.output_units}
        terms = []
        totals = {}
        for instance in self.instances:
            active = activation_value(instance.activation, context)
            for account in instance.accounts:
                key = account.name + "@" + account.unit
                totals[key] = totals.get(key, Fraction()) + instance.multiplicity * account.amount
            for action in instance.actions:
                weight = instance.multiplicity * active * activation_value(action.activation, context)
                pulled = matmul(transpose(action.pullback), matmul(action.form, action.pullback))
                term_forms = {}
                for name, coefficient in action.coefficients.items():
                    scaled = tuple(tuple(weight * coefficient * value for value in row) for row in pulled)
                    term_forms[name] = scaled
                    for i, row in enumerate(scaled):
                        for j, value in enumerate(row):
                            forms[name][i][j] += value
                terms.append({"instance_id": instance.instance_id, "action_id": action.action_id,
                              "activation": weight, "forms": term_forms})
        return CompiledConstruction(self, context, {key: matrix(value) for key, value in forms.items()}, terms, totals)


@dataclass(frozen=True)
class CompiledConstruction:
    source: ConstructionSpec
    context: dict
    forms: dict
    terms: list
    source_account_totals: dict

    def to_dict(self):
        return canonical({"schema": "GEN2_COMPILED_CONSTRUCTION_V1", "source": self.source.to_dict(),
                          "source_sha256": digest(self.source.to_dict()), "context": self.context,
                          "forms": self.forms, "terms": self.terms, "source_account_totals": self.source_account_totals,
                          "account_total_policy": "INVENTORY_MULTIPLICITY_WITHOUT_RESPONSE_ACTIVATION"})

    def evaluate(self, values):
        x = vec(values)
        if len(x) != len(self.source.coordinates):
            raise ValueError("construction operand dimension differs")
        return canonical({"schema": "GEN2_CONSTRUCTION_RESPONSE_V1", "construction_id": self.source.construction_id,
                          "values": {name: quadratic_value(q, x) for name, q in self.forms.items()},
                          "output_units": self.source.output_units, "context": self.context,
                          "instances": [{"instance_id": term["instance_id"], "action_id": term["action_id"],
                                         "values": {name: quadratic_value(q, x) for name, q in term["forms"].items()}}
                                        for term in self.terms], "alternatives": self.source.alternatives})


def activation_change(source, before, after, *, before_context=None, after_context=None):
    spec = source if isinstance(source, ConstructionSpec) else ConstructionSpec.from_dict(source)
    c0, c1 = spec.compile(before_context), spec.compile(after_context)
    x, y = vec(before), vec(after)
    if len(x) != len(y) or len(x) != len(spec.coordinates):
        raise ValueError("construction change dimensions differ")
    delta = tuple(b - a for a, b in zip(x, y))
    results = {}
    for name in c0.forms:
        q0, q1 = c0.forms[name], c1.forms[name]
        form_change = tuple(tuple(b - a for a, b in zip(row0, row1)) for row0, row1 in zip(q0, q1))
        self_value = quadratic_value(q1, delta)
        cross = 2 * dot(x, matvec(q1, delta))
        changed_construction = quadratic_value(form_change, x)
        direct = quadratic_value(q1, y) - quadratic_value(q0, x)
        if direct != self_value + cross + changed_construction:
            raise ArithmeticError("activation change reconstruction differs")
        results[name] = {"before": quadratic_value(q0, x), "after": quadratic_value(q1, y),
                         "difference": direct, "self": self_value, "occupied_cross": cross,
                         "changed_construction": changed_construction}
    return canonical({"schema": "GEN2_ACTIVATION_CHANGE_V1", "accounts": results,
                      "before_context": c0.context, "after_context": c1.context,
                      "output_units": spec.output_units, "source_sha256": digest(spec.to_dict())})


@lru_cache(maxsize=1)
def li6_geometry():
    return json.loads((DEPENDENCIES / "LI6_GEOMETRY.json").read_text())


@lru_cache(maxsize=1)
def _li6_selection():
    return json.loads((DEPENDENCIES / "LI6_SELECTION_DERIVATION.json").read_text())


@lru_cache(maxsize=1)
def _li6_tensors():
    data = (DEPENDENCIES / "LI6_TMR1.i64le").read_bytes()
    if len(data) != 3 * 128 * 3 * 8:
        raise ValueError("bound Li6 TMR1 tensor dimensions differ")
    return struct.unpack("<" + "q" * (len(data) // 8), data)


def li6_edge_vectors(state=None, *, phases=None, kind=0):
    if kind not in (0, 1):
        raise ValueError("Li6 direction kind must be native or phase-erased")
    if phases is None:
        if type(state) is not int or not 0 <= state < 262144:
            raise ValueError("Li6 state is an eighteen-bit T18 phase address")
        phases = [((state >> e) & 1) + 2 * ((state >> (e + 9)) & 1) for e in range(9)]
    if len(phases) != 9 or any(type(q) is not int or not 0 <= q < 4 for q in phases):
        raise ValueError("nine Z4 phases required")
    re = tuple((1, 0, -1, 0)[q] for q in phases)
    im = tuple((0, 1, 0, -1)[q] for q in phases)
    return (tuple(abs(x) for x in re), tuple(abs(x) for x in im)) if kind else (re, im)


def site_cycle_forward(edges, *, geometry=None):
    g = li6_geometry() if geometry is None else geometry
    j = vec(edges)
    if len(j) != 9:
        raise ValueError("Li6 requires nine edge currents")
    return canonical({"sites": matvec(matrix(g["site_incidence"]), j),
                      "cycles": matvec(matrix(g["cycle_incidence"]), j)})


def site_cycle_inverse(sites, cycles, *, geometry=None, require_integer=False):
    g = li6_geometry() if geometry is None else geometry
    b, c = vec(sites), vec(cycles)
    if len(b) != len(g["site_incidence"]) or len(c) != len(g["cycle_incidence"]):
        raise ValueError("site/cycle dimensions differ from the source geometry")
    independent = b[:5] + tuple(c[i] for i in g["independent_cycle_rows"])
    inverse = tuple(tuple(Fraction(x, g["edge_inverse_denominator"]) for x in row) for row in g["edge_inverse_numerator"])
    edges = matvec(inverse, independent)
    full = site_cycle_forward(edges, geometry=g)
    valid = full == canonical({"sites": b, "cycles": c})
    if require_integer:
        valid = valid and all(x.denominator == 1 for x in edges)
    return canonical({"schema": "GEN2_JOINT_ANSWER_V1", "strategy": "LI6_SITE_CYCLE_EXACT",
                      "complete": True, "unique": valid, "member_count": int(valid),
                      "members": [edges] if valid else [], "source_lattice": "INTEGER" if require_integer else "RATIONAL",
                      "all_supplied_rows_checked": True})


def site_cycle_complex_inverse(real, imaginary, *, mask=None):
    """Join signed component inverses and enforce the admitted native edge lattice."""
    a = site_cycle_inverse(real["sites"], real["cycles"], require_integer=True)
    b = site_cycle_inverse(imaginary["sites"], imaginary["cycles"], require_integer=True)
    flags = (1,) * 9 if mask is None else tuple(mask)
    if len(flags) != 9 or any(type(x) is not int or x not in (0, 1) for x in flags):
        raise ValueError("native current mask requires nine zero/one entries")
    valid = bool(a["member_count"] and b["member_count"])
    pair = None
    if valid:
        re, im = a["members"][0], b["members"][0]
        pairs = tuple(zip(re, im))
        allowed = {(1, 0), (0, 1), (-1, 0), (0, -1)}
        valid = all(value in allowed if flag else value == (0, 0) for value, flag in zip(pairs, flags))
        if valid:
            pair = {"real": re, "imaginary": im}
    return {"schema": "GEN2_JOINT_ANSWER_V1", "strategy": "LI6_COMPLEX_SITE_CYCLE_EXACT", "complete": True,
            "unique": valid, "member_count": int(valid), "members": [pair] if valid else [],
            "source_lattice": "MASKED_Z4_UNIT_EDGE_CURRENT", "mask": list(flags)}


def _complex_pullback(row):
    zero = (0,) * len(row)
    return (tuple(row) + zero, zero + tuple(row))


def li6_construction(*, cover=3, assignment=0, rho=1, mask=3, hidden_loop=True, receiver="CIRCULATION"):
    g = li6_geometry()
    if not all(type(x) is int for x in (cover, assignment, rho, mask)) or not (0 <= cover < 5 and 0 <= assignment < 6 and 1 <= rho <= 128 and 0 <= mask < 4):
        raise ValueError("Li6 construction setting outside source domain")
    if type(hidden_loop) is not bool or receiver not in ("CIRCULATION", "ENDPOINT"):
        raise ValueError("Li6 response setting outside source domain")
    mask_values = g["masks"][mask]
    b = matrix(g["site_incidence"])
    site = tuple(tuple(value * flag for value, flag in zip(row, mask_values)) for row in b)
    instances = []
    # One-body records remain source context with their exact account, without
    # silently turning a catalog mass into a new response term.
    for one in g["one_body"]:
        instances.append({"instance_id": one["object"]["object_id"], "kind": "ONE_BODY",
                          "accounts": [{"name": "native", "amount": one["object"]["M_native"], "unit": "CATALOG_NATIVE"}],
                          "actions": [], "context": one})
    endpoint_rows = []
    for p, q in g["endpoints"]:
        endpoint_rows.append(tuple(a - z for a, z in zip(site[p], site[q])))
    current_cover = g["covers"][cover]
    for edge in current_cover["pair_edges"]:
        motif = g["pair_motifs"][edge]
        instances.append({"instance_id": "pair:" + motif["relation_id"], "kind": "TWO_OWNER",
                          "accounts": [{"name": account, "amount": motif[account], "unit": "CATALOG_" + account.upper()}
                                       for account in ("native", "observed")],
                          "actions": [{"action_id": "endpoint", "pullback": _complex_pullback(endpoint_rows[edge]),
                                       "form": [[1, 0], [0, 1]], "activation": bool(mask_values[edge]),
                                       "coefficients": {account: motif[account] for account in ("native", "observed")}}],
                          "context": motif})
    for triad in current_cover["triads"]:
        motif = g["triad_motifs"][triad]
        active = all(mask_values[e] for e in motif["edge_indices"])
        if receiver == "CIRCULATION":
            rows = [tuple(value * flag for value, flag in zip(motif["cycle_incidence"], mask_values))]
        else:
            rows = [endpoint_rows[e] for e in motif["edge_indices"]]
        instances.append({"instance_id": "triad:" + str(triad), "kind": "THREE_OWNER",
                          "accounts": [{"name": account, "amount": motif[account], "unit": "CATALOG_" + account.upper()}
                                       for account in ("native", "observed")],
                          "actions": [{"action_id": "triad:" + str(i), "pullback": _complex_pullback(row),
                                       "form": [["1/3", 0], [0, "1/3"]], "activation": bool(active),
                                       "coefficients": {account: motif[account] for account in ("native", "observed")}}
                                      for i, row in enumerate(rows)], "context": motif})
    selected_assignment = g["source_assignments"][assignment]
    tensors = _li6_tensors()
    for index, edge in enumerate(g["center_relation_indices"]):
        component = selected_assignment["relation_component_ids"][index]
        numerator = selected_assignment["native_account_numerators"][index]
        offset = (index * 128 + rho - 1) * 3
        aa, bb, cc = tensors[offset:offset + 3]
        actions = [{"action_id": "center", "pullback": _complex_pullback(endpoint_rows[edge]),
                    "form": [[aa, bb], [bb, cc]], "activation": bool(mask_values[edge]),
                    "coefficients": {"native": 8 * numerator, "observed": 8 * numerator},
                    "metadata": {"source_scale": "8_TIMES_NATIVE_ACCOUNT_NUMERATOR", "account_denominator": 16}}]
        account = {"name": "native", "amount": str(Fraction(numerator, 16)), "unit": "CATALOG_NATIVE"}
        if component == "HIDDEN_SUPPORT_9":
            account["formula"] = {"operation": "hidden_lift", "partition": 9}
            cycle = tuple(value * flag for value, flag in zip(g["cycle_incidence"][-1], mask_values))
            actions.append({"action_id": "hidden_depth_loop", "pullback": _complex_pullback(cycle),
                            "form": [["1/4", 0], [0, "1/4"]],
                            "activation": bool(hidden_loop and mask_values[1] and mask_values[4]),
                            "coefficients": {"native": "9/16", "observed": "9/16"},
                            "metadata": {"source_account_reference": "native", "formula": "p^2/144", "partition": 9}})
        instances.append({"instance_id": component, "kind": "HIDDEN_SUPPORT" if component == "HIDDEN_SUPPORT_9" else "CENTER_SOURCE",
                          "accounts": [account], "actions": actions,
                          "context": {"relation": g["relation_ids"][edge], "assignment": selected_assignment["adapter_id"]}})
    selection = _li6_selection()
    return ConstructionSpec.from_dict({"construction_id": "LI6_GRAMMAR_PROP4_V1",
        "coordinates": [part + ":" + edge for part in ("real", "imaginary") for edge in g["relation_ids"]],
        "instances": instances, "output_units": {"native": "CANDIDATE_SOURCE_ACTION", "observed": "CANDIDATE_SOURCE_ACTION"},
        "alternatives": {"selected_covers": ["COVER_03", "COVER_04"], "center_placements": g["source_assignments"],
                         "selected_states": selection["states"], "all_ties_retained": True},
        "metadata": {"cover": current_cover, "assignment": assignment, "rho": rho, "mask": g["mask_names"][mask],
                     "hidden_loop": hidden_loop, "receiver": receiver, "physical_coefficient_assigned": False}})


def _dispatch_base(operation, payload):
    operation = operation.removeprefix("GEN2_")
    if operation == "CONSTRUCTION_COMPILE":
        compiled = ConstructionSpec.from_dict(payload["source"]).compile(payload.get("context"))
        result = compiled.to_dict()
        if "values" in payload:
            result["response"] = compiled.evaluate(payload["values"])
        return result
    if operation == "CONSTRUCTION_CHANGE":
        return activation_change(payload["source"], payload["before"], payload["after"],
                                 before_context=payload.get("before_context"), after_context=payload.get("after_context"))
    if operation == "LI6_SITE_CYCLE":
        if "edges" in payload:
            return site_cycle_forward(payload["edges"])
        if "real" in payload and "imaginary" in payload:
            return site_cycle_complex_inverse(payload["real"], payload["imaginary"], mask=payload.get("mask"))
        return site_cycle_inverse(payload["sites"], payload["cycles"], require_integer=payload.get("require_integer", False))
    if operation == "LI6_CONSTRUCTION":
        source = li6_construction(**{key: payload[key] for key in ("cover", "assignment", "rho", "mask", "hidden_loop", "receiver") if key in payload})
        compiled = source.compile()
        result = {"schema": "GEN2_LI6_CONSTRUCTION_V1", "source": source.to_dict(),
                  "source_sha256": digest(source.to_dict())}
        if "state" in payload or "phases" in payload:
            real, imaginary = li6_edge_vectors(payload.get("state"), phases=payload.get("phases"), kind=payload.get("kind", 0))
            result["response"] = compiled.evaluate(real + imaginary)
            mask = li6_geometry()["masks"][payload.get("mask", 3)]
            result["site_cycle"] = {"real": site_cycle_forward(tuple(x * flag for x, flag in zip(real, mask))),
                                    "imaginary": site_cycle_forward(tuple(x * flag for x, flag in zip(imaginary, mask)))}
            result["state"] = payload.get("state")
        if payload.get("include_forms", False):
            result["compiled"] = compiled.to_dict()
        return result
    raise ValueError("unsupported GEN2 construction operation")


def dispatch(operation, payload):
    from .motion_adapters import construction_geometry
    from .boundary_information import register_ordinary
    from .write_foundation import annotate_construction
    result = register_ordinary(operation, payload,
                               construction_geometry(operation, payload, _dispatch_base(operation, payload)))
    return annotate_construction(operation, payload, result)
