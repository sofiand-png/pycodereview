from app.main_loop import run_single_step


def test_run_single_step_returns_command() -> None:
    cmd = run_single_step(seed=1)
    assert isinstance(cmd, dict)
    assert "value" in cmd
    assert "status" in cmd
