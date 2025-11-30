# CRSS-Python Standard Levels & Applicability

## Table of Contents

- [CRSS-Python Standard Levels & Applicability](#crss-python-standard-levels-applicability)
  - [0. Purpose](#0-purpose)
  - [1. Profiles & Safety Levels](#1-profiles-safety-levels)
  - [2. Safety Level Mapping (Updated & Evidence-Based)](#2-safety-level-mapping-updated-evidence-based)
    - [2.1 ISO 26262 Automotive (ASIL A–D)](#21-iso-26262-automotive-asil-a-d)
    - [CRSS-ASIL Boundary Statement](#crss-asil-boundary-statement)
    - [2.2 IEC 61508 (SIL 1–4)](#22-iec-61508-sil-1-4)
    - [2.3 DO-178C / DO-278A (Avionics)](#23-do-178c-do-278a-avionics)
    - [2.4 IEC 62304 (Medical)](#24-iec-62304-medical)
  - [3. Strict Level A Mandatory Constraints (Expanded)](#3-strict-level-a-mandatory-constraints-expanded)
    - [3.1 Execution Constraints](#31-execution-constraints)
    - [3.2 Timing & Performance](#32-timing-performance)
    - [3.3 Architecture & Deployment](#33-architecture-deployment)
    - [3.4 Data Integrity](#34-data-integrity)
    - [3.5 Evidence & Certification](#35-evidence-certification)
  - [4. Architectural Preconditions (Updated)](#4-architectural-preconditions-updated)
  - [5. Explicit Non-Supported Use Cases](#5-explicit-non-supported-use-cases)
  - [6. What CRSS Enables (Objective Assessment)](#6-what-crss-enables-objective-assessment)
  - [7. Certification Realism & Completeness](#7-certification-realism-completeness)
    - [✅ Technically Realistic](#✅-technically-realistic)
    - [✅ Certifiable in Real Industries](#✅-certifiable-in-real-industries)
    - [✅ Complete Framework](#✅-complete-framework)
    - [⚠ Remaining Boundaries](#⚠-remaining-boundaries)
  - [8. Governance](#8-governance)
  - [9. Final Summary](#9-final-summary)

Version: v1.0.0
Status: Official Release
© 2025 Sofian Daghsen – All rights reserved

---

## 0. Purpose

This document defines the **applicability, safety level coverage, system constraints, and certification limits** of the CRSS-Python framework **after the full integration** of:

- SCEM (Safety Case & Evidence Model)
- EAP (External Assessment Protocol)
- Timing Constraints Methodology
- TCA (Toolchain Confidence Assessment)
- Deployment & Release Governance
- Compliance Automation
- Microservices, networking, big data, sensitive data & caching rules
- Architectural safety rules

It clarifies, objectively:

✅ Where CRSS **can** be used
✅ Under what **conditions**
✅ What **levels** it supports
✅ What CRSS **cannot** certify
✅ The **system architecture requirements** for each level

This document supersedes v0.1.0.

---

## 1. Profiles & Safety Levels

CRSS defines three enforceable configurations:

| Profile | Description | Intended Criticality |
|--------|-------------|----------------------|
| **Core** | General safety subset | Low to Medium |
| **Strict** | High-integrity subset | Medium to High |
| **Strict Level A** | Maximum constraint mode | Highest criticality (supervisory roles only) |

**Strict Level A** is now a formally defined configuration, not merely a guidance layer.

---

## 2. Safety Level Mapping (Updated & Evidence-Based)

### 2.1 ISO 26262 Automotive (ASIL A–D)

| Safety Level | CRSS Applicability | Constraints | Status |
|--------------|--------------------|-------------|--------|
| **ASIL A** | Core or Strict | Standard compliance | ✅ Supported |
| **ASIL B** | Core or Strict | Standard compliance | ✅ Supported |
| **ASIL C** | Strict | MC/DC recommended, SCEM optional | ✅ Supported |
| **ASIL D** | **Strict Level A** | Isolation, watchdog, supervisory-only, dual-channel architecture | ✅ Supported (Supervisory role only) |

**NOT PERMITTED:** Python executing primary actuation loops (e.g., steering torque, braking modulation).

### CRSS-ASIL Boundary Statement
CRSS cannot replace certified ASIL-D real-time control firmware but **can supervise, validate, monitor, calculate setpoints, detect anomalies, or request safe states**.

---

### 2.2 IEC 61508 (SIL 1–4)

| SIL Level | CRSS Applicability | Constraints | Status |
|-----------|--------------------|-------------|--------|
| **SIL 1–2** | Core/Strict | Standard compliance | ✅ Supported |
| **SIL 3** | Strict Level A | Separation kernel, watchdog, dual-channel architecture, EAP required | ✅ Supported (Supervisory role) |
| **SIL 4** | Not suitable | Python cannot satisfy formal timing and toolchain cert requirements | ❌ Not Supported |

SIL 4 requires mathematical real-time guarantees and proven compiler determinism, which CPython cannot provide.

---

### 2.3 DO-178C / DO-278A (Avionics)

| Level | Applicability | Constraints | Status |
|-------|--------------|-------------|--------|
| **DO-278A** | Ground systems, test tools, monitoring platforms | CRSS compliance | ✅ Supported |
| **DAL D/C** | Non-flight-critical onboard utilities | Strict Level A recommended | ⚠ Conditionally Supported |
| **DAL B/A** | Flight controls, engine control | Real-time determinism required | ❌ Not Supported |

Python cannot meet DAL A/B timing determinism, toolchain qualification burden, or airborne certification constraints.

---

### 2.4 IEC 62304 (Medical)

| Class | Applicability | Constraints | Status |
|-------|--------------|-------------|--------|
| **Class A/B** | Full system components | Standard compliance | ✅ Supported |
| **Class C** | Supervisory components only | Strict Level A, multi-layered safety | ✅ Supported (Supervisory role only) |

Single-channel Class C primary control loops are not permitted.

---

## 3. Strict Level A Mandatory Constraints (Expanded)

Strict Level A requires all of the following:

### 3.1 Execution Constraints
1. **GC Disabled**
2. **No Dynamic Allocation**
3. **Bounded Loops**
4. **No Recursion**
5. **Single-threaded execution inside critical zones**
6. **Process isolation for critical components**
7. **No finalizers (`__del__`)**
8. **Acyclic object graphs**
9. **No dynamic imports or runtime code loading**
10. **No subprocess or shell execution**

### 3.2 Timing & Performance
11. **WCET evidence via Formal Timing Methodology**
12. **On-target performance testing**
13. **Latency budgets defined and verified**
14. **No blocking or unbounded I/O**

### 3.3 Architecture & Deployment
15. **Immutable deployments**
16. **Frozen interpreter, OS, containers, dependencies**
17. **Private package mirror**
18. **Zero-drift enforcement**
19. **Reproducible build snapshots**
20. **Independent watchdog supervision**

### 3.4 Data Integrity
21. **Explicit numeric bounds**
22. **NaN/Inf rejection**
23. **Schema validation for all external data**
24. **Payload size limits**
25. **Integrity checks for network/file transfers**

### 3.5 Evidence & Certification
26. **Full SCEM safety case**
27. **EAP external assessment**
28. **100% MUST rule compliance**
29. **MC/DC or equivalent coverage**
30. **Signed Compliance Certificate**

No deviation is permitted at Level A.

---

## 4. Architectural Preconditions (Updated)

CRSS assumes:

✅ CPython 3.9–3.12
✅ General-purpose OS (Linux/RT-POSIX recommended)
✅ Python is **not** the sole safety mechanism
✅ Safety relies on **multi-layer system design**
✅ Timing guarantees are **tested, not formal**
✅ Isolation from primary actuation loops

Additionally:

✅ For ASIL D/SIL 3: dual-channel or multi-channel safety architecture is required
✅ For Strict Level A: watchdogs and safe-state triggers are mandatory

---

## 5. Explicit Non-Supported Use Cases

CRSS **cannot** certify:

❌ Hard real-time primary control loops
❌ SIL 4 or DAL A/B primary systems
❌ Single-channel ASIL D primary actuators
❌ Systems requiring formal WCET proof at microsecond scale
❌ Systems without hardware redundancy
❌ Systems requiring certified toolchains at compiler/interpreter level

---

## 6. What CRSS Enables (Objective Assessment)

CRSS now achieves:

✅ Python in **ASIL D / SIL 3 supervisory roles**
✅ Certifiable safety cases (SCEM + EAP)
✅ Independent third-party verification
✅ Immutable and reproducible deployments
✅ Toolchain and timing confidence models
✅ Full lifecycle traceability and governance

This is **unprecedented** in the Python ecosystem.

No other publicly documented Python framework provides:

- Coding standard
- Deployment model
- Certification process
- External audit protocol
- Toolchain and timing methodologies

CRSS represents the **maximum safety rigor practically achievable** with CPython.

---

## 7. Certification Realism & Completeness

### ✅ Technically Realistic
- All rules align with known safety practices
- No reliance on unproven technology
- Requirements enforceable via tools and processes
- Architecture assumptions are realistic and testable

### ✅ Certifiable in Real Industries
CRSS can support certification efforts for:
- ISO 26262 ASIL D (supervisory)
- IEC 61508 SIL 3 (supervisory)
- IEC 62304 Class C (multi-layer)
- DO-278A ground systems

### ✅ Complete Framework
CRSS now covers:
- Coding rules
- Processes
- Evidence models
- Timing
- Toolchain confidence
- Deployment integrity
- Release governance
- External audits

### ⚠ Remaining Boundaries
CRSS does **not** overcome:
- CPython non-deterministic garbage collector at interpreter level
- Lack of certified CPython interpreter
- Hard real-time kernel absence

These are inherent platform limitations.

---

## 8. Governance

This document:

- Is versioned alongside all core specifications
- Must be referenced in Safety Plans and SCEM
- Shall be updated only through controlled Release Management

---

## 9. Final Summary

CRSS does **not** transform Python into a SIL 4 kernel or a DAL A flight controller.

However:

> **CRSS reaches the maximum theoretically achievable safety level for CPython-based systems: ASIL D / SIL 3 in supervisory roles, under strict architectural conditions.**

This is a landmark achievement for Python in safety-critical engineering.
