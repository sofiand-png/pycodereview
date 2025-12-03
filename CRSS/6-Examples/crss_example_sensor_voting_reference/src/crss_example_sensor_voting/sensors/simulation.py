"""Deterministic and stochastic sensor simulation (Core-C).

Simulates three cooling temperature sensors in degrees Celsius
with several fault scenarios:

- normal noise
- single-sensor high fault
- single-sensor low fault
- severe disagreement
- frozen sensors (values stop changing)
- stuck-at-safe values drifting slowly
"""

from typing import List, Optional
import random

from crss_example_sensor_voting.sensors.interfaces import SensorSource


class SimulatedSensors(SensorSource):
    """Three-channel sensor simulation for cooling temperature.

    Parameters
    ----------
    seed:
        Optional seed for deterministic RNG.
    forced_mode:
        For tests only. If provided, forces the scenario to one of:
        "normal", "high_fault", "low_fault",
        "severe_disagreement", "frozen", "stuck_drift".

    In production, `forced_mode` MUST be left as None.
    """

    def __init__(
        self,
        seed: Optional[int] = None,
        forced_mode: Optional[str] = None,
    ) -> None:
        self._rng = random.Random(seed) if seed is not None else random.Random()
        self._forced_mode = forced_mode
        self._frozen_values: Optional[List[float]] = None
        self._stuck_value: Optional[float] = None

    def _base_value(self) -> float:
        # Realistic normalized cooling band; not safety limits, just sim range.
        return self._rng.uniform(0.5, 4.5)

    def _noise(self) -> float:
        # Small sensor noise.
        return self._rng.uniform(-0.05, 0.05)

    def _initial_triplet(self) -> List[float]:
        base = self._base_value()
        return [base + self._noise() for _ in range(3)]

    def _select_mode(self) -> str:
        """Select a scenario based on RNG if no forced_mode is set."""
        if self._forced_mode is not None:
            return self._forced_mode

        r = self._rng.random()
        # Distribution:
        # 50% normal
        # 20% single-sensor high fault
        # 15% single-sensor low fault
        # 5% severe disagreement
        # 5% frozen
        # 5% stuck_drift
        if r < 0.50:
            return "normal"
        if r < 0.70:
            return "high_fault"
        if r < 0.85:
            return "low_fault"
        if r < 0.90:
            return "severe_disagreement"
        if r < 0.95:
            return "frozen"
        return "stuck_drift"

    def read_all(self) -> List[float]:
        mode = self._select_mode()

        # Base triplet used by several modes.
        values = self._initial_triplet()

        if mode == "normal":
            return values

        if mode == "high_fault":
            idx = self._rng.randrange(3)
            values[idx] = values[idx] + 2.5  # clearly out of plausible range
            return values

        if mode == "low_fault":
            idx = self._rng.randrange(3)
            values[idx] = values[idx] - 2.5  # clearly out of plausible range
            return values

        if mode == "severe_disagreement":
            base = self._base_value()
            return [base - 2.0, base, base + 2.0]

        if mode == "frozen":
            # First time: adopt whatever we computed as frozen values.
            if self._frozen_values is None:
                self._frozen_values = values
            return list(self._frozen_values)

        if mode == "stuck_drift":
            # Stuck near a safe mid-range value with small slow drift.
            if self._stuck_value is None:
                self._stuck_value = 2.5  # mid of [0, 5] band
            # Small drift per call, bounded into [0.0, 5.0].
            drift = self._rng.uniform(-0.05, 0.05)
            self._stuck_value = min(5.0, max(0.0, self._stuck_value + drift))
            center = self._stuck_value
            return [
                center + self._noise(),
                center + self._noise(),
                center + self._noise(),
            ]

        # Fallback: should never happen, but keep behaviour defined.
        return values
