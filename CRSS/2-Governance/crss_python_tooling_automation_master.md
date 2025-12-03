# CRSS-Python Tooling & Automation Master Specification

**Version:** v1.0.0
**Status:** Normative
**Maturity:** Stable
© 2025 Sofian Daghsen – All rights reserved
Distributed under CC BY-NC-ND 4.0 — see LICENSE-CRSS.

---

## Table of Contents

- [CRSS-Python Tooling & Automation Master Specification](#crss-python-tooling-automation-master-specification)
- [0. Purpose](#0-purpose)
- [1. Tooling Governance Model](#1-tooling-governance-model)
  - [1.1 Role of Tools in CRSS](#11-role-of-tools-in-crss)
  - [1.2 Tool Categories](#12-tool-categories)
- [2. Automation Requirements](#2-automation-requirements)
  - [2.1 Mandatory Automation Targets](#21-mandatory-automation-targets)
  - [2.2 Non-Automatable Components](#22-non-automatable-components)
- [3. Tool Capability Levels](#3-tool-capability-levels)
  - [3.1 Tool Confidence Levels (TCL)](#31-tool-confidence-levels-tcl)
  - [3.2 Tool Confidence Assessment (TCA)](#32-tool-confidence-assessment-tca)
- [4. Automated Evidence Requirements](#4-automated-evidence-requirements)
  - [4.1 Mandatory Artifacts](#41-mandatory-artifacts)
  - [4.2 File Format Requirements](#42-file-format-requirements)
- [5. Toolchain Version Control](#5-toolchain-version-control)
  - [5.1 One-Version Rule](#51-one-version-rule)
  - [5.2 Toolchain Drift = Automatic FAIL](#52-toolchain-drift-automatic-fail)
- [6. SCEM Tool-Assisted Templates](#6-scem-tool-assisted-templates)
  - [6.1 MAR Template](#61-mar-template)
  - [6.2 Propagation Report Template](#62-propagation-report-template)
  - [6.3 Coverage Template](#63-coverage-template)
- [7. Tool Acceptance Criteria](#7-tool-acceptance-criteria)
  - [7.1 Automated Evidence Acceptance](#71-automated-evidence-acceptance)
  - [7.2 Automatic Rejection Conditions](#72-automatic-rejection-conditions)
  - [7.3 Tool Confidence Categories](#73-tool-confidence-categories)
  - [7.4 Minimum Expectations per Category](#74-minimum-expectations-per-category)
- [8. Summary](#8-summary)

---

# 0. Purpose

This master specification consolidates and replaces three prior documents:

1. **Compliance Automation Specification**
2. **SCEM v1.1 Tool-Assisted Templates**
3. **Toolchain Confidence Assessment (TCA) Requirements**

It is fully aligned with:
✅ CRSS Unified Safety Specification v3.0.0
✅ Compliance Master v3.0.1
✅ SCEM Master v3.0.0

This document defines:
- Tooling requirements
- Automation rules
- Evidence-generation workflows
- Toolchain qualification
- Data schemas & templates
- Acceptance criteria for automated outputs

It is the **single source of truth** for automation and tool usage in CRSS-Python certification.

---

# 1. Tooling Governance Model

## 1.1 Role of Tools in CRSS
Tools are used to:
- Analyze code
- Enforce rules
- Generate evidence
- Track Modes & Phases
- Validate SCEM artifacts
- Support certification audits

Tools **do not reduce** responsibility for correctness.

## 1.2 Tool Categories

| Category | Examples | Purpose |
|----------|----------|---------|
| Static Analysis | Rule checkers, linters | Detect violations |
| Mode Analysis | Propagation engines | Compute Modes |
| Test Automation | Coverage, MC/DC | Generate test evidence |
| Build & Baseline | Package lock, container builder | Freeze configuration |
| Monitoring | Determinism probes, timing checks | Validate runtime behavior |

---

# 2. Automation Requirements

## 2.1 Mandatory Automation Targets

Automation must support:
- Rule compliance checking
- Mode & Phase detection
- Dependency graph extraction
- Critical boundary validation
- Violation classification
- CBM generation
- SCEM completeness validation

## 2.2 Non-Automatable Components

The following require human review:
- Safety Level assignment
- Risk analysis for deviations
- Architecture safety rationale
- Final certification judgment

Human approval is mandatory for Strict-A.

---

# 3. Tool Capability Levels

## 3.1 Tool Confidence Levels (TCL)

| TCL | Name | Usage |
|-----|------|-------|
| **TCL-0** | Unverified | Not allowed in certification |
| **TCL-1** | Trusted Output with Review | Allowed with manual validation |
| **TCL-2** | Trusted Output | Allowed without manual review for Core/Strict |
| **TCL-3** | Safety-Critical Capable | Allowed for Strict-A evidence |

Strict-A requires **TCL-3** for:
- MC/DC reporting
- Determinism analysis
- Mode propagation validation

## 3.2 Tool Confidence Assessment (TCA)

TCA evaluates:
- Correctness
- Repeatability
- Version immutability
- Test coverage of the tool itself

A tool **cannot** be upgraded without:
- New TCA
- New baseline
- New certification

---

# 4. Automated Evidence Requirements

## 4.1 Mandatory Artifacts

Automation MUST generate:
- Rule Compliance Report (RCR)
- Mode Assignment Register (MAR)
- Critical Boundary Violations Report (CBVR)
- Propagation Report (PR)
- Coverage Report (CR)
- CBM Extract (baseline snapshot)
- SCEM Completeness Score

## 4.2 File Format Requirements

All automated outputs must be:
✅ Deterministic
✅ Machine-parsable
✅ Immutable after baseline
✅ Version-tagged

Recommended formats:
- YAML
- JSON
- CSV (tabular)

---

# 5. Toolchain Version Control

## 5.1 One-Version Rule

All tools used in certification:
✅ Must be version-fixed
✅ Must be captured in CBM
✅ Must not auto-update

## 5.2 Toolchain Drift = Automatic FAIL

If any tool changes version after CBM:
❌ All automated evidence is invalid
❌ Certification must restart

---

# 6. SCEM Tool-Assisted Templates

## 6.1 MAR Template

```yaml
- function: "module.Class.method"
  profile: "Strict"
  safety_level: "A"
  mode: "Strict-A"
  phase: "critical"
  calls:
    - "other.module.function"
  promoted_from: "Strict-B"
  reviewer: "Name"
```

## 6.2 Propagation Report Template

```yaml
propagation_events:
  - caller: "A"
    callee: "B"
    reason: "Data dependency"
    new_mode: "Strict-A"
    approved_by: "Reviewer"
```

## 6.3 Coverage Template

```yaml
coverage:
  mode: "Strict-A"
  critical_mcdc: 100
  unit_tests: 100
```

---

# 7. Tool Acceptance Criteria

This section defines how **Tool Capability Levels (TCL)** and **Tool Compliance Attributes (TCA)** map to a tool confidence story suitable for safety assessments.
CRSS does not define a full ISO 26262 Tool Confidence Level (TCL) process, but provides a structured approach that can be mapped onto it.

## 7.1 Automated Evidence Acceptance

Accepted only if:
✅ TCL level is sufficient
✅ Output matches CBM tool version
✅ Data is complete and valid
✅ No missing artifacts

## 7.2 Automatic Rejection Conditions

❌ Output generated after tool version drift
❌ Missing data fields
❌ Non-deterministic results
❌ Unsupported output formats

### 7.3 Tool Confidence Categories

Tools are grouped into three confidence categories:

- **Q0 — Advisory Tools**  
  - Linting, style checkers, non-safety-critical analyzers.  
  - Findings are advisory; no certification reliance.  

- **Q1 — Supporting Safety Evidence**  
  - Static analyzers, type checkers, coverage tools used to build SCEM evidence, but with cross-checks and manual review.  

- **Q2 — Safety-Critical Decision Tools**  
  - Tools whose output is directly used as *primary evidence* that safety requirements are met (e.g., the main CRSS compliance analyzer for Strict-A).  

### 7.4 Minimum Expectations per Category

**Q1 – Supporting Safety Evidence:**

- Fixed-version in CBM  
- No auto-update  
- Results cross-checked with at least one other tool or manual sampling  
- Failures cannot directly hide a violation; human review present  

**Q2 – Safety-Critical Decision Tools:**

- All Q1 expectations, plus:  
  - Documented failure modes and mitigations  
  - Validation on representative benchmark projects  
  - Periodic sanity checks (e.g., seeding synthetic violations and verifying detection)  
  - Transparent versioning and changelog  
  - Toolchain Version Registry entry in SCEM-D5  

Projects using a tool as Q2 MUST describe the tool confidence argument in SCEM (D3/D5) and optionally reference ISO 26262-8 / DO-330 style tool qualification documents.


---

# 8. Summary

This master specification:

✅ Centralizes all tooling and automation policy
✅ Defines confidence and acceptance levels
✅ Supports Strict-A certification workflows
✅ Ensures deterministic, auditable evidence
✅ Enforces one-version-per-toolchain policy

This is the mandatory reference for all CRSS-Python automation systems.

---
