from safety_logic.voting import compute_voted_value
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


def test_mcdc_pair_01_plausible() -> None:
    cfg = _cfg()
    values = [1.0, 1.1, 2.0]
    result = compute_voted_value(values, cfg)
    assert result != cfg.fallback_value


def test_mcdc_pair_02_plausible() -> None:
    cfg = _cfg()
    values = [1.0, 2.0, 1.05]
    result = compute_voted_value(values, cfg)
    assert result != cfg.fallback_value


def test_mcdc_pair_12_plausible() -> None:
    cfg = _cfg()
    values = [2.0, 1.0, 1.05]
    result = compute_voted_value(values, cfg)
    assert result != cfg.fallback_value


def test_mcdc_no_pair_plausible() -> None:
    cfg = _cfg()
    values = [1.0, 3.0, 5.0]
    result = compute_voted_value(values, cfg)
    assert result == cfg.fallback_value
