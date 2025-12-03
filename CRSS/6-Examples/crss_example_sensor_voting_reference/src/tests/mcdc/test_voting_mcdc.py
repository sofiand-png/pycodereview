# src/tests/mcdc/test_voting_mcdc.py

from crss_example_sensor_voting.safety_logic.voting import compute_voted_value
from crss_example_sensor_voting.config.model import SafetyConfig, SAFE_DEFAULT


def _cfg(threshold: float = 0.2) -> SafetyConfig:
    return SafetyConfig(
        min_safe=0.0,
        max_safe=5.0,
        max_delta=0.5,
        plausibility_threshold=threshold,
        fallback_value=SAFE_DEFAULT,
        initial_output=SAFE_DEFAULT,
    )


def test_mcdc_all_pairs_plausible() -> None:
    cfg = _cfg()
    values = [1.0, 1.05, 1.02]
    result, _ = compute_voted_value(values, cfg)
    assert result != cfg.fallback_value


def test_mcdc_only_pair_01_plausible() -> None:
    cfg = _cfg()
    values = [1.0, 1.05, 2.0]
    result, _ = compute_voted_value(values, cfg)
    assert result != cfg.fallback_value


def test_mcdc_only_pair_02_plausible() -> None:
    cfg = _cfg()
    values = [1.0, 2.0, 1.05]
    result, _ = compute_voted_value(values, cfg)
    assert result != cfg.fallback_value


def test_mcdc_only_pair_12_plausible() -> None:
    cfg = _cfg()
    values = [2.0, 1.0, 1.05]
    result, _ = compute_voted_value(values, cfg)
    assert result != cfg.fallback_value


def test_mcdc_no_pair_plausible_fallback() -> None:
    cfg = _cfg()
    values = [1.0, 3.0, 5.0]
    result, _ = compute_voted_value(values, cfg)
    assert result == cfg.fallback_value


def test_mcdc_wrong_length_input() -> None:
    cfg = _cfg()
    values = [1.0, 2.0]  # not 3 values
    result, _ = compute_voted_value(values, cfg)
    assert result == cfg.fallback_value
