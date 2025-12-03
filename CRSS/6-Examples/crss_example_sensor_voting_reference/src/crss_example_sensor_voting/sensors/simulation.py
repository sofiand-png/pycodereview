
"""Deterministic and stochastic sensor simulation (Core-C).

Simulates three cooling temperature sensors in degrees Celsius.
"""


from typing import List, Optional
import random

from crss_example_sensor_voting.sensors.interfaces import SensorSource


class SimulatedSensors(SensorSource):
    """3-channel sensor simulation with optional deterministic seeding.

    Behavior:
    - If seed is provided, the RNG is deterministic for reproducible tests.
    - If seed is None, the RNG uses system entropy for varied runs.
    - Scenarios include:
        * normal operation (all sensors plausible),
        * single-sensor high fault,
        * single-sensor low fault,
        * severe disagreement (no plausible pair).
    """  # noqa: D401

    def __init__(self, seed: Optional[int] = None) -> None:
        self._rng = random.Random(seed) if seed is not None else random.Random()

    def _base_value(self) -> float:
        # Simulate a realistic cooling temperature in [0.5, 4.5] (normalized band).
        return self._rng.uniform(0.5, 4.5)

    def _noise(self) -> float:
        # Small sensor noise
        return self._rng.uniform(-0.05, 0.05)

    def read_all(self) -> List[float]:
        base = self._base_value()
        values = [base + self._noise() for _ in range(3)]

        # Select a scenario
        r = self._rng.random()
        if r < 0.6:
            # Normal operation: small noise only
            return values
        elif r < 0.8:
            # Single-sensor high fault
            idx = self._rng.randrange(3)
            values[idx] = base + 2.5  # clearly out of plausible range
            return values
        elif r < 0.95:
            # Single-sensor low fault
            idx = self._rng.randrange(3)
            values[idx] = base - 2.5  # clearly out of plausible range
            return values
        else:
            # Severe disagreement: all three far apart
            return [
                base - 2.0,
                base + 0.0,
                base + 2.0,
            ]
