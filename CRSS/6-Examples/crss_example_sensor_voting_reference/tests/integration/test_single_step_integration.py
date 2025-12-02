from app.main_loop import run_single_step


def test_single_step_integration() -> None:
    cmd = run_single_step(seed=1)
    assert cmd["status"] == "NORMAL"
    assert 0.0 <= cmd["value"] <= 5.0
