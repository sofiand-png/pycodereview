# CRSS-Python Standard Safety Master

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
	- [1.6 Granularity of Safety Levels and Modes] (#16-granularity-of-safety-levels-and-modes)
	- [1.7 Profile Granularity Model] (#17-profile-granularity-model)
	- [2. Environment and Boundaries ](#2-environment-and-boundaries-rewritten--expanded)
	  - [2.1 Definition of Boundaries](#21-definition-of-boundaries)
		- [2.1.1 OS Process Boundary](#211-os-process-boundary)
		- [2.1.2 Service / Network Boundary](#212-service--network-boundary)
		- [2.1.3 Hardware Integration Boundary](#213-hardware-integration-boundary)
	  - [2.2 No Promotion Across Boundaries](#22-no-promotion-across-boundaries)
	  - [2.3 No Safety Leakage Beyond Boundaries](#23-no-safety-leakage-beyond-boundaries)
	  - [2.4 Boundary Interaction Contracts](#24-boundary-interaction-contracts)
		- [2.4.1 OS Process Boundary Contract](#241-os-process-boundary-contract)
		- [2.4.2 Service / Network Boundary Contract](#242-service--network-boundary-contract)
		- [2.4.3 Hardware Integration Boundary Contract](#243-hardware-integration-boundary-contract)
	  - [2.5 Call Graph Interaction with Boundaries](#25-call-graph-interaction-with-boundaries)
	  - [2.6 Boundary Failures Must Not Break Level-A Logic](#26-boundary-failures-must-not-break-level-a-logic)
	  - [2.7 Summary of Boundary Rules](#27-summary-of-boundary-rules)
	  - [2.8 Final Statement](#28-final-statement)
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
    - [6.2 Enforcement Matrix](#62-enforcement-matrix)
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
  - [15. Third-Party Library and Framework Containment](#15-third-party-library-and-framework-containment)	
  - [16 Call Graph, Orchestrators, and Level-A Data Validation )](#16-call-graph-Orchestrators-and-level-A-data-validation)
  - [17. Machine-Readable Metadata (Optional Annex)](#17-machine-readable-metadata-optional-annex)
  - [18. Summary](#18-summary)
  

---

## 0. Purpose and Conflict Resolution

The **CRSS-Python Unified Safety Specification** is the **single, authoritative** standard for:

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


In case of any ambiguity, conflict, inconsistency, or contradiction between
this document and any other CRSS-related document (including models, rules,
interpretation guides, profiles, examples, or tooling documentation),
**this Master specification SHALL take precedence**.

Other CRSS documents may provide:
- interpretation,
- rationale,
- explanatory models,
- examples,
- or implementation guidance,

but MUST NOT override, weaken, or contradict the requirements defined herein.


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

- **Strict profile**  
  - Most restrictive rules  
  - No dynamic features on critical path  
  - Bounded loops and memory  
  - GC and non-deterministic behavior excluded from critical execution  
  - Intended for **safety-critical core logic**

- **Core profile**  
  - Still disciplined and deterministic where needed  
  - Allows more Python features (e.g., more dynamic constructs)  
  - Intended for **supporting or lower-safety elements**

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

- It cannot be downgraded (e.g. Strict-A -> Strict-B).
- It can be promoted (e.g. Strict-B -> Strict-A) if safety analysis changes.

Any change in Mode requires:

- Impact analysis
- Re-testing
- Re-baselining
- Re-certification

## 1.6 Granularity of Safety Levels, Profiles, and Modes

CRSS distinguishes between:

- **Profiles**: Core / Strict  
- **Safety Levels**: A / B / C  
- **Modes**: combinations such as Strict-A, Strict-B, Core-C

This section defines:

- where Modes are applied,  
- how Safety Levels and Profiles interact,  
- how promotion and “no demotion” work.

---

### 1.6.1 Enforcement Granularity — One Mode per Module

**CRSS-Gran-1 (Normative)**  
A **module** (`.py` file) is the enforcement unit.

Each module SHALL declare exactly:

- one Profile (`core` or `strict`),  
- one Safety Level (`A`, `B`, or `C`),

→ forming one Mode such as `Strict-A`, `Core-C`, etc.

There is **no Core-A** (Level A always implies Strict).

Example:

```python
# CRSS_PROFILE: strict
# CRSS_SAFETY_LEVEL: A
# CRSS_MODE: Strict-A
```

---

### 1.6.2 Promotion by Highest Safety Level

**CRSS-Gran-2 (Normative)**  

If any function or class inside a module is Level A → the module becomes Level A.  
If any is Level B (and none A) → module becomes Level B.

```
module_level = max(safety_levels of functions/classes)
```

Thus no module can declare “Level B” while containing Level-A code.

Refactor Level-A responsibilities into their own module if needed.

**CRSS-Gran-3 (Normative)**  
If a class or module is used by multiple call sites with different Safety Levels, it SHALL be assigned the **highest** Safety Level among its callers and a compatible Mode.  
If this is not acceptable, the functionality MUST be refactored into separate modules/classes.

---

#### 1.6.3 Class-Level Mixing of Safety Levels

**CRSS-Gran-4 (Normative)**  
A single class SHALL NOT mix methods that are treated as different safety levels in a way that affects shared state or safety-relevant behavior.  
If part of a class must behave as Safety Level A and another part as Level B/C, these responsibilities SHALL be split into separate classes and, if needed, separate modules.

In practice:

- A class involved in Level A logic is treated as **Level A / Strict-A** as a whole.  
- Support code for Level B/C behavior SHOULD live in separate classes/modules assigned to lower Modes.


### 1.6.3 Allowed Module Modes

**CRSS-Gran-5 (Normative)**

| Mode      | Profile | Level | Common Use |
|-----------|---------|-------|------------|
| Strict-A  | Strict  | A     | Critical kernel, validators |
| Strict-B  | Strict  | B     | Safety-related logic |
| Strict-C  | Strict  | C     | Disciplined low-level logic |
| Core-B    | Core    | B     | Support logic |
| Core-C    | Core    | C     | Gateways, logging, UI |

There is no Core-A.

---

### 1.6.4 Propagation of Safety Levels

**CRSS-Gran-6 (Normative)**  

If caller at Level L₁ calls a function whose result affects safety decisions:

```
SafetyLevel(callee) := max(SafetyLevel(callee), SafetyLevel(caller))
```

For Level A:  
Anything used by Level-A safety logic must itself be Level A.

---

### 1.6.5 Documentation vs Enforcement

Documentation may record function-level Safety Levels, but:

**CRSS-Gran-7 (Normative)**  
Module-level enforcement always wins.  
If metadata and module declaration disagree → stricter interpretation applies or code must be refactored.

---

## 1.7 Profile Granularity Model (Core vs Strict)

Profiles describe rule strictness; Safety Levels describe hazard severity.

---

### 1.7.1 Where Profiles Apply

Profiles may be conceptually attached at package, module, class, or function level, but:

**CRSS-Profile-1 (Normative)**  

- Modules declare one Profile (Core or Strict).  
- Profile mixing inside a module is forbidden.  
- Function/class metadata cannot weaken the module’s Profile.

---

### 1.7.2 Safety Level vs Profile

**CRSS-Profile-2 (Normative)**

| Safety Level | Allowed Profiles | Notes |
|--------------|------------------|-------|
| A            | Strict only      | Mode Strict-A |
| B            | Core or Strict   | Strict preferred |
| C            | Core or Strict   | Core default |

---

### 1.7.3 Core vs Strict Imports

**CRSS-Profile-3 (Normative)**  

- Core modules MAY import Core or Strict.  
- Strict modules MUST NOT import Core (baseline).  
- Strict→Core allowed only for tests/tools, not deployed code.

---

#### 1.7.5 How Profiles and Safety Levels Interact

Profiles = enforcement intensity  
Safety Levels = hazard severity

They combine as:

| Safety Level | Allowed Profiles | Notes |
|--------------|------------------|-------|
| **Level A**  | Strict only       | No Core logic in Level-A data path |
| **Level B**  | Core or Strict    | Strict preferred for boundaries or safety checks |
| **Level C**  | Core or Strict    | Minimal restrictions |

**CRSS-Profile-3 (Normative)**  
A function at Safety Level A **MUST** be Strict profile.  
A function at Safety Level B or C **MAY** be Core.


---

## 2. Environment and Boundaries

Safety Levels and Profile responsibilities exist inside a well-defined software safety domain.
Not all components of a deployed system share that domain, and not all boundaries permit safety-level propagation.

This section defines:

- what counts as an environment boundary,
- whether Safety Levels can cross that boundary,
- how CRSS components must interact with external or lower-assurance elements,
- how to avoid accidental safety responsibility leakage,
- how call-graph promotion interacts with boundaries.

---

## 2.1 Definition of Boundaries

A boundary is any architectural separation across which CRSS cannot enforce Python-level guarantees.

Hard boundaries include:

### 2.1.1 OS Process Boundary

Examples:

- subprocesses
- independent microservices
- external hardware drivers
- sandboxed runtimes

Crossing the process boundary means:

- no shared memory safety,
- no call-graph continuity,
- no Profile enforcement,
- no CRSS guarantees.

---

### 2.1.2 Service / Network Boundary

Examples:

- REST endpoints
- TCP/UDP sensors
- message queues
- cloud services

Network boundaries introduce nondeterminism, latency, loss, malicious inputs, and break call-graph semantics.

---

### 2.1.3 Hardware Integration Boundary

Examples:

- microcontrollers
- FPGAs
- PLCs
- motor drivers
- sensor ASICs

Hardware/firmware is outside the CRSS domain and cannot be treated as Level-A/B.

---

## 2.2 No Promotion Across Boundaries

**CRSS-Boundary-1 (Normative)**  
Safety Level promotion does **not** cross boundaries.

If a Level-A function receives data from:

- other processes,
- network services,
- devices,
- or any environment,

the external source is **not** promoted to Level-A.

Python code must:

1. treat external data as untrusted  
2. validate through Strict-B  
3. enforce domain invariants through Strict-A  

---

## 2.3 No Safety Leakage Beyond Boundaries

**CRSS-Boundary-2 (Normative)**  
Strict-A/B components MUST assume:

- all external inputs may be malformed or adversarial.

- External → Core-C Gateway → Strict-B Validation → Strict-A Validation

- Only after this chain does data become eligible for Level-A use.

---

## 2.4 Boundary Interaction Contracts

### 2.4.1 OS Process Boundary Contract

**Allowed:**

- gateway processes providing data
- non-critical subprocesses
- isolated pipelines
- IPC treated as untrusted

**Required:**

- treat IPC input as Core-C raw data
- Strict-B structural validation
- Strict-A domain validation
- subprocess failure must not break deterministic Level-A logic

**Forbidden:**

- placing Level-A logic in external processes
- making external processes part of Level-A path
- depending on external timing inside @critical

---

### 2.4.2 Service / Network Boundary Contract

**Allowed:**

- TCP/UDP sensor data
- REST sources
- cloud diagnostics
- telemetry

**Required:**

- network I/O only in Core-C
- Strict-B and Strict-A validation before Level-A use
- timeouts, malformed-frame handling

**Forbidden:**

- trusting remote ordering or uptime
- using network data directly in Level-A
- letting remote services participate in safety decisions

---

### 2.4.3 Hardware Integration Boundary Contract

**Allowed:**

- raw sensor data from drivers
- MCU/FPGA/PLC outputs

**Required:**

- Strict-B structural validation (range, saturation)
- Strict-A physical plausibility
- SAFE_DEFAULT fallback on device failure

**Forbidden:**

- any hardware access inside Strict-A critical sections
- assuming deterministic hardware timing
- treating firmware as Level-A

---

## 2.5 Call Graph Interaction with Boundaries

Boundaries **break** call-graph promotion.

### Example 1 — Correct

```
MCU → TCP → Core-C Gateway
      → Strict-B Validator
          → Strict-A Validator
              → Strict-A Critical Kernel
```

Promotion applies **after** validators.

---

### Example 2 — Incorrect

```
Strict-A Critical Kernel → driver SPI read
```

Violations:

- Strict → Core
- nondeterministic behavior
- I/O in @critical
- hardware cannot be promoted

---

### Example 3 — Incorrect

```
Strict-A @critical → REST API → cloud
```

Violations:

- I/O in @critical
- Strict→Core
- nondeterministic external service
- cannot promote remote service

---

### Example 4 — Allowed (Constrained)

```
Core Orchestrator → Strict-B Validator → Strict-A Validator → Strict-A @critical
```

Valid because:

- Core handles I/O  
- Strict-B validates  
- Strict-A enforces invariants  
- Strict-A @critical uses only internal immutable data  

---

## 2.6 Boundary Failures Must Not Break Level-A Logic

**CRSS-Boundary-3 (Normative)**  
External failure — timeout, corruption, crash, stall — MUST NOT break:

- Level-A determinism  
- Level-A safe outputs  
- Level-A timing guarantees  

Required responses:

- SAFE_DEFAULT fallback  
- inhibited/degenerate behaviors  
- fixed-rate continuation  
- bounded internal recovery  

---

## 2.7 Summary of Boundary Rules

| Boundary | Promotion Allowed? | Strict-A Assumption | Required Path | Forbidden |
|----------|---------------------|----------------------|----------------|-----------|
| OS process | No | external untrusted | Gateway → Strict-B → Strict-A | critical dependence |
| Service/network | No | data may be corrupt | Gateway → Strict-B → Strict-A | I/O in Strict layers |
| Hardware | No | hardware may misbehave | Driver → Gateway → Validators | hardware inside @critical |
| In-process Python | Yes | CRSS rules enforceable | Strict-only chain | Strict→Core |

---

## 2.8 Final Statement

Boundaries define non-trustable edges.  
CRSS safety responsibilities begin only once:

- data enters Strict-B validation, and  
- control enters Strict-A execution.



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
SafetyLevel(Y) := higher_of(SafetyLevel(X), SafetyLevel(Y))

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

 **Critical code may never call non-critical code.**

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
- [NOT ALLOWED] Does **not** occur. Global profile rules still apply everywhere.

In other words:

- Non-critical code has more operational freedom
- [NOT ALLOWED] But no lower enforcement for MUST/MUST-NOT rules.

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

This section aligns analyzer severities with the updated Profile and Safety-Level model.

---

## 6.1 Severity Levels

- **INFO**  
  Non-actionable, stylistic, or informational messages.

- **WARN**  
  SHOULD/SHOULD-NOT violations.  
  Indicates reduced robustness but not unsafe behavior.

- **ERROR**  
  MUST/MUST-NOT violation for Core or Strict in **non-critical phase**.

- **BLOCKER**  
  MUST/MUST-NOT violation in:
  - **Strict-A critical phase**, OR
  - any context where a violation directly impacts Safety Level A.

---

## 6.2 Enforcement Matrix

| Mode / Phase             | MUST/MUST-NOT Violation        | SHOULD/SHOULD-NOT Violation          |
|--------------------------|---------------------------------|--------------------------------------|
| **Core (any phase)**     | ERROR                           | WARN                                 |
| **Strict (any phase)**   | ERROR                           | WARN (≤10% cumulative, explainable)  |
| **Strict-A — Critical**  | **BLOCKER**                     | **BLOCKER** (treated as MUST)        |
| **Strict-A — Non-Crit.** | BLOCKER (with deviation process) | WARN/ERROR per Strict rules          |

**Interpretation for Strict-A non-critical:**

A violation is **BLOCKER** by default, but may be accepted *only if*:

- The violation is documented as a deviation,
- Risk analysis demonstrates non-interference with critical path,
- It is isolated and justified,
- It is approved independently (e.g., by safety reviewer).


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

- Allowed:

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


## 10. Inheritance Policy

### 10.1 Depth Constraint

- Maximum inheritance depth in Strict code: **1** (base + one subclass)
- Multiple inheritance in Strict code: **forbidden** unless explicitly justified

### 10.2 Mode Constraints

Strict-A class **MUST NOT** inherit from:

- Core classes
- Lower-level Strict classes (Strict-B/C)

Strict-B class **MUST NOT** inherit from:

- Core classes
- Lower-level Strict classes (Strict-C)

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

- `ConfigLoader.load` -> Mode: Strict-B, non-critical
- `Sensor.read_raw` -> Mode: Strict-B, non-critical
- `SafetyController.initialize` -> Mode: Strict-A, `@non_critical_phase`
- `SafetyController.control_loop` -> Mode: Strict-A, `@critical`
- `Logger.log` -> Mode: Core-C, non-critical utility

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
- Any MUST violation -> **BLOCKER** unless deviation with isolation is fully justified.

**read_sensor_raw** and **load_config**:

- Non-critical Strict-B
- Called only before critical loop

**Logger:**

- Core-C
- Used only in non-critical phases

---

## 15. Third-Party Library and Framework Containment

### 15.1 Scope

This section defines how third-party Python packages, frameworks, and native extensions MAY be used in a CRSS-Python system without compromising Strict-A guarantees.

It applies to:

- PyPI and internal package indexes  
- Native extensions (C/C++/Rust)  
- Large frameworks (web, ORM, ML, etc.)

### 15.2 Version and Source Control

**TPL-1 — Pinned Versions Only**  
All third-party dependencies MUST be:

- Version-pinned in the dependency manifest, and  
- Recorded in the Configuration Baseline Manifest (CBM).   

**TPL-2 — No Implicit Online Resolution**  
Production builds and certification builds MUST NOT fetch packages from the public internet at build or deploy time. All dependencies MUST come from:

- an internal mirror, or  
- a pre-frozen local repository.

**TPL-2.1 — Certified Build Offline Install Mode (Normative)**
Certification builds MUST enforce offline dependency resolution by using at least one of:
- pip --no-index --find-links <frozen_repo>, or
- pip --index-url <internal_mirror> --no-deps with a fully pinned lock,

such that no dependency can be fetched from the public internet.

**TPL-2.2 — Frozen Repository Requirement (Normative)**
If a pre-frozen local repository is used, it MUST be treated as a baseline input:
- its contents (wheels/sdists) MUST be versioned or hash-manifested,
- the manifest MUST be recorded in the CBM,
- any change to frozen repository contents triggers a new baseline (new CBM + re-test).

This directly operationalizes TPL-1/TPL-2 in CI.

Test and evidence tools (pytest/coverage/etc.) are permitted in certification only if :
- they are version-pinned
- they are included in CBM/toolchain registry.

### 15.3 Critical vs Non-Critical Usage

TPL-3 — **No Direct Third-Party Calls in Strict-A @critical**

`@critical` Strict-A code MUST NOT call third-party libraries directly (including pure Python or native extensions).

Third-party usage MAY occur in:

- Core-C / Strict-B **non-critical** code paths, or  
- Strict/Strict-A **non-critical** initialization, configuration loading, or preprocessing steps, provided that the results are validated and converted into CRSS-controlled data structures before entering `@critical` code.

TPL-4 — **Adapter Pattern for Safety Boundaries**

If third-party functionality is required for safety-relevant behavior, it MUST be wrapped in a **Strict-compliant adapter**:

- Adapter defines a narrow, typed interface.  
- All inputs are validated before calling the third-party library.  
- All outputs are range-checked and converted into CRSS-controlled types.  
- Only the adapter’s stable, deterministic result is passed into `@critical` code.

TPL-5 — **Core Profile Isolation**

Third-party libraries that are not amenable to static analysis (heavy reflection, dynamic imports, metaprogramming) MUST be confined to **Core-C** utilities and MUST NOT influence Strict-A control decisions except through:

- offline tooling, or  
- explicit, validated inputs at non-critical boundaries.

### 15.4 SCEM Impact

Use of third-party libraries in any safety-relevant path MUST be:

- Documented in the Mode Assignment Register and dependency map (SCEM-D1/D2), and  
- Supported by robustness tests and fault injection in the Test Evidence Package (SCEM-D4).

For Strict-A systems, auditors SHOULD be able to see a clear **“third-party dependency map”** that proves:

- No third-party calls occur in `@critical` code, and  
- Any third-party influence is bounded and validated before it affects safety decisions.


## 16 Call Graph, Orchestrators, and Level-A Data Validation

### 16.1 Purpose

Defines cross-safety call rules, orchestrator structure, and the mandatory Level-A data flow:

```
Core-C/B Gateway
    → Strict-B Config/Data Provider
    → Strict-A Level-A Validator
    → Strict-A Critical Kernel
```

---

### 16.2 Definitions

**Outer Orchestrator (Core Orchestrator)**  
A Core-profile entrypoint that interacts with the external world:


OS, network, files, CLI, JSON, simulators, UI, etc.

Examples: TCP sensor server main, HTTP service main, process supervisor.

The outer orchestrator is Level C or B and is not part of the Level-A critical call graph. Its failure modes must be covered in the safety case, but it does not implement Level-A safety decisions.

**Strict-B Config/Data Provider**  
A Strict-B (or Core-B+Strict-B combination) component that:

- runs in non-critical phase,
- reads raw configuration and data from Core-C/B sources (files, JSON, env, gateways),
- performs structural and semantic validation (types, ranges, enums, completeness),
- normalizes into typed, bounded data structures passed into Strict-A.

Typical example: config.model + config.loader in the sensor-voting reference.

**Strict-A Level-A Validator (Mandatory)**  
A Strict-A component (often @non_critical_phase) that:

- receives only data already validated and typed by Strict-B Config/Data Providers,
- checks Level-A domain invariants, e.g.:
  - envelope parameters (min_safe, max_safe, SAFE_DEFAULT) are consistent,
  - thresholds and timeouts make physical and system sense,
  - initial values are within the safe operating region.
- runs under Strict-A determinism constraints: no I/O, no GC, no dynamic behavior.

The Level-A validator is the last gate before data enters the @critical path.

**Strict-A Critical Kernel**  
The minimal Strict-A @critical code implementing:

- voting, plausibility, and safety envelope,
- bounded state evolution (e.g. last safe actuator command),
- fail-safe behavior and SAFE_DEFAULT handling.

This is the only place where Level-A safety decisions are made.

---

### 16.3 Safety-Level Call Constraints (A/B/C)


| Caller ↓ / Callee → | C | B | A |
|----------------------|-----|-----|-----|
| C | Allowed | Allowed | Allowed |
| B | Not Allowed | Allowed | Allowed |
| A | Not Allowed | Not Allowed | Allowed |

Interpretation:

- Level-A MUST NOT depend on B or C.  
- Level-B MUST NOT depend on C.  
- Level-C may call A/B but is never in critical path.


#### 16.3.1 Absolute Rules for Level-A Code

Level-A code is the most sensitive. We enforce a **hard separation**:

**CRSS-Call-1 (Normative — Level-A Isolation)**  

1. A Level-A function (critical or non-critical):

   - MUST use the Strict profile (Strict-A).
   - MUST NOT call any Level-B or Level-C code.
   - MUST NOT call any Core code (Core-B/Core-C), including logging, metrics,
     monitoring, or helpers.

2. Level-A functions MAY only call:

   - other Level-A Strict functions, or
   - local pure helpers that are explicitly classified as Level-A Strict.

3. If a Level-A function currently calls a Level-B/C function and **uses its
   result for safety decisions, thresholds, or configuration**, then that
   callee must be **reclassified and refactored as Level-A Strict** or removed
   from the Level-A call path.

This guarantees that:

- Level-A behavior does not depend on lower-safety or Core behavior.
- A failure in a Core logging or utility function cannot break Level-A logic.

> **Practical effect:**  
> If you want Level-A behavior + logging, you do **not** log from inside the
> Level-A function. Instead, a lower-level component observes inputs/outputs
> (e.g. at Strict-B or Core-C) and logs them externally.

---

#### 16.3.2 Rules for Level-B and Level-C

Level-B and Level-C are less strict but still controlled.

**CRSS-Call-2 (Normative — Level-B)**  

1. Level-B functions:

   - Are not allowed to call level-C functions
   - Strict-B functions are not allowed to call Core-B functions (both direct and indirect calls are forbidden)


**CRSS-Call-3 (Normative — Level-C)**  

1. Level-C functions:

   - MAY call Level-C, Level-B, or Level-A functions.
   - MUST NOT be considered part of the Level-A critical path.
   - MUST be covered by the safety case as “environment / outer logic”.

Level-C is typically where the **Outer Orchestrator** lives (TCP servers, CLI
tools, UI adapters, etc.).

---

## 16.4 Profile Call Constraints (Strict vs Core)

Core ↔ Core: Allowed  
Core → Strict: Allowed  
Strict → Strict: Allowed  
Strict → Core: **Not Allowed** (baseline)

**CRSS-Call-Profile-1**  
Strict modules must not import/call Core in baseline.

**CRSS-Call-Profile-2**  
Strict→Core allowed only in tests/tools.

---

## 16.5 Phase Interaction

**CRSS-Call-Phase-1 (Normative)**  

- @critical MUST NOT call @non_critical_phase.  
- Level-A @critical may call only Strict-A that respects critical-phase rules.  
- Non-critical may enter critical, but control must not bounce between phases.

---

## 16.6 Level-A Separation

**CRSS-Call-A-1 (Normative)**  

Level-A MUST NOT call:

- Level-B or Level-C,  
- Core-B or Core-C,  
- logging/metrics/utilities in Core.

Logging must occur in wrappers (Strict-B/Core-C), not within Level-A.

---

## 16.7 Canonical Data Flow

```
Core-C/B Gateway
    ↓ non-critical
Strict-B Config/Data Provider
    ↓ validated, typed
Strict-A Level-A Validator
    ↓ domain-validated, immutable
Strict-A Critical Kernel
```

**CRSS-Call-A-2 — No Direct Core→Level-A Flow**  
Strict-A MUST NOT consume raw Core-C/B data.  
It MUST pass through:

1. Strict-B Config/Data Provider  
2. Strict-A Level-A Validator

before any @critical use.

---

## 16.8 Orchestrators

**Outer Orchestrator (Core)**  
Handles I/O, frames, invokes Strict-B/A.

**CRSS-Orch-1**  
May not implement Level-A logic; may not bypass Strict-B/A.

**Inner Orchestrator (Strict-B)**  
Sequences validator + kernel.

**CRSS-Orch-2**  
Must be Strict-B or higher; must appear in SCEM; must not call Core on critical path.

---

### 16.9 Concrete Call Graph Examples

**Example 1 — Correct (Level-A isolated)**

```python
# strict_a_controller.py  (Level A, Strict-A)
def level_a_step(cfg: SafetyConfig, sensors: list[float]) -> ActuatorCommand:
    voted = level_a_voting(cfg, sensors)         # Level-A Strict
    clamped = level_a_envelope(cfg, voted)       # Level-A Strict
    return ActuatorCommand(clamped, "NORMAL")
```

All callees (level_a_voting, level_a_envelope) are Level-A Strict.

No logging, no Core utilities → fully compliant with CRSS-Call-1.

---

**Example 2 — Wrong (Level-A calling lower level)**

```python
# bad_example.py
def level_a_step(cfg, sensors):
    log_debug("entering level_a_step")           # Core-C logging
    voted = level_b_voting(cfg, sensors)        # Level-B logic
    return apply_level_a_envelope(cfg, voted)
```

Violations:

- `log_debug` is Core-C → forbidden for Level-A.
- `level_b_voting` is Level-B → forbidden; must be Level-A Strict or removed.

---

**Example 3 — Correct (B calling A)**

```python
# strict_b_step.py  (Level B, Strict-B)
def level_b_safety_step(cfg_b, cfg_a, sensors):
    voted = purely_level_b_monitoring_logic(cfg_b, sensors)   # Level-B
    cmd   = level_a_step(cfg_a, sensors)                      # Level-A Strict
    return cmd
```

Level-B may call Level-A.  
Level-B failure does not change Level-A logic, only whether we reach it.

---

### 16.10 Data Handling

**CRSS-Call-Data-1 (Normative — Level-A Data Entry Chain)**
Any data (inputs, configuration, thresholds, state) that influences a Level-A `@critical` decision MUST traverse the following chain:

1. **Ingestion at Core-C/B or Strict-B** (gateway, I/O, files, JSON, env, bus).
2. **Structural + semantic validation at Strict-B Config/Data Provider** (types, ranges, enums, completeness, shape).
3. **Level-A domain validation at Strict-A Level-A Validator** (envelope consistency, physical plausibility, SAFE_DEFAULT consistency).
4. **Consumption by Strict-A Critical Kernel** using **immutable, bounded structures**.

Direct feeding of raw or partially validated data into Strict-A validators or kernels (e.g. `Core → Strict-A kernel`, `Strict-B → Strict-A kernel` without steps 2 and 3) is **NOT ALLOWED** and constitutes a violation of **CRSS-Call-Data-1**.

**CRSS-Data-Ownership-1 (Normative — Level-A Data Ownership & Immutability)**

1. Any data structure owned by Level-A (validators or kernel) MUST NOT be mutated by Level-B, Level-C, or Core code after it has been passed into Level-A.
2. Data shared between Level-A and lower levels MUST be:
   - immutable (e.g. tuples, frozen dataclasses, closed Enums), or
   - copied on handoff (Level-A receives its own private copy).
3. Lower-level code (B/C/Core) MUST NOT hold mutable references to Level-A internal state or configuration.
4. SCEM/MAR MUST capture these ownership assumptions for all Level-A-relevant configuration and state structures.

**CRSS-Config-1 (Normative — Configuration Boundary for Level-A)**

1. All configuration ingestion, parsing, and initial decoding (JSON, YAML, TOML, env vars, CLI, raw bytes, bus payloads) MUST be implemented at Safety Level B or C (Core or Strict).
2. Level-A code (validators and kernel) MUST operate only on already validated, normalized, bounded configuration structures provided by Strict-B Config/Data Providers.
3. Level-A MUST NOT:
   - open files or sockets to read configuration,
   - parse JSON/YAML/etc.,
   - reinterpret raw strings, bytes, or untyped dictionaries as configuration.

**CRSS-Call-Profile-2 (Normative — Strict→Core Only in Non-Baseline Artifacts)**

1. In the certified safety baseline (code included in CBM/SCEM and production artifacts), Strict code (Strict-A/B/C) MUST NOT:
   - import Core modules, or
   - call Core functions.
2. Strict→Core calls are allowed only in:
   - test modules (e.g. under `tests/`),
   - offline tools and scripts (e.g. under `tools/`),
   provided that:
   - they are clearly separated by namespace/path, and
   - they are **excluded** from certified/production builds and from SCEM/CBM.
3. Any Strict→Core call discovered in production artifacts SHALL be treated as a **hard non-compliance**.

---

### 16.11 Level-A Output & Actuation Boundary

**CRSS-Output-1 (Normative — Level-A Output Semantics)**

1. Strict-A Critical Kernels MUST produce **abstract, immutable outputs** that fully represent the safety-relevant decision, e.g. `ActuatorCommand` with:
   - bounded numeric value,
   - status (NORMAL/DEGRADED/FAILSAFE),
   - `safe_default_used` flag.
2. Strict-A kernels MUST NOT perform I/O, network, bus operations, or hardware access to apply these commands directly to external systems.

**CRSS-Output-2 (Normative — Actuation Adapter Role)**

1. Application of Level-A outputs to the outside world (actuator buses, RTOS hooks, hardware drivers, external protocols) MUST be implemented by an **Actuation Adapter** at:
   - Strict-B, or
   - Core-C/B,
   **outside** the Level-A critical path.
2. The Actuation Adapter:
   - MAY encode Level-A commands into wire formats (CAN/LIN/TCP/JSON/etc.),
   - MAY perform best-effort logging/telemetry,
   - MAY further **tighten** safety (e.g. additional clamping, dropping commands),
   but MUST NOT:
   - generate a command that is more dangerous than the Strict-A output,
   - relax any Level-A safety constraint or envelope,
   - silently substitute a different command without being treated as a safety-relevant component itself.

**CRSS-Output-3 (Normative — One-Way Semantic Dependence)**

1. Level-A decision logic MUST NOT depend on the behavior of the Actuation Adapter: the adapter is downstream only.
2. Failures in the Actuation Adapter MUST be treated in the safety case as:
   - fail-stop (no command sent), or
   - safe degradation (e.g. holding last safe command or using SAFE_DEFAULT),
   but MUST NOT cause unsafe actuation *relative to the Level-A command*.
3. SCEM/MAR MUST document:
   - where Level-A outputs are generated,
   - where they are adapted to external interfaces,
   - what guarantees exist that adaptation cannot violate Level-A decisions.

**CRSS-Output-4 (Normative — Level-A Safety Closure)**
Any Level-A Strict-A kernel function MUST guarantee that for all inputs within its representable domain:

- The produced actuator command is either:
  - within the configured safe envelope, OR
  - an explicitly defined SAFE_DEFAULT or failsafe command,

and MUST NEVER produce an actuator output that violates the declared safe envelope.

**CRSS-Kernel-Total-1 (Normative — Total Safe Behavior)**
Level-A Strict-A kernel functions SHALL be designed and verified as total safe functions over their representable input domain:

- For any combination of input data and internal state reachable in the system, the kernel MUST NOT produce an actuator command that violates the configured safe envelope or the declared safety goals.
- In the presence of invalid, inconsistent, implausible, or missing inputs, the kernel MUST transition to a defined safe behavior (e.g. SAFE_DEFAULT + failsafe status).

Level-A safety arguments MUST NOT rely solely on upstream validators behaving perfectly; Level-A kernels must be intrinsically safe by construction.

**How Level-A should react to bad or garbage inputs (Guidance)**

Examples of bad inputs:
- All sensors NaN or inf.
- Completely out-of-range values (e.g. ±1e12).
- Empty arrays / wrong lengths.
- Flags inconsistent with values.

Expected Level-A kernel behavior in those cases:
- Treat the situation as no valid safe measurement.
- Produce SAFE_DEFAULT (e.g. minimal torque, inhibit, neutral position) and a status like FAILSAFE, DEGRADED, or NO_VALID_SENSORS.

The validator chain exists for assurance and clarity, not as a fragile precondition that lets Level-A misbehave if someone upstream forgot a check.

---

### 16.12 Level-A API & Signature Rules

**CRSS-API-1 (Normative — Closed Signatures for Level-A)**
Level-A Strict-A kernel functions SHALL use fixed, explicit signatures:

- No `*args`
- No `**kwargs`
- No dynamic argument unpacking from dictionaries
- No runtime signature changes or decorators that alter call semantics

Level-A functions MAY only accept:
- primitive types (e.g. `float`, `int`, `bool`), and/or
- closed Enums defined at import time (no dynamic extension), and/or
- immutable, typed data structures (e.g. frozen dataclasses) with well-defined fields.

**Rationale:**
Signatures must be statically inspectable and analyzable. No dynamic or flexible API shape on the critical kernel.

**CRSS-API-2 (Normative — No Arity Flexibility)**
Level-A kernel functions SHALL NOT rely on optional positional parameters whose presence/absence changes behavior:

- Either the parameter is always required (and enforced by the caller), or
- the “optional” nature is represented as an explicit field in a typed input object (e.g. `Optional[float]`), with defined semantics in the kernel.

Example (Allowed):
```python
from dataclasses import dataclass

@dataclass(frozen=True)
class VotedInputs:
    sensors: tuple[float, float, float]
    has_valid_vote: bool
```

Kernel always receives `VotedInputs` and handles `has_valid_vote` explicitly — no “missing argument” concept at runtime.

#### 16.12.1 Defaults in Level-A Signatures

**CRSS-API-3 (Normative — Default Values in Level-A)**

- No mutable defaults.
- Level-A functions MUST NOT use mutable default arguments (`list`, `dict`, custom objects).

Defaults MUST represent safe, conservative behavior. If a Level-A parameter has a default value, that default MUST:
- be within the safe envelope, and
- correspond to a non-dangerous behavior (e.g. SAFE_DEFAULT, inhibit).

Defaults MUST NOT hide missing validation. Defaults SHALL NOT be used to silently compensate for missing Level-B or Level-A validation. If a parameter is conceptually mandatory from a safety perspective, it MUST either:
- be supplied explicitly by the caller, or
- be part of a validated config object that is guaranteed to exist.

**Recommended practice:**
For Level-A kernels, prefer no defaults at all and require fully constructed input objects. Use defaults in the config/data layer (Strict-B) instead.

#### 16.12.2 Handling “Non-Provided” or Unknown Data

**CRSS-API-4 (Normative — Explicit Representation of Missing Data)**

Level-A kernels MUST NOT infer “missingness” of data from call-shape (e.g. checking argument count or presence in `**kwargs`).

If safety semantics depend on data being present or absent, this MUST be represented explicitly in the input model, for example:
- a `present: bool` flag,
- an `Optional[...]` field,
- an explicit status enum: `OK / MISSING / INVALID`.

Level-A kernel MUST handle all allowed combinations of these states by:
- producing a safe command, or
- falling back to SAFE_DEFAULT / failsafe.

---

### 16.13 Upstream Responsibility for Uncallable Cases

**CRSS-API-5 (Normative — No “Half-Baked” Calls into Level-A)**

Gateways and Strict-B providers MUST ensure that Level-A kernel functions are never called with:
- wrong arity,
- wrong types,
- missing mandatory fields that cannot be represented in the input model.

If raw inputs cannot be parsed or mapped into the Level-A input model:
- Level-A MUST NOT be called, OR
- the call MUST be made with a well-defined “no data / degraded” representation that the kernel can handle safely (e.g. `has_valid_vote=False`, all sensors flagged invalid).

---

### 16.14 Level-A Composition and Call Graph

**CRSS-Call-Graph-1 (Normative — Level-A Call Graph Structure)**
For Level-A code, the call graph SHOULD form a Directed Acyclic Graph (DAG) at the module or service boundary.

Where Level-A cycles are unavoidable (e.g. small mutual recursion):

- They MUST NOT cross phase boundaries (`@critical` ↔ `@non_critical_phase`),
- They MUST NOT involve profile changes (Strict-A only),
- They MUST be documented in SCEM/MAR, and
- They MUST be justified in the safety case with respect to:
  - bounded recursion or loop depth,
  - timing analysis,
  - state convergence and stability.

**CRSS-LA-Chain-1 (Normative — Composition of Level-A Kernels)**
When a Level-A function A-2 consumes a value produced by another Level-A function A-1:

- The preferred pattern is a pure Level-A pipeline: the orchestration (A1 → A2) is itself implemented as Level-A Strict.
- If orchestration is implemented outside Level-A (e.g. in Strict-B), that layer MUST remain a pass-through and MUST NOT introduce safety-relevant branching.

If a Strict-B orchestrator wires A-1 and A-2, it MUST NOT:
- mutate the intermediate Level-A result,
- perform safety-relevant branching on that result,
- derive new safety decisions from that result.

Any such behavior MUST be moved into Level-A code.

**Pattern 1 — Recommended: Level-A orchestrates Level-A**
```python
# strict_a_controller.py   (Mode: Strict-A)

def A1_voting(inputs: VotedInputs) -> VotingResult:
    ...

def A2_envelope(cfg: SafetyConfig, v: VotingResult) -> ActuatorCommand:
    ...

def A_step(cfg: SafetyConfig, inputs: VotedInputs) -> ActuatorCommand:
    # Level-A orchestrator (still Level-A Strict code)
    v = A1_voting(inputs)
    cmd = A2_envelope(cfg, v)
    return cmd
```

**Pattern 2 — Acceptable: Strict-B wires A₁ and A₂ only as a pass-through**
```python
# strict_b_orchestrator.py  (Mode: Strict-B)

def safety_step(cfg_a: SafetyConfig, inputs: VotedInputs) -> ActuatorCommand:
    v = level_a_voting(cfg_a, inputs)        # A1 (Level-A)
    cmd = level_a_envelope(cfg_a, v)         # A2 (Level-A)
    return cmd
```

If Strict-B starts doing safety-relevant logic (example NOT ALLOWED):
```python
if v.confidence < 0.8:
    # different safety behavior here
    ...
```
then that logic is effectively Level-A and MUST be moved into Level-A (into A₂ or a new A₃).

**CRSS-LA-Result-1 (Normative — Single Source of Truth for Level-A Results)**
Safety-relevant derived quantities at Level-A (e.g. voted value, final actuator command, safety envelope status) SHOULD have a single authoritative implementation.

It is NOT ALLOWED to have multiple ad-hoc implementations of the same safety concept in different Level-A functions, whose outputs are treated as equally authoritative, unless:
- the pattern is a deliberate redundant/diverse safety mechanism, and
- the arbitration logic is itself Level-A, safe-biased, and documented in SCEM/MAR.

Reusing the same Level-A helper function in multiple places is encouraged; duplicating its logic in different modules/classes is discouraged and may be treated as a finding in review.

**CRSS-LA-Result-2 (Normative — No Downward Re-Derivation)**
Lower-level components (Level-B/C, Core) MUST NOT re-compute or reinterpret Level-A kernel results for **safety decisions**.

They may:
- log them,
- display them,
- use them for non-safety analytics,

but any further safety decision or transformation based on these results MUST be implemented in Level-A Strict code.

A “safety decision” here means any logic that can change actuation behavior relative to the Level-A command based on reinterpretation or recomputation of Level-A derived quantities. Adapters may still **tighten** safety (drop/clamp), but MUST NOT compute an alternative actuation target from Level-A results.

**CRSS-LA-Decision-Model-1 (Normative — Single Logical Level-A Decision)**

Even when implemented as multiple Level-A Strict-A functions, a safety decision
SHALL be considered a single logical Level-A decision if:

- the functions are composed deterministically,
- no external state or lower-level logic intervenes in the composition,
- intermediate results are not independently acted upon outside the composition.

In such cases, the composed pipeline SHALL be treated as a single Level-A
kernel for the purposes of:

- safety argumentation,
- SCEM/MAR documentation,
- call-graph analysis,
- and compliance assessment.

Intermediate Level-A functions in such a pipeline are considered internal
computational stages, not independent safety decisions.


## 17. Machine-Readable Metadata (Optional Annex)

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

## 18 Allowed / Forbidden Matrix

### 18.1 Modes

SA = Strict-A  
SB = Strict-B  
SC = Strict-C  
CB = Core-B  
CC = Core-C  

### 18.2 Safety-Level Matrix

| Caller ↓ / Callee → | C | B | A |
|----------------------|-----|-----|-----|
| C | Allowed | Allowed | Allowed |
| B | Not Allowed | Allowed | Allowed |
| A | Not Allowed | Not Allowed | Allowed |

---

### 18.3 Mode→Mode Matrix (Baseline)

| Caller ↓ / Callee → | SA | SB | SC | CB | CC |
|----------------------|------|------|------|------|------|
| SA | Allowed | Not Allowed | Not Allowed | Not Allowed | Not Allowed |
| SB | Allowed | Allowed | Not Allowed | Not Allowed | Not Allowed |
| SC | Allowed | Allowed | Allowed | Not Allowed | Not Allowed |
| CB | Allowed | Allowed | Not Allowed | Allowed | Not Allowed |
| CC | Allowed | Allowed | Allowed | Allowed | Allowed |

Strict→Core is always **Not Allowed** in baseline.

---

### 18.4 Utility & Logging Rules

- Level-A never calls logging/metrics/utilities.  
- Strict→Core allowed only in tools/tests.  

---

### 18.5 Canonical Safe Pattern

```
Core-C/B Gateway
    → Strict-B Config/Data Provider
    → Strict-A Level-A Validator
    → Strict-A Critical Kernel (@critical)
    → Actuation layer (outside CRSS scope)
```

---

## 19. Summary

This Unified Safety Specification

- Centralizes all semantics for Profiles, Levels, Modes, and Phases
- Clearly distinguishes:
  - Global vs phase-scoped rules
  - Strict vs Strict-A enforcement
  - Operational vs rule relaxation
- Defines:
  - How Modes propagate and never demote
  - How imports and inheritance are constrained
  - How non-critical phases are allowed, but never allowed to pollute critical execution
- Provides:
  - A realistic, minimal, fully compliant example
  - A basis for tool implementation and certification arguments

It is intended to be the single master reference for **CRSS-Python** safety behavior and enforcement, while allowing software to still do its job under strong, explicit, and auditable constraints.