
"""TCP JSON client that runs the Strict-A controller.

Requirements: 
SV-INT-01..03
"""


from __future__ import annotations

import argparse
import socket
from typing import Optional

from crss_example_sensor_voting.crss_phase.markers import non_critical_phase
from crss_example_sensor_voting.config.loader import load_config
from crss_example_sensor_voting.config.model import SAFE_DEFAULT
from crss_example_sensor_voting.safety_logic.controller import SafetyController
from crss_example_sensor_voting.io.json_protocol import (
    SensorFrame,
    ActuatorRequest,
    sensor_frame_from_json,
    actuator_request_to_json,
    validate_sensor_frame,
)
from crss_example_sensor_voting.logging_utils.logger import get_logger


LOGGER = get_logger(__name__)


@non_critical_phase
def run_client(host: str = "127.0.0.1", port: int = 9000) -> None:
    cfg = load_config()
    controller = SafetyController(cfg)

    with socket.create_connection((host, port)) as sock:
        LOGGER.info("Connected to TCP sensor server at %s:%s", host, port)
        sock_file = sock.makefile("rwb", buffering=0)
        try:
            while True:
                line = sock_file.readline()
                if not line:
                    LOGGER.info("Server closed connection")
                    break

                frame_json = line.decode("utf-8").strip()
                LOGGER.info("[CLIENT] Received SensorFrame: %s", frame_json)
                frame: SensorFrame = sensor_frame_from_json(frame_json)

                validate_sensor_frame(frame, cfg)

                cmd = controller.step(frame.values)

                safe_default_used = cmd.value == SAFE_DEFAULT

                req = ActuatorRequest(
                    command_value=cmd.value,
                    status=cmd.status,
                    safe_default_used=safe_default_used,
                    reason="OK",
                )

                req_json = actuator_request_to_json(req)
                LOGGER.info("[CLIENT] Sending ActuatorRequest: %s", req_json)
                sock_file.write(req_json.encode("utf-8") + b"\n")
        except KeyboardInterrupt:
            LOGGER.info("Client stopped by user (Ctrl+C)")
        except Exception as exc:
            LOGGER.exception("Client error: %s", exc)


def main(argv: Optional[list] = None) -> None:
    parser = argparse.ArgumentParser(description="CRSS TCP controller client")
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", type=int, default=9000)
    args = parser.parse_args(argv)
    run_client(host=args.host, port=args.port)


if __name__ == "__main__":
    main()
