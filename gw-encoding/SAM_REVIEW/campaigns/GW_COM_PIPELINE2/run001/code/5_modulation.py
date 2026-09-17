"""Prescribed C4 source controls and exact native quadrupole generation."""
from fractions import Fraction as F
import random
from .native import Graph

PROFILE = [0, 1, 3, 6, 8, 6, 3, 1, 0]


def source(message, active=True):
    events = []
    start = 256  # Declared quiet calibration/validation prefix.
    for _ in range(2):
        packet = [start + 16 * i for i in range(4)]
        for value in message:
            packet.append(packet[-1] + 16 * value)
        events += packet
        start = packet[-1] + 23 * 16
    radius = [F(1)] * (events[-1] + 33)
    if active:
        for center in events:
            for offset, value in enumerate(PROFILE):
                radius[center + offset - 4] += F(value, 128)
    axes = [(1,0),(0,1),(-1,0),(0,-1)]
    xy = [(r*axes[i%4][0], r*axes[i%4][1]) for i,r in enumerate(radius)]
    return {'positions':xy, 'stencils':[tuple(xy[i-1:i+2]) for i in range(1,len(xy)-1)],
            'truth':{'message':message, 'marker_source_ticks':events, 'unit_ticks':16}}


def wave_library(native, sources):
    stencils = sorted({s for source in sources.values() for s in source['stencils']})
    graph = Graph()
    two = graph.value(2, 'two antipodal unit-weight bodies')
    outputs = []
    for j, stencil in enumerate(stencils):
        q = []
        for k,(x,y) in enumerate(stencil):
            a = graph.value(x, {'stencil':j,'offset':k,'coordinate':'x'})
            b = graph.value(y, {'stencil':j,'offset':k,'coordinate':'y'})
            # Trace terms cancel exactly in Qxx-Qyy for the antipodal pair.
            delta = graph.op('SUBTRACT',graph.op('MULTIPLY',a,a),graph.op('MULTIPLY',b,b))
            q.append(graph.op('MULTIPLY',two,delta))
        outputs.append(graph.op('SUBTRACT',graph.op('ADD',q[0],q[2]),graph.op('MULTIPLY',two,q[1])))
    values, receipt = native.evaluate(graph, 'GW-COM H000733 source: exact antipodal quadrupole projection and second difference for each distinct prescribed orbit stencil')
    library = {s:values[key] for s,key in zip(stencils,outputs)}
    for stencil, value in library.items():
        q = [2*(x*x-y*y) for x,y in stencil]
        assert q[0]-2*q[1]+q[2] == value  # Independent Fraction check.
    return library, receipt


def observe(native, wave, *, gain=F(1), drift=F(0), offset=F(0), noise=F(0), seed=0):
    rng = random.Random(seed)
    graph = Graph()
    gain_id, offset_id = graph.value(gain,'channel gain'), graph.value(offset,'DC offset')
    out = []
    for i,w in enumerate(wave):
        # An amplitude-drift nuisance of the signed carrier, distinct from pulses.
        base = graph.value(w, {'native_source_sample':i})
        nuisance = graph.value(drift*i*((-1)**i), {'carrier_drift_sample':i})
        error = graph.value(noise*F(rng.randint(-100,100),100), {'measurement_noise_sample':i,'seed':seed})
        out.append(graph.op('ADD',graph.op('ADD',graph.op('MULTIPLY',gain_id,
            graph.op('ADD',base,nuisance)),offset_id),error))
    values, receipt = native.evaluate(graph,'GW-COM readout: exact signed source gain, carrier drift, DC offset and bounded sampled noise')
    return [values[x] for x in out], receipt
