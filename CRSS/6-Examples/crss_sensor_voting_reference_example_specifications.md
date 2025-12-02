# CRSS-Python Reference Program – Sensor Voting & Actuator Safety Controller

**Version:** v1.0.0
**Status:** Informative (Reference Example)
**Maturity:** Stable Draft
© 2025 Sofian Daghsen – All rights reserved
Distributed under CC BY-NC-ND 4.0 — see LICENSE-CRSS.

---

## Table of Contents

- [0. Reference Program Overview](#0-reference-program-overview)
- [1. System Concept](#1-system-concept)
- [2. High-Level Safety Goals & Hazards](#2-high-level-safety-goals--hazards)
  - [2.1 Safety Goals (SG)](#21-safety-goals-sg)
  - [2.2 Hazards (H)](#22-hazards-h)
- [3. Operational Context & Assumptions](#3-operational-context--assumptions)
- [4. CRSS Safety Model for This Program](#4-crss-safety-model-for-this-program)
  - [4.1 Profiles Used](#41-profiles-used)
  - [4.2 Safety Levels](#42-safety-levels)
  - [4.3 Modes](#43-modes)
  - [4.4 Critical vs Non-Critical Phases](#44-critical-vs-non-critical-phases)
- [5. Architectural Design](#5-architectural-design)
  - [5.1 Repository / Package Layout](#51-repository--package-layout)
  - [5.2 Module Responsibilities](#52-module-responsibilities)
- [6. Interfaces & Data Flows](#6-interfaces--data-flows)
  - [6.1 Main Control Path (Critical)](#61-main-control-path-critical)
  - [6.2 Conceptual Data Types](#62-conceptual-data-types)
- [7. Mode Assignment Register (MAR)](#7-mode-assignment-register-mar)
- [8. Critical Boundary Declaration (CBD)](#8-critical-boundary-declaration-cbd)
- [9. SCEM Skeleton for This Program](#9-scem-skeleton-for-this-program)
- [10. Test & MC/DC Strategy](#10-test--mcdc-strategy)
  - [10.1 Units Under MC/DC Focus](#101-units-under-mcdc-focus)
  - [10.2 Example Boolean Decisions](#102-example-boolean-decisions)
  - [10.3 Fault Injection Scenarios](#103-fault-injection-scenarios)
- [11. Sensor Simulation Strategy](#11-sensor-simulation-strategy)
- [12. Execution Model](#12-execution-model)
- [13. CRSS Rule Constraints (Relevant Subset)](#13-crss-rule-constraints-relevant-subset)

---

## 0. Reference Program Overview

**Name:** CRSS-Python Sensor Voting & Actuator Safety Controller

**Goal:** Provide a small but fully CRSS-compliant **Strict-A** example that demonstrates:

- sensor voting on redundant inputs
- a safety envelope on actuator output (min/max + rate limiting)
- strict separation of **critical** vs **non-critical** code and phases
- use of **Core / Strict Profiles** and **Safety Levels (A/B/C)**
- concrete **Modes**, **SCEM** artifacts, and **MC/DC** coverage
- a realistic path to full CI/CD later using a CRSS reference Docker image

This program is the flagship **reference use case**.
Micro examples per individual rule live separately and are not duplicated here.

---

## 1. System Concept

We model a small but realistic safety-supervisory control function.

A **Safety Controller** reads three redundant sensor channels measuring the same physical quantity (e.g. steering angle, torque, or pressure) and produces a **safe actuator command** for a downstream actuator (e.g. valve, brake modulator, or motor controller).

**Key features:**

- **Redundant sensors:** three channels `S1`, `S2`, `S3`.
- **Sensor voting:** identify faulty readings and compute a safe representative value.
- **Safety envelope:** clamp the command within safe `min/max` and apply per-step rate limits.
- **Critical path:** validated sensor data → safety logic → actuator command.
- **Non-critical path:** logging, sensor simulation, configuration loading, diagnostics, CLI.

The example is intentionally small but powerful enough to demonstrate a convincing safety story aligned with the CRSS standard.

Target python version: 3.11
Target supported OS: Windows, Linux

---

## 2. High-Level Safety Goals & Hazards

### 2.1 Safety Goals (SG)

- **SG-1 – Safe envelope:**
  The Safety Controller must not command an actuator value that exceeds a safe envelope
  (`MIN_SAFE ≤ cmd ≤ MAX_SAFE`) under any circumstances.

- **SG-2 – Single-fault tolerance (sensors):**
  The Safety Controller must tolerate one faulty sensor (1-out-of-3) without issuing an unsafe command.

- **SG-3 – Fail-safe on severe disagreement:**
  If available sensors disagree beyond a configured plausibility threshold, the Safety Controller must fail safe
  (e.g. hold last safe command or use a known-safe default command).

- **SG-4 – Deterministic @critical path:**
  The Safety Controller must be deterministic in its `@critical` path:
  given the same inputs and internal state, it must produce the same output on every run.

- **SG-5 – No non-deterministic Python features in Strict-A:**
  The Strict-A critical path must not rely on Python features that can introduce non-determinism
  (e.g. GC-visible allocation, threads, async scheduling, random number generation, system time).

- **SG-6 – Bounded control logic:**
  Strict-A logic must not contain unbounded loops, recursion, or unbounded collection growth.
  All loops must be statically bounded (e.g. over the fixed set of three sensors).

- **SG-7 – Isolation of non-critical behavior:**
  Faults in non-critical code (simulation, logging, config loading, CLI) must **not** affect the behavior of the
  Strict-A `@critical` path beyond defined safe fallback modes.
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

### 2.2 Hazards (H)

- **H-1 – Unsafe actuator command:**
  Actuator command outside the safe envelope, leading to hazardous physical behavior.

- **H-2 – Incorrect voting:**
  Voting logic incorrectly accepts faulty sensor data, causing unsafe actuator commands.

- **H-3 – Undetected sensor drift:**
  Slow drift of one or more sensors leads to subtle but long-term unsafe outputs.

- **H-4 – Sensor disagreement mishandled:**
  Multiple sensors disagree and the controller fails to enter a safe degraded or fail-safe mode.

- **H-5 – Non-deterministic execution:**
  Timing, GC, or async behavior causes non-repeatable control outputs for identical inputs.

- **H-6 – Non-critical faults bleed into critical path:**
  Errors in logging, configuration loading, sensor simulation, or CLI cause changes to
  the Strict-A decision logic or mask unsafe behavior.

---

## 3. Operational Context & Assumptions

- Execution occurs in a **periodic control loop** (e.g. every 10 ms or 50 ms) in the target system.
- Python is used for the safety logic at **Strict-A**, within a supervised environment.
- Underlying scheduling and OS behavior are assumed sufficiently reliable (out of scope for this example).
- Sensors are abstracted as data sources providing scalar values (`float` or `Decimal`).
- We assume no hard real-time guarantees, but we require **bounded execution time** of the Strict-A loop.
- In the demonstrator, sensors are simulated **in-process**; in a real system they would be sourced from hardware or a separate service.

---

## 4. CRSS Safety Model for This Program

We apply CRSS-Python constructs explicitly.

### 4.1 Profiles Used

- **Strict Profile:** all safety-relevant logic and actuator commands.
- **Core Profile:** utilities and infrastructure:
  - logging
  - simulation
  - configuration loading
  - CLI harness / orchestration

### 4.2 Safety Levels

- **Level A:** Safety Controller core decisions (sensor voting, envelope, actuator command).
- **Level B:** Sensor interfaces and configuration model.
- **Level C:** Simulation, diagnostics, logging, CLI, and test harness.

### 4.3 Modes

Mode = `Profile × Safety Level`.

- **Strict-A:** Safety-critical decision logic and actuator command.
- **Strict-B:** Safety-relevant support modules (typed config, interfaces).
- **Core-B:** Non-critical but safety-adjacent configuration and orchestration.
- **Core-C:** Logging, simulation, CLI, tests.

### 4.4 Critical vs Non-Critical Phases

- **`@critical` phase**
  Execution of the control step that:
  - reads **validated** sensor values,
  - computes the safe actuator command (voting + envelope),
  - emits a pure **actuator command structure**.

- **Non-critical phase**
  Includes:
  - sensor simulation or hardware driver wrappers,
  - configuration loading,
  - logging and diagnostics,
  - CLI + orchestration,
  - offline analysis, MC/DC testing, coverage.

This program applies CRSS phase-aware interpretation:

- Non-critical components (sensor simulation, logging, config loader) MAY prepare inputs for
  Strict-A logic only when:
  1. Inputs satisfy their type and structural constraints.
  2. Inputs contain no nondeterministic artifacts.
  3. Inputs are validated before crossing the critical boundary.

Strict-A logic MUST NOT depend on any non-critical side effects.

Strict-A logic MAY accept inputs originating from non-critical modules (e.g., sensor drivers,
config loader, simulation), provided these inputs are validated, deterministic, and passed as
pure data without accompanying side effects.

---

## 5. Architectural Design

### 5.1 Repository / Package Layout

Conceptual repository layout:

```text
crss_example_sensor_voting/
  src/
    crss_phase/                # tiny package for @critical markers, metadata
      __init__.py
      markers.py
    crss_modes/                # optional: modes / MAR metadata as data
      __init__.py
      modes.py

    sensors/                   # sensor abstraction & simulation
      __init__.py
      interfaces.py            # Strict-B types, contracts (no I/O)
      simulation.py            # Core-C deterministic simulation only

    safety_logic/              # core Strict-A code
      __init__.py
      voting.py                # Strict-A @critical voting logic
      envelope.py              # Strict-A @critical envelope & rate limit
      controller.py            # Strict-A SafetyController (ties voting+envelope)

    actuator/
      __init__.py
      interface.py             # Strict-A actuator command structure (pure)

    config/
      __init__.py
      model.py                 # Strict-B typed configuration model
      loader.py                # Core-B config loader (file/env), non-critical

    logging_utils/
      __init__.py
      logger.py                # Core-C logging utilities

    app/
      __init__.py
      main_loop.py             # Orchestrates phases, CLI entrypoint (Core-B/C)
      run_once.py              # Single-step demo / tests

  tests/
    unit/                      # pure unit tests by module
    mcdc/                      # explicit MC/DC tests for Strict-A decisions
    integration/               # integration tests for app/main_loop

  scem/
    mar.yaml                   # Mode Assignment Register
    cbd.yaml                   # Critical Boundary Declaration
    deps.yaml                  # Dependency graph & mode propagation
    cbm.json                   # Configuration Baseline Manifest
    rcr.yaml                   # Rule Compliance Report
    tep.yaml                   # Test Evidence Package
    crc.yaml                   # Certification Readiness / summary

  README.md
  design_spec.md               # this document
```

### 5.2 Module Responsibilities

- **`crss_phase.markers`**
  - Provides `@critical` / `@non_critical_phase` (or equivalent) decorators and phase metadata.
  - Purely syntactic markers for tools; no behavioral logic.

- **`crss_modes`**
  - Optionally encodes mode metadata (`Strict-A`, `Core-B`, …) as data for tooling and SCEM export.

- **`sensors.interfaces`** (Strict-B)
  - Defines typed interfaces / protocols for reading sensors.
  - No I/O; no simulation; pure contracts and type definitions.

- **`sensors.simulation`** (Core-C, non-critical)
  - Deterministic sensor simulation driven by a fixed seed.
  - Generates a “true” physical value plus bounded noise per channel.
  - Can introduce controlled fault modes (stuck-at, drift, spikes).
  - Used only in non-critical phases and tests.

- **`safety_logic.voting`** (Strict-A, `@critical`)
  - Implements voting logic over the three redundant sensor channels.
  - Responsibilities:
    - plausibility checks per sensor,
    - 2-out-of-3 (or equivalent) voting,
    - detection of major sensor disagreement,
    - safe fallback strategy when disagreement or insufficient valid sensors occur.
	- Fallback Priority Clarification:
	If both LAST_SAFE_VALUE and SAFE_DEFAULT are viable fallback options, the controller MUST
	prefer SAFE_DEFAULT. This ensures deterministic and conservative safety behavior.

  - Must be:
    - pure (no I/O, no logging),
    - without unbounded loops (only fixed iteration over 3 sensors),
    - exception-free at the interface (no exceptions cross the critical boundary),
    - free of dynamic allocation beyond trivial bounded temporaries.

Fallback conditions MUST be handled deterministically in the following order:

1. **Two or more sensors fail plausibility → FAILSAFE**
   - Output: SAFE_DEFAULT

2. **Exactly one sensor fails but two remain plausible**
   - Output: average of the two plausible sensors

3. **All three sensors are plausible**
   - Output: average of all three

4. **Envelope or rate limiter detects unsafe condition**
   - Output: clamped or rate-limited value

5. **Any internal error, inconsistency, or undefined state**
   - Output: SAFE_DEFAULT

- **`safety_logic.envelope`** (Strict-A, `@critical`)
  - Applies safety envelope and rate limiting:
    - clamp output between `MIN_SAFE` and `MAX_SAFE`,
    - enforce per-step rate-of-change limits (`max_delta_per_step`),
    - choose a safe fallback (e.g. last safe command or defined safe default) on violations.
  - Same determinism and boundedness constraints as `voting`.
  - Formula: Let V be the voted sensor value and P be the previous actuator value.

		- Step 1: Hard Clamp
			- C = clamp(V, min_safe, max_safe)

		- Step 2: Rate Limit
			- If abs(C - P) > max_delta:
				  new_value = P + sign(C - P) * max_delta
				Else:
				  new_value = C

		- Step 3: Failsafe
			- If C was clamped due to envelope violation AND abs(C - P) > max_delta:
				new_value = SAFE_DEFAULT

		- Return new_value

- **`safety_logic.controller`** (Strict-A, `@critical`)
  - Orchestrates the Strict-A path:
    - consumes validated sensor readings and configuration,
    - calls `voting.compute_safe_value(...)`,
    - calls `envelope.apply_safety_limits(...)`,
    - produces an `ActuatorCommand` structure.
  - Maintains minimal bounded state (e.g. last safe output).
  - Guarantees no non-deterministic behavior, no I/O, no logging.

- **`actuator.interface`** (Strict-A boundary)
  - The Actuator Interface is the output boundary of the Strict-A Safety Controller.
	It MUST:
		- contain no I/O,
		- be pure and side-effect-free,
		- produce a deterministic structured command:
			 { "value": <float>, "status": <enum> }

	The reference program does NOT interface with hardware.
	Any downstream physical interaction occurs outside the scope of Strict-A logic.

- **`config.model`** (Strict-B)
  - Captures typed safety configuration:
    - safe envelope limits,
    - rate limiter settings,
    - plausibility thresholds,
    - timeouts.

- **`config.loader`** (Core-B, non-critical)
  - Loads configuration from static or slowly changing sources (JSON/YAML/env vars).
  - Executes only in non-critical phases (e.g. startup or explicit reload).
  - Errors must not directly impact the running Strict-A loop without a safe fallback.

- **`logging_utils.logger`** (Core-C, non-critical)
  - Simple, robust logging facility (e.g. console logging) with best-effort behavior.
  - Failures to log must not influence safety behavior.

- **`app.main_loop`** (Core-B/C, non-critical orchestrator)
  - Provides top-level orchestration:
    - load or cache configuration,
    - initialize simulation or sensor interface,
    - read raw sensor values,
    - call the Strict-A SafetyController,
    - log or expose outputs in a non-critical way.
  - May implement a single-step `run_control_step()` or a demonstration loop.

Note: The `timestamp` field of `SensorReading` is permitted for diagnostics in non-critical
code but MUST NOT be used by any Strict-A logic. Strict-A modules SHALL treat sensor values
as pure numeric inputs. Timestamps MUST NOT influence any voting, envelope, fallback, or
safety-critical decision.

---

## 6. Interfaces & Data Flows

### 6.1 Main Control Path (Critical)

**Conceptual pseudo-flow:**

1. **`app.main_loop.run_control_step()`** (non-critical)
   - obtains raw sensor values via `sensors.interfaces.SensorSource`, implemented (in this example)
     by `sensors.simulation.SimulatedSensors`,
   - retrieves or caches `SafetyConfig` from `config.loader`.

2. **`SafetyController.step(raw_sensors, config)`** (Strict-A, `@critical`)
   - calls `voting.compute_safe_value(raw_sensors, config)`,
   - calls `envelope.apply_safety_limits(voted_value, previous_command, config)`,
   - returns an `ActuatorCommand` (pure data).

3. **`app.main_loop`** (non-critical)
   - passes `ActuatorCommand` across the critical boundary to a downstream layer,
   - in this reference example, it merely logs or prints the command.

The only `@critical` code resides in `safety_logic.controller`, `safety_logic.voting`, `safety_logic.envelope`, and (purely) `actuator.interface`.

### 6.2 Conceptual Data Types

These types are conceptual; concrete representation can be dataclasses, `NamedTuple`, or simple dicts, as long as they remain well-typed and deterministic in Strict-A code.

- **`SensorReading`**
  - `value: float | Decimal`
  - `timestamp: float` (monotonic time in non-critical path if needed)
  - `status: enum {OK, FAULTY, MISSING}`

- **`SafetyConfig`**
  - `min_safe: float`
  - `max_safe: float`
  - `max_delta_per_step: float`
  - `plausibility_threshold: float`
  - `sensor_timeout_ms: int`

- **`ActuatorCommand`**
  - `value: float` (bounded by `min_safe`/`max_safe`)
  - `status: enum {NORMAL, DEGRADED, FAILSAFE}`

---

## 7. Mode Assignment Register (MAR)

Conceptual **Mode Assignment Register** (D1 SCEM artifact), typically stored as `scem/mar.yaml`:

| Module                | Profile | Level | Mode      | Phase usage          |
|-----------------------|---------|-------|-----------|----------------------|
| `safety_logic.controller` | Strict  | A     | Strict-A | `@critical`          |
| `safety_logic.voting`     | Strict  | A     | Strict-A | `@critical`          |
| `safety_logic.envelope`   | Strict  | A     | Strict-A | `@critical`          |
| `actuator.interface`      | Strict  | A     | Strict-A | `@critical`          |
| `config.model`            | Strict  | B     | Strict-B | non-critical         |
| `config.loader`           | Core    | B     | Core-B   | non-critical         |
| `sensors.interfaces`      | Strict  | B     | Strict-B | non-critical         |
| `sensors.simulation`      | Core    | C     | Core-C   | non-critical only    |
| `logging_utils.logger`    | Core    | C     | Core-C   | non-critical only    |
| `app.main_loop`           | Core    | B     | Core-B   | orchestrator         |
| `crss_phase.markers`      | Core    | C     | Core-C   | infrastructural      |
| `tests.*`                 | Core    | C     | Core-C   | test-only            |

This table is the logical basis for SCEM **Mode Assignment Register** D1.

---

## 8. Critical Boundary Declaration (CBD)

The **critical boundary** surrounds:

- `safety_logic.controller`
- `safety_logic.voting`
- `safety_logic.envelope`
- `actuator.interface`

The **non-critical world** includes:

- sensor simulation and actual sensor drivers,
- configuration loading and validation logic,
- logging and diagnostics,
- CLI and orchestration layers,
- tests and coverage tooling.

**Boundary rules:**

- Only **pure data** crosses the boundary:
  - raw validated sensor values enter the critical core,
  - `ActuatorCommand` leaves the critical core.
- No direct logging, I/O, or external blocking calls from Strict-A modules.
- No third-party libraries are called from Strict-A modules.
- No exceptions cross the critical boundary; failures are reflected via safe, explicit data states.

The CBD is typically stored as `scem/cbd.yaml`.

---

## 9. SCEM Skeleton for This Program

Minimal but complete SCEM artifacts:

- **D1 — Mode Assignment Register**
  - **File:** `scem/mar.yaml`
  - Contains a structured representation of section 7.

- **D2 — Dependency Graph & Mode Propagation**
  - **File:** `scem/deps.yaml`
  - Shows:
    - `app.main_loop → safety_logic.controller` (Strict-A),
    - `safety_logic.controller → voting`, `envelope`, `actuator.interface`,
    - all Strict-A dependencies remain Strict-A or stricter; no demotion.

- **D3 — Rule Compliance Report (RCR)**
  - **File:** `scem/rcr.yaml`
  - Contains:
    - CRSS rules applied,
    - static analysis tooling used,
    - counts of violations and justifications,
    - residual risk assessment (ideally tiny or zero).

- **D4 — Test Evidence Package (TEP)**
  - **File:** `scem/tep.yaml`
  - Contains:
    - list of test suites (unit, MC/DC, integration),
    - coverage numbers (statement, branch, MC/DC) for Strict-A modules,
    - description of fault injection tests (sensor faults, missing sensors, out-of-range inputs, config errors).

- **D5 — Configuration Baseline Manifest (CBM)**
  - **File:** `scem/cbm.json`
  - Contains:
    - Python version (e.g. 3.11.9),
    - Docker image tag / environment hash,
    - tool versions,
    - dependency hashes (e.g. of `requirements.txt`).

- **D6 — Certification Readiness / Project Summary**
  - **File:** `scem/crc.yaml`
  - Contains a short summary:
    - all required artifacts exist,
    - Strict-A coverage targets are met,
    - no unresolved **BLOCKER** violations,
    - environment is pinned and reproducible.

---

## 10. Test & MC/DC Strategy

The goal is **high coverage** and **MC/DC** for Strict-A logic, while keeping tests conceptually small and readable.

### 10.1 Units Under MC/DC Focus

MC/DC focus units:

- `voting.compute_safe_value(sensor_values, config)`
- `envelope.apply_safety_limits(voted_value, prev_cmd, config)`

These functions contain the key boolean decisions that directly affect safety.
Custom small tool should be developed as part of the use case to calculare MC/DC (simple conditions only will occur in the program)

Unit test coverage: 100%
MC/DC test coverage: 95%
Condition and decision mapping coverage (truth-table verification): 100%
Integration test coverage: 100%

**Coverage.py configruation:**

The reference program uses coverage.py ONLY for:
- statement coverage
- branch coverage

Enforced configuration:

    - coverage run --branch -m pytest
    - coverage xml
    - coverage html

Coverage.py is classified as a Non-Critical Evidence Tool (NCET).
It MUST NOT be imported or executed from Strict-A modules.

### 10.2 Example Boolean Decisions

For **sensor voting**:

- `is_s1_valid`
- `is_s2_valid`
- `is_s3_valid`
- `has_major_disagreement`
- `use_fallback`

For **envelope**:

- `violates_min_max`
- `violates_rate_limit`
- `use_last_safe_value`

**MC/DC requirement:**
For each boolean condition, test pairs exist where only that condition changes and the overall decision outcome flips.

Dedicated MC/DC tests live in:

- `tests/mcdc/test_voting_mcdc.py`
- `tests/mcdc/test_envelope_mcdc.py`

### 10.3 Fault Injection Scenarios

Representative fault injection tests:

- Single sensor stuck-at value (`S1` stuck, `S2` & `S3` OK).
- One sensor noisy, consistently outside plausible range.
- Two sensors faulty → controller must fall back to last safe command or a safe default.
- Config with extremely narrow safe limits → controller still respects envelope and stays safe.

---

## 11. Sensor Simulation Strategy

We aim for deterministic but “realistic enough” simulation.

**Approach:**

- `sensors.simulation.SimulatedSensors`:
  - takes a **fixed seed** (from config or test),
  - generates a base “true” signal (e.g. ramp or sine wave),
  - adds small bounded noise to each sensor channel,
  - optionally injects fault modes:
    - stuck-at,
    - slowly drifting,
    - random spikes.

**In tests:**

- Tests set the random seed explicitly to guarantee reproducibility.
- SCEM TEP records which seeds were used for which test scenarios.

**In non-test demonstration runs:**

- The example should still use a fixed seed by default to keep behavior predictable and easy to reason about.

This keeps the overall system deterministic and aligned with CRSS determinism constraints.

---

## 12. Execution Model

For the **reference implementation**, the execution model is a simple **single-step** or short demonstration loop on top of the conceptual periodic control model.

**Single-step execution (demo):**

```bash
python -m app.main_loop
```

**Sequence:**

1. Load stable configuration (non-critical, `config.loader`).
2. Create deterministic sensor simulation or connect to a sensor interface (non-critical).
3. Read raw sensor values (non-critical).
4. Call the Strict-A controller:
   - voting,
   - envelope,
   - compute next safe command.
5. Produce an `ActuatorCommand` structure for the downstream actuation layer.
6. Terminate (no long-running real-time loop in the reference program).

**Properties:**

- No real-time scheduling assumptions in the example program.
- No uncontrolled timing dependencies or implicit concurrency.
- All safety-relevant behavior is captured in the Strict-A pure logic.

---

## 13. CRSS Rule Constraints (Relevant Subset)

The reference program is designed to comply with the following **subset** of CRSS-Python rules as they apply to Strict-A and related modes.

### 13.1 Determinism and Stable Execution Context
**Determinism:**
Garbage Collector Disablement:

Before entering any Strict-A function, the runtime MUST execute:

    gc.disable()

Strict-A modules MUST NOT:
- allocate complex temporary structures,
- trigger allocations that could re-enable GC.

The orchestrator MUST disable GC in the non-critical phase before invoking any Strict-A step.

- No threads or concurrency primitives used from Strict-A modules.
- No `async` / `await` in Strict-A code paths.
- No random number generation in critical code.
- No use of system time or wall-clock time in Strict-A logic.
- No mutable globals in Strict-A.

**Stable Execution Context:**

- Strict-A logic MUST execute under a Stable Execution Context (SEC):
	- No dynamic dispatch
	- No dynamic imports
	- No reflection or attribute injection
	- No runtime code generation
	- No mutable global state
	- No dependency on system time, wall-clock, environment variables, or OS state
	- No randomness or OS entropy sources
	- Fully deterministic code paths
	- Fixed iteration structure

### 13.2 Bounded Behavior

- No unbounded loops.
- Iteration only over the fixed sensor list of size 3 or other statically bounded sets.
- No recursion.
- No unbounded string or collection growth in Strict-A code.

The only loop in Strict-A logic iterates over exactly 3 sensors. This bound is fixed at compile-time
and cannot vary at runtime.

### 13.3 Dynamic Feature Restrictions

- No dynamic imports in Strict-A.
- No introspection / reflection-based behavior (`getattr` with dynamic names, monkey-patching, etc.) in Strict-A.
- No monkey-patching or runtime modification of Strict-A objects.
- No dynamic attribute creation on critical data structures.

### 13.4 Error Handling

- No exceptions may cross the critical boundary.
- Strict-A functions must signal error / degraded / fail-safe states via explicit data (e.g. `ActuatorCommand.status`).
- Fallback values must always preserve safety (e.g. inhibit command, last safe command, or safe default).

### 13.5 Data Rules

- Only immutable or effectively immutable, well-typed data crosses the critical boundary.
- `ActuatorCommand` must be fully typed and consistent (no partially initialized states).
- No direct references to mutable global state are passed into Strict-A functions.

### 13.6 Third-Party Libraries

- Strict-A modules must not call third-party libraries.
- The only permitted third-party tool in this example is `coverage.py` used **only** in non-critical test code.

### 13.7 Python Semantics

- All float comparisons in Strict-A must be stable and deterministic given the selected numeric model.
- No implicit coercions that alter safety decisions (e.g. mixed-type comparison quirks).
- No non-deterministic iteration over sets or dicts in critical code (use ordered data structures or explicit sorting if needed).

---

This specification defines the **intended behavior, architecture, and safety model** of the
“CRSS-Python Sensor Voting & Actuator Safety Controller” reference program and is the normative basis
for its implementation and verification against the CRSS-Python standard.
