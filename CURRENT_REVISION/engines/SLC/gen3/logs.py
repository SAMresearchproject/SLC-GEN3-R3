"""Typed, unfactored exact log accounts; no serialization inside the edge loop.

ln is strictly monotone on positive rationals, so the whole ratio determines
direction. Multiplication of positive arguments is exact logarithmic addition.
Source states, signed values and gaps retain their separate meanings.
"""
from copy import deepcopy
from fractions import Fraction
from ..gen2.exact import canonical, rational
from ..gen2.history_summary import _admit_source, _point, _edge
try:
    from flint import fmpq as _FastRatio
except ImportError:
    _FastRatio = None


def ratio(value):
    if _FastRatio is not None:
        if isinstance(value, _FastRatio): return value
        if isinstance(value, Fraction): return _FastRatio(value.numerator, value.denominator)
        return _FastRatio(value)
    return rational(value)


def ratio_json(value):
    if _FastRatio is not None and isinstance(value, _FastRatio):
        return int(value.numerator) if value.denominator == 1 else str(value)
    return canonical(value)


def log_value(argument):
    argument = ratio(argument)
    if argument <= 0:
        raise ValueError('A logarithmic argument must be strictly positive')
    return {'type': 'EXACT_LOG_POSITIVE_RATIONAL', 'argument': ratio_json(argument),
            'sign': (argument > 1) - (argument < 1)}


class Segment:
    def __init__(self, point):
        self.first = self.last = point['id']
        self.initial = self.final = ratio(point['action'])
        self.up = self.down = self.maximum = ratio(1)
        self.ties = [self.first]
        self.edges = 0

    def advance(self, point):
        value = ratio(point['action'])
        delta = value / self.final
        if delta > 1:
            self.up *= delta
        elif delta < 1:
            self.down /= delta
        net = value / self.initial
        if net > self.maximum:
            self.maximum, self.ties = net, [point['id']]
        elif net == self.maximum:
            self.ties.append(point['id'])
        self.last, self.final = point['id'], value
        self.edges += 1

    def snapshot(self):
        return {'first': self.first, 'last': self.last,
            **{key: ratio_json(getattr(self,key)) for key in ('initial','final','up','down','maximum')},
            'ties': list(self.ties), 'edges': self.edges}

    @classmethod
    def restore(cls, row):
        obj = object.__new__(cls)
        obj.__dict__.update(row)
        for key in ('initial', 'final', 'up', 'down', 'maximum'):
            setattr(obj, key, ratio(row[key]))
        return obj

    def readout(self):
        net = self.final / self.initial
        if self.up / self.down != net:
            raise AssertionError('Exact rise/fall and endpoint ratio disagree')
        return {'first_point': self.first, 'last_point': self.last,
            'initial_action': ratio_json(self.initial), 'final_action': ratio_json(self.final),
            'U': log_value(self.up), 'D': log_value(self.down),
            'V': log_value(self.up * self.down), 'L': log_value(net),
            'net': log_value(net), 'M': log_value(self.maximum),
            'maximizing_points': list(self.ties), 'edge_count': self.edges}


