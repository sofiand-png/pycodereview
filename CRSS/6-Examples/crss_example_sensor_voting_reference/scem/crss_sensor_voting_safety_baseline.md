# Safety Baseline — CRSS Python Sensor Voting Reference Example

## 1. System Overview

- **Function**: cooling temperature supervision using triple-redundant sensors,
  voting, and safety envelope.
- **Output**: normalized actuator command representing cooling demand.

## 2. Environment

- **Language runtime**: CPython 3.11.x
- **Dependencies**:
  - `pytest` (test only)
  - `coverage` (test only)
- **GC policy**:
  - `SafetyController.step` is called with GC disabled in offline tests
    (`app.main_loop.run_single_step`), reflecting Strict-A GC discipline.

## 3. Safety Modes and Profiles

- **Strict-A**:
  - `safety_logic.voting`
  - `safety_logic.envelope`
  - `safety_logic.controller`
  - `actuator.interface`
- **Strict-B**:
  - `config.model`
  - `sensors.interfaces`
- **Core-B**:
  - `app.main_loop`
  - `app.tcp_controller_client`
  - `config.loader`
- **Core-C**:
  - `sensors.simulation`
  - `app.tcp_sensor_server`
  - `logging_utils.logger`
  - `io.json_protocol`

## 4. Assumptions

- Underlying platform provides:
  - deterministic basic arithmetic for doubles within the range used
  - OS-level process isolation and standard TCP behaviour
- The example represents the **safety kernel**, not a full embedded deployment.

## 5. Evidence Summary

- CRSS compliance report: `docs/crss_sensor_voting_compliance_report.md`
- Coverage report: `reports/coverage_report.md`
- Fault injection report: `reports/fault_injection_report.md`
- SCEM artefacts: `scem/*`
