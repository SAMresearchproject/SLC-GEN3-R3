"""Exact cumulative quarter-turn approximation to the golden-angle schedule.

The native sequence is a deterministic approximation. Every requested target
and its exact residual remain present; no new T18 phase resolution is implied.
"""
from decimal import Decimal, localcontext
from fractions import Fraction
from math import isqrt, lcm


def _fraction(value):
    if type(value) not in (int, str, Fraction):
        raise ValueError("Quadratic coefficients require exact integers or rationals")
    return Fraction(value)


def sqrt5_sign(a, b):
    """Return the exact sign of a + b sqrt(5), with rational a and b."""
    a, b = _fraction(a), _fraction(b)
    if b == 0:
        return (a > 0) - (a < 0)
    if a == 0:
        return (b > 0) - (b < 0)
    if (a > 0) == (b > 0):
        return 1 if a > 0 else -1
    difference = a * a - 5 * b * b
    comparison = (difference > 0) - (difference < 0)
    return comparison if a > 0 else -comparison


def compare_sqrt5(a, b, c=0, d=0):
    """Compare a + b sqrt(5) with c + d sqrt(5), exactly."""
    return sqrt5_sign(_fraction(a) - _fraction(c), _fraction(b) - _fraction(d))


def sqrt5_floor(a, b):
    """Floor a + b sqrt(5) using an isqrt enclosure and exact comparisons."""
    a, b = _fraction(a), _fraction(b)
    if b == 0:
        return a.numerator // a.denominator
    denominator = lcm(a.denominator, b.denominator)
    integer_a = a.numerator * (denominator // a.denominator)
    integer_b = b.numerator * (denominator // b.denominator)
    scale = abs(integer_b) + 1
    lower_root = isqrt(5 * scale * scale)
    # lower_root/scale < sqrt(5) < (lower_root+1)/scale.
    # Multiplication by negative integer_b reverses this enclosure.
    root_endpoint = lower_root if integer_b > 0 else lower_root + 1
    lower_numerator = integer_a * scale + integer_b * root_endpoint
    result = lower_numerator // (denominator * scale)
    # The enclosure width is |integer_b|/(denominator*scale) < 1.
    if compare_sqrt5(a, b, result + 1, 0) >= 0:
        result += 1
    if not (compare_sqrt5(a, b, result, 0) >= 0
            and compare_sqrt5(a, b, result + 1, 0) < 0):
        raise ArithmeticError("Exact square-root floor enclosure failed")
    return result


def _nonnegative_integer(value, label):
    if type(value) is not int or value < 0:
        raise ValueError(label + " must be a nonnegative integer")
    return value


def quarter_count(index):
    """K_n = floor(6n - 2n sqrt(5) + 1/2), exact nearest quarter count."""
    index = _nonnegative_integer(index, "Macro index")
    return sqrt5_floor(Fraction(12 * index + 1, 2), -2 * index)


def packet_quarters(index):
    """The exact one/two Write count of a positive-index logical packet."""
    if type(index) is not int or index < 1:
        raise ValueError('Packet index must be a positive integer')
    count = quarter_count(index) - quarter_count(index - 1)
    if count not in (1, 2):
        raise ArithmeticError('Native golden packet must contain one or two quarter Writes')
    return count


def packet_target(index, *, direction=1, initial_phase=0):
    """Exact signed requested phase and residual for one role's turn account.

    Additional partner Writes remain in the shared native phase history; they
    are not silently counted as this role's designated golden turn account.
    """
    count = packet_quarters(index)
    if type(direction) is not int or direction not in (-1, 1):
        raise ValueError('Golden role direction must be -1 or +1')
    if type(initial_phase) is not int or initial_phase not in range(4):
        raise ValueError('Initial native role phase must be in Z4')
    total = quarter_count(index)
    a = direction * (Fraction(3 * index, 2) - Fraction(total, 4))
    b = direction * Fraction(-index, 2)
    bounded = compare_sqrt5(a, b, Fraction(-1, 8)) >= 0 and compare_sqrt5(a, b, Fraction(1, 8)) <= 0
    if not bounded:
        raise ArithmeticError('Signed golden target residual exceeds its exact quarter-grid bound')
    return {'packet': index, 'packet_quarters': count, 'direction': direction,
            'signed_cumulative_quarters': direction * total,
            'target_phase_turns': _pair(Fraction(initial_phase, 4) + direction * Fraction(3 * index, 2),
                                       direction * Fraction(-index, 2)),
            'scheduled_phase_turns': str(Fraction(initial_phase + direction * total, 4)),
            'residual_target_minus_scheduled_turns': _pair(a, b),
            'exact_residual_bound_turns': '1/8', 'residual_bound_verified': bounded}


def initial_cursor(packets):
    packets = _nonnegative_integer(packets, 'Packet count')
    return {'packet': 1, 'role': 0, 'offset': 0, 'completed_packets': 0,
            'native_writes': 0, 'complete': packets == 0}


def peek_event(intent, cursor):
    """Return the next declared event and its exact role/packet association."""
    if cursor['complete']:
        return None
    role = intent['roles'][cursor['role']]
    count = packet_quarters(cursor['packet'])
    offset = cursor['offset']
    event = role['event'] if offset < count else role['after_packet'][offset - count]
    return {'step': cursor['native_writes'] + 1, 'packet': cursor['packet'],
            'role_id': role['role_id'], 'role_index': cursor['role'],
            'offset': offset, 'packet_quarters': count,
            'kind': 'TURN' if offset < count else 'AFTER_PACKET', 'event': event}


def advance_cursor(intent, cursor):
    """Advance exactly one native Write, including midpacket partner progress."""
    if cursor['complete']:
        raise ValueError('Completed golden cursor has no next event')
    result = dict(cursor)
    role = intent['roles'][result['role']]
    result['offset'] += 1
    result['native_writes'] += 1
    if result['offset'] == packet_quarters(result['packet']) + len(role['after_packet']):
        result['offset'] = 0
        result['role'] += 1
        if result['role'] == len(intent['roles']):
            result['role'] = 0
            result['completed_packets'] = result['packet']
            result['packet'] += 1
            result['complete'] = result['packet'] > intent['packets']
    return result


def _pair(a, b):
    return {"rational": str(_fraction(a)), "sqrt5": str(_fraction(b))}


def _degree_diagnostic(a, b):
    """Decimal text for display only; no schedule decision consumes it."""
    a, b = _fraction(a), _fraction(b)
    with localcontext() as context:
        context.prec = 40
        value = (Decimal(a.numerator) / Decimal(a.denominator)
                 + Decimal(b.numerator) / Decimal(b.denominator) * Decimal(5).sqrt()) * 360
        return format(value, ".24f")


def build_schedule(steps=256, *, coordinate=1, include_diagnostics=False):
    """Return the complete source-bound schedule, residuals, and baseline.

    Every row is one requested golden-angle macro step represented by one or
    two native positive quarter-turn Writes. No floating value drives rounding.
    """
    steps = _nonnegative_integer(steps, "Step count")
    if steps == 0:
        raise ValueError("A schedule requires at least one macro step")
    if type(coordinate) is not int or not 0 <= coordinate <= 8:
        raise ValueError("The declared T18 coordinate must be an integer from 0 to 8")
    if type(include_diagnostics) is not bool:
        raise ValueError("include_diagnostics must be boolean")
    previous = 0
    rows = []
    packet_counts = {1: 0, 2: 0}
    max_absolute_residual = (Fraction(), Fraction())
    max_absolute_residual_indices = []
    for index in range(1, steps + 1):
        count = quarter_count(index)
        packet_count = count - previous
        if packet_count not in (1, 2):
            raise ArithmeticError("Golden-angle nearest-quarter packet was not one or two Writes")
        packet_counts[packet_count] += 1
        target_a, target_b = Fraction(3 * index, 2), Fraction(-index, 2)
        residual_a, residual_b = target_a - Fraction(count, 4), target_b
        lower_ok = compare_sqrt5(residual_a, residual_b, Fraction(-1, 8), 0) >= 0
        upper_ok = compare_sqrt5(residual_a, residual_b, Fraction(1, 8), 0) <= 0
        if not (lower_ok and upper_ok):
            raise ArithmeticError("Exact one-eighth-turn residual certificate failed")
        residual_sign = sqrt5_sign(residual_a, residual_b)
        absolute_residual = (residual_sign * residual_a, residual_sign * residual_b)
        comparison = compare_sqrt5(*absolute_residual, *max_absolute_residual)
        if comparison > 0:
            max_absolute_residual = absolute_residual
            max_absolute_residual_indices = [index]
        elif comparison == 0:
            max_absolute_residual_indices.append(index)
        row = {
            "macro_index": index,
            "target_turns": _pair(target_a, target_b),
            "native_cumulative_quarters": count,
            "native_cumulative_turns": str(Fraction(count, 4)),
            "packet_quarters": packet_count,
            "packet": [f"W{coordinate}+"] * packet_count,
            "residual_target_minus_native_turns": _pair(residual_a, residual_b),
            "residual_sign": residual_sign,
            "exact_residual_bound_turns": "1/8",
            "residual_bound_verified": lower_ok and upper_ok,
            "fixed_two_quarter_baseline_cumulative_quarters": 2 * index,
            "fixed_two_quarter_baseline_residual_turns": _pair(index, Fraction(-index, 2)),
        }
        if include_diagnostics:
            row["diagnostic_degrees"] = {
                "target": _degree_diagnostic(target_a, target_b),
                "residual": _degree_diagnostic(residual_a, residual_b),
                "fixed_two_quarter_baseline_residual": _degree_diagnostic(index, Fraction(-index, 2)),
            }
        rows.append(row)
        previous = count
    result = {
        "schema": "GEN2_GOLDEN_TARGET_CUMULATIVE_QUARTER_SCHEDULE_V1",
        "interpretation": "DETERMINISTIC_NATIVE_SEQUENCE_APPROXIMATION_WITH_EXACT_TARGET_AND_RESIDUAL",
        "target_alpha_turns": _pair(Fraction(3, 2), Fraction(-1, 2)),
        "target_mean_angle_degrees": _pair(540, -180),
        "rounding_law": "K_n=floor(6*n-2*n*sqrt(5)+1/2)",
        "decision_arithmetic": "EXACT_RATIONAL_AND_INTEGER_SQRT_ENCLOSURE",
        "tie_rule": "No half-integer tie for n>0 because sqrt(5) has a nonzero rational coefficient",
        "steps": steps,
        "coordinate": coordinate,
        "native_event": f"W{coordinate}+",
        "native_phase_resolution_turns": "1/4",
        "native_total_quarters": previous,
        "native_mean_angle_degrees": str(Fraction(90 * previous, steps)),
        "one_quarter_packets": packet_counts[1],
        "two_quarter_packets": packet_counts[2],
        "maximum_absolute_residual_turns": _pair(*max_absolute_residual),
        "maximum_absolute_residual_macro_indices": max_absolute_residual_indices,
        "all_exact_residual_bounds_passed": all(row["residual_bound_verified"] for row in rows),
        "fixed_two_quarter_baseline": {
            "quarters_per_step": 2,
            "native_mean_angle_degrees": "180",
            "residual_slope_target_minus_native_turns_per_step": _pair(1, Fraction(-1, 2)),
            "residual_slope_target_minus_native_degrees_per_step": _pair(360, -180),
            "endpoint_residual_turns": _pair(steps, Fraction(-steps, 2)),
        },
        "rows": rows,
    }
    if include_diagnostics:
        result["diagnostic_target_mean_angle_degrees"] = _degree_diagnostic(Fraction(3, 2), Fraction(-1, 2))
        result["diagnostic_maximum_absolute_residual_degrees"] = _degree_diagnostic(*max_absolute_residual)
    return result