class LogAccount:
    def __init__(self, quantity, source_binding):
        self.quantity = _admit_source(quantity, source_binding)
        self.source_binding = canonical(source_binding)
        self.points, self.edges = set(), set()
        self.first = self.last = None
        self.segments, self.unavailable = [], []
        self.chunks = []
        self.pending = []

    @staticmethod
    def positive(point):
        return point['status'] == 'OBSERVED' and rational(point['action']) > 0

    def append(self, raw_points, raw_edges):
        # Admit the whole suffix before changing live state. A rejected batch
        # cannot leave half an event or half a source account committed.
        if not isinstance(raw_points, list) or not isinstance(raw_edges, list):
            raise ValueError('Ordered source points and edges must be lists')
        points = [_point(p) for p in raw_points]
        needed = len(points) if self.last is not None else max(0, len(points) - 1)
        if len(raw_edges) != needed or (self.last is None and not points):
            raise ValueError('Supply the original point and every connecting source edge')
        ids, eids, edges = set(), set(), []
        prior = self.last
        for point in points:
            if point['id'] in self.points or point['id'] in ids:
                raise ValueError('A point occurrence ID cannot be reused')
            ids.add(point['id'])
            if prior is not None:
                edge = _edge(raw_edges[len(edges)], prior, point)
                if edge['id'] in self.edges or edge['id'] in eids:
                    raise ValueError('An edge occurrence ID cannot be reused')
                eids.add(edge['id']); edges.append(edge)
            prior = point
        for point in points:
            if self.first is None:
                self.first = point
            if self.positive(point):
                if self.last is not None and self.positive(self.last):
                    self.segments[-1].advance(point)
                else:
                    self.segments.append(Segment(point))
            else:
                self.unavailable.append(point['id'])
            self.last = point
        self.points.update(ids); self.edges.update(eids)
        if points:
            self.pending.append({'points': points, 'edges': edges})
        return needed

    def readout(self):
        defined = len(self.segments) == 1 and not self.unavailable
        return {'schema': 'GEN3_LOG_EXECUTION_READOUT_V1',
            'status': 'DEFINED' if defined else 'UNDEFINED_GAPS',
            'quantity': deepcopy(self.quantity), 'source_binding': deepcopy(self.source_binding),
            'point_count': len(self.points), 'edge_count': len(self.edges),
            'summary': self.segments[0].readout() if defined else {
                **{k: None for k in ('U', 'D', 'V', 'L', 'net', 'M')},
                'unavailable_points': list(self.unavailable),
                'segments': [s.readout() for s in self.segments]},
            'normalization': {'kind': 'ORIGINAL_POSITIVE_SOURCE_RATIO',
                'reference_point': self.first['id'] if self.first else None},
            'identities': {'U_minus_D_equals_L': defined, 'U_plus_D_equals_V': defined},
            'full_history_retained': True, 'V_is_universal_objective': False}

    def persist(self, store):
        for chunk in self.pending:
            self.chunks.append(store.put({'type': 'source_history_chunk', **chunk}))
        self.pending.clear()
        return store.put({'type': 'log_account', 'quantity': self.quantity,
            'source_binding': self.source_binding, 'first': self.first, 'last': self.last,
            'segments': [s.snapshot() for s in self.segments],
            'unavailable': self.unavailable, 'point_count': len(self.points),
            'edge_count': len(self.edges), 'chunks': self.chunks})

    @classmethod
    def restore(cls, store, ref):
        # Called only after the root and complete object closure authenticate.
        row = store.get(ref)
        obj = cls(row['quantity'], row['source_binding'])
        obj.first, obj.last = row['first'], row['last']
        obj.segments = [Segment.restore(s) for s in row['segments']]
        obj.unavailable, obj.chunks = row['unavailable'], row['chunks']
        for chunk in obj.chunks:
            part = store.get(chunk)
            obj.points.update(p['id'] for p in part['points'])
            obj.edges.update(e['id'] for e in part['edges'])
        if len(obj.points) != row['point_count'] or len(obj.edges) != row['edge_count']:
            raise ValueError('Authenticated history index differs')
        return obj

    def history(self, store=None):
        points, edges = [], []
        for ref in self.chunks:
            row = store.get(ref)
            shared = bool(points and row['points'] and points[-1] == row['points'][0])
            points.extend(row['points'][int(shared):]); edges.extend(row['edges'])
        for row in self.pending:
            shared = bool(points and row['points'] and points[-1] == row['points'][0])
            points.extend(row['points'][int(shared):]); edges.extend(row['edges'])
        return {'quantity': deepcopy(self.quantity), 'source_binding': deepcopy(self.source_binding),
                'points': deepcopy(points), 'edges': deepcopy(edges)}

    @classmethod
    def compose(cls, left, right):
        if left.quantity != right.quantity or left.source_binding != right.source_binding:
            raise ValueError('Compose one identical source quantity, frame and reference account')
        if left.last != right.first:
            raise ValueError('Composed chunks must share the complete same boundary occurrence')
        if left.unavailable or right.unavailable or len(left.segments)!=1 or len(right.segments)!=1:
            raise ValueError('Compose positive segments explicitly when an account contains gaps')
        if left.points & right.points != {left.last['id']} or left.edges & right.edges:
            raise ValueError('Chunk occurrences overlap beyond their shared boundary')
        out=cls(left.quantity,left.source_binding)
        out.first,out.last=deepcopy(left.first),deepcopy(right.last)
        out.points=left.points | right.points;out.edges=left.edges | right.edges
        a,b=left.segments[0],right.segments[0]
        segment=Segment(out.first);segment.last=b.last;segment.final=b.final
        segment.up=a.up*b.up;segment.down=a.down*b.down;segment.edges=a.edges+b.edges
        shifted=b.maximum*a.final/a.initial
        segment.maximum=max(a.maximum,shifted)
        segment.ties=(list(a.ties) if a.maximum>shifted else list(b.ties) if shifted>a.maximum
                      else list(dict.fromkeys(a.ties+b.ties)))
        out.segments=[segment]
        # Flush order is explicit: shared immutable chunks stay referenced, and
        # pending source data is retained in the same order without re-summarizing.
        if left.pending and right.chunks:
            raise ValueError('Commit the left account before composing it with committed right chunks')
        out.chunks=list(left.chunks)+list(right.chunks)
        out.pending=deepcopy(left.pending+right.pending)
        return out
