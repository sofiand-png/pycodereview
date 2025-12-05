
"""Strict-A voting logic (@critical).

Requirements:
SV-FUNC-02 — TMR voting

SV-FLT-01 — Single-sensor fault tolerance

SV-FLT-02 — Severe disagreement detection
"""


from typing import List, Tuple

from crss_example_sensor_voting.crss_phase.markers import critical_phase
from crss_example_sensor_voting.config.model import SafetyConfig


VOTING_STATUS_NORMAL = "NORMAL"
VOTING_STATUS_DEGRADED = "DEGRADED"
VOTING_STATUS_FAILSAFE = "FAILSAFE"


def _pairwise_indices() -> List[Tuple[int, int]]:
    # Exactly three sensors: indices 0, 1, 2
    return [(0, 1), (0, 2), (1, 2)]


def _pairwise_plausibility(values: List[float], threshold: float) -> List[Tuple[int, int]]:
    plausible_pairs: List[Tuple[int, int]] = []
    for i, j in _pairwise_indices():
        if abs(values[i] - values[j]) <= threshold:
            plausible_pairs.append((i, j))
    return plausible_pairs


@critical_phase
def compute_voted_value(values: List[float], cfg: SafetyConfig) -> Tuple[float, str]:
    """Compute a voted value and voting status from three sensors.

    Rules:
    - If all three sensors are mutually plausible (all pairwise deltas
      within threshold), the mean of all three is used (NORMAL).
    - If at least one plausible pair exists but not all three mutually
      plausible, the first plausible pair in fixed order is used
      (DEGRADED).
    - If no plausible pair exists, SAFE_DEFAULT (cfg.fallback_value) is
      returned (FAILSAFE).
    - If len(values) != 3, SAFE_DEFAULT is returned (FAILSAFE).
    """  # noqa: D401
    if len(values) != 3:
        return cfg.fallback_value, VOTING_STATUS_FAILSAFE

    threshold = cfg.plausibility_threshold
    pairs = _pairwise_plausibility(values, threshold)

    if not pairs:
        # no plausible pair
        return cfg.fallback_value, VOTING_STATUS_FAILSAFE

    # Check if all three are mutually plausible: then average all three.
    # For three sensors, mutual plausibility == 3 plausible pairs.
    if len(pairs) == 3:
        avg_all = (values[0] + values[1] + values[2]) / 3.0
        return avg_all, VOTING_STATUS_NORMAL

    # Otherwise, use the first plausible pair deterministically.
    i, j = pairs[0]
    mean_pair = (values[i] + values[j]) / 2.0
    return mean_pair, VOTING_STATUS_DEGRADED
