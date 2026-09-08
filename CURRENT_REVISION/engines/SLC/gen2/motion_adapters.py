"""Automatic source-defined geometry for construction, readout and encounter routes.

Static phase/direction data supplies orientation. Ordered native source histories
supply accumulated turning. These are separate output types.
"""
from .exact import canonical, digest, rational


def _base(profile, kind):
    return {'schema': 'GEN2_AUTOMATIC_GEOMETRY_V1', 'profile_id': profile,
            'kind': kind, 'automatic': True, 'ordered_history_supplied': False,
            'winding': None, 'physical_spin_assigned': False}


def construction_geometry(operation, payload, result):
    if operation.removeprefix('GEN2_') != 'LI6_CONSTRUCTION':
        return result
    from .construction import li6_edge_vectors, li6_geometry
    g = li6_geometry()
    geometry = _base('LI6_NATIVE_UNIT_PHASE_V1', 'STATIC_PHASE_SPHERES')
    geometry['source_binding'] = digest(g)
    geometry['scale_rule'] = 'UNIT_PHASE_SCALE_ONE'
    if 'state' not in payload and 'phases' not in payload:
        geometry.update(status='SOURCE_PROFILE_REGISTERED', required_input='native state or nine phases')
    elif payload.get('kind', 0) != 0:
        geometry.update(status='NOT_APPLICABLE', reason='PHASE_ERASED_INPUT')
    else:
        re, im = li6_edge_vectors(payload.get('state'), phases=payload.get('phases'))
        flags = g['masks'][payload.get('mask', 3)]
        geometry.update(status='APPLIED', sphere_radius='1', log_scale_terms=[],
            points=[{'edge': name, 'active': bool(flag),
                     'sphere_point': [a, b, 0] if flag else None}
                    for name, a, b, flag in zip(g['relation_ids'], re, im, flags)],
            relative_phases=[{'left': g['relation_ids'][i], 'right': g['relation_ids'][j],
                              'cos': re[i]*re[j]+im[i]*im[j],
                              'sin_right_minus_left': re[i]*im[j]-im[i]*re[j]}
                             for i in range(9) for j in range(i+1, 9) if flags[i] and flags[j]])
    return {**result, 'geometry': canonical(geometry)}


def readout_geometry(operation, payload, result):
    if operation.removeprefix('GEN2_') != 'READOUT':
        return result
    strategy = payload.get('strategy', 'polynomial')
    if strategy not in ('angular', 'angular_compact', 'angular_power', 'radial', 'radial_compact'):
        return result
    from .readouts import AXES, SHELL_RADII
    amounts = [rational(v) for v in payload['amounts']]
    if strategy.startswith('angular'):
        geometry = _base('GEN2_SIX_AXIS_CLOSED_SPHERE_V1', 'STATIC_ANGULAR_DISTRIBUTION')
        geometry.update(status='APPLIED', sphere_radius='1',
            points=[{'direction': list(direction), 'amount': amount}
                    for direction, amount in zip(AXES, amounts)],
            source_binding=digest({'directions': AXES, 'order': '+x,-x,+y,-y,+z,-z'}))
    else:
        radii = tuple(rational(r) for r in payload.get('radii', SHELL_RADII))
        geometry = _base('GEN2_NATIVE_RADIAL_SHELLS_V1', 'STATIC_NESTED_SPHERES')
        geometry.update(status='APPLIED',
            shells=[{'radius': r, 'amount': a} for r, a in zip(radii, amounts)],
            source_binding=digest({'radii': radii}),
            radius_unit='DECLARED_NATIVE_RADIAL_COORDINATE')
    return {**result, 'geometry': canonical(geometry)}


def encounter_geometry(operation, payload, result, *, log_class=None):
    geometry = _base('GEN2_ENCOUNTER_SOURCE_MOTION_V1', 'LINKED_SOURCE_HISTORIES')
    sources = payload.get('source_motion')
    if sources is None:
        geometry.update(status='NOT_APPLICABLE', reason='EMISSIONS_HAVE_NO_DECLARED_NATIVE_MOTION_HISTORY')
        return {**result, 'geometry': geometry}
    if not isinstance(sources, dict) or not sources or 'emissions' not in payload or 'observations' in payload:
        raise ValueError('Encounter source_motion needs named source programs and their supplied emissions')
    from .compiler import compile_block
    from .native import native_contract
    histories = {}
    for source, request in sources.items():
        if source not in payload['emissions'] or not isinstance(request, dict):
            raise ValueError('Motion source must be a declared emitting source')
        if set(request) - {'contract', 'rho', 'blocks', 'initial', 'program', 'emission_indices'}:
            raise ValueError('Undeclared encounter source motion fields')
        block = compile_block(request.get('contract') or native_contract(
            rho=request.get('rho', 1), **({'blocks': request['blocks']} if 'blocks' in request else {})))
        history = block.run(request['initial'], request['program'], log_class=log_class)
        indices = request['emission_indices']
        emission = payload['emissions'][source]
        if not isinstance(indices, dict) or set(indices) != set(emission):
            raise ValueError('Every supplied emission tick needs an explicit native history index')
        for tick, index in indices.items():
            if type(index) is not int or not 0 <= index < len(history['states']):
                raise ValueError('Emission history index outside supplied history')
            if canonical(emission[tick]) != canonical(history['observations'][index]):
                raise ValueError('Supplied encounter emission differs from its native source history')
        histories[source] = {'native': history, 'emission_indices': indices,
                             'contract_id': block.contract_id}
    geometry.update(status='APPLIED', ordered_history_supplied=True, sources=histories,
                    source_binding=digest(sources), clock_alignment='EXPLICIT_EMISSION_INDEX_MAP')
    return {**result, 'geometry': canonical(geometry)}
