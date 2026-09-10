"""
CR002 — QGC T2 Prescreening + K1-Frozen Hardware Envelope

Component B: computational substrate-response model for candidate
trigger mechanisms. Computes a coupling score per candidate under
parameterized assumptions about the SAM-silent pathway-directness
factor. Tests ranking robustness across parameter variation.

100% DISCLAIMER — read CR002_PRECOMMIT.md disclaimer block before
interpreting any output. This is internal-consistency-of-SAM-predictions
ONLY. Not empirical SAM validation. Not hardware test.
"""

import csv
import json
import os
import math
import random
from dataclasses import dataclass, asdict
from typing import Dict, List, Tuple


# ── Candidate trigger mechanisms (from QGC_HARDWARE_SKETCH §2) ──────

@dataclass
class Candidate:
    name: str
    stress_energy_magnitude_log10: float  # log10 of relative stress-energy perturbation
    spatial_localization: float            # 0..1 (higher = more localized to target site)
    temporal_localization: float           # 0..1 (higher = sharper event in time)
    pathway_directness_baseline: float    # 0..1 (higher = more direct stress-energy → substrate)
    notes: str

    def score(self, pathway_multiplier: float = 1.0) -> float:
        """Coupling score under given pathway-directness multiplier."""
        pathway = self.pathway_directness_baseline * pathway_multiplier
        pathway = max(0.0, min(1.0, pathway))  # clamp to [0, 1]
        # log-scale score: stress-energy is in log10, others are linear factors
        # Score is (linear product) × 10^(stress_energy_log10) for log-scale magnitude
        linear_factor = self.spatial_localization * self.temporal_localization * pathway
        if linear_factor <= 0:
            return float('-inf')
        log_score = (
            self.stress_energy_magnitude_log10
            + math.log10(self.spatial_localization)
            + math.log10(self.temporal_localization)
            + math.log10(pathway)
        )
        return log_score


CANDIDATES = [
    Candidate(
        name='mass_density_modulation_BEC',
        stress_energy_magnitude_log10=-2.0,   # BEC modulation depth at trap volume
        spatial_localization=0.95,             # optical trap precision
        temporal_localization=0.5,             # atom-transit timescales
        pathway_directness_baseline=0.9,       # direct mass-density coupling
        notes='cooled-atom / BEC density transients at trap site',
    ),
    Candidate(
        name='MEMS_pressure',
        stress_energy_magnitude_log10=-3.0,   # mechanical density modulation
        spatial_localization=0.8,              # MEMS device geometry
        temporal_localization=0.5,             # kHz-MHz mechanical timescales
        pathway_directness_baseline=0.85,      # direct density modulation
        notes='mechanical pressure transducer',
    ),
    Candidate(
        name='EM_laser_focal',
        stress_energy_magnitude_log10=-2.5,   # high-intensity laser focal energy density
        spatial_localization=0.9,              # diffraction-limited focus
        temporal_localization=0.95,            # femtosecond pulse possible
        pathway_directness_baseline=0.45,      # via EM stress-energy (indirect)
        notes='high-intensity laser at site focal volume',
    ),
    Candidate(
        name='acoustic_phonon',
        stress_energy_magnitude_log10=-10.0,  # phonon energy per atom is small
        spatial_localization=0.25,             # phonons propagate
        temporal_localization=0.2,             # continuous-wave mode
        pathway_directness_baseline=0.2,       # weak stress-energy via lattice
        notes='piezoelectric phonon excitation',
    ),
    Candidate(
        name='charge_pulse_low_field',
        stress_energy_magnitude_log10=-6.0,   # EM field energy at moderate field
        spatial_localization=0.85,             # electrode placement
        temporal_localization=0.95,            # nanosecond pulse
        pathway_directness_baseline=0.15,      # very weak via EM stress-energy
        notes='charge pulse via electrode at low E field',
    ),
    Candidate(
        name='spontaneous_baseline',
        stress_energy_magnitude_log10=-20.0,  # essentially zero perturbation
        spatial_localization=1.0,              # per-site reference
        temporal_localization=0.5,             # always-on background
        pathway_directness_baseline=1.0,       # native
        notes='no trigger; substrate native baseline activity (reference)',
    ),
]

