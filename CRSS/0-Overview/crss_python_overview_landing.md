# CRSS-Python Overview & Repository Map

**Version:** v1.0.0  
**Status:** Informative  
**Maturity:** Stable  
© 2025 Sofian Daghsen - All rights reserved  
Distributed under CC BY-NC-ND 4.0 - see LICENSE-CRSS.

---

## Table of Contents
- [CRSS-Python Overview & Repository Map](#crss-python-overview-repository-map)
  - [Table of Contents](#table-of-contents)
  - [1. CRSS-Python Overview](#1-crss-python-overview)
    - [1.1 What Is CRSS-Python?](#11-what-is-crss-python)
    - [1.2 Why Does This Matter?](#12-why-does-this-matter)
    - [1.3 High-Level Concept Map](#13-high-level-concept-map)
    - [1.4 Profiles: How Strict Are the Rules?](#14-profiles-how-strict-are-the-rules)
    - [1.5 Safety Levels: How Dangerous Is Failure?](#15-safety-levels-how-dangerous-is-failure)
    - [1.6 Modes: The Enforcement Engine](#16-modes-the-enforcement-engine)
    - [1.7 Phases: Critical vs Non-Critical](#17-phases-critical-vs-non-critical)
      - [Properties `@critical`](#properties-critical)
      - [Properties `@non_critical_phase`](#properties-non_critical_phase)
    - [1.8 The Compliance Journey](#18-the-compliance-journey)
    - [1.9 Recommended Strategy by Project Type](#19-recommended-strategy-by-project-type)
      - [1.9.1 New Projects (Greenfield)](#191-new-projects-greenfield)
      - [1.9.2 Mid-Development Projects](#192-mid-development-projects)
      - [1.9.3 Production Systems Scaling Up](#193-production-systems-scaling-up)
    - [1.10 Architecture Recommendations](#110-architecture-recommendations)
    - [1.11 How to Navigate the Framework](#111-how-to-navigate-the-framework)
    - [1.12 Two Worlds: Readers vs Auditors](#112-two-worlds-readers-vs-auditors)
      - [Developers / Readers](#developers-readers)
      - [Auditors / Regulators](#auditors-regulators)
    - [1.13 Final Message](#113-final-message)
  - [2. Repository Map (CRSS/)](#2-repository-map-crss)
    - [2.1 Overview](#21-overview)
    - [2.2 Specifications](#22-specifications)
    - [2.3 Governance & Evidence](#23-governance-evidence)
    - [2.4 Deployment & Baselines](#24-deployment-baselines)
    - [2.5 Policies](#25-policies)
    - [2.6 Annexes, Guides & Roadmaps](#26-annexes-guides-roadmaps)
    - [2.7 Examples](#27-examples)
    - [2.8 Release & Meta](#28-release-meta)

---

## 1. CRSS-Python Overview

### 1.1 What Is CRSS-Python?

CRSS-Python is a **safety and compliance framework** that makes Python suitable for:

- Automotive safety systems
- Industrial control
- Medical devices
- Critical monitoring systems
- High-assurance automation
- Mission-critical supervisory logic

It provides:

- Strict rules  
- Structured processes  
- Deterministic execution models  
- Certification-ready evidence  

CRSS-Python does not claim to transform Python into a real-time operating system/controller,
nor does it authorize Python to directly control time-critical physical actuators (e.g. torque, braking, flight control surfaces).

- The standard is explicitly scoped to supervisory, decision-making, validation, arbitration, monitoring, and safety-envelope logic, where determinism, bounded behavior, and strong evidence can be established through architectural constraints and process discipline.
- For avionics, CRSS-Python is intended for ground systems, tooling, test infrastructure, and safety-support functions, not airborne flight-critical control software.

Any claims of safety integrity remain system-level claims: CRSS defines how Python software can be made certifiable within its declared scope, not how an entire system achieves certification.

---

### 1.2 Why Does This Matter?

In safety-critical domains, software failures can lead to:

- Injury or loss of life
- System damage
- Regulatory violations
- Legal and financial consequences

Python is popular-but normally considered too dynamic and unpredictable.

CRSS-Python changes that by:

- Removing unsafe behaviors  
- Enforcing strict development rules  
- Requiring full traceability  
- Making deployments reproducible  
- Enabling certification paths  

---

### 1.3 High-Level Concept Map

To understand CRSS-Python, you only need five core ideas:

| Concept | Meaning |
|--------|---------|
| **Profiles** | How strict the rules are (Core / Strict) |
| **Safety Levels** | How critical the code is (A / B / C) |
| **Modes** | Profile × Safety Level (e.g., Strict-A) |
| **Phases** | Critical vs Non-Critical execution |
| **Evidence** | Proof that rules were followed |

The entire framework is built around these ideas.

---

### 1.4 Profiles: How Strict Are the Rules?

| Profile | Purpose |
|--------|---------|
| **Core** | General safety, best practice, low risk |
| **Strict** | High-integrity and mission-critical use |

Strict is tougher than Core.  
It has more rules, stronger testing, and tighter deployment requirements.

---

### 1.5 Safety Levels: How Dangerous Is Failure?

| Safety Level | Meaning |
|--------------|---------|
| **Level C** | Low impact failures |
| **Level B** | Moderate impact |
| **Level A** | Highest criticality |

Level A demands the strongest safety controls.

---

### 1.6 Modes: The Enforcement Engine

A **Mode** = Profile × Safety Level.

Valid examples:

- Core-C
- Core-B
- Strict-C
- Strict-B
- **Strict-A** (maximum rigor)

> **Important Note:** “Core-A” is **not permitted**.  
> Any Safety Level A element must use the **Strict** profile (Mode = Strict-A).

The Mode determines:

- Which rule catalog applies (Core vs Strict)  
- How violations are treated (warning, error, or blocker)  
- How much evidence is required (coverage, MC/DC, SCEM, CBM, CRC)  
- Deployment and certification eligibility

In particular:

- **Strict-A** uses the **Strict** profile at **Level A**, with:
  - zero-tolerance for rule violations in critical code,
  - mandatory SCEM/CBM/CRC evidence,
  - full coverage and MC/DC on safety-critical logic.

- **Strict-B / Strict-C** use the **same Strict rules**, but:
  - may allow a very small number of justified SHOULD violations,
  - can have lower coverage targets than Strict-A,
  - require proportionally lighter evidence packages.

Strict-A = **maximum assurance**, not a different programming language.

---

### 1.7 Phases: Critical vs Non-Critical

CRSS-Python distinguishes:

#### Properties `@critical`

Where safety decisions happen - must be:

- Deterministic
- No allocation or blocking
- Single-threaded
- Fully tested
- Zero violation in Strict-A

#### Properties `@non_critical_phase`

Used for:

- Setup
- Loading config
- Object creation
- Networking
- File access

Still must follow rules - but less restrictive.

> **Key rule:** Critical code may **not** call non-critical code.

---

### 1.8 The Compliance Journey

Compliance follows a **5-phase process**:

1. Requirements & Traceability  
2. Rule Compliance  
3. Testing & Coverage  
4. Baseline (CBM) Freeze  
5. Approval & Certification  

Compliance is **binary**:

- PASS  
- FAIL  

There is no “partial compliance.”

---

### 1.9 Recommended Strategy by Project Type

#### 1.9.1 New Projects (Greenfield)

**Goal:** Start clean and grow safely.

Recommended steps:

1. Start with **Core-C** Mode  
2. Use clean modular architecture  
3. Introduce `@critical` only when needed  
4. Adopt CBM early (even before certification)  
5. Move toward **Strict-B** as maturity increases  

**Design recommendations:**

- Stateless components where possible  
- Clear boundaries between modules  
- Logging, monitoring, and testing early  
- No global state  
- No dynamic imports  

**Refactoring priority:**

1. Remove unsafe dynamic behaviors  
2. Add tests and coverage  
3. Introduce Mode assignments  
4. Move to Strict profile  

**Target maturity path:**  
Core -> Strict -> Strict-B -> Strict-A (if needed)

---

#### 1.9.2 Mid-Development Projects

**Goal:** Gain safety without stopping progress.

Recommended steps:

1. Identify safety-critical modules  
2. Apply Modes only where needed  
3. Introduce `@non_critical_phase` to split logic  
4. Freeze Python version  
5. Build CBM for the next release  

**Refactoring priority:**

1. Break monoliths into components  
2. Separate critical and non-critical code paths  
3. Replace dynamic behavior  
4. Add deterministic interfaces  

**Target maturity path:**  
Core-B -> Strict-B -> Strict-A (selected modules)

---

#### 1.9.3 Production Systems Scaling Up

**Goal:** Move toward certification and reliability.

Required actions:

- Convert deployments to immutable  
- Create CBM  
- Enforce zero-drift policy  
- Establish SCEM  
- Begin compliance cycle  

**Refactoring priority:**

1. Isolate safety-critical components  
2. Introduce process isolation  
3. Harden APIs and communication  
4. Strengthen monitoring and watchdogs  

**Target maturity path:**  
Strict-B -> Strict-A

---

### 1.10 Architecture Recommendations

Regardless of project stage:

- Use process isolation  
- Avoid shared state  
- Keep critical logic small and simple  
- Use message-based communication  
- Pre-allocate resources before critical execution  
- Avoid circular dependencies  
- One layer in -> one layer out (clear boundaries)

---

### 1.11 How to Navigate the Framework

| If you want to understand… | Read |
|----------------------------|------|
| Overall rules & concepts | **Standard Safety Master** |
| How to prove compliance | **Compliance Process Master** |
| Evidence and certification | **Safety Case Evidence Model (SCEM)** |
| Deployment & release | **Deployment Master** |
| Tooling automation | **Tooling & Automation Master** |

The Overview Page is your **map**.  
The specs are the **manuals**.

---

### 1.12 Two Worlds: Readers vs Auditors

#### Developers / Readers

Focus on:

- Profiles  
- Modes  
- Critical vs non-critical  
- Recommended strategy  
- Practical rules  

#### Auditors / Regulators

Focus on:

- SCEM  
- CBM  
- Evidence chains  
- Enforcement logic  
- Deployment immutability  

A separate **Auditor FAQ** supports certification discussions.

---

### 1.13 Final Message

You do **not** need to understand everything at once.

Start small:

- Choose a Mode  
- Mark critical code  
- Follow rules  
- Build evidence  

You can grow into Strict-A maturity step by step.

CRSS-Python gives you a **path**, not just rules.

---

## 2. Repository Map (CRSS/)

All paths below are under the `CRSS/` folder of the public repository.

### 2.1 Overview

- [CRSS-Python Overview & Repository Map](./crss_python_overview_landing.md)  
  High-level introduction, concepts, and navigation map.

- [Study Path & Curriculum](./crss_python_study_path_curriculum.md)  
  Recommended learning order and topics.

- [FAQ (General)](./crss_python_FAQ_general.md)  
  General CRSS-Python Q&A.

- [FAQ (Auditors & Regulators)](./crss_python_FAQ_auditors_regulators.md)  
  Certification-facing and regulator-oriented Q&A.

---

### 2.2 Specifications

**Profiles**
- [CRSS-Python Core Profile Specification](../1-Specifications/Profiles/crss_python_core_spec.md)  
- [CRSS-Python Strict Profile Specification](../1-Specifications/Profiles/crss_python_strict_spec.md)

**Master (cross-cutting)**
- [CRSS-Python Standard Safety Master](../1-Specifications/Master/crss_python_standard_safety_master.md)  
- [Phase-Aware Rule Interpretation Model](../1-Specifications/Master/crss_phase_aware_rule_interpretation_model.md)  
- [Safety Standard Mapping Annex](../1-Specifications/Master/crss_python_safety_standard_mapping_annex.md)

---

### 2.3 Governance & Evidence

- [Compliance Process Master](../2-Governance/crss_python_compliance_process_master.md)  
- [Safety Case Evidence Model](../2-Governance/crss_python_safety_case_evidence_model.md)  
- [SCEM Annexes](../2-Governance/crss_python_SCEM_annexes.md)  
- [Certification Readiness Kit](../2-Governance/crss_python_certification_readiness_kit.md)  
- [External Assessment Master](../2-Governance/crss_python_external_assessment_master.md)  
- [Integration with V-Model and ASPICE](../2-Governance/crss_python_integration_with_v-model_and-ASPICE.md)  
- [Tooling & Automation Master](../2-Governance/crss_python_tooling_automation_master.md)

---

### 2.4 Deployment & Baselines

- [Deployment Master](../3-Deployment/crss_python_deployment_master.md)  
- [Release Management](../3-Deployment/crss_python_release_management.md)  
- [CBM Template](../3-Deployment/crss_python_cbm_template.md)

---

### 2.5 Policies

- [Deviations Policy](../4-Policies/crss_python_deviations_policy.md)  
- [Repository Publication Standard](../4-Policies/crss_python_repository_publication_standard.md)  
- [Toolchain Baseline](../4-Policies/crss_python_toolchain_baseline.md)

---

### 2.6 Annexes, Guides & Roadmaps

- [Architecture Blueprint](../5-Annexes/crss_python_architecture_blueprint.md)  
- [Architecture Guide](../5-Annexes/crss_python_architecture_guide.md)  
- [Distributed System Design Guide](../5-Annexes/crss_python_distributed_system_design_guide.md)  
- [Integration Architecture](../5-Annexes/crss_python_integration_architecture.md)  
- [Multi-Service Integration Guide](../5-Annexes/crss_python_multi_service_integration_guide.md)  
- [Toolchain Hardening Guide](../5-Annexes/crss_python_toolchain_hardening_guide.md)  
- [ML / Pandas / NumPy Safety](../5-Annexes/crss_python_ml_pandas_numpty_safety.md)  
- [Common Mistakes](../5-Annexes/crss_python_common_mistakes.md)  
- [Ecosystem Improvement Roadmap](../5-Annexes/crss_python_ecosystem_evolution_directions.md)  
- [Veteran Enhancement Pack](../5-Annexes/crss_python_veteran_enhancement_pack.md)

---

### 2.7 Examples

- [Sensor Voting Reference Example (README)](../6-Examples/crss_example_sensor_voting_reference/README.md)  
- [Sensor Voting Certification Example](../6-Examples/crss_example_sensor_voting_reference/docs/crss_sensor_voting_certification_example.md)  
- [Sensor Voting Compliance Report](../6-Examples/crss_example_sensor_voting_reference/docs/crss_sensor_voting_compliance_report.md)

---

### 2.8 Release & Meta

- [Release Notes v1.0.0](../7-Release/release_notes_v1-0-0.md)  
- [Whitepaper (PDF)](../7-Release/CRSS_Python_Whitepaper_v1_0_0.pdf)
