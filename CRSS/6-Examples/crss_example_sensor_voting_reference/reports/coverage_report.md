# Coverage Report - Sensor Voting Reference Example

**Version:** v1.0.0
**Status:** Informative (Reference Example)
**Maturity:** Stable
© 2025 Sofian Daghsen - All rights reserved
Distributed under CC BY-NC-ND 4.0 - see LICENSE-CRSS.

---

## Table of Contents
- [Coverage Report - Sensor Voting Reference Example](#coverage-report-sensor-voting-reference-example)
  - [Table of Contents](#table-of-contents)
  - [1. Tools](#1-tools)
  - [2. Test Suite Breakdown](#2-test-suite-breakdown)
    - [Unit tests](#unit-tests)
    - [MC/DC-style tests (logical decisions)](#mcdc-style-tests-logical-decisions)
    - [Integration tests](#integration-tests)
  - [3. Coverage Metrics (core logic only)](#3-coverage-metrics-core-logic-only)
  - [4. MC/DC Justification (summary)](#4-mcdc-justification-summary)
    - [4.1 compute_voted_value (voting)](#41-compute_voted_value-voting)
    - [4.2 apply_safety_envelope (envelope)](#42-apply_safety_envelope-envelope)
    - [4.3 SafetyController.step (controller)](#43-safetycontrollerstep-controller)
- [5. Fault Injection Report](#5-fault-injection-report)
  - [5.1 Fault model](#51-fault-model)
  - [5.2 Fault Classes Exercised](#52-fault-classes-exercised)
  - [5.3 Evidence: Test Locations](#53-evidence-test-locations)
  - [5.4 Expected Safety Response](#54-expected-safety-response)

---

# 5. Fault Injection Report

## 5.1 Fault model
The following faults are modelled at the sensor/input level:

1. **Single-sensor high fault**
   - One sensor is driven significantly above the plausible range
     (e.g. base + 2.5) while others remain near nominal.
2. **Single-sensor low fault**
   - One sensor is driven significantly below plausible range (e.g. base - 2.5).
3. **Severe disagreement**
   - All three sensors differ strongly (e.g. base - 2.0, base, base + 2.0),
     so no plausible pair exists.
4. **Inconsistent metadata**
   - Per-sensor status vs value range mismatches:
     - status `OK` but value out of safety range
     - status `ERROR` but value inside safety range
   - Aggregated `source_status` vs sensor_statuses mismatches:
     - `source_status = OK` but some sensors not `OK`
     - `source_status = ERROR` but all sensors `OK`
5. **Frozen sensors**
   - All three sensors stop changing and keep returning the same triplet.
6. **Stuck-at-safe with slow drift**
   - Sensors remain near a mid-range safe value and only drift very slowly
     within the safe band over time.

Faults are injected via:

- `sensors.simulation.SimulatedSensors` (modes: normal, high_fault, low_fault,
  severe_disagreement, frozen, stuck_drift)
- `_derive_sensor_statuses` in `app.tcp_sensor_server`
- random status flipping (low probability) to simulate diagnostic metadata bugs.


## 5.2 Fault Classes Exercised

The test suite covers the following fault classes (representative, not exhaustive):

1. **Sensor disagreement / plausibility faults**
   - One sensor deviates beyond the plausibility threshold.
   - Two sensors deviate (insufficient agreement).
2. **Out-of-range values**
   - Inputs below `min_safe` or above `max_safe` and/or outside sanity limits.
3. **Degenerate input shapes**
   - Wrong sensor vector length (handled upstream / non-critical validation).
4. **SAFE_DEFAULT fallback**
   - Conditions where no valid vote exists result in SAFE_DEFAULT command.

## 5.3 Evidence: Test Locations

Primary tests exercising these behaviors:

- Voting MC/DC:
  - `src/tests/mcdc/test_voting_mcdc.py`
- Envelope MC/DC:
  - `src/tests/mcdc/test_envelope_mcdc.py`
- Controller (integration of vote + envelope + status):
  - `src/tests/unit/test_controller.py`
  - `src/tests/integration/test_single_step_integration.py`
  - `src/tests/integration/test_full_cycle_integration.py`

## 5.4 Expected Safety Response

For invalid / inconsistent / implausible inputs, the Strict-A kernel MUST:

- avoid unsafe actuation,
- select SAFE_DEFAULT or equivalent failsafe command,
- expose a FAILSAFE/DEGRADED status in the returned abstract command object.
