# CRSS-Python Standard Levels & Applicability

**Version:** v1.0.0
**Status:** Normative
**Maturity:** Stable
© 2025 Sofian Daghsen – All rights reserved
Distributed under CC BY-NC-ND 4.0 — see LICENSE-CRSS.

---

## Table of Contents

- [CRSS-Python Standard Levels & Applicability](#crss-python-standard-levels-applicability)
  - [0. Purpose](#0-purpose)
  - [1. Relationship to Core & Strict](#1-relationship-to-core-strict)
  - [2. Safety Levels & Mapping](#2-safety-levels-mapping)
    - [2.1 ISO 26262 Automotive (ASIL A–D)](#21-iso-26262-automotive-asil-a-d)
    - [2.2 IEC 61508 (SIL 1–4)](#22-iec-61508-sil-1-4)
    - [2.3 DO-178C / DO-278A (Avionics)](#23-do-178c-do-278a-avionics)
    - [2.4 IEC 62304 (Medical Class A/B/C)](#24-iec-62304-medical-class-abc)
  - [3. Strict Level A Mandatory Constraints](#3-strict-level-a-mandatory-constraints)
  - [4. Architectural Assumptions](#4-architectural-assumptions)
  - [5. What CRSS Cannot Support](#5-what-crss-cannot-support)
  - [6. What CRSS Achieves](#6-what-crss-achieves)
  - [7. Versioning & Governance](#7-versioning-governance)
  - [8. Summary](#8-summary)

## 0. Purpose

This document defines the **applicability, scope, and safety level coverage** of the CRSS-Python framework. It clarifies:
- The domains and safety integrity levels where CRSS may be used.
- The conditions and architectural constraints required for compliance.
- The limits of CRSS with respect to hard real-time and primary safety functions.

It is an official companion to:
1. **CRSS-Python Core Specification**
2. **CRSS-Python Strict Specification**
3. **CRSS-Python Deviations Matrix**

---

## 1. Relationship to Core & Strict

CRSS supports two profiles:
- **Core**: General safety-oriented Python subset.
- **Strict**: Critical and mission-focused subset.

This document does **not** introduce a new profile. Instead, it defines **safety levels** based on:
- Profile selection (Core or Strict)
- Criticality levels (A/B/C)
- Additional mandatory measures for **Strict Level A**

---

## 2. Safety Levels & Mapping

### 2.1 ISO 26262 Automotive (ASIL A–D)

| Safety Level | CRSS Profile | Applicability | Constraints |
|--------------|--------------|--------------|-------------|
| **ASIL A** | Core/Strict | General software units | None beyond Core/Strict rules |
| **ASIL B** | Core/Strict | Non-critical ECUs, services | Standard Core/Strict compliance |
| **ASIL C** | Strict | Supervisory, monitoring, diagnostics | Level A rules recommended |
| **ASIL D** | Strict | Supervisory / decision-support | **Mandatory**: Strict Level A constraints, isolation, watchdog, not primary actuator control, final actuation is handled by a certified ASIL-D stack |

**Not Allowed:** Python/CPython controlling primary braking/steering torque loops.

---

### 2.2 IEC 61508 (SIL 1–4)

| SIL Level | CRSS Applicability | Constraints |
|-----------|--------------------|-------------|
| **SIL 1–2** | Fully supported via Core/Strict | Standard compliance |
| **SIL 3** | Supported for supervisory/control | Strict Level A required |
| **SIL 4** | Not suitable for primary function | Can support tools/aux components |

---

### 2.3 DO-178C / DO-278A (Avionics)

| Level | Applicability | Constraints |
|-------|---------------|-------------|
| **DO-278A** | Ground systems, support tools | Standard compliance |
| **DAL D/C** | Non-flight-critical onboard utilities | Strict Level A recommended |
| **DAL B/A** | Not suitable | Python not permitted as primary flight control logic |

---

### 2.4 IEC 62304 (Medical Class A/B/C)

| Class | Applicability | Constraints |
|-------|--------------|-------------|
| **Class A/B** | Fully supported | Standard compliance |
| **Class C** | Supervisory/monitoring components | Strict Level A required; not single safety mechanism |

---

## 3. Strict Level A Mandatory Constraints

For the highest criticality (Level A), **the following rules are non-deviable**:

1. **GC Disabled** during critical execution
2. **No Dynamic Allocation** in critical paths
3. **Single-Threaded Execution**
4. **Process Isolation**
5. **Watchdog Supervision**
6. **Acyclic Object Graphs**
7. **No Finalizers (`__del__`)**
8. **NaN/Inf Checks on Numeric Outputs**
9. **On-Target / Hardware-in-the-Loop Testing**
10. **Frozen Interpreter & OS Configuration**
11. **Interpreter Conformance Test Suite**
12. **No Blocking Operations**
13. **Explicit Range Enforcement**

---

## 4. Architectural Assumptions

CRSS assumes:
- CPython on a general-purpose OS
- Python process is **not** the only line of defense
- Safety relies on **multiple layers**
- Timing guarantees are empirical, not formally certified

---

## 5. What CRSS Cannot Support

CRSS **cannot** certify:
- Hard real-time primary actuation loops
- Single-channel safety functions at ASIL D / SIL 4 (example:braking ECU, SIL 4 shutdown kernel)
- DAL A/B flight control or engine control

---

## 6. What CRSS Achieves

CRSS is suitable as a coding and verification standard for:
- ASIL D supervisory elements
- SIL 3 supervisory/control systems
- Class C multi-layer medical systems
- High-assurance industrial automation
- Ground avionics systems (DO-278)

CRSS represents one of the **strongest known Python safety standards**, enabling Python’s use in high-integrity environments where it was previously excluded.

---

## 7. Versioning & Governance

This document:
- Is versioned alongside Core & Strict specs
- May expand supported levels as evidence grows
- Must be referenced in project Safety Plans

---

## 8. Summary

CRSS does not turn Python into a certified RTOS or a SIL 4 kernel.

However, when fully applied:

> **CRSS enables Python to be used in ASIL D / SIL 3 supervisory safety roles under strict architectural conditions.**

This is a significant and unprecedented achievement for Python in safety-critical domains.