# Ordering of candidates by name → rank for the expected (theoretical) ranking
EXPECTED_RANKING_BY_NAME = [
    'mass_density_modulation_BEC',     # #1
    'MEMS_pressure',                    # #2
    'EM_laser_focal',                   # #3
    'acoustic_phonon',                  # #4
    'charge_pulse_low_field',           # #5
    'spontaneous_baseline',             # #REF (lowest score by construction)
]


def rank_by_score(scores: Dict[str, float]) -> List[str]:
    """Return candidate names sorted by score descending."""
    return sorted(scores.keys(), key=lambda n: -scores[n])


def compute_baseline_ranking() -> Tuple[Dict[str, float], List[str]]:
    """Baseline scores using pathway_multiplier = 1.0."""
    scores = {c.name: c.score(1.0) for c in CANDIDATES}
    ranking = rank_by_score(scores)
    return scores, ranking


def assess_robustness(num_samples: int = 1000, rng_seed: int = 42) -> Dict:
    """Vary pathway-directness multiplier across [0.25, 4.0] uniformly in log
    space; check how often the resulting ranking matches the baseline ranking.
    """
    rng = random.Random(rng_seed)
    baseline_scores, baseline_ranking = compute_baseline_ranking()

    matches = 0
    partial_matches_top3 = 0
    partial_matches_top5 = 0
    samples_per_candidate_scores: Dict[str, List[float]] = {
        c.name: [] for c in CANDIDATES
    }

    for _ in range(num_samples):
        # Sample multiplier in log-uniform [0.25, 4.0]
        log_mult = rng.uniform(math.log10(0.25), math.log10(4.0))
        mult = 10.0 ** log_mult
        scores = {c.name: c.score(mult) for c in CANDIDATES}
        for name, score in scores.items():
            samples_per_candidate_scores[name].append(score)
        ranking = rank_by_score(scores)
        if ranking == baseline_ranking:
            matches += 1
        if ranking[:3] == baseline_ranking[:3]:
            partial_matches_top3 += 1
        if ranking[:5] == baseline_ranking[:5]:
            partial_matches_top5 += 1

    return {
        'num_samples': num_samples,
        'pathway_multiplier_range': [0.25, 4.0],
        'baseline_ranking': baseline_ranking,
        'baseline_scores': baseline_scores,
        'exact_match_fraction': matches / num_samples,
        'top3_match_fraction': partial_matches_top3 / num_samples,
        'top5_match_fraction': partial_matches_top5 / num_samples,
        'samples_per_candidate_scores': samples_per_candidate_scores,
    }


def write_scores_csv(robustness: Dict, path: str) -> None:
    """Write per-candidate per-sample scores."""
    candidates = list(robustness['samples_per_candidate_scores'].keys())
    num_samples = robustness['num_samples']
    with open(path, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['sample_idx'] + candidates)
        for i in range(num_samples):
            row = [i]
            for c in candidates:
                row.append(round(robustness['samples_per_candidate_scores'][c][i], 4))
            writer.writerow(row)


