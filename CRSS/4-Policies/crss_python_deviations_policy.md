# CRSS-Python Deviation Policy

**Version:** v1.0.0
**Status:** Normative
**Maturity:** Stable
© 2025 Sofian Daghsen - All rights reserved
Distributed under CC BY-NC-ND 4.0 - see LICENSE-CRSS.

---

<a id="toc"></a>
## Table of Contents

- [CRSS-Python Deviation Policy](#crss-python-deviation-policy)
  - [1. Purpose](#1-purpose)
  - [2. Principles (Foundational)](#2-principles-foundational)
    - [2.1 Deviations Are NEVER Allowed for MUST and MUST-NOT](#21-deviations-are-never-allowed-for-must-and-must-not)
    - [2.2 Deviations Are NEVER Allowed Inside Strict-A @critical](#22-deviations-are-never-allowed-inside-strict-a-critical)
    - [2.3 Deviations Are Allowed Only for SHOULD and SHOULD-NOT](#23-deviations-are-allowed-only-for-should-and-should-not)
  - [3. Deviation Types (Formal)](#3-deviation-types-formal)
    - [3.1 RIC Rule Interpretation Clarification](#31-ric-rule-interpretation-clarification)
    - [3.2 CD Conditional Deviation](#32-cd-conditional-deviation)
    - [3.3 ED Exceptional Deviation](#33-ed-exceptional-deviation)
  - [4. Forbidden Deviations Categories](#4-forbidden-deviations-categories)
  - [5. Allowed Deviations Categories](#5-allowed-deviations-categories)
  - [6. Required Contents of a Deviation (DMR)](#6-required-contents-of-a-deviation-dmr)
    - [Identification](#identification)
    - [Technical Justification](#technical-justification)
    - [Risk Analysis](#risk-analysis)
    - [Compensating Safety Measures](#compensating-safety-measures)
    - [Evidence](#evidence)
    - [Approvals](#approvals)
    - [Traceability](#traceability)
  - [7. Deviation Matrix](#7-deviation-matrix)
  - [8. Scope Rules](#8-scope-rules)
  - [9. Integration With Mode Model](#9-integration-with-mode-model)
  - [10. Final Policy Statement (Normative)](#10-final-policy-statement-normative)
  - [11. Summary](#11-summary)

---

## 1. Purpose

> [⬆ Back to Table of Contents](#toc)


This document defines the formal deviation policy for the CRSS-Python Standard.
It provides:

- Allowed deviation types
- Forbidden deviations
- Deviation process
- Required deviation content
- Deviation classification matrix
- Relationship with Profiles, Modes, Safety Levels, and Phases

This specification is machine-parsable, auditor-ready, and aligned with
ASIL-D / SIL-3 supervisory safety expectations.

---

## 2. Principles (Foundational)

> [⬆ Back to Table of Contents](#toc)


### 2.1 Deviations Are NEVER Allowed for MUST / MUST-NOT

A CRSS rule of type:

- **MUST**
- **MUST NOT**

is *non-deviable*, meaning:

- No waiver
- No justification
- No conditional allowance

A violation of a MUST/MUST-NOT rule is **always non-compliant**.

---

### 2.2 Deviations Are NEVER Allowed Inside Strict-A @critical

Inside **Strict-Level-A + @critical phase**:

- No deviations permitted
- No exceptions
- No compensating measures

Strict-A critical code is a **zero-tolerance** zone.

---

### 2.3 Deviations Are Allowed Only for SHOULD and SHOULD-NOT

Valid deviation candidates must be rules of type:

- **SHOULD**
- **SHOULD NOT**

These represent strong guidance but can be deviated through a **controlled process**.

---

## 3. Deviation Types (Formal)

> [⬆ Back to Table of Contents](#toc)


### 3.1 RIC Rule Interpretation Clarification

Used when:

- No violation exists
- The rule text requires contextual clarification

**Approval:** Technical lead
**Risk analysis:** Not required

---

### 3.2 CD Conditional Deviation

Used when:

- A SHOULD / SHOULD-NOT rule is violated
- Risk impact is low
- Compensating conditions mitigate impact

**Approval:** Component Owner + Technical Lead
**Required:** Justification + Limited impact analysis

---

### 3.3 ED Exceptional Deviation

Used when:

- A SHOULD / SHOULD-NOT rule is violated
- Safety-impact exists
- Must introduce **Compensating Safety Mechanisms (CSM)**

**Approval:** Independent Safety Authority
**Requires:**
- Safety analysis
- SCEM update
- Verification evidence

This is the **highest severity** deviation.

---

## 4. Deviations - Forbidden Categories

> [⬆ Back to Table of Contents](#toc)


These rules can **NEVER** be deviated:

| Category | Reason |
|----------|--------|
| MUST / MUST-NOT rules | Non-negotiable safety requirements |
| Any rule inside Strict-A @critical | Zero tolerance |
| GC behavior rules | Determinism must be guaranteed |
| Determinism rules (loop bounds, recursion limits) | Safety timing |
| Race-condition prohibitions | Concurrency safety |
| I/O forbidden in @critical | Deterministic critical loops |
| Dynamic imports (Strict) | Non-analyzable |
| Monkeypatching (Strict) | Runtime mutation |
| eval/exec | Arbitrary code execution |
| Environment mutation rules | Platform integrity |
| Deployment integrity rules | Certification boundaries |

Violating any of these is always unsafe.

---

## 5. Deviations - Allowed Categories

> [⬆ Back to Table of Contents](#toc)


Permitted ONLY for SHOULD/SHOULD-NOT rules in:

- **Core A/B/C**
- **Strict B/C**
- **Strict-A non-critical only**
- Architectural exceptions
- Import exceptions
- Logging/monitoring exceptions (never in @critical)
- Performance-tuning exceptions
- Toolchain/analysis limitations
- Legacy refactors

Approval level depends on deviation type (RIC/CD/ED).

---

## 6. Required Contents of a Deviation (DMR)

> [⬆ Back to Table of Contents](#toc)


Every deviation MUST include:

### Identification
- Rule ID
- Rule text excerpt
- Deviation type: RIC / CD / ED
- Safety Level: A/B/C
- Profile: Core / Strict
- Phase: Critical / Non-critical
- Scope: line/function/class/module

### Technical Justification
- Why deviation is needed
- Why no compliant alternative exists
- Expected lifetime

### Risk Analysis
- Determinism impact
- Safety logic impact
- Resource usage impact
- External interface impact
- Hazard consequences
- Propagation impact

### Compensating Safety Measures
- Bounds
- Guards
- Validations
- Monitoring
- Containment

### Evidence
- Tests
- Static analysis
- Review notes

### Approvals
- Technical Lead
- Safety Lead
- Independent Safety Authority (ED only)

### Traceability
- SCEM linkage
- RCR linkage
- CBM linkage

---

## 7. Deviation Matrix

> [⬆ Back to Table of Contents](#toc)


A rule is evaluated by:

(Profile) × (Safety Level) × (Phase)

Example rows:

| Rule ID | Core A/B/C | Strict-A | Strict B/C | Phase | Allowed? | Deviation Type | Approval |
|---------|-------------|----------|------------|--------|----------|----------------|----------|
| CRSS-7.8.3 | YES | NO | CD | Critical | | - | - |
| CRSS-5.4.9 | YES | NO | YES | Non-Critical | Yes | CD | TL + SA |
| CRSS-6.4.4 | YES | ED | ED | Any | Yes | ED | ISA |

---

## 8. Scope Rules

> [⬆ Back to Table of Contents](#toc)


Deviations MUST specify:

- line range
- function/method
- class
- module/package
- phase (critical/non-critical)

**Unscoped deviations = forbidden.**

---

## 9. Integration With Mode Model

> [⬆ Back to Table of Contents](#toc)


| Mode | Deviation Allowed? |
|-------|---------------------|
| Core (A/B/C) | SHOULD rules only |
| Strict B/C | SHOULD rules only |
| Strict-A Non-Critical | SHOULD rules only (CD/ED required) |
| Strict-A Critical | NEVER |

---

## 10. Final Policy Statement (Normative)

> [⬆ Back to Table of Contents](#toc)


**Deviations are permitted ONLY for SHOULD / SHOULD-NOT rules,
NEVER for MUST / MUST-NOT rules,
and NEVER inside Strict-Level-A @critical code.**

Every deviation must include:

- justification
- bounded scope
- risk analysis
- traceability
- independent approval (for ED)

Unscoped/open-ended deviations are prohibited.

---

## 11. Summary

> [⬆ Back to Table of Contents](#toc)


This deviation model:

- Preserves strictness of MUST/MUST-NOT
- Protects Strict-A critical execution
- Allows safe, auditable flexibility
- Supports legacy constraints and real-world integration
- Is fully certifier-ready
- Enables automated tooling

This is the **normative deviation scheme for CRSS-Python v1.0.0*.
