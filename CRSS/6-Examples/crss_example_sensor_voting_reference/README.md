
# CRSS Python Sensor Voting Reference Example (v3)

Strict-A safety controller for cooling temperature supervision with:

- 3-channel sensor voting with plausibility checks,
- safety envelope (min/max + rate limiting),
- deterministic fallback (SAFE_DEFAULT),
- actuator status classification (NORMAL / DEGRADED / FAILSAFE),
- deterministic or stochastic sensor simulation,
- JSON over TCP between a sensor server and a controller client,
- JSON schemas for SensorFrame and ActuatorRequest,
- clear separation of critical and non-critical code,
- installation via `setup.py` (src-layout).

## Quick start

> [⬆ Back to Table of Contents](#toc)


```bash
python -m venv .venv
# On Windows:
.venv\\Scripts\\activate
# On Unix:
source .venv/bin/activate

pip install -r requirements.txt
pip install .
```

### Run TCP server and client

In one terminal (sensor server):

```bash
python -m crss_example_sensor_voting.app.tcp_sensor_server
```

In another terminal (controller client):

```bash
python -m crss_example_sensor_voting.app.tcp_controller_client
```

Stop both with `Ctrl+C`.

### Offline single-step run (no TCP)

```bash
python -m crss_example_sensor_voting.app.main_loop
```

### Tests

```bash
python -m pytest
coverage run --branch -m pytest
coverage html
```
