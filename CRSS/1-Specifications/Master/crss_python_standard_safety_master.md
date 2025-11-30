# CRSS-Python Unified Safety Specification

**Version:** v1.0.0
**Status:** Normative
**Maturity:** Stable
© 2025 Sofian Daghsen – All rights reserved
Distributed under CC BY-NC-ND 4.0 — see LICENSE-CRSS.

---

## Table of Contents

- [CRSS-Python Unified Safety Specification](#crss-python-unified-safety-specification)
  - [0. Purpose](#0-purpose)
  - [1. Core Concepts](#1-core-concepts)
    - [1.1 Profiles](#11-profiles)
    - [1.2 Safety Levels](#12-safety-levels)
    - [1.3 Mode = Profile × Safety Level](#13-mode-profile-×-safety-level)
    - [1.4 Critical and Non-Critical Code](#14-critical-and-non-critical-code)
    - [1.5 Immutability of Mode](#15-immutability-of-mode)
  - [2. Code Units and Boundaries](#2-code-units-and-boundaries)
    - [2.1 Canonical Code Unit](#21-canonical-code-unit)
    - [2.2 Class Promotion](#22-class-promotion)
    - [2.3 Module Context](#23-module-context)
    - [2.4 Architectural Boundaries](#24-architectural-boundaries)
  - [3. Safety Level Assignment and Propagation](#3-safety-level-assignment-and-propagation)
    - [3.1 Assignment from Requirements](#31-assignment-from-requirements)
    - [3.2 Propagation Along Calls (Call-Chain Promotion)](#32-propagation-along-calls-call-chain-promotion)
    - [3.3 Class Promotion](#33-class-promotion)
    - [3.4 No Demotion](#34-no-demotion)
  - [4. Critical vs Non-Critical Execution Model](#4-critical-vs-non-critical-execution-model)
    - [4.1 Definitions](#41-definitions)
    - [4.2 Golden Interaction Rule](#42-golden-interaction-rule)
    - [4.3 Phase Boundaries](#43-phase-boundaries)
    - [4.4 Operational Relaxation vs Rule Relaxation](#44-operational-relaxation-vs-rule-relaxation)
- [CRSS-Python Unified Safety Specification — Remaining Sections](#crss-python-unified-safety-specification-remaining-sections)
  - [5. Rule Categorization](#5-rule-categorization)
    - [5.1 Scope](#51-scope)
    - [5.2 Type and Severity (MUST/SHOULD)](#52-type-and-severity-mustshould)
  - [6. Error and Violation Categorization](#6-error-and-violation-categorization)
    - [6.1 Severity Levels](#61-severity-levels)
    - [6.2 Enforcement by Mode and Phase](#62-enforcement-by-mode-and-phase)
  - [7. Critical-Phase Rules (CP)](#7-critical-phase-rules-cp)
    - [CP-1 — No Allocation in Critical](#cp-1-no-allocation-in-critical)
    - [CP-2 — No Blocking or External I/O](#cp-2-no-blocking-or-external-io)
    - [CP-3 — No GC Interference](#cp-3-no-gc-interference)
    - [CP-4 — Deterministic Control Flow](#cp-4-deterministic-control-flow)
  - [8. Non-Critical-Phase Rules (NCP)](#8-non-critical-phase-rules-ncp)
    - [NCP-1 — Allowed Operations](#ncp-1-allowed-operations)
    - [NCP-2 — Still Under Profile Rules](#ncp-2-still-under-profile-rules)
    - [NCP-3 — Prepare and Freeze](#ncp-3-prepare-and-freeze)
  - [9. Import Policy](#9-import-policy)
    - [9.1 Core vs Strict](#91-core-vs-strict)
    - [9.2 Mode-Specific Restrictions](#92-mode-specific-restrictions)
    - [9.3 Utility Exemption](#93-utility-exemption)
  - [10. Inheritance Policy](#10-inheritance-policy)
    - [10.1 Depth Constraint](#101-depth-constraint)
    - [10.2 Mode Constraints](#102-mode-constraints)
    - [10.3 Promotion via Inheritance](#103-promotion-via-inheritance)
  - [11. Exceptions and Utilities](#11-exceptions-and-utilities)
    - [11.1 Logging](#111-logging)
    - [11.2 Telemetry / Metrics](#112-telemetry-metrics)
    - [11.3 Diagnostics and Debug](#113-diagnostics-and-debug)
  - [12. Compliance and Acceptance Model](#12-compliance-and-acceptance-model)
    - [12.1 Core-Only Projects](#121-core-only-projects)
    - [12.2 Strict-Only Projects (No Level A)](#122-strict-only-projects-no-level-a)
    - [12.3 Strict-A Components](#123-strict-a-components)
    - [12.4 Mixed Systems (Core + Strict + Strict-A)](#124-mixed-systems-core-strict-strict-a)
  - [13. Certification-Grade Conditions (High-Level)](#13-certification-grade-conditions-high-level)
  - [14. Reference Use Case (Mode + Phases + Dependencies)](#14-reference-use-case-mode-phases-dependencies)
    - [14.1 Scenario](#141-scenario)
    - [14.2 Architecture](#142-architecture)
    - [14.3 Modes](#143-modes)
    - [14.4 Python Example](#144-python-example)
- [logger.py (Core-C)](#loggerpy-core-c)
- [config_loader.py (Strict-B, non-critical)](#configloaderpy-strict-b-non-critical)
- [sensor.py (Strict-B, non-critical)](#sensorpy-strict-b-non-critical)
- [safety_controller.py (Strict-A)](#safetycontrollerpy-strict-a)
- [main.py (Strict-B or Strict-A non-critical orchestrator)](#mainpy-strict-b-or-strict-a-non-critical-orchestrator)
    - [14.5 Compliance Interpretation](#145-compliance-interpretation)
  - [15. Machine-Readable Metadata (Optional Annex)](#15-machine-readable-metadata-optional-annex)
  - [16. Summary](#16-summary)

---

## 0. Purpose

The **CRSS-Python Unified Safety Specification v3.0.0** is the **single, authoritative** standard for:

- Profiles (**Core**, **Strict**)
- Safety Levels (**A**, **B**, **C**)
- Modes (Profile × Safety Level)
- Critical vs Non-Critical execution
- Error & violation categorization
- Safety Level propagation
- Import & inheritance constraints
- Runtime and architectural constraints
- Exceptions (logging, telemetry, diagnostics)
- Compliance & acceptance criteria (Core-only, Strict-only, mixed)
- A realistic, minimal reference use case

This document **consolidates and supersedes**:

- CRSS-Python Standard Levels v1.0.0 / v2.0.0
- CRSS Profile/Safety/Critical Interaction v1.0.0
- CRSS Non-Critical Phase Model
- CRSS Critical Annotation Policy
- CRSS Import Policy
- CRSS Inheritance Policy
- CRSS Python Mode and Safety Model

It is designed to:

- Achieve the **strongest feasible safety guarantees** with Python
- Remain **realistic and implementable** in real projects
- Support **ASIL D / SIL 3 supervisory roles** under appropriate architectures

---

## 1. Core Concepts

### 1.1 Profiles

A **Profile** defines which rule catalog applies to a codebase or component.

| Profile | Scope | Enforcement Basis |
|--------|-------|-------------------|
| **Core** | General safety-oriented Python subset | MUST / SHOULD (WARN) |
| **Strict** | High-integrity, safety-focused subset | MUST / SHOULD (ERROR) |

**Profile is a property of rules**, not of Safety Levels.

- A rule will specify:
  `Core: MUST/SHOULD/MUST-NOT/SHOULD-NOT/N/A`
  `Strict: MUST/SHOULD/MUST-NOT/SHOULD-NOT/N/A`
- A code unit (module/class/function) is analyzed under either **Core** or **Strict**.

### 1.2 Safety Levels

**Safety Level** is a system-level classification for requirements and code units:

| Level | Meaning            | Typical Mapping                                |
|-------|--------------------|-----------------------------------------------|
| **A** | Highest criticality | ASIL D, SIL 3 (supervisory), Class C (multi-layer) |
| **B** | Medium–high        | ASIL C, SIL 2–3                              |
| **C** | Low–medium         | ASIL A/B, SIL 1–2                            |

Safety Levels apply to **functions/methods**, then propagate to classes and modules.

### 1.3 Mode = Profile × Safety Level

A **Mode** is the enforcement identity of a code unit:

```
Mode = (Profile, Safety Level)
      = (Core|Strict, A|B|C)
```

Examples:

- Core-C, Core-B
- Strict-C, Strict-B
- Strict-A (highest)

#### Strict-A (Strict Level A) Mode

Strict-A is defined as:

- **Profile:** Strict
- **Safety Level:** A

**Enforcement:**

- Zero-tolerance for violations in critical code
- SCEM/EAP evidence
- Critical-phase runtime constraints

Not a third profile, but a Mode with additional obligations.

### 1.4 Critical and Non-Critical Code

A code unit can be annotated as:

- `@critical` — safety-critical, timing-critical, deterministic segment.
- `@non_critical_phase` — preparatory, shutdown, or reconfiguration segment.

These annotations are Phase labels within a Mode.

### 1.5 Immutability of Mode

Once a Mode is established for a baseline:

- It cannot be downgraded (e.g. Strict-A → Strict-B).
- It can be promoted (e.g. Strict-B → Strict-A) if safety analysis changes.

Any change in Mode requires:

- Impact analysis
- Re-testing
- Re-baselining
- Re-certification

---

## 2. Code Units and Boundaries

### 2.1 Canonical Code Unit

The canonical unit for Mode assignment is the function/method.

```
Mode(Function) = (Profile, Level)
```

A function may have internal phases (@critical regions) but one Mode.

### 2.2 Class Promotion

If any method of a class is Level A:

- The entire class is promoted to Mode Strict-A.
- All methods in that class:
  - Are analyzed under Strict profile.
  - Inherit Strict-A Mode for enforcement.
  - Respect critical vs non-critical rules as per their annotations.

### 2.3 Module Context

Modules are not primary Mode units, but:

- If a module contains one or more Strict-A classes:
  - The module is treated as a Strict-A context for tools and review.

Mixed-level classes in a module are allowed but discouraged.

A project MAY adopt a stricter rule:
“Any module with Strict-A must only contain Strict-A classes + trivial utilities (logging, tracing).”

### 2.4 Architectural Boundaries

Promotion and safety responsibilities DO NOT cross:

- OS process boundaries
- Service boundaries
- Hardware integration boundaries

Unless there is explicit safety-relevant data coupling.

---

## 3. Safety Level Assignment and Propagation

### 3.1 Assignment from Requirements

Each function/method is linked to one or more requirements via the RTM:

- Each requirement has a Safety Level (A/B/C).
- Function’s Safety Level = maximum of its linked requirement levels.

If no safety requirements are mapped:

- Default level = C or “unclassified”, depending on project policy.

### 3.2 Propagation Along Calls (Call-Chain Promotion)

If a function F (Mode X) calls G, and:

The output of G influences:

- Safety decisions
- Actuator outputs
- Safety-relevant data

Then:

```
Level(G) := max(Level(G), Level(F))
Profile(G) := max(Profile(G), Profile(F))   # Where Strict > Core
```

For Strict-A callers:

- Any callee in the critical path must effectively be Strict-A as well.

### 3.3 Class Promotion

If any method in class C:

- Has Level A OR
- Becomes Level A by propagation OR
- Is @critical and part of a Level A path

Then:

**Class C Mode = Strict-A**

All methods in C are analyzed and enforced as Strict-A.

### 3.4 No Demotion

If a unit is once classified as **Strict-A** it cannot be later interpreted as:

- Strict-B / Strict-C / Core-X

without re-certification.

---

## 4. Critical vs Non-Critical Execution Model

### 4.1 Definitions

**Critical Code (`@critical`)**
A function or region where:

- Safety decisions are made
- Outputs can affect safety
- Strict timing and determinism are required

**Non-Critical Code (`@non_critical_phase`)**
Code in the same component, but executed:

- Before critical windows (startup/preparation)
- After critical windows (shutdown)
- During safe reconfiguration windows

Non-critical does **not** mean “non-regulated”; it means “not subject to the additional critical-phase constraints”.

### 4.2 Golden Interaction Rule

🚫 **Critical code may never call non-critical code.**

Once execution has entered a `@critical` function/region:

It may only:

- Execute local logic
- Call other functions also configured as `@critical` (or fully compatible with CP rules)

It MUST NOT:

- Invoke `@non_critical_phase` functions
- Invoke I/O or allocation operations
- Use low-level dependencies not proven safe for critical use

### 4.3 Phase Boundaries

Critical begins:

- At the first executed instruction of a `@critical` function, or
- When a defined critical region/context manager begins.

Critical ends:

- At the return or raised exception from a `@critical` function/region.

### 4.4 Operational Relaxation vs Rule Relaxation

**Operational relaxation:**
Non-critical code may perform operations that are forbidden in critical code:

- Allocation
- I/O
- Networking
- Subprocess
- Blocking operations (within limits)

**Rule relaxation:**
❌ Does **not** occur. Global profile rules still apply everywhere.

In other words:

✅ Non-critical code has more operational freedom
❌ But no lower enforcement for MUST/MUST-NOT rules.

---

# CRSS-Python Unified Safety Specification — Remaining Sections

## 5. Rule Categorization

Rules are categorized along two orthogonal axes:

- **Scope:** Global vs Phase-scoped
- **Type:** MUST, MUST-NOT, SHOULD, SHOULD-NOT

### 5.1 Scope

#### 5.1.1 Global Rules

Apply everywhere (critical and non-critical):

- No `eval` / `exec`
- No monkeypatching
- No dynamic imports
- No modification of global state from multiple threads unsafely
- No unsafe subprocess or shell execution
- No recursion beyond bounded limits

#### 5.1.2 Phase-Scoped Rules (Critical-Only)

Apply only within `@critical`:

- No heap allocation (beyond trivial, bounded temporaries)
- No file I/O, network, DB, IPC
- No subprocess
- No acquiring locks that may block
- No dynamic imports
- No heavy logging or formatting
- GC must not run or cause pauses

### 5.2 Type and Severity (MUST/SHOULD)

- **MUST / MUST-NOT:** Hard requirements
- **SHOULD / SHOULD-NOT:** Strong recommendations

---

## 6. Error and Violation Categorization

### 6.1 Severity Levels

We define the following analyzer-level severities:

- **INFO** – informational, non-actionable
- **WARN** – recommendation violated (SHOULD/SHOULD-NOT)
- **ERROR** – MUST/MUST-NOT violation under Core/Strict
- **BLOCKER** – MUST/MUST-NOT violation under Strict-A in critical context

### 6.2 Enforcement by Mode and Phase

| Mode / Phase             | MUST/MUST-NOT Violation        | SHOULD/SHOULD-NOT Violation                       |
|--------------------------|---------------------------------|---------------------------------------------------|
| Core (any phase)         | ERROR                           | WARN (no fixed threshold, but monitored)          |
| Strict (any phase)       | ERROR                           | WARN (cumulative ≤ 10% allowed, with justification) |
| Strict-A — Critical      | BLOCKER                         | BLOCKER (treated as MUST)                         |
| Strict-A — Non-Critical  | BLOCKER (with deviation process) | WARN/ERROR per Strict rules                      |

**Interpretation for Strict-A non-critical:**

MUST violation:

- Default = **BLOCKER**
- May be accepted only if:
  - Recorded as deviation
  - Risk-assessed
  - Proven isolated from critical
  - Approved by independent authority

---

## 7. Critical-Phase Rules (CP)

### CP-1 — No Allocation in Critical

Within `@critical`:

- No creation of new heap objects
  (beyond trivial, bounded local temporaries that tools can approve)

### CP-2 — No Blocking or External I/O

Within `@critical`:

- No I/O (file, network, DB, IPC)
- No subprocess or shell
- No acquiring possibly-blocking locks
- No waiting on conditions, futures, or external events

### CP-3 — No GC Interference

For Strict-A:

- GC MUST be disabled or guaranteed not to run during `@critical`.

Evidence must show:

- No GC pause can occur during critical windows.

### CP-4 — Deterministic Control Flow

Within `@critical`:

- No unbounded loops
- No data-dependent unbounded recursion
- No calls to functions whose complexity is unknown

---

## 8. Non-Critical-Phase Rules (NCP)

### NCP-1 — Allowed Operations

In `@non_critical_phase` (Strict & Strict-A):

✅ Allowed:

- Object creation & memory allocation
- Configuration loading (e.g., JSON, YAML)
- Network I/O (e.g., retrieving config or calibrations)
- DB access
- Subprocess usage (within profile rules)
- Logging and monitoring

### NCP-2 — Still Under Profile Rules

Global profile rules continue to apply:

- No `eval` / `exec`
- No dynamic import hacks
- No unsafe subprocess shell calls
- No monkeypatching

MUST violations still produce **ERROR/BLOCKER** as per Mode.

### NCP-3 — Prepare and Freeze

Any data used in `@critical` must:

- Be fully prepared in non-critical code
- Be validated (range checks, structure checks)
- Be frozen or treated as immutable for critical use
- Not be modified during critical execution

---

## 9. Import Policy

### 9.1 Core vs Strict

| Importer Profile | Imported Profile | Allowed?                  |
|------------------|------------------|---------------------------|
| Core             | Core             | ✅                         |
| Core             | Strict           | ❌                         |
| Strict           | Core             | ✅ (subject to Mode)      |
| Strict           | Strict           | ✅                         |

### 9.2 Mode-Specific Restrictions

For Strict-A critical code:

May only call functions that are:

- Mode = **Strict-A**
- And satisfy CP rules

For Strict-A non-critical:

May import and call:

- Core or Strict code, provided:
  - Outputs are validated and frozen before entering any critical phase
  - They do not break profile rules

### 9.3 Utility Exemption

Strict-A non-critical code may call Core utilities (logging, metrics, simple math) if:

They have **NO**:

- Side effects affecting safety decisions
- Timing impact on critical scheduling

Failure of the utility results at most in loss of observability, not unsafe behavior.

---

## 10. Inheritance Policy

### 10.1 Depth Constraint

- Maximum inheritance depth in Strict code: **1** (base + one subclass)
- Multiple inheritance in Strict code: **forbidden** unless explicitly justified

### 10.2 Mode Constraints

Strict-A class **MUST NOT** inherit from:

- Core classes
- Lower-level Strict classes (Strict-B/C)

Strict-A may:

- Inherit from a sealed Strict-A base class
- Use composition for lower-level behavior instead of inheritance

### 10.3 Promotion via Inheritance

If a Strict-B/C subclass participates in a Strict-A call chain:

- Its base class may be **promoted to Strict-A** (if polymorphic behavior is used critically).
- Tools must trace virtual dispatch.

---

## 11. Exceptions and Utilities

### 11.1 Logging

Allowed in non-critical code if:

- Non-blocking or bounded blocking
- No dynamic imports
- No remote logging over unreliable network (unless explicitly allowed and non-critical)
- Exceptions thrown by logger are caught and ignored (best-effort)

**Forbidden in `@critical`.**

### 11.2 Telemetry / Metrics

Allowed:

- Outside critical code
- Asynchronous in nature

They must not:

- Affect control decisions
- Affect timing guarantees of critical code

### 11.3 Diagnostics and Debug

Enabled only:

- In development/testing, or
- In non-critical maintenance windows

Strictly forbidden in `@critical`.

---

## 12. Compliance and Acceptance Model

### 12.1 Core-Only Projects

Evaluated under **Core** profile.

- MUST violations = **ERROR**.
- SHOULD violations = **WARN** (monitored, but threshold is project-chosen).

Cannot claim Strict or Strict-A integrity.

### 12.2 Strict-Only Projects (No Level A)

Evaluated under **Strict** profile.

- MUST violations = **ERROR**.

SHOULD violations:

- Allowed up to 10% of total applicable rules,
- Each with:
  - Justification
  - Risk assessment

Cannot claim Strict-A (Level A) integrity.

### 12.3 Strict-A Components

Components with Mode **Strict-A** must:

- Have **zero MUST and zero SHOULD violations** in `@critical` code.

For `@non_critical_phase`:

- MUST/MUST-NOT violations are still **BLOCKER** by default,
- Can be treated as acceptable only via approved deviation:
  - Deviations documented
  - Risk analysis attached
  - Isolation from critical proven
  - Approved by independent safety function.

### 12.4 Mixed Systems (Core + Strict + Strict-A)

System passes only if:

- All Strict-A critical paths satisfy:
  - No violations,
  - No calls to non-critical,
  - No unsafe imports/inheritance.
- All deviations in non-critical Strict-A code are:
  - Documented and approved.
- Strict components meet their ERROR/WARN caps.
- Core components:
  - Do not compromise Strict-A behavior (e.g., only used for non-safety concerns or behind safe adapters).

---

## 13. Certification-Grade Conditions (High-Level)

When implemented correctly, this specification supports:

Use of Python in **ASIL D / SIL 3** supervisory roles, under conditions:

- Final actuation and hard real-time loops handled by a certified lower-level stack.
- Python only supervises, monitors, and decides within bounded timing and architecture.

Python is **not** used:

- As a SIL 4 kernel,
- As primary actuation in DO-178C DAL A.

(The detailed domain mapping can be covered in a separate *“Standard Levels & Applicability”* document.)

---

## 14. Reference Use Case (Mode + Phases + Dependencies)

### 14.1 Scenario

A safety-supervisory component:

- Reads sensor data (from a lower-level driver)
- Uses pre-loaded configuration and thresholds
- Executes a deterministic `@critical` control loop
- Produces a safety decision (e.g. "allow / inhibit")
- Logs only outside of critical execution

### 14.2 Architecture

```text
+-------------------------+
|   Sensor Interface      |  (Strict-B, non-critical)
+-----------+-------------+
            |
            v
+-------------------------+
|   SafetyController      |  (Strict-A)
|  - @non_critical_phase  |
|  - @critical            |
+-----------+-------------+
            |
            +--> Actuation Supervisor (outside Python scope)
            |
            +--> Logger (Core-C, utilities)
            |
            +--> ConfigLoader (Strict-B)
```

### 14.3 Modes

- `ConfigLoader.load` → Mode: Strict-B, non-critical
- `Sensor.read_raw` → Mode: Strict-B, non-critical
- `SafetyController.initialize` → Mode: Strict-A, `@non_critical_phase`
- `SafetyController.control_loop` → Mode: Strict-A, `@critical`
- `Logger.log` → Mode: Core-C, non-critical utility

### 14.4 Python Example

```python
# logger.py (Core-C)
def log_info(msg: str) -> None:
    try:
        print(msg)  # non-blocking console logging
    except Exception:
        # Best-effort; logging failures must not affect behavior
        pass
```

```python
# config_loader.py (Strict-B, non-critical)
from crss_annotations import non_critical_phase

class Config:
    def __init__(self, threshold: float):
        self.threshold = threshold

@non_critical_phase
def load_config() -> Config:
    # File or network I/O allowed here (non-critical)
    raw_value = 0.75  # imagine loaded from JSON/DB
    return Config(threshold=float(raw_value))
```

```python
# sensor.py (Strict-B, non-critical)
from crss_annotations import non_critical_phase

@non_critical_phase
def read_sensor_raw() -> float:
    # Interacts with hardware or driver (non-critical side)
    # May perform I/O, blocking calls allowed within budget
    return 0.42
```

```python
# safety_controller.py (Strict-A)
from crss_annotations import critical, non_critical_phase

class SafetyController:
    def __init__(self, config_loader, logger):
        self._config_loader = config_loader
        self._logger = logger
        self._threshold = 0.0
        self._initialized = False

    @non_critical_phase
    def initialize(self) -> None:
        '''
        Non-critical phase:
        - May allocate
        - May perform I/O
        - Must prepare all data needed for critical loop
        '''
        cfg = self._config_loader.load_config()
        self._threshold = float(cfg.threshold)
        self._initialized = True
        self._logger.log_info(f"SafetyController initialized with thr={self._threshold!r}")

    @critical
    def control_loop(self, sensor_value: float) -> int:
        '''
        Critical phase:
        - No allocation
        - No I/O
        - No logging
        - Deterministic branching
        '''
        if not self._initialized:
            # Defensive: treat uninitialized as safe fallback (e.g., inhibit)
            return 0

        # Pure computation on primitive fields
        if sensor_value > self._threshold:
            return 1  # e.g., "trip" or "inhibit"
        return 0
```

```python
# main.py (Strict-B or Strict-A non-critical orchestrator)
from sensor import read_sensor_raw
from config_loader import load_config
from safety_controller import SafetyController
import logger

def main() -> None:
    ctrl = SafetyController(config_loader=__import__("config_loader"),
                            logger=logger)

    # Non-critical start-up
    ctrl.initialize()

    # Example external loop:
    # In actual system, this would be orchestrated by real-time scheduler
    while True:
        raw = read_sensor_raw()  # non-critical I/O
        # At this point, we are outside @critical.
        # The call below enters critical region.
        decision = ctrl.control_loop(raw)
        # Decision is passed to a certified actuation layer (not shown here)

        # Sleep / wait / throttle loop in non-critical context (omitted)
        break
```

### 14.5 Compliance Interpretation

**SafetyController.control_loop:**

Must have:

- No allocation
- No I/O
- No violations of Strict rules

Mode = **Strict-A**, Phase = `@critical`

**SafetyController.initialize:**

- Mode = **Strict-A**, Phase = `@non_critical_phase`
- May allocate & perform I/O
- Any MUST violation → **BLOCKER** unless deviation with isolation is fully justified.

**read_sensor_raw** and **load_config**:

- Non-critical Strict-B
- Called only before critical loop

**Logger:**

- Core-C
- Used only in non-critical phases

---

## 15. Machine-Readable Metadata (Optional Annex)

Tools may represent each code unit as:

```yaml
- unit: "safety_controller.SafetyController.control_loop"
  profile: "Strict"
  safety_level: "A"
  mode: "Strict-A"
  phase: "critical"
  calls:
    - "builtins.float"  # safe
  allows_allocation: false
  allows_io: false
  must_violations: 0
  should_violations: 0

- unit: "safety_controller.SafetyController.initialize"
  profile: "Strict"
  safety_level: "A"
  mode: "Strict-A"
  phase: "non_critical"
  calls:
    - "config_loader.load_config"
    - "logger.log_info"
  allows_allocation: true
  allows_io: true
  must_violations: 0    # or >0 with approved deviations
  should_violations: 0
```

This schema enables:

- Automated Mode calculation
- Enforcement checks
- Report generation for SCEM/EAP artifacts

---

## 16. Summary

This Unified Safety Specification v3.0.0:

- Centralizes all semantics for Profiles, Levels, Modes, and Phases
- Clearly distinguishes:
  - Global vs phase-scoped rules
  - Strict vs Strict-A enforcement
  - Operational vs rule relaxation
- Defines:
  - How violations are categorized and handled
  - How Modes propagate and never demote
  - How imports and inheritance are constrained
  - How non-critical phases are allowed, but never allowed to pollute critical execution
- Provides:
  - A realistic, minimal, fully compliant example
  - A basis for tool implementation and certification arguments

It is intended to be the single master reference for **CRSS-Python** safety behavior and enforcement, while allowing software to still do its job under strong, explicit, and auditable constraints.
