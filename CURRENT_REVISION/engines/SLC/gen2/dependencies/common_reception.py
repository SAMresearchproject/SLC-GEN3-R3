"""One-event direct-sum reception and a branching, observation-only inverse."""
from dataclasses import dataclass

LANES = ('SIGNED_PHASE', 'AXIS_OCCUPANCY')
RELATIONS = ('N100_EDGE_002', 'N100_EDGE_006', 'N100_EDGE_084')
CHANNELS = ('forward_amplitude', 'reverse_amplitude')
SLOTS = (1, 4, 7)
PHASE = ((1, 0), (0, 1), (-1, 0), (0, -1))
VIEWS = ('JOINT', 'SIGNED', 'OCCUPANCY', 'ENDPOINTS', 'WRONG_POST_ABS')


def require(ok, message):
    if not ok:
        raise ValueError(message)


def encode(q):
    return sum((v & 1) << s | (v >> 1) << (s+9) for v, s in zip(q, SLOTS, strict=True))


def source_lift(q):
    return tuple(PHASE[v][side] for side in (0, 1) for v in q)


@dataclass(frozen=True)
class Frame:
    signed: tuple
    occupancy: tuple

    def __post_init__(self):
        for lane in (self.signed, self.occupancy):
            require(type(lane) is tuple and len(lane) == 16 and
                    all(type(x) is int for x in lane), 'Reception lane requires sixteen exact integers')

    def payload(self):
        return {LANES[0]: list(self.signed), LANES[1]: list(self.occupancy)}

    @classmethod
    def admit(cls, payload):
        require(type(payload) is dict and set(payload) == set(LANES), 'Missing or extra reception field')
        require(all(type(payload[k]) in (list, tuple) for k in LANES), 'Wrong reception container')
        return cls(tuple(payload[LANES[0]]), tuple(payload[LANES[1]]))


class CurrentReception:
    """Current state only; the caller owns any chronological research record."""
    __slots__ = ('current',)

    def __init__(self):
        self.current = None

    def receive(self, payload):
        next_frame = Frame.admit(payload)
        self.current = next_frame
        return next_frame


def common_reception(h, templates):
    """Both source lanes are made from this same immutable native six-vector."""
    require(len(h) == 6 and all(type(x) is int for x in h), 'Invalid native lift')
    output = [[], []]
    for channel in CHANNELS:
        for k in range(4):
            sums = [[0, 0], [0, 0]]
            for j, relation in enumerate(RELATIONS):
                x, y = templates[relation][channel][k]
                for lane, (a, b) in enumerate(((h[j], h[j+3]), (abs(h[j]), abs(h[j+3])))):
                    sums[lane][0] += a*x-b*y
                    sums[lane][1] += a*y+b*x
            for lane in (0, 1):
                output[lane].extend(sums[lane])
    return Frame(tuple(output[0]), tuple(output[1]))


def difference(after, before):
    return (tuple(a-b for a, b in zip(after.signed, before.signed, strict=True)),
            tuple(a-b for a, b in zip(after.occupancy, before.occupancy, strict=True)))


def phase_path(initial, direction, word):
    q = list(initial)
    states = [tuple(q)]
    for j in word:
        q[j] = (q[j]+direction) % 4
        states.append(tuple(q))
    return tuple(states)


def contact(q):
    p = [PHASE[v] for v in q]
    dot02 = sum(a*b for a, b in zip(p[0], p[2]))
    dot12 = sum(a*b for a, b in zip(p[1], p[2]))
    return 6-2*dot02+2*dot12


def recovered(initial, direction, word):
    states = phase_path(initial, direction, word)
    profile = tuple(contact(q) for q in states)
    return {'order': list(word), 'phase_path': [list(q) for q in states],
            'contact_profile': list(profile), 'barrier': max(v-profile[0] for v in profile)}


def inverse(initial, direction, observations, calibration):
    """No order, ID, address, receipt, barrier or source truth argument exists."""
    initial = tuple(initial)
    require(len(initial) == 3 and all(type(v) is int and 0 <= v < 4 for v in initial), 'Invalid initial phase')
    require(type(direction) is int and direction in (-1, 1), 'Invalid direction')
    require(len(observations) == 4 and all(type(f) is Frame for f in observations), 'Invalid observation history')
    if observations[0] != calibration[initial]:
        return []
    states = [((), initial)]
    for n in range(1, 4):
        observed_delta = difference(observations[n], observations[n-1])
        following = []
        for word, q in states:
            for j in range(3):
                if j in word:
                    continue
                next_q = list(q)
                next_q[j] = (next_q[j]+direction) % 4
                next_q = tuple(next_q)
                if difference(calibration[next_q], calibration[q]) == observed_delta:
                    following.append((word+(j,), next_q))
        states = following
    return [recovered(initial, direction, word) for word, q in sorted(states)]


def signature(frames, view):
    s = tuple(x for f in frames for x in f.signed)
    u = tuple(x for f in frames for x in f.occupancy)
    if view == 'JOINT':
        return s+u
    if view == 'SIGNED':
        return s
    if view == 'OCCUPANCY':
        return u
    if view == 'ENDPOINTS':
        return frames[0].signed+frames[0].occupancy+frames[-1].signed+frames[-1].occupancy
    if view == 'WRONG_POST_ABS':
        return s+tuple(abs(x) for x in s)
    raise ValueError('Unknown receiver view')
