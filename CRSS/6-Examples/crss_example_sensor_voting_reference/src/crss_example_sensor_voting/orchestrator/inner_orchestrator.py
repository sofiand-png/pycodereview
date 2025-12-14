"""Strict-B inner orchestrator (non-critical).

Implements the CRSS reference architecture pattern:

Outer Orchestrator (Core) -> Inner Orchestrator (Strict-B) -> Level-A (Strict-A)

Responsibilities:
- Accept already-framed inputs/config from Core.
- Perform Strict-B structural validation and normalization.
- Invoke Strict-A domain validator (non-critical).
- Invoke Strict-A @critical kernel step.

This module MUST remain non-critical and MUST NOT perform I/O.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import List

from crss_example_sensor_voting.crss_phase.markers import non_critical_phase
from crss_example_sensor_voting.config.model import SafetyConfig
from crss_example_sensor_voting.safety_logic.validator import validate_config_domain
from crss_example_sensor_voting.safety_logic.controller import SafetyController
from crss_example_sensor_voting.actuator.interface import ActuatorCommand


@dataclass(frozen=True)
class FramedInputs:
    """Strict-B framed input structure passed into Level-A.

    This object represents *structural validation* at Strict-B:
    - fixed arity (exactly 3 sensors),
    - typed values (float).

    Domain-level plausibility is handled by Strict-A logic.
    """
    sensors: tuple[float, float, float]


@non_critical_phase
def frame_inputs(sensor_values: List[float]) -> FramedInputs:
    """Normalize and structurally validate raw sensor values from Core.

    Raises:
        ValueError: if input cannot be framed into the Level-A model.
    """  # noqa: D401
    if len(sensor_values) != 3:
        raise ValueError("Expected exactly 3 sensor values for TMR voting")
    try:
        a = float(sensor_values[0])
        b = float(sensor_values[1])
        c = float(sensor_values[2])
    except (TypeError, ValueError) as e:
        raise ValueError("Sensor values must be numeric") from e
    return FramedInputs(sensors=(a, b, c))


class InnerOrchestrator:
    """Strict-B inner orchestrator.

    Holds a Strict-A controller instance and exposes a non-critical interface
    that sequences domain validation + critical step.
    """  # noqa: D401

    def __init__(self, cfg: SafetyConfig) -> None:
        # Strict-A domain validation (non-critical)
        validated_cfg = validate_config_domain(cfg)
        # Strict-A controller (kernel wrapper)
        self._controller = SafetyController(validated_cfg)

    def step(self, framed: FramedInputs) -> ActuatorCommand:
        """Execute one control cycle.

        Note: The underlying Strict-A controller step is @critical; this method
        is intentionally not annotated as critical to keep Strict-B non-critical.
        """  # noqa: D401
        # Convert tuple to list for existing Strict-A API.
        return self._controller.step(list(framed.sensors))
