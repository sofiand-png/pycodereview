from typing import List

from crss_phase.markers import critical_phase
from config.model import SafetyConfig
from .voting import compute_voted_value
from .envelope import apply_safety_envelope
from actuator.interface import ActuatorCommand, create_command


class SafetyController:
    def __init__(self, cfg: SafetyConfig) -> None:
        self._cfg = cfg
        self._previous_value = cfg.initial_output

    @critical_phase
    def step(self, sensor_values: List[float]) -> ActuatorCommand:
        voted = compute_voted_value(sensor_values, self._cfg)
        safe_value = apply_safety_envelope(voted, self._previous_value, self._cfg)
        self._previous_value = safe_value
        return create_command(safe_value, status="NORMAL")
