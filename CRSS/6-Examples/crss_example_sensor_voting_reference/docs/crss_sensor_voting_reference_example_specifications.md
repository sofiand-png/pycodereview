# CRSS Reference Specification - Sensor Voting & Safe Actuation System

**Version:** v1.0.0
**Status:** Informative (Reference Example)
**Maturity:** Stable
© 2025 Sofian Daghsen - All rights reserved
Distributed under CC BY-NC-ND 4.0 - see LICENSE-CRSS.

---

**Python Target:** 3.11
**CRSS Modes Used:** Strict-A, Strict-B, Core-B, Core-C
*(Modes follow Mode = (Profile, Safety Level); e.g. “Strict-A” = Strict, Level A.)*
**System Type:** Safety-related sensor-voting control loop with gateway interaction
**Domain Fit:** Automotive, Clinical, Railway, Industrial Control, Embedded Simulation

---

## Table of Contents
- [CRSS Reference Specification - Sensor Voting & Safe Actuation System](#crss-reference-specification-sensor-voting-safe-actuation-system)
  - [Table of Contents](#table-of-contents)
  - [1. Introduction](#1-introduction)
  - [2. Goals of the Example](#2-goals-of-the-example)
  - [3. System Overview](#3-system-overview)
    - [3.1 Safety Goals](#31-safety-goals)
    - [3.2 Hazards](#32-hazards)
    - [3.3 Design Model](#33-design-model)
    - [3.4 Functional Requirements](#34-functional-requirements)
      - [3.4.1 Safety / Envelope Requirements](#341-safety-envelope-requirements)
      - [3.4.2 Fault-Handling Requirements](#342-fault-handling-requirements)
      - [3.4.3 Interface / JSON / TCP Requirements](#343-interface-json-tcp-requirements)
      - [3.4.5 Test & Coverage Requirements](#345-test-coverage-requirements)
  - [4. High-Level Architecture](#4-high-level-architecture)
  - [5. Key CRSS Compliance Principles Used](#5-key-crss-compliance-principles-used)
  - [6. Actors and Data Flow](#6-actors-and-data-flow)
  - [7. Profiles and Criticality Zones](#7-profiles-and-criticality-zones)
  - [8. Detailed External Interface](#8-detailed-external-interface)
  - [9. Message Timing Requirements](#9-message-timing-requirements)
  - [10. Data Model (Full Definition)](#10-data-model-full-definition)
    - [10.1 SensorFrame Structure](#101-sensorframe-structure)
    - [10.2 SensorFrame Validation Rules (Core-C)](#102-sensorframe-validation-rules-core-c)
  - [11. ActuatorRequest Structure](#11-actuatorrequest-structure)
  - [12. JSON Schemas (Canonical Version)](#12-json-schemas-canonical-version)
    - [12.1 SensorFrame Schema](#121-sensorframe-schema)
    - [12.2 ActuatorRequest Schema](#122-actuatorrequest-schema)
  - [13. Fault Model: Full Specification](#13-fault-model-full-specification)
    - [13.1 Fault Modes Overview](#131-fault-modes-overview)
    - [13.2 Deterministic Fault Selection](#132-deterministic-fault-selection)
  - [14. Sensor Simulation: Full Behavioral Specification](#14-sensor-simulation-full-behavioral-specification)
    - [14.1 Value Generation Base Logic](#141-value-generation-base-logic)
    - [14.2 Mode: high_fault](#142-mode-high_fault)
    - [14.3 Mode: low_fault](#143-mode-low_fault)
    - [14.4 Mode: severe_disagreement](#144-mode-severe_disagreement)
    - [14.5 Mode: frozen](#145-mode-frozen)
    - [14.6 Mode: stuck_drift](#146-mode-stuck_drift)
  - [15. Voting Algorithm (Core-B Deterministic Logic)](#15-voting-algorithm-core-b-deterministic-logic)
    - [15.1 Pre-Voting Checks](#151-pre-voting-checks)
    - [15.2 Spread and Disagreement](#152-spread-and-disagreement)
    - [15.3 Voting Rule](#153-voting-rule)
    - [15.4 Voting Status Output](#154-voting-status-output)
  - [16. Safety Envelope (Strict-A)](#16-safety-envelope-strict-a)
    - [16.1 Inputs](#161-inputs)
    - [16.2 Clamp to Safe Bounds](#162-clamp-to-safe-bounds)
    - [16.3 Rate Limiting](#163-rate-limiting)
    - [16.4 Severe Disagreement → FAILSAFE](#164-severe-disagreement-failsafe)
    - [16.5 Frozen Sensors](#165-frozen-sensors)
    - [16.6 Stuck-Drift Behavior](#166-stuck-drift-behavior)
  - [17. Actuator Command Classification](#17-actuator-command-classification)
  - [18. Logging Rules (Core-C)](#18-logging-rules-core-c)
  - [19. Execution Model (End-to-End)](#19-execution-model-end-to-end)
  - [20. Timing Constraints](#20-timing-constraints)
  - [21. Configuration Model (CRSS-Compliant)](#21-configuration-model-crss-compliant)
    - [21.1 CRSS Constraints for Config](#211-crss-constraints-for-config)
    - [21.2 Parameters](#212-parameters)
  - [22. CRSS Compliance Mapping (Full Version)](#22-crss-compliance-mapping-full-version)
    - [22.1 Strict-A Responsibilities](#221-strict-a-responsibilities)
    - [22.2 Core-B Responsibilities](#222-core-b-responsibilities)
    - [22.3 Core-C Responsibilities](#223-core-c-responsibilities)
  - [23. Test & Verification Requirements (Full)](#23-test-verification-requirements-full)
    - [23.1 Unit Testing Requirements](#231-unit-testing-requirements)
    - [23.2 MC/DC Requirements](#232-mcdc-requirements)
    - [23.3 Integration Tests](#233-integration-tests)
    - [23.4 Fault Injection Testing Requirements](#234-fault-injection-testing-requirements)
  - [24. CI/CD Pipeline Requirements](#24-cicd-pipeline-requirements)
  - [25. Deployment and Runtime Environment](#25-deployment-and-runtime-environment)
    - [25.1 Environment Freezing](#251-environment-freezing)
    - [25.2 Execution Isolation](#252-execution-isolation)
    - [25.3 Safety Lifecycle Requirements](#253-safety-lifecycle-requirements)
  - [26. Shutdown and Restart Behavior](#26-shutdown-and-restart-behavior)
  - [27. Informative Domain-Specific Notes](#27-informative-domain-specific-notes)

---

## 1. Introduction
This document describes a complete CRSS reference example demonstrating how to implement a safety-related closed-loop control function in Python while maintaining CRSS compliance, determinism, and isolating critical versus non-critical behavior.

It systematically defines:
- the functional specification
- the fault model
- the voting algorithm
- the Strict-A safety envelope
- the gateway JSON-over-TCP protocol
- the actuator safety logic
- the timing model
- the simulation rules
- the phase/criticality assignment
- the test requirements
- CRSS compliance mapping

This reference is designed to act as:
- a teaching example for new CRSS users
- a verification anchor for tool testing
- a template for teams building real CRSS applications

## 2. Goals of the Example
This system is intended to:

- Demonstrate how CRSS strict-level code interacts with real-world systems through a deterministic interface (gateway).
- Show how Python can be used safely in critical function chains without violating strict determinism boundaries.
- Provide a runnable, testable, high-coverage, fault-injection-enabled reference.
- Illustrate correct separation of:
  - Strict-A (critical safety logic)
  - Core-B (deterministic preprocessing)
  - Core-C (I/O, JSON, TCP, logging, simulation)
- Provide a known-good example for auditors to evaluate CRSS compliance.

## 3. System Overview
### 3.1 Safety Goals

- **SG-1 - Safe envelope:**
  The Safety Controller must not command an actuator value that exceeds a safe envelope
  (`MIN_SAFE ≤ cmd ≤ MAX_SAFE`) under any circumstances.

- **SG-2 - Single-fault tolerance (sensors):**
  The Safety Controller must tolerate one faulty sensor (1-out-of-3) without issuing an unsafe command.

- **SG-3 - Fail-safe on severe disagreement:**
  If available sensors disagree beyond a configured plausibility threshold, the Safety Controller must fail safe
  (e.g. use SAFE_DEFAULT; last safe command may be used only when explicitly configured).

- **SG-4 - Deterministic @critical path:**
  The Safety Controller must be deterministic in its `@critical` path:
  given the same inputs and internal state, it must produce the same output on every run.

- **SG-5 - No non-deterministic Python features in Strict-A:**
  The Strict-A critical path must not rely on Python features that can introduce non-determinism
  (e.g. GC-visible allocation, threads, async scheduling, random number generation, system time).

- **SG-6 - Bounded control logic:**
  Strict-A logic must not contain unbounded loops, recursion, or unbounded collection growth.
  All loops must be statically bounded (e.g. over the fixed set of three sensors).

- **SG-7 - Isolation of non-critical behavior:**
  Faults in non-critical code (simulation, logging, config loading, CLI) must **not** affect the behavior of the
  Strict-A `@critical` path beyond defined safe fallback modes.
  Strict-A logic receives normalized input structures only (already parsed and validated). It never processes raw JSON strings or external resources.
- **SG-8 - SAFE_DEFAULT:**

**Reference Safe Default Command (SAFE_DEFAULT):**
	The Safe Default command used by the controller in fallback conditions is defined as:
	SAFE_DEFAULT = min_safe
	This guarantees:
	- determinism,
	- a physically non-dangerous fallback,
	- bounded output independent of sensor input,
	- no reliance on previous-state memory when unsafe conditions arise.

	SAFE_DEFAULT is a configuration parameter but MUST default to min_safe unless explicitly overridden.

### 3.2 Hazards

- **H-1 - Unsafe actuator command:**
  Actuator command outside the safe envelope, leading to hazardous physical behavior.

- **H-2 - Incorrect voting:**
  Voting logic incorrectly accepts faulty sensor data, causing unsafe actuator commands.

- **H-3 - Undetected sensor drift:**
  Slow drift of one or more sensors leads to subtle but long-term unsafe outputs.

- **H-4 - Sensor disagreement mishandled:**
  Multiple sensors disagree and the controller fails to enter a safe degraded or fail-safe mode.

- **H-5 - Non-deterministic execution:**
  Timing, GC, or async behavior causes non-repeatable control outputs for identical inputs.

- **H-6 - Non-critical faults bleed into critical path:**
  Errors in logging, configuration loading, sensor simulation, or CLI cause changes to
  the Strict-A decision logic or mask unsafe behavior.

### 3.3 Design Model

The implemented Version-3 system is a closed-loop sensor-voting controller that processes a continuous stream of three temperature sensor values, determines the safest output command, and returns a bounded and deterministic actuator value.

Loop:
`[SENSOR GATEWAY] → SensorFrame JSON → [CLIENT] → Strict-A logic → ActuatorRequest JSON → [GATEWAY]`

The system runs indefinitely (until Ctrl+C) at ~60 ms cycle time.

### 3.4 Functional Requirements

**SV-FUNC-01 - Triple sensor input**
The system shall process exactly three sensor channels per cycle and reject any SensorFrame that does not contain exactly three values.

**SV-FUNC-02 - TMR voting**
The system shall compute a single voted value from the three sensor inputs using a deterministic TMR-style voting algorithm (median-based).

**SV-FUNC-03 - Stateless per-cycle computation**
Each control cycle shall compute the actuator command using only the current SensorFrame and the previous actuator output; no additional hidden internal state is permitted.

---

#### 3.4.1 Safety / Envelope Requirements

**SV-SAF-01 - Envelope clamp**
The system shall ensure that every actuator command satisfies:
`min_safe ≤ command_value ≤ max_safe`.

**SV-SAF-02 - Rate limiting**
The system shall ensure that the difference between successive actuator commands does not exceed `max_delta` in magnitude, except when transitioning to SAFE_DEFAULT.

**SV-SAF-03 - SAFE_DEFAULT application**
When the system enters FAILSAFE state, it shall set the actuator command to `SAFE_DEFAULT = min_safe` and may bypass rate limiting for that transition.

**SV-SAF-04 - Deterministic Strict-A**
For any given configuration, previous output, and set of validated sensor values, the Strict-A logic shall always return the same actuator command and status.

---

#### 3.4.2 Fault-Handling Requirements

**SV-FLT-01 - Single-sensor fault tolerance**
If at most one sensor is faulty and a plausible pair exists, the system shall produce a bounded actuator command with status `DEGRADED` or `NORMAL`, never `FAILSAFE`.

**SV-FLT-02 - Severe disagreement to FAILSAFE**
If no plausible sensor pair exists due to severe disagreement, the system shall enter FAILSAFE and output SAFE_DEFAULT.

**SV-FLT-03 - Frozen behavior**
If sensor readings are detected as frozen over multiple cycles, the system shall hold or slowly adjust the actuator command within the configured envelope and mark the status as at most `DEGRADED`.

**SV-FLT-04 - Stuck-drift behavior**
Slow sensor drift within the safe band shall not cause oscillatory or unsafe actuator commands; the envelope shall keep the command bounded and rate-limited.

---

#### 3.4.3 Interface / JSON / TCP Requirements

**SV-INT-01 - SensorFrame format**
The gateway shall send SensorFrame messages conforming to the specified JSON schema (IDs, values, statuses, timestamp, unit).

**SV-INT-02 - ActuatorRequest format**
The client shall send ActuatorRequest messages conforming to the specified JSON schema (command_value, status, safe_default_used, reason).

**SV-INT-03 - Strict-A isolation**
Strict-A logic shall not directly handle JSON strings, sockets, or timestamps; it shall operate exclusively on normalized numeric values and configuration.

---

#### 3.4.5 Test & Coverage Requirements

**SV-TEST-01 - Unit coverage**
All Strict-A modules shall achieve **100% statement coverage** and **≥ 95% branch coverage**.

**SV-TEST-02 - MC/DC**
All decision points in Strict-A logic (envelope, fallback, status classification) shall be covered by MC/DC-style tests.

**SV-TEST-03 - Fault injection coverage**
The test suite shall exercise all six fault modes:
`normal`, `high_fault`, `low_fault`, `severe_disagreement`, `frozen`, `stuck_drift`,
and verify the resulting statuses and outputs.

## 4. High-Level Architecture
```text
 ┌─────────────────────────┐
 │ Sensor Simulator (Core-C)│
 │  - Fault injection       │
 │  - JSON schema outputs   │
 │  - TCP server            │
 └───────────┬─────────────┘
             │ JSON/TCP
             ▼
 ┌─────────────────────────┐
 │ CRSS Client App         │
 │  - JSON parsing (Core-C)│
 │  - Framing/shape checks │
 │    (Core-C / Strict-B)  │
 │  - Inner Orchestrator   │
 │    (Strict-B)           │
 │  - Voting + Envelope    │
 │    + Rate-limiting      │
 │    + Safe-default       │
 │    (Strict-A @critical) │
 └───────────┬─────────────┘
             │ JSON/TCP
             ▼
 ┌─────────────────────────┐
 │ Actuator Sink (Core-C) │
 │ Logs + Acknowledges     │
 │ Receives ActuatorRequest│
 └─────────────────────────┘
```

All safety-critical calculations are pure functions in Strict-A. All nondeterministic activity stays in Core-C.

## 5. Key CRSS Compliance Principles Used
- **Strict determinism in critical logic**
  No randomness, no I/O, no GC, no dynamic creation in Strict-A.
- **Phase-aware profiles**
  - Strict-A: envelope, fallback, clamps
  - Core-B: deterministic voting
  - Core-C: everything else (TCP, JSON, simulator, logging)
- **Bounded operations**
  All loops are bounded; all lists have fixed length.
- **Explicit SAFE_DEFAULT**
  Failures always resolve into a bounded safe state.
- **Fault injection + MC/DC ≥ 95%**
  The example includes a full test suite ensuring CRSS verification quality.

## 6. Actors and Data Flow
Inputs:
- Three simulated sensors
- Fault modes applied via deterministic or random model
- Gateway sends SensorFrame messages to the client

Outputs:
- Actuator command with:
  - bounded value
  - deterministic reasoning
  - safe default fallback
  - fault-aware status classification

Execution loop:
- Runs indefinitely at a nominal period of 60 ms.

## 7. Profiles and Criticality Zones
| Component                     | CRSS Profile |
|------------------------------|--------------|
| Safety Envelope              | Strict-A     |
| Safe-default mechanism       | Strict-A     |
| Severe-disagreement detection| Strict-A     |
| Voting logic                 | Core-B       |
| JSON schema validation       | Core-C       |
| TCP I/O                      | Core-C       |
| Logging                      | Core-C       |
| Simulation of sensors        | Core-C       |
| Actuator sink                | Core-C       |

Strict-A logic must remain pure, side-effect free, deterministic, and isolated.

## 8. Detailed External Interface
The system exchanges two message types:
- `SensorFrame` (gateway → CRSS client)
- `ActuatorRequest` (CRSS client → gateway)

Both are JSON, line-delimited, UTF-8 encoded. This ensures maximal tooling compatibility and allows integration on Windows, Linux, embedded shells, or cloud systems.

## 9. Message Timing Requirements
- Sensor frames must arrive approximately every 60 ms.
- Client must produce a corresponding actuator output for every frame.
- Long gaps (>200 ms) are interpreted as gateway degradation (Core-C concern).
- Strict-A logic must complete within a stable deterministic execution bound.

## 10. Data Model (Full Definition)
The reference system exchanges two structured message types:

- `SensorFrame` - from gateway simulator to CRSS client
- `ActuatorRequest` - from CRSS client to gateway

Both are line-delimited JSON objects.

### 10.1 SensorFrame Structure
A `SensorFrame` represents a single synchronous sampling of three physical sensors measuring cooling temperature (degC).

```json
{
  "sensor_ids": ["T1", "T2", "T3"],
  "unit": "degC",
  "values": [1.52, 1.48, 1.49],
  "timestamp": 1764771503.3181,
  "source_status": "OK",
  "sensor_statuses": ["OK", "OK", "OK"]
}
```

**Fields:**

| Field           | Type        | Description                         | Constraints                  |
|----------------|------------|-------------------------------------|------------------------------|
| `sensor_ids`   | List[str]   | Names of sensors                    | Must be exactly 3 items      |
| `unit`         | str         | Always `"degC"` in this example     | Equality check applied       |
| `values`       | List[float] | Raw sensor floating-point readings  | Must be exactly 3 values     |
| `timestamp`    | float       | UNIX epoch timestamp                | Must increase monotonically  |
| `source_status`| str         | Gateway-level status                | `"OK"`, `"DEGRADED"`, `"ERROR"` |
| `sensor_statuses`| List[str] | Per-sensor status                   | Length 3, values `"OK"`/`"ERROR"` |

### 10.2 SensorFrame Validation Rules (Core-C)
Validation must enforce:
- `sensor_ids` length = 3
- `sensor_statuses` length = 3
- `values` length = 3
- `unit == "degC"`
- All statuses in allowed sets
- `timestamp` monotonic (soft warning only)
- Values must be parseable floats

Warnings are emitted when:
- status mismatches values (e.g., status `OK` but value implausible)
- large sudden jumps are not flagged by status
- degenerate timestamp behavior occurs

Warnings remain Core-C and do not affect Strict-A determinism.

## 11. ActuatorRequest Structure
Returned by the Strict-A/Core-B client logic back to the gateway.

```json
{
  "command_value": 1.5,
  "status": "NORMAL",
  "safe_default_used": false,
  "reason": "OK"
}
```

**Fields:**

| Field             | Type   | Description                                      |
|-------------------|--------|--------------------------------------------------|
| `command_value`   | float  | Final envelope-limited actuator value           |
| `status`          | str    | `"NORMAL"`, `"DEGRADED"`, or `"FAILSAFE"`       |
| `safe_default_used`| bool  | Indicates if `SAFE_DEFAULT` was applied         |
| `reason`          | str    | Contextual explanation (`"OK"`, `"SEVERE_DISAGREEMENT"`, etc.) |

## 12. JSON Schemas (Canonical Version)
These schemas define the on-wire protocol.

### 12.1 SensorFrame Schema
```json
{
  "type": "object",
  "required": [
    "sensor_ids", "unit", "values",
    "timestamp", "source_status", "sensor_statuses"
  ],
  "properties": {
    "sensor_ids": {
      "type": "array",
      "minItems": 3,
      "maxItems": 3,
      "items": { "type": "string" }
    },
    "unit": { "type": "string", "enum": ["degC"] },
    "values": {
      "type": "array",
      "minItems": 3,
      "maxItems": 3,
      "items": { "type": "number" }
    },
    "timestamp": { "type": "number" },
    "source_status": {
      "type": "string",
      "enum": ["OK", "DEGRADED", "ERROR"]
    },
    "sensor_statuses": {
      "type": "array",
      "minItems": 3,
      "maxItems": 3,
      "items": {
        "type": "string",
        "enum": ["OK", "ERROR"]
      }
    }
  }
}
```

### 12.2 ActuatorRequest Schema
```json
{
  "type": "object",
  "required": [
    "command_value", "status",
    "safe_default_used", "reason"
  ],
  "properties": {
    "command_value": { "type": "number" },
    "status": {
      "type": "string",
      "enum": ["NORMAL", "DEGRADED", "FAILSAFE"]
    },
    "safe_default_used": { "type": "boolean" },
    "reason": { "type": "string" }
  }
}
```

## 13. Fault Model: Full Specification
The reference example simulates six deterministic fault modes. Fault selection follows either:
- deterministic `forced_mode` (for testing), or
- probabilistic distribution based on RNG seed at runtime.

### 13.1 Fault Modes Overview
| Mode                | Description                              | Real-World Analogy                       |
|---------------------|------------------------------------------|------------------------------------------|
| `normal`            | small Gaussian-like noise               | stable sensor                            |
| `high_fault`        | one channel unrealistically high        | hardware spike / thermal runaway         |
| `low_fault`         | one channel unrealistically low         | short to ground / ADC underflow          |
| `severe_disagreement`| all channels diverge strongly          | cross-talk or mixed-sensor failure       |
| `frozen`            | all values repeat indefinitely          | dead sensor / broken sampling            |
| `stuck_drift`       | very slow drift from mid-range          | aged sensor drifting out of calibration  |

### 13.2 Deterministic Fault Selection
```python
SimulatedSensors(seed=123, forced_mode=None)
```

Distribution (implementation v3):

| Probability | Mode               |
|-------------|--------------------|
| 50%         | normal             |
| 20%         | high_fault         |
| 15%         | low_fault          |
| 5%          | severe_disagreement|
| 5%          | frozen             |
| 5%          | stuck_drift        |

Tests may use:
```python
SimulatedSensors(seed=1, forced_mode="frozen")
```

## 14. Sensor Simulation: Full Behavioral Specification
This section fixes missing details and aligns the specification with the v3 code.

### 14.1 Value Generation Base Logic
```python
base = uniform(0.5, 4.5)
values = [base + noise() for _ in range(3)]
noise() = uniform(-0.05, 0.05)
```

These do not represent safety bounds; they approximate sensor physics.

### 14.2 Mode: high_fault
- Choose random index `i`.
- Apply: `values[i] += 2.5`.
- Large spread is guaranteed.
- Value may remain inside physical safe band, which is acceptable.
- Strict-A still treats it as disagreement based on spread detection.

### 14.3 Mode: low_fault
Same as `high_fault` but subtract `2.5` instead of adding.

### 14.4 Mode: severe_disagreement
Produce a tri-modal distribution:
```python
values = [base - 2.0, base, base + 2.0]
```

### 14.5 Mode: frozen
- On first call, freeze current `values`.
- All subsequent outputs reuse the same frozen triplet.
- Timestamp still increases (gateway responsibility).

### 14.6 Mode: stuck_drift
- Initialize `stuck_value = 2.5`.
- Each frame drifts by ±0.05 and is clamped to `[0.0, 5.0]`.
- Current frame values derive from `stuck_value` plus small noise.

## 15. Voting Algorithm (Core-B Deterministic Logic)
The voting algorithm is designed to:
- remove obvious outliers
- detect single-channel failures
- detect severe multi-channel disagreement
- provide stable output

### 15.1 Pre-Voting Checks
- All lists must be length 3.
- Values must be finite floats (no NaN or inf).
- No missing entries.

### 15.2 Spread and Disagreement
```python
spread = max(values) - min(values)
```

- If `spread > plausibility_threshold` → severe disagreement.
- Else if exactly one outlier exceeds threshold → degraded.
- Else → normal.

`plausibility_threshold` comes from `SafetyConfig`.

### 15.3 Voting Rule
The voted value is always the median:
```python
voted_value = median(values)
```
This matches common TMR practice.

### 15.4 Voting Status Output
| Condition            | Returned Status          |
|----------------------|-------------------------|
| normal spread        | `"NORMAL"`              |
| one outlier          | `"DEGRADED"`            |
| severe disagreement  | `"SEVERE_DISAGREEMENT"` |

Note: `SEVERE_DISAGREEMENT` is not yet a failsafe event; Strict-A envelope decides how to react.

## 16. Safety Envelope (Strict-A)
### 16.1 Inputs
- `voted_value` (from Core-B)
- `previous_output`
- `SafetyConfig` containing:
  - `min_safe`
  - `max_safe`
  - `max_delta`
  - `plausibility_threshold`
  - `fallback_value` (SAFE_DEFAULT)
  - `initial_output`

### 16.2 Clamp to Safe Bounds
```python
clamped = clamp(voted_value, min_safe, max_safe)
```

### 16.3 Rate Limiting
```python
delta = clamped - previous_output
if abs(delta) > max_delta:
    final = previous_output + sign(delta) * max_delta
else:
    final = clamped
```

### 16.4 Severe Disagreement → FAILSAFE
When status is `"SEVERE_DISAGREEMENT"`:
```python
final = SAFE_DEFAULT
status = "FAILSAFE"
safe_default_used = True
reason = "SEVERE_DISAGREEMENT"
```

### 16.5 Frozen Sensors
Frozen sensors are detected implicitly by observing identical values across multiple frames;
the gateway does not transmit a dedicated "FROZEN" status:
```python
final = previous_output  # stable hold
status = "DEGRADED"
reason = "FROZEN_SENSORS_DETECTED"
```

### 16.6 Stuck-Drift Behavior
Slow drift is allowed as long as envelope clamps and rate limits maintain safety. The system may remain `"NORMAL"` or `"DEGRADED"` depending on configuration and drift magnitude.

## 17. Actuator Command Classification
The controller produces status values:
- `"NORMAL"`
- `"DEGRADED"`
- `"FAILSAFE"`

`"FAILSAFE"` is only produced by Strict-A (envelope / SAFE_DEFAULT logic).

## 18. Logging Rules (Core-C)
The implementation logs:
- gateway sending frames
- client receiving frames
- client sending commands
- gateway receiving commands
- warnings for mismatches:
  - error status but plausible value
  - OK status but implausible value
  - unexpected drift
  - frozen or stuck-drift detection events

Logging is purely diagnostic and entirely outside Strict-A.

## 19. Execution Model (End-to-End)
The system follows a deterministic, safety-oriented loop:

```python
initialize_configuration()
previous_output = initial_output

connect_to_gateway()
while True:
    frame = read_sensor_frame()
    parsed_values = validate_and_extract(frame)
    voted_value, vote_status = compute_voted_value(parsed_values)
    final_value, envelope_status, safe_default = apply_safety_envelope(
        voted_value,
        previous_output,
        SafetyConfig
    )
    send_actuator_request(final_value, envelope_status, safe_default)
    previous_output = final_value
```

Execution continues until:
- user presses Ctrl+C
- a fatal network failure occurs (Core-C)
- the deployment environment forces shutdown

Strict-A code never handles exceptions nor performs retries - exception handling belongs to Core-C.

## 20. Timing Constraints
This reference example does not implement real-time scheduling, jitter monitoring, deadlines, or latency tracking.
Instead:

- The gateway simply emits SensorFrame every ≈60 ms.
- The client processes frames upon arrival.
- Strict-A logic remains deterministic and bounded, but no explicit execution deadlines are enforced.
- No gateway degradation logic is implemented beyond JSON validity and socket errors.

This example demonstrates CRSS-compliant structure, not real-time behavior.
Real applications must define domain-appropriate timing constraints separately.

## 21. Configuration Model (CRSS-Compliant)
All configuration is immutable after startup.

Example config:
```json
{
  "min_safe": 0.0,
  "max_safe": 5.0,
  "max_delta": 0.5,
  "plausibility_threshold": 0.2,
  "fallback_value": 0.0,
  "initial_output": 0.0
}
```

### 21.1 CRSS Constraints for Config
Configuration:
- must not be modified by runtime logic
- must be validated once at startup
- must not contain dynamic lists or nested dicts of unbounded size
- must not contain external code references

### 21.2 Parameters
| Field                 | Meaning                            | CRSS Notes              |
|-----------------------|------------------------------------|-------------------------|
| `min_safe`            | safe actuator lower bound          | Strict-A clamp          |
| `max_safe`            | safe actuator upper bound          | Strict-A clamp          |
| `max_delta`           | rate limit step per cycle          | Strict-A bounded delta  |
| `plausibility_threshold`| spread beyond which voting is invalid | used in Core-B     |
| `fallback_value`      | SAFE_DEFAULT                       | must be constant        |
| `initial_output`      | boot output                        | must still obey bounds  |

## 22. CRSS Compliance Mapping (Full Version)
This expands the shorter table from the high-level spec.

### 22.1 Strict-A Responsibilities
Strict-A code must:
- be pure, deterministic, and side-effect free
- avoid:
  - file I/O
  - sockets
  - randomness
  - exceptions crossing boundaries
  - logging
  - dynamic structures and class mutation

Strict-A implements:
- clamp
- rate limit
- severe disagreement fallback
- SAFE_DEFAULT logic
- single-sensor freeze handling
- drift mitigation
- output status classification

Strict-A must satisfy:
- bounded WCET
- MC/DC ≥ 95%
- 100% branch determinism
- static memory footprint

### 22.2 Core-B Responsibilities
Core-B implements non-critical, deterministic orchestration and integration helpers that are **not** on the Level-A critical decision path.

Typical Core-B responsibilities in this example:
- non-critical application loops (offline step runner, TCP client controller harness)
- calling the Strict-B inner orchestrator with already-framed inputs
- scheduling / GC control (non-critical)
- error handling and restart logic around non-critical infrastructure

Core-B MUST NOT implement or duplicate Level-A safety logic such as voting, envelope application, SAFE_DEFAULT selection, or safety status classification (those are Strict-A).
### 22.3 Core-C Responsibilities
Core-C handles:
- TCP networking
- JSON parsing and schema validation
- logging
- simulation
- error reporting
- interaction with the environment

Core-C is allowed:
- threads (optional)
- GC
- dynamic memory
- OS calls

But Core-C must:
- not contaminate strict logic
- not leak nondeterminism into Strict-A
- enforce schema correctness
- isolate external faults

## 23. Test & Verification Requirements (Full)
Testing and verification are central to this reference example.

### 23.1 Unit Testing Requirements
Required coverage:

| Component              | Profile | Required Coverage                        |
|------------------------|---------|------------------------------------------|
| Strict-A (envelope)    | Strict-A| 100% line, 100% branch, ≥95% MC/DC       |
| Core-B (voting)        | Core-B  | 100% line, ≥95% MC/DC                    |
| Simulation logic       | Core-C  | best effort                              |
| JSON handling          | Core-C  | schema validation tested                 |
| TCP client             | Core-C  | smoke tests only                         |

Strict-A unit test guidelines:
- no randomness
- pure functional assertions
- edge-case testing, including:
  - maximum ramp
  - sign changes
  - borderline deltas
  - boundary clamping
  - SAFE_DEFAULT transitions

### 23.2 MC/DC Requirements
MC/DC must cover:
- branch transitions inside envelope
- severe disagreement → fallback paths
- clamp vs non-clamp paths
- `max_delta` vs fine-grained deltas
- sign-changing deltas
- previous-state memory behavior

The version 3 test suite achieves approximately 95-98% MC/DC.

### 23.3 Integration Tests
Integration tests must validate:
- full round-trip: gateway → client → gateway
- correct propagation of fault injection effects
- severe disagreement producing FAILSAFE
- TCP pipeline operating correctly for at least 5 seconds
- sensor freeze → stable output behavior
- stuck drift → slowly evolving output

### 23.4 Fault Injection Testing Requirements
Fault injection tests must include, at minimum:
- `normal`
- `high_fault`
- `low_fault`
- `severe_disagreement`
- `frozen`
- `stuck_drift`

Tests must assert:
- correct spread interpretation
- correct envelope fallback behavior
- correct status classification
- SAFE_DEFAULT application where required
- absence of nondeterministic exceptions

## 24. CI/CD Pipeline Requirements
The reference CI/CD pipeline must:
- use pinned Python version (3.11)
- pin unit test + coverage packages
- run full unit test suite
- run coverage with branch + MC/DC reporting
- upload coverage artifacts
- perform a TCP smoke test

Recommended extensions:
- Windows + Linux matrix
- coverage gates (≥90%)
- MC/DC gating (≥95%)
- JSON schema linting
- static analysis (ruff, mypy)

## 25. Deployment and Runtime Environment
Even for a reference system, CRSS defines deployment constraints.

### 25.1 Environment Freezing
Deployment must:
- pin Python version
- freeze dependencies
- prohibit OS-driven automatic upgrades

### 25.2 Execution Isolation
At minimum, Python should run in:
- a container (e.g., Docker), or
- a dedicated virtual environment, or
- a standalone Python installation without shared system libs

### 25.3 Safety Lifecycle Requirements
Deployment must include:
- versioned artifacts
- test evidence
- fault injection evidence
- configuration freeze snapshots
- SCEM artifacts (Safety Case Evidence Model)
- TEP (Test Evidence Package / Tool Evaluation Plan, per your governance)
- CBM (Configuration Baseline Manifest)

## 26. Shutdown and Restart Behavior
On shutdown (Ctrl+C):
- Core-C handles `KeyboardInterrupt`.
- Strict-A logic is not involved.
- Client closes TCP socket gracefully.
- Gateway stops emitting frames.

On restart:
- previous output resets to `initial_output`.

This matches CRSS principles: no hidden state and no unintended side effects.

## 27. Informative Domain-Specific Notes
This reference system is suitable for:
- automotive: thermal management, sensor fusion
- medical: temperature-controlled environments
- industrial: process line monitoring
- robotics: multi-sensor estimation

This implementation fully satisfies the provided functional and safety specifications.
It is not tied to any specific domain (automotive, medical, industrial).
Real-world use requires domain-specific timing, performance, and safety constraints to be defined externally.
Once such constraints are defined, this design can serve as an actual certified subsystem.
