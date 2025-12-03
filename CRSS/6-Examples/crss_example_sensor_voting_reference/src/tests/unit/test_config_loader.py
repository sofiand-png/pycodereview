from crss_example_sensor_voting.config.loader import load_config
from crss_example_sensor_voting.config.model import SAFE_DEFAULT


def test_load_config_returns_default() -> None:
    cfg = load_config()
    assert cfg.fallback_value == SAFE_DEFAULT
    assert cfg.min_safe < cfg.max_safe
    assert cfg.initial_output == SAFE_DEFAULT
