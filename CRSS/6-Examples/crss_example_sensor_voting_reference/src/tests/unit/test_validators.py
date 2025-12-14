import pytest

from crss_example_sensor_voting.config.model import SafetyConfig
from crss_example_sensor_voting.safety_logic.validator import validate_config_domain


def _valid_cfg() -> SafetyConfig:
    """
    Construct a known-good config that should pass validate_config_domain().
    Keep values safely away from boundaries so we can tweak one field at a time.
    """
    return SafetyConfig(
        min_safe=-1.0,
        max_safe=+1.0,
        max_delta=0.5,
        plausibility_threshold=0.0,
        fallback_value=0.0,
        initial_output=0.0,
    )


def test_validate_config_domain_ok_returns_same_object():
    cfg = _valid_cfg()
    out = validate_config_domain(cfg)
    # The function returns cfg (no copy); this asserts that behavior explicitly.
    assert out is cfg


@pytest.mark.parametrize(
    "mutate, msg_substr",
    [
        (lambda c: c.__class__(**{**c.__dict__, "min_safe": 1.0, "max_safe": 1.0}), "min_safe must be < max_safe"),
        (lambda c: c.__class__(**{**c.__dict__, "max_delta": 0.0}), "max_delta must be > 0"),
        (lambda c: c.__class__(**{**c.__dict__, "max_delta": -0.1}), "max_delta must be > 0"),
        (lambda c: c.__class__(**{**c.__dict__, "plausibility_threshold": -0.01}), "plausibility_threshold must be >= 0"),
        (lambda c: c.__class__(**{**c.__dict__, "fallback_value": 2.0}), "fallback_value must lie within"),
        (lambda c: c.__class__(**{**c.__dict__, "fallback_value": -2.0}), "fallback_value must lie within"),
        (lambda c: c.__class__(**{**c.__dict__, "initial_output": 2.0}), "initial_output must lie within"),
        (lambda c: c.__class__(**{**c.__dict__, "initial_output": -2.0}), "initial_output must lie within"),
    ],
)
def test_validate_config_domain_raises_on_invalid_ranges(mutate, msg_substr):
    cfg = _valid_cfg()
    bad = mutate(cfg)
    with pytest.raises(ValueError, match=msg_substr):
        validate_config_domain(bad)


def test_validate_config_domain_safe_default_within_envelope_passes():
    """
    Covers the branch where SAFE_DEFAULT exists (or doesn't) but does not trigger an error.
    If SAFE_DEFAULT is None, this test still passes because the check is skipped.
    """
    cfg = _valid_cfg()
    validate_config_domain(cfg)  # Should not raise.


def test_validate_config_domain_safe_default_out_of_range_raises(monkeypatch):
    """
    The validator checks a module-level SAFE_DEFAULT constant. To cover the raise branch,
    we monkeypatch it to an out-of-range value.
    """
    import crss_example_sensor_voting.safety_logic.validator as v

    cfg = _valid_cfg()

    # Force SAFE_DEFAULT to be out of envelope.
    monkeypatch.setattr(v, "SAFE_DEFAULT", 999.0, raising=True)

    with pytest.raises(ValueError, match="SAFE_DEFAULT must lie within"):
        v.validate_config_domain(cfg)
