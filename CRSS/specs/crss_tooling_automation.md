
# CRSS-Python Tooling & Automation Master Specification  
Version: v3.0.0  
Status: Normative  
© 2025 Sofian Daghsen – All rights reserved  

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
