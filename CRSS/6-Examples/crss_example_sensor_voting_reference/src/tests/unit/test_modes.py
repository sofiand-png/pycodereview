# src/tests/unit/test_modes.py

from crss_example_sensor_voting.crss_modes.modes import MODES


def test_modes_metadata_is_defined() -> None:
    assert MODES
    assert any(m.name == "Strict-A" for m in MODES)
    assert any(m.profile == "Strict" for m in MODES)
