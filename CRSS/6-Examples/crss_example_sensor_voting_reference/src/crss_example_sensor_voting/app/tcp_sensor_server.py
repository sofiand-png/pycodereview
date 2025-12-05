
"""TCP JSON server that simulates cooling temperature sensors.

Requirements:
SV-INT-01 — SensorFrame producer

SV-FLT-01..04 — via injected fault scenarios

SV-TEST-03 — basis for FI tests
"""


from __future__ import annotations

import socket
import time
from typing import List, Tuple

from crss_example_sensor_voting.config.loader import load_config
from crss_example_sensor_voting.config.model import SafetyConfig
from crss_example_sensor_voting.sensors.simulation import SimulatedSensors
from crss_example_sensor_voting.io.json_protocol import (
    SensorFrame,
    sensor_frame_to_json,
)
from crss_example_sensor_voting.logging_utils.logger import get_logger


LOGGER = get_logger(__name__)


def _derive_sensor_statuses(
    values: List[float],
    cfg: SafetyConfig,
    rng: SimulatedSensors,
) -> Tuple[List[str], str]:
    min_v, max_v = cfg.min_safe, cfg.max_safe
    sensor_statuses: List[str] = []
    for val in values:
        inside = min_v <= val <= max_v
        status = "OK" if inside else "ERROR"
        r = rng._rng.random()  # type: ignore[attr-defined]
        if r < 0.05:
            status = "ERROR" if status == "OK" else "OK"
        sensor_statuses.append(status)

    if all(s == "OK" for s in sensor_statuses):
        source_status = "OK"
    elif any(s != "OK" for s in sensor_statuses) and not all(s != "OK" for s in sensor_statuses):
        source_status = "DEGRADED"
    else:
        source_status = "ERROR"

    return sensor_statuses, source_status


def run_server(host: str = "127.0.0.1", port: int = 9000, period_s: float = 0.06) -> None:
    cfg = load_config()
    simulator = SimulatedSensors(seed=None)

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_sock:
        server_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server_sock.bind((host, port))
        server_sock.listen(1)
        LOGGER.info("TCP sensor server listening on %s:%s", host, port)

        conn, addr = server_sock.accept()
        LOGGER.info("Client connected from %s", addr)
        with conn:
            conn_file = conn.makefile("rwb", buffering=0)
            try:
                while True:
                    values: List[float] = simulator.read_all()
                    sensor_ids = ["T1", "T2", "T3"]
                    sensor_statuses, source_status = _derive_sensor_statuses(values, cfg, simulator)

                    frame = SensorFrame(
                        sensor_ids=sensor_ids,
                        unit="degC",
                        values=values,
                        timestamp=time.time(),
                        source_status=source_status,
                        sensor_statuses=sensor_statuses,
                    )

                    frame_json = sensor_frame_to_json(frame)
                    LOGGER.info("[SERVER] Sending SensorFrame: %s", frame_json)
                    conn_file.write(frame_json.encode("utf-8") + b"\n")

                    resp = conn_file.readline()
                    if not resp:
                        LOGGER.info("Client disconnected")
                        break

                    resp_str = resp.decode("utf-8").strip()
                    LOGGER.info("[SERVER] Received ActuatorRequest: %s", resp_str)

                    time.sleep(period_s)
            except KeyboardInterrupt:
                LOGGER.info("Server stopped by user (Ctrl+C)")
            except Exception as exc:
                LOGGER.exception("Server error: %s", exc)


def main() -> None:
    run_server()


if __name__ == "__main__":
    main()
