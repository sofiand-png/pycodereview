from crss_example_sensor_voting.crss_phase.markers import (
    critical_phase,
    non_critical_phase,
)


def test_critical_phase_preserves_behavior() -> None:
    calls = []

    @critical_phase
    def f(x: int) -> int:
        calls.append(x)
        return x + 1

    assert f(41) == 42
    assert calls == [41]


def test_non_critical_phase_preserves_behavior() -> None:
    calls = []

    @non_critical_phase
    def f(x: int) -> int:
        calls.append(x)
        return x * 2

    assert f(3) == 6
    assert calls == [3]
