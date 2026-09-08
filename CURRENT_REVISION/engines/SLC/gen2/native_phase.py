"""Pure nine-coordinate motion attachment for an existing sealed T18 word.

Copy into gen2/native_phase.py; imports use the already bound, byte-identical
native receipt algebra. This helper neither executes native Writes nor compiles
the full address domain. The original receipt and its seal remain embedded;
the expanded R3 response receives its own new schema and seal.
"""
from copy import deepcopy

from .dependencies.native.exact import ExactError, integer, token, verify, seal


PHASE = ((1, 0), (0, 1), (-1, 0), (0, -1))
SOURCE_SCHEMA = 'SLC_T18_RETAINED_WORD_V1'
RESULT_SCHEMA = 'SLC_T18_RETAINED_MOTION_WORD_V1'


def _phases(address):
    if not 0 <= integer(address) < (1 << 18):
        raise ExactError('Retained T18 address is outside its two Theta9 factors')
    return [((address >> c) & 1) + 2 * ((address >> (c + 9)) & 1) for c in range(9)]


def annotate_word(word):
    """Attach complete phase/lift/winding history while preserving source custody."""
    body = verify(word, SOURCE_SCHEMA)
    required = {'schema', 'source_endpoint', 'target_endpoint', 'address_before',
                'address_after', 'trajectory', 'directed_history', 'W8_shell_state',
                'X1_completion_custody', 'coordinate_group', 'factor_dimensions'}
    if set(body) != required:
        raise ExactError('Retained T18 source receipt has missing or undeclared fields')
    token(body['source_endpoint']); token(body['target_endpoint'])
    if body['source_endpoint'] == body['target_endpoint']:
        raise ExactError('Directed source endpoint identities must remain distinct')
    shell = integer(body['W8_shell_state'], minimum=0)
    if shell >= 256:
        raise ExactError('Retained W8 shell lies outside its eight coordinates')
    if body['coordinate_group'] != 'Z4^9' or body['factor_dimensions'] != [512, 512] or type(body['X1_completion_custody']) is not int or body['X1_completion_custody'] != 0:
        raise ExactError('T18 source geometry or completion custody differs')
    trajectory, writes = body['trajectory'], body['directed_history']
    if not isinstance(trajectory, list) or not isinstance(writes, list) or len(trajectory) != len(writes) + 1:
        raise ExactError('Retained T18 trajectory must include every directed Write')
    phases = [_phases(address) for address in trajectory]
    if body['address_before'] != trajectory[0] or body['address_after'] != trajectory[-1]:
        raise ExactError('Retained T18 endpoint addresses differ from the full trajectory')
    # Validate endpoint types too: bool must not masquerade as address 0/1.
    _phases(body['address_before']); _phases(body['address_after'])
    initial, lifts, records = phases[0], [0] * 9, []
    for step, (address, state) in enumerate(zip(trajectory, phases, strict=True)):
        if step:
            event = writes[step - 1]
            fields = {'record_index', 'orientation', 'address_before', 'address_after', 'retained_W8_shell_state'}
            if not isinstance(event, dict) or set(event) != fields:
                raise ExactError('Directed native record fields differ')
            coordinate = integer(event['record_index'])
            direction = integer(event['orientation'])
            if not 0 <= coordinate < 9 or direction not in (-1, 1):
                raise ExactError('Directed native record must be a signed unit Write on one of nine coordinates')
            if integer(event['address_before']) != trajectory[step - 1] or integer(event['address_after']) != address or integer(event['retained_W8_shell_state']) != shell:
                raise ExactError('Directed native edge loses trajectory or retained W8 custody')
            expected = list(phases[step - 1])
            expected[coordinate] = (expected[coordinate] + direction) % 4
            if expected != state:
                raise ExactError('Directed native phases disagree with the supplied quarter Write')
            lifts[coordinate] += direction
        coordinates = {}
        for coordinate in range(9):
            lifted = initial[coordinate] + lifts[coordinate]
            if lifted % 4 != state[coordinate]:
                raise ExactError('Ordered native lift does not match the retained phase')
            coordinates[str(coordinate)] = {
                'wrapped_quarter_phase': state[coordinate],
                'lifted_quartersteps': lifts[coordinate],
                'lifted_phase_quartersteps': lifted,
                'winding': lifted // 4,
                'phase_pair': list(PHASE[state[coordinate]])}
        records.append({'step': step, 'address': address, 'state': state, 'coordinates': coordinates})
    motion = {'schema': 'GEN2_NATIVE_T18_PHASE_HISTORY_V1', 'complete': True,
              'status': 'PHASE_HISTORY_AVAILABLE', 'native_coordinate_count': 9,
              'initial_phases': initial, 'final_phases': phases[-1],
              'coordinate_records': records,
              'sphere_status': 'NO_SOURCE_ACTION_PROFILE',
              'physical_spin_or_orbit_assigned': False,
              'source_receipt_semantic_sha256': word['semantic_sha256']}
    native = deepcopy(body)
    native.pop('schema')
    return seal(RESULT_SCHEMA, **native, source_receipt=deepcopy(word), motion=motion)
