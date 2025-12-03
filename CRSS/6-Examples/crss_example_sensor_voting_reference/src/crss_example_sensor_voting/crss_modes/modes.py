
"""Static metadata for Modes used in the reference example."""


from dataclasses import dataclass


@dataclass(frozen=True)
class ModeInfo:
    name: str
    profile: str
    safety_level: str
    description: str


MODES = [
    ModeInfo(
        name="Strict-A",
        profile="Strict",
        safety_level="A",
        description="Safety-critical controller, voting, and envelope",
    ),
    ModeInfo(
        name="Strict-B",
        profile="Strict",
        safety_level="B",
        description="Safety-support modules such as typed config",
    ),
    ModeInfo(
        name="Core-B",
        profile="Core",
        safety_level="B",
        description="Non-critical orchestrator and config loader",
    ),
    ModeInfo(
        name="Core-C",
        profile="Core",
        safety_level="C",
        description="Simulation, logging, and TCP/JSON I/O",
    ),
]
