
"""Configuration model for the safety controller (Strict-B)."""


from dataclasses import dataclass


# Explicit SAFE_DEFAULT constant for clarity and traceability.
SAFE_DEFAULT: float = 0.0


@dataclass(frozen=True)
class SafetyConfig:
    min_safe: float
    max_safe: float
    max_delta: float
    plausibility_threshold: float
    fallback_value: float  # SAFE_DEFAULT
    initial_output: float


DEFAULT_CONFIG = SafetyConfig(
    min_safe=0.0,
    max_safe=5.0,
    max_delta=0.5,
    plausibility_threshold=0.2,
    fallback_value=SAFE_DEFAULT,
    initial_output=SAFE_DEFAULT,
)
