from dataclasses import dataclass


@dataclass(frozen=True)
class ActuatorCommand:
    value: float
    status: str


def create_command(value: float, status: str = "NORMAL") -> ActuatorCommand:
    return ActuatorCommand(value=value, status=status)
