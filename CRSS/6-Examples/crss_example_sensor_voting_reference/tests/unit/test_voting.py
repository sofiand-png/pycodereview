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


def test_voting_all_plausible() -> None:
    cfg = _cfg()
    values = [1.0, 1.05, 0.98]
    result = compute_voted_value(values, cfg)
    assert 0.98 <= result <= 1.05


def test_voting_single_outlier() -> None:
    cfg = _cfg()
    values = [1.0, 1.02, 3.5]
    result = compute_voted_value(values, cfg)
    assert 1.0 <= result <= 1.02


def test_voting_no_plausible_pair_falls_back() -> None:
    cfg = _cfg()
    values = [1.0, 3.0, 5.0]
    result = compute_voted_value(values, cfg)
    assert result == cfg.fallback_value
