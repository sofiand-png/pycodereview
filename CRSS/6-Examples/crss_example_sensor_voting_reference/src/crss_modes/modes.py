from dataclasses import dataclass


@dataclass(frozen=True)
class ModeInfo:
    name: str
    profile: str
    safety_level: str
    description: str


MODES = [
    ModeInfo(name="Strict-A", profile="Strict", safety_level="A",
             description="Safety-critical controller, voting, and envelope"),
    ModeInfo(name="Strict-B", profile="Strict", safety_level="B",
             description="Safety-support modules such as typed config"),
    ModeInfo(name="Core-B", profile="Core", safety_level="B",
             description="Non-critical config loader and orchestrator"),
    ModeInfo(name="Core-C", profile="Core", safety_level="C",
             description="Simulation, logging, and diagnostics"),
]
