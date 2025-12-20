# CRSS-Python Deployment, Release and Baseline Master Specification

**Version:** v1.0.0
**Status:** Normative
**Maturity:** Stable
© 2025 Sofian Daghsen - All rights reserved
Distributed under CC BY-NC-ND 4.0 - see LICENSE-CRSS.

---

<a id="toc"></a>
## Table of Contents
- [CRSS-Python Deployment, Release and Baseline Master Specification](#crss-python-deployment-release-baseline-master-specification)
  - [Table of Contents](#table-of-contents)
  - [0. Purpose](#0-purpose)
  - [1. Deployment and Baseline Rule Catalog](#1-deployment-and-baseline-rule-catalog)
    - [1.1 Environment and Immutability](#11-environment-and-immutability)
    - [1.2 Baseline and CBM](#12-baseline-and-cbm)
    - [1.3 Releases and Immutability](#13-releases-and-immutability)
    - [1.4 Updates and Upgrade Process](#14-updates-and-upgrade-process)
    - [1.5 CI/CD and Deployment Pipeline](#15-cicd-and-deployment-pipeline)
    - [1.6 Environment Parity and Testing](#16-environment-parity-and-testing)
    - [1.7 Production Safeguards](#17-production-safeguards)
  - [1.8 Upgrade process](#18-upgrade-process)
  - [2. Relationship to Code-Level 12.x Rules](#2-relationship-to-code-level-12x-rules)
  - [3. Versioning and Governance](#3-versioning-and-governance)
  - [4. Summary](#4-summary)

---

## 0. Purpose

> [⬆ Back to Table of Contents](#toc)


This master specification defines **how CRSS-Python projects are deployed, released, versioned, and baselined**.

It consolidates and supersedes:

- CRSS-Python Deployment Policy
- CRSS-Python Release Management Specification
- CRSS-Python CBM (Configuration Baseline Manifest) Guide

It is **normative** for all projects claiming CRSS-Python compliance (Core or Strict).
All MUST / MUST-NOT / SHOULD / SHOULD-NOT statements in this document are identified by **DPL-12.x** IDs.

CRSS deliberately separates architectural safety rules from release and build governance.

The authoritative, normative definition of how a CRSS-compliant software artifact is produced - including dependency freezing, 
offline installation, wheel generation, and evidence collection - is specified in the Release Management and Deployment Policy.

The whitepaper does not re-define these procedures. Instead, it relies on the Release Management specification as the single source of truth for:

Dependency freezing and lockfile generation

Offline, deterministic installation

Certified wheel creation

Artifact immutability and cryptographic hashing

Evidence integration into CBM, TEP, and CRC

This separation ensures that conceptual guidance remains stable while allowing build and release processes to evolve in a controlled, auditable manner.

---

## 1. Deployment and Baseline Rule Catalog

> [⬆ Back to Table of Contents](#toc)


This section defines the **canonical deployment, release, and baseline rules**.

Each rule has:

- **Category** - thematic grouping
- **Type** - Process / Configuration / Governance
- **Profiles** - obligations per profile
- **Scope** - optional rule application scope
- **Explanation** - intent and usage

### 1.1 Environment and Immutability

**DPL-12.1 - Immutable Production Deployment**
- **Category**: Deployment Environment
- **Type**: Process
- **Profiles**:
  - Core: MUST
  - Strict: MUST

Production deployments SHALL be **immutable**. After deployment, no code, dependencies, containers, or system libraries may be modified in place. Any change requires a **new build**, a **new CBM**, and a **new release**.

---

**DPL-12.2 - Zero-Drift Environment Enforcement**
- **Category**: Deployment Environment
- **Type**: Process
- **Profiles**:
  - Core: MUST
  - Strict: MUST

Runtime environments (TEST, PRE-PROD, PROD) MUST NOT drift from their recorded configuration. Any drift (package version change, OS update, container change, configuration change) SHALL invalidate deployment compliance until a new baseline is established.

---

**DPL-12.3 - One-Version-Per-Project Deployment Rule**
- **Category**: Versioning
- **Type**: Governance
- **Profiles**:
  - Core: MUST
  - Strict: MUST

Each project SHALL select exactly **one Python interpreter version** for its certified baseline deployment. Supporting additional Python versions constitutes a **separate project** and requires its own CBM, testing, and certification.

---

**DPL-12.4 - Runtime Package Installation Prohibition**
- **Category**: Dependencies
- **Type**: Process
- **Profiles**:
  - Core: MUST-NOT
  - Strict: MUST-NOT

Production environments MUST NOT install, upgrade, or remove Python packages at runtime (e.g. via `pip install` on a live system). All dependencies SHALL be frozen and defined in the CBM and built into the deployment artifact.

---

### 1.2 Baseline and CBM

**DPL-12.5 - Certified Baseline Requirement for Deployment**
- **Category**: Baseline and CBM
- **Type**: Governance
- **Profiles**:
  - Core: MUST
  - Strict: MUST

Every production deployment SHALL be based on a **certified baseline**, consisting of:

- a tagged source code revision,
- a single Python version,
- a dependency lock (requirements file or equivalent),
- a CBM describing environment and tools, and
- a valid Compliance Certificate for that baseline.

Deploying without a certified baseline is forbidden.

---

**DPL-12.6 - Deployment = Tested Configuration Only**
- **Category**: Baseline and CBM
- **Type**: Process
- **Profiles**:
  - Core: MUST
  - Strict: MUST

The configuration deployed to production MUST match a configuration **that has been tested and approved**. Deploying a configuration that differs from all tested configurations (e.g., changed OS, changed Python version, changed dependency versions) is prohibited.

---

**DPL-12.7 - PROD Must Match CBM Identically**
- **Category**: Baseline and CBM
- **Type**: Configuration
- **Profiles**:
  - Core: MUST
  - Strict: MUST

Before deployment, the target production environment SHALL be checked against the CBM. Interpreter version, OS version, container image, dependency versions, and tool versions MUST match the CBM exactly. Any discrepancy SHALL block deployment.

---

**DPL-12.8 - CBM Completeness and Traceability**
- **Category**: Baseline and CBM
- **Type**: Configuration
- **Profiles**:
  - Core: MUST
  - Strict: MUST

The CBM MUST include, at minimum:

- source commit hash / tag
- Python interpreter version
- all dependencies with exact versions
- OS distribution and version
- container/VM image identifiers
- build flags and options
- test tools and versions
- hardware / platform characteristics (CPU, RAM, storage, network bounds)

The CBM SHALL be stored alongside test artifacts and Compliance Certificates.

---

### 1.3 Releases and Immutability

**DPL-12.9 - Release Immutability Mandated**
- **Category**: Release Management
- **Type**: Governance
- **Profiles**:
  - Core: MUST
  - Strict: MUST

Each release SHALL be uniquely identified (e.g. semantic version + build number) and mapped to a single CBM. Once published, a release artifact MUST NOT be modified or overwritten. Corrections require a **new release**.

---

**DPL-12.10 - No Hotfixes in Place**
- **Category**: Release Management
- **Type**: Process
- **Profiles**:
  - Core: MUST-NOT
  - Strict: MUST-NOT

Applying hotfixes directly to running production systems (e.g. editing code on the server, patching containers in place) is forbidden. All fixes SHALL go through a full build, test, CBM update, and release process.

---

**DPL-12.11 - Release Registry and Audit Trail**
- **Category**: Release Management
- **Type**: Governance
- **Profiles**:
  - Core: SHOULD
  - Strict: MUST

Organizations SHOULD (Core) and MUST (Strict) maintain a **release registry** that records:

- release identifier
- associated CBM id
- date/time of deployment
- target environment(s)
- responsible approvers

The registry MUST be immutable and auditable.

---

### 1.4 Updates and Upgrade Process

**DPL-12.12 - Controlled Upgrade Process**
- **Category**: Updates and Upgrades
- **Type**: Process
- **Profiles**:
  - Core: MUST
  - Strict: MUST

All changes to a deployed system (code, dependencies, configuration, Python version, OS version, container image) MUST follow a **controlled upgrade process** including:

1. change proposal / RFC,
2. impact analysis (safety, performance, compatibility),
3. updated tests and SCEM where required,
4. creation of a new CBM, and
5. updated Compliance Certificate before deployment.

---

**DPL-12.13 - Automated Updates Forbidden in PROD**
- **Category**: Updates and Upgrades
- **Type**: Configuration
- **Profiles**:
  - Core: MUST-NOT
  - Strict: MUST-NOT

Automatic updates in production (e.g. OS unattended upgrades, package auto-updates, container auto-pulls) MUST be disabled. Updates SHALL occur only as part of the controlled upgrade process.

---

**DPL-12.14.1 - Rollback Strategy Required**
- **Category**: Updates and Upgrades
- **Type**: Process
- **Profiles**:
  - Core: SHOULD
  - Strict: MUST

Each release MUST define a rollback strategy that enables restoration to the previous certified baseline if deployment fails or critical issues are discovered. Rollbacks SHALL use CBM-backed, versioned artifacts, not manual patching.

---

**DPL-12.14.2 Rollback as First-Class Design Concern**
- **Category**: Rollback Strategy
- **Type**: Governance
- **Profiles**:
  - Core: SHOULD
  - Strict: MUST

The rollback strategy SHALL be defined during **architecture and design**, not improvised after implementation. It MUST address:

- what can be rolled back (code, config, data, infra),
- how quickly rollback can be executed,
- how safety-related behavior is preserved during and after rollback.

The strategy SHALL be referenced in SCEM and in the Deployment/Release Master.

**DPL-12.14.3 Rollback Uses Certified Baselines Only**
- **Category**: Rollback Strategy
- **Type**: Process
- **Profiles**:
  - Core: MUST
  - Strict: MUST

Rollback MUST always target a **previously certified baseline** (previous CBM + release), not ad hoc snapshots.
The rollback target SHALL have:

- a valid CBM,
- a valid Compliance Certificate (CC),
- archived evidence (RCR, TEP, SCEM).

---

**DPL-12.14.4 Forward-Compatible Data Changes**
- **Category**: Rollback Strategy
- **Type**: Process
- **Profiles**:
  - Core: SHOULD
  - Strict: MUST

When changes affect **data formats, database schema, or message schemas**, projects SHALL design migrations such that:

- rolling back code does not render existing, migrated data unreadable, OR
- rollback procedures explicitly include a safe data migration/restore step.

Unsafe assumptions (e.g., “DB always stays compatible on rollback”) are forbidden for Strict projects.

---

**DPL-12.14.5 Rollback Impact Analysis for External Interfaces**
- **Category**: Rollback Strategy
- **Type**: Process
- **Profiles**:
  - Core: SHOULD
  - Strict: MUST

Any rollback strategy MUST explicitly analyze and document effects on:

- external APIs and microservices,
- message queues / topics,
- external clients (e.g. other ECUs, devices, gateways).

If a rollback version changes protocol behavior or message schemas, the strategy SHALL define:

- acceptable configurations,
- constraints on mixed-version environments,
- mitigations (e.g. maintenance windows, draining queues).

---

**DPL-12.14.6 Rollback Scenario Testing**
- **Category**: Rollback Strategy
- **Type**: Testing
- **Profiles**:
  - Core: SHOULD
  - Strict: MUST

Strict projects SHALL include at least one test scenario in the TEP that:

- deploys a new version,
- executes representative safety-relevant flows,
- performs a rollback to the prior certified baseline,
- verifies that safety behavior and data integrity remain acceptable.

Core projects SHOULD perform at least basic rollback testing for Level A/B modules.

---

**DPL-12.14.7 Rollback Drills for Operational Readiness**
- **Category**: Rollback Strategy
- **Type**: Governance
- **Profiles**:
  - Core: SHOULD
  - Strict: SHOULD

Organizations SHOULD periodically perform “rollback drills” in non-production but realistic environments to ensure:

- runbooks are correct and usable,
- staff can execute rollback under time pressure,
- CI/CD automation behaves as expected.

Evidence MAY be captured as part of SCEM and operational readiness.

---

### 1.5 CI/CD and Deployment Pipeline

**DPL-12.15 - Deployment via Controlled Pipeline Only**
- **Category**: CI/CD
- **Type**: Process
- **Profiles**:
  - Core: SHOULD
  - Strict: MUST

Deployments to production SHOULD (Core) and MUST (Strict) be performed exclusively via **controlled CI/CD pipelines** that:

- use versioned configuration-as-code,
- operate from signed release artifacts, and
- enforce CBM conformity checks before deployment.

CI pipelines used for baseline creation MUST implement TPL-2 controls (offline install mode) 
and MUST record dependency + toolchain versions into CBM.

---

**DPL-12.16 - Separation of Duties in Deployment**
- **Category**: CI/CD
- **Type**: Governance
- **Profiles**:
  - Core: SHOULD
  - Strict: MUST

For Strict projects, the person or role approving the release SHALL NOT be the same as the person who authored the code changes. Core projects SHOULD follow the same practice. This separation SHALL be visible in the release registry.

---

**DPL-12.17 - Configuration-as-Code for Deployment**
- **Category**: CI/CD
- **Type**: Configuration
- **Profiles**:
  - Core: SHOULD
  - Strict: MUST

Deployment configuration (runtime options, environment variables, feature flags) SHOULD (Core) and MUST (Strict) be stored as **version-controlled configuration-as-code**. Manual configuration changes on production systems are forbidden.

---

### 1.6 Environment Parity and Testing

**DPL-12.18 - Environment Parity Across TEST/PRE-PROD/PROD**
- **Category**: Environment Parity
- **Type**: Configuration
- **Profiles**:
  - Core: SHOULD
  - Strict: MUST

TEST, PRE-PROD, and PROD environments SHOULD (Core) and MUST (Strict) be **as similar as practical**, differing only in allowed dimensions (e.g. load, scale). Differences in OS, Python version, dependency versions, hardware class, or network characteristics MUST be documented in CBM and justified.

---

**DPL-12.19 - Configuration Matrix Coverage**
- **Category**: Environment Parity
- **Type**: Process
- **Profiles**:
  - Core: SHOULD
  - Strict: MUST

Projects SHALL define the **supported configuration matrix** (platforms, OSes, architectures, Python version, major infra variants) and demonstrate that all **declared supported configurations** are covered by testing. Strict projects MUST provide explicit evidence.

---

**DPL-12.20 - On-Target or High-Fidelity Test Environments**
- **Category**: Environment Parity
- **Type**: Process
- **Profiles**:
  - Core: SHOULD
  - Strict: MUST

For Strict projects, at least one test environment MUST be **on-target** (same hardware/OS as production) or demonstrably **high-fidelity** (e.g. realistic virtualization). Core projects SHOULD follow the same practice for safety-relevant systems.

---

### 1.7 Production Safeguards

**DPL-12.21 - Restricted Direct Shell Access to PROD**
- **Category**: Production Safeguards
- **Type**: Governance
- **Profiles**:
  - Core: SHOULD
  - Strict: MUST

Direct shell access to production hosts SHOULD (Core) and MUST (Strict) be restricted, audited, and minimized. Routine operations SHOULD be performed via automation and deployment tools, not manual shell sessions.

---

**DPL-12.22 - Logging and Monitoring of Deployments**
- **Category**: Production Safeguards
- **Type**: Process
- **Profiles**:
  - Core: SHOULD
  - Strict: MUST

Deployments MUST be logged with at least:

- release identifier
- CBM id
- timestamp
- target environment
- result (success/failure)

Monitoring SHOULD (Core) and MUST (Strict) detect configuration drift and unauthorized changes.

---

**DPL-12.23 - Disaster Recovery Baseline Preservation**
- **Category**: Production Safeguards
- **Type**: Governance
- **Profiles**:
  - Core: SHOULD
  - Strict: MUST

Certified baselines (code, CBM, artifacts) MUST be stored in durable, redundant locations such that they can be restored in case of catastrophic data loss. This includes offsite or geo-redundant storage for Strict projects.

---

## 1.8 Upgrade process

> [⬆ Back to Table of Contents](#toc)


### DPL-12.24 - Interpreter Version Range with Single-Baseline Freeze

-   **Category**: Controlled Upgrade Process
-   **Type**: Process
-   **Profiles**:
    -   Core: SHOULD
    -   Strict: MUST

**Phase 1 - Change Proposal**
- Document requested change
- Identify affected baseline elements
- Classify change (code, dependency, interpreter, OS, hardware)

**Phase 2 - Impact Analysis**
- Identify safety impact
- Reassess hazards
- Update risk analysis

**Phase 3 - Test Requalification**
- Re-run full TEP
- Re-run platform matrix
- Re-run performance and reliability tests

**Phase 4 - New Baseline Creation**
- Create new CBM
- Update RCR, TEP, SBR
- Assign new Baseline ID

**Phase 5 - Approval and Release**
- Independent approval
- Issue new Compliance Certificate

**Key Principles**:
- No “delta approval”
- No partial acceptance
- No auto-updates

Any change leads automatically to a new baseline.

### DPL-12.25 - Emergency Release

-   **Category**: Controlled Upgrade Process
-   **Type**: Process
-   **Profiles**:
    -   Core: SHOULD
    -   Strict: MUST

A critical defect may trigger an Emergency Release, which:
- MUST follow the full Compliance Process
- MAY use accelerated execution paths

MUST produce:
- New CBM
- New TEP (focused but complete)
- New SBR
- New CC
- New Release ID

### DPL-12.26 - Scope Limitation

-   **Category**: Controlled Upgrade Process
-   **Type**: Process
-   **Profiles**:
    -   Core: SHOULD
    -   Strict: MUST

Emergency Releases:
- SHALL contain only the minimal change required to correct the issue
- SHALL NOT introduce new functionality
- SHALL NOT update dependencies unless safety-justified

### DPL-12.27 - Backport Requirement

-   **Category**: Controlled Upgrade Process
-   **Type**: Process
-   **Profiles**:
    -   Core: SHOULD
    -   Strict: MUST

Emergency fixes MUST be integrated back into:
- Next planned release
- Development branches
- Future baselines

No divergence.

## 2. Relationship to Code-Level 12.x Rules

> [⬆ Back to Table of Contents](#toc)


The **DPL-12.x** rules in this document complement the **CRSS-12.x** code-level configuration and deployment integrity rules defined in the Core/Strict catalogs.

- `CRSS-12.x` → what the **code and technical configuration** must guarantee.
- `DPL-12.x`  → what the **organization and deployment process** must enforce.

Both sets MUST be satisfied for a project to claim full CRSS-Python compliance.

---

## 3. Versioning and Governance

> [⬆ Back to Table of Contents](#toc)


This master specification:

- Is versioned alongside the Core/Strict specs and SCEM
- May be extended with additional DPL-12.x rules in future versions
- MUST be referenced in the project’s Safety Plan and Compliance Master

All projects SHALL clearly state:

- Which **DPL-12.x** rules they claim compliance with
- Any approved deviations and their justification
- The mapping to certification objectives (ASIL/SIL/DO/IEC classes)

---

## 4. Summary

> [⬆ Back to Table of Contents](#toc)


This master specification:

- Centralizes deployment, release, and baseline governance
- Enforces one-version-per-project deployment
- Eliminates drift and mutation risk
- Enables reproducible, certifiable deployments
- Supports Strict-A to the highest rigor

These rules are **mandatory** for all CRSS-Python projects seeking strong safety assurance in deployment and operations.
