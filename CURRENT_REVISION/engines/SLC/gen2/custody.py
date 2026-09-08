"""Target-bound adapter around the completed finite custody compiler."""
from .dependencies.slc_custody_native.compiler import CompiledCustodyMorphism, FiberReceipt
from .dependencies.slc_custody_native.program import CompiledCustodyProgram, ProgramReceipt
from .dependencies.slc_custody_native.algebra import PrimeLogWeight
from .exact import canonical, canonical_bytes, digest


class NativeCustodyMap:
    def __init__(self, records, *, target, known_information=None,
                 source_contract=None, receipt_channel='SUPPLIED_RECONSTRUCTIVE_CUSTODY'):
        if not target:
            raise ValueError('Custody requires an explicit reconstruction target')
        self.records = tuple({'source': canonical(r['source']), 'visible': canonical(r['visible'])}
                             for r in records)
        self.binding = canonical({'target': target, 'known_information': known_information or {},
                                  'source_contract': source_contract.to_dict() if hasattr(source_contract, 'to_dict') else source_contract,
                                  'receipt_channel': receipt_channel,
                                  'source_body': sorted(self.records, key=canonical_bytes)})
        self.binding_id = digest(self.binding)
        by_source = {canonical_bytes(r['source']): canonical_bytes(r['visible']) for r in self.records}
        if len(by_source) != len(self.records):
            raise ValueError('Duplicate source members in finite custody declaration')
        self._originals = {canonical_bytes(r['source']): r['source'] for r in self.records}
        self._visible_originals = {canonical_bytes(r['visible']): r['visible'] for r in self.records}
        self.morphism = CompiledCustodyMorphism('GEN2_TARGET:' + self.binding_id,
                                               by_source, by_source.__getitem__,
                                               source_references=(self.binding_id,))

    def encode(self, source):
        state = self.morphism.encode(canonical_bytes(source))
        receipt = state.receipt.to_dict()
        # Exact integer container width, including arbitrary-size fibers.
        receipt['container_bits'] = (receipt['fiber_multiplicity'] - 1).bit_length()
        return {'visible': self._visible_originals[state.visible],
                'receipt': {'schema': 'SLC_GEN2_TARGET_RECEIPT_V1',
                            'binding_id': self.binding_id,
                            'visible_value': self._visible_originals[state.visible],
                            'information_weight': self._information(receipt['fiber_multiplicity']),
                            'native_receipt': receipt}}

    @staticmethod
    def _information(multiplicity):
        weight = PrimeLogWeight.from_multiplicity(multiplicity)
        powers = dict(weight.prime_exponents)
        return {'expression': weight.expression,
                'prime_log_coefficients': [{'prime': p, 'coefficient': n} for p, n in weight.prime_exponents],
                'ln2_coefficient': powers.get(2, 0), 'ln3_coefficient': powers.get(3, 0),
                'primitive_values': {'h_hat': 2, 'd_hat': 3},
                'meaning': 'Additive information coordinates; primitive h_hat and d_hat retain values 2 and 3'}

    def decode(self, visible, receipt):
        if receipt.get('schema') != 'SLC_GEN2_TARGET_RECEIPT_V1' or receipt.get('binding_id') != self.binding_id:
            raise ValueError('Receipt reconstruction target, source body or known-information binding mismatch')
        if receipt.get('visible_value') != canonical(visible):
            raise ValueError('Receipt belongs to a different visible value')
        native = FiberReceipt(**receipt['native_receipt'])
        if native.container_bits != (native.fiber_multiplicity - 1).bit_length():
            raise ValueError('Invalid exact receipt container width')
        if receipt.get('information_weight') != self._information(native.fiber_multiplicity):
            raise ValueError('Receipt symbolic information weight mismatch')
        key = self.morphism.decode(canonical_bytes(visible), native)
        return self._originals[key]

    def fiber(self, visible):
        return [self._originals[key] for key in self.morphism.fiber(canonical_bytes(visible))]

    def to_dict(self):
        return {'schema': 'SLC_GEN2_CUSTODY_MAP_V1', 'binding_id': self.binding_id,
                'binding': self.binding, 'native_profile': self.morphism.profile.to_dict(),
                'source_body_bytes': len(canonical_bytes(self.binding)),
                'native_profile_measure': 'Uniform probability over the declared finite source members',
                'receipt_policy': 'Observation-only returns every member; supplied receipt selects its admitted member'}


def compile_custody(spec):
    allowed = {'records', 'target', 'known_information', 'source_contract', 'receipt_channel'}
    if set(spec) - allowed:
        raise ValueError('Undeclared custody fields')
    return NativeCustodyMap(**spec)


class NativeCustodySequence:
    """Retain each completed component's receipt across a compatible sequence."""
    def __init__(self, name, stages):
        self.stages = tuple(stages)
        self.program = CompiledCustodyProgram(name, [s.morphism for s in self.stages])

    def encode(self, source):
        state = self.program.execute(canonical_bytes(source))
        return {'visible': self.stages[-1]._visible_originals[state.visible],
                'receipt': {'schema': 'SLC_GEN2_CUSTODY_SEQUENCE_RECEIPT_V1',
                            'visible_value': self.stages[-1]._visible_originals[state.visible],
                            'program_receipt': state.receipt.to_dict()}}

    def decode(self, visible, receipt):
        if receipt.get('schema') != 'SLC_GEN2_CUSTODY_SEQUENCE_RECEIPT_V1' or receipt.get('visible_value') != canonical(visible):
            raise ValueError('Sequence receipt visible-value binding mismatch')
        receipt = receipt['program_receipt']
        receipt = ProgramReceipt(receipt['schema'], receipt['program_id'],
                                 tuple(FiberReceipt(**r) for r in receipt['stage_receipts']))
        key = self.program.reconstruct(canonical_bytes(visible), receipt)
        return self.stages[0]._originals[key]

    def audit(self):
        return self.program.audit()
