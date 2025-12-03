from crss_example_sensor_voting.app.main_loop import run_single_step


def test_single_step_integration_seeded() -> None:
    cmd = run_single_step(seed=1)
    assert cmd["status"] in {"NORMAL", "DEGRADED", "FAILSAFE"}
    assert 0.0 <= cmd["value"] <= 5.0
