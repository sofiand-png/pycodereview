# CRSS Phase-Aware Rule Interpretation Model

**Version:** v1.0.0
**Status:** Informative
**Maturity:** Stable
© 2025 Sofian Daghsen - All rights reserved
Distributed under CC BY-NC-ND 4.0 - see LICENSE-CRSS.


**This document is NON-NORMATIVE.**
It provides interpretation, rationale, and examples for the phase-related
rules defined normatively in:
- crss_python_standard_safety_master.md
In case of any discrepancy, the Master specification SHALL prevail.

This document MUST NOT introduce new requirements beyond those in the Master.


---

## Table of Contents
- [CRSS Phase-Aware Rule Interpretation Model](#crss-phase-aware-rule-interpretation-model)
  - [Table of Contents](#table-of-contents)
  - [0. Scope of this document](#0-scope-of-this-document)
  - [1. Interpretation in `@critical` Code](#1-interpretation-in-critical-code)
    - [Forbidden in Critical Code](#forbidden-in-critical-code)
    - [Critical Code Principle](#critical-code-principle)
  - [2. Interpretation in Non-Critical Code](#2-interpretation-in-non-critical-code)
    - [[OK] Permitted in Non-Critical Code](#ok-permitted-in-non-critical-code)
  - [3. Meaning for Compliance Tools](#3-meaning-for-compliance-tools)
    - [Tool Interpretation Matrix](#tool-interpretation-matrix)
  - [4. Meaning for Human Review](#4-meaning-for-human-review)
  - [5. Meaning for Runtime / Architecture](#5-meaning-for-runtime-architecture)
  - [Summary](#summary)

---

A rule marked **`Scope: all_code (phase-aware)`** **shall be interpreted using the following principles**.

---

## 0. Scope of this document

This document defines normative semantics for CRSS execution phases
(e.g. `@critical`, `@non_critical_phase`) and the interpretation of
Master-spec rules within those phases.

This document does NOT redefine:
- safety levels,
- profiles,
- call or import legality,
- data-flow architecture,
- output semantics.

In case of any conflict, the CRSS Master Specification SHALL prevail.


## 1. Interpretation in `@critical` Code
Applicable to:

- Strict-A critical functions
- Core-profile code explicitly marked as critical (Core-critical)
- Any function identified as critical in the Mode Assignment Register (MAR)

When inside a **critical execution phase**, a phase-aware rule is enforced at **maximum strictness**:

### Forbidden in Critical Code

- **I/O of any kind**
  - filesystem
  - network
  - database
  - IPC
- **Blocking operations**
  - locks
  - waits
  - condition variables
  - blocking queues
- **Dynamic memory allocation** beyond trivial proven-bounded temporaries
- **Subprocess invocation / OS commands**
- **Environment variable access**
- **Runtime scheduling-dependent behavior**
- **Operations that may trigger GC**
- **Unbounded or non-deterministic timing operations**
- **String or collection growth** beyond statically provable limits
- **Cache interaction** except read-only access to bounded structures
- **Interaction with external systems** of any kind

### Critical Code Principle

> **Critical = deterministic, bounded, allocation-free, I/O-free, and timing-safe.**

---

## 2. Interpretation in Non-Critical Code

Phase-aware rules still apply, but with **operational relaxation**.

### [OK] Permitted in Non-Critical Code

- File / network I/O
- Memory allocation & object creation
- Caching, buffering, lookup tables
- Subprocess invocation
- Configuration loading
- Platform / environment access

However, these allowances are valid only if:

1. **All other rule semantics remain respected**
   - (e.g., security, correctness, boundedness, purity constraints)

2. **No dynamic / non-deterministic behavior leaks into critical execution**
   - results must be validated
   - results must be frozen or immutable before entering critical execution

3. **Non-critical effects MUST NOT occur during a critical phase**
   - All external interactions must happen strictly **before** or **after** each critical call.

---

## 3. Meaning for Compliance Tools

A **phase-aware rule** MUST be evaluated in two contexts:

###  Tool Interpretation Matrix

| Context     | Required Interpretation                                                                                 |
|-------------|----------------------------------------------------------------------------------------------------------|
| **Critical**     | *Stricter interpretation:* I/O forbidden, allocation forbidden, boundedness MUST be statically provable, determinism required |
| **Non-Critical** | *Normal interpretation:* I/O & allocation allowed, but rule semantics still enforced; must ensure no leakage into critical |

Tools must:

- identify critical regions (via annotations: `@critical`, MAR rules)
- verify phase-appropriate enforcement
- ensure purity and determinism of critical paths
- ensure non-critical behavior cannot influence timing or semantics of critical execution

---

## 4. Meaning for Human Review

Human reviewers must apply this principle:

> **A phase-aware rule changes only its interpretation, never its presence.**

Meaning:

- The **rule still applies** in all code.
- Only the **strictness** changes depending on phase.
- No code segment is exempt from phase-aware rules.

---

## 5. Meaning for Runtime / Architecture

A phase-aware rule MUST guarantee:

- **No critical execution path is polluted** by non-deterministic behavior originating from non-critical code.
- **All non-critical effects occur strictly outside critical execution windows.**
- **MAR boundaries are respected**:
  - If MAR classifies a function as critical, phase-aware strictness applies.
  - If MAR classifies a function as non-critical, relaxed interpretation applies - but rule still applies.

> **Phase boundaries (critical / non-critical) are architectural-
> not dynamic, not implicit, not inferred by tools.**

---

## Summary

This model ensures:

- Deterministic and analyzable critical behavior
- Safe operational flexibility outside critical regions
- No surprises for tooling or certification reviewers
- Full alignment with CRSS Mode semantics (Core/Strict × Phase)

It is now the **normative interpretation model** used across CRSS-Python for any rule tagged with: