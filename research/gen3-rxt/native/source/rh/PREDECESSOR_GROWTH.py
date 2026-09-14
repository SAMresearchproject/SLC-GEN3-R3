"""Source-bound RH growth calculations compiled into the shared GEN3 machine.

Python constructs index sets and operation graphs. GEN3 evaluates arithmetic,
inverse witnesses and logarithmic histories. No campaign imports or workers.
"""
from __future__ import annotations
from fractions import Fraction
from math import isqrt
import hashlib
import json
import sys

# Exact native inverse witnesses can contain thousands of decimal digits.
sys.set_int_max_str_digits(0)

VERSION = 'RH-GEN3-GROWTH-V4'
OPERATIONS = ('RH_GROWTH_TARGET', 'RH_PREFIX_PROJECT', 'RH_QUARTIC_TRANSPORT', 'RH_RESTRICTED_OPERATOR',
              'RH_GAIN_CERTIFICATE', 'RH_GROWTH_LOG', 'RH_GROWTH_RECOVER', 'RH_SOURCE_STRUCTURE', 'RH_WEIGHTED_SOURCE', 'RH_MOBIUS_SOURCE', 'RH_SOURCE_HISTORY', 'RH_GROWTH_SOURCE_PREPARE')
TARGET = {
    'original_contract': 'SAM_REVIEW/campaigns/RH_DYADIC_ODD_TRANSFER1/TARGET_AND_CONTINUATION.md',
    'projection': 'SAM_REVIEW/campaigns/RH_WEIGHTED_PREFIX_PROJECTION1/RESULT.md',
    'transport': 'SAM_REVIEW/campaigns/RH_QUARTIC_JOINT_REMAINDER1/DERIVATION.md',
    'remaining': 'SAM_REVIEW/campaigns/RH_QUARTIC_JOINT_REMAINDER1/RECURSIVE_BOUND_TARGET.md',
    'quantifier': 'For every epsilon>0, sum_original_roster[Bhat+Xhat]_+ <= C_epsilon U_j^epsilon on the SAME common unbounded sequence.',
    'constant_dependencies': 'Original fixed parameters; independent of scale and admissible stops.',
    'uniform_completed_component': 'Q(a2) <= 32(1+H_u)^4(1+8H_(s-1)); u=floor((2s-1)^(1/4)).',
    'uniform_transport_gain': 'OPEN',
    'source_structure': 'SAM_REVIEW/campaigns/RH_GEN3_STOP_STRUCTURE1/DERIVATION.md',
    'source_specific_target': 'In low divisor-defect coordinates b=epsilon, bound G_b[1,1] <= C_epsilon s^epsilon D_b[1,1] uniformly in original scale and stop.',
    'search_priority': 'Explore weighted, fourth-root, cofactor and harmonic-divisor representations; native acquired feedback selects route changes, new combinations, scales and additional stops. Weighted analysis is a starting capability, not an exclusive route.',
    'weighted_target': 'For every eta>0, V_Uj=sum_original_roster[X_adm]_+ <= C_eta U_j^eta on the SAME common unbounded sequence.',
    'completed_admission_diagonal': '0 <= D_adm <= trace(Khat) <= 2-1/s, with original tau equal to the full geometric trace budget.',
    'formula_packet': 'CURRENT_REVISION/domains/RH/source/FORMULA_PACKET_V3.json',
    'weighted_source': 'SAM_REVIEW/campaigns/RH_GEN3_FORMULA_PACKET1/WEIGHTED_CUT_DERIVATION.md',
    'finite_certificate_scope': 'Specified source-dependent operator and geometry only.',
    'completion_type': 'Auxiliary f(u+1), generally different from mu(u+1).',
}


class Graph:
    def __init__(self):
        self.nodes, self.constants = [], {}
        self.zero = self.value(0)

    def value(self, value):
        value = str(Fraction(str(value)))
        if value not in self.constants:
            node = 'n' + str(len(self.nodes))
            self.constants[value] = node
            self.nodes.append({'id': node, 'op': 'VALUE', 'value': value})
        return self.constants[value]

    def binary(self, op, left, right):
        node = 'n' + str(len(self.nodes))
        self.nodes.append({'id': node, 'op': op, 'left': left, 'right': right})
        return node

    def add(self, a, b): return self.binary('ADD', a, b)
    def sub(self, a, b): return self.binary('SUBTRACT', a, b)
    def mul(self, a, b): return self.binary('MULTIPLY', a, b)
    def div(self, a, b): return self.binary('DIVIDE', a, b)
    def sum(self, items):
        result = self.zero
        for value in items:
            result = self.add(result, value)
        return result


def cells(s):
    result = []
    for side, cuts in enumerate((range(1, s//2+1), range(s//2+1, s))):
        groups = {}
        for r in cuts:
            groups.setdefault(isqrt(r if side == 0 else s-r), []).append(r)
        result.extend({'side': side, 'k': k, 'cuts': rr} for k, rr in sorted(groups.items()))
    return result


def geometry(payload):
    s, t = payload['s'], payload['t']
    if type(s) is not int or s < 1 or s & (s-1):
        raise ValueError('s must be an original dyadic scale')
    if type(t) is not int or not 0 <= t <= s:
        raise ValueError('t must be an original stop between zero and s')
    return s, t


def project_graph(g, source, s, t):
    pref = [g.zero]
    for i in range(s):
        pref.append(g.add(pref[-1], source[i] if i < t else g.zero))
    mean = pref[-1]
    centered = {r: g.sub(pref[r], g.div(g.mul(g.value(r), mean), g.value(s))) for r in range(1, s)}
    mean_energy = g.div(g.mul(mean, mean), g.value(s))
    full = g.add(mean_energy, g.sum(g.div(g.mul(c, c), g.value(r*(s-r))) for r, c in centered.items()))
    rows, terms = [], []
    for cell in cells(s):
        weights = {r: g.div(g.value(1), g.value(r*(s-r))) for r in cell['cuts']}
        W = g.sum(weights.values())
        Z = g.sum(g.mul(w, centered[r]) for r, w in weights.items())
        terms.append(g.div(g.mul(Z, Z), W))
        rows.append(dict(cell, W=W, Z=Z))
    projected = g.add(mean_energy, g.sum(terms))
    return {'M': mean, 'Q': full, 'Qhat': projected, 'residual': g.sub(full, projected)}, rows


class GrowthSession:
    def __init__(self, runtime):
        self.runtime = runtime
        self.calls = []
        self.stages = []

    def call(self, operation, payload):
        result = self.runtime.execute(operation, payload)
        self.calls.append({'operation': operation,
                           'input_sha256': hashlib.sha256(json.dumps(payload, sort_keys=True).encode()).hexdigest()})
        return result

    def graph(self, graph):
        out = None
        for start in range(0, len(graph.nodes), 30000):
            nodes = graph.nodes[start:start+30000]
            if out is None:
                out = self.call('GEN2_SIGNED_LOG', {'nodes': nodes, 'result_id': nodes[-1]['id'], 'representation': 'RATIONAL'})
            else:
                out = self.call('GEN2_SIGNED_LOG_RESUME', {'checkpoint': out['checkpoint'], 'append_nodes': nodes, 'result_id': nodes[-1]['id']})
        if not out['complete'] or any(row['status'] != 'DEFINED' for row in out['nodes']):
            raise ValueError('RH exact graph contains an undefined operation')
        self.stages.append(out)
        return {row['id']: str(Fraction(str(row['value']))) for row in out['nodes']}, out

    def execute(self, operation, payload):
        self.calls = []
        self.stages = []
        if operation in ('RH_PREFIX_PROJECT','RH_WEIGHTED_SOURCE','RH_SOURCE_HISTORY','RH_GROWTH_SOURCE_PREPARE'):
            from .native.growth_fabric import execute
            return execute(operation,payload,self.runtime)
        if operation == 'RH_GROWTH_TARGET':
            return {'version': VERSION, 'target': TARGET, 'operations': OPERATIONS + ('RH_GROWTH_RUN', 'GEN3_RH_GROWTH_RUN'), 'paired_routine': 'GEN3-RH-GROWTH-ROUTINE-V4', 'routine_dispatch': 'RH_DOMAIN_VIA_CE'}
        binding = payload.get('source_binding')
        if not isinstance(binding, dict) or not binding:
            raise ValueError('RH growth calls require an explicit source_binding')
        if operation == 'RH_GROWTH_RECOVER':
            out = self.call('GEN2_SIGNED_LOG_RESUME', {'checkpoint': payload['checkpoint']})
            return {'version': VERSION, 'source_binding': binding, 'native': out, 'calls': self.calls}
        if operation == 'RH_GROWTH_LOG':
            # Caller supplies the ordered original history or explicitly typed assembly.
            if payload.get('history_role') not in ('ORIGINAL_ADMISSION', 'REPRESENTATION_ASSEMBLY'):
                raise ValueError('State the exact history_role')
            if Fraction(str(payload['fixed_tau'])) <= 0:
                raise ValueError('fixed_tau must be positive')
            if 'original_tau' in binding and Fraction(str(binding['original_tau'])) != Fraction(str(payload['fixed_tau'])):
                raise ValueError('Original source tau and fixed_tau differ')
            graph = Graph()
            actions = [graph.add(graph.value(payload['fixed_tau']), graph.value(point['energy'])) for point in payload['points']]
            values, native = self.graph(graph)
            if any(Fraction(values[x]) <= 0 for x in actions):
                raise ValueError('Every fixed-tau potential argument must be positive')
            log_payload = {key: payload[key] for key in ('account', 'quantity', 'source_binding', 'edges')}
            log_payload['source_binding'] = dict(binding, history_role=payload['history_role'], fixed_tau=str(payload['fixed_tau']))
            quantity = dict(payload['quantity'])
            normalization = dict(quantity.get('normalization') or {})
            if 'tau' in normalization and Fraction(str(normalization['tau'])) != Fraction(str(payload['fixed_tau'])):
                raise ValueError('Quantity normalization and fixed_tau differ')
            normalization['tau'] = str(payload['fixed_tau'])
            quantity['normalization'] = normalization
            log_payload['quantity'] = quantity
            log_payload['points'] = [{'id': point['id'], 'state': point['state'], 'action': values[x]} for point, x in zip(payload['points'], actions)]
            out = self.call('GEN3_LOG_OPEN', log_payload)
            return {'version': VERSION, 'source_binding': binding, 'history_role': payload['history_role'], 'fixed_tau': payload['fixed_tau'], 'log': out, 'native': native, 'calls': self.calls}
        if operation == 'RH_WEIGHTED_SOURCE':
            return weighted_source(self, payload)
        if operation == 'RH_MOBIUS_SOURCE':
            return mobius_source(self, payload)
        if operation == 'RH_PREFIX_PROJECT':
            s, t = geometry(payload)
            source = payload['source']
            if len(source) != s:
                raise ValueError('source must retain the full original block')
            g = Graph()
            refs, rows = project_graph(g, [g.value(x) for x in source], s, t)
            vals, out = self.graph(g)
            result = {'s': s, 't': t, 'readouts': {key: vals[ref] for key, ref in refs.items()},
                      'cells': [dict(row, W=vals[row['W']], Z=vals[row['Z']]) for row in rows]}
            if all(abs(Fraction(str(x))) <= 1 for x in source):
                if not 0 <= Fraction(vals[refs['residual']]) <= 8:
                    raise ValueError('Original unit-source projection residual exceeds its established bound')
                result['uniform_projection_residual_bound'] = '8'
        elif operation == 'RH_QUARTIC_TRANSPORT':
            s, t = geometry(payload)
            u = isqrt(isqrt(2*s-1)); A = u+1; M = (2*s-1)//(A*A)
            if A >= s:
                raise ValueError('Quartic support requires u+1<s; use direct projection at base scales')
            anchors = payload['anchors']
            if len(anchors) != M:
                raise ValueError('Supply exactly mu(1)..mu(M), M=floor((2s-1)/(u+1)^2)')
            g = Graph(); v = g.value
            # Explicitly check the source-defining divisor equations n<=M.
            equations = []
            mu = {n: v(x) for n, x in enumerate(anchors, 1)}
            for n in range(1, M+1):
                equations.append(g.sub(g.sum(mu[d] for d in range(1, n+1) if n%d == 0), v(int(n == 1))))
            S = g.sum(g.div(mu[n], v(n)) for n in range(1, u+1))
            f = {n: mu[n] for n in range(1, u+1)}
            f[A] = g.sub(g.zero, g.mul(v(A), S))
            r = {n: g.sub(g.sum(x for d, x in f.items() if n%d == 0), v(int(n == 1))) for n in range(1, (2*s-1)//A+1)}
            rr = {}
            for a in range(A, isqrt(2*s-1)+1):
                for b in range(a, (2*s-1)//a+1):
                    term = g.mul(r[a], r[b])
                    if a != b: term = g.mul(v(2), term)
                    rr[a*b] = g.add(rr.get(a*b, g.zero), term)
            c2 = {}
            for a, x in f.items():
                for b, y in f.items(): c2[a*b] = g.add(c2.get(a*b, g.zero), g.mul(x, y))
            low, high = [], []
            for n in range(s, 2*s):
                low.append(g.sum(x for k, x in c2.items() if n%k == 0))
                high.append(g.sum(g.mul(mu[m], rr[n//m]) for m in range(1, M+1) if n%m == 0 and n//m in rr))
            original = [g.sub(a, b) for a, b in zip(high, low)]
            vals, out = self.graph(g)
            from .native.growth_fabric import execute as distributed
            projections = {}
            projection_receipts = {}
            for name, source in [('original', original), ('quadratic', low), ('transport', high)]:
                projected = distributed('RH_PREFIX_PROJECT',dict(s=s,t=t,source=[vals[x] for x in source],source_binding=binding),self.runtime)
                projections[name] = projected['readouts']
                projection_receipts[name] = projected['hardware']
            if any(Fraction(vals[x]) != 0 for x in equations):
                raise ValueError('Anchor values violate the actual source divisor equations')
            result = {'s': s, 't': t, 'u': u, 'A': A, 'smaller_source_cutoff': M,
                      'f': {str(n): vals[x] for n, x in f.items()}, 'r_squared': {str(n): vals[x] for n, x in rr.items()}, 'completion_type': TARGET['completion_type'],
                      'source': [vals[x] for x in original], 'quadratic': [vals[x] for x in low], 'transport': [vals[x] for x in high],
                      'readouts': projections, 'projection_hardware': projection_receipts,
                      'uniform_component': TARGET['uniform_completed_component']}
        elif operation == 'RH_RESTRICTED_OPERATOR':
            s, t = geometry(payload)
            transport = payload['transport']
            u = isqrt(isqrt(2*s-1)); M = (2*s-1)//((u+1)**2)
            if transport.get('version') != VERSION or transport.get('s') != s or transport.get('u') != u:
                raise ValueError('Use the matching RH_QUARTIC_TRANSPORT result')
            g = Graph(); v = g.value; E = {}
            for n in range(1, M+1):
                E[n] = [v(int(n == j)) for j in range(1, u+1)] if n <= u else [g.sub(g.zero, g.sum(E[d][j] for d in range(1, n) if n%d == 0)) for j in range(u)]
            rr = {int(n): v(x) for n, x in transport['r_squared'].items()}
            raw = []
            for j in range(u):
                source = [g.sum(g.mul(E[m][j], rr[n//m]) for m in range(1, M+1) if n%m == 0 and n//m in rr) for n in range(s, 2*s)]
                refs, rows = project_graph(g, source, s, t)
                raw.append([refs['M']] + [row['Z'] for row in rows])
            denominators = [v(s)] + [row['W'] for row in rows]
            width = len(denominators); columns = []; D = []; actual = []; labels = []; N = 1
            while N <= u:
                stop = min(N, u-N+1)
                columns.append([g.div(g.add(g.sum(raw[N+i-1][k] for i in range(stop)), g.mul(v(N-stop), raw[N+stop-2][k])), v(N)) for k in range(width)])
                D.append(g.add(v(Fraction(stop, N*N)), g.div(g.sum(g.div(v(1), v(r)) for r in range(stop, N)), v(N))))
                prefix = [g.zero]
                for i in range(stop): prefix.append(g.add(prefix[-1], v(transport['f'][str(N+i)])))
                mean = prefix[-1]; actual.append(mean); labels.append({'block': N, 'stop': stop, 'coordinate': 'M'})
                for r in range(1, stop):
                    columns.append([g.sub(raw[N+r-2][k], raw[N+r-1][k]) for k in range(width)])
                    D.append(v(Fraction(1, r*(N-r))))
                    actual.append(g.sub(prefix[r], g.mul(v(Fraction(r, N)), mean)))
                    labels.append({'block': N, 'stop': stop, 'coordinate': 'C'+str(r)})
                N *= 2
            gram = [[g.sum(g.div(g.mul(a, b), d) for a, b, d in zip(columns[i], columns[j], denominators)) for j in range(u)] for i in range(u)]
            output = [g.sum(g.mul(actual[j], columns[j][k]) for j in range(u)) for k in range(width)]
            energy = g.sum(g.div(g.mul(x, x), d) for x, d in zip(output, denominators))
            input_energy = g.sum(g.mul(d, g.mul(x, x)) for d, x in zip(D, actual))
            vals, out = self.graph(g)
            result = {'s': s, 't': t, 'input_dimension': u, 'prior_input_dimension': M, 'output_dimension': width,
                      'G': [[vals[x] for x in row] for row in gram], 'D': [vals[x] for x in D],
                      'labels': labels, 'actual_coordinates': [vals[x] for x in actual],
                      'actual_output_energy': vals[energy], 'actual_input_energy': vals[input_energy],
                      'canonical_columns': [[vals[x] for x in col] for col in columns],
                      'output_denominators': [vals[x] for x in denominators],
                      'restriction': 'ACTUAL_DIVISOR_IDENTITIES_ABOVE_FOURTH_ROOT'}
        elif operation == 'RH_SOURCE_STRUCTURE':
            s, t = geometry(payload)
            operator = payload['operator']
            n = isqrt(isqrt(2*s-1))
            if operator.get('s') != s or operator.get('t') != t or operator.get('source_binding') != binding:
                raise ValueError('Source structure requires the matching source-bound operator')
            G, D, z = operator['G'], operator['D'], operator['actual_coordinates']
            if len(D) != n or len(z) != n or len(G) != n or any(len(row) != n for row in G):
                raise ValueError('Source structure dimension differs from fourth-root geometry')
            if any(Fraction(x) <= 0 for x in D) or any(Fraction(G[i][j]) != Fraction(G[j][i]) for i in range(n) for j in range(n)):
                raise ValueError('Source structure requires positive geometry and symmetric Gram')
            if len(payload['low_source']) != n:
                raise ValueError('Supply every actual low source coefficient')
            g = Graph(); v = g.value
            zz = list(map(v, z)); dd = list(map(v, D)); gg = [[v(x) for x in row] for row in G]
            low = []; labels = []; expected_D = []; offset = 0; N = 1
            while N <= n:
                stop = min(N, n-N+1); mean = zz[offset]
                cc = [g.zero] + zz[offset+1:offset+stop] + [g.mul(v(Fraction(N-stop, N)), mean)]
                low.extend(g.add(g.div(mean, v(N)), g.sub(cc[i+1], cc[i])) for i in range(stop))
                labels.append({'block': N, 'stop': stop, 'coordinate': 'M'})
                expected_D.append(Fraction(stop, N*N) + sum((Fraction(1, r*N) for r in range(stop, N)), Fraction(0)))
                for r in range(1, stop):
                    labels.append({'block': N, 'stop': stop, 'coordinate': 'C'+str(r)})
                    expected_D.append(Fraction(1, r*(N-r)))
                offset += stop; N *= 2
            if operator['labels'] != labels or list(map(Fraction, D)) != expected_D:
                raise ValueError('Source structure must retain the original canonical input geometry')
            defects = [g.sum(low[d-1] for d in range(1, m+1) if m%d == 0) for m in range(1, n+1)]
            total = g.sum(g.mul(g.mul(zz[i], gg[i][j]), zz[j]) for i in range(n) for j in range(n))
            diagonal = g.sum(g.mul(gg[i][i], g.mul(zz[i], zz[i])) for i in range(n))
            energy = g.sum(g.mul(dd[i], g.mul(zz[i], zz[i])) for i in range(n))
            cross = g.sub(total, diagonal)
            refs = {'actual_input_energy': energy, 'actual_output_energy': total,
                    'diagonal_energy': diagonal, 'cross_energy': cross,
                    'signed_cancellation_energy': g.sub(diagonal, total),
                    'actual_gain': g.div(total, energy), 'diagonal_gain': g.div(diagonal, energy),
                    'cross_gain': g.div(cross, energy)}
            vals, out = self.graph(g)
            actual_low = [vals[x] for x in low]; defect_values = [vals[x] for x in defects]
            if list(map(Fraction, actual_low)) != list(map(Fraction, payload['low_source'])):
                raise ValueError('Canonical coordinates differ from the actual low source')
            if defect_values != ['1'] + ['0']*(n-1):
                raise ValueError('Actual source must satisfy low divisor identities b=epsilon')
            readouts = {key: vals[node] for key, node in refs.items()}
            if any(Fraction(readouts[key]) != Fraction(operator[key]) for key in ('actual_input_energy', 'actual_output_energy')):
                raise ValueError('Source contraction differs from retained operator energy')
            result = {'s': s, 't': t, 'input_dimension': n, 'actual_low_source': actual_low,
                      'low_divisor_coordinates': defect_values, 'source_line': 'b=epsilon',
                      'readouts': readouts, 'source_identity_status': 'PASS',
                      'scope': 'Exact actual-source contraction at this original scale and stop; uniform source gain remains open.'}
        elif operation == 'RH_GAIN_CERTIFICATE':
            G, D, gain = payload['G'], payload['D'], payload['gain']
            n = len(D)
            if not n or len(G) != n or any(len(row) != n for row in G):
                raise ValueError('Gain certificate dimensions differ')
            if any(Fraction(str(x)) <= 0 for x in D) or Fraction(str(gain)) <= 0:
                raise ValueError('Positive input energy weights and candidate gain required')
            if any(Fraction(str(G[i][j])) != Fraction(str(G[j][i])) for i in range(n) for j in range(n)):
                raise ValueError('Output Gram must be symmetric')
            g = Graph(); v = g.value
            matrix = [[g.sub(g.mul(v(gain), v(D[i])) if i == j else g.zero, v(abs(Fraction(str(G[i][j]))))) for j in range(n)] for i in range(n)]
            vals, constructed = self.graph(g)
            inverse = self.call('GEN2_READOUT_INVERSE', {'strategy': 'linear', 'matrix': [[vals[x] for x in row] for row in matrix], 'observed': list(map(str, D))})
            if not inverse['unique'] or any(Fraction(x) <= 0 for x in inverse['particular']):
                return {'version': VERSION, 'status': 'NO_POSITIVE_WEIGHT_CERTIFICATE', 'source_binding': binding,
                        'gain': gain, 'inverse': inverse, 'native': constructed, 'calls': self.calls, 'target': TARGET}
            w = [str(Fraction(str(x))) for x in inverse['particular']]; g = Graph(); v = g.value
            margins = [g.sub(g.mul(g.mul(v(gain), v(D[i])), v(w[i])), g.sum(g.mul(v(abs(Fraction(str(G[i][j])))), v(w[j])) for j in range(n))) for i in range(n)]
            vals, out = self.graph(g)
            if any(Fraction(vals[x]) != Fraction(str(D[i])) for i, x in enumerate(margins)):
                raise ValueError('Exact positive-weight inverse identity differs')
            result = {'gain': str(gain), 'weights': w, 'inverse': inverse, 'input_dimension': n,
                      'margins': [vals[x] for x in margins], 'scope': TARGET['finite_certificate_scope']}
        else:
            raise ValueError('Unknown RH growth operation: ' + operation)
        return dict(result, version=VERSION, status='PASS', source_binding=binding,
                    target=TARGET, native=out, prior_native_stages=self.stages[:-1], calls=self.calls)


def mobius_source(engine, payload):
    """Native divisor recurrence; Python supplies divisibility indices only."""
    limit=payload['limit']
    if type(limit) is not int or limit<1:
        raise ValueError('limit must be a positive integer')
    divisors=[[] for _ in range(limit+1)]
    for d in range(1,limit//2+1):
        for n in range(2*d,limit+1,d):divisors[n].append(d)
    g=Graph();mu={1:g.value(1)}
    for n in range(2,limit+1):mu[n]=g.sub(g.zero,g.sum(mu[d] for d in divisors[n]))
    values,native=engine.graph(g)
    source={str(n):values[node] for n,node in mu.items()}
    if any(x not in ('-1','0','1') for x in source.values()):raise ValueError('Source recurrence returned a non-Mobius value')
    return dict(version=VERSION,status='PASS',source_binding=payload['source_binding'],mu=source,
                definition='mu(1)=1; sum_(d|n)mu(d)=0 for n>1',native=native,calls=engine.calls)


def weighted_source(engine, payload):
    """Original fixed cut geometry and O(s) native signed kernel contraction."""
    s,t=geometry(payload);source=payload['source']
    if len(source)!=s or any(str(Fraction(str(x))) not in ('-1','0','1') for x in source):
        raise ValueError('Retain a full signed Mobius block with entries -1,0,1')
    if payload.get('cells') is not None and payload['cells']!=cells(s):
        raise ValueError('Weighted source uses the original fixed cut cells')
    g=Graph();v=g.value;mu=[v(x) for x in source]
    projection,cell_geometry=project_graph(g,mu,s,t)
    pref=[g.zero];counts=[g.zero]
    for x in mu:
        pref.append(g.add(pref[-1],x));counts.append(g.add(counts[-1],g.mul(x,x)))
    checks=[];refs=[];tail_factor=g.div(v(1),v(s))
    for index,cell in enumerate(cell_geometry):
        cuts=cell['cuts'];l,h=cuts[0],cuts[-1]
        w={r:g.div(v(1),v(r*(s-r))) for r in cuts};W=cell['W']
        offset=g.div(g.sum(g.mul(v(r),w[r]) for r in cuts),v(s))
        before=g.sub(W,offset);after=g.sub(g.zero,offset);suffix=g.zero;beta={}
        for r in reversed(cuts[1:]):
            suffix=g.add(suffix,w[r]);beta[r-1]=g.sub(suffix,offset)
        before2=g.mul(before,before);after2=g.mul(after,after);inside=list(range(l,min(t,h)))
        z=g.sum([g.mul(pref[min(t,l)],before),g.mul(g.sub(pref[t],pref[min(t,h)]),after),
                 *[g.mul(mu[i],beta[i]) for i in inside]])
        checks.append(g.sub(z,cell['Z']))
        diagonal=g.div(g.sum([g.mul(counts[min(t,l)],before2),g.mul(g.sub(counts[t],counts[min(t,h)]),after2),
                  *[g.mul(g.mul(mu[i],mu[i]),g.mul(beta[i],beta[i])) for i in inside]]),W)
        trace=g.div(g.sum([g.mul(v(l),before2),g.mul(v(s-h),after2),*[g.mul(b,b) for b in beta.values()]]),W)
        energy=g.div(g.mul(z,z),W)
        region='POST_STOP' if l>=t else ('PRE_STOP' if h<t else 'STRADDLING')
        if region=='POST_STOP':
            factor=g.div(before2,W);tail_factor=g.add(tail_factor,factor)
            checks.extend([g.sub(z,g.mul(pref[t],before)),g.sub(diagonal,g.mul(counts[t],factor))])
        refs.append(dict(cell=index,l=l,h=h,region=region,energy=energy,diagonal=diagonal,
                         cross=g.sub(energy,diagonal),trace=trace))
    mean=g.div(g.mul(pref[t],pref[t]),v(s));mean_d=g.div(counts[t],v(s))
    energy=g.add(mean,g.sum(r['energy'] for r in refs));diagonal=g.add(mean_d,g.sum(r['diagonal'] for r in refs))
    cross=g.sub(energy,diagonal);trace=g.add(v(1),g.sum(r['trace'] for r in refs));full=g.sub(v(2),g.div(v(1),v(s)))
    active=g.sum(r['energy'] for r in refs if r['region']!='POST_STOP')
    known=g.mul(g.mul(pref[t],pref[t]),tail_factor)
    known_cross=g.mul(g.sub(g.mul(pref[t],pref[t]),counts[t]),tail_factor)
    active_cross=g.sum(r['cross'] for r in refs if r['region']!='POST_STOP')
    checks.extend([g.sub(energy,projection['Qhat']),g.sub(energy,g.add(known,active)),g.sub(cross,g.add(known_cross,active_cross))])
    margins=[diagonal,g.sub(trace,diagonal),g.sub(full,trace),projection['residual'],g.sub(v(8),projection['residual'])]
    readouts=dict(Q=projection['Q'],Qhat=energy,residual=projection['residual'],M=pref[t],N=counts[t],
        D_adm=diagonal,X_adm=cross,mean_energy=mean,mean_diagonal=mean_d,mean_cross=g.sub(mean,mean_d),
        projected_trace=trace,full_trace=full,known_tail_factor=tail_factor,known_mean_tail_energy=known,
        active_energy=active,known_mean_tail_cross=known_cross,active_cross=active_cross,
        active_to_one_plus_mean=g.div(active,g.add(v(1),mean)))
    regions={region:{key:g.sum(r[key] for r in refs if r['region']==region) for key in ('energy','diagonal','cross','trace')}
             for region in ('PRE_STOP','STRADDLING','POST_STOP')}
    values,native=engine.graph(g)
    if any(Fraction(values[x])!=0 for x in checks):raise ValueError('Weighted source identity failed')
    if any(Fraction(values[x])<0 for x in margins):raise ValueError('Weighted source trace/residual margin failed')
    result_cells=[{key:(value if key in ('cell','l','h','region') else values[value]) for key,value in row.items()} for row in refs]
    # Host locates exact extrema; native differences certify all returned ties.
    maximum=max((Fraction(r['energy']) for r in result_cells),default=Fraction(0))
    cert=Graph();cert_refs=[cert.sub(cert.value(maximum),cert.value(r['energy'])) for r in result_cells]
    positive=cert.value(max(Fraction(0),Fraction(values[cross])))
    cert_refs.extend([cert.sub(positive,cert.value(values[cross])),positive,
                      cert.sub(cert.value(values[energy]),positive),
                      cert.sub(cert.add(positive,cert.value(values[full])),cert.value(values[energy]))])
    cv,cn=engine.graph(cert)
    if any(Fraction(cv[x])<0 for x in cert_refs):raise ValueError('Exact extremum certificate failed')
    return dict(version=VERSION,status='PASS',s=s,t=t,source_binding=payload['source_binding'],
        readouts={**{key:values[node] for key,node in readouts.items()},'positive_X':cv[positive]},
        regions={region:{key:values[node] for key,node in rr.items()} for region,rr in regions.items()},
        cells=result_cells,largest_cells=[r['cell'] for r in result_cells if Fraction(r['energy'])==maximum],
        exact_equalities=len(checks),nonnegative_margins=len(margins)+len(cert_refs),
        native=native,maximum_certificate=cn,calls=engine.calls,
        source_contract='Actual source supplied with explicit provenance; operation checks signed alphabet and original fixed geometry.',
        uniform_bound_status='OPEN')
