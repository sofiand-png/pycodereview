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


def test_mcdc_envelope_clamp_min() -> None:
    cfg = _cfg()
    prev = 1.0
    voted = -10.0
    result = apply_safety_envelope(voted, prev, cfg)
    assert result == cfg.min_safe


def test_mcdc_envelope_clamp_max() -> None:
    cfg = _cfg()
    prev = 1.0
    voted = 10.0
    result = apply_safety_envelope(voted, prev, cfg)
    assert result == cfg.max_safe


def test_mcdc_envelope_rate_limit_positive() -> None:
    cfg = _cfg()
    prev = 1.0
    voted = 3.0
    result = apply_safety_envelope(voted, prev, cfg)
    assert result - prev <= cfg.max_delta + 1e-9


def test_mcdc_envelope_rate_limit_negative() -> None:
    cfg = _cfg()
    prev = 3.0
    voted = 0.0
    result = apply_safety_envelope(voted, prev, cfg)
    assert prev - result <= cfg.max_delta + 1e-9
