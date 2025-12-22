# Annex E — Formal Timing Methodology (FTM)

**Version:** v1.0.0  
**Status:** Normative
**Maturity:** Stable
© 2025 Sofian Daghsen - All rights reserved  
Distributed under CC BY-NC-ND 4.0 - see LICENSE-CRSS.

---

<a id="toc"></a>
## Table of Contents

- [1. Purpose and Scope](#1-purpose-and-scope)
- [2. Fundamental Position on Timing](#2-fundamental-position-on-timing)
- [3. Definitions](#3-definitions)
- [4. Timing Evidence Objectives](#4-timing-evidence-objectives)
- [5. Applicability by CRSS Profile](#5-applicability-by-crss-profile)
- [6. Formal Timing Evidence Model](#6-formal-timing-evidence-model)
  - [6.1 Identified Timing-Critical Paths](#61-identified-timing-critical-paths)
  - [6.2 Deterministic Structure Evidence](#62-deterministic-structure-evidence)
  - [6.3 Bounded Execution Evidence](#63-bounded-execution-evidence)
- [7. Measurement and Observation Rules](#7-measurement-and-observation-rules)
- [8. What Is Explicitly NOT Claimed](#8-what-is-explicitly-not-claimed)
- [9. Required Artifacts](#9-required-artifacts)
- [10. Auditor Interpretation Guidance](#10-auditor-interpretation-guidance)
- [11. Summary](#11-summary)

---

## 1. Purpose and Scope

This annex defines the **Formal Timing Methodology (FTM)** used in CRSS-Python
to provide **objective, reviewable timing evidence** for safety-relevant software.

FTM applies to:

- supervisory control logic,
- safety monitoring and arbitration,
- bounded decision-making paths,
- Strict and Strict-Level-A systems.

This methodology **does NOT attempt to establish hard real-time guarantees or WCET**.

---

## 2. Fundamental Position on Timing

CRSS-Python explicitly recognizes that:

- CPython does **not** provide analyzable hard WCET,
- general-purpose operating systems introduce scheduling variability,
- garbage collection and interpreter behavior cannot be statically bounded.

Therefore, CRSS adopts a **timing confidence model**, not a real-time proof model.

Timing evidence demonstrates:

- bounded structure,
- bounded work per cycle,
- absence of unbounded constructs,
- stable observed execution under defined conditions.

---

## 3. Definitions

**Timing-Critical Path**  
A code path whose execution time may influence safety decisions,
timeouts, watchdogs, or degraded-mode transitions.

**Bounded Execution**  
Execution whose upper complexity is structurally limited
(e.g., fixed loops, no recursion, bounded data sizes).

**Timing Evidence**  
Measured or reasoned data demonstrating predictable execution
behavior under defined operational assumptions.

---

## 4. Timing Evidence Objectives

The Formal Timing Methodology aims to demonstrate that:

1. All safety-relevant execution paths are **structurally bounded**.
2. No unbounded loops, recursion, or data growth exists in critical paths.
3. Execution occurs within **defined time budgets** under nominal conditions.
4. Timing assumptions are explicit, documented, and reviewable.
5. Failure or delay results in **safe degradation**, not unsafe actuation.

---

## 5. Applicability by CRSS Profile

| Profile | Formal Timing Evidence Required |
|--------|--------------------------------|
| Core | Optional (recommended if safety-relevant) |
| Strict | Mandatory for safety-relevant paths |
| Strict Level A | Mandatory for all `@critical` paths |

---

## 6. Formal Timing Evidence Model

FTM is based on **three complementary evidence layers**.

### 6.1 Identified Timing-Critical Paths

Projects SHALL:

- identify all timing-relevant functions,
- document trigger conditions,
- document expected execution frequency.

This information SHALL appear in the SCEM and/or PTR.

---

### 6.2 Deterministic Structure Evidence

For each timing-critical path, the project SHALL demonstrate:

- no unbounded loops,
- no recursion,
- bounded collection sizes,
- no dynamic dispatch based on unvalidated input,
- no blocking I/O in critical paths.

This evidence is typically provided by:

- code inspection,
- static analysis,
- rule compliance results.

---

### 6.3 Bounded Execution Evidence

Projects SHALL provide **observational timing data**, such as:

- execution time measurements under controlled conditions,
- repeated runs with worst-case input sizes,
- execution envelopes (min / max / percentile).

Measurements SHALL:

- be performed on the declared deployment platform,
- use the declared interpreter version,
- include environmental assumptions.

This evidence **does not constitute WCET**.

---

## 7. Measurement and Observation Rules

Timing measurements SHALL observe the following rules:

- measurements MUST NOT alter control flow,
- instrumentation MUST NOT be present in certified code paths,
- wall-clock and monotonic clocks MAY be used,
- results MUST be repeatable within defined tolerance.

Statistical summaries MAY be used, but raw data MUST be retained.

---

## 8. What Is Explicitly NOT Claimed

The Formal Timing Methodology does **NOT** claim:

- hard real-time determinism,
- cycle-accurate execution bounds,
- OS-level scheduling guarantees,
- GC pause elimination,
- compliance with RTOS standards.

Any claim beyond these limits is **out of CRSS scope**.

---

## 9. Required Artifacts

The following artifacts SHALL reference Formal Timing Evidence:

- Performance & Timing Report (PTR),
- Safety Case (SCEM),
- Rule Compliance Report (RCR),
- Test Evidence Package (TEP).

All timing assumptions SHALL be traceable.

---

## 10. Auditor Interpretation Guidance

Auditors SHOULD verify that:

- timing-critical paths are explicitly identified,
- structural bounds are clearly demonstrated,
- observed timing is consistent with system role,
- delays result in safe fallback behavior,
- no real-time claims are implied.

Absence of WCET claims is **intentional and correct**.

---

## 11. Summary

The Formal Timing Methodology provides:

- defensible timing confidence,
- bounded execution reasoning,
- transparent assumptions,
- auditor-friendly evidence.

It enables Python-based systems to be **used safely in supervisory
and safety-adjacent roles without misrepresenting real-time guarantees**.
