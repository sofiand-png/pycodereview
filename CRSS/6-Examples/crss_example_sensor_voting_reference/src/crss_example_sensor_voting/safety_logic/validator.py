"""Strict-A domain validator (non-critical).

This module provides *Level-A domain validation* that checks consistency of
already-parsed, already-typed, bounded configuration structures before they are
used by Strict-A @critical kernels.

It is intentionally non-critical:
- it may raise exceptions on invalid configuration,
- it must not perform I/O,
- it must remain pure and deterministic.

Used by the Strict-B inner orchestrator as part of the Level-A data entry chain.
"""

from __future__ import annotations

from crss_example_sensor_voting.crss_phase.markers import non_critical_phase
from crss_example_sensor_voting.config.model import SafetyConfig, SAFE_DEFAULT


@non_critical_phase
def validate_config_domain(cfg: SafetyConfig) -> SafetyConfig:
    """Validate SafetyConfig domain constraints.

    Raises:
        ValueError: if configuration violates Level-A domain assumptions.
    """  # noqa: D401
    # Basic ordering
    if cfg.min_safe >= cfg.max_safe:
        raise ValueError("Invalid SafetyConfig: min_safe must be < max_safe")

    # Bounds and non-negativity
    if cfg.max_delta <= 0.0:
        raise ValueError("Invalid SafetyConfig: max_delta must be > 0")

    if cfg.plausibility_threshold < 0.0:
        raise ValueError("Invalid SafetyConfig: plausibility_threshold must be >= 0")

    # SAFE_DEFAULT / fallback behavior must be within envelope.
    if not (cfg.min_safe <= cfg.fallback_value <= cfg.max_safe):
        raise ValueError("Invalid SafetyConfig: fallback_value must lie within [min_safe, max_safe]")

    if SAFE_DEFAULT is not None and not (cfg.min_safe <= SAFE_DEFAULT <= cfg.max_safe):
        raise ValueError("Invalid SafetyConfig: SAFE_DEFAULT must lie within [min_safe, max_safe]")

    # Initial output should start safe.
    if not (cfg.min_safe <= cfg.initial_output <= cfg.max_safe):
        raise ValueError("Invalid SafetyConfig: initial_output must lie within [min_safe, max_safe]")

    return cfg
