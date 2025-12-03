from crss_example_sensor_voting.safety_logic.envelope import apply_safety_envelope
from crss_example_sensor_voting.config.model import SafetyConfig, SAFE_DEFAULT


def _cfg() -> SafetyConfig:
    return SafetyConfig(
        min_safe=0.0,
        max_safe=5.0,
        max_delta=0.5,
        plausibility_threshold=0.2,
        fallback_value=SAFE_DEFAULT,
        initial_output=SAFE_DEFAULT,
    )


def test_envelope_within_limits_no_rate_limit() -> None:
    cfg = _cfg()
    prev = 1.0
    voted = 1.3  # within max_delta and inside [min, max]
    result = apply_safety_envelope(voted, prev, cfg)
    assert result == voted


def test_envelope_clamps_to_min_without_rate_limit() -> None:
    """Value below min_safe with prev already at min_safe => pure clamp."""
    cfg = _cfg()
    prev = cfg.min_safe
    voted = -1.0
    result = apply_safety_envelope(voted, prev, cfg)
    assert result == cfg.min_safe


def test_envelope_clamps_to_max_without_rate_limit() -> None:
    """Value above max_safe with prev already at max_safe => pure clamp."""
    cfg = _cfg()
    prev = cfg.max_safe
    voted = 10.0
    result = apply_safety_envelope(voted, prev, cfg)
    assert result == cfg.max_safe


def test_envelope_rate_limited_up() -> None:
    cfg = _cfg()
    prev = 1.0
    voted = 3.0  # way higher => rate limitation must apply
    result = apply_safety_envelope(voted, prev, cfg)
    assert result - prev <= cfg.max_delta + 1e-9


def test_envelope_rate_limited_down() -> None:
    cfg = _cfg()
    prev = 3.0
    voted = 0.0  # way lower => rate limitation must apply
    result = apply_safety_envelope(voted, prev, cfg)
    assert prev - result <= cfg.max_delta + 1e-9
