from crss_example_sensor_voting.io.json_protocol import (
    SensorFrame,
    ActuatorRequest,
    sensor_frame_to_json,
    sensor_frame_from_json,
    actuator_request_to_json,
    validate_sensor_frame,
)
from crss_example_sensor_voting.config.model import SafetyConfig, SAFE_DEFAULT


def _cfg() -> SafetyConfig:
    return SafetyConfig(
        min_safe=0.0,
        max_safe=5.0,
        max_delta=0.5,
        plausibility_threshold=0.2,
        fallback_value=SAFE_DEFAULT,
        initial_output=SAFE_DEFAULT,
    )


def test_sensor_frame_roundtrip() -> None:
    frame = SensorFrame(
        sensor_ids=["T1", "T2", "T3"],
        unit="degC",
        values=[1.0, 1.1, 1.2],
        timestamp=123.0,
        source_status="OK",
        sensor_statuses=["OK", "OK", "OK"],
    )
    js = sensor_frame_to_json(frame)
    parsed = sensor_frame_from_json(js)
    assert parsed.sensor_ids == frame.sensor_ids
    assert parsed.values == frame.values
    assert parsed.unit == "degC"


def test_actuator_request_json_serialization() -> None:
    req = ActuatorRequest(
        command_value=0.5,
        status="NORMAL",
        safe_default_used=False,
        reason="OK",
    )
    js = actuator_request_to_json(req)
    assert "command_value" in js
    assert "NORMAL" in js


def test_validate_sensor_frame_inconsistent_statuses() -> None:
    cfg = _cfg()
    # status says OK but some values are out of range, and one sensor has ERROR
    frame = SensorFrame(
        sensor_ids=["T1", "T2", "T3"],
        unit="degC",
        values=[-1.0, 10.0, 2.0],
        timestamp=123.0,
        source_status="OK",
        sensor_statuses=["OK", "OK", "ERROR"],
    )
    # We only check that it executes; warnings go to logger.
    validate_sensor_frame(frame, cfg)
