# src/tests/unit/test_voting.py

from crss_example_sensor_voting.safety_logic.voting import (
    compute_voted_value,
    VOTING_STATUS_NORMAL,
    VOTING_STATUS_DEGRADED,
    VOTING_STATUS_FAILSAFE,
)
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


def test_voting_all_plausible_normal() -> None:
    cfg = _cfg()
    values = [1.0, 1.05, 1.02]
    result, status = compute_voted_value(values, cfg)
    assert status == VOTING_STATUS_NORMAL
    assert 0.99 <= result <= 1.06


def test_voting_single_outlier_degraded() -> None:
    cfg = _cfg()
    values = [1.0, 1.02, 3.0]
    result, status = compute_voted_value(values, cfg)
    assert status == VOTING_STATUS_DEGRADED
    assert 1.0 <= result <= 1.03


def test_voting_no_plausible_pair_failsafe() -> None:
    cfg = _cfg()
    values = [1.0, 3.0, 5.0]
    result, status = compute_voted_value(values, cfg)
    assert status == VOTING_STATUS_FAILSAFE
    assert result == SAFE_DEFAULT


def test_voting_wrong_length_triggers_failsafe() -> None:
    cfg = _cfg()
    values = [1.0, 2.0]  # not 3 values
    result, status = compute_voted_value(values, cfg)
    assert status == VOTING_STATUS_FAILSAFE
    assert result == SAFE_DEFAULT
