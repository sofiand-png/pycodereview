# CRSS-Python Compliance Master Specification

**Version:** v1.0.0
**Status:** Normative
**Maturity:** Stable
© 2025 Sofian Daghsen - All Rights Reserved
Distributed under CC BY-NC-ND 4.0

---

<a id="toc"></a>
## Table of Contents
- [CRSS-Python Compliance Master Specification](#crss-python-compliance-master-specification)
  - [Table of Contents](#table-of-contents)
- [Purpose](#purpose)
- [Scope](#scope)
- [Normative References](#normative-references)
- [Definitions](#definitions)
- [Identifier Model](#identifier-model)
- [Compliance Overview](#compliance-overview)
- [Profiles](#profiles)
- [Safety Levels](#safety-levels)
- [MAR and Phase Model](#mar-and-phase-model)
- [Entry Criteria](#entry-criteria)
- [Compliance Actor Roles](#compliance-actor-roles)
- [Compliance Lifecycle (Five-Phase Model)](#compliance-lifecycle-five-phase-model)
  - [Phase1 Design Compliance](#phase-1-design-compliance)
  - [Phase2 Rule Compliance](#phase-2-rule-compliance)
  - [Phase3 Test Compliance](#phase-3-test-compliance)
  - [Phase4 Baseline Compliance](#phase-4-baseline-compliance)
  - [Phase5 Certification Readiness](#phase-5-certification-readiness)
  - [Release Approval](#release-approval)
  - [Post-Release Monitoring](#post-release-monitoring)
- [Enforcement and Acceptance Model](#enforcement-and-acceptance-model)
  - [Rule Severity](#rule-severity)
  - [Strict-A Requirements](#strict-a-requirements)
  - [Deviations](#deviations)
  - [No Silent Downgrade](#no-silent-downgrade)
- [One-Version Rule (Interpreter Freeze)](#one-version-rule-interpreter-freeze)
- [Mandatory Artifacts](#mandatory-artifacts)
  - [RCR Rule Compliance Report](#rcr-rule-compliance-report)
  - [TEP Test Evidence Package](#tep-test-evidence-package)
  - [CBM Configuration Baseline Manifest](#cbm-configuration-baseline-manifest)
  - [SBR Safety Baseline Report](#sbr-safety-baseline-report)
  - [CC Compliance Certificate](#cc-compliance-certificate)
  - [DL Deviations Log](#dl-deviations-log)
  - [MAR Mode Assignment Register](#mar-mode-assignment-register)
  - [SCEM Evidence Matrix](#scem-evidence-matrix)
- [Artifact Chain](#artifact-chain)
- [Re-Approval Rules](#re-approval-rules)
- [Deviations and Exceptions](#deviations-and-exceptions)
  - [Allowed Deviations](#allowed-deviations)
  - [Forbidden Deviations](#forbidden-deviations)
- [Testing Compliance](#testing-compliance)
- [Deployment Compliance](#deployment-compliance)
- [Toolchain Confidence Assessment](#toolchain-confidence-assessment)
- [Certificate Issuance](#certificate-issuance)
- [Archival Rules](#archival-rules)
- [Auditor Guidance](#auditor-guidance)
- [Checklists](#checklists)
  - [Developer Checklist](#developer-checklist)
  - [Reviewer Checklist](#reviewer-checklist)
  - [Safety Manager Checklist](#safety-manager-checklist)
  - [Release Authority Checklist](#release-authority-checklist)
- [Compliance Flow](#compliance-flow)

---

# Purpose
This unified specification consolidates:
- crss_compliance_process_version_to_verify.md
- crss_python_compliance_process_master.md
- CRSS_Python_Compliance_Master_Spec.md

It defines the complete compliance lifecycle, enforcement model, artifacts, acceptance criteria, and certification rules for CRSS-Python.

---

# Scope
Covers the full lifecycle:
- design
- implementation
- review
- testing
- baseline creation
- release certification
- deployment
- re-approval
- archival

---

# Normative References
All requirements with status: Normative are relevant.

---

# Definitions
**Rule Compliance:** conformity to CRSS rules.
**Baseline:** fully frozen snapshot w/ CBM, dependencies, interpreter, config.
**Release:** certified output bound to one baseline.
**Artifact:** formal evidence used for certification.
**Level:** A/B/C safety category.
**Profile:** Core or Strict.
**Phase Model:** @critical or non-critical execution.

---

# Identifier Model
Every artifact and release includes:
- Release ID
- Baseline ID
- Commit Hash
- Safety Level
- Profile

---

# Compliance Overview
Compliance requires:
- All rules applicable to Profile and Level satisfied
- MAR validated
- Complete and consistent artifacts (RCR, TEP, CBM, SBR, CC, SCEM)
- Reproducibility from baseline
- Change management controls applied

**Compliance outcome:** PASS or FAIL.

---

# Profiles
**Core** - general-purpose safety.
**Strict** - high-integrity, critical subset with highest constraints.

---

# Safety Levels
- **A** - highest assurance
- **B** - medium assurance
- **C** - lowest assurance

Levels apply per unit/function, not module.

---

# MAR and Phase Model
The Mode Assignment Register specifies:
- Level
- Profile
- Phase: @critical or non-critical

All rules, tests, and evidence map through MAR.

---

# Entry Criteria
A project enters compliance when:
- rule catalog is selected
- MAR is established
- architecture is stable
- interpreter version chosen

---

# Compliance Actor Roles
| Role | Responsibilities |
|------|------------------|
| Developer | Implements code, tests, prepares RCR inputs |
| Reviewer | Rule verification |
| Safety Manager | Safety mapping, SBR |
| Independent Assessor | Independent evaluation |
| Release Authority | Signs CC |
| Audit Authority | External compliance |
| Toolchain Validator | Toolchain correctness |

---

# Compliance Lifecycle (Five-Phase Model)

## Phase1 Design Compliance

> [⬆ Back to Table of Contents](#toc)

Activities:
- hazard mapping
- level assignment
- rule set selection
Artifacts:
- MAR
- initial SBR

## Phase2 Rule Compliance

> [⬆ Back to Table of Contents](#toc)

Activities:
- static analysis
- manual review
Artifact:
- RCR

## Phase3 Test Compliance

> [⬆ Back to Table of Contents](#toc)

Activities:
- unit tests
- MC/DC (for Level A)
- negative tests
- performance and determinism tests
- security tests
Artifact:
- TEP

## Phase4 Baseline Compliance

> [⬆ Back to Table of Contents](#toc)

Activities:
- freeze environment
- produce CBM
Artifact:
- CBM

The certification baseline SHALL reference a Certified Build as defined in the
Release Management specification, including the certified wheel artifact and
its associated dependency freeze evidence.

## Phase5 Certification Readiness

> [⬆ Back to Table of Contents](#toc)

Artifacts:
- final SBR
- SCEM

## Release Approval

> [⬆ Back to Table of Contents](#toc)

- independent assessment
- CC issued

## Post-Release Monitoring

> [⬆ Back to Table of Contents](#toc)

- anomaly tracking
- dependency CVE monitoring
- safety event logging

---

# Enforcement and Acceptance Model

## Rule Severity

> [⬆ Back to Table of Contents](#toc)

- **INFO** - informational
- **WARN** - counts toward threshold
- **ERROR** - blocking unless justified
- **BLOCKER** - unconditional failure

## Strict-A Requirements

> [⬆ Back to Table of Contents](#toc)

- **0 WARN**
- **0 ERROR**
- **0 BLOCKER**

## Deviations

> [⬆ Back to Table of Contents](#toc)

Allowed only if:
- no Level A @critical rule affected
- documented risk assessment
- approved by Safety Manager

Forbidden for:
- Strict-Level-A MUST rules
- deterministic behavior
- baseline integrity
- interpreter freeze rules

## No Silent Downgrade

> [⬆ Back to Table of Contents](#toc)

Reviewers cannot reduce severity to pass compliance.

---

# One-Version Rule (Interpreter Freeze)
A project MUST select one Python interpreter version for its certified baseline.

Any change triggers:
- new CBM
- new TEP
- new CC

No partial acceptance.

---

# Mandatory Artifacts

## RCR Rule Compliance Report

> [⬆ Back to Table of Contents](#toc)

Includes:
- Release/Baseline IDs
- mapping of rules
- deviations
- signatures

## TEP Test Evidence Package

> [⬆ Back to Table of Contents](#toc)

Includes:
- test suite version
- platform matrix
- coverage
- MC/DC
- fault injection
- negative and security tests

## CBM Configuration Baseline Manifest

> [⬆ Back to Table of Contents](#toc)

Includes:
- Python version
- OS version
- dependencies
- container image
- build flags
- hardware details
- hashes

## SBR Safety Baseline Report

> [⬆ Back to Table of Contents](#toc)

Includes hazard mappings, risks, platform, deployment context.

## CC Compliance Certificate

> [⬆ Back to Table of Contents](#toc)

Includes official release certification.

## DL Deviations Log

> [⬆ Back to Table of Contents](#toc)

Contains rule ID, justification, approver, evidence.

## MAR Mode Assignment Register

> [⬆ Back to Table of Contents](#toc)

Defines unit -> level -> profile -> phase.

## SCEM Evidence Matrix

> [⬆ Back to Table of Contents](#toc)

Maps Requirements -> Rules -> Tests -> Evidence.

---

# Artifact Chain
Artifact Relationship Model
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

All artifacts share the same:
- Release ID
- Baseline ID

They form a single versioned unit.

---

# Re-Approval Rules
Re-approval required for:
- interpreter version change
- OS/kernel change
- dependency version change
- hardware change
- MAR change
- safety goal change
- new features
- behavior change affecting safety

Severity:
- **Minor** -> TEP only
- **Major** -> full cycle

---

# Deviations and Exceptions

## Allowed Deviations

> [⬆ Back to Table of Contents](#toc)

Only if:
- not Level A critical
- risk documented
- Safety Manager approval

## Forbidden Deviations

> [⬆ Back to Table of Contents](#toc)

For:
- Strict-Level-A MUST rules
- deterministic behavior
- baseline integrity

---

# Testing Compliance
Includes:
- unit tests
- interface/boundary tests
- negative testing
- MC/DC for Level A
- determinism testing
- stress/reliability tests
- security tests

---

# Deployment Compliance
Requires:
- immutable deployment
- reproducible builds
- attestation
- rollback strategy
- production gating

**Certification Build Definition:** 
A “certification build” is a build executed under TPL-2 constraints:
- no public internet package resolution 
- using the baseline interpreter + pinned dependencies
- and producing TEP/CBM inputs.

---

# Toolchain Confidence Assessment
Includes:
- qualification
- classification
- error analysis
- validation
- regression testing

---

# Certificate Issuance
Contains:
- certification statement
- IDs
- hash list
- signature
- expiry

---

# Archival Rules
- 15-year retention
- offsite backup
- cryptographic hashing
- tamper protection
- disaster recovery protocol

---

# Auditor Guidance
Auditors verify:
- traceability
- independence
- MAR correctness
- coverage results
- reproducibility
- absence of forbidden deviations
- alignment between SBR/RCR/TEP/CBM/CC

---

# Checklists

## Developer Checklist

> [⬆ Back to Table of Contents](#toc)

- no rule violations
- tests complete
- MAR correct
- coverage adequate

## Reviewer Checklist

> [⬆ Back to Table of Contents](#toc)

- rule-by-rule analysis
- static review
- deviation validation

## Safety Manager Checklist

> [⬆ Back to Table of Contents](#toc)

- SBR correctness
- SCEM completeness
- risk soundness

## Release Authority Checklist

> [⬆ Back to Table of Contents](#toc)

- ID consistency
- artifact integrity
- signature and attestation

---

# Compliance Flow
**Design -> Rule -> Test -> Baseline -> SBR -> CC -> Release**