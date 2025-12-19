# CRSS-Python Architecture Guide

**Version:** v1.0.0
**Status:** Informative
**Maturity:** Stable
© 2025 Sofian Daghsen – All rights reserved
Distributed under CC BY-NC-ND 4.0 — see LICENSE-CRSS.

---

## Table of Contents

- [1. Purpose](#1-purpose)
- [2. Core Architectural Principles](#2-core-architectural-principles)
  - [2.1 Isolation Over Complexity](#21-isolation-over-complexity)
  - [2.2 Process, Not Thread Isolation](#22-process-not-thread-isolation)
  - [2.3 Critical Code Must Be Minimal](#23-critical-code-must-be-minimal)
  - [2.4 Stateless-by-Default](#24-stateless-by-default)
  - [2.5 Defensive Boundaries](#25-defensive-boundaries)
- [3. Recommended System Architecture](#3-recommended-system-architecture)
- [4. Recommended Deployment Architecture](#4-recommended-deployment-architecture)
- [5. Module Design Templates](#5-module-design-templates)
  - [5.1 Critical Module](#51-critical-module)
  - [5.2 Non-Critical Module](#52-non-critical-module)
- [6. Data Flow Best Practices](#6-data-flow-best-practices)
- [7. Logging & Monitoring Strategy](#7-logging--monitoring-strategy)
- [8. Architecture Anti-Patterns (Avoid)](#8-architecture-anti-patterns-avoid)
- [9. Path to Strict-A Architecture](#9-path-to-strict-a-architecture)
- [10. Summary](#10-summary)


---

# 1. Purpose

This guide provides **practical architectural direction** for teams designing software under the CRSS-Python framework. It translates the rules and policies into **real design choices** that:

- Reduce risk
- Improve determinism
- Support certification
- Enable scalable, robust systems

This is NOT a rulebook — it is **highly recommended guidance** to help build systems that naturally align with CRSS-Python compliance.

---

# 2. Core Architectural Principles

## 2.1 Isolation Over Complexity
Prefer **small, isolated components** over large, multi-purpose modules.

- Single responsibility
- Clear boundaries
- Easier testing
- Easier certification

- Avoid monoliths with mixed responsibilities.

---

## 2.2 Process, Not Thread Isolation
For safety and determinism:

- Isolate components into **separate processes**
- Communicate via message passing or IPC
- Failures stay contained

Threads inside a shared interpreter increase unpredictability and risk.

---

## 2.3 Critical Code Must Be Minimal
`@critical` code should be:

- Small
- Deterministic
- Free of side effects
- Well-tested

Goal: **Make the critical core tiny, predictable, and rock-solid.**

---

## 2.4 Stateless-by-Default
State introduces danger. Prefer:

- Stateless processing
- Explicit state transitions
- Message-based workflows

If state is required:

- Track it explicitly
- Validate transitions
- Persist safely

---

## 2.5 Defensive Boundaries
All external inputs must be treated as untrusted.

- Validate
- Sanitize
- Range-check

Never expose critical logic directly to external inputs.

---

# 3. Recommended System Architecture

A CRSS-Python-compliant system typically uses:

```
+--------------------------+
|  External Environment    |
| (Sensors, APIs, Users)   |
+------------+-------------+
             |
             v
+--------------------------+
|  Input Validation Layer  |  (Non-Critical)
+------------+-------------+
             |
             v
+--------------------------+
|  Decision Logic Layer    |  (May contain @critical)
+------------+-------------+
             |
             v
+--------------------------+
|  Output Actuation Layer  |  (Non-Critical)
+--------------------------+
```

Key rules:

- Only the Decision Logic can contain `@critical`
- Actuation MUST be indirect (Python supervisory role)
- Validation occurs BEFORE critical execution

---

# 4. Recommended Deployment Architecture

```
+------------------------------+
|       Supervisory App        |
|      (CRSS-Python Strict)    |
+------------+-----------------+
             |
    Process-level IPC
             |
+------------v-----------------+
|     Actuation System         |
|   (Certified Primary Logic)  |
+------------------------------+
```

Python must not command actuators directly — it must supervise or recommend.

---

# 5. Module Design Templates

## 5.1 Critical Module

- No I/O
- No allocation
- No blocking calls
- Pure logic
- Small functions
- Deterministic branching

## 5.2 Non-Critical Module

- Initialization
- File/Network access
- Configuration loading
- Pre-computation

Still must follow rules — but more flexible.

---

# 6. Data Flow Best Practices

- Explicit schemas
- Range enforcement
- Type validation
- Use immutable data structures in critical paths

- No dynamic typing magic
- No unstructured blobs

---

# 7. Logging & Monitoring Strategy

Logging MUST NOT appear in `@critical`.

Recommended approach:

- Log ONLY in non-critical phases
- Use structured logs (JSON)
- Timestamp in UTC
- Secure write paths

---

# 8. Architecture Anti-Patterns (Avoid)

- Shared global state
- Circular dependencies
- Overloaded classes
- Dynamic imports
- Runtime configuration mutation
- Mixed criticality in same function

---

# 9. Path to Strict-A Architecture

Step 1 — Identify critical decisions
Step 2 — Isolate into a dedicated module
Step 3 — Shrink critical logic
Step 4 — Split phases (`@non_critical_phase`)
Step 5 — Pre-compute everything possible
Step 6 — Freeze toolchain and CBM

---

# 10. Summary

Good architecture makes compliance **easier, cheaper, and safer**.

CRSS-Python promotes:

- Simplicity
- Determinism
- Isolation
- Traceability

---
