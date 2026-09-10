"""Motion attachments for retained CE packet results, without native re-execution."""
from hashlib import sha256
from inspect import getsourcefile
from fractions import Fraction
import json
from pathlib import Path

from .exact import canonical, digest
from . import motion
from .native import unpack


SCHEMA = 'GEN2_PACKET_MOTION_ATTACHMENT_V1'
CONTACT_GRAM = [[2, 0, -1], [0, 2, 1], [-1, 1, 2]]


def _seal(body):
    body = canonical(body)
    return {'body': body, 'sha256': digest(body)}


def annotate_packet(packet, mathematical, *, runtime, source_output_sha256,
                    generation, ce_source_path=None, contact_contract_path=None):
    """Annotate actual returned paths using the caller's active GEN2 runtime.

    Source receipts remain byte-for-byte independent of this sealed attachment.
    Packet ordering is prescribed. This adapter adds readouts, never scheduling.
    """
    from CURRENT_REVISION.engines.SLC.native.exact import canonical_bytes, verify
    verify(packet, 'CE_HFM5_SOURCE_SIMULATION_V1')
    if sha256(canonical_bytes(mathematical)).hexdigest() != source_output_sha256:
        raise ValueError('Motion attachment output differs from the verified native receipt')
    base = Path(__file__).resolve().parent
    binding = {'packet_motion.py': sha256(Path(__file__).read_bytes()).hexdigest()}
    binding['gen2_runtime.py'] = sha256(Path(getsourcefile(type(runtime))).read_bytes()).hexdigest()
    if ce_source_path is not None:
        binding['ce/gen2_current.py'] = sha256(Path(ce_source_path).read_bytes()).hexdigest()
    body = {'schema': SCHEMA, 'complete': True, 'automatic': True,
            'generation': generation, 'domain': packet['domain'],
            'source_packet_semantic_sha256': packet['semantic_sha256'],
            'source_output_sha256': source_output_sha256,
            'native_source_result_preserved': True, 'native_science_reexecuted': False,
            'prescribed_word_order_preserved': True, 'implementation_binding': binding,
            'arithmetic_graphs': {}, 'histories': [], 'summary': {'source_task_count': len(packet['tasks']),
                                        'distinct_source_histories': 0}}
    if packet['domain'] != 'ATOM3D' or packet.get('domain_revision') != 'A3D41-T18-CONTACT-R2':
        body.update(status='NOT_APPLICABLE', reason='NO_REGISTERED_PACKET_CONTACT_SOURCE')
        return _seal(body)
    if contact_contract_path is None:
        from CURRENT_REVISION.runtime import HERE
        contact_contract_path = HERE / 'domains/ATOM3D/CONTACT_CONTRACT.json'
    contact_bytes = Path(contact_contract_path).read_bytes()
    contact = json.loads(contact_bytes)
    contact_hash = sha256(contact_bytes).hexdigest()
    if contact_hash != packet.get('contact_contract_sha256'):
        raise ValueError('Motion packet contact binding differs from its installed source')
    if (contact.get('schema') != 'ATOM3D_NATIVE_CONTACT_CONTRACT_R2'
            or contact.get('domain_revision') != packet['domain_revision']
            or contact.get('phase_slots') != [1, 4, 7]
            or contact.get('phase_coordinates') != 'REAL_THEN_IMAGINARY_OF_I_POWER_Q'
            or contact.get('contact_gram') != CONTACT_GRAM):
        raise ValueError('Current packet contact has no matching registered motion construction')
    body['contact_contract_sha256'] = contact_hash
    slots = tuple(contact['phase_slots'])
    block = runtime.compile(blocks=(slots,))
    cls = runtime.exact_information().hd_module.FormalLogElement
    profile = motion.resolve_profile(block)
    if profile is None:
        raise ValueError('Registered packet has no active source motion profile')
    body['profile'] = profile
    body['profile_sha256'] = digest(profile)
    body['compiled_source_contract_sha256'] = digest(block.contract.to_dict())
    rows = mathematical.get('rows')
    if not isinstance(rows, list) or len(rows) != len(packet['tasks']):
        raise ValueError('Motion attachment needs the complete verified source roster')
    contacts = [(i, form) for i, form in enumerate(packet['forms']) if form.get('id') == 'N100_CONTACT']
    if len(contacts) != 1:
        raise ValueError('Registered contact packet requires one N100_CONTACT readout')
    contact_index, contact_form = contacts[0]
    signed_contact_checks = 0
    histories = {}
    for task, row in zip(packet['tasks'], rows, strict=True):
        if (row.get('id'), row.get('index')) != (task['id'], task['index']):
            raise ValueError('Motion source task and returned history identity differ')
        path, writes = row['T18_trajectory'], task['fiber']['writes']
        if not path or len(path) != len(writes) + 1 or path[0] != task['fiber']['address']:
            raise ValueError('Motion attachment requires the complete original native trajectory')
        if any(type(address) is not int or not 0 <= address < (1 << 18) for address in path):
            raise ValueError('Returned T18 trajectory contains an invalid native address')
        states = [list(unpack(address, slots)) for address in path]
        if states[0] != task['initial_phases']:
            raise ValueError('Returned T18 initial phases differ from source task')
        if any(not isinstance(w, (list, tuple)) or len(w) != 2 or
               type(w[0]) is not int or w[0] not in slots or type(w[1]) is not int or w[1] not in (-1, 1)
               for w in writes):
            raise ValueError('Packet Write has no declared contact coordinate or direction')
        program = [f'W{coordinate}{"+" if direction == 1 else "-"}' for coordinate, direction in writes]
        # The complete packed history is retained even though the chart reads
        # only its declared source coordinates. No unobserved coordinate may change.
        outside = ((1 << 18) - 1) ^ sum((1 << c) | (1 << (c + 9)) for c in slots)
        if any((address & outside) != (path[0] & outside) for address in path):
            raise ValueError('Packet trajectory changes an undeclared contact coordinate')
        native = {'initial': states[0], 'program': program, 'states': states}
        stage = task['stage']
        if stage not in ('HISTORY', 'ABSOLUTE_CONTACT'):
            raise ValueError('Packet has no declared source-history stage')
        identity = task.get('history_id') if stage == 'HISTORY' else 'ABSOLUTE_CONTACT:' + digest(native)
        if type(identity) is not str or not identity:
            raise ValueError('Packet history needs its original source identity')
        key = (stage, identity)
        prefix = task['readout_prefix']
        if type(prefix) is not int or not 0 <= prefix < len(path):
            raise ValueError('Packet source readout prefix lies outside its retained trajectory')
        if task['readout_kind'] == 'NATIVE_SIGNED_PHASE':
            expected = block.contacts[tuple(states[prefix])]
            if stage == 'HISTORY':
                expected -= block.contacts[tuple(states[0])]
            measured = Fraction(row['quadratic_numerators'][contact_index], contact_form['denominator'])
            if measured != expected:
                raise ValueError('Returned signed contact differs from the registered motion action')
            signed_contact_checks += 1
        reference = {'task_id': task['id'], 'task_index': task['index'],
                     'readout_kind': task['readout_kind'], 'readout_prefix': prefix,
                     'source_endpoint': task['fiber']['source_endpoint'],
                     'target_endpoint': task['fiber']['target_endpoint']}
        if key in histories:
            previous = histories[key]
            if previous['native'] != native or previous['T18_trajectory'] != path:
                raise ValueError('One source history identity has conflicting returned trajectories')
            previous['source_tasks'].append(reference)
        else:
            histories[key] = {'source_history_id': identity, 'stage': stage,
                              'native': native, 'T18_trajectory': path,
                              'source_tasks': [reference],
                              'motion': motion.motion_readout(block, **native, log_class=cls)}
            from .write_arithmetic import intern_history
            intern_history(histories[key]['motion']['write_foundation'], body['arithmetic_graphs'])
    body['histories'] = list(histories.values())
    body['status'] = 'AVAILABLE'
    body['implementation_binding'].update(motion._binding(cls))
    body['implementation_binding']['motion_profiles.json'] = sha256((base / 'motion_profiles.json').read_bytes()).hexdigest()
    body['summary'].update(distinct_source_histories=len(histories),
                           history_stage_count=sum(h['stage'] == 'HISTORY' for h in histories.values()),
                           absolute_contact_stage_count=sum(h['stage'] == 'ABSOLUTE_CONTACT' for h in histories.values()),
                           role_history_count=sum(len(h['motion']['roles']) for h in histories.values()),
                           signed_contact_values_bound=signed_contact_checks,
                           source_task_references=sum(len(h['source_tasks']) for h in histories.values()),
                           all_motion_histories_available=all(h['motion']['status'] == 'AVAILABLE' for h in histories.values()))
    return _seal(body)
