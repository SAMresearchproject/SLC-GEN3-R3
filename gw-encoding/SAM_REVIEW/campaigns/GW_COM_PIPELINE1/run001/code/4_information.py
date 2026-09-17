"""Symbol discovery and transparent diagnostics; no prime-message knowledge."""
from collections import Counter
from fractions import Fraction as F
import math
import random
from statistics import median
import zlib
from .native import Graph


def framing(markers):
    frames = []
    for start in range(max(0,len(markers)-9)):
        block = markers[start:start+10]
        gaps = [b-a for a,b in zip(block,block[1:])]
        unit = median(gaps[:3])
        if unit <= 0 or any(abs(F(g,unit)-1)>F(3,25) for g in gaps[:3]):
            continue
        ratios = [F(g,unit) for g in gaps[3:]]
        bins = [round(v) for v in ratios]
        if any(n<1 or abs(v-n)>F(3,25) for v,n in zip(ratios,bins)):
            continue
        frames.append({'marker_indices':list(range(start,start+10)), 'unit_samples':unit,
            'interval_ratio_bins':bins,'ratios':[str(v) for v in ratios],
            'sample_spans':[[block[i],block[i+1]] for i in range(3,9)]})
    return frames


def max_repetition(frames):
    # Count disjoint packets only; overlapping windows cannot multiply evidence.
    groups = {}
    for index, frame in enumerate(frames):
        key = tuple(frame['interval_ratio_bins'])
        group = groups.setdefault(key,[])
        if not group or frame['marker_indices'][0] > frames[group[-1]]['marker_indices'][-1]:
            group.append(index)
    return max((len(v) for v in groups.values()),default=0), groups


def symbolize(residual, amplitude):
    threshold = abs(amplitude)*F(3,100)
    active = [i for i,v in enumerate(residual) if abs(v)>threshold]
    groups = []
    for i in active:
        if not groups or i-groups[-1][-1]>2:
            groups.append([])
        groups[-1].append(i)
    kept, rejected = [], []
    for g in groups:
        row = {'sample_span':[g[0],g[-1]],'peak_sample':max(g,key=lambda i:abs(residual[i])),
               'signed_samples':[str(residual[i]) for i in range(g[0],g[-1]+1)]}
        (kept if 3<=len(g)<=11 else rejected).append(row)
    markers = [g['peak_sample'] for g in kept]
    frames = framing(markers)
    count, groups = max_repetition(frames)
    alphabet = sorted({n for f in frames for n in f['interval_ratio_bins']})
    symbols = {v:'S'+str(i) for i,v in enumerate(alphabet)}
    for f in frames:
        f['symbols'] = [symbols[v] for v in f['interval_ratio_bins']]
    return {'threshold':str(threshold),'markers':markers,'marker_evidence':kept,
            'rejected_marker_groups':rejected,'frames':frames,
            'alphabet':[{'symbol':symbols[v],'interval_ratio_bin':v} for v in alphabet],
            'repetition_count':count,'repetition_groups':[{'bins':list(k),'frame_indices':v} for k,v in groups.items()]}


def tests(native, symbols, permutations=99, seed=20260917):
    markers = symbols['markers']
    gaps = [b-a for a,b in zip(markers,markers[1:])]
    observed = symbols['repetition_count']
    rng = random.Random(seed)
    nulls = []
    for index in range(permutations):
        shuffled = list(gaps)
        rng.shuffle(shuffled)
        surrogate = [0]
        for value in shuffled:
            surrogate.append(surrogate[-1]+value)
        frames = framing(surrogate) if gaps else []
        score,_ = max_repetition(frames)
        nulls.append({'index':index,'gap_order':shuffled,'repetition_count':score,
                      'candidate_frames':frames})
    exceedances = sum(n['repetition_count']>=observed for n in nulls)
    graph = Graph()
    numerator = graph.value(1+exceedances,'one plus null exceedance count; ties included')
    denominator = graph.value(1+permutations,'one plus permutation count')
    p_id = graph.op('DIVIDE',numerator,denominator)
    counts = Counter(s for f in symbols['frames'] for s in f['symbols'])
    total = sum(counts.values())
    probabilities = {}
    for symbol,n in counts.items():
        probabilities[symbol] = graph.op('DIVIDE',graph.value(n,{'symbol_count':symbol}),graph.value(total,'symbol count total'))
    native,receipt = native.evaluate(graph,'GW-COM information tests: exact permutation rank probability and empirical alphabet probabilities; full framing search repeated for each null')
    probs = {s:native[k] for s,k in probabilities.items()}
    entropy = -sum(float(p)*math.log2(float(p)) for p in probs.values())
    sequence = '|'.join(','.join(f['symbols']) for f in symbols['frames']).encode()
    lag_counts = Counter(b-a for j,a in enumerate(markers) for b in markers[j+1:])
    return {'observed_repetition':observed,'permutation_p':str(native[p_id]),
        'null_hypothesis':'exchangeable order of detected gaps conditional on their multiset; not a universal astrophysical noise model',
        'permutations':nulls,'permutation_seed':seed,
        'periodicity':{'pairwise_marker_lag_histogram':dict(sorted(lag_counts.items()))},
        'entropy':{'alphabet_probabilities':{s:str(p) for s,p in probs.items()},
                   'shannon_bits_per_symbol':entropy,'numeric_log_role':'derived display from native exact probabilities'},
        'compression':{'encoding':'UTF-8 symbol labels, comma and pipe separators','codec':'zlib default with header',
                       'input_bytes':len(sequence),'compressed_bytes':len(zlib.compress(sequence))},
        'synchronization':{'format':'four unit-spaced markers then six interval symbols','searched_starts':max(0,len(markers)-9)},
        'error_correcting_structure':{'status':'NOT_IMPLEMENTED','reason':'This protocol repeats packets but defines no parity/code family; no error correction is inferred.'},
        'tests_used_for_admission':['disjoint_packet_repetition','full_search_gap_permutation_rank'],
        'criteria':{'minimum_disjoint_repetitions':2,'maximum_permutation_p':'1/20'},
        'pass':observed>=2 and native[p_id]<=F(1,20)}, receipt
