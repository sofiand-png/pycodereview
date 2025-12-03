
"""JSON protocol definitions for sensor frames and actuator requests (Core-C)."""


from __future__ import annotations

from dataclasses import dataclass
from typing import List, Optional, Dict, Any

import json

from crss_example_sensor_voting.config.model import SafetyConfig
from crss_example_sensor_voting.logging_utils.logger import get_logger


LOGGER = get_logger(__name__)


@dataclass
class SensorFrame:
    sensor_ids: List[str]
    unit: str                 # "degC"
    values: List[float]       # three temperatures
    timestamp: Optional[float]
    source_status: str        # "OK" | "DEGRADED" | "ERROR"
    sensor_statuses: List[str]  # per-sensor status strings


@dataclass
class ActuatorRequest:
    command_value: float
    status: str                 # "NORMAL" | "DEGRADED" | "FAILSAFE"
    safe_default_used: bool
    reason: str                 # "OK" | "VOTING_FAILSAFE" | "ENVELOPE_LIMIT" | ...


def sensor_frame_to_dict(frame: SensorFrame) -> Dict[str, Any]:
    return {
        "sensor_ids": frame.sensor_ids,
        "unit": frame.unit,
        "values": frame.values,
        "timestamp": frame.timestamp,
        "source_status": frame.source_status,
        "sensor_statuses": frame.sensor_statuses,
    }


def sensor_frame_to_json(frame: SensorFrame) -> str:
    return json.dumps(sensor_frame_to_dict(frame), separators=(",", ":"))


def sensor_frame_from_json(payload: str) -> SensorFrame:
    data = json.loads(payload)
    return SensorFrame(
        sensor_ids=list(data["sensor_ids"]),
        unit=str(data["unit"]),
        values=[float(v) for v in data["values"]],
        timestamp=float(data["timestamp"]) if data.get("timestamp") is not None else None,  # noqa: E501
        source_status=str(data["source_status"]),
        sensor_statuses=list(data.get("sensor_statuses", ["UNKNOWN"] * 3)),
    )


def actuator_request_to_dict(req: ActuatorRequest) -> Dict[str, Any]:
    return {
        "command_value": req.command_value,
        "status": req.status,
        "safe_default_used": req.safe_default_used,
        "reason": req.reason,
    }


def actuator_request_to_json(req: ActuatorRequest) -> str:
    return json.dumps(actuator_request_to_dict(req), separators=(",", ":"))


def validate_sensor_frame(frame: SensorFrame, cfg: SafetyConfig) -> None:
    """Validate consistency between status and value ranges.

    - If sensor_status == "OK" but value is outside [min_safe, max_safe]
      -> warning.
    - If sensor_status != "OK" but value is inside [min_safe, max_safe]
      -> warning.
    - If source_status == "OK" but any sensor_status != "OK"
      -> warning.
    - If source_status == "ERROR" but all sensor_statuses are OK
      -> warning.

    Validation is non-critical: it logs warnings but does not alter
    Strict-A behavior.
    """  # noqa: D401
    min_v, max_v = cfg.min_safe, cfg.max_safe

    for sid, val, sstatus in zip(frame.sensor_ids, frame.values, frame.sensor_statuses):
        inside = min_v <= val <= max_v
        if sstatus == "OK" and not inside:
            LOGGER.warning(
                "Sensor %s status=OK but value %.3f outside [%.3f, %.3f]",
                sid,
                val,
                min_v,
                max_v,
            )
        if sstatus != "OK" and inside:
            LOGGER.warning(
                "Sensor %s status=%s but value %.3f inside [%.3f, %.3f]",
                sid,
                sstatus,
                val,
                min_v,
                max_v,
            )

    any_bad = any(status != "OK" for status in frame.sensor_statuses)
    all_ok = all(status == "OK" for status in frame.sensor_statuses)

    if frame.source_status == "OK" and any_bad:
        LOGGER.warning(
            "Frame source_status=OK but some sensor_statuses are not OK: %s",
            frame.sensor_statuses,
        )
    if frame.source_status == "ERROR" and all_ok:
        LOGGER.warning(
            "Frame source_status=ERROR but all sensor_statuses are OK: %s",
            frame.sensor_statuses,
        )
