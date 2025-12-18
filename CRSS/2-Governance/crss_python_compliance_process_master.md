# CRSS-Python Compliance Master Specification

**Version:** v1.0.0
**Status:** Normative
**Maturity:** Stable
© 2025 Sofian Daghsen — All Rights Reserved
Distributed under CC BY-NC-ND 4.0

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
**Core** — general-purpose safety.
**Strict** — high-integrity, critical subset with highest constraints.

---

# Safety Levels
- **A** – highest assurance
- **B** – medium assurance
- **C** – lowest assurance

Levels apply per unit/function, not module.

---

# MAR & Phase Model
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

## Phase 1 — Design Compliance
Activities:
- hazard mapping
- level assignment
- rule set selection
Artifacts:
- MAR
- initial SBR

## Phase 2 — Rule Compliance
Activities:
- static analysis
- manual review
Artifact:
- RCR

## Phase 3 — Test Compliance
Activities:
- unit tests
- MC/DC (for Level A)
- negative tests
- performance & determinism tests
- security tests
Artifact:
- TEP

## Phase 4 — Baseline Compliance
Activities:
- freeze environment
- produce CBM
Artifact:
- CBM

The certification baseline SHALL reference a Certified Build as defined in the
Release Management specification, including the certified wheel artifact and
its associated dependency freeze evidence.

## Phase 5 — Certification Readiness
Artifacts:
- final SBR
- SCEM

## Release Approval
- independent assessment
- CC issued

## Post-Release Monitoring
- anomaly tracking
- dependency CVE monitoring
- safety event logging

---

# Enforcement & Acceptance Model

## Rule Severity
- **INFO** — informational
- **WARN** — counts toward threshold
- **ERROR** — blocking unless justified
- **BLOCKER** — unconditional failure

## Strict-A Requirements
- **0 WARN**
- **0 ERROR**
- **0 BLOCKER**

## Deviations
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

## RCR — Rule Compliance Report
Includes:
- Release/Baseline IDs
- mapping of rules
- deviations
- signatures

## TEP — Test Evidence Package
Includes:
- test suite version
- platform matrix
- coverage
- MC/DC
- fault injection
- negative & security tests

## CBM — Configuration Baseline Manifest
Includes:
- Python version
- OS version
- dependencies
- container image
- build flags
- hardware details
- hashes

## SBR — Safety Baseline Report
Includes hazard mappings, risks, platform, deployment context.

## CC — Compliance Certificate
Includes official release certification.

## DL — Deviations Log
Contains rule ID, justification, approver, evidence.

## MAR — Mode Assignment Register
Defines unit -> level -> profile -> phase.

## SCEM — Evidence Matrix
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

# Deviations & Exceptions

## Allowed Deviations
Only if:
- not Level A critical
- risk documented
- Safety Manager approval

## Forbidden Deviations
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
- no rule violations
- tests complete
- MAR correct
- coverage adequate

## Reviewer Checklist
- rule-by-rule analysis
- static review
- deviation validation

## Safety Manager Checklist
- SBR correctness
- SCEM completeness
- risk soundness

## Release Authority Checklist
- ID consistency
- artifact integrity
- signature and attestation

---

# Compliance Flow
**Design -> Rule -> Test -> Baseline -> SBR -> CC -> Release**