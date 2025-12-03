from crss_example_sensor_voting.safety_logic.controller import SafetyController
from crss_example_sensor_voting.config.model import SafetyConfig, SAFE_DEFAULT


def _cfg() -> SafetyConfig:
    return SafetyConfig(
        min_safe=0.0,
        max_safe=5.0,
        max_delta=1.0,
        plausibility_threshold=0.2,
        fallback_value=SAFE_DEFAULT,
        initial_output=SAFE_DEFAULT,
    )


def test_mcdc_controller_normal_path() -> None:
    cfg = _cfg()
    c = SafetyController(cfg)
    cmd = c.step([1.0, 1.05, 1.02])
    assert cmd.status == "NORMAL"


def test_mcdc_controller_degraded_path() -> None:
    cfg = _cfg()
    c = SafetyController(cfg)
    cmd = c.step([1.0, 1.05, 3.0])
    assert cmd.status == "DEGRADED"


def test_mcdc_controller_failsafe_path() -> None:
    cfg = _cfg()
    c = SafetyController(cfg)
    cmd = c.step([1.0, 3.0, 5.0])
    assert cmd.status == "FAILSAFE"
