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
  - [12. Summary](#11-summary)

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

## 11. Certified Build and Packaging Process

### 11.1 Purpose and Scope

This section defines the mandatory process by which a CRSS-compliant project SHALL produce a certified software package, including:

- dependency freezing and locking,
- offline, deterministic installation,
- generation of immutable build artifacts,
- and collection of certification evidence.

This process applies to all projects claiming CRSS compliance at any Safety Level.

---

### 11.2 Conceptual Model

CRSS distinguishes between two fundamentally different activities:

- Dependency Freeze Operations
- Certified Builds

These activities MUST be logically and operationally separated.

| Activity | Internet Access | Purpose |
|---------|-----------------|---------|
| Dependency Freeze | Allowed (controlled) | Produce frozen dependency baseline |
| Certified Build | Forbidden | Produce certifiable software artifact |

This separation enforces TPL-2 (No Implicit Online Resolution) and ensures reproducibility.

---

### 11.3 Dependency Freeze Operation (Normative)

A Dependency Freeze Operation is a controlled maintenance action whose goal is to produce a frozen dependency baseline.

#### 11.3.1 Inputs

- `requirements.txt`, or equivalent manifests
- Approved package sources (internal mirror or PyPI during freeze only)

#### 11.3.2 Mandatory Outputs

The freeze operation SHALL produce:

- `requirements.lock.txt`  
  Fully pinned dependency list (exact versions).

- A platform-specific wheelhouse, for example:
  - `third_party/wheelhouse/linux/`
  - `third_party/wheelhouse/windows/`

- A cryptographic manifest:
  - `wheelhouse_manifest_<platform>.sha256.txt`

#### 11.3.3 Constraints

- Only binary distributions (`.whl`) SHALL be used.
- Source builds during freeze SHOULD be avoided.
- The freeze operation MUST be auditable and repeatable.

#### 11.3.4 Status

Freeze operations:

- MAY be manual,
- MAY be CI-driven,
- MUST NOT be considered certification builds.

---

### 11.4 Certified Build (Normative)

A Certified Build is the authoritative process that produces the certified software artifact.
#### 11.4.1 Certified Build Definition

A Certified Build is a build execution that satisfies all of the following
conditions:

1. All third-party dependencies are installed exclusively from a frozen,
   version-pinned, offline dependency baseline (TPL-1, TPL-2).
2. No implicit online dependency resolution occurs at build, test, or packaging time.
3. The software is packaged into an immutable, versioned artifact
   (e.g. Python wheel).
4. All verification activities (tests, coverage, robustness checks) are executed
   against the packaged artifact or an installation thereof.
5. All build outputs and evidence are recorded in the Configuration Baseline
   Manifest (CBM) and Test Evidence Package (TEP).

A Certified Build represents the authoritative technical basis for CRSS
certification claims and SHALL be the build referenced by SCEM and CRC artifacts.


#### 11.4.2 Network Policy

During a certified build:

- No public internet access is permitted.
- Package installation MUST use:
  - `--no-index`
  - pre-frozen wheelhouse only

Any violation SHALL be treated as hard non-compliance.

#### 11.4.3 Certified Build Steps (Required Order)

A certified build SHALL execute the following steps in order:

#### Step 1 — Offline Dependency Installation

Dependencies MUST be installed exclusively from the frozen wheelhouse:

```bash
python -m pip install --no-index   --find-links third_party/wheelhouse/<platform>   -r third_party/requirements.lock.txt
```

This step SHALL fail if any dependency is missing.

#### Step 2 — Certified Wheel Generation

The project SHALL be packaged into an immutable wheel artifact:

```bash
python -m pip wheel . --no-deps -w certified/wheels
```

Rules:

- Editable installs (`-e`) are NOT allowed.
- Dependency resolution is NOT allowed during packaging.
- The wheel SHALL represent the exact certified software unit.

#### Step 3 — Offline Installation of Certified Artifact

The certified wheel SHALL be installed offline to verify installability:

```bash
python -m pip install --no-index certified/wheels/<project>-*.whl
```

This confirms:

- no hidden dependencies,
- no implicit resolution,
- correct packaging metadata.

#### Step 4 — Verification and Testing

All verification activities SHALL be executed against the installed wheel, including:

- unit tests,
- integration tests,
- coverage measurement,
- robustness / fault injection tests (if applicable).

---

### 11.5 Certified Build Outputs (Normative)

A certified build SHALL produce a Certified Build Package containing:

```text
certified/
  wheels/
    <project>-<version>-py3-none-any.whl
  evidence/
    coverage.xml
    wheel_manifest.sha256.txt
    tool_versions.txt
```

#### 11.5.1 Mandatory Evidence

- Certified wheel (primary deliverable)
- Wheel hash manifest (immutability proof)
- Coverage report
- Tool version record

These artifacts SHALL be referenced in:

- CBM (Configuration Baseline Manifest),
- TEP (Test Evidence Package),
- CRC (Certification Readiness Checklist).

---

### 11.6 Packaging Rules and CRSS Implications

Projects claiming CRSS compliance SHALL observe the following packaging rules:

- Packaging MUST be deterministic.
- `setup.py` / `pyproject.toml` MUST:
  - declare all runtime dependencies explicitly,
  - avoid dynamic dependency computation.

The resulting wheel MUST:

- be installable offline,
- not execute network operations at install time,
- not rely on editable source layouts.

For pure-Python CRSS projects, wheels SHOULD use the `py3-none-any` tag where possible.

---

### 11.7 Platform-Specific Certification Baselines

CRSS permits platform-specific certified builds.

- Dependency wheelhouses MAY differ per platform.
- Certified wheels MAY be generated per platform, even if functionally identical.
- Each certified build SHALL maintain its own evidence and hash manifests.
- Platform-specific certification SHALL be treated as distinct certification baselines.

---

### 11.8 Relationship to Other CRSS Artifacts

| Artifact | Role |
|---------|------|
| CBM | Records certified wheel + dependency baseline |
| SCEM | Explains certification argument |
| TEP | Holds test and coverage evidence |
| CRC | Final readiness decision |


## 12. Summary

A Release is:
- Immutable
- Traceable
- Reproducible
- Fully Tested
- Independently Approved
- The ONLY deployable unit

This specification ensures Releases are safe, auditable, and certifiable for
**ASIL D / SIL 3 supervisory environments**.
