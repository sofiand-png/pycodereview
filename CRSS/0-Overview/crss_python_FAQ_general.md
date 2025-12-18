# CRSS-Python Frequently Asked Questions (FAQ)

**Version:** v1.0.0
**Status:** Informative
**Maturity:** Stable
© 2025 Sofian Daghsen – All rights reserved
Distributed under CC BY-NC-ND 4.0 — see LICENSE-CRSS.

---

## Table of Contents

- [CRSS-Python Frequently Asked Questions (FAQ)](#crss-python-frequently-asked-questions-faq)
  - [1. What is CRSS-Python?](#1-what-is-crss-python)
  - [2. What problem does CRSS-Python solve?](#2-what-problem-does-crss-python-solve)
  - [3. Does CRSS-Python certify Python applications for ASIL-D / SIL3?](#3-does-crss-python-certify-python-applications-for-asil-d-sil3)
  - [4. What are Profiles, Levels, and Modes?](#4-what-are-profiles-levels-and-modes)
  - [5. What is `@critical`?](#5-what-is-critical)
  - [6. What is `@non_critical_phase`?](#6-what-is-noncriticalphase)
  - [7. Can we use multiple Python versions in a project?](#7-can-we-use-multiple-python-versions-in-a-project)
  - [8. Does CRSS-Python allow hotfixes?](#8-does-crss-python-allow-hotfixes)
  - [9. Is automated deployment allowed?](#9-is-automated-deployment-allowed)
  - [10. Can Python install dependencies at runtime?](#10-can-python-install-dependencies-at-runtime)
  - [11. Can CRSS-Python software use threads?](#11-can-crss-python-software-use-threads)
  - [12. Can we build microservices under CRSS-Python?](#12-can-we-build-microservices-under-crss-python)
  - [13. How are violations handled?](#13-how-are-violations-handled)
  - [14. How do we know if a project is compliant?](#14-how-do-we-know-if-a-project-is-compliant)
  - [15. Can CRSS-Python be extended?](#15-can-crss-python-be-extended)
  - [16. Can CRSS-Python be used for Machine Learning systems?](#16-can-crss-python-be-used-for-machine-learning-systems)
  - [17. Does CRSS-Python replace ISO 26262 / IEC 61508?](#17-does-crss-python-replace-iso-26262-iec-61508)
  - [18. Where do I start?](#18-where-do-i-start)
  - [19. How do I contribute?](#19-how-do-i-contribute)
  - [20. Is CRSS-Python unique?](#20-is-crss-python-unique)
  - [21. Which components define what in the overall CRSS ?](#21-which-components-define-what-in-the-overall-crss)

---

## 1. What is CRSS-Python?
CRSS-Python is a rigorous safety and compliance framework for Python, enabling its use in high-integrity and mission-critical environments. It defines strict rules, processes, and evidence requirements to ensure predictable, deterministic, and certifiable software behavior.

---

## 2. What problem does CRSS-Python solve?
Python is traditionally excluded from high-risk domains due to:
- Dynamic behavior
- Non-deterministic runtime features
- Garbage collection pauses
- Lack of timing guarantees
- Interpreter/toolchain unpredictability

CRSS-Python introduces architecture, rules, and governance to control risks and make Python **safe enough** for supervisory and high-assurance roles.

---

## 3. Does CRSS-Python certify Python applications for ASIL-D / SIL3?
CRSS-Python enables Python to be used in:
- ASIL-D supervisory roles
- SIL3 supervisory/control roles
- IEC 62304 Class C (multi-layer systems)
- DO-278 ground systems

However, it **does not certify** Python for:
- Primary actuation loops (e.g., braking, flight control)
- Single-channel safety enforcement
- Hard real-time DAL A avionics

Python must operate as part of a **multilayer safety architecture**.

---

## 4. What are Profiles, Levels, and Modes?
- **Profiles**: Core, Strict
- **Safety Levels**: A, B, C
- **Mode** = Profile × Safety Level

Example: Strict-A is Strict + Level A enforcement.

Modes determine:
- Rule severity
- Allowed deviations
- Testing requirements
- Certification scope

---

## 5. What is `@critical`?
`@critical` marks code that executes safety decisions. It must be:
- Deterministic
- Free from allocation, I/O, blocking, GC
- Zero violation under Strict-A
- Fully covered by MC/DC testing

Critical code **may not call non-critical code**.

---

## 6. What is `@non_critical_phase`?
It marks pre/post-critical functions where:
- Initialization
- Object creation
- File I/O
- Configuration

are allowed **before** critical execution begins.

However:
- Strict-A rules still apply
- MUST violations remain blocking
- Critical code cannot call non-critical code

---

## 7. Can we use multiple Python versions in a project?
- No.

The standard covers Python **3.9–3.12**, but each project MUST:
- Select exactly one version
- Freeze it in the CBM
- Never change it after approval

Switching versions = new baseline + new certification.

---

## 8. Does CRSS-Python allow hotfixes?
- No hotfixes.
- No patch-in-production.
- No runtime edits.

Any change -> new:
- CBM
- Release
- Compliance cycle

This ensures reproducibility and safety traceability.

---

## 9. Is automated deployment allowed?
- In TEST environment
- Never in PROD

Prod deployments must be:
- Manual approval
- Immutable
- CBM-validated

---

## 10. Can Python install dependencies at runtime?
- Absolutely not.
Runtime installation (pip, apt, conda, etc.) is prohibited.

Dependencies must be:
- Frozen
- Private repository
- Version-locked

---

## 11. Can CRSS-Python software use threads?
In Strict-A `@critical`: No
In Strict: Allowed with restrictions
In Core: Allowed

Strict-A requires single-threaded critical execution to guarantee determinism.

---

## 12. Can we build microservices under CRSS-Python?
- Yes, with:
- Process isolation
- Stable APIs
- Network timeout rules
- Retry & fail-safe strategies
- Mode propagation policies

---

## 13. How are violations handled?
Severity levels:
- WARN – Should violation
- ERROR – Violation of a MUST requirement (Core), or a MUST/SHOULD requirement (Strict)
- BLOCKER – Any such violation inside Strict-A `@critical` code (certification failure)


---

## 14. How do we know if a project is compliant?
A project is compliant only if:
- Compliance phases completed
- SCEM complete
- CRC approved
- CBM frozen
- Toolchain fixed

Compliance is **binary**:
- PASS or FAIL

---

## 15. Can CRSS-Python be extended?
Yes, but extensions must:
- Not weaken rules
- Maintain compatibility with Modes
- Preserve one-Python-version-per-project
- Not contradict normative documents

---

## 16. Can CRSS-Python be used for Machine Learning systems?
- Yes for:
- Supervisory logic
- Safety wrappers
- Monitoring pipelines
- Data validation

- Not for:
- Real-time inference controlling primary actuators

ML models must be treated as untrusted components.

---

## 17. Does CRSS-Python replace ISO 26262 / IEC 61508?
- No.

It is a **coding and software governance standard**, not a full system-level safety standard. It must operate **under** the applicable domain standard.

---

## 18. Where do I start?
1. Read Unified Safety Spec v3.0.0
2. Assign Modes in MAR
3. Annotate `@critical` and `@non_critical_phase`
4. Generate SCEM
5. Freeze CBM
6. Begin compliance cycle

---

## 19. How do I contribute?
All proposals must:
- Follow the repository publication standard
- Use semantic versioning
- Respect rule ID stability
- Be reviewed by safety governance roles

---

## 20. Is CRSS-Python unique?
Yes. As of 2025, it is the **most comprehensive and strict Python safety framework ever published**, enabling Python in domains previously considered unreachable.

---

## 21. Which components define what in the overall CRSS ?

- Core + Strict define the what
- Phase model + scopes + phase-aware notes define the how and where
- SCEM / compliance process define the proof