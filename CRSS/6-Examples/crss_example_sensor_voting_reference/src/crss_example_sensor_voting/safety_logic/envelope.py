"""Strict-A safety envelope (@critical)

Requirements:
SV-SAF-01 — Envelope clamp

SV-SAF-02 — Rate limiting

SV-SAF-03 — SAFE_DEFAULT application

SV-SAF-04 — Deterministic Strict-A

SV-FLT-02 — Severe disagreement - FAILSAFE
"""


from crss_example_sensor_voting.crss_phase.markers import critical_phase
from crss_example_sensor_voting.config.model import SafetyConfig


@critical_phase
def apply_safety_envelope(voted_value: float, previous_value: float, cfg: SafetyConfig) -> float:
    """Apply the safety envelope to the voted value.
    Requirements:
        SV-SAF-01, SV-SAF-02, SV-SAF-03, SV-FLT-02

    Steps (deterministic):

    1. Hard clamp the voted value into [min_safe, max_safe].
    2. Apply rate limiting based on max_delta.
    """  # noqa: D401
    # Step 1: clamp
    clamped = voted_value
    if clamped < cfg.min_safe:
        clamped = cfg.min_safe
    elif clamped > cfg.max_safe:
        clamped = cfg.max_safe

    # Step 2: rate limit
    delta = clamped - previous_value
    if delta > cfg.max_delta:
        return previous_value + cfg.max_delta
    if delta < -cfg.max_delta:
        return previous_value - cfg.max_delta

    return clamped
