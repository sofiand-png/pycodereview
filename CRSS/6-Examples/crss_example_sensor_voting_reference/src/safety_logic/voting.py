from typing import List, Tuple

from crss_phase.markers import critical_phase
from config.model import SafetyConfig


def _pairwise_indices() -> List[Tuple[int, int]]:
    return [(0, 1), (0, 2), (1, 2)]


@critical_phase
def compute_voted_value(values: List[float], cfg: SafetyConfig) -> float:
    if len(values) != 3:
        return cfg.fallback_value

    pairs = _pairwise_indices()
    threshold = cfg.plausibility_threshold
    chosen_pair = None

    for i, j in pairs:
        if abs(values[i] - values[j]) <= threshold:
            chosen_pair = (values[i], values[j])
            break

    if chosen_pair is None:
        return cfg.fallback_value

    return (chosen_pair[0] + chosen_pair[1]) / 2.0
