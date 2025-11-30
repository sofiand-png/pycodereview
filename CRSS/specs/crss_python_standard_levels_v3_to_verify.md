# CRSS-Python Standard Levels, Modes & Enforcement Model

## Table of Contents

- [CRSS-Python Standard Levels, Modes & Enforcement Model](#crss-python-standard-levels-modes-enforcement-model)
  - [0. Purpose](#0-purpose)
  - [1. Profiles](#1-profiles)
  - [2. Safety Levels](#2-safety-levels)
  - [3. Modes (Unified Mechanism)](#3-modes-unified-mechanism)
  - [4. How Critical Marking Affects Mode](#4-how-critical-marking-affects-mode)
  - [5. Enforcement Matrix (Mandatory)](#5-enforcement-matrix-mandatory)
  - [6. Propagation Rules](#6-propagation-rules)
    - [6.1 Call-Chain Promotion](#61-call-chain-promotion)
    - [6.2 Class Promotion](#62-class-promotion)
    - [6.3 No Demotion](#63-no-demotion)
  - [7. Applicability Mapping (Corrected)](#7-applicability-mapping-corrected)
  - [8. Mixed System Acceptance](#8-mixed-system-acceptance)
  - [9. Summary](#9-summary)

Version: v2.0.0
Status: Normative Replacement
© 2025 Sofian Daghsen – All rights reserved

---

## 0. Purpose

This document unifies and replaces:

- **CRSS-Python Standard Levels v1.0.0**
- **CRSS Profile/Safety/Critical Interaction v1.0.0**

It defines, with zero ambiguity:

1. What CRSS can certify
2. What configurations exist (Core, Strict, Strict-A)
3. What a Mode is and how it is used
4. How rule violations are treated per Mode
5. How critical code affects Mode
6. How propagation works across dependencies
7. How mixed systems are evaluated

This document supersedes **Standard Levels v1.0.0**.

---

## 1. Profiles

Profiles define which rule set applies:

| Profile | Description | Enforcement Basis |
|--------|-------------|------------------|
| **Core** | General safety subset | MUST/WARN |
| **Strict** | High-integrity subset | MUST/ERROR |

Profiles are rule-level properties, not code-level properties.

---

## 2. Safety Levels

Safety Levels define system criticality:

| Level | Meaning | Typical Domains |
|-------|---------|-----------------|
| **A** | Highest | ASIL D / SIL 3 supervisory |
| **B** | Medium-High | ASIL C / SIL 2–3 |
| **C** | Low-Medium | ASIL A/B / SIL 1–2 |

Safety Levels apply to **code units**, not rules.

---

## 3. Modes (Unified Mechanism)

Mode = (Profile, Safety Level)

Valid Modes include:

- Core-C
- Core-B
- Strict-C
- Strict-B
- **Strict-A**

📌 **Strict-A = Strict + Level A + Zero Tolerance + SCEM/EAP**

Strict-A is NOT a new profile — it is a Mode.

---

## 4. How Critical Marking Affects Mode

- `@critical` forces **Strict** profile assignment
- `@critical` signals likely Level A/B
- Critical code cannot be Core
- Critical code requires Mode calculation and propagation

---

## 5. Enforcement Matrix (Mandatory)

| Mode | MUST | SHOULD | Result |
|------|------|--------|--------|
| Core-C/B | ERROR | WARN (≤20% allowed with justification) | Pass/Fail |
| Strict-C/B | ERROR | WARN (≤10% allowed with justification) | Pass/Fail |
| **Strict-A** | **BLOCKER** | **BLOCKER** | **0 violations permitted** |

Zero-tolerance for Strict-A is mandatory.

---

## 6. Propagation Rules

### 6.1 Call-Chain Promotion
If Level X code calls lower-level code that affects safety output:

> The callee is promoted to Level X.

### 6.2 Class Promotion
If any method becomes Level A:

> The entire class becomes Mode Strict-A.

### 6.3 No Demotion
Modes never decrease without full re-certification.

---

## 7. Applicability Mapping (Corrected)

All mappings in v1.0.0 remain correct **with one clarification**:

> All “Strict Level A” references must be interpreted as Mode Strict-A, not as a third profile.

All supervisory ASIL D / SIL 3 claims remain valid.

---

## 8. Mixed System Acceptance

A system passes only if:

✅ All Strict-A components have 0 violations
✅ Strict components meet Strict thresholds
✅ Core components cannot compromise Strict-A

---

## 9. Summary

This model guarantees:

✅ Deterministic critical behavior
✅ No hidden unsafe dependencies
✅ Fully analyzable Mode structure
✅ Complete certification alignment
✅ Practical, real-world feasibility

This v2.0.0 document is now the authoritative standard for Modes, Enforcement, Propagation, and Applicability in CRSS-Python.

---
