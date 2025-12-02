from dataclasses import dataclass


@dataclass(frozen=True)
class SafetyConfig:
    min_safe: float
    max_safe: float
    max_delta: float
    plausibility_threshold: float
    fallback_value: float
    initial_output: float


DEFAULT_CONFIG = SafetyConfig(
    min_safe=0.0,
    max_safe=5.0,
    max_delta=0.5,
    plausibility_threshold=0.2,
    fallback_value=0.0,
    initial_output=0.0,
)
