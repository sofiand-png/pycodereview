from crss_phase.markers import critical_phase
from config.model import SafetyConfig


@critical_phase
def apply_safety_envelope(voted_value: float, previous_value: float, cfg: SafetyConfig) -> float:
    clamped = voted_value
    if clamped < cfg.min_safe:
        clamped = cfg.min_safe
    elif clamped > cfg.max_safe:
        clamped = cfg.max_safe

    delta = clamped - previous_value
    if delta > cfg.max_delta:
        return previous_value + cfg.max_delta
    if delta < -cfg.max_delta:
        return previous_value - cfg.max_delta

    return clamped
