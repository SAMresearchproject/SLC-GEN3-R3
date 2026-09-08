"""Native T18 direction/history fiber: nine Z4 records, two Theta9 factors.

Source: H000136 and the installed Exact Algebra of the Write. Endpoint IDs
are retained independently of packed fiber addresses and W8 shell state.
"""
from .exact import ExactError, integer, token, seal

RECORD_COUNT = 9
ADDRESS_COUNT = 1 << 18
MAP_SHA256 = "5cd4e3001b11e8c1ecb828087aaab94bbace51c1129d5bacbd4218f95e7f9ab3"


def validate_write(address, record, delta):
    if not 0 <= integer(address) < ADDRESS_COUNT:
        raise ExactError("T18 address outside its two Theta9 factors")
    if not 0 <= integer(record) < RECORD_COUNT or integer(delta) not in (-1, 1):
        raise ExactError("T18 requires one of nine records and a signed unit Write")


def write(address, record, delta):
    validate_write(address, record, delta)
    low = (address >> record) & 1
    return address ^ (1 << record) ^ ((low ^ (delta == -1)) << (record + 9))


def word(address, writes, *, source_endpoint, target_endpoint, shell_state=0):
    integer(shell_state, minimum=0)
    if shell_state >= 256:
        raise ExactError("W8 shell state outside its eight coordinates")
    token(source_endpoint); token(target_endpoint)
    if source_endpoint == target_endpoint:
        raise ExactError("directed endpoint identities must remain distinct")
    start = address
    trajectory = [address]
    records = []
    for record, delta in writes:
        following = write(address, record, delta)
        records.append({"record_index": record, "orientation": delta,
                        "address_before": address, "address_after": following,
                        "retained_W8_shell_state": shell_state})
        trajectory.append(following)
        address = following
    return seal("SLC_T18_RETAINED_WORD_V1", source_endpoint=source_endpoint,
                target_endpoint=target_endpoint, address_before=start,
                address_after=address, trajectory=trajectory, directed_history=records,
                W8_shell_state=shell_state, X1_completion_custody=0,
                coordinate_group="Z4^9", factor_dimensions=[512, 512])


def history_quotient(left, right):
    if len(left) != 81 or len(right) != 81:
        raise ExactError("T18 reciprocal views require 81 coordinates each")
    left = tuple(integer(x) for x in left)
    right = tuple(integer(x) for x in right)
    symmetric = tuple(a+b for a, b in zip(left, right))
    antisymmetric = tuple(a-b for a, b in zip(left, right))
    return tuple(x-symmetric[-1] for x in symmetric[:-1]) + antisymmetric


def full_map():
    """Branch-free CPU map in the frozen big-endian transition-map order."""
    import numpy as np
    addresses = np.arange(ADDRESS_COUNT, dtype=np.uint32)
    result = np.empty((2, 9, ADDRESS_COUNT), dtype=np.uint32)
    for direction, delta in enumerate((1, -1)):
        for record in range(9):
            low = (addresses >> np.uint32(record)) & np.uint32(1)
            result[direction, record] = addresses ^ np.uint32(1 << record) ^ (
                (low ^ np.uint32(delta == -1)) << np.uint32(record+9))
    return result
