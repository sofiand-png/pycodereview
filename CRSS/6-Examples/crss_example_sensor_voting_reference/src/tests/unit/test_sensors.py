from typing import List

from crss_example_sensor_voting.sensors.simulation import SimulatedSensors


def _within_range(values: List[float], low: float = 0.0, high: float = 5.0) -> bool:
    return all(low <= v <= high for v in values)


def test_simulator_normal_mode() -> None:
    sim = SimulatedSensors(seed=1, forced_mode="normal")
    values = sim.read_all()
    assert len(values) == 3
    assert _within_range(values, 0.0, 5.0)


def test_simulator_high_fault_mode() -> None:
    sim = SimulatedSensors(seed=1, forced_mode="high_fault")
    values = sim.read_all()
    assert len(values) == 3
    # Expect one channel significantly higher than the others (large spread),
    # not necessarily numerically outside [0.0, 5.0].
    spread = max(values) - min(values)
    assert spread > 1.0



def test_simulator_low_fault_mode() -> None:
    sim = SimulatedSensors(seed=1, forced_mode="low_fault")
    values = sim.read_all()
    assert len(values) == 3
    spread = max(values) - min(values)
    assert spread > 1.0



def test_simulator_severe_disagreement_mode() -> None:
    sim = SimulatedSensors(seed=1, forced_mode="severe_disagreement")
    values = sim.read_all()
    assert len(values) == 3
    # Large spread between min and max
    assert max(values) - min(values) > 1.5


def test_simulator_frozen_mode_returns_same_values() -> None:
    sim = SimulatedSensors(seed=1, forced_mode="frozen")
    first = sim.read_all()
    second = sim.read_all()
    assert first == second
    assert len(first) == 3


def test_simulator_stuck_drift_mode_slowly_changes() -> None:
    sim = SimulatedSensors(seed=1, forced_mode="stuck_drift")
    readings = [sim.read_all() for _ in range(10)]
    # Always within safe-ish band
    for vals in readings:
        assert len(vals) == 3
        assert _within_range(vals, 0.0, 5.0)

    # Check that at least one value changed over time
    v0_first = readings[0][0]
    assert any(abs(r[0] - v0_first) > 1e-6 for r in readings[1:])
