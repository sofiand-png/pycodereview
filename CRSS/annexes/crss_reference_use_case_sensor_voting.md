# CRSS-Python Reference Use Case  
## Redundant Sensor Voting + Safe Actuator Limiting  
Version: 1.0  
Status: Informative Example  
© 2025 Sofian Daghsen — All rights reserved  

---

# 🎯 Overview

This reference use case demonstrates how to design a **CRSS-Core + CRSS-Strict–compliant** safety subsystem using a small but realistic scenario: **redundant sensor voting** combined with a **safe actuator command limiter**.

This is intentionally inspired by aerospace / automotive supervisory safety logic (ASIL-D / SIL-3–style), but small enough to fit in **1–3 files**.

The system showcases:

- deterministic pure safety logic  
- clear separation of Strict vs Core responsibilities  
- explicit typing and state structs  
- MC/DC-friendly boolean conditions  
- no randomness, no I/O, no dynamic imports in Strict logic  
- clean architectural decomposition  

---

# 🔧 Functional Scenario  
## “Redundant Sensor Voting + Safe Actuator Limit”

We assume a rover / autonomous vehicle wheel-speed monitoring subsystem with:

- **3 redundant sensors**
- **commanded target speed**
- **configurable safety limits**
- **strict purity and determinism** for safety logic

### Inputs (per evaluation cycle)

- `sensor_a: float | None`
- `sensor_b: float | None`
- `sensor_c: float | None`
- `commanded_speed: float`
- `mode: Mode` (IDLE / ARMED / ACTIVE)

### Config / constants

- `MAX_SAFE_SPEED`
- `MAX_SENSOR_DIFF` — max allowed disagreement between sensors
- `MAX_ACCEL_STEP` — max allowed speed change per cycle
- `SENSOR_TIMEOUT_COUNT` — consecutive faults → safe mode

### Outputs

- `voted_speed: float | None`
- `limited_commanded_speed: float`
- `status: Status`  
  (OK, DEGRADED, SENSOR_FAULT, SAFE_MODE)
- `faults: list[FaultCode]`

---

# 🚦 Core Safety Logic (High-Level)

### 1. Sensor plausibility & voting

1. If ≥2 sensors present and within `MAX_SENSOR_DIFF`, use their **median** → `voted_speed`.
2. If only 1 plausible sensor available → `status = DEGRADED`.
3. If all sensors invalid or disagree →  
   `voted_speed = None`, `status = SENSOR_FAULT`.

---

### 2. Safe command envelope

- Enforce `commanded <= MAX_SAFE_SPEED`
- Enforce `|commanded - last_applied_speed| <= MAX_ACCEL_STEP`

---

### 3. Safe mode triggering

If sensors are faulty for `SENSOR_TIMEOUT_COUNT` consecutive cycles:

- enter `SAFE_MODE`
- output command = `0.0`

---

### 4. Determinism & purity

Strict safety logic must:

- be **pure**
- be **deterministic**
- not call I/O or use randomness
- not depend on system time
- operate only on explicit  
  `SensorSet`, `SafetyState`, `SafetyConfig`, `SafetyInputs`

This makes the system trivially machine-verifiable and MC/DC-testable.

---

# 📁 Suggested File Structure (1–3 Files)

## 1. `safety_types.py`  (Strict)

Contains CRSS-Strict-safe type definitions:

- Enums:
  - `Mode`
  - `Status`
  - `FaultCode`

- Dataclasses:
  - `SensorSet`
  - `SafetyConfig`
  - `SafetyState`
  - `SafetyInputs`
  - `SafetyOutput`

These enforce:

- clean typing
- no global mutable state
- data-only containers

---

## 2. `safety_logic.py` (CRSS-Strict)

All **strict, pure, deterministic** logic functions:

- `vote_sensors(sensor_set, config) -> (voted_speed, faults)`
- `limit_command(...) -> float`
- `update_safety_state(...) -> SafetyState`
- `evaluate_cycle(...) -> SafetyOutput`

Strict constraints demonstrated:

- no randomness  
- no I/O  
- no reflection  
- no dynamic imports  
- no lambdas  
- no global state  
- no unbounded loops  
- fully typed signatures  
- MC/DC-oriented conditions  

This file becomes the canonical example of **CRSS-Strict** coding.

---

## 3. `safety_runner.py` (CRSS-Core)

Optional Core-only wrapper that may:

- load config from JSON/YAML  
- read sample sensor logs  
- print results  
- feed data into strict logic  

This demonstrates proper CRSS architecture:

- **Strict**: pure safety logic
- **Core**: integration, config, and I/O

---

# 🧪 Why This Is an Ideal CRSS Demonstrator

- Clear separation of profiles (Core vs Strict)
- Perfect MC/DC case study  
- Pure functional core logic is deeply testable  
- Deterministic, bounded boolean conditions
- Canonical safety state struct used everywhere  
- Perfect example for:
  - call-chain promotion
  - mode assignment  
  - strict critical-phase behavior  
  - non-critical integration boundaries

---

# 🧷 Optional Short Name

**RWSM — Redundant Wheel-Speed Monitor**  
(“CRSS Safety Example – Sensor Voting & Safe Actuator Limit”)
