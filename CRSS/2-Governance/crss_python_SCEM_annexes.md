# CRSS-Python SCEM Annexes

## Table of Contents

- [CRSS-Python SCEM Annexes](#crss-python-scem-annexes)
  - [0. Purpose](#0-purpose)
  - [1. Annex A — FMEA Template](#1-annex-a-fmea-template)
    - [A.1 FMEA Table](#a1-fmea-table)
    - [A.2 Rules](#a2-rules)
  - [2. Annex B — Hazard Log Template](#2-annex-b-hazard-log-template)
  - [3. Annex C — Safety Architecture Diagram Requirements](#3-annex-c-safety-architecture-diagram-requirements)
  - [4. Annex D — Auditor Checklist](#4-annex-d-auditor-checklist)
  - [5. Annex E — Timing Evidence Protocol](#5-annex-e-timing-evidence-protocol)
  - [6. Summary](#6-summary)

Version: v1.0.0
Status: Official Release
© 2025 Sofian Daghsen – All rights reserved

---

## 0. Purpose

This annex set formalizes templates, checklists, and required structures that support SCEM v1.0. These annexes ensure that safety cases are:

- Complete
- Auditable
- Repeatable
- Objective
- Evidence-driven

All Strict Level A systems MUST use these annexes.

---

## 1. Annex A — FMEA Template

### A.1 FMEA Table

| Field | Description |
|-------|-------------|
| Failure Mode ID | Unique identifier |
| Description | What fails |
| Cause | Root cause |
| Effect | Impact on system |
| Severity | Ranked 1–5 |
| Likelihood | Ranked 1–5 |
| Detection Method | How failure is detected |
| Mitigation | Design-level prevention |
| Safe State | Behavior on failure |
| Evidence | Test/proof reference |

### A.2 Rules

- All critical paths MUST have FMEA coverage
- Each mitigation MUST map to CRSS rule or design element
- Evidence MUST be recorded in TEP or PTR

---

## 2. Annex B — Hazard Log Template

| Field | Description |
|-------|-------------|
| Hazard ID | Unique identifier |
| Description | Hazard definition |
| Severity | Risk impact |
| Trigger | What activates hazard |
| Mitigation | Prevention |
| Residual Risk | Post-mitigation |
| Evidence | Linked proof |

---

## 3. Annex C — Safety Architecture Diagram Requirements

Diagrams MUST include:

- Data flow
- Trust boundaries
- Failure boundaries
- Primary vs supervisory roles
- Python architectural constraints

Format: PDF or PNG, under version control.

---

## 4. Annex D — Auditor Checklist

Auditors MUST verify:

- All SCEM artifacts exist
- All assumptions match deployment
- Zero-drift policy upheld
- All evidence hashed and versioned
- Deployment == Tested baseline

---

## 5. Annex E — Timing Evidence Protocol

See Formal Timing Methodology.

---

## 6. Summary

These annexes convert SCEM into a repeatable, certifiable workflow.
