
# CRSS-Python Compliance & Acceptance Master Specification  
Version: v3.0.1  
Status: Normative  
© 2025 Sofian Daghsen – All rights reserved  

---

## 0. Purpose

This document is the **single authoritative specification** governing:

- The CRSS-Python **Compliance Process**
- The **External Assessment Protocol (EAP)**
- The **Acceptance Rules & Enforcement Criteria**

It replaces prior standalone documents and preserves the **strong, structured, phase-based format** of the original Compliance Process while fully updating terminology and policies to match:

✅ **CRSS Unified Safety Specification v3.0.0**  
✅ Mode model (Core/Strict/Strict-A)  
✅ Critical / Non-Critical execution model  
✅ Enforcement matrix (WARN / ERROR / BLOCKER)  
✅ Strict-A deviation policy (Option 2)  
✅ One-Python-version-per-project mandate  

No other compliance documents are required. This is the single source of truth for CRSS-Python certification.

---

# 1. Definitions

### 1.1 Profile
A rule catalog domain:
- **Core**
- **Strict**

### 1.2 Safety Level
A risk classification:
- **A**, **B**, **C**

### 1.3 Mode
A code unit’s enforcement identity:
```
Mode = Profile × Safety Level
```

### 1.4 Strict-A
A Mode defined as:
- Profile: **Strict**
- Safety Level: **A**
- Zero-tolerance in `@critical`
- SCEM/EAP evidence required

### 1.5 Critical Code
A function or region marked `@critical` where safety decisions are executed.

### 1.6 Non-Critical Code
A function marked `@non_critical_phase` executed **before or after** critical windows.

### 1.7 One-Version Rule
Each project MUST use **one fixed Python version**. Supporting another version requires **a new project baseline and new certification**.

---

# 2. Compliance Process (Phased Model)

## Phase 1 — Requirements & Safety Classification

### Objectives
- Map system requirements to Safety Levels (A/B/C)
- Assign Modes (Profile × Level) to functions/methods
- Identify `@critical` and `@non_critical_phase` boundaries

### Mandatory Outputs
- **Requirements Traceability Matrix (RTM)**
- **Mode Assignment Register (MAR)**

### Pass/Fail Criteria
✅ Complete RTM  
✅ Complete MAR  
❌ Missing Mode assignments → FAIL  
❌ Undefined critical boundaries → FAIL  

---

## Phase 2 — Rule Compliance Verification

### Objectives
- Apply Core/Strict rule catalogs
- Enforce Mode constraints
- Categorize violations per severity

### Mandatory Outputs
- **Rule Compliance Report (RCR)**

### Pass/Fail Criteria
✅ Automated + manual review performed  
✅ Violations categorized as WARN/ERROR/BLOCKER  
❌ Any unresolved BLOCKER → FAIL  

---

## Phase 3 — Testing & Coverage Evidence

### Objectives
- Validate behavior under test
- Achieve required coverage:
  - Core: **Statement**
  - Strict: **Branch**
  - Strict-A `@critical`: **MC/DC**
- Validate deterministic execution in `@critical`

### Mandatory Outputs
- **Test Evidence Package (TEP)**

### Pass/Fail Criteria
✅ Coverage targets met  
✅ Critical execution deterministic  
❌ Missed coverage target → FAIL  
❌ Timing nondeterminism in `@critical` → FAIL  

---

## Phase 4 — Baseline Establishment

### Objectives
- Freeze:
  - Python version (single fixed version)
  - Dependencies
  - OS version
  - Containers/VMs
  - Build flags/configs
- Produce reproducible build artifacts

### Mandatory Outputs
- **Configuration Baseline Manifest (CBM)**

### Pass/Fail Criteria
✅ CBM complete & immutable  
✅ Build reproducible  
❌ Version drift → FAIL  
❌ Multiple Python versions → FAIL  

---

## Phase 5 — External Assessment & Approval (EAP)

### Objectives
Independent validation of:
- RCR
- TEP
- CBM
- MAR
- Mode enforcement
- Critical boundary integrity
- Strict-A deviation handling

### Mandatory Outputs
- **Compliance Certificate (CC)**

### Pass/Fail Criteria
✅ All evidence accepted  
✅ No unresolved deviations  
❌ Any Strict-A `@critical` violation → FAIL  
❌ Critical calling non-critical → FAIL  

---

# 3. Enforcement & Violation Handling

## 3.1 Severity Categories

- **INFO** – non-actionable
- **WARN** – SHOULD/SHOULD-NOT violation
- **ERROR** – MUST/MUST-NOT violation (Core/Strict)
- **BLOCKER** – MUST/MUST-NOT violation in Strict-A `@critical`

## 3.2 Enforcement Matrix

| Mode | MUST Violation | SHOULD Violation |
|------|----------------|------------------|
| Core | ERROR | WARN |
| Strict | ERROR | WARN (≤10%) |
| Strict-A `@critical` | BLOCKER | BLOCKER |
| Strict-A `@non_critical_phase` | BLOCKER unless deviation | WARN/ERROR per Strict |

## 3.3 Strict-A Deviation Policy (Option 2)

Allowed **only** in `@non_critical_phase`, if:

✅ Documented  
✅ Risk assessed  
✅ Proven isolated from `@critical`  
✅ Independently approved  

Not permitted in `@critical` under ANY circumstance.

---

# 4. Acceptance Rules

## 4.1 Project Pass Criteria

A project passes compliance **only if**:

✅ Strict-A `@critical` has **zero** violations  
✅ Strict-A deviations (non-critical only) are approved  
✅ Strict meets WARN ≤ 10% threshold  
✅ Core violations do not compromise Strict-A safety  
✅ Critical never calls non-critical  
✅ Mode propagation is resolved  
✅ One fixed Python version is used  

## 4.2 Automatic Failure Conditions

A project FAILS if:

❌ Any Strict-A `@critical` violation exists  
❌ Critical code calls non-critical code  
❌ Multiple Python versions are used  
❌ CBM is incomplete  
❌ Build is not reproducible  
❌ Any unresolved BLOCKER  

---

# 5. Python Version Policy

✅ Standard supports Python **3.9–3.12**  
✅ Projects must choose **exactly one version**  
✅ That version must remain frozen in CBM  

Switching versions requires:

- New baseline
- New compliance cycle
- New certification

---

# 6. Summary

This document:

✅ Restores the strong structured format of the original process  
✅ Fully aligns with v3.0.0 Unified Spec  
✅ Integrates Acceptance Rules directly and cleanly  
✅ Defines clear PASS/FAIL logic  
✅ Enforces one-version-per-project policy  
✅ Enables certifiable, auditable compliance  

This is the **mandatory certification reference** for all CRSS-Python projects.

---
