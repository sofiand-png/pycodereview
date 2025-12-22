# CRSS-Python Strict Profile

**Version:** v1.0.0
**Status:** Normative
**Maturity:** Stable
© 2025 Sofian Daghsen - All rights reserved
Distributed under CC BY-NC-ND 4.0 - see LICENSE-CRSS.

---

<a id="toc"></a>
## Table of Contents

- [1. Introduction](#1-introduction)
- [2. Relation to Core Profile and Intention](#2-relation-to-core-profile-and-intention)
- [3. Strengthened Rules From Core To Strict](#3-strengthened-rules-from-core-to-strict)
- [4. Core Language Usage](#4-core-language-usage)
  - [4.1 Type System Restrictions](#41-type-system-restrictions)
- [5. Error Handling, Exceptions and Control Flow](#5-error-handling-exceptions-and-control-flow)
  - [5.1 Looping and Termination](#51-looping-and-termination)
  - [5.2 Timing and Blocking Constraints](#52-timing-and-blocking-constraints)
- [6. Types, Data and Interfaces](#6-types-data-and-interfaces)
  - [6.1 Object Design and Allocation Rules](#61-object-design-and-allocation-rules)
- [7. Robustness and Portability](#7-robustness-and-portability)
  - [7.1 Imports and Isolation](#71-imports-and-isolation)
- [8. Maintainability and Documentation](#8-maintainability-and-documentation)
  - [8.1 Module Design](#81-module-design)
- [9. Testing and Coverage Guidelines](#9-testing-and-coverage-guidelines)
  - [9.1 Verification and Evidence](#91-verification-and-evidence)

---

## 1. Introduction

> [⬆ Back to Table of Contents](#toc)


### 0.1 Purpose and Objectives

The **CRSS-Python Strict** profile defines a safety-oriented subset of Python designed for:

- Runtime-critical logic
- Safety-sensitive behavior
- Mission-critical decision paths
- High-assurance data transformations

Its primary goals are:

- **Prevent classes of runtime failures**
  by restricting language constructs that are dynamic, ambiguous, or difficult to reason about.

- **Enable predictable and analyzable control flow**
  suitable for formal review, static analysis, and high-coverage testing (e.g., MC/DC).

- **Increase reliability and security**
  through disciplined type usage, defensive checks, and restricted state mutation.

- **Support auditability and certification**
  by requiring traceability, deviation documentation, and repeatable compliance evidence.

- **Reduce ambiguity in multi-team environments**
  by enforcing a consistent coding model for critical components.

### 0.1 What Strict Is Not

- It is **not** a general-purpose coding style guide.
- It **does not** guarantee system safety on its own.
- It **does not** replace architectural reviews, testing, or verification.
- It **does not** forbid Python in non-critical layers.

**Strict** defines rules only for critical units and strengthens Core rules to achieve higher assurance.

------------------------------------------------------------------------

------------------------------------------------------------------------

---

## 2. Relation to Core Profile and Intention

> [⬆ Back to Table of Contents](#toc)

CRSS Strict reuses the rule catalog defined in
`crss_python_core.md`. For each rule `CRSS-x.y.z`:

- Core specifies a **baseline** level (MUST / SHOULD / MAY).
- Strict may:
  - keep the same level,
  - or **strengthen** it (for example, Core: SHOULD-NOT --> Strict: MUST-NOT).

In addition, Strict introduces rules that are **Strict-only**
(Core: N/A, Strict: MUST/SHOULD).

Strict code is expected to be:

- a **subset of Core-compliant Python**, and
- close in spirit to subsets used under standards like DO-178C, ISO 26262,
  IEC 61508, and MISRA.

The **Strict** profile is not intended for all Python code in a project.

- Typical projects will have the majority of code in **Core** (e.g. 70-90%),
  and a smaller subset in **Strict** (e.g. 10-30%) for critical logic.
- Strict code is expected to be **less "Pythonic" and more "safety-subset"**:
  dynamic features, lambdas, casts, and nondeterministic randomness are
  deliberately constrained or forbidden.
- Critical code **cannot** be evaluated under a weaker profile.

Strict should be applied to:

- `@critical` functions and classes,
- modules implementing safety or mission-critical behavior,
- units where MC/DC, traceability and strong guarantees are required.

The rest of the codebase can and should remain in the **Core** profile,
where Python idioms are more freely used under controlled rules.

### 1.1 Rule ID and Chapter Mapping

The Strict profile shares the same rule catalog and chapter structure as
the Core profile (see `crss_python_core.md`, section 0.2):

- **3.x**  - Core Language and Dynamic Features
- **4.x**  - Error Handling and Control Flow
- **5.1x** - Types and Interfaces
- **5.2x** - State and Global Effects
- **5.3x** - Randomness and Determinism
- **5.4x** - Memory, Collections and Resources
- **6.x**  - Security
- **7.x**  - Robustness and Portability
- **8.x**  - Maintainability and Documentation
- **9.x**  - Testing, Coverage and Process
- **10.x** - Python Versioning and Tooling
- **11.chapter_id_[3..10].x** - Strict only rules

All rule IDs in the 3.x-10.x ranges are owned by the **Core** catalog.
Strict:

- reuses those IDs with stronger profile levels (for example, SHOULD -> MUST), and
- introduces additional **Strict-only** rules in the dedicated
  `CRSS-11.x.x` namespace (Core: N/A, Strict: MUST/SHOULD/MUST-NOT).

### 1.2 Criticality Levels

Criticality levels (Level A/B/C) are defined in the Core profile
(section 9.0). In summary:

- **Level A (Safety Critical)** units are expected to use the **Strict** profile
  and comply with all Strict process rules (including MC/DC and traceability).
- **Level B (High Integrity)** units should use Strict or an enhanced Core
  profile with strong testing and traceability.
- **Level C (Standard)** units typically use the Core profile.

### 1.3 Companion Documents

The Strict profile shares the same rule catalog as Core and refines behaviour
through additional rules and stronger levels.

Import, inheritance, deviation and criticality behaviour are detailed in:

- `docs/annexes/crss_import_policy.md`
- `docs/annexes/crss_inheritance_policy.md`
- `docs/annexes/crss_exceptions_deviations.md`
- `docs/annexes/crss_critical_annotation.md`
- `docs/annexes/crss_versioning_and_rule_stability.md`

### 1.4 Python Version Scope and Relation to Core

CRSS-Python Strict v1.0.0 is defined as a strengthening of the
CRSS-Python Core profile. It inherits the same interpreter and Python

Declaring a Strict profile does not change the supported version range,
it only increases rule strength.

version assumptions:

- **Interpreter:** CPython
- **Supported Python versions (normative):** 3.9-3.12 (inclusive)

All rules in this document apply only within that range. Use of
CRSS-Strict outside this range is not covered by the specification.

Projects that adopt the Strict profile **MUST** also declare their own
Python version target, using the same project-declared model as Core:

- `target_python_version` - expected supported Python version

The following constraints apply:

1. The declared target python version **MUST** be declared in the CRSS-Strict
   supported range (3.9-3.12 for v1.0.0).

2. When a unit or module is treated as **critical** (e.g. by annotation or
   configuration), the applicable profile is Strict, regardless of the
   global project profile. Version-related rules for Strict SHALL still
   respect the project-declared Python range.

3. Tooling MAY refuse to analyse projects whose declared Python range lies
   outside the CRSS-Strict supported interval, or MAY treat such analysis
   as non-compliant.

For detailed behaviour of project-declared version ranges, rule evolution,
and profile selection, see the Core specification chapter 10 and the
*Versioning and Rule Stability* annex.

------------------------------------------------------------------------

---

## 3. Strengthened Rules From Core To Strict

> [⬆ Back to Table of Contents](#toc)


The following existing rules from the Core catalog are strengthened in
the Strict profile:

| RULE ID     | Description                                  | Core Level   | Strict Level   | Note |
|-------------|----------------------------------------------|--------------|----------------|------|
| CRSS-3.1.2  | Constrain dynamic imports                      | SHOULD-NOT   | MUST-NOT       |      |
| CRSS-3.1.3  | No runtime monkeypatching of imported modules  | SHOULD-NOT   | MUST-NOT       |      |
| CRSS-3.1.4  | Limit lambda usage to simple local expressions | SHOULD-NOT   | MUST-NOT       |      |
| CRSS-3.2.1  | Reflection shall not drive high-level contr... | SHOULD-NOT   | MUST-NOT       |      |
| CRSS-3.2.2  | globals/locals/vars for introspection only     | SHOULD-NOT   | MUST-NOT       |      |
| CRSS-3.2.3  | Cross-profile import policy                    | SHOULD       | MUST           |      |
| CRSS-3.3.1  | Assignment expressions (walrus) limited / f... | SHOULD-NOT   | MUST-NOT       |      |
| CRSS-3.4.1  | Inheritance across profiles                    | SHOULD       | MUST           |      |
| CRSS-4.1.1  | Assertions not for runtime validation          | SHOULD-NOT   | MUST-NOT       |      |
| CRSS-4.2.2  | except Exception requires explicit handling    | SHOULD-NOT   | MUST-NOT       |      |
| CRSS-4.2.3  | Exceptions shall not be used for normal con... | SHOULD-NOT   | MUST-NOT       |      |
| CRSS-4.2.4  | Preserve exception context when re-raising     | SHOULD       | MUST           |      |
| CRSS-4.3.1  | Avoid multiple evaluations of function call... | SHOULD-NOT   | MUST-NOT       |      |
| CRSS-4.3.2  | Loop conditions should be free of hidden si... | SHOULD       | MUST           |      |
| CRSS-4.3.4  | Avoid late-bound closures over loop variables  | SHOULD       | MUST           |      |
| CRSS-4.3.5  | Handle async task failures and cancellation explicitly | SHOULD       | MUST           |      |
| CRSS-5.1.1  | Type hints on public APIs                      | SHOULD       | MUST           |      |
| CRSS-5.1.2  | Constrain use of Any                           | SHOULD-NOT   | MUST-NOT       |      |
| CRSS-5.1.5  | Restrict use of `typing.cast`                  | SHOULD-NOT   | MUST-NOT       |      |
| CRSS-5.1.7  | Ban mutable default arguments                  | SHOULD-NOT   | MUST-NOT       |      |
| CRSS-5.1.8  |  Use is only for None and singletons                  | SHOULD-NOT   | MUST-NOT       |      |
| CRSS-5.2.1  | Avoid hidden mutable global state              | SHOULD-NOT   | MUST-NOT       |      |
| CRSS-5.2.2  | No implicit side effects on import             | SHOULD-NOT   | MUST-NOT       |      |
| CRSS-5.3.1  | Constrain nondeterministic random number ge... | SHOULD-NOT   | MUST-NOT       |      |
| CRSS-5.3.2  | No nondeterministic randomness in Strict code  | SHOULD-NOT   | MUST-NOT       |      |
| CRSS-5.3.3  | Cryptographic-strength randomness only via ... | SHOULD       | MUST           |      |
| CRSS-5.3.6  | Unified internal time representation (UTC)     | SHOULD       | MUST           |      |
| CRSS-5.3.7  | Ban on naive datetimes in cross-boundary logic | SHOULD-NOT   | MUST-NOT       |      |
| CRSS-5.3.8  | Controlled date parsing and formatting         | SHOULD       | MUST           |      |
| CRSS-5.3.9  | Declared numeric precision and tolerance       | SHOULD       | MUST           |      |
| CRSS-5.3.10  | Prefer fixed-point or decimal for exact dom... | SHOULD       | MUST           |      |
| CRSS-5.4.1  | Avoid unbounded growth of in-memory collect... | SHOULD       | MUST           |      |
| CRSS-5.4.2  | Explicit lifecycle for large objects and bu... | SHOULD       | MUST           |      |
| CRSS-5.4.3  | Resource pools and caches must support expl... | SHOULD       | MUST           |      |
| CRSS-6.1.2  | Hardcoded secrets                              | SHOULD-NOT | MUST-NOT    |      |
| CRSS-6.2.1  | Insecure HTTP and disabled TLS verification    | SHOULD-NOT   | MUST-NOT       |      |
| CRSS-6.3.1  | Input validation for external data             | SHOULD       | MUST           |      |
| CRSS-7.1.1  | Explicit encoding for text file I/O            | SHOULD       | MUST           |      |
| CRSS-7.1.3  | Maximum length for external string inputs      | SHOULD       | MUST           |      |
| CRSS-7.1.4  | Encoding and Unicode handling                  | SHOULD       | MUST           |      |
| CRSS-7.1.5  | Special character and control character val... | SHOULD       | MUST           |      |
| CRSS-7.1.6  | Language and locale configuration              | MAY          | SHOULD         |      |
| CRSS-7.6.1  | Explicit architecture definition               | SHOULD       | MUST           |      |
| CRSS-7.6.2  | Architecture Decision Records (ADR)            | SHOULD       | MUST           |      |
| CRSS-7.6.4  | Bounded retries and timeouts for network calls | SHOULD       | MUST           |      |
| CRSS-7.6.6  | Architecture responsibility and approval roles | SHOULD       | MUST           |      |
| CRSS-7.7.1  | No unmanaged global single connection for s... | SHOULD-NOT   | MUST-NOT       |      |
| CRSS-7.7.2  | Connection health check before use             | SHOULD       | MUST           |      |
| CRSS-7.7.3  | Bounded reconnect policies                     | SHOULD       | MUST           |      |
| CRSS-7.7.4  | Safe file transfer preconditions               | SHOULD       | MUST           |      |
| CRSS-8.1.1  | Limit cyclomatic complexity                    | SHOULD       | MUST           |      |
| CRSS-8.1.2  | Require docstrings on public APIs              | SHOULD       | MUST           |      |
| CRSS-8.2.1  | Do not shadow Python builtins or core types    | SHOULD-NOT   | MUST-NOT       |      |
| CRSS-9.1.1  | Target high branch coverage                    | SHOULD       | MUST           |      |
| CRSS-9.4.1  | Guideline Compliance Summary (GCS)             | SHOULD       | MUST           |      |
| CRSS-10.1.2  | Static analysis uses the declared target ve... | SHOULD       | MUST           |      |
| CRSS-10.1.3  | No usage of features newer than the minimum... | SHOULD-NOT   | MUST-NOT       |      |
| CRSS-10.1.4  | No use of removed or deprecated-in-target f... | SHOULD-NOT   | MUST-NOT       |      |
| CRSS-10.2.1  | Analysis Python version may differ, but mus... | SHOULD       | MUST           |      |
| CRSS-4.4.1   | Index bounds validation on externally derived indices | SHOULD   | MUST   |      |
| CRSS-4.4.2   | Safe dictionary access for external keys | SHOULD   | MUST   |      |
| CRSS-4.4.3   | Safe unpacking and length assumptions | SHOULD   | MUST   |      |
| CRSS-5.5.1   | Bounded memory usage for bulk data | SHOULD   | MUST   |      |
| CRSS-5.5.2   | Chunked processing and pagination | SHOULD   | MUST   |      |
| CRSS-5.5.3   | Query efficiency and index awareness | SHOULD   | SHOULD (MUST when DB load affects safety)   |      |
| CRSS-5.6.1   | Explicit cache policy and scope | SHOULD   | MUST   |      |
| CRSS-5.6.2   | Bounded cache size and eviction policy | SHOULD   | MUST   |      |
| CRSS-5.6.3   | Freshness requirements for cached safety-relevant data | SHOULD   | MUST   |      |
| CRSS-5.6.4   | Defined behavior on cache miss/failure | SHOULD   | MUST   |      |
| CRSS-5.6.5   | No hidden dependence on cache availability | SHOULD   | MUST   |      |
| CRSS-6.4.1   | Data classification and tagging | SHOULD   | MUST   |      |
| CRSS-6.4.2   | Encryption in transit and at rest for sensitive data | SHOULD   | MUST   |      |
| CRSS-6.4.3   | Redaction and minimization in logs | SHOULD   | MUST   |      |
| CRSS-6.4.4   | Access control for sensitive data flows | SHOULD   | MUST   |      |
| CRSS-6.4.5   | Approved key exchange and storage | SHOULD   | MUST   |      |
| CRSS-6.4.6   | Key rotation and expiry | SHOULD   | MUST   |      |
| CRSS-6.4.7   | No long-lived caching of sensitive data | SHOULD   | MUST   |      |
| CRSS-6.4.8   | Cache isolation between tenants/security domains | SHOULD   | MUST  |      |
| CRSS-7.8.1   | Stable service contracts and versioning | SHOULD   | MUST   |      |
| CRSS-7.8.2   | Bounded payload sizes and rates | SHOULD   | MUST   |      |
| CRSS-7.8.3   | Circuit breakers and backpressure for critical dependencies | SHOULD   | MUST   |      |
| CRSS-7.8.4   | Latency budgets for critical network operations | SHOULD   | MUST   |      |
| CRSS-7.8.5   | Distributed cache consistency for critical data | SHOULD   | MUST   |      |
| CRSS-7.8.6   | Cache is never the source of truth | SHOULD   | MUST   |      |
| CRSS-7.8.7   | Explicit HTTP caching directives | SHOULD   | MUST for HTTP APIs   |      |
| CRSS-7.9.1   | Strict JSON parsing and schema validation | SHOULD   | MUST   |      |
| CRSS-7.9.2   | Explicit CSV dialect and header handling | SHOULD   | MUST   |      |
| CRSS-7.9.3   | Handling malformed or binary-like text input | SHOULD   | MUST   |      |
| CRSS-7.9.4   | Detection of partial network writes and reads | SHOULD   | MUST   |      |
| CRSS-7.9.5   | Integrity checks for critical transfers | SHOULD   | MUST   |      |
| CRSS-7.9.6   | Safe behavior on mid-operation disconnection | SHOULD   | MUST   |      |
| CRSS-7.10.1  | Restricted operating system interaction | SHOULD   | MUST   |      |
| CRSS-7.10.2  | Environment variables as configuration inputs | SHOULD   | MUST   |      |
| CRSS-7.10.3  | No hidden behavior toggles in environment | SHOULD-NOT   | MUST-NOT   |      |

Strict-compliant code must therefore be a **subset** of Core-compliant
code.

The rules in all the next sections apply **only** in the Strict profile. For clarity,
they are described here (Core: N/A, Strict: MUST/SHOULD/MUST-NOT).

------------------------------------------------------------------------

---

## 4. Core Language Usage

> [⬆ Back to Table of Contents](#toc)


### 4.1 Type System Restrictions

### CRSS-11.3.3 - Structural typing prohibited in Strict code (Strict-only)
-   **Profiles**:
    -   Core: ** N/A
    -   Strict: ** MUST NOT
-   **Scope**: `all_code`

- **Category:** Type System Discipline
- **Type:** Static
- **Profiles:**

In Strict code (including critical units), **structural typing SHALL NOT be
used.** This includes, but is not limited to:

- `Protocol` and `@runtime_checkable`
- structural subtyping based on attribute “shape”
- complex polymorphism driven by `TypeVar` or inferred structural interfaces

Strict units SHALL use **nominal types only**, such as:

- explicit classes and abstract base classes (ABCs)
- declared inheritance hierarchies
- simple, non-polymorphic generics (e.g. `list[int]`, `dict[str, int]`)

**Rationale**:

Structural typing:

- makes behavioral contracts implicit
- complicates static analysis
- undermines interface traceability
- increases risk of hidden polymorphism
- reduces predictability required for safety certification

Strict requires **explicit, verifiable, nominal interfaces**.

---

## 5. Error Handling, Exceptions and Control Flow

> [⬆ Back to Table of Contents](#toc)


### 5.1 Looping and Termination

### CRSS-11.4.1 - Loops must be demonstrably bounded
-   **Category**: Control Flow
-   **Type**: Static / Process
-   **Profiles**:
    -   Core: N/A
    -   Strict: MUST
-   **Scope**: `all_code`

All loops in Strict units must be demonstrably finite:

- `for` loops must iterate over clearly finite iterables.
- `while` loops must have termination conditions that are statically
  understandable and converge under all expected operating conditions.

### CRSS-11.4.2 - No raw `while True` loops
-   **Category**: Control Flow
-   **Type**: Static
-   **Profiles**:
    -   Core: N/A
    -   Strict: MUST-NOT
-   **Scope**: `all_code`

Raw `while True:` loops are forbidden in Strict modules, except for a
small set of documented infrastructure patterns explicitly reviewed at
system level (for example, event loop wrappers).

### CRSS-11.4.3 - No unbounded recursion in Strict code
-   **Category**: Control Flow
-   **Type**: Static / Process
-   **Profiles**:
    -   Core: N/A
    -   Strict: MUST
-   **Scope**: `all_code`

Recursive functions in Strict code must have statically evident depth
bounds (e.g. recursion limited by a small constant or input bound) or
be refactored to iterative forms with explicit bounds. Deep or
data-dependent recursion is not allowed.

### 5.2 Timing and Blocking Constraints

### CRSS-11.4.5 - No dependence on scheduling or GC timing
-   **Category**: Runtime Behavior
-   **Type**: Process / Static (partial)
-   **Profiles**:
    -   Core: N/A
    -   Strict: MUST
-   **Scope**: `all_code`

Strict code must not rely on:

- thread scheduling order,
- garbage-collector timing,
- or other non-deterministic runtime behavior

to maintain correctness. Any concurrency must be designed so that all
valid schedules are safe.

### CRSS-11.4.6 - Documented execution bounds for Strict units
-   **Category**: Control Flow / Timing
-   **Type**: Process
-   **Profiles**:
    -   Core: N/A
    -   Strict: MUST
-   **Scope**: `critical`

For each @critical function / Strict Level A unit:

The design shall document:
- maximum number of loop iterations,
- maximum size of data structures processed,
- expected worst-case call frequency.
- Tests and reviews shall confirm that the implementation matches these bounds.

**Rationale**

Makes WCET approximation possible by combining structural bounds with empirical measurements.

### CRSS-11.4.7 - No blocking operations in Strict units
-   **Category**: Control Flow / OS Interaction
-   **Type**: Static / Process
-   **Profiles**:
    -   Core: N/A
    -   Strict: MUST-NOT
-   **Scope**: `all_code`

Strict units shall not perform operations that can block indefinitely or for unbounded durations, including:
- time.sleep, threading.Event.wait, Condition.wait, blocking I/O, or network calls,
- acquisition of locks that may be held by non-Strict or lower-criticality code.

Any waits or blocking must be confined to non-critical coordination layers, with explicit timeouts and safe fallback strategies.

**Rationale**

Blocking destroys timing guarantees and can deadlock critical loops.

### CRSS-11.4.8 - No dependence on wall-clock time for correctness
-   **Category**: Control Flow / Determinism
-   **Type**: Static / Process
-   **Profiles**:
    -   Core: N/A
    -   Strict: MUST-NOT
-   **Scope**: `all_code`

Strict units shall not use wall-clock time (e.g. time.time(), datetime.now()) to determine core safety decisions. Time-based behavior in Strict code must:
- rely on monotonic tick counters or externally provided timing signals, and
- be designed so that jitter or clock skew cannot cause unsafe states

**Rationale**

External clock behavior is platform-dependent and vulnerable to drift, NTP jumps, etc. Critical correctness must not depend on it.

---

## 6. Types, Data and Interfaces

> [⬆ Back to Table of Contents](#toc)


### 6.1 Object Design and Allocation Rules

### CRSS-11.5.1 - Object-oriented design restrictions
-   **Category**: Design / Types
-   **Type**: Static / Process
-   **Profiles**:
    -   Core: N/A
    -   Strict: MUST
-   **Scope**: `all_code`

In Strict modules:

- Multiple inheritance is forbidden. Single inheritance is allowed but
  should be shallow (1-2 levels).
- Dynamic attribute creation (e.g. `obj.new_attr = ...` where `new_attr`
  is not declared in `__init__`) is forbidden.
- Operator overloading is discouraged; projects may opt to forbid it
  completely in Strict zones.

### CRSS-11.5.2 - Decorator whitelist (Strict-only)
-   **Category**: Design / Language Usage
-   **Type**: Static
-   **Profiles**:
    -   Core: N/A
    -   Strict: MUST
-   **Scope**: `all_code`

Only a small, vetted set of decorators may be used in Strict code,
for example:

- `@critical` (marker),
- `@staticmethod`,
- `@classmethod`,
- `@dataclass` (with documented restrictions).

All other decorators must either be banned or explicitly justified and
documented as deviations.

### CRSS-11.5.3 - No I/O in core computational logic - I/O vs Critical and Non-Critical Phases
-   **Category**: I/O / Design
-   **Type**: Process / Static (partial)
-   **Profiles**:
    -   Core: N/A
    -   Strict: MUST
-   **Scope**: critical_only

Functions implementing core algorithms (often in critical units such as
those marked `@critical`) must not perform file or network I/O; they
should operate on data already in memory. I/O should be handled at
boundaries.

### CRSS-11.5.6 - No dynamic allocation in critical execution paths (Strict-only)
-   **Category**: Memory and Resources / Determinism
-   **Type**: Static
-   **Profiles**:
    -   Core: N/A
    -   Strict: MUST
-   **Scope**: critical_only

Functions in Strict units that are part of a critical control cycle (e.g. @critical) shall not perform dynamic memory allocation during normal execution. In particular, within such functions:
- Creation of new lists, dicts, sets, tuples, user objects, or large strings is forbidden.
- Growing existing containers (e.g. append, extend, add, inserting new dict keys) is forbidden.

New objects may only be created:
- in initialization phases, or
- in explicitly non-critical setup / shutdown logic.

Static analysis must flag bytecode opcodes and patterns associated with allocation inside annotated critical functions.

**Rationale**

Eliminates allocation-induced latency and GC pressure inside timing-critical paths, making execution more predictable.

### CRSS-11.5.7 - GC disabled during Strict critical execution
-   **Category**: Runtime Behavior / Memory
-   **Type**: Process / Static (partial)
-   **Profiles**:
    -   Core: N/A
    -   Strict: MUST
-   **Scope**: critical_only

During execution of Strict critical cycles:
-The cyclic garbage collector (gc) shall be disabled (e.g. via gc.disable()).

A project-defined “critical mode” mechanism shall ensure:
- gc.isenabled() is False while any @critical code is running.
- gc.isenabled() is restored to its configured non-critical state afterward.

The design must document when GC can run (startup, shutdown, maintenance windows). Strict code must not rely on GC being enabled for correctness.

**Rationale**

Disables non-deterministic GC pauses during the most time-critical operations, aligning behavior with hard real-time constraints.

### CRSS-11.5.8 - No finalizers (__del__) in Strict object graphs
-   **Category**: Memory and Resources
-   **Type**: Static
-   **Profiles**:
    -   Core: N/A
    -   Strict: MUST-NOT
-   **Scope**: `all_code`

Classes used by Strict units shall not define __del__ methods, nor rely on finalizer semantics for releasing resources. Strict code must use explicit cleanup methods or context managers instead.

**Rationale**
Finalizers introduce unpredictable, GC-driven behavior at object destruction and can run at arbitrary times under memory pressure.

### CRSS-11.5.9 - Acyclic Strict-owned object graphs
-   **Category**: Memory and Resources / Determinism
-   **Type**: Process / Static (partial)
-   **Profiles**:
    -   Core: N/A
    -   Strict: MUST
-   **Scope**: `all_code`

Object graphs owned or manipulated by Strict units shall be designed to be acyclic (no reference cycles) except for a small set of explicitly documented internal structures with proven bounded size and lifetime.

Static analysis and design review must:
- prohibit obvious cyclic patterns (e.g. parent↔child back-references) in Strict types, or
- document and justify them with evidence of bounded size and lifetime.

**Rationale**

Acyclic graphs ensure refcounting alone is sufficient for reclamation and avoid GC-dependence for memory release.

### CRSS-11.6.1 - Strict execution shall be single-threaded
-   **Category**: Concurrency / Architecture
-   **Type**: Static / Process
-   **Profiles**:
    -   Core: N/A
    -   Strict: MUST
-   **Scope**: `all_code`

Strict modules and @critical units must execute in a single OS thread:
- No use of threading, multiprocessing, concurrent.futures, or asyncio within Strict modules.
- If the same process uses threads for non-critical work, Strict units must execute only on one designated thread with no shared mutable state with others.

**Rationale**

Single-threaded execution eliminates data races and heavily simplifies reasoning about timing.

---

## 7. Robustness and Portability

> [⬆ Back to Table of Contents](#toc)


### 7.1 Imports and Isolation

### CRSS-11.7.1 - No wildcard imports (Strict-only)
-   **Category**: Imports
-   **Type**: Static
-   **Profiles**:
    -   Core: N/A
    -   Strict: MUST-NOT
-   **Scope**: `all_code`

`from module import *` is forbidden in Strict code.

### CRSS-11.7.2 - No implicit relative imports (Strict-only)
-   **Category**: Imports
-   **Type**: Static
-   **Profiles**:
    -   Core: N/A
    -   Strict: MUST-NOT
-   **Scope**: `all_code`

Strict code must use absolute imports or explicit relative imports
(`from .mod import X`), not rely on implicit `sys.path` ordering.

### CRSS-11.7.3 - Process isolation for safety-critical Python
-   **Category**: Architecture and Robustness
-   **Type**: Process
-   **Profiles**:
    -   Core: N/A
    -   Strict: MUST
-   **Scope**: `all_code`

Safety-critical Strict units shall run in a dedicated process isolated from:
- non-critical UI
- logging
- data acquisition
- or ML/AI components

Inter-process communication must:
- use well-specified message formats (e.g., schema-validated JSON, protobuf)
- enforce bounds on message size and rate
- treat malformed or missing messages as faults leading to a safe state

**Rationale**

Prevents failures in non-critical or experimental Python code from compromising safety-critical control logic.

### CRSS-11.7.4 - Safe-state watchdog for Strict processes
-   **Category**: Architecture and Fault Handling
-   **Type**: Process
-   **Profiles**:
    -   Core: N/A
    -   Strict: MUST
-   **Scope**: `all_code`

The process hosting Strict code shall be monitored by an independent watchdog (hardware, RTOS, or external supervisor). If the Strict process:
- stops responding within a defined period
- crashes
- or reports an unrecoverable error

the watchdog must drive the system into a defined safe state.

**Rationale**

Even with strict coding rules, unexpected faults must not lead to uncontrolled behavior; a simple external monitor provides a last-resort safety net.

---

## 8. Maintainability and Documentation

> [⬆ Back to Table of Contents](#toc)


### 8.1 Module Design

### CRSS-11.8.1 - Single responsibility per Strict module (Strict-only)
-   **Category**: Design / Maintainability
-   **Type**: Process
-   **Profiles**:
    -   Core: N/A
    -   Strict: SHOULD
-   **Scope**: `all_code`

Each Strict module should have a single, clear purpose. Mixing unrelated
concerns in one file is discouraged.

---

## 9. Testing and Coverage Guidelines

> [⬆ Back to Table of Contents](#toc)


### 9.1 Verification and Evidence

### CRSS-11.9.1 - 100% branch coverage for Strict modules
-   **Category**: Testing and Coverage
-   **Type**: Process
-   **Profiles**:
    -   Core: N/A
    -   Strict: MUST
-   **Scope**: `all_code`

All Strict modules must target 100% branch coverage, or a justified and
documented exception (for example, defensive code paths that cannot be
reached in normal operation).

### CRSS-11.9.2 - MC/DC for critical decisions
-   **Category**: Testing and Coverage
-   **Type**: Process / Dynamic (future tooling)
-   **Profiles**:
    -   Core: N/A
    -   Strict: MUST
-   **Scope**: `all_code`

Critical units (functions/classes in critical zones or marked
`@critical`) should have tests designed to satisfy Modified
Condition/Decision Coverage (MC/DC) for important decisions.

Future tools (for example, a `pycodereview` MC/DC extension) are expected
to:

- instrument decisions and conditions,
- collect condition/decision pairs,
- generate MC/DC satisfaction reports.

### CRSS-11.9.3 - Documented test matrices for critical logic
-   **Category**: Testing and Coverage
-   **Type**: Process
-   **Profiles**:
    -   Core: N/A
    -   Strict: SHOULD
-   **Scope**: `all_code`

For core decision logic, maintain test matrices that list input
conditions and expected outcomes, referencing MC/DC where applicable.

---

### CRSS-11.9.4 - Requirements traceability for Strict units
-   **Category**: Process / Traceability
-   **Type**: Process
-   **Profiles**:
    -   Core: N/A
    -   Strict: MUST
-   **Scope**: `all_code`

Each Strict module and each `@critical` function must be traceable to
one or more requirements. Each such requirement must be traceable
forward to design, implementation, and tests.

---

### CRSS-11.9.5 - Guideline Compliance Summary for CRSS-Strict
-   **Category**: Process / Compliance
-   **Type**: Process
-   **Profiles**:
    -   Core: N/A
    -   Strict: MUST
-   **Scope**: `all_code`

Projects using CRSS-Strict must maintain a “Guideline Compliance
Summary” (GCS-style report) that:

- lists each CRSS rule,
- states compliance (Yes/No/N.A.),
- records any deviations with justification and impact analysis,
- references supporting evidence (reviews, test reports, coverage).

This mirrors MISRA-Compliance-style reporting.

### CRSS-11.9.7 - Fault injection for safety mechanisms
-   **Category**: Testing and Fault Tolerance
-   **Type**: Process
-   **Profiles**:
    -   Core: N/A
    -   Strict: SHOULD (MUST for level A)
-   **Scope**: `critical`

Safety mechanisms implemented in Strict code (range checks, error paths, safe-state transitions) must be validated with fault injection tests, e.g.:

- injecting malformed messages

- simulating sensor failures

- forcing exceptions in dependencies

Test suites must show that the system reaches defined safe states under these faults.

**Rationale**
High ASIL/SIL levels explicitly expect fault-injection-based verification of safety mechanisms.

---
