# CRSS-Python Release Management Specification

**Version:** v1.0.0
**Status:** Normative
**Maturity:** Stable
© 2025 Sofian Daghsen – All rights reserved
Distributed under CC BY-NC-ND 4.0 — see LICENSE-CRSS.

---

## Table of Contents

- [CRSS-Python Release Management Specification](#crss-python-release-management-specification)
  - [0. Purpose](#0-purpose)
  - [1. Definition of a Release](#1-definition-of-a-release)
    - [**CRSS Definition**](#crss-definition)
  - [2. Required Properties of a Release](#2-required-properties-of-a-release)
    - [2.1 Uniquely Identifiable](#21-uniquely-identifiable)
    - [2.2 Immutable](#22-immutable)
    - [2.3 Reproducible](#23-reproducible)
    - [2.4 Tested](#24-tested)
    - [2.5 Approved](#25-approved)
    - [2.6 Deployable](#26-deployable)
  - [3. Release Contents](#3-release-contents)
  - [4. Distinction Between Build, Baseline, and Release](#4-distinction-between-build-baseline-and-release)
  - [5. Release Versioning Rules](#5-release-versioning-rules)
    - [**CRSS-13.1 – Unique Versioning**](#crss-131-unique-versioning)
    - [**CRSS-13.2 – Single Unit Principle**](#crss-132-single-unit-principle)
    - [**CRSS-13.3 – Supersession**](#crss-133-supersession)
  - [6. Release Lifecycle](#6-release-lifecycle)
    - [6.1 Stages](#61-stages)
    - [6.2 State Transitions](#62-state-transitions)
  - [7. Release Registry Policy](#7-release-registry-policy)
  - [8. Release Deployment Rules](#8-release-deployment-rules)
    - [8.1 Deployment Eligibility](#81-deployment-eligibility)
    - [8.2 Deployment Prohibition](#82-deployment-prohibition)
    - [8.3 Production Environment Rule](#83-production-environment-rule)
  - [9. Release Modification](#9-release-modification)
    - [9.1 Zero Modification](#91-zero-modification)
    - [9.2 Change Requires New Release](#92-change-requires-new-release)
  - [10. Release Approval Authority](#10-release-approval-authority)
  - [11. Summary](#11-summary)

---

## 0. Purpose

This document defines the mandatory requirements, definitions, processes, rules, and artifacts governing **Release Management** under the CRSS-Python standard.

It acts as an official annex to the **CRSS-Python Configuration & Deployment Integrity Policy** and ensures that:

- Releases are unambiguous and formally defined
- Releases are immutable, traceable, and certifiable
- Releases are the only deployable units for Production
- Release changes are controlled through new baselines
- Release artifacts remain complete and intact for the system lifecycle

This specification is **non-deviable** for Strict Level A components.

---

## 1. Definition of a Release

### **CRSS Definition**
A **Release** is:

> **The uniquely identified, immutable, approved, and deployable software unit consisting of a build artifact and its complete Safety Baseline, created through the CRSS Compliance Process and authorized for Production deployment.**

A Release is:
- A certified software package
- A frozen configuration state
- A deployable unit
- A traceable artifact set
- A compliance boundary

A Release is **not**:
- A build artifact alone
- A Git tag or branch alone
- A CI pipeline output
- A mutable test version

A Release exists **only after** Compliance Certification.

---

## 2. Required Properties of a Release

A Release MUST be:

### 2.1 Uniquely Identifiable
Each Release SHALL have:
- Release ID
- Baseline ID
- Commit Hash
- Version Number

### 2.2 Immutable
Once approved:
- A Release SHALL NOT be modified
- Any change SHALL create a new Release

### 2.3 Reproducible
A Release MUST be rebuildable using only:
- The Reproducible Build Snapshot
- The Safety Baseline
- The Release Artifact Set

### 2.4 Tested
A Release MUST include:
- Test Evidence Package (TEP)
- Coverage reports
- Fault injection results (Level A)
- Reliability results (Level A)

### 2.5 Approved
A Release MUST:
- Complete all Compliance Process phases
- Receive a signed Compliance Certificate (CC)
- Be approved by an independent authority

### 2.6 Deployable
Only Releases may be deployed to Production.

---

## 3. Release Contents

A Release SHALL consist of the following minimum components:

| Component | Source |
|----------|--------|
| Build Artifact | Derived from source repo |
| Source Code Archive | Version-controlled |
| Configuration Baseline Manifest (CBM) | Phase 4 |
| Safety Baseline Report (SBR) | Phase 4 |
| Rule Compliance Report (RCR) | Phase 2 |
| Test Evidence Package (TEP) | Phase 3 |
| Reproducible Build Snapshot | Phase 4 |
| Compliance Certificate (CC) | Phase 5 |

If **any** required component is missing:
- The Release is **invalid**
- The Release is **non-compliant**
- The Release **shall not** be deployed

---

## 4. Distinction Between Build, Baseline, and Release

| Concept | Defines | Mutable? | Deployable? | Certified? |
|--------|---------|----------|-------------|------------|
| **Build** | Compiled artifact | Yes |  No |  No |
| **Baseline** | Frozen configuration state |  Changes create new baseline |  No |  No |
| **Release** | Certified deployment unit |  No |  Yes |  Yes |

Therefore:
- Builds → many
- Baselines → fewer
- Releases → fewest

A Release is the **final authorized output**.

---

## 5. Release Versioning Rules

### **CRSS-13.1 – Unique Versioning**
- Every Release SHALL have a unique version number.
- Version numbers SHALL NOT be reused.
- Releases SHALL NOT be modified after approval.

### **CRSS-13.2 – Single Unit Principle**
A Release SHALL be treated as **one indivisible unit**:
- All components must share the same Release ID
- All components must share the same Baseline ID
- All components must reference the same Commit Hash

### **CRSS-13.3 – Supersession**
A new Release:
- Does NOT modify or delete previous Releases
- Becomes the sole Production-authorized version
- Coexists in long-term archival storage

---

## 6. Release Lifecycle

### 6.1 Stages
1. **Candidate Build** (DEV)
2. **Baseline Candidate** (TEST)
3. **Compliance Complete**
4. **Certified Release**
5. **Production Deployment**

### 6.2 State Transitions

```
DEV Build → Baseline Candidate → Release → Production Deployment
```

Transition rules:
- DEV → TEST: pinned build required
- TEST → RELEASE: only after CC approval
- RELEASE → PROD: only approved Release may be deployed

---

## 7. Release Registry Policy

A Release MUST be stored in a **controlled Release Registry** with:

- Restricted write access
- Cryptographic integrity checks
- Permanent retention
- Version history
- Baseline linkage

No Release may be deleted or overwritten.

---

## 8. Release Deployment Rules

### 8.1 Deployment Eligibility
A Release is deployable ONLY IF:
- It is fully certified
- It matches the CBM exactly

### 8.2 Deployment Prohibition
The following SHALL NOT be deployed:
- Builds
- Candidates
- Snapshots
- Branches
- Uncertified versions

### 8.3 Production Environment Rule
Production SHALL execute **only one Release at a time** unless redundancy architecture explicitly requires multiple nodes of the **same Release**.

---

## 9. Release Modification

### 9.1 Zero Modification
Releases SHALL NOT be:
- Patched
- Hotfixed
- Rebuilt
- Reconfigured

### 9.2 Change Requires New Release
Any change to:
- Code
- Dependencies
- Interpreter
- OS
- Build process
- Infrastructure
- Configuration
- Test suite

**Invalidates the Release** and requires:
- New Baseline
- New Compliance Process
- New Release

There is no partial acceptance.

---

## 10. Release Approval Authority

A Release MUST be:
- Reviewed
- Validated
- Approved
- Signed

by an **Independent Assessor** with no modification authority.

Developers and CI/CD systems **cannot self-approve** Releases.

---

## 11. Summary

A Release is:
- Immutable
- Traceable
- Reproducible
- Fully Tested
- Independently Approved
- The ONLY deployable unit

This specification ensures Releases are safe, auditable, and certifiable for
**ASIL D / SIL 3 supervisory environments**.
