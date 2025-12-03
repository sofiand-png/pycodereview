
"""Sensor interfaces for the reference example (Strict-B)."""


from typing import List, Protocol


class SensorSource(Protocol):
    """Abstract source of redundant sensor values.

    Implementations must return exactly three sensor values per call.
    """  # noqa: D401

    def read_all(self) -> List[float]:
        ...
