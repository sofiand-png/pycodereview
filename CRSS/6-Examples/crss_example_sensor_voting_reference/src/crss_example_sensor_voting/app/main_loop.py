
"""Single-step orchestrator (non-critical) for offline runs and tests.

Requirements:
SV-FUNC-01 — Single frame per cycle

SV-FUNC-03 — previous_output used per cycle

SV-INT-03 — Strict-A is not doing I/O

SV-TEST-01 — runtime behavior implicitly covered by integration tests
"""


from typing import Optional, List
import gc

from crss_example_sensor_voting.crss_phase.markers import non_critical_phase
from crss_example_sensor_voting.sensors.simulation import SimulatedSensors
from crss_example_sensor_voting.config.loader import load_config
from crss_example_sensor_voting.orchestrator.inner_orchestrator import InnerOrchestrator, frame_inputs
from crss_example_sensor_voting.logging_utils.logger import get_logger
from crss_example_sensor_voting.config.model import SAFE_DEFAULT


LOGGER = get_logger(__name__)


@non_critical_phase
def run_single_step(seed: Optional[int] = None) -> dict:
    """Run a single control step and return a serializable command.

    This is used for unit tests and offline runs; it bypasses JSON/TCP
    and feeds simulated sensor values directly into the Strict-A logic.
    """  # noqa: D401
    cfg = load_config()
    simulator = SimulatedSensors(seed=seed)

    values: List[float] = simulator.read_all()

    gc.disable()
    inner = InnerOrchestrator(cfg)
    framed = frame_inputs(values)
    command = inner.step(framed)
    gc.enable()

    safe_default_used = command.value == SAFE_DEFAULT

    LOGGER.info("[OFFLINE] Sensor values: %s", values)
    LOGGER.info("[OFFLINE] Actuator command: %s", command)

    return {"value": command.value, "status": command.status, "safe_default_used": safe_default_used}
