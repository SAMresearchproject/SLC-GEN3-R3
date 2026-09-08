"""Source-bound native transition and real J4 source-lane lowering."""
from functools import lru_cache
from pathlib import Path
import hashlib
import json
from .contracts import Event, Receiver, SourceContract
from .dependencies.native.t18 import write
from .dependencies import common_reception as common


def pack(q, coordinates):
    return sum((v & 1) << c | (v >> 1) << (c + 9) for c, v in zip(coordinates, q, strict=True))


def unpack(address, coordinates):
    return tuple(((address >> c) & 1) + 2 * ((address >> (c + 9)) & 1) for c in coordinates)


def transition(q, event, coordinates):
    return unpack(write(pack(q, coordinates), event.coordinate, event.direction), coordinates)


@lru_cache(maxsize=128)
def j4_matrix(rho):
    if type(rho) is not int or rho < 1:
        raise ValueError('rho must name a positive integer calibration')
    path = Path(__file__).parent / 'dependencies/J4_RESPONSES.jsonl'
    templates = {}
    with path.open() as stream:
        for line in stream:
            row = json.loads(line)
            if row['rho'] == rho and row['relation_id'] in common.RELATIONS:
                if row['relation_id'] in templates:
                    raise ValueError('Duplicate receiver calibration')
                templates[row['relation_id']] = {ch: row[ch] for ch in common.CHANNELS}
    if set(templates) != set(common.RELATIONS):
        raise ValueError('rho has no complete source-bound receiver calibration')
    columns = []
    for i in range(6):
        h = tuple(int(i == j) for j in range(6))
        columns.append(common.common_reception(h, templates).signed)
    return tuple(tuple(columns[j][i] for j in range(6)) for i in range(16))


def native_contract(rho=1, blocks=((1, 4, 7),), events=None, *, name=None,
                    contact_coordinates=None):
    blocks = tuple(tuple(b) for b in blocks)
    if any(len(b) != 3 for b in blocks):
        raise ValueError('J4 blocks each read three coordinates')
    coordinates = tuple(sorted({c for b in blocks for c in b}))
    if events is None:
        events = tuple(Event(f'W{c}{"+" if d == 1 else "-"}', c, d)
                       for c in coordinates for d in (-1, 1))
    else:
        events = tuple(e if isinstance(e, Event) else Event(**e) for e in events)
    source_file = Path(__file__).parent / 'dependencies/J4_RESPONSES.jsonl'
    binding = 'H980_J4:' + hashlib.sha256(source_file.read_bytes()).hexdigest() + ':rho=' + str(rho)
    return SourceContract(name or 'native-j4-construction', coordinates,
                          tuple(sorted(events, key=lambda e: e.label)),
                          tuple(Receiver(f'J4_{i}', b, j4_matrix(rho)) for i, b in enumerate(blocks)),
                          contact_coordinates=tuple(contact_coordinates or blocks[0]),
                          source_binding=binding)


def receive(q, contract):
    state = dict(zip(contract.coordinates, q, strict=True))
    signed, occupancy = [], []
    for receiver in contract.receivers:
        h = tuple(common.PHASE[state[c]][side] for side in (0, 1) for c in receiver.coordinates)
        for row in receiver.matrix:
            signed.append(sum(a * b for a, b in zip(row, h, strict=True)))
            occupancy.append(sum(a * abs(b) for a, b in zip(row, h, strict=True)))
    return {'SIGNED_PHASE': tuple(signed), 'AXIS_OCCUPANCY': tuple(occupancy)}


def contact(q, contract):
    if contract.contact_coordinates is None:
        return None
    state = dict(zip(contract.coordinates, q, strict=True))
    return common.contact(tuple(state[c] for c in contract.contact_coordinates))
