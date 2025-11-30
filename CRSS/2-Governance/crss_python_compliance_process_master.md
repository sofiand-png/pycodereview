# CRSS-Python Compliance Process Specification

**Version:** v1.0.0
**Status:** Normative
**Maturity:** Stable
© 2025 Sofian Daghsen – All rights reserved
Distributed under CC BY-NC-ND 4.0 — see LICENSE-CRSS.

---

## Table of Contents

- [CRSS-Python Compliance Process Specification](#crss-python-compliance-process-specification)
  - [0. Purpose](#0-purpose)
  - [1. Scope](#1-scope)
  - [2. Compliance Phases](#2-compliance-phases)
    - [2.1 Phase 1 — Requirements & Traceability Setup](#21-phase-1-requirements-traceability-setup)
    - [2.2 Phase 2 — Static Rule Compliance](#22-phase-2-static-rule-compliance)
    - [2.3 Phase 3 — Test & Coverage Compliance](#23-phase-3-test-coverage-compliance)
    - [2.4 Phase 4 — Baseline Establishment](#24-phase-4-baseline-establishment)
    - [2.5 Phase 5 — Independent Approval & Release](#25-phase-5-independent-approval-release)
  - [3. Compliance Completion Criteria](#3-compliance-completion-criteria)
  - [4. Roles & Responsibilities](#4-roles-responsibilities)
    - [4.1 Development Team](#41-development-team)
    - [4.2 Independent Assessor](#42-independent-assessor)
    - [4.3 Configuration Authority](#43-configuration-authority)
  - [5. Artifact Summary Table](#5-artifact-summary-table)
  - [6. Re-Approval Rules](#6-re-approval-rules)
  - [8. Mandatory Artifacts Definition](#8-mandatory-artifacts-definition)
  - [8. Archival Rules](#8-archival-rules)
  - [9. Summary](#9-summary)

---

## 0. Purpose
This document defines the **mandatory Compliance Process** required for any project claiming CRSS-Python compliance.
Compliance is **not achieved** by rule adoption alone — only by completion of this process and generation of required artifacts.

---

## 1. Scope
This specification applies to:
- All CRSS-Strict projects
- All Level A, B, and C components
- All software releases intended for deployment

It is **non-deviable** for Strict Level A components.

---

## 2. Compliance Phases

### 2.1 Phase 1 — Requirements & Traceability Setup
**Objectives**
- Define functional & safety requirements
- Assign criticality levels (A/B/C)
- Map requirements to code modules

**Mandatory Outputs**
- Requirements Traceability Matrix (RTM)
- Criticality Classification Record (CCR)

---

### 2.2 Phase 2 — Static Rule Compliance
**Objectives**
- Verify conformance to CRSS-Core/Strict
- Identify deviations

**Mandatory Outputs**
- Rule Compliance Report (RCR)
- Deviations Log (DL)

---

### 2.3 Phase 3 — Test & Coverage Compliance
**Objectives**
- Validate correctness, safety, and robustness
- Achieve:
  - 100% branch coverage (Strict)
  - MC/DC (Level A only)

**Mandatory Outputs**
- Test Evidence Package (TEP)
- Coverage Reports
- Fault Injection Results

---

### 2.4 Phase 4 — Baseline Establishment
**Objectives**
- Freeze all configuration elements
- Create an immutable Safety Baseline

**Mandatory Outputs**
- Configuration Baseline Manifest (CBM)
- Safety Baseline Report (SBR)

---

### 2.5 Phase 5 — Independent Approval & Release
**Objectives**
- Obtain independent sign-off
- Archive all artifacts

**Mandatory Outputs**
- Compliance Certificate (CC)

---

## 3. Compliance Completion Criteria
A project is considered **COMPLIANT** only when:
1. All phases are completed
2. All artifacts are present
3. All artifacts share the same Baseline ID
4. The CC is issued and signed

Partial compliance is invalid.

---

## 4. Roles & Responsibilities

### 4.1 Development Team
- Executes Phases 1–4
- Produces all artifacts

### 4.2 Independent Assessor
- Executes Phase 5
- Reviews evidence
- Signs Compliance Certificate

### 4.3 Configuration Authority
- Maintains baseline archive
- Controls changes and access

---

## 5. Artifact Summary Table

| Artifact | Producer | Phase | Mandatory Level |
|---------|----------|-------|------------------|
| RTM | Dev Team | 1 | A/B/C |
| CCR | Dev Team | 1 | A/B/C |
| RCR | Dev Team | 2 | A/B/C |
| DL | Dev Team | 2 | A/B/C |
| TEP | Dev Team | 3 | A/B/C |
| CBM | Dev Team | 4 | A/B/C |
| SBR | Dev Team | 4 | A/B/C |
| CC | Assessor | 5 | A/B/C |

---

## 6. Re-Approval Rules
Any change to:
- Code
- Dependencies
- Interpreter
- OS
- Hardware
- Test suite

**Invalidates compliance.**

Full process restart is required.

---
## 8. Mandatory Artifacts Definition
Mandatory Artifact Definitions
A. Rule Compliance Report (RCR)

Required Fields:
- Release ID
- Baseline ID
- Commit hash
- List of applicable rules
- Pass/Fail status per rule
- Deviations list with approvals
- Reviewer identity & timestamp

Must reference: RTM, CBM

B. Test Evidence Package (TEP)

Required Contents:
- Test suite version
- Platform matrix results
- Coverage reports (including MC/DC when Level A)
- Fault injection results
- Reliability test results
- Performance benchmarks
- Test artifacts (logs, traces)

Must reference: RCR, CBM

C. Configuration Baseline Manifest (CBM)

Required Contents:
- Interpreter version
- OS version & kernel
- Container/VM images
- Dependency manifest (exact versions)
- Hardware specs
- Build flags & configs
- Environment variables
- Hashes/checksums

Must reference: RCR, TEP

D. Compliance Certificate (CC)

Required Elements:
- Statement of compliance
- Release ID
- Baseline ID
- List of artifacts included
- Approval signature by independent authority
- Expiry/validity conditions

Must reference: RCR, TEP, CBM, SBR

E. Safety Baseline Report (SBR)

Required Elements:

Full baseline definition
- Safety level (ASIL/SIL/Class)
- Criticality mapping
- Hazard impact summary
- Residual risk assessment
- Configuration matrix
-Deployment context

Must reference: ALL artifacts

3. Artifact Relationship Model
           ┌─────────┐
           │  RCR    │
           └────┬────┘
                │
           ┌────▼────┐
           │   TEP   │
           └────┬────┘
                │
           ┌────▼────┐
           │   CBM   │
           └────┬────┘
                │
           ┌────▼────┐
           │   SBR   │
           └────┬────┘
                │
           ┌────▼────┐
           │   CC    │
           └─────────┘

All five share the same:
- Release ID
- Baseline ID
- Commit hash TODO: check if this is possible ?

They form a single versioned unit.

---

## 8. Archival Rules
All artifacts must be:
- Versioned
- Stored together
- Cryptographically hashed
- Retained for 15+ years (Level A recommended)

---

## 9. Summary
Compliance is not a declaration — it is a **process**.
Only by executing this process and producing all required artifacts can a project claim CRSS compliance.
