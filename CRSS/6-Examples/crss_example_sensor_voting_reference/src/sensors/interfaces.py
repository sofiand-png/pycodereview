from typing import Protocol, List


class SensorSource(Protocol):
    def read_all(self) -> List[float]:
        ...
