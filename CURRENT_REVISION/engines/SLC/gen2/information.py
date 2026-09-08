"""GEN2 calls into the installed, bound V6/ICF1 HD/formal-log algebra."""
from fractions import Fraction

OPERATIONS = ('GEN2_HD', 'GEN2_HD_PRIMITIVES', 'GEN2_FORMAL_LOG')


def exact(value):
    if type(value) not in (int, str, Fraction):
        raise ValueError('HD operands require exact integers or rational strings')
    return Fraction(value)


def dispatch(operation, payload, foundation):
    hd = foundation.hd_module
    if operation == 'GEN2_HD':
        if set(payload) - {'value', 'source_provenance'}:
            raise ValueError('Unknown HD input field')
        return foundation.serialize_hd(exact(payload['value']),
            source_provenance=payload.get('source_provenance', 'GEN2_DECLARED_EXACT_OPERAND'))
    if operation == 'GEN2_FORMAL_LOG':
        if set(payload) - {'terms', 'compare_terms'}:
            raise ValueError('Unknown formal-log input field')
        def terms(rows):
            return hd.FormalLogElement.from_terms((p, exact(c)) for p, c in rows)
        value = terms(payload['terms'])
        result = {'formal_log': value.to_dict(), 'exact_sign': value.sign}
        if 'compare_terms' in payload:
            other = terms(payload['compare_terms'])
            result.update(comparison=other.to_dict(), exact_comparison=value.compare(other))
        return result
    if operation == 'GEN2_HD_PRIMITIVES':
        if payload:
            raise ValueError('The source-bound primitive map takes no fitted operands')
        values = {'h_hat': 2, 'd_hat': 3, 'surface': 8, 'closure': 9,
                  'R': 12, 'Theta': 18, 'closure_ratio': Fraction(9, 8)}
        rows = {}
        for name, value in values.items():
            signature = hd.HDSignature.from_rational(value)
            rows[name] = {'exact_value': str(value), 'hd_signature': signature.to_dict(),
                          'formal_log': signature.formal_log.to_dict()}
        return {'schema': 'GEN2_HD_PRIMITIVE_READOUT_V1', 'foundation': 'SLCV33-ICF1',
                'primitive_values': {'h_hat': 2, 'd_hat': 3}, 'coordinates': rows,
                'closure_identity': {'left': 9, 'right_power': 8, 'additive_surplus': 1},
                'meaning': 'Exact logarithmic coordinates of the source primitives and their products; primitive values remain 2 and 3.',
                'source': 'volume_I/SAM_VOLUME_I_SUBSTRATE_TECHNICAL_SPINE.md:79-91',
                'physical_energy_assignment': None}
    raise ValueError('Unknown GEN2 information operation')
