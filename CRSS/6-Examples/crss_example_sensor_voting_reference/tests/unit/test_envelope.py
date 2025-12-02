from safety_logic.envelope import apply_safety_envelope
from config.model import SafetyConfig


def _cfg() -> SafetyConfig:
    return SafetyConfig(
        min_safe=0.0,
        max_safe=5.0,
        max_delta=0.5,
        plausibility_threshold=0.2,
        fallback_value=0.0,
        initial_output=0.0,
    )


def test_envelope_within_limits_no_rate_limit() -> None:
    cfg = _cfg()
    prev = 1.0
    voted = 1.3
    result = apply_safety_envelope(voted, prev, cfg)
    assert result == voted


def test_envelope_clamps_to_min() -> None:
    cfg = _cfg()
    prev = 1.0
    voted = -1.0
    result = apply_safety_envelope(voted, prev, cfg)
    assert result == cfg.min_safe


def test_envelope_clamps_to_max() -> None:
    cfg = _cfg()
    prev = 1.0
    voted = 10.0
    result = apply_safety_envelope(voted, prev, cfg)
    assert result == cfg.max_safe


def test_envelope_rate_limited_up() -> None:
    cfg = _cfg()
    prev = 1.0
    voted = 2.0
    result = apply_safety_envelope(voted, prev, cfg)
    assert result - prev <= cfg.max_delta + 1e-9


def test_envelope_rate_limited_down() -> None:
    cfg = _cfg()
    prev = 2.0
    voted = 0.0
    result = apply_safety_envelope(voted, prev, cfg)
    assert prev - result <= cfg.max_delta + 1e-9
