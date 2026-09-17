"""Receiver: wave samples only; no message, emission times, or source controls."""
from statistics import median


def decode(samples):
    if len(samples) < 20:
        return {'markers': [], 'packets': []}
    envelope = [abs(v) for v in samples]
    baseline = median(envelope)
    if baseline <= 0:
        return {'markers': [], 'packets': []}
    active = [i for i, v in enumerate(envelope) if v - baseline > .03 * baseline]
    groups = []
    for i in active:
        if not groups or i - groups[-1][-1] > 2:
            groups.append([])
        groups[-1].append(i)
    markers = [max(g, key=lambda i: envelope[i]) for g in groups if len(g) >= 3]
    packets = []
    cursor = 0
    # Protocol: four sync markers separated by one unit, then six data gaps.
    # No prime membership or expected sequence is consulted.
    while cursor + 9 < len(markers):
        block = markers[cursor:cursor + 10]
        sync = [block[i + 1] - block[i] for i in range(3)]
        unit = median(sync)
        if unit > 0 and max(abs(v / unit - 1) for v in sync) <= .12:
            ratios = [(block[i + 1] - block[i]) / unit for i in range(3, 9)]
            values = [round(v) for v in ratios]
            if min(values) >= 1 and max(abs(a - b) for a, b in zip(ratios, values)) <= .12:
                packets.append({'start_sample': block[0], 'unit_samples': unit,
                                'intervals': values, 'measured_ratios': ratios})
                cursor += 10
                continue
        cursor += 1
    return {'baseline': baseline, 'markers': markers, 'packets': packets}
