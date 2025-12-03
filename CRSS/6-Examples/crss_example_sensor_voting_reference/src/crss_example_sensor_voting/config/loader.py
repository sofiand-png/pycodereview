
"""Configuration loader (Core-B, non-critical)."""


from crss_example_sensor_voting.config.model import SafetyConfig, DEFAULT_CONFIG


def load_config() -> SafetyConfig:
    """Load the SafetyConfig for the controller.

    For the reference example, this returns DEFAULT_CONFIG.
    A real system could load configuration from validated static files.
    """  # noqa: D401
    return DEFAULT_CONFIG
