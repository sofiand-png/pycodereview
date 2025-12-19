# CRSS-Python Safety Case & Maturity Master Specification

**Version:** v1.0.0
**Status:** Normative
**Maturity:** Stable
© 2025 Sofian Daghsen – All rights reserved
Distributed under CC BY-NC-ND 4.0 — see LICENSE-CRSS.

---

## Table of Contents

- [0. Purpose](#0-purpose)
- [1. SCEM — Safety Case Evidence Model](#1-scem--safety-case-evidence-model)
  - [1.1 Objective](#11-objective)
  - [1.2 SCEM Evidence Categories](#12-scem-evidence-categories)
  - [1.3 Mandatory SCEM Artifacts](#13-mandatory-scem-artifacts)
    - [D1 — Requirements & Classification](#d1--requirements--classification)
    - [D2 — Design & Architecture](#d2--design--architecture)
    - [D3 — Compliance Artifacts](#d3--compliance-artifacts)
    - [D4 — Testing & Behavior](#d4--testing--behavior)
    - [D5 — Configuration Integrity](#d5--configuration-integrity)
    - [D6 — Operational Readiness](#d6--operational-readiness)
  - [1.4 SCEM Completion Rules](#14-scem-completion-rules)
  - [1.5 SCEM & Modes](#15-scem--modes)
  - [1.6 Quantitative Verification Targets per Mode](#16-quantitative-verification-targets-per-mode)
    - [1.6.1 Coverage Targets](#161-coverage-targets)
    - [1.6.2 Robustness & Fault Injection](#162-robustness--fault-injection)
    - [1.6.3 Independence](#163-independence)
- [2. SCEM Annexes (Consolidated)](#2-scem-annexes-consolidated)
  - [Annex A — Mode Assignment Register (MAR)](#annex-a--mode-assignment-register-mar)
  - [Annex B — Critical Boundary Declaration (CBD)](#annex-b--critical-boundary-declaration-cbd)
  - [Annex C — Mode Propagation Record](#annex-c--mode-propagation-record)
  - [Annex D — Deviation Register](#annex-d--deviation-register)
  - [Annex E — Determinism Validation Checklist (Strict-A Only)](#annex-e--determinism-validation-checklist-strict-a-only)
  - [Annex F — One-Version Python Confirmation](#annex-f--one-version-python-confirmation)
- [3. Safety Maturity Model (SMM)](#3-safety-maturity-model-smm)
  - [3.1 Purpose](#31-purpose)
  - [3.2 Levels](#32-levels)
  - [3.3 Maturity Requirements](#33-maturity-requirements)
    - [S1 — Controlled](#s1--controlled)
    - [S2 — Managed](#s2--managed)
    - [S3 — Verified](#s3--verified)
    - [S4 — Certified](#s4--certified)
  - [3.4 Maturity Assessment Output](#34-maturity-assessment-output)
- [4. Summary](#4-summary)

---

# 0. Purpose

This master document consolidates and replaces three prior specifications:

1. **SCEM — Safety Case Evidence Model**
2. **SCEM Annexes**
3. **Safety Maturity Model**

It fully aligns with:

- CRSS Unified Safety Specification v3.0.0
- Compliance Master v3.0.1
- Mode Model (Core/Strict/Strict-A)
- Critical / Non-Critical execution
- Strict-A deviation policy (Option 2)
- One-version-per-project policy

This is the **single authoritative reference** for building, maintaining, and evaluating a safety case under CRSS-Python.

---

# 1. SCEM — Safety Case Evidence Model

## 1.1 Objective

The SCEM defines **what evidence** must exist to:
- Support safety claims,
- Demonstrate rule compliance,
- Substantiate Mode (Profile × Level),
- Justify certification readiness.

It answers:
> “Do we have the proof that this system is safe under CRSS-Python?”

It is formal, auditable, and mandatory for **Strict** and **Strict-A** projects.

---

## 1.2 SCEM Evidence Categories

The SCEM is organized into **six mandatory evidence domains**:

| Domain | Purpose |
|--------|---------|
| D1 — Requirements & Safety Classification | Shows correct Mode & Level assignment |
| D2 — Design & Architecture Control | Shows structural safety compliance |
| D3 — Rule Compliance Evidence | Shows adherence to CRSS rules |
| D4 — Testing & Behavioral Evidence | Shows correctness & determinism |
| D5 — Configuration & Environment Integrity | Shows reproducibility & immutability |
| D6 — Operational Safety Readiness | Shows runtime safety measures & monitoring |

Each domain contains required artifacts.

---

## 1.3 Mandatory SCEM Artifacts

### D1 — Requirements & Classification
- Requirements Traceability Matrix (RTM)
- Mode Assignment Register (MAR)
- Critical Boundary Declaration (CBD)

### D2 — Design & Architecture
- System Architecture Diagram
- Module/Class Dependency Map
- Mode Propagation Analysis
- Critical/Non-Critical Interaction Matrix

### D3 — Compliance Artifacts
- Rule Compliance Report (RCR)
- Deviation Register (if applicable)
- Static Analysis Logs

### D4 — Testing & Behavior
- Coverage Report (per Mode)
- Determinism Validation Report (Strict-A)
- Fault Injection Logs
- MC/DC Results (`@critical`, Strict-A only)

### D5 — Configuration Integrity
- Configuration Baseline Manifest (CBM)
- Reproducible Build Snapshot
- One-Version Python Confirmation
- Toolchain Version Registry

### D6 — Operational Readiness
- Watchdog Configuration
- Monitoring/Telemetry Policy
- Safe-State/Fallback Strategy

---

## 1.4 SCEM Completion Rules

A SCEM is considered **complete** only if:

- All artifacts exist
- All artifacts are versioned
- All artifacts trace to a single CBM
- No unresolved deviations exist
- Strict-A evidence is present (if applicable)

If any artifact is missing -> SCEM **INCOMPLETE** -> project cannot certify.

---

## 1.5 SCEM & Modes

| Mode      | SCEM Required | MC/DC Required | Determinism Proof Required |
|-----------|---------------|----------------|----------------------------|
| Core      | Recommended   | No             | No                         |
| Strict    | Mandatory     | No             | Only if safety-relevant    |
| Strict-A  | Mandatory     | Yes            | Yes                        |


Strict-A MUST include:

- Deterministic timing evidence
- Zero `@critical` violations
- Approved deviations for non-critical

---

## 1.6 Quantitative Verification Targets per Mode

This section defines **minimum quantitative verification targets** per Mode. Projects MAY exceed these targets; falling below them is only allowed if justified by an approved deviation in SCEM-D4 (Testing & Behavior).

### 1.6.1 Coverage Targets

**Strict-A (Level A):**

- Statement coverage: **≥ 100%** on all `@critical` code paths  
- Branch/decision coverage: **≥ 100%** on all `@critical` code paths  
- MC/DC coverage: **MANDATORY** on all Boolean decisions in `@critical` Strict-A code  
- For non-critical Strict-A code:  
  - Statement coverage ≥ 95%  
  - Branch coverage ≥ 90%  

**Strict (Level B/C):**

- Statement coverage: **≥ 95%** on safety-relevant modules  
- Branch/decision coverage: **≥ 90%** on safety-relevant modules  
- MC/DC coverage: strongly RECOMMENDED for Level B, not required for Level C  

**Core (all Levels):**

- Coverage targets defined by the project, but:  
  - Level A/B Core code SHOULD target ≥ 90% statement coverage.  

All coverage evidence is recorded in **TEP** and referenced from SCEM-D4.   

### 1.6.2 Robustness & Fault Injection

**Strict-A @critical:**

- Fault injection MUST be performed for:  
  - input boundary conditions,  
  - sensor / data loss scenarios,  
  - configuration corruption,  
  - out-of-range values.  
- Results MUST be recorded in TEP and referenced from SCEM-D4.  

**Strict (non-A):**

- Fault injection is REQUIRED for Level B safety-relevant modules.  
- At minimum, abnormal inputs and configuration errors MUST be exercised.  

**Core:**

- Fault injection is RECOMMENDED for Level A/B components, optional for Level C.  

### 1.6.3 Independence

For **Strict-A**:

- Verification of `@critical` code MUST be performed by an engineer or team **independent** from the original author.  
- Independence MUST be documented in SCEM-D3 (Compliance Artifacts) and in the Compliance Certificate (CC).   


# 2. SCEM Annexes (Consolidated)

The following annexes define **standard templates** for SCEM artifacts.

---

## Annex A — Mode Assignment Register (MAR)

**Purpose:** Record Mode (Profile × Level) for each function/method.

**Fields:**
- Identifier (file/class/function)
- Profile (Core/Strict)
- Safety Level (A/B/C)
- Mode
- Phase (`@critical` / `@non_critical_phase` / None)
- Dependencies
- Notes

Modes MUST NOT be downgraded after assignment.

---

## Annex B — Critical Boundary Declaration (CBD)

**Purpose:** Declare where critical execution begins and ends.

**Fields:**
- Function signature
- Phase annotation
- Preconditions
- Postconditions
- Allowed operations
- Forbidden operations

Critical code may **never** call non-critical code.

---

## Annex C — Mode Propagation Record

**Purpose:** Capture promotions triggered by the call chain.

**Fields:**
- Caller unit
- Callee unit
- Trigger type (data-flow / control-flow / polymorphism)
- New Mode
- Reviewer approval

Modes only **increase**.

---

## Annex D — Deviation Register

**Purpose:** Document Strict-A non-critical deviations.

**Fields:**
- Reference ID
- Mode
- Phase
- Rule violated
- Risk analysis summary
- Isolation proof
- Approval signature

Strict-A `@critical` deviations are **not permitted**.

---

## Annex E — Determinism Validation Checklist (Strict-A Only)

Confirms:

- No dynamic allocation
- No I/O
- No blocking waits
- GC disabled or proven safe
- Bounded execution

Failure -> Strict-A **BLOCKER**.

---

## Annex F — One-Version Python Confirmation

Confirms:

- Exactly one Python version used
- Version frozen in CBM
- No drift across build/deploy

Multiple versions -> **Automatic FAIL**.

---

# 3. Safety Maturity Model (SMM)

## 3.1 Purpose

The SMM defines organizational readiness to develop CRSS-compliant systems.

It answers:
> “Is the organization capable of producing safe Python software?”

The SMM assesses **process maturity**, not code correctness.

---

## 3.2 Levels

| Level | Name | Description |
|-------|------|-------------|
| **S0** | Ad-Hoc | No safety discipline |
| **S1** | Controlled | Basic rule awareness |
| **S2** | Managed | Formal compliance process |
| **S3** | Verified | Evidence-driven, audited compliance |
| **S4** | Certified | Capable of Strict-A certification & external audits |

---

## 3.3 Maturity Requirements

### S1 — Controlled
- Rules known
- Basic documentation

### S2 — Managed
- Formal compliance lifecycle
- SCEM mandatory for Strict

### S3 — Verified
- Independent review
- Full SCEM
- Mode tracking automated

### S4 — Certified
- Strict-A certification achieved
- Organization capable of:
  - MC/DC tooling
  - Determinism validation
  - Deviation governance

---

## 3.4 Maturity Assessment Output

- Maturity Level Statement
- Gap Analysis
- Improvement Plan

Organizations below **S2** may not attempt Strict-A projects.

---

# 4. Summary

This master document:

- Centralizes SCEM, Annexes, and Maturity Model
- Updates terminology to v3.0.0
- Enforces one-version-per-project
- Defines mandatory evidence for certification
- Establishes organizational readiness levels

This is the **foundation of the CRSS safety case** and must be referenced in all certification programs.

---