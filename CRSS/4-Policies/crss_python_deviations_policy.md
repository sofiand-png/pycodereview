# CRSS-Python Deviation Policy

**Version:** v1.0.0  
**Status:** Normative  
**Maturity:** Stable  
© 2025 Sofian Daghsen - All rights reserved  
Distributed under CC BY-NC-ND 4.0 - see LICENSE-CRSS.

---

## Table of Contents

- [1. Purpose](#1-purpose)
- [2. Principles (Foundational)](#2-principles-foundational)
- [3. Deviation Types (Formal)](#3-deviation-types-formal)
- [4. Forbidden Deviations Categories](#4-forbidden-deviations-categories)
- [5. Allowed Deviations Categories](#5-allowed-deviations-categories)
- [6. Required Contents of a Deviation (DMR)](#6-required-contents-of-a-deviation-dmr)
- [7. Scope Rules](#7-scope-rules)
- [8. Integration With Mode Model](#8-integration-with-mode-model)
- [9. Final Policy Statement](#9-final-policy-statement)
- [10. Summary](#10-summary)

---

## 1. Purpose

This document defines the formal deviation policy for the CRSS-Python Standard.
It establishes:

- Which rules are non-deviable
- Which rules may be deviated under controlled conditions
- How deviations are classified, justified, reviewed, and traced
- How deviations integrate with RCR, SCEM, and EAP

This policy is aligned with CRSS v1.x, the Compliance Process, and the External Assessment Protocol.

---

## 2. Principles (Foundational)

### 2.1 MUST and MUST-NOT Rules

Rules classified as **MUST** or **MUST-NOT** are **non-deviable**.

- Violations SHALL be recorded in the Rule Compliance Report (RCR)
- Any such violation results in a **NOT CERTIFIED** outcome
- No waiver, justification, or compensating measure is permitted

---

### 2.2 Strict-A @critical Execution

Within **Strict-A @critical execution paths**:

- No deviations are permitted
- No compensating measures are allowed **within the critical path**
- Remediation may only occur via architectural refactoring or boundary redesign

---

### 2.3 SHOULD and SHOULD-NOT Rules

Only rules classified as **SHOULD** or **SHOULD-NOT** may be deviated, and only through the formal deviation process defined herein.

All deviations MUST be:
- Explicitly documented
- Bounded in scope
- Assessed for risk
- Recorded in the RCR

---

## 3. Deviation Types (Formal)

All deviations SHALL be recorded in the Rule Compliance Report (RCR) and assessed through the External Assessment Protocol (EAP).

### 3.1 RIC Rule Interpretation Clarification

Used when:
- No actual violation exists
- Rule intent requires contextual clarification

Approval: Technical Lead  
Risk analysis: Not required

---

### 3.2 CD Conditional Deviation

Used when:
- A SHOULD / SHOULD-NOT rule is violated
- Risk impact is low
- Compensating conditions mitigate impact

Approval: Component Owner + Technical Lead

---

### 3.3 ED Exceptional Deviation

Used when:
- A SHOULD / SHOULD-NOT rule is violated
- Safety impact exists

Requires:
- Formal safety analysis
- Compensating safety mechanisms outside critical paths
- SCEM update

Approval: Independent Safety Authority

---

## 4. Forbidden Deviations Categories

The following deviations are never permitted:

| Category | Reason |
|--------|--------|
| MUST / MUST-NOT rules | Non-negotiable safety requirements |
| Strict-A @critical logic | Zero-tolerance execution zone |
| Unbounded memory effects in @critical | Determinism violation |
| Unbounded loops / recursion | Timing unpredictability |
| Race conditions | Concurrency safety |
| I/O in @critical | Deterministic execution |
| Dynamic imports in Strict | Non-analyzable behavior |
| Monkeypatching | Runtime mutation |
| eval / exec | Arbitrary code execution |
| Deployment integrity rules | Certification boundary violation |

---

## 5. Allowed Deviations Categories

Permitted ONLY for SHOULD / SHOULD-NOT rules in:

- Core modes (A/B/C)
- Strict-B / Strict-C
- Strict-A non-critical only

Typical cases:
- Architectural constraints
- Legacy integration
- Tooling limitations
- Performance tuning (non-critical)

---

## 6. Required Contents of a Deviation (DMR)

Every deviation MUST include:

### Identification
- Rule ID
- Deviation type (RIC / CD / ED)
- Mode (e.g., Strict-A)
- Phase (critical / non-critical)
- Exact scope

### Technical Justification
- Rationale
- Why no compliant alternative exists
- Expected lifetime

### Risk Analysis
- Determinism impact
- Safety impact
- Propagation analysis

### Compensating Measures (if applicable)
- Guards
- Validation
- Monitoring

### Evidence
- Tests
- Reviews
- Analysis

### Approvals
- Required signatories per deviation type

### Traceability
- RCR reference
- SCEM reference
- CBM reference

---

## 7. Scope Rules

Deviations MUST be explicitly scoped.

Unscoped or open-ended deviations are forbidden.

---

## 8. Integration With Mode Model

| Mode | Deviations Allowed |
|------|-------------------|
| Core-A/B/C | SHOULD only |
| Strict-B/C | SHOULD only |
| Strict-A Non-Critical | SHOULD only |
| Strict-A Critical | NEVER |

---

## 9. Final Policy Statement

Deviations are permitted ONLY for SHOULD / SHOULD-NOT rules,
NEVER for MUST / MUST-NOT rules,
and NEVER within Strict-A @critical execution paths.

All deviations must be documented, justified, bounded, traceable, and approved.

---

## 10. Summary

This deviation policy:
- Preserves strict safety guarantees
- Aligns with RCR and EAP
- Supports real-world constraints
- Is structured to support automated tooling
