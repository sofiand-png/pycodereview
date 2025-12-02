from typing import List
import random

from .interfaces import SensorSource


class SimulatedSensors(SensorSource):
    def __init__(self, seed: int = 1) -> None:
        self._rng = random.Random(seed)

    def read_all(self) -> List[float]:
        base = self._rng.uniform(1.0, 2.0)
        noise1 = self._rng.uniform(-0.05, 0.05)
        noise2 = self._rng.uniform(-0.05, 0.05)
        noise3 = self._rng.uniform(-0.05, 0.05)
        return [base + noise1, base + noise2, base + noise3]
