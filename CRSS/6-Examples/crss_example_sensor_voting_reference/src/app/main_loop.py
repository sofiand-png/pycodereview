from typing import Optional
import gc

from crss_phase.markers import non_critical_phase
from sensors.simulation import SimulatedSensors
from config.loader import load_config
from safety_logic.controller import SafetyController
from logging_utils.logger import get_logger


LOGGER = get_logger(__name__)


@non_critical_phase
def run_single_step(seed: int = 1) -> dict:
    cfg = load_config()
    simulator = SimulatedSensors(seed=seed)

    gc.disable()

    controller = SafetyController(cfg)
    sensor_values = simulator.read_all()
    command = controller.step(sensor_values)

    gc.enable()

    LOGGER.info("Sensor values: %s", sensor_values)
    LOGGER.info("Actuator command: %s", command)

    return {"value": command.value, "status": command.status}


def main(args: Optional[list] = None) -> None:
    _ = args
    cmd = run_single_step(seed=1)
    print(f"Actuator command: value={cmd['value']:.3f}, status={cmd['status']}")


if __name__ == "__main__":
    main()
