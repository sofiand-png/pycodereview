# CRSS-Python Certification FAQ for Auditors & Regulators

**Version:** v1.0.0
**Status:** Informative
**Maturity:** Stable
© 2025 Sofian Daghsen – All rights reserved
Distributed under CC BY-NC-ND 4.0 — see LICENSE-CRSS.

---

## Table of Contents

- [1. What Is the Certification Scope of CRSS-Python?](#1-what-is-the-certification-scope-of-crss-python)
- [2. What Safety Levels Can CRSS-Python Support?](#2-what-safety-levels-can-crss-python-support)
- [3. Is Compliance Binary?](#3-is-compliance-binary)
- [4. What Are the Core Enforcement Mechanisms?](#4-what-are-the-core-enforcement-mechanisms)
- [5. What Evidence Is Required?](#5-what-evidence-is-required)
- [6. What Violations Automatically Fail Certification?](#6-what-violations-automatically-fail-certification)
- [7. Are Deviations Allowed?](#7-are-deviations-allowed)
  - [Strict-A `@critical`](#strict-a-critical)
  - [Strict-A `@non_critical_phase`](#strict-a-non_critical_phase)
  - [Strict-B/C and Core](#strict-bc-and-core)
- [8. How Is Determinism Verified?](#8-how-is-determinism-verified)
- [9. How Is the Interpreter Addressed?](#9-how-is-the-interpreter-addressed)
- [10. How Are Deployments Certified?](#10-how-are-deployments-certified)
- [11. What Is the Role of Organizational Maturity?](#11-what-is-the-role-of-organizational-maturity)
- [12. What Is the Auditor’s Checklist?](#12-what-is-the-auditors-checklist)
- [13. Final Summary](#13-final-summary)

---

##  1. What Is the Certification Scope of CRSS-Python?

CRSS-Python certification applies to **software units written in Python**, specifically:

- Supervisory logic
- Safety monitoring
- Decision-support components
- High-integrity control logic NOT performing direct actuation

Certification DOES NOT apply to:

- System-level safety certification
- Hardware certification
- Primary actuator control loops

CRSS-Python certification confirms **software compliance**, not system compliance.

---

##  2. What Safety Levels Can CRSS-Python Support?

| Domain | Supported Level |
|--------|------------------|
| ISO 26262 | ASIL D (Supervisory only) |
| IEC 61508 | SIL 3 (Supervisory only) |
| IEC 62304 | Class C (Multi-layer systems) |
| DO-278A | Ground Systems |
| DO-178C | DAL C/D (Non-flight-critical utilities) |

CRSS-Python does **not** support:

- ASIL D primary actuation
- SIL 4
- DAL A/B flight control

---

##  3. Is Compliance Binary?

Yes.

CRSS-Python defines certification status as:

- **PASS** or **FAIL**

There is no partial, percentage-based, or “conditional” compliance.

---

##  4. What Are the Core Enforcement Mechanisms?

Auditors should confirm:

- Mode assignments recorded in the MAR
- `@critical` annotations for safety decision paths
- `@non_critical_phase` boundaries
- Strict-A enforcement in critical code
- Zero deviation in Strict-A `@critical`
- One-Python-version-per-project rule
- Immutable deployment
- CBM (Configuration Baseline Manifest)

These are non-negotiable for certification.

---

##  5. What Evidence Is Required?

Evidence is produced through the SCEM (Safety Case Evidence Model). Mandatory artifacts include:

- **MAR** – Mode Assignment Register
- **RCR** – Rule Compliance Report
- **TEP** – Test Evidence Package
- **CBM** – Configuration Baseline Manifest
- **SCEM** – Consolidated evidence
- **CRC** – Certification Readiness Checklist
- **CC** – Compliance Certificate

All must be versioned, immutable, and traceable.

---

##  6. What Violations Automatically Fail Certification?

- Critical code calling non-critical code
- Dynamic allocation in `@critical`
- GC enabled in `@critical`
- Threads in `@critical`
- Deviation in Strict-A `@critical`
- Python version mismatch
- Dependency drift from CBM
- Hotfixes or runtime updates

Any one of these = **FAIL**.

---

##  7. Are Deviations Allowed?

###  Strict-A `@critical`
- No deviations permitted.

###  Strict-A `@non_critical_phase`
- Deviations allowed only if:
- Documented in MAR
- Risk assessed
- Approved by authority
- Does NOT affect `@critical`

###  Strict-B/C and Core
- Deviations permitted with:
- Documentation
- Mitigation
- Approval
- Testing evidence

---

##  8. How Is Determinism Verified?

Auditors should require:

- Bounded execution
- No recursion
- No unbounded loops
- No GC in critical code
- Single-threaded execution
- WCET measurement on target hardware
- Repeatability across runs

---

##  9. How Is the Interpreter Addressed?

CRSS-Python uses:

- Interpreter freezing in the CBM
- Toolchain Confidence Assessment (TCA)
- Python version immutability
- Configuration drift detection

Rebuilding MUST produce the same behavior.

---

##  10. How Are Deployments Certified?

PROD deployment is only allowed when:

- Release approved
- CBM validated
- PROD matches TEST environment
- Zero drift verified
- Manual authorization performed

No auto-deploy. No mutable builds.

---

##  11. What Is the Role of Organizational Maturity?

Strict-A requires:

- Safety Maturity Model Level S4
- Defined roles and responsibilities
- Controlled process environment
- Change governance

Low-maturity organizations cannot certify Strict-A.

---

##  12. What Is the Auditor’s Checklist?

Auditors should confirm:

- Mode correctness
- Critical/non-critical boundaries
- Zero violations in critical code
- CBM integrity
- SCEM completeness
- Deployment immutability
- One Python version
- Determinism evidence
- Test completeness (MC/DC for Strict-A)

If any fail -> Certification fails.

---

##  13. Final Summary

CRSS-Python certification confirms:

- The software follows strict rules
- Behavior is controlled and deterministic
- Deployment is immutable and reproducible
- Evidence is complete and traceable

It does **not** certify Python for primary real-time actuation.

Certification is rigorous by design — ensuring maximum safety.

---