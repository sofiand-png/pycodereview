
"""Strict-A SafetyController (@critical).

Requirements:
SV-FUNC-01 — Three-sensor input per cycle

SV-FUNC-02 — TMR voting (via voting)

SV-FUNC-03 — Stateless per-cycle + previous output only

SV-SAF-01..03 — via envelope

SV-FLT-01..04 — combined behavior

SV-TEST-03 — Fault injection coverage target
"""


from typing import List

from crss_example_sensor_voting.crss_phase.markers import critical_phase
from crss_example_sensor_voting.config.model import SafetyConfig
from crss_example_sensor_voting.safety_logic.voting import (
    compute_voted_value,
    VOTING_STATUS_NORMAL,
    VOTING_STATUS_DEGRADED,
    VOTING_STATUS_FAILSAFE,
)
from crss_example_sensor_voting.safety_logic.envelope import apply_safety_envelope
from crss_example_sensor_voting.actuator.interface import (
    ActuatorCommand,
    STATUS_NORMAL,
    STATUS_DEGRADED,
    STATUS_FAILSAFE,
    create_command,
)


class SafetyController:
    """Strict-A safety controller coordinating voting and envelope.

    The controller maintains a previous actuator value to support the
    rate limiter. State is simple and bounded.
    """  # noqa: D401

    def __init__(self, cfg: SafetyConfig) -> None:
        self._cfg = cfg
        self._previous_value = cfg.initial_output

    @critical_phase
    def step(self, sensor_values: List[float]) -> ActuatorCommand:
        """Execute a single Strict-A control step.

        The controller:
        - computes a voted value and voting status,
        - validates previous value,
        - applies the safety envelope,
        - derives an actuator status,
        - returns an ActuatorCommand.
        """  # noqa: D401
        voted_value, voting_status = compute_voted_value(sensor_values, self._cfg)

        # Validate and clamp previous value before using it.
        prev = self._previous_value
        if prev < self._cfg.min_safe:
            prev = self._cfg.min_safe
        elif prev > self._cfg.max_safe:
            prev = self._cfg.max_safe

        safe_value = apply_safety_envelope(voted_value, prev, self._cfg)
        self._previous_value = safe_value

        if voting_status == VOTING_STATUS_FAILSAFE:
            status = STATUS_FAILSAFE
        elif voting_status == VOTING_STATUS_DEGRADED:
            status = STATUS_DEGRADED
        else:
            status = STATUS_NORMAL

        return create_command(safe_value, status=status)
