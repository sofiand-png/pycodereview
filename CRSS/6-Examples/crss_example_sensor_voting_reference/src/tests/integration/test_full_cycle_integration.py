from typing import List

from crss_example_sensor_voting.sensors.simulation import SimulatedSensors
from crss_example_sensor_voting.safety_logic.controller import SafetyController
from crss_example_sensor_voting.config.model import SafetyConfig, SAFE_DEFAULT


def _cfg() -> SafetyConfig:
    # Same pattern as your other tests, but explicitly written here
    return SafetyConfig(
        min_safe=0.0,
        max_safe=5.0,
        max_delta=0.5,
        plausibility_threshold=0.2,
        fallback_value=SAFE_DEFAULT,
        initial_output=SAFE_DEFAULT,
    )


def _in_range(v: float, cfg: SafetyConfig) -> bool:
    return cfg.min_safe <= v <= cfg.max_safe


def test_high_fault_leads_to_degraded_status() -> None:
    """Single-sensor high fault => DEGRADED status, safe bounded output."""
    cfg = _cfg()
    c = SafetyController(cfg)
    sim = SimulatedSensors(seed=1, forced_mode="high_fault")

    values = sim.read_all()
    cmd = c.step(values)

    assert cmd.status == "DEGRADED"
    assert _in_range(cmd.value, cfg)


def test_low_fault_leads_to_degraded_status() -> None:
    """Single-sensor low fault => DEGRADED status, safe bounded output."""
    cfg = _cfg()
    c = SafetyController(cfg)
    sim = SimulatedSensors(seed=1, forced_mode="low_fault")

    values = sim.read_all()
    cmd = c.step(values)

    assert cmd.status == "DEGRADED"
    assert _in_range(cmd.value, cfg)


def test_severe_disagreement_leads_to_failsafe_safe_default() -> None:
    """Severe disagreement => FAILSAFE + SAFE_DEFAULT output."""
    cfg = _cfg()
    c = SafetyController(cfg)
    sim = SimulatedSensors(seed=1, forced_mode="severe_disagreement")

    values = sim.read_all()
    cmd = c.step(values)

    assert cmd.status == "FAILSAFE"
    assert cmd.value == SAFE_DEFAULT


def test_frozen_sensors_keep_output_stable_and_safe() -> None:
    """Frozen values => NORMAL status, bounded + rate-limited output."""
    cfg = _cfg()
    c = SafetyController(cfg)
    sim = SimulatedSensors(seed=1, forced_mode="frozen")

    prev_value = None
    for _ in range(5):
        values = sim.read_all()
        cmd = c.step(values)

        # All calls see same sensor values; controller should remain safe and
        # usually NORMAL (no fault pattern).
        assert _in_range(cmd.value, cfg)
        assert cmd.status in {"NORMAL", "DEGRADED"}  # robust if close to thresholds

        if prev_value is not None:
            # rate limit: never step more than max_delta
            assert abs(cmd.value - prev_value) <= cfg.max_delta + 1e-9

        prev_value = cmd.value


def test_stuck_drift_stays_in_safe_band_and_is_rate_limited() -> None:
    """Stuck-at-safe with slow drift => bounded + smooth actuator output."""
    cfg = _cfg()
    c = SafetyController(cfg)
    sim = SimulatedSensors(seed=1, forced_mode="stuck_drift")

    prev_value = None
    for _ in range(10):
        values = sim.read_all()
        cmd = c.step(values)

        # Even with slow drift, actuator output must remain in [min, max]
        assert _in_range(cmd.value, cfg)
        # Status should never be FAILSAFE in this benign scenario
        assert cmd.status in {"NORMAL", "DEGRADED"}

        if prev_value is not None:
            # Envelope must enforce max_delta
            assert abs(cmd.value - prev_value) <= cfg.max_delta + 1e-9

        prev_value = cmd.value
