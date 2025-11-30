# CRSS-Python Architecture Blueprint (Reference Example)

**Version:** v1.0.0
**Status:** Informative
**Maturity:** Stable
© 2025 Sofian Daghsen – All rights reserved
Distributed under CC BY-NC-ND 4.0 — see LICENSE-CRSS.

---

## Table of Contents

- [CRSS-Python Architecture Blueprint (Reference Example)](#crss-python-architecture-blueprint-reference-example)
  - [0. Purpose](#0-purpose)
  - [1. Example Scenario – Safety Supervisory System](#1-example-scenario-safety-supervisory-system)
  - [2. High-Level Architecture](#2-high-level-architecture)
    - [2.1 Logical View](#21-logical-view)
    - [2.2 Process View](#22-process-view)
  - [3. Component Breakdown](#3-component-breakdown)
    - [3.1 Components Overview](#31-components-overview)
    - [3.2 Critical vs Non-Critical](#32-critical-vs-non-critical)
  - [4. Modes & Phases in the Blueprint](#4-modes-phases-in-the-blueprint)
    - [4.1 Mode Assignment](#41-mode-assignment)
    - [4.2 Phase Interaction Rules](#42-phase-interaction-rules)
  - [5. Example Code – Core Critical Flow](#5-example-code-core-critical-flow)
    - [5.1 Input & Config (Non-Critical)](#51-input-config-non-critical)
- [input_gateway.py (Strict-B, non-critical)](#inputgatewaypy-strict-b-non-critical)
- [config_manager.py (Strict-B, non-critical)](#configmanagerpy-strict-b-non-critical)
    - [5.2 Safety Controller (Strict-A)](#52-safety-controller-strict-a)
- [safety_controller.py (Strict-A)](#safetycontrollerpy-strict-a)
    - [5.3 Decision Publishing (Non-Critical)](#53-decision-publishing-non-critical)
- [decision_publisher.py (Strict-B, non-critical)](#decisionpublisherpy-strict-b-non-critical)
    - [5.4 Orchestrator (Non-Critical Main Loop)](#54-orchestrator-non-critical-main-loop)
- [main_supervisor.py (Strict-B orchestrator)](#mainsupervisorpy-strict-b-orchestrator)
  - [6. Deployment & CBM View](#6-deployment-cbm-view)
    - [6.1 Deployment Diagram](#61-deployment-diagram)
    - [6.2 CBM Excerpt](#62-cbm-excerpt)
  - [7. Compliance Story for the Blueprint](#7-compliance-story-for-the-blueprint)
    - [7.1 Modes and Enforcement](#71-modes-and-enforcement)
    - [7.2 What Makes This Certifiable?](#72-what-makes-this-certifiable)
  - [8. How to Adapt This Blueprint](#8-how-to-adapt-this-blueprint)
  - [9. Summary](#9-summary)

---

## 0. Purpose

This document provides a **complete reference architecture blueprint** for a CRSS-Python–compliant system.

It is designed to show, end-to-end:

- How to structure components
- How to assign Profiles, Safety Levels, and Modes
- How to separate `@critical` and `@non_critical_phase` logic
- How processes and services interact safely
- How deployment, CBM, and compliance fit together

This blueprint is **non-normative** (informative), but fully aligned with all v3.0.0 policies and design decisions.

---

## 1. Example Scenario – Safety Supervisory System

We model a generic **Safety Supervisory System** used in domains such as:

- Industrial robot safety monitoring
- Autonomous subsystem supervision
- High-risk machinery permissive logic

The Python-based supervisor:

- Reads health and sensor signals
- Applies safety logic
- Issues **“permit / inhibit / degraded”** decisions
- Communicates decisions to a certified actuation system
- Logs and reports system state

Python is **not** directly commanding actuators. It supervises and decides; certified lower-level systems handle actuation.

---

## 2. High-Level Architecture

### 2.1 Logical View

```text
+-----------------------------------------------------------+
|                  Safety Supervisory System                |
+---------------------------+-------------------------------+
|   Input & Health Layer    |      Safety Decision Layer    |
|  (Strict-B / Core)        |       (Strict-A)              |
+---------------------------+-------------------------------+
            |                              |
            v                              v
+---------------------------+    +---------------------------+
|     Logging & Telemetry   |    |    Certified Actuation    |
|         (Core)            |    |  System / Safety PLC etc. |
+---------------------------+    +---------------------------+
```

### 2.2 Process View

```text
+-----------------------+
|  Process: supervisor  |  (CRSS-Python, Strict-A)
+----------+------------+
           |
           | IPC (messages)
           v
+-----------------------+
|  Process: actuator    |  (Non-Python, certified stack)
+-----------------------+
```

- The **supervisor** process runs CRSS-Python–compliant code.
- The **actuator** process is a certified safety PLC/RTOS or equivalent.
- Communication is **bounded, validated, and monitored**.

---

## 3. Component Breakdown

### 3.1 Components Overview

| Component                  | Responsibility                         | Mode        |
|---------------------------|-----------------------------------------|-------------|
| `InputGateway`            | Read raw signals, preprocess            | Strict-B    |
| `ConfigManager`           | Load & validate config                  | Strict-B    |
| `SafetyController`        | Apply safety decision logic             | Strict-A    |
| `DecisionPublisher`       | Send decisions to Actuation System      | Strict-B    |
| `Logger`                  | Local logging only                      | Core-C      |
| `TelemetryClient`         | Optional remote metrics                 | Core-C      |

All Python components run inside the **supervisor** process.

### 3.2 Critical vs Non-Critical

Only **part of `SafetyController`** is `@critical`:

- `SafetyController.initialize()` – `@non_critical_phase`
- `SafetyController.update_inputs()` – `@non_critical_phase` (data pre-processing)
- `SafetyController.decide()` – `@critical` (Strict-A core decision function)

---

## 4. Modes & Phases in the Blueprint

### 4.1 Mode Assignment

Example entries (MAR-style):

```yaml
- unit: "safety_controller.SafetyController.decide"
  profile: "Strict"
  safety_level: "A"
  mode: "Strict-A"
  phase: "critical"

- unit: "safety_controller.SafetyController.initialize"
  profile: "Strict"
  safety_level: "A"
  mode: "Strict-A"
  phase: "non_critical"

- unit: "input_gateway.read_inputs"
  profile: "Strict"
  safety_level: "B"
  mode: "Strict-B"
  phase: "non_critical"

- unit: "decision_publisher.publish"
  profile: "Strict"
  safety_level: "B"
  mode: "Strict-B"
  phase: "non_critical"

- unit: "logger.log_info"
  profile: "Core"
  safety_level: "C"
  mode: "Core-C"
  phase: "non_critical"
```

### 4.2 Phase Interaction Rules

- `SafetyController.decide()` (`@critical`) **may not** call:
  - `InputGateway` functions
  - `ConfigManager` functions
  - `Logger`
  - `TelemetryClient`
- `SafetyController.initialize()` (`@non_critical_phase`) **may** call:
  - `ConfigManager`
  - `Logger`
- The main loop runs:
  - Non-critical input reading
  - Then calls `SafetyController.decide()` as the **only critical segment** in the cycle.

---

## 5. Example Code – Core Critical Flow

### 5.1 Input & Config (Non-Critical)

```python
# input_gateway.py (Strict-B, non-critical)
from crss_annotations import non_critical_phase

@non_critical_phase
def read_inputs() -> dict:
    # Read from hardware, network, shared memory, etc.
    # Some I/O is allowed here; validated before critical.
    return {
        "sensor_1": 0.73,
        "sensor_2": 1.02,
        "health_flag": True,
    }
```

```python
# config_manager.py (Strict-B, non-critical)
from crss_annotations import non_critical_phase

@non_critical_phase
def load_config() -> dict:
    # Load configuration via file I/O, network or db
    raw = {
        "sensor_1_threshold": 0.8,
        "sensor_2_threshold": 1.5,
        "require_health_flag": True,
    }
    # Basic validation here
    return raw
```

### 5.2 Safety Controller (Strict-A)

```python
# safety_controller.py (Strict-A)
from crss_annotations import critical, non_critical_phase

class SafetyController:
    def __init__(self):
        self._cfg = None
        self._threshold_1 = 0.0
        self._threshold_2 = 0.0
        self._require_health = True
        self._initialized = False
        self._last_state = 0  # 0 = PERMIT, 1 = INHIBIT, 2 = DEGRADED

    @non_critical_phase
    def initialize(self, cfg: dict) -> None:
        # Non-critical: parsing, validation, object creation allowed.
        self._cfg = cfg
        self._threshold_1 = float(cfg["sensor_1_threshold"])
        self._threshold_2 = float(cfg["sensor_2_threshold"])
        self._require_health = bool(cfg["require_health_flag"])
        self._initialized = True

    @critical
    def decide(self, sensor_1: float, sensor_2: float, health_flag: bool) -> int:
        # Critical: no I/O, no allocation, no logging, no blocking.
        if not self._initialized:
            # Conservative default: inhibit if not initialized.
            return 1  # INHIBIT

        # Example simple safety logic:
        if self._require_health and not health_flag:
            return 1  # INHIBIT

        if sensor_1 > self._threshold_1 or sensor_2 > self._threshold_2:
            return 1  # INHIBIT

        # Example degraded mode logic:
        if sensor_1 > 0.9 * self._threshold_1 or sensor_2 > 0.9 * self._threshold_2:
            return 2  # DEGRADED

        return 0  # PERMIT
```

### 5.3 Decision Publishing (Non-Critical)

```python
# decision_publisher.py (Strict-B, non-critical)
from crss_annotations import non_critical_phase

@non_critical_phase
def publish_decision(decision: int) -> None:
    # Non-critical: send to actuation system via IPC.
    # Network or IPC I/O allowed, with timeouts.
    # Example pseudo-code:
    #   ipc.send({"decision": decision})
    pass
```

### 5.4 Orchestrator (Non-Critical Main Loop)

```python
# main_supervisor.py (Strict-B orchestrator)
from input_gateway import read_inputs
from config_manager import load_config
from safety_controller import SafetyController
from decision_publisher import publish_decision
import logger  # Core-C

def main():
    ctrl = SafetyController()

    # Non-critical startup phase
    cfg = load_config()
    ctrl.initialize(cfg)
    logger.log_info("SafetyController initialized.")

    # Representative single scan cycle (in real systems this is repeated by scheduler)
    inputs = read_inputs()
    decision = ctrl.decide(
        sensor_1=inputs["sensor_1"],
        sensor_2=inputs["sensor_2"],
        health_flag=inputs["health_flag"],
    )
    publish_decision(decision)
```

This orchestrator is **non-critical**; only `decide()` is `@critical`.

---

## 6. Deployment & CBM View

### 6.1 Deployment Diagram

```text
+-------------------------------------------------------+
|                 Safety Platform Node                  |
+---------------------------+---------------------------+
|  OS: Linux RT Profile     | Python: 3.10.7            |
|  CBM: cbm_v1.0.yaml       | Supervisor Container      |
+---------------------------+---------------------------+
            |
            | IPC (shared memory / socket)
            v
+---------------------------+
|  Actuation System (PLC)   |
+---------------------------+
```

### 6.2 CBM Excerpt

```yaml
cbm_version: "1.0"
project_version: "1.2.3"
python_version: "3.10.7"

os:
  name: "Linux"
  version: "5.15-rt"

containers:
  - name: "supervisor"
    image: "registry.local/supervisor:1.2.3"
    hash: "sha256:...abc"

dependencies:
  - name: "crss-runtime"
    version: "3.0.0"
  - name: "pydantic"
    version: "2.7.0"

tools:
  - name: "crss-analyzer"
    version: "1.1.0"
  - name: "coverage"
    version: "7.3.0"

tests:
  coverage_report: "artifacts/coverage.xml"
  mcdc_report: "artifacts/mcdc.json"

signatures:
  - role: "Release Manager"
    hash: "sha256:..."
```

Prod deployment must match this CBM exactly.

---

## 7. Compliance Story for the Blueprint

### 7.1 Modes and Enforcement

- `SafetyController.decide` → Strict-A, `@critical`
  - Zero violations allowed
  - MC/DC required
  - Determinism proven
- `SafetyController.initialize` → Strict-A, `@non_critical_phase`
  - More operational freedom (allocation, parsing)
  - Must still obey Strict rules
- Other components → Strict-B / Core-C

### 7.2 What Makes This Certifiable?

- Clean separation of concerns
- Minimal critical core
- No dynamic behavior in safety logic
- Immutable deployment with CBM
- One Python version (frozen)
- Clear evidence chain via SCEM

---

## 8. How to Adapt This Blueprint

You can adapt this architecture for:

- Multiple sensors and channels
- Multi-node deployments
- Different domains (medical, automotive, industrial)

Guiding rules:

✅ Keep the critical core small & isolated
✅ Push all I/O and complexity to non-critical layers
✅ Enforce immutable deploys with CBM
✅ Use Modes rigorously in MAR

---

## 9. Summary

This blueprint shows:

- How CRSS-Python can be applied in a realistic system
- How architecture, Modes, Phases, deployment, and evidence work together
- How to design for **maximum safety with realistic constraints**

It is an example — not a limit. You can extend it, but you should always preserve:

✅ Simplicity
✅ Determinism
✅ Isolation
✅ Traceability

Those four pillars are the heart of CRSS-Python.

---
