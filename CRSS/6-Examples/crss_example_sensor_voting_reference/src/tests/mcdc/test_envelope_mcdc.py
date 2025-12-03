from crss_example_sensor_voting.safety_logic.envelope import apply_safety_envelope
from crss_example_sensor_voting.config.model import SafetyConfig, SAFE_DEFAULT


def _cfg(max_delta: float = 0.5) -> SafetyConfig:
    return SafetyConfig(
        min_safe=0.0,
        max_safe=5.0,
        max_delta=max_delta,
        plausibility_threshold=0.2,
        fallback_value=SAFE_DEFAULT,
        initial_output=SAFE_DEFAULT,
    )


def test_mcdc_envelope_clamp_min_without_rate_limit() -> None:
    """MC/DC: exercise clamp-to-min branch with no rate limiting."""
    cfg = _cfg()
    prev = cfg.min_safe
    voted = -10.0  # far below min
    result = apply_safety_envelope(voted, prev, cfg)
    assert result == cfg.min_safe


def test_mcdc_envelope_clamp_max_without_rate_limit() -> None:
    """MC/DC: exercise clamp-to-max branch with no rate limiting."""
    cfg = _cfg()
    prev = cfg.max_safe
    voted = 10.0  # far above max
    result = apply_safety_envelope(voted, prev, cfg)
    assert result == cfg.max_safe


def test_mcdc_envelope_rate_limit_positive() -> None:
    """MC/DC: exercise positive rate-limit branch."""
    cfg = _cfg(max_delta=0.5)
    prev = 1.0
    voted = 3.0  # large upward step
    result = apply_safety_envelope(voted, prev, cfg)
    assert result - prev <= cfg.max_delta + 1e-9


def test_mcdc_envelope_rate_limit_negative() -> None:
    """MC/DC: exercise negative rate-limit branch."""
    cfg = _cfg(max_delta=0.5)
    prev = 3.0
    voted = 0.0  # large downward step
    result = apply_safety_envelope(voted, prev, cfg)
    assert prev - result <= cfg.max_delta + 1e-9


def test_mcdc_envelope_no_rate_limit_inside_band() -> None:
    """MC/DC: branch where no clamp and no rate limiting occurs."""
    cfg = _cfg(max_delta=2.0)
    prev = 1.0
    voted = 1.5  # inside [min, max], delta within max_delta
    result = apply_safety_envelope(voted, prev, cfg)
    assert result == voted
