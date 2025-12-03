# Coverage Report — Sensor Voting Reference Example
## 1. Tools
- **Test runner**: pytest
- **Coverage tool**: coverage.py (branch coverage enabled)
- **Command**:
```bash
coverage run --branch -m pytest
coverage xml
coverage html
```
Config: `.coveragerc` excludes non-critical harness modules:
```
*/app/tcp_sensor_server.py
*/app/tcp_controller_client.py
*/logging_utils/*
*/sensors/simulation.py
```
## 2. Test Suite Breakdown
### Unit tests
- tests/unit/test_voting.py
- tests/unit/test_envelope.py
- tests/unit/test_controller.py
- tests/unit/test_config_loader.py
- tests/unit/test_markers.py
- tests/unit/test_json_protocol_validation.py
### MC/DC-style tests (logical decisions)
- tests/mcdc/test_voting_mcdc.py
- tests/mcdc/test_envelope_mcdc.py
- tests/mcdc/test_controller_mcdc.py
### Integration tests
- tests/integration/test_single_step_integration.py
## 3. Coverage Metrics (core logic only)
**Statement coverage (core modules): ~100%**
`safety_logic.*`, `config.*`, `actuator.interface`, `crss_phase.markers`,
`io.json_protocol`, `app.main_loop`, `crss_modes.modes`
**Branch coverage (core modules): ~95–98%**
All key decisions in:
- `compute_voted_value`
- `apply_safety_envelope`
- `SafetyController.step`
are exercised by MC/DC-style tests.
For detailed line-by-line coverage, see `htmlcov/index.html`.
## 4. MC/DC Justification (summary)
### 4.1 compute_voted_value (voting)
Decisions covered:
- **D1**: `len(values) != 3`
- **D2**: any plausible pair exists
- **D3**: all three pairs plausible (NORMAL) vs only one pair (DEGRADED)
### 4.2 apply_safety_envelope (envelope)
Decisions covered:
- **D1**: `voted_value < min_safe` → clamp to min
- **D2**: `voted_value > max_safe` → clamp to max
- **D3**: `delta > max_delta` → positive rate limit
- **D4**: `delta < -max_delta` → negative rate limit
- **D5**: otherwise → use clamped value unchanged
### 4.3 SafetyController.step (controller)
Decisions covered:
- **D1**: voting returns FAILSAFE → FAILSAFE command
- **D2**: voting returns DEGRADED → DEGRADED command
- **D3**: voting returns NORMAL → NORMAL command
---
# Fault Injection Report — Sensor Voting Reference Example
## 1. Fault Model
Faults modeled:
1. **Single-sensor high fault**
2. **Single-sensor low fault**
3. **Severe disagreement**
4. **Inconsistent metadata**
Faults injected via:
- `sensors.simulation.SimulatedSensors`
- `_derive_sensor_statuses` in `app.tcp_sensor_server`
- low-probability random status flipping
## 2. Expected Behaviour under Faults
- No plausible pair → FAILSAFE
- Single faulty sensor → DEGRADED
- All sensors plausible → NORMAL
- Metadata inconsistencies → warnings logged (non-critical)
## 3. Injected Faults vs Tests
- Functional MC/DC tests cover extreme scenarios.
- Demo TCP server/client triggers stochastic faults.
## 4. Residual Risks
Not yet simulated:
- frozen sensors
- stuck-at-safe values drifting slowly
