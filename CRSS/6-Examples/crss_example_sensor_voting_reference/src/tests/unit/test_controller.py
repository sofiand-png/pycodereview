from crss_example_sensor_voting.safety_logic.controller import SafetyController
from crss_example_sensor_voting.config.model import SafetyConfig, SAFE_DEFAULT
from crss_example_sensor_voting.app.main_loop import run_single_step

def _cfg() -> SafetyConfig:
    return SafetyConfig(
        min_safe=0.0,
        max_safe=5.0,
        max_delta=1.0,
        plausibility_threshold=0.2,
        fallback_value=SAFE_DEFAULT,
        initial_output=SAFE_DEFAULT,
    )


def test_controller_normal_status() -> None:
    cfg = _cfg()
    c = SafetyController(cfg)
    cmd = c.step([1.0, 1.05, 1.02])
    assert cmd.status == "NORMAL"
    assert 0.0 <= cmd.value <= 5.0


def test_controller_degraded_status() -> None:
    cfg = _cfg()
    c = SafetyController(cfg)
    cmd = c.step([1.0, 1.05, 3.0])
    assert cmd.status == "DEGRADED"


def test_controller_failsafe_status_and_prev_validation() -> None:
    cfg = _cfg()
    c = SafetyController(cfg)
    # Force previous value out of range to exercise validation branch
    c._previous_value = 10.0  # type: ignore[attr-defined]
    cmd = c.step([1.0, 3.0, 5.0])  # no plausible pair => FAILSAFE
    assert cmd.status == "FAILSAFE"
    assert 0.0 <= cmd.value <= 5.0


def test_run_single_step_returns_command() -> None:
    cmd = run_single_step(seed=1)
    assert isinstance(cmd, dict)
    assert "value" in cmd
    assert "status" in cmd
