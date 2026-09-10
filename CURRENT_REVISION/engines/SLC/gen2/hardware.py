"""Reusable finite native-source batching; hardware identity stays in telemetry.

The mathematical output is next packed T18 address followed by before/after
signed-phase and source-axis-occupancy frames for up to two source blocks.
Each block has 16 receiver coordinates; unused block slots are exactly zero.
"""
import hashlib
import multiprocessing as mp
import os
import time

import numpy as np

from .compiler import compile_block
from .contracts import Event, SourceContract
from .native import native_contract, pack, unpack, j4_matrix

OUTPUT_WIDTH = 129
H14F_PHYSICAL_CPUS = (0, 2, 4, 6, 8, 10, 12, 13, 14, 15, 16, 17, 18, 19)
_PRIMARY_BLOCKS = None
_PRIMARY_ROWS = None


def qualification_contracts():
    contracts = [native_contract(rho, name=f'original_rho_{rho}') for rho in (1, 2, 8, 128)]
    for label, blocks in (('disjoint', ((1, 4, 7), (0, 2, 8))),
                          ('shared', ((1, 4, 7), (0, 2, 7)))):
        events = tuple(Event(f'{block}_{coordinate}_{direction:+d}', coordinate, direction)
                       for block, coordinates in enumerate(blocks)
                       for coordinate in coordinates for direction in (-1, 1))
        contracts.append(native_contract(1, blocks, events, name=label + '_two_block'))
    return tuple(contracts)


def plan_batch(contracts=None):
    """Compile each source once and retain every declared state/event row."""
    started = time.perf_counter()
    contracts = qualification_contracts() if contracts is None else tuple(contracts)
    blocks = tuple(compile_block(c if isinstance(c, SourceContract) else SourceContract.from_dict(c)) for c in contracts)
    if not blocks:
        raise ValueError('Native hardware batch requires at least one source contract')
    rows, sections = [], []
    for index, block in enumerate(blocks):
        if len(block.contract.receivers) > 2 or any(len(r.matrix) != 16 or len(r.coordinates) != 3 for r in block.contract.receivers):
            raise ValueError('This hardware batch requires one or two sixteen-channel three-coordinate receivers')
        if not block.contract.source_binding.startswith('H980_J4:') or ':rho=' not in block.contract.source_binding:
            raise ValueError('This batch profile requires declared source-bound J4 receiver calibrations')
        rho = int(block.contract.source_binding.split(':rho=')[1])
        expected_matrix = j4_matrix(rho)
        if any(r.matrix != expected_matrix for r in block.contract.receivers):
            raise ValueError('Receiver matrix differs from its declared native J4 calibration')
        start = len(rows)
        labels = list(block.events)
        for state, label, target, direction in block.transitions:
            event = block.events[label]
            rows.append((index, pack(state, block.contract.coordinates), event.coordinate, direction, labels.index(label)))
        sections.append({'contract_id': block.contract_id, 'name': block.contract.name,
                         'contract': block.contract.to_dict(), 'rows': len(rows) - start, 'start': start,
                         'states': len(block.states), 'events': labels})
    if not rows:
        raise ValueError('Native hardware batch requires at least one admitted transition')
    maximum = max(sum(abs(int(v)) for v in row) for b in blocks for r in b.contract.receivers for row in r.matrix)
    if any(v.denominator != 1 for b in blocks for r in b.contract.receivers for row in r.matrix for v in row if hasattr(v, 'denominator')):
        raise ValueError('This exact i64 hardware profile requires integral calibration coefficients')
    if maximum > np.iinfo(np.int64).max:
        raise OverflowError('Receiver absolute contraction bound exceeds signed int64')
    metadata = {'schema': 'GEN2_NATIVE_HARDWARE_BATCH_V1', 'sections': sections,
                'row_fields': ['contract_index', 'packed_before', 'write_coordinate', 'write_direction', 'event_label_index'],
                'output_width': OUTPUT_WIDTH,
                'output_layout': {'next_address': 0, 'block_offsets': [1, 65],
                                  'within_block': {'before_signed': 0, 'before_occupancy': 16,
                                                   'after_signed': 32, 'after_occupancy': 48}},
                'zero_padding': 'second block is zero for original single-block sources',
                'integer_bound': {'maximum_absolute_row_sum': maximum, 'source_lift_maximum_absolute': 1,
                                  'maximum_output_absolute': maximum, 'signed_i64_safe': True},
                'compile_seconds': time.perf_counter() - started,
                'inverse_graph_execution_device': 'CPU'}
    return metadata, np.asarray(rows, dtype=np.int64), blocks


def _pin(queue):
    os.sched_setaffinity(0, [queue.get()])


def _primary_chunk(bounds):
    start, stop = bounds
    output = np.zeros((stop - start, OUTPUT_WIDTH), np.int64)
    for i, row in enumerate(_PRIMARY_ROWS[start:stop]):
        section, address, axis, direction, label_index = map(int, row)
        block = _PRIMARY_BLOCKS[section]
        before = unpack(address, block.contract.coordinates)
        label = tuple(block.events)[label_index]
        after = block.forward(before, label)
        output[i, 0] = pack(after, block.contract.coordinates)
        for b in range(len(block.contract.receivers)):
            for t, state in enumerate((before, after)):
                frame = block.frames[state]
                for lane, key in enumerate(('SIGNED_PHASE', 'AXIS_OCCUPANCY')):
                    begin = 1 + 64 * b + 32 * t + 16 * lane
                    output[i, begin:begin + 16] = frame[key][16 * b:16 * (b + 1)]
    return start, output, {'pid': os.getpid(), 'affinity': sorted(os.sched_getaffinity(0)), 'rows': stop - start}


def evaluate_primary(rows, blocks, workers=14):
    """Pinned H14F workers consume the actual compiled-source frames."""
    if type(workers) is not int or workers < 1:
        raise ValueError('Worker count must be positive')
    available = set(map(int,os.environ['SAM_R3_ALLOWED_CPUS'].split(','))) if 'SAM_R3_ALLOWED_CPUS' in os.environ else os.sched_getaffinity(0)
    order = tuple(map(int,os.environ['SAM_R3_CPU_ORDER'].split(','))) if 'SAM_R3_CPU_ORDER' in os.environ else H14F_PHYSICAL_CPUS
    cpus = [c for c in order if c in available][:workers]
    if len(cpus) != workers:
        raise ValueError('Requested pinned H14F physical profile is unavailable')
    global _PRIMARY_BLOCKS, _PRIMARY_ROWS
    _PRIMARY_BLOCKS, _PRIMARY_ROWS = blocks, rows
    context = mp.get_context('fork'); queue = context.Queue()
    for cpu in cpus:
        queue.put(cpu)
    bounds = np.linspace(0, len(rows), workers + 1, dtype=int)
    started = time.perf_counter()
    with context.Pool(workers, initializer=_pin, initargs=(queue,)) as pool:
        pieces = pool.map(_primary_chunk, [(int(a), int(b)) for a, b in zip(bounds[:-1], bounds[1:])], chunksize=1)
    output = np.empty((len(rows), OUTPUT_WIDTH), np.int64)
    for start, value, telemetry in pieces:
        output[start:start + len(value)] = value
    receipt = {'workers': workers, 'cpus': cpus, 'seconds': time.perf_counter() - started,
               'worker_processes': [x[2] for x in pieces], 'rows': len(rows), 'values': int(output.size),
               'sha256': hashlib.sha256(output.astype('<i8', copy=False).tobytes()).hexdigest()}
    _PRIMARY_BLOCKS = _PRIMARY_ROWS = None
    return output, receipt