def main():
    folder = os.path.dirname(os.path.abspath(__file__))
    print('CR002 — QGC T2 Prescreening + K1-Frozen Hardware Envelope')
    print('Component B: Computational substrate-response model')
    print('=' * 60)
    print()
    print('DISCLAIMER REMINDER:')
    print('  This is an internal-consistency test of SAM hardware')
    print('  predictions. NOT empirical SAM validation. NOT hardware')
    print('  test. See CR002_PRECOMMIT.md disclaimer block.')
    print()

    # Compute baseline
    baseline_scores, baseline_ranking = compute_baseline_ranking()
    print('Baseline coupling scores (pathway_multiplier = 1.0):')
    print('-' * 60)
    for c_name in baseline_ranking:
        c = next(c for c in CANDIDATES if c.name == c_name)
        print(f'  {c.name:<35} score = {baseline_scores[c_name]:>8.4f}  {c.notes}')
    print()

    print('Baseline ranking:')
    for i, name in enumerate(baseline_ranking, 1):
        print(f'  {i}. {name}')
    print()

    print(f'Expected (theoretical) ranking from PRECOMMIT §A:')
    for i, name in enumerate(EXPECTED_RANKING_BY_NAME, 1):
        print(f'  {i}. {name}')
    print()

    # V-2: baseline matches expected
    v2_match = baseline_ranking == EXPECTED_RANKING_BY_NAME
    print(f'V-2 (baseline matches expected theoretical ranking): '
          f'{"PASS" if v2_match else "FAIL"}')
    print()

    # Robustness assessment
    print('Robustness assessment:')
    print('  Sampling pathway_multiplier across [0.25, 4.0] log-uniformly...')
    robustness = assess_robustness(num_samples=1000)
    print(f'  num_samples: {robustness["num_samples"]}')
    print(f'  Exact-match (full ranking matches baseline): '
          f'{robustness["exact_match_fraction"]*100:.1f}%')
    print(f'  Top-3 match: {robustness["top3_match_fraction"]*100:.1f}%')
    print(f'  Top-5 match: {robustness["top5_match_fraction"]*100:.1f}%')
    print()

    # V-3: robust if exact-match >= 80%
    v3_robust = robustness['exact_match_fraction'] >= 0.80
    print(f'V-3 (ranking robust under parameter variation, ≥80% '
          f'exact match): {"PASS" if v3_robust else "BOUNDARY/FAIL"}')
    print()

    # Verdict — honors precommit's B1 (V-3 fragile) and B2 (1-2 swaps)
    # Count position differences between baseline and expected
    position_diffs = sum(
        1 for i, name in enumerate(baseline_ranking)
        if name != EXPECTED_RANKING_BY_NAME[i]
    )
    # Count adjacent transpositions needed to sort one into the other
    # (a single pair swap = 2 position differences)
    pair_swaps = position_diffs // 2
    # Top-1 candidate must match for B2 to apply
    top_matches = baseline_ranking[0] == EXPECTED_RANKING_BY_NAME[0]
    # Bottom (reference) must match
    bottom_matches = baseline_ranking[-1] == EXPECTED_RANKING_BY_NAME[-1]

    if v2_match and v3_robust:
        verdict = 'PASS'
    elif v2_match and not v3_robust:
        verdict = 'BOUNDARY'  # B1: agree but fragile
    elif top_matches and bottom_matches and pair_swaps <= 2 and v3_robust:
        verdict = 'BOUNDARY'  # B2: top/bottom right, 1-2 pair swaps in middle
    else:
        verdict = 'FAIL'  # F1: substantially different rankings

    print(f'Position differences vs expected: {position_diffs}')
    print(f'Inferred pair swaps: {pair_swaps}')
    print(f'Top candidate matches: {top_matches}')
    print(f'Bottom (reference) matches: {bottom_matches}')

    print('=' * 60)
    print(f'CR002 COMPONENT B VERDICT: {verdict}')
    print()
    print(f'(Component A ranking and Component C K1 envelope are in')
    print(f' CR002_PRECOMMIT.md; this runner exercises component B only.)')
    print()

    # Write outputs
    write_scores_csv(robustness,
                     os.path.join(folder, 'CR002_candidate_scores.csv'))

    summary = {
        'cr_id': 'CR002',
        'branch': '18_SAM_NATIVE_QC',
        'title': 'QGC T2 Prescreening + K1-Frozen Hardware Envelope',
        'disclaimer': (
            'INTERNAL-CONSISTENCY ONLY. CR002 does NOT validate SAM '
            'empirically and does NOT constitute a hardware test. See '
            'CR002_PRECOMMIT.md disclaimer block for full framing.'
        ),
        'component_B_verdict': verdict,
        'baseline_ranking': baseline_ranking,
        'expected_ranking': EXPECTED_RANKING_BY_NAME,
        'baseline_ranking_matches_expected': v2_match,
        'baseline_scores': {n: round(s, 4) for n, s in baseline_scores.items()},
        'robustness_assessment': {
            'num_samples': robustness['num_samples'],
            'pathway_multiplier_range': robustness['pathway_multiplier_range'],
            'exact_match_fraction': round(robustness['exact_match_fraction'], 4),
            'top3_match_fraction': round(robustness['top3_match_fraction'], 4),
            'top5_match_fraction': round(robustness['top5_match_fraction'], 4),
        },
        'verification_gates': {
            'V-2_baseline_matches_expected': v2_match,
            'V-3_ranking_robust_80pct': v3_robust,
            'position_differences': position_diffs,
            'pair_swaps': pair_swaps,
            'top_candidate_matches': top_matches,
            'bottom_reference_matches': bottom_matches,
        },
    }
    with open(os.path.join(folder, 'CR002_summary.json'), 'w',
              encoding='utf-8') as f:
        json.dump(summary, f, indent=2)

    print(f'Candidate scores : CR002_candidate_scores.csv')
    print(f'Summary JSON     : CR002_summary.json')


if __name__ == '__main__':
    main()
