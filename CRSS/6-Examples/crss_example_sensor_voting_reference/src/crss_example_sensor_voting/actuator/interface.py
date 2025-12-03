
"""Actuator command definition (Strict-A boundary).

Represents a cooling command, e.g. valve opening or pump speed request.
"""


from dataclasses import dataclass


STATUS_NORMAL = "NORMAL"
STATUS_DEGRADED = "DEGRADED"
STATUS_FAILSAFE = "FAILSAFE"


@dataclass(frozen=True)
class ActuatorCommand:
    value: float
    status: str  # One of STATUS_NORMAL / STATUS_DEGRADED / STATUS_FAILSAFE


def create_command(value: float, status: str = STATUS_NORMAL) -> ActuatorCommand:
    """Create a pure actuator command structure.

    This module performs no I/O. It only structures the output of the
    safety controller before it is consumed by non-critical code.
    """  # noqa: D401
    return ActuatorCommand(value=value, status=status)
