# CRSS-Python Core Profile

**Version:** v1.0.0  
**Status:** Normative  
**Maturity:** Stable  
© 2025 Sofian Daghsen - All rights reserved  
Distributed under CC BY-NC-ND 4.0 - see LICENSE-CRSS.

---

<a id="toc"></a>
## Table of Contents

- [2. Introduction](#2-introduction)
- [3. Scope and Applicability](#3-scope-and-applicability)
- [4. CRSS Rule Model](#4-crss-rule-model)
- [5. Core Language and Dynamic Features](#5-core-language-and-dynamic-features)
- [6. Error Handling, Exceptions, and Control Flow](#6-error-handling-exceptions-and-control-flow)
- [7. State, Determinism, and Time](#7-state-determinism-and-time)
- [8. Resources, Memory, and Performance](#8-resources-memory-and-performance)
- [9. Robustness Against Index Errors](#9-robustness-against-index-errors)
- [10. Caching and Derived State](#10-caching-and-derived-state)
- [11. Signal Processing and Threshold Safety](#11-signal-processing-and-threshold-safety)
- [12. Security Rules (Core)](#12-security-rules-core)
- [13. Testing, Verification, and Process Expectations](#13-testing-verification-and-process-expectations)
- [14. Big Data and Large Dataset Handling](#14-big-data-and-large-dataset-handling)
- [15. Sensitive Data Handling](#15-sensitive-data-handling)
- [16. Key Exchange and Cryptographic Material](#16-key-exchange-and-cryptographic-material)
- [17. Python Versioning and Tooling Compatibility](#17-python-versioning-and-tooling-compatibility)
- [18. Phase-Aware Interpretation Rules](#18-phase-aware-interpretation-rules)
- [19. Summary](#19-summary)


---

## 2. Introduction

> [⬆ Back to Table of Contents](#toc)

The **CRSS-Python Core** profile establishes a baseline safety and reliability rule set for Python projects that require:

- Defect reduction
- Predictable behavior
- Static analyzability
- Secure coding practices
- Long-term maintainability

Its objectives are:

- **Reduce common Python failure modes**
  such as dynamic surprises, silent type coercion, unsafe mutation, and unchecked exceptions.

- **Promote deterministic, testable software**
  by encouraging explicit state, traceable flow, and defensive design.

- **Enable automated code review and compliance**
  via rules that are directly enforceable by tools like *pycodereview*.

- **Provide a foundation for higher assurance profiles**
  such as CRSS-Python Strict.

- **Remain broadly usable**
  across non-critical and mixed-criticality systems without prohibitive cost.

### 2.1 What Core Is Not

- It is **not** a formal certification standard.
- It is **not** a performance or optimization guide.
- It **does not** enforce the extreme constraints required for mission-critical logic (that is Strict’s role).

### 2.2 Relation to Strict

- **Strict builds on Core.**
- Core can be used alone for general reliability, while Strict applies to critical paths requiring the highest assurance.

### 2.3 Versioning and Rule ID Stability

CRSS-Python uses semantic versioning: `vMAJOR.MINOR.PATCH`.

- **Rule IDs are never reused.**
- When a rule is removed or replaced, its ID remains reserved and is
  marked as **Deprecated** in this document.
- Rule IDs are stable across profiles: the same `CRSS-x.y.z` refers to
  the same conceptual rule in both Core and Strict.

### 2.4 Chapter Structure and ID Ranges

The following chapters define stable ranges for rule IDs:

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
- **11.chapter_id_[3..10, 12].x** - Strict only rules
- **12.x** - Configurationand Deployment Integrity
Within each chapter, rule IDs (`CRSS-x.y.z`) are not reused. When a rule
is retired, its ID remains reserved and is marked as deprecated rather
than being reassigned.

### 2.5 Companion Documents and Annexes

This Core specification defines the **normative rules** for the CRSS-Python Core profile
(rule IDs `CRSS-x.y.z`).

Additional guidance and process details are provided in companion documents:

- `docs/specs/crss_python_companion.md` - high-level usage guide and workflow.
- `docs/annexes/crss_import_policy.md` - Cross-profile import policy (Core vs Strict).
- `docs/annexes/crss_inheritance_policy.md` - Inheritance rules between Core and Strict classes.
- `docs/annexes/crss_exceptions_deviations.md` - Deviation model, justification and GCS.
- `docs/annexes/crss_critical_annotation.md` - Critical units, `@critical` usage, and relation to Strict.
- `docs/annexes/crss_versioning_and_rule_stability.md` - Versioning of CRSS-Python and rule ID stability.
- `docs/annexes/crss_official_example.md` - Worked example of a CRSS-compliant project.
- `docs/annexes/crss_architecture.md` - Architecture of the pycodereview engine and its integration with CRSS.

Where there is any conflict between this specification and a companion document,
**this specification is authoritative for the meaning and applicability of CRSS rule IDs**.

### 2.6 Tooling
CRSS-Python is tool-independent.
pycodereview is a reference implementation that can enforce CRSS profiles (Core and Strict).
Other tools may implement CRSS support as long as they respect the rule IDs and semantics defined in this standard.

### 2.7 Python Version Scope

CRSS-Python Core v1.0.0 defines rules for a stable subset of the Python
language. To ensure deterministic behaviour and consistent analysis,
this specification is defined for:

- **Interpreter:** CPython
- **Supported Python versions (normative):** 3.9-3.12 (inclusive)

Within this range, CRSS-Core rules and their intended semantics are
guaranteed. Use of CRSS-Core on other versions or interpreters is at the
user’s risk and is not covered by this specification.

### 2.8 Project-Declared Python Target Version

Each project applying CRSS-Core MUST declare the Python versions it
intends to support.

The project-declared version expresses the Python version the project
claims to support at runtime, deployment, testing, and certification.

The following constraints apply:

1. The project-declared version **MUST be** within the CRSS-Core
   supported range (3.9-3.12 for v1.0.0). Projects that declare version
   outside this interval are not CRSS-compliant.


This separation between **spec range** and **project target** ensures that
CRSS-Core remains stable and conservative at the standard level, while each
project can make precise and auditable claims about the Python version it
supports.

---

---

## 3. Scope and Applicability

> [⬆ Back to Table of Contents](#toc)

CRSS-Python Core aims to:

-   Reduce common correctness and security bugs.
-   Improve testability and diagnosability.
-   Encourage predictable control flow and error handling.
-   Make static analysis and future MC/DC / path tools easier to apply.

It is suitable for:

-   Backend services and internal tools.
-   Test automation frameworks and integration harnesses.
-   Non-hard-real-time but business-critical systems.
-   Code that must be maintainable and auditable over time.

---

---

## 4. CRSS Rule Model

> [⬆ Back to Table of Contents](#toc)

Each rule has:

-   **ID**: `CRSS-x.y.z`
-   **Title**
-   **Category** (optional): e.g. Dynamic Features, Correctness, Security,
    Robustness, Maintainability.
-   **Type** (optional): 
    -   *Static* -- enforceable via static analysis
        (e.g. `pycodereview`).
    -   *Dynamic* -- requires runtime / coverage tooling.
    -   *Process* -- requires process discipline (tests, review,
        traceability).
-   **Profiles** -- which profiles this rule applies to, and at what
    strength:
    -   Core: MUST / SHOULD / SHOULD-NOT / MUST-NOT / N/A
    -   Strict: MUST / SHOULD / SHOULD-NOT / MUST-NOT / N/A
-   **Rationale** (optional)
-   **Examples** (optional)
-   **Scope** (optional)


This document is the **canonical catalog** of CRSS rules.
The **Strict** profile reuses these IDs with stronger requirements and
adds a small number of Strict-only rules (see `crss_python_strict_spec.md`).

---

---

## 5. Core Language and Dynamic Features

> [⬆ Back to Table of Contents](#toc)

### CRSS-3.1.1 - Avoid runtime code generation

-   **Category**: Dynamic Features
-   **Type**: Static
-   **Profiles**:
    -   Core: MUST-NOT
    -   Strict: MUST-NOT
-   **Scope**: `all_code`

Use of `eval()` and `exec()` is forbidden in production logic. It may be
allowed in isolated tooling scripts or REPL helpers that are clearly
separated from main application code (for example, dev-only notebooks).

**Rationale**:

Dynamic code generation is extremely hard to analyze, easy to misuse,
and a major security risk when combined with untrusted input.

**Non-compliant**

``` python
result = eval(user_input)
exec(config_snippet)
```

**Compliant**:

``` python
# Use explicit parsing:

result = safe_parse_expression(user_input)

# Use a static dispatch table instead of exec:

OPERATORS = {"+": operator.add, "-": operator.sub}
OPERATORS[op](a, b)
```

### CRSS-3.1.2 - Constrain dynamic imports

-   **Category**: Dynamic Features
-   **Type**: Static
-   **Profiles**:
    -   Core: SHOULD-NOT
    -   Strict: MUST-NOT
-   **Scope**: `all_code`

Dynamic imports like `importlib.import_module(name)` where name is not a
literal string should be avoided in Core code and are forbidden in
Strict code.

**Non-compliant**

``` python
module = importlib.import_module(plugin_name)  # plugin_name from user
```

**Compliant**:

``` python
ALLOWED_PLUGINS = {
    "csv": "myapp.plugins.csv_plugin",
    "json": "myapp.plugins.json_plugin",
}
module = importlib.import_module(ALLOWED_PLUGINS[plugin_name])
```

### CRSS-3.1.3 - No runtime monkeypatching of imported modules

-   **Category**: Dynamic Features
-   **Type**: Static
-   **Profiles**:
    -   Core: SHOULD-NOT
    -   Strict: MUST-NOT
-   **Scope**: `all_code`

Rebinding functions, methods, or attributes of imported modules at
runtime is strongly discouraged in Core and forbidden in Strict code,
except in clearly separated test modules.

**Non-compliant**

``` python
import math
math.sin = custom_sin  # monkeypatching
```

### CRSS-3.1.4 - Limit lambda usage to simple local expressions
-   **Category**: Dynamic Features / Readability
-   **Type**: Static
-   **Profiles**:
    -   Core: SHOULD-NOT
    -   Strict: MUST-NOT
-   **Scope**: `all_code`

In the Core profile, lambda usage is reported as warning.

`lambda` expressions shall not be used in Strict units or functions
annotated `@critical`. Use named functions instead. This improves
traceability, stack traces, logging, and static analysis.

**Non-compliant (Core)**

``` python
handler = lambda req: (
    do_a(req) if cond_a(req)
    else do_b(req) if cond_b(req)
    else do_c(req)
)
```

**Compliant**:

``` python
def choose_handler(req: Request) -> Response:
    if cond_a(req):
        return do_a(req)
    if cond_b(req):
        return do_b(req)
    return do_c(req)

handler = choose_handler
```

### CRSS-3.1.5 - Identifiers shall not reuse reserved keywords or builtins

- **Category**: Core Language Usage / Maintainability
- **Type**: Static
- **Profiles**:
- **Scope**: all_code
  - Core: MUST-NOT
  - Strict: MUST-NOT

Identifiers for variables, functions, methods, classes and modules shall not:

- reuse Python reserved keywords (e.g. `class`, `async`, `await`, `yield`, `global`, ...), or
- shadow builtins such as `list`, `dict`, `len`, `sum`, `id`, `type`, `input`, `open`, etc.

**Rationale**:

Shadowing reserved keywords or builtins reduces code clarity, complicates static analysis
and can lead to subtle runtime failures when the original builtin is expected.

**Non-compliant**

``` python
class = 5
list = [1, 2, 3]
def len(x): ...
```

**Compliant**:

``` items_list = [1, 2, 3]

def length(value: str) -> int:
    return len(value)
```

### CRSS-3.1.6 - Ban custom metaclasses in Strict

- **Category**: Dynamic Features / Metaprogramming
- **Type**: Static
- **Profiles**:
  - Core: SHOULD-NOT
  - Strict: MUST-NOT

**Rule**

- In the **Strict** profile, user-defined or third-party **custom metaclasses** MUST NOT be used in safety-relevant code.
- Only a small, explicitly-defined whitelist of standard library metaclasses (e.g. `abc.ABCMeta`) **MAY** be allowed, and only if:
  - They are used in a simple, conventional way (for declaring abstract methods), and
  - Their behavior is well understood and documented in the safety case.
- In the **Core** profile, metaclasses SHOULD-NOT be used. If they are used, their behavior MUST be:
  - Documented,
  - Limited to non-safety-critical modules,
  - Covered by tests.

**Rationale**

Metaclasses can arbitrarily alter class creation and behavior at runtime. This makes code:

- Harder to reason about statically
- More difficult to analyze and verify
- Vulnerable to hidden behavior changes

In a safety standard, classes must be **predictable, explicit, and analyzable**. Metaclasses are therefore incompatible with Strict, except for tightly-controlled whitelisted cases.

**Non-compliant (Strict)**

```python
class Meta(type):
    def __new__(mcls, name, bases, attrs):
        # dynamic attribute injection, logging, etc.
        attrs["extra_flag"] = True
        return super().__new__(mcls, name, bases, attrs)

class SafetyThing(metaclass=Meta):
    ...
```

**Compliant (Strict)**

```python
from abc import ABC, abstractmethod

class SafetyInterface(ABC):
    @abstractmethod
    def decide(self, data: "Input") -> "Decision":
        ...
```

### CRSS-3.2.1 - Reflection shall not drive high-level control flow

-   **Category**: Dynamic Features / Maintainability
-   **Type**: Static
-   **Profiles**:
    -   Core: SHOULD-NOT
    -   Strict: MUST-NOT
-   **Scope**: `all_code`

Avoid using `getattr`, `setattr`, `globals()`, `locals()`, or `vars()`
as primary drivers of control flow.

**Non-compliant**

``` python
action = getattr(self, f"do_{cmd}")
action()
```

**Compliant**

``` python
ACTIONS = {
    "start": start_handler,
    "stop": stop_handler,
}
ACTIONS[cmd]()
```

### CRSS-3.2.2 - globals/locals/vars for introspection only

-   **Category**: Dynamic Features
-   **Type**: Static
-   **Profiles**:
    -   Core: SHOULD-NOT
    -   Strict: MUST-NOT
-   **Scope**: `all_code`

### CRSS-3.2.3 - Cross-profile import policy

- **Category**: Modules and Dependencies
- **Type**: Static / Process
- **Profiles**:
  - Core: SHOULD
  - Strict: MUST

Projects SHALL define an import policy that governs imports between Core and Strict modules
(for example, hybrid or encapsulation mode).

At minimum:

- Core modules MAY import other Core modules.
- Core modules MUST-NOT import Strict modules.
- Strict modules MAY import Core modules, subject to the configured import policy
  and additional constraints defined in the import policy annex.

### CRSS-3.3.1 - Assignment expressions (walrus) limited / forbidden

-   **Category**: Core Language Usage / Readability
-   **Type**: Static
-   **Profiles**:
    -   Core: SHOULD-NOT
    -   Strict: MUST-NOT
-   **Scope**: `all_code`

The `:=` assignment expression (walrus operator, Python ≥ 3.8) must not be
used in Strict code. In Core code, its use should be limited to **simple,
local patterns** where it clearly improves readability, and must not be
used in nested or complex boolean expressions.

**Rationale**

Walrus expressions can hide state changes inside conditions, making
control flow analysis and testing more difficult.

**Non-compliant (Core)**

``` python
while (line := f.readline()) and not line.startswith("#"):
    ...
```

**Compliant**

``` python
while True:
    line = f.readline()
    if not line or line.startswith("#"):
        break
    ...
```

### CRSS-3.4.1 - Inheritance across profiles

- **Category**: Design / Types
- **Type**: Static / Process
- **Profiles**:
  - Core: SHOULD
  - Strict: MUST

Inheritance relationships between Core and Strict classes SHALL follow these principles:

- A Strict class SHOULD-NOT inherit from a Core class.
- A Core class MAY inherit from a Strict class.

For Strict code:

- A Strict class MUST-NOT inherit from a Core class unless a documented and approved
  deviation exists.

**Rationale**

Inheritance governs behavioural extension and substitutability. If a Strict
(safety-critical) class inherits from Core (non-critical) code, the parent class
may introduce nondeterminism, unchecked side effects, or unsafe behaviour into
the critical unit. Core -> Strict is safer because Strict provides stronger guarantees.

---

## 6. Error Handling, Exceptions, and Control Flow

> [⬆ Back to Table of Contents](#toc)

### CRSS-4.1.1 - Assertions not for runtime validation

-   **Category**: Error Handling / Correctness
-   **Type**: Static
-   **Profiles**:
    -   Core: SHOULD-NOT
    -   Strict: MUST-NOT
-   **Scope**: `all_code`

### CRSS-4.2.1 - No bare except:

-   **Category**: Error Handling
-   **Type**: Static
-   **Profiles**:
    -   Core: MUST-NOT
    -   Strict: MUST-NOT
-   **Scope**: `all_code`

**Non-compliant**

``` python
try:
    do_work()
except:
    log_error("failed")
```

**Compliant**

``` python
try:
    do_work()
except (IOError, ValueError) as exc:
    logger.error("Failed to do work: %s", exc)
    raise
```

### CRSS-4.2.2 - except Exception requires explicit handling

-   **Category**: Error Handling
-   **Type**: Static
-   **Profiles**:
    -   Core: SHOULD-NOT
    -   Strict: MUST-NOT
-   **Scope**: `all_code`

### CRSS-4.2.3 - Exceptions shall not be used for normal control flow

-   **Category**: Error Handling / Correctness
-   **Type**: Static
-   **Profiles**:
    -   Core: SHOULD-NOT
    -   Strict: MUST-NOT
-   **Scope**: `all_code`

### CRSS-4.2.4 - Preserve exception context when re-raising

-   **Category**: Error Handling / Correctness
-   **Type**: Static
-   **Profiles**:
    -   Core: SHOULD
    -   Strict: MUST
-   **Scope**: `all_code`

When an exception is re-raised or converted to another type, the
original context (stack trace and message) should be preserved using
either bare `raise` or exception chaining (`raise NewError(...) from exc`).
Losing context makes diagnosis and forensics significantly harder.

### CRSS-4.3.1 - Avoid multiple evaluations of function calls in one condition

-   **Category**: Control Flow / Correctness
-   **Type**: Static
-   **Profiles**:
    -   Core: SHOULD-NOT
    -   Strict: MUST-NOT
-   **Scope**: `all_code`

A function with potential **side effects** or non-trivial cost shall not
be called more than once within a single boolean expression or condition.
Evaluate it once and store the result in a local variable.

**Rationale**

Multiple evaluations can:

-   change program behavior if the function has side effects,
-   cause performance problems,
-   make MC/DC reasoning harder.

**Non-compliant**

``` python
if is_ready() and not is_ready():
    ...
```

**Compliant**

``` python
ready = is_ready()
if ready and not_ready_condition(ready):
    ...
```

### CRSS-4.3.2 - Loop conditions should be free of hidden side effects

-   **Category**: Control Flow / Correctness
-   **Type**: Static
-   **Profiles**:
    -   Core: SHOULD
    -   Strict: MUST
-   **Scope**: `all_code`

Loop conditions (`while` and `for` with generator expressions) should not rely
on function calls that perform non-trivial side effects. Side effects
should be moved into the loop body or a clearly named helper.

**Rationale**

Side effects in loop conditions obscure control flow, complicate testing
and MC/DC analysis, and can introduce subtle bugs if conditions are
reordered.

**Non-compliant**

``` python
while advance_state_and_check():
    ...
```

**Compliant**

``` python
while True:
    state_ok = advance_state()
    if not state_ok:
        break
    ...
```

### CRSS-4.3.3 - Async only for non-hard-real-time paths

- **Category**: Async
- **Type**: Static
- **Profiles**:
  - Core: SHOULD
  - Strict: MUST

Time-critical logic must be synchronous and deterministic.
`async`/`await` may be used for coordination layers or non-critical
paths, not for core safety decisions.

### CRSS-4.3.4 - Avoid late-bound closures over loop variables
-   **Category**: Control Flow / Loops and Closures
-	**Type**: Static
-	**Profiles**:
	- 	Core: SHOULD-NOT
	- 	Strict: MUST-NOT
-   **Scope**: `all_code`

**Rule**

Closures inside loops MUST NOT capture loop variables using late
binding. Capture via default argument or explicitly.

**Rationale**

Python closures capture names, not values. All closures see final value.

**Non-compliant**

``` python
callbacks = []
for i in range(3):
    callbacks.append(lambda: print(f"slot={i}"))
```

**Compliant**

``` python
callbacks.append(lambda i=i: print(f"slot={i}"))
```

### CRSS-4.3.5 - Handle async task failures and cancellation explicitly

-	**Category**: Async / Concurrency
-	**Type**: Static / Process
-	**Profiles**:
	- 	Core: SHOULD
	- 	Strict: MUST
-   **Scope**: `all_code`

**Rule**

All async tasks MUST be awaited or supervised.\
Unhandled exceptions must be logged and escalated.\
Cleanup must be deterministic under cancellation.

**Non-compliant**

``` python
asyncio.create_task(process_event(ev))
```

**Compliant**

``` python
tasks = [asyncio.create_task(process_event(ev)) for ev in events]
for t in tasks:
    await t
```

---

### CRSS-5.1.1 - Type hints on public APIs

-   **Category**: Types & Interfaces
-   **Type**: Static
-   **Profiles**:
    -   Core: SHOULD
    -   Strict: MUST
-   **Scope**: `all_code`

### CRSS-5.1.2 - Constrain use of Any

-   **Category**: Types & Interfaces
-   **Type**: Static
-   **Profiles**:
    -   Core: SHOULD-NOT
    -   Strict: MUST-NOT
-   **Scope**: `all_code`

### CRSS-5.1.3 - Use nominal interfaces (ABCs) for Strict code

- **Category**: Types & Interfaces
- **Type**: Static / Design
- **Profiles**:
  - Core: SHOULD
  - Strict: MUST

**Rule**

- In **Strict** units, interfaces between components (especially safety-relevant ones) MUST be expressed using:
  - Abstract base classes (`abc.ABC` + `@abstractmethod`), or
  - Concrete base classes with clearly documented “abstract” methods to be implemented by subclasses.
- Strict code MUST NOT rely on **implicit structural interfaces** (e.g. “anything with a `.run()` method” without a shared base class).
- Core code SHOULD follow the same pattern for clarity and maintainability.

**Rationale**

Nominal interfaces:

- Make type relationships explicit
- Enable static analysis and tooling to reason about contracts
- Prevent accidental interface drift
- Support safe polymorphism and substitute implementations

In safety-critical contexts, “if it quacks like a duck” is not sufficient; interfaces must be explicit and analyzable.

### CRSS-5.1.4 – Control polymorphism and ban duck typing in Strict

- **Category**: Types & Interfaces
- **Type**: Static / Design
- **Profiles**:
  - Core: SHOULD-NOT (for safety-relevant code paths)
  - Strict: MUST-NOT

**Rule**

- In **Strict** units, **duck-typed polymorphism** (behavior based solely on the presence of methods or attributes without a common base class or protocol) MUST-NOT be used in safety-relevant code.
- Strict units MUST:
  - Depend on explicit, nominal base classes or approved `Protocol` types (if allowed by the project’s type discipline), and
  - Avoid polymorphism based on `hasattr`, `getattr` with string method names, or ad-hoc duck-typing.
- In **Core** units, such patterns SHOULD-NOT be used in safety-relevant paths (e.g. input validation, decision logic), and SHOULD be limited to non-critical glue code if used at all.

**Non-compliant (Strict)**

```python
def run_task(task) -> None:
    # "Duck typing": anything with run() is accepted.
    task.run()
```

**Compliant (Strict)**

```python
from abc import ABC, abstractmethod

class Task(ABC):
    @abstractmethod
    def run(self) -> None:
        ...

def run_task(task: Task) -> None:
    task.run()
```

**Rationale**

Duck typing makes it difficult to:

- Know which implementations are valid
- Guarantee that all variants respect safety contracts
- Reason about future changes

Explicit polymorphism allows Stronger guarantees and better tool support.

### CRSS-5.1.5 - Restrict use of `typing.cast`

-   **Category**: Types & Interfaces
-   **Type**: Static
-   **Profiles**:
    -   Core: SHOULD-NOT
    -   Strict: MUST-NOT
-   **Scope**: `all_code`

The `typing.cast()` helper shall not be used in Strict code, and should
be avoided in Core code except in tightly controlled situations.

Instead of using `cast()` to override the type checker, code should:

-   use explicit runtime checks (`isinstance`, `hasattr`, etc.) and let
    the type checker infer the narrowed type, or
-   refactor APIs and data structures to use precise types
    (`TypedDict`, `Protocol`, `Enum`, etc.).

**Rationale**

`cast()` has no runtime effect and can easily hide genuine type errors,
which undermines the guarantees of strict static typing in critical code.

**Non-compliant (Strict)**

``` python
from typing import Any, cast

def get_speed(raw: Any) -> float:
    return cast(float, raw)  # hides type uncertainty
```

**Compliant**

``` python
from typing import Any

def get_speed(raw: Any) -> float:
    if not isinstance(raw, (int, float)):
        raise ValueError(f"Invalid speed value: {raw!r}")
    return float(raw)
```
### CRSS-5.1.6 - Explicit module exports via `__all__` in Strict

- **Category**: Types & Interfaces / Encapsulation
- **Type**: Static
- **Profiles**:
  - Core: SHOULD
  - Strict: MUST

**Rule**

- Strict modules MUST define `__all__` to explicitly enumerate public symbols (functions, classes, constants) intended for external use.
- Names not listed in `__all__` MUST be treated as internal implementation details and MUST NOT be imported or used in other modules.
- Core modules SHOULD follow this pattern for safety-relevant components.

**Rationale**

Explicit exports:

- Make the public API surface clear
- Encapsulate internal details
- Reduce coupling and unintended dependencies
- Make refactoring safer

This also helps tooling understand which parts of a module may be referenced across boundaries.

**Compliant (Strict)**

```python
# safety_controller/__init__.py

from .controller import SafetyController

__all__ = ["SafetyController"]
```

### CRSS-5.1.7 - Ban mutable default arguments

-	**Category**: Types & Interfaces / Functions
-	**Type**: Static
-	**Profiles**:
	- 	Core: SHOULD-NOT
	- 	Strict: MUST-NOT
-	**Scope**: `all_code`

**Rule**
Functions and methods MUST NOT declare mutable default argument values
such as `[]`, `{}`, `set()`, or other mutable containers.\
Defaults MUST be immutables (`None`, numbers, strings, tuples, enums...)
and any mutable structure MUST be created inside the function body.

**Rationale**

Python evaluates default arguments once at function definition time.\
Mutable defaults lead to shared unexpected state.

**Non-compliant**

``` python
def add_sensor_reading(reading, buffer=[]):
    buffer.append(reading)
    return buffer
```

**Compliant**

``` python
def add_sensor_reading(reading: float, buffer: Optional[List[float]] = None) -> List[float]:
    if buffer is None:
        buffer = []
    buffer.append(reading)
    return buffer
```

---

### CRSS-5.1.8 - Use is only for None and singletons

-	**Category**: Types and Interfaces / Semantics
-	**Type**: Static
-	**Profiles**:
	- 	Core: SHOULD
	- 	Strict: MUST
-	**Scope**: `all_code`

**Rule**

`is` / `is not` allowed only for None or documented singletons.

**Non-compliant**

``` python
return x is 0
return flag is "OK"
```

**Compliant**

``` python
return x == 0
return flag == "OK"
```

---

## 7. State, Determinism, and Time

> [⬆ Back to Table of Contents](#toc)

### CRSS-5.2.1 - Avoid hidden mutable global state

-   **Category**: State and Concurrency
-   **Type**: Static
-   **Profiles**:
    -   Core: SHOULD-NOT
    -   Strict: MUST-NOT
-   **Scope**: `all_code`

### CRSS-5.2.2 - No implicit side effects on import

-   **Category**: State and Initialization
-   **Type**: Static
-   **Profiles**:
    -   Core: SHOULD-NOT
    -   Strict: MUST-NOT
-   **Scope**: `all_code`

### CRSS-5.3.1 - Constrain nondeterministic random number generation

-   **Category**: Correctness / Determinism
-   **Type**: Static / Process
-   **Profiles**:
    -   Core: SHOULD-NOT
    -   Strict: MUST-NOT
-   **Scope**: `all_code (phase-aware)`

Use of nondeterministic randomness via the `random` module or `secrets`
in core computational logic should be avoided unless:

-   The randomness is not part of correctness (e.g., sampling, load
    tests), **or**
-   The random generator is explicitly seeded for reproducibility in
    tests.

Randomness must **never** influence control-flow or business-critical
decisions.

**Non-compliant (Core)**

``` python
import random

if random.random() < 0.5:
    execute_path_a()
else:
    execute_path_b()
```

**Compliant**

``` python
import random

rng = random.Random(42)  # Explicit seeded RNG for reproducibility
value = rng.random()
process_sample(value)
```

### CRSS-5.3.2 - No nondeterministic randomness in Strict code

-   **Category**: Determinism / Safety
-   **Type**: Static / Process
-   **Profiles**:
    -   Core: SHOULD-NOT
    -   Strict: MUST-NOT
-   **Scope**: `all_code`

Strict code shall not use non-seeded or nondeterministic random number
generation (`random.random()`, `random.randint()`, `secrets`, or
similar).

Strict components must behave deterministically across runs. Randomness
may only be used when:

1.  An explicit fixed seed is provided, **and**
2.  The value is not used for program control-flow, safety logic, or
    data that influences correctness, **and**
3.  The randomness is strictly confined to non-critical utility
    functions.

**Non-compliant (Strict)**

``` python
import random

token = random.randint(1, 999999)  # nondeterministic
```

**Compliant (Strict)**

``` python
import random

rng = random.Random(12345)  # fixed seed
nonce = rng.randint(1000, 9999)  # permitted only if not safety-critical
```

### CRSS-5.3.3 - Cryptographic-strength randomness only via approved APIs

-   **Category**: Security
-   **Type**: Static
-   **Profiles**:
    -   Core: SHOULD
    -   Strict: MUST
-   **Scope**: `all_code (phase-aware)`

Strict security-relevant code (authentication, key generation, secure
tokens) must use `secrets` or `os.urandom()` --- but only in
non-deterministic security boundaries, such as:

-   Key generation tools
-   Authentication services
-   Security provisioning scripts

These must not run as part of the deterministic critical logic flow.

**Example (Strict-compliant but must be outside safety-critical path)**

``` python
from secrets import token_urlsafe

def generate_session_key() -> str:
    return token_urlsafe(32)
```
### CRSS-5.3.4 - NaN/Inf checks on Strict numeric outputs

-   **Category**: Determinism / Numeric Safety
-   **Type**: Static / Process
-   **Profiles**:
    -   Core: SHOULD
    -   Strict: MUST
-   **Scope**: `all_code`

Strict numeric functions that produce floating-point results must:
- check results for NaN and Inf (math.isnan, math.isinf, or equivalent),

handle such values via:
- saturation to a safe bound, or
- rejection and transition to a safe error state.

Unchecked NaN/Inf values must not propagate into actuators or safety decisions.

**Rationale**

NaN/Inf propagation can silently poison control loops and is often triggered only under extreme conditions.

### CRSS-5.3.5 - Explicit range margins for safety-critical signals

-   **Category**: Numeric Safety
-   **Type**: Process / Static (partial)
-   **Profiles**:
    -   Core: SHOULD
    -   Strict: MUST
-   **Scope**: `all_code`

For each safety-critical numeric input and output:
- the valid range and safety margin (e.g. min/max, clamping, sanitization behavior) must be documented,

Strict code must enforce these ranges and either:
- clamp to safe limits, or
- raise a controlled fault that leads to safe behavior.

**Rationale**

Strongly aligns with ISO 26262 expectations: no unchecked value should reach a safety-critical actuator or algorithm.

### CRSS-5.3.6 - Unified internal time representation (UTC)

-   **Category**: Data Semantics / Date-Time
-   **Type**: Static / Design
-   **Profiles**:
    -   Core: SHOULD
    -   Strict: MUST
-   **Scope**: `all_code (phase-aware)`

Strict systems shall represent all internal timestamps in a single canonical format:
- UTC time, and
- a project-defined standard string or binary representation (for example ISO 8601 with `Z`).

Conversion to local time zones is only permitted at external boundaries (UI display, reporting, export).
Internal logic and persistence must not depend on local wall-clock settings or environment-specific time zones.

**Rationale**

Inconsistent handling of local vs UTC time leads to subtle bugs around daylight savings, leap seconds, and cross-region logic.

### CRSS-5.3.7 - Ban on naive datetimes in cross-boundary logic

-   **Category**: Date-Time Correctness
-   **Type**: Static
-   **Profiles**:
    -   Core: SHOULD-NOT
    -   Strict: MUST-NOT
-   **Scope**: `all_code`

Strict code shall not use naive `datetime` objects for values that:
- may cross time zones,
- may cross DST boundaries, or
- are stored, transmitted, or compared across systems.

All such datetimes must be timezone-aware (UTC or explicit offset). Existing legacy naive values must be normalized at system boundaries.

**Rationale**

Naive datetimes are ambiguous and lead to non-portable behavior across platforms and deployments.

### CRSS-5.3.8 - Controlled date parsing and formatting

-   **Category**: Date-Time Robustness
-   **Type**: Static / Process
-   **Profiles**:
    -   Core: SHOULD
    -   Strict: MUST
-   **Scope**: `all_code`

Strict code shall use a small, vetted set of functions or utilities for date/time parsing and formatting. It must:
- avoid ad-hoc parsing logic scattered throughout the code,
- validate input strings against the canonical format(s),
- treat unknown or invalid formats as errors (not guessed or auto-corrected).

**Rationale**

Multiple ad-hoc date formats lead to inconsistent behavior and fragile code when integrated with third-party systems.

### CRSS-5.3.9 - Declared numeric precision and tolerance

-   **Category**: Numeric Safety
-   **Type**: Design / Process
-   **Profiles**:
    -   Core: SHOULD
    -   Strict: MUST
-   **Scope**: `all_code`

For each safety-critical numeric algorithm, the project shall:
- document the required precision and tolerated numerical error,
- define how comparisons are performed (for example, using explicit tolerances rather than raw `==` on floating-point values),
- include tests that exercise boundary and tolerance conditions.

**Rationale**

Many numeric failures arise from unstated assumptions about precision. Making these explicit allows targeted verification and review.

### CRSS-5.3.10 - Prefer fixed-point or decimal for exact domains

-   **Category**: Numeric Semantics
-   **Type**: Design / Static
-   **Profiles**:
    -   Core: SHOULD
    -   Strict: MUST
-   **Scope**: `all_code`

Where arithmetic requires exact decimal behavior (for example financial calculations, billing, or business-critical accounting), Strict code shall use a fixed-point or decimal representation such as `decimal.Decimal` with:
- a configured precision,
- a documented rounding mode,
- and a stable context defined at system initialization.

Use of binary floating-point in such domains must be justified as a deviation with impact analysis.

**Rationale**

Binary floating-point cannot represent many decimal fractions exactly and can cause invisible rounding errors that are unacceptable in financial or exact business logic.

---

## 8. Resources, Memory, and Performance

> [⬆ Back to Table of Contents](#toc)

### CRSS-5.4.1 - Avoid unbounded growth of in-memory collections

-   **Category**: State and Resources
-   **Type**: Static / Process
-   **Profiles**:
    -   Core: SHOULD
    -   Strict: MUST
-   **Scope**: `all_code (phase-aware)`

Long-lived collections (lists, dicts, sets, caches, queues) used in
services or background processes **must not grow without a defined bound**
or eviction strategy.

Examples include:

-   in-memory caches
-   global registries
-   message queues or buffers

**Rationale**

Even with garbage collection, unbounded structures are a primary source of
memory leaks and latency spikes in long-running Python processes.

**Non-compliant**

``` python
# Grows forever for each request

REQUEST_LOG = []

def handle_request(req):
    REQUEST_LOG.append(req)  # never truncated
```

**Compliant**

``` python
from collections import deque

REQUEST_LOG = deque(maxlen=1000)

def handle_request(req):
    REQUEST_LOG.append(req)  # bounded by maxlen
```

### CRSS-5.4.2 - Explicit lifecycle for large objects and buffers

-   **Category**: State and Resources
-   **Type**: Static / Process
-   **Profiles**:
    -   Core: SHOULD
    -   Strict: MUST
-   **Scope**: `all_code (phase-aware)`

Objects holding **large data** (e.g. huge lists, numpy arrays, big JSON
structures, large strings or byte buffers) must have an **explicit
lifecycle**:

-   avoid keeping references in long-lived globals unless justified,
-   clear or replace references once data is no longer needed,
-   for Strict code, this lifecycle must be visible in the design or
    documented.

**Rationale**

Hidden references to large objects can silently prevent garbage collection
and cause memory pressure in long-lived processes.

**Non-compliant**

``` python
BIG_DATA = None

def load_every_hour():
    global BIG_DATA
    BIG_DATA = fetch_entire_database()  # old value never cleared
```

**Compliant**

``` python
def load_snapshot():
    data = fetch_entire_database()
    try:
        process(data)
    finally:
        # Let 'data' go out of scope; don't store globally
        del data
```

### CRSS-5.4.3 - Resource pools and caches must support explicit reset

-   **Category**: State and Resources
-   **Type**: Static / Process
-   **Profiles**:
    -   Core: SHOULD
    -   Strict: MUST
-   **Scope**: `all_code (phase-aware)`

Custom resource pools and caches (DB connections, sessions, object pools)
must provide an **explicit reset/clear interface** that:

-   frees or closes resources, and
-   can be invoked in tests and shutdown paths.

**Rationale**

Without a reset hook, tests can interfere with each other and long-running
processes may accumulate unused resources.

**Non-compliant**

``` python
_connection_pool = {}

def get_connection(key):
    # Creates and stores, but never allows cleanup:
    ...
```

**Compliant**

``` python
_connection_pool = {}

def get_connection(key):
    ...

def reset_connection_pool() -> None:
    for conn in _connection_pool.values():
        conn.close()
    _connection_pool.clear()
```
### CRSS-5.4.4 - No silent failure

- **Category**: Defensive Programming
- **Type**: Static / Process
- **Profiles**:
  - Core: SHOULD-NOT
  - Strict: MUST-NOT
- **Scope**: `all_code`

Catching an exception or detecting an error must either:

- be handled with a defined mitigation, or
- be logged and propagated.

Silent `pass` or no-op handlers are forbidden in Strict code.

### CRSS-5.4.5 - Explicit preconditions and range checks

- **Category**: Defensive Programming
- **Type**: Process / Static (partial)
- **Profiles**:
  - Core: SHOULD
  - Strict: MUST

Functions in Strict units must explicitly validate their inputs (ranges,
types, enums) before use. Violations must lead to defined behavior (error,
safe fallback), not undefined states.

### CRSS-5.4.6 - Bounded heap usage for Strict processes

- **Category**: State and Processes
- **Type**: Process
- **Profiles**:
  - Core: SHOULD
  - Strict: MUST

Processes hosting Strict units must define and enforce:
- a maximum allowed heap size (e.g., via OS-level limits or monitoring), and
- a policy when the limit is approached or exceeded (graceful shutdown, degraded mode, or safe-state).

Tests must exercise behavior near the heap limit.

**Rationale**

Prevents unbounded memory usage from causing unpredictable failures or OS-level intervention.

---
### CRSS-5.5.1 - Bounded memory usage for bulk data

-   **Category**: Memory and Performance
-   **Type**: Design / Static
-   **Profiles**:
    -   Core: SHOULD
    -   Strict: MUST
-   **Scope**: `all_code (phase-aware)`

Operations over large datasets must be designed to:

- avoid loading unbounded data into memory at once,
- use streaming or iterator-based processing where feasible,
- define and respect upper bounds on in-memory working sets.

**Rationale**
Naively loading “big data” into lists or DataFrames can exhaust memory, causing unpredictable failures.

---

### CRSS-5.5.2 - Chunked processing and pagination

-   **Category**: Big Data / IO
-   **Type**: Design / Static
-   **Profiles**:
    -   Core: SHOULD
    -   Strict: MUST
-   **Scope**: `all_code (phase-aware)`

When interacting with data sources (databases, APIs, files) that may hold large datasets, Strict code should:

- use pagination, windowing, or chunked reads,
- commit partial progress where safe,
- avoid assuming the full dataset fits into memory or within a single transaction.

**Rationale**
Chunking and pagination keep processing within resource limits and improve resilience to failures.

---

### CRSS-5.5.3 - Query efficiency and index awareness

-   **Category**: Database Performance
-   **Type**: Design / Process
-   **Profiles**:
    -   Core: SHOULD
    -   Strict: SHOULD (MUST when DB load affects safety)
-   **Scope**: `all_code (phase-aware)`

For database-backed systems where performance or load can affect safety (for example time-critical alerts), queries and schema design must:

- be reviewed for index usage,
- avoid N+1 query patterns in critical paths,
- be profiled under expected load.

**Rationale**
Inefficient queries can cause slowdowns or lock contention, impacting timely safety decisions.

---

## 9. Robustness Against Index Errors

> [⬆ Back to Table of Contents](#toc)

> Python does not suffer from classic C-style buffer overflows, but it is still vulnerable to memory blowup, `IndexError`, `KeyError`, and unchecked growth when driven by external input.

### CRSS-4.4.1 - Index bounds validation on externally derived indices

-   **Category**: Defensive Programming
-   **Type**: Static / Process
-   **Profiles**:
    -   Core: SHOULD
    -   Strict: MUST
-   **Scope**: `all_code`

Where list or array indices are derived from external data (user input, network, files), Strict code shall:

- validate that indices are within valid bounds before access, or
- use safe patterns (`for element in sequence`) instead of direct indexing.

Blind indexing based on external offsets without validation is forbidden.

---

### CRSS-4.4.2 - Safe dictionary access for external keys

-   **Category**: Defensive Programming
-   **Type**: Static / Process
-   **Profiles**:
    -   Core: SHOULD
    -   Strict: MUST
-   **Scope**: `all_code`

When accessing dictionaries with keys from external sources, Strict code must:

- check key presence (`if key in mapping`), or
- use `mapping.get(key)` with a well-defined default, or
- catch `KeyError` and handle it explicitly.

Relying on unguarded key access without error handling in critical logic is prohibited.

---

### CRSS-4.4.3 - Safe unpacking and length assumptions

-   **Category**: Defensive Programming
-   **Type**: Static
-   **Profiles**:
    -   Core: SHOULD
    -   Strict: MUST
-   **Scope**: `all_code`

Strict code shall not assume that sequences derived from external data have a fixed length when unpacking (for example `a, b, c = external_list`).

Length assumptions must be validated, and invalid length must be treated as an error path.

**Rationale**
Malformed input can produce sequences of unexpected length, causing `ValueError` or misaligned semantics.

---

## 10. Caching and Derived State

> [⬆ Back to Table of Contents](#toc)

### CRSS-5.6.1 - Explicit cache policy and scope

-   **Category**: Caching / Data Semantics
-   **Type**: Design / Process
-   **Profiles**:
-   **Scope**: `all_code (phase-aware)`
    -   Core: SHOULD
    -   Strict: MUST

Any cache used in the system (in-memory, HTTP cache, distributed cache, on-disk cache) SHALL have an explicitly defined policy which includes:
- What is cached (keys, value types).
- Why it is cached (performance vs availability vs cost).
- Maximum lifetime (TTL) of cached entries.
- Consistency model (eventually consistent, read-through, write-through, etc.).
- Which components are allowed to access it.

This policy MUST be documented (ADR + Safety Baseline) and not live only “in code”.

**Rationale**
Caches are invisible state. Without an explicit policy, their behavior and impact on correctness/latency becomes unpredictable.

2. Cache Size and Memory Bounds

---

### CRSS-5.6.2 - Bounded cache size and eviction policy

-   **Category**: Memory and Performance / Caching
-   **Type**: Design / Static
-   **Profiles**:
-   **Scope**: `all_code (phase-aware)`
    -   Core: SHOULD
    -   Strict: MUST

All caches SHALL:
- have explicit upper bounds on size (number of entries and/or memory usage),
- use a defined eviction strategy (LRU, LFU, FIFO, etc.),
- avoid unbounded growth driven by external input.

Monitoring or inspection MUST be possible to confirm cache size stays within configured limits.

**Rationale**
Unbounded caches behave like memory leaks: over time they can starve the system and cause failures.

3. Freshness Constraints in Safety Decisions

---

### CRSS-5.6.3 - Freshness requirements for cached safety-relevant data

-   **Category**: Safety Semantics / Caching
-   **Type**: Design / Process
-   **Profiles**:
-   **Scope**: `all_code (phase-aware)`
    -   Core: SHOULD
    -   Strict Level A/B: MUST

For any safety-relevant decision that uses cached information (e.g. latest sensor values, status of another system, configuration flags):
- maximum acceptable age of cached data SHALL be documented,
- cache entries older than this age MUST be treated as invalid (cache miss),
- behavior on stale data MUST be defined (e.g. re-fetch, enter safe state).
- Safety logic MUST NOT rely on indefinitely stale cached state.

**Rationale**
“Fast but stale” is dangerous; using outdated data for safety-critical decisions is often worse than having no data.

4. Cache Failure Modes and Fallback Behavior

---

### CRSS-5.6.4 - Defined behavior on cache miss/failure

-   **Category**: Robustness / Caching
-   **Type**: Design / Static
-   **Profiles**:
-   **Scope**: `all_code (phase-aware)`
    -   Core: SHOULD
    -   Strict: MUST

For each cache, the system SHALL define:

what happens on cache miss,

what happens on cache read failure,

what happens if the backing store is unavailable.

Fallbacks MUST be:

deterministic,

safe (e.g. fail-closed, reduced functionality, safe default),

not silently masking systemic failures.

It is forbidden for Strict code to treat cache failures as “just ignore and continue as if success” without explicit handling.

---

### CRSS-5.6.5 - No hidden dependence on cache availability

-   **Category**: Reliability / Architecture
-   **Type**: Design / Process
-   **Profiles**:
-   **Scope**: `all_code (phase-aware)`
    -   Core: SHOULD
    -   Strict: MUST

The system SHALL NOT have a mode where:
- it appears operational but silently produces degraded or incorrect behavior solely due to cache outages or corruption.

If a critical cache becomes unavailable or corrupt and data cannot be re-fetched or recomputed within defined limits, the system MUST:
- signal a clear fault, and
- follow a defined safe state strategy.

**Rationale**
Caches are optimizations; they must not become hidden single points of correctness.

---

## 11. Signal Processing and Threshold Safety

> [⬆ Back to Table of Contents](#toc)

### CRSS-5.7.1 - Document operating ranges and thresholds for safety-relevant signals

- **Category**: Numeric / Signal Processing
- **Type**: Design / Process
- **Profiles**:
  - Core: SHOULD
  - Strict: MUST
-   **Scope**: `all_code`

**Rule**

- For any signal or numeric value that influences safety decisions (e.g., thresholds for alarms, shutdowns, or degraded modes), the following MUST be documented:
  - Expected operating range(s)
  - Units (e.g. °C, m/s²)
  - Threshold values used for safety decisions
  - Assumptions about noise, jitter, or measurement error
- The documentation MUST be:
  - Traceable to requirements, and
  - Referenced in design descriptions and tests.

**Rationale**

Implicit, undocumented thresholds and ranges increase the risk of misinterpretation and silent behavior changes. Safety-critical thresholds must be explicit and justified.

---

### CRSS-5.7.2 - Test behavior around thresholds and noise margins

- **Category**: Numeric / Signal Processing / Testing
- **Type**: Process
- **Profiles**:
  - Core: SHOULD
  - Strict: MUST

**Rule**

- Tests for safety-relevant numeric decisions (alarms, shutdowns, degraded modes, etc.) MUST:
  - Cover values **below, at, and above** each threshold,
  - Cover realistic noisy variations around thresholds, and
  - Check both false-positive and false-negative scenarios (spuriously triggering vs failing to trigger when needed).
- In Strict projects:
  - These tests MUST be part of the Test Evidence Package (TEP) and linked in the SCEM.

**Rationale**

Many real-world failures in safety systems arise at boundary conditions: just below or just above thresholds, under noisy or marginal conditions. Targeted tests ensure robustness at these critical points.

---

---

### CRSS-5.7.3 - Bound and document filter/processing latency

- **Category**: Numeric / Signal Processing / Timing
- **Type**: Design / Process
- **Profiles**:
  - Core: SHOULD
  - Strict: MUST

**Rule**

- If safety-relevant decisions depend on filtered or processed signals (e.g. moving averages, low-pass filters, debouncing), the design MUST:
  - Document the worst-case **latency** introduced by the filter, and
  - Show that this latency is acceptable for the safety function (e.g. system can still respond in time).
- For Strict-A critical logic:
  - The latency bounds MUST be verified via tests or analysis on the target platform.

**Rationale**

Filters improve stability but also add delay. In safety applications, this delay can matter as much as the threshold itself.

---

5. Caching in Microservices / Distributed Systems

## 12. Security Rules (Core)

> [⬆ Back to Table of Contents](#toc)

---

### CRSS-6.1.1 - Dangerous functions and APIs

-   **Category**: Security
-   **Type**: Static
-   **Profiles**:
    -   Core: MUST-NOT
    -   Strict: MUST-NOT
-   **Scope**: `all_code`

### CRSS-6.1.2 - Hardcoded secrets

-   **Category**: Security
-   **Type**: Static
-   **Domain**: Security
-   **Severity**: High
-   **Profiles**:
    -   Core: MUST-NOT
    -   Strict: MUST-NOT
-   **Deviation**:
    -   Core: must not; only with strong justification
    -   Strict: Not allowed
-   **Scope**: `all_code`

### CRSS-6.1.3 - Concurrency only via approved patterns

- **Category**: Concurrency
- **Type**: Process + Static hints
- **Profiles**:
  - Core: SHOULD
  - Strict: MUST

Use of `threading`, `multiprocessing`, low-level locks, or similar
primitives in Strict modules must be:

- centralized in a small set of wrappers (for example, `SafeThread`,
  `SafeProcess`), and
- subject to explicit review and documentation.

### CRSS-6.1.4 - Native extensions and FFI only via approved adapters

-	**Category**: Concurrency / Platform / Interop
-	**Type**: Static / Process
-	**Profiles**:
	- 	Core: SHOULD
	- 	Strict: MUST
-	**Scope**:`all_code`

**Rule**

Strict units MUST NOT call native interfaces directly except via
approved adapter modules.

**Non-compliant**

``` python
lib = ctypes.CDLL("libcontrol.so")
lib.set_thruster_power(level)
```

**Compliant**

Centralized adapter with validation and error handling.

### CRSS-6.2.1 - Insecure HTTP and disabled TLS verification

-   **Category**: Security
-   **Type**: Static
-   **Profiles**:
    -   Core: SHOULD-NOT
    -   Strict: MUST-NOT
-   **Scope**: `all_code`

### CRSS-6.2.3 - Prohibition of subprocess execution in Strict units

- **Category**: Execution and External Interfaces
- **Type**: Static
- **Profiles**:
  - Core: SHOULD-NOT
  - Strict: MUST-NOT

Strict units (including all @critical code) shall not invoke:
- subprocess.* APIs
- Shell commands (bash, PowerShell, CMD, sh, zsh, etc.)
- System utilities or external executables

Exceptions:
- Explicitly approved non-critical infrastructure scripts
- Documented and justified deviations at project level (not allowed for Level A)

**Rationale**

External command execution is non-deterministic, platform-dependent, and cannot be WCET-bounded or safety-verified.

### CRSS-6.2.4 - Shell invocation forbidden

- **Category**: Execution
- **Type**: Static
- **Profiles**:
  - Core: SHOULD-NOT
  - Strict: MUST-NOT

Use of shell=True or equivalent parameterization that spawns a command interpreter is strictly prohibited.

### CRSS-6.3.1 - Input validation for external data

-   **Category**: Security / Correctness
-   **Type**: Process / Static
-   **Profiles**:
    -   Core: SHOULD
    -   Strict: MUST
-   **Scope**: `all_code`

---
### CRSS-6.4.1 - Data classification and tagging

-   **Category**: Security / Data Protection
-   **Type**: Process
-   **Profiles**:
    -   Core: SHOULD
    -   Strict: MUST
-   **Scope**: `all_code`

Projects shall classify data handled by the system (for example public, internal, confidential, safety-critical, personal data) and document:

- which data falls into which category,
- where it is stored and transmitted,
- what protection mechanisms apply (encryption, access control, masking).

---

### CRSS-6.4.2 - Encryption in transit and at rest for sensitive data

-   **Category**: Security / Cryptography
-   **Type**: Design / Static
-   **Profiles**:
    -   Core: SHOULD
    -   Strict: MUST
-   **Scope**: `all_code`

Sensitive and safety-critical data shall:

- be transmitted only over encrypted channels (for example TLS, mTLS),
- be stored using database or filesystem encryption mechanisms where appropriate,
- never be sent in clear text over untrusted networks.

Use of home-grown cryptography or custom key exchange is forbidden.

---

### CRSS-6.4.3 - Redaction and minimization in logs

-   **Category**: Security / Logging
-   **Type**: Static / Process
-   **Profiles**:
    -   Core: SHOULD
    -   Strict: MUST
-   **Scope**: `all_code`

Logs in Strict systems must:

- avoid recording secrets (keys, tokens, passwords) and highly sensitive data (for example full personal identifiers),
- use masking or truncation when such data must be referenced,
- be reviewed to ensure that error paths do not accidentally leak sensitive payloads.

---

### CRSS-6.4.4 - Access control for sensitive data flows

-   **Category**: Security / Access Control
-   **Type**: Design / Static
-   **Profiles**:
    -   Core: SHOULD
    -   Strict: MUST
-   **Scope**: `all_code`

Access to sensitive data in code must:

- be mediated by explicit interfaces (for example service methods, repositories),
- enforce role-based or capability-based access checks where applicable,
- not be spread as raw direct database access across arbitrary modules.

---

### CRSS-6.4.5 - Approved key exchange and storage

-   **Category**: Security / Cryptography
-   **Type**: Design / Process
-   **Profiles**:
    -   Core: SHOULD
    -   Strict: MUST
-   **Scope**: `all_code`

Cryptographic keys and certificates must:

- be generated and exchanged using standard, vetted protocols (for example TLS, mTLS, SSH),
- be stored in secure mechanisms (for example OS key stores, HSMs, secret managers),
- never be hard-coded in source code or stored in version control.

### CRSS-6.4.6 - Key rotation and expiry

-   **Category**: Security / Lifecycle
-   **Type**: Process
-   **Profiles**:
    -   Core: SHOULD
    -   Strict: MUST
-   **Scope**: `all_code`

Projects should define policies for:

- key and certificate rotation,
- expiry and revocation handling,
- updating running systems to new keys without downtime where required.

---

### CRSS-6.4.7 - No long-lived caching of sensitive data

-   **Category**: Security / Caching
-   **Type**: Design / Static
-   **Profiles**:
    -   Core: SHOULD
    -   Strict: MUST
-   **Scope**: `all_code`

Sensitive data (secrets, tokens, credentials, personal data) SHALL NOT:
- be stored in long-lived caches, especially shared caches,
- be cached across user sessions, tenants, or security boundaries,
- be written into caches without at-rest protection equivalent to their primary storage.

If short-lived caching is unavoidable (e.g. token validation results):
- TTLs MUST be short,
- cache scope MUST be limited (per-process, per-session),
- logs MUST NOT contain cached payloads.

### CRSS-6.4.8 - Cache isolation between tenants/security domains

-   **Category**: Security / Multi-tenancy
-   **Type**: Design / Process
-   **Profiles**:
-   **Scope**: `all_code`
    -   Core: SHOULD
    -   Strict: MUST

In multi-tenant environments or mixed-trust setups, cache keys and namespaces MUST be designed so that:
- one tenant cannot read or infer another tenant’s cached data,
- cross-domain poisoning (one domain populates cache used by another) is not possible.

This applies both to in-memory and distributed caches.

---

### CRSS-6.4.9 - Centralize RBAC and access checks

- **Category**: Security / Access Control
- **Type**: Design / Process
- **Profiles**:
  - Core: SHOULD
  - Strict: MUST

**Rule**

- Role-based access control (RBAC), permission checks, and authorization logic MUST be **centralized** in a small number of dedicated components (e.g. `authz_service`, `AccessManager`).
- Strict units MUST NOT:
  - Implement ad-hoc RBAC logic scattered across modules (e.g. `if user.role == "admin"` in random functions).
  - Access raw user/role data and apply their own independent rules without going through the central RBAC component.
- Core units SHOULD avoid duplicated or inline RBAC logic and SHOULD use the central RBAC service when present.
- The central RBAC layer MUST:
  - Have clearly documented policies and data sources,
  - Be covered by comprehensive tests, and
  - Be treated as a safety-relevant component if its decisions affect safety behavior.

**Rationale**

Scattered and ad-hoc RBAC logic:

- Is hard to audit
- Is prone to inconsistencies and gaps
- Is easy to break when roles/permissions evolve

Centralizing authorization logic improves:

- Traceability
- Auditability
- Consistency

and reduces security-related safety failures.

---

### CRSS-6.4.10 - Secret Storage and Lifecycle

- **Category**: Security / Secrets
- **Type**: Design / Process
- **Profiles**:
  - Core: SHOULD
  - Strict: MUST
- **Scope**: `non_critical`

Secrets (passwords, private keys, certificates, tokens, API keys, connection strings) SHALL NOT:

- be stored in source control (including private repos),
- be embedded directly in source code, comments, test data, or documentation,
- be hardcoded in configuration files without proper encryption/protection.

Projects SHALL:

- retrieve secrets exclusively from:
  - a secure vault / KMS / password manager, OR
  - a tightly controlled environment/config file with restricted OS permissions;
- define for each secret:
  - a named **owner**,
  - a **rotation policy**,
  - a **maximum lifetime**;
- upon suspected or confirmed exposure:
  - rotate the secret immediately,
  - invalidate all derived tokens/sessions,
  - record a **security incident** in safety logs.

**Rationale**
Secret leakage leads to system compromise and loss of trust in safety-significant operations.

---

### CRSS-6.4.11 - Password and Credential Policy

- **Category**: Security / Authentication
- **Type**: Design / Process
- **Profiles**:
  - Core: SHOULD
  - Strict: MUST
- **Scope**: `non_critical`

Where password-based authentication is used:

- Passwords MUST be hashed using strong, modern algorithms:
  - PBKDF2, bcrypt, scrypt, Argon2, or equivalent.
- Plaintext passwords SHALL NOT be logged, stored, or captured in analytics.
- Authentication endpoints SHALL implement:
  - rate limiting,
  - exponential backoff OR
  - account lockout thresholds.
- Shared passwords SHALL NOT be used for safety-significant actions.
- Password reuse across environments (dev/test/stage/prod) is forbidden.

**Rationale**
Weak credential handling is a major source of compromise in operational systems.

---

### CRSS-6.4.12 - Token and Session Lifetime Management

- **Category**: Security / Sessions and Tokens
- **Type**: Design / Process
- **Profiles**:
  - Core: SHOULD
  - Strict: MUST
- **Scope**: `non_critical`

Access tokens, session identifiers, and refresh tokens MUST:

- have explicit **expiry times**,
- be bounded in total lifetime,
- be integrity-protected (e.g., HMAC/JWT signatures),
- be validated on **every use**, not just at login.

Tokens and sessions MUST be invalidated when:

- passwords/credentials change,
- roles/permissions change,
- anomalies or compromises are detected,
- a device or client is revoked.

Safety-significant operations MUST require **fresh authorization** (e.g., re-auth or time-bounded session).

**Rationale**
Long-lived or unchecked sessions create unsafe implicit trust.

---

### CRSS-6.4.13 - Authentication vs Authorization Separation

- **Category**: Security / Access Control
- **Type**: Design / Static
- **Profiles**:
  - Core: SHOULD
  - Strict: MUST
- **Scope**: `non_critical`

The system SHALL maintain strict separation between:

- **Authentication** (identity verification), and
- **Authorization** (permission verification).

Authorization MUST:

- be performed on the server side,
- NEVER rely solely on UI/client checks,
- NOT be bypassable via debug flags, local toggles, or test hooks.

Roles tied to safety MUST:

- be explicitly defined,
- follow least-privilege principles,
- be auditable.

**Rationale**
Auth bypass is one of the most common and catastrophic security failures.

---

### CRSS-6.4.14 - Safety-Significant Action Authorization

- **Category**: Security / Safety Interaction
- **Type**: Design / Process
- **Profiles**:
  - Core: SHOULD
  - Strict: MUST
- **Scope**: `non_critical`

Operations affecting:

- safety configurations,
- thresholds,
- supervisory logic,
- indirect actuation parameters,

MUST:

- require explicit authorization based on roles/capabilities,
- be logged as safety events (without secrets),
- require fresh authorization (Strict-Level-A).

Systems SHALL NOT trust:

- long-lived admin sessions,
- generic credentials,
- debug interfaces.

**Rationale**
Safety configuration changes must not rely on weak or stale access control.

---

---

## 13. Testing, Verification, and Process Expectations

> [⬆ Back to Table of Contents](#toc)

### 12.1 Criticality Levels

CRSS defines three criticality levels for modules and functions:

- **Level A - Safety Critical**
  Failure may lead to loss of life, severe injury, or major system hazard.
- **Level B - High Integrity**
  Failure may lead to loss of service, significant economic damage,
  or reduction of safety margins.
- **Level C - Standard**
  Normal production quality; failure has limited impact.

Projects may map their own safety classifications (ASIL, DAL, SIL, etc.)
onto these three levels. At minimum:

- **Level A** code must use the **Strict** profile and comply with all
  Strict process rules (traceability, MC/DC, deviation controls).
- **Level B** code should use the **Strict** profile or an enhanced **Core**
  configuration with strong testing and traceability.
- **Level C** code typically uses the **Core** profile.

### CRSS-9.1.1 - Target high branch coverage

-   **Category**: Testing and Coverage
-   **Type**: Process
-   **Profiles**:
    -   Core: SHOULD
    -   Strict: MUST
-   **Scope**: `all_code`

### CRSS-9.1.2 - Every bugfix must have a regression test

-   **Category**: Testing and Coverage
-   **Type**: Process
-   **Profiles**:
    -   Core: MUST
    -   Strict: MUST
-   **Scope**: `all_code`

### CRSS-9.1.3 - Strict type checking for critical units (Strict)

- **Category**: Types / Tooling
- **Type**: Process
- **Profiles**:
  - Core: SHOULD
  - Strict: MUST

All Strict modules/functions (for example, in configured Strict zones or
annotated `@critical`) must pass strict static type checking (e.g.
`mypy --strict` or an equivalent configuration) with zero errors.
Type-ignores (`# type: ignore`) are disallowed or must be treated as
explicit deviations with justification and impact analysis.

### CRSS-9.2.1 - Authentication, Token and Session Negative Testing

- **Category**: Testing and Security
- **Type**: Process
- **Profiles**:
  - Core: SHOULD
  - Strict: MUST

Projects SHALL test:
- invalid credentials,
- brute-force attempts -> rate limiting or lockout behavior,
- expired tokens,
- tampered or modified tokens,
- access after:
  - role change,
  - password change,
  - revocation,
- concurrent session behavior (if applicable),
- replay or duplicate token usage.

For internet-exposed systems, additional tests SHOULD include:
- CSRF or replay attempts,
- credential stuffing simulations.

**Rationale**

Negative testing is essential for verifying robustness under malicious or degraded conditions.

---

### CRSS-9.2.2 - SCEM Evidence for Authentication and Authorization

- **Category**: SCEM and Compliance
- **Type**: Process
- **Profiles**:
  - Core: SHOULD
  - Strict: MUST

SCEM SHALL include:
- list of all authentication mechanisms (passwords, tokens, mTLS, SSO, OAuth, etc.),

- token/session model documentation:
  - structure,
  - lifetime,
  - scope,
  - validation logic,

- mapping of roles -> safety-significant operations,

- test evidence for:
  - expiry behavior,
  - revocation behavior,
  - lockout,
  - privilege changes,

- documentation of:
  - how secrets are stored,
  - how they are rotated,
  - how compromise is detected and handled.

Absence of this section SHALL be a **blocking failure** for Strict-Level-A certification.

**Rationale**

Authentication/authorization control must be demonstrably safe in operation.

### CRSS-9.3.1 - MC/DC for Level A decisions

-   **Category**: Testing and Coverage
-   **Type**: Process
-   **Profiles**:
    -   Core: SHOULD
    -   Strict (Level A): MUST
-   **Scope**: `all_code`

For **Level A** functions, all safety-relevant decisions (boolean
expressions affecting safety outcomes) should be covered according to
**Modified Condition/Decision Coverage (MC/DC)**.

Projects should maintain a **test matrix** for each such decision
documenting:

-   the individual boolean conditions,
-   the set of test cases,
-   for each test: the condition values and the outcome,
-   evidence that each condition can independently affect the outcome.

A simple table template:

| Test ID | Condition A | Condition B | Condition C | Outcome | Notes            |
|--------|-------------|-------------|-------------|---------|------------------|
| T1     | 0           | 0           | 0           | 0       | Only A toggled   |
| T2     | 1           | 0           | 0           | 1       | ...              |

### CRSS-9.3.2 - On-target / hardware-in-the-loop testing for Strict units

-   **Category**: Testing and Coverage
-   **Type**: Process
-   **Profiles**:
    -   Core: SHOULD
    -   Strict: MUST
-   **Scope**: `all_code`

For Level A (highest criticality) Strict units, tests must include on-target execution:

- either in hardware-in-the-loop (HIL) setups, or
- on representative embedded platforms under realistic loads.

Captured evidence must include:

- timing behavior
- memory usage
- correct handling of boundary and fault cases

**Rationale**

Desktop-only testing is insufficient to claim timing and resource safety on real hardware.

### CRSS-9.4.1 - Guideline Compliance Summary (GCS)

-   **Category**: Process / Compliance
-   **Type**: Process
-   **Profiles**:
    -   Core: SHOULD
    -   Strict: MUST
-   **Scope**: `all_code`

Projects using CRSS-Python Strict should maintain a **Guideline
Compliance Summary (GCS)** that, for each rule:

-   records whether it is:
    -   Compliant
    -   Deviated (with reference)
    -   Not applicable
-   references any documented deviations with IDs and justifications.

The GCS may be maintained as a spreadsheet or YAML/JSON file and must be
kept in version control.

### CRSS-9.5.1 - Declared target platform set

-   **Category**: Configuration Management
-   **Type**: Process
-   **Profiles**:
    -   Core: SHOULD
    -   Strict: MUST
-   **Scope**: `all_code`

Projects must declare:
- Supported operating systems
- Supported hardware variants
- Supported Python versions (subset of CRSS-allowed)
- Supported browsers (if applicable)

This declaration becomes part of the compliance baseline.

### CRSS-9.5.2 - Full configuration testing matrix

-   **Category**: Verification
-   **Type**: Process
-   **Profiles**:
    -   Core: SHOULD
    -   Strict: MUST
-   **Scope**: `all_code`

All combinations of declared platforms/flags must be covered by:
- Functional tests
- Safety tests
 Performance/timing tests

Where exhaustive testing is infeasible:
- Simulation tools or validated emulators may be used
- Deviations must document residual risk

### CRSS-9.5.3 - Environment delta documentation

-   **Category**: Risk Analysis
-   **Type**: Process
-   **Profiles**:
    -   Core: SHOULD
    -   Strict: MUST
-   **Scope**: `all_code`

Any difference between Testing environment and Deployment environment must be:
- Documented
- Risk-assessed
- Versioned
- Addressed with mitigation (e.g., HIL testing, platform-specific validation)

---

### CRSS-8.1.1 - Limit cyclomatic complexity

-   **Category**: Maintainability
-   **Type**: Static
-   **Profiles**:
    -   Core: SHOULD
    -   Strict: MUST
-   **Scope**: `all_code`

### CRSS-8.1.2 - Require docstrings on public APIs

-   **Category**: Maintainability
-   **Type**: Static
-   **Profiles**:
    -   Core: SHOULD
    -   Strict: MUST
-   **Scope**: `all_code`

### CRSS-8.2.1 - Do not shadow Python builtins or core types

-   **Category**: Core Language Usage / Maintainability
-   **Type**: Static
-   **Profiles**:
    -   Core: SHOULD-NOT
    -   Strict: MUST-NOT
-   **Scope**: `all_code`

Identifiers for variables, functions, methods, classes, and modules must
not reuse names of Python builtins or core container types, such as:

-   `list`, `dict`, `set`, `tuple`, `str`, `int`, `float`, `bool`, `bytes`
-   `len`, `id`, `type`, `input`, `open`, `sum`, `min`, `max`, etc.

**Rationale**

Shadowing builtins leads to confusing behavior, hard-to-debug errors, and
makes static analysis and reasoning about code more difficult.

**Non-compliant**

``` python
def process_items(list: list[int]) -> None:
    for dict in list:
        ...
```

**Compliant**

``` python
from collections.abc import Sequence
from typing import Mapping

def process_items(items: Sequence[Mapping[str, int]]) -> None:
    for item in items:
        ...
```

---

### CRSS-7.1.1 - Explicit encoding for text file I/O

-   **Category**: Robustness / Portability
-   **Type**: Static
-   **Profiles**:
    -   Core: SHOULD
    -   Strict: MUST
-   **Scope**: `all_code (phase-aware)`

### CRSS-7.1.2 - Use context managers for file I/O

-   **Category**: Resource Management
-   **Type**: Static
-   **Profiles**:
    -   Core: MUST
    -   Strict: MUST
-   **Scope**: `all_code (phase-aware)`

### CRSS-7.1.3 - Maximum length for external string inputs

-   **Category**: Robustness / Input Validation
-   **Type**: Static / Process
-   **Profiles**:
    -   Core: SHOULD
    -   Strict: MUST
-   **Scope**: `all_code (phase-aware)`

All strings originating from external sources (user input, network messages, files, third-party APIs) must have:
- documented maximum allowed lengths (in characters and/or bytes), and
- validation logic enforcing these limits.

Unbounded accumulation of external strings is forbidden in Strict code.

**Rationale**

Unbounded string inputs can lead to memory exhaustion, performance degradation, denial-of-service, or downstream overflow in external systems.

### CRSS-7.1.4 - Encoding and Unicode handling

-   **Category**: Encoding and Internationalization
-   **Type**: Static / Process
-   **Profiles**:
    -   Core: SHOULD
    -   Strict: MUST
-   **Scope**: `all_code`

Strict code shall:
- assume UTF-8 as the default encoding for textual data unless explicitly configured otherwise,
- normalize Unicode strings to a project-wide normalization form (for example NFC) when storing or comparing,
- avoid assuming a fixed relationship between characters and bytes.

Critical paths must include tests with non-ASCII data (for example Chinese, Japanese, accented characters, combining marks).

**Rationale**

Incorrect assumptions about encoding or character length lead to truncation, misalignment, or security issues (such as log forging or bypassing validation).

### CRSS-7.1.5 - Special character and control character validation

-   **Category**: Input Validation and Security
-   **Type**: Static / Process
-   **Profiles**:
    -   Core: SHOULD
    -   Strict: MUST
-   **Scope**: `all_code (phase-aware)`

Where strings are used as file names, protocol tokens, identifiers, or UI labels, Strict code shall:
- define allowed character sets or patterns (for example via regular expressions),
- reject or safely escape control characters and other unsafe characters (for example newlines, null bytes, terminal control sequences),
- apply additional constraints where strings cross system boundaries (such as shells, databases, or logs).

**Rationale**

Control characters and unexpected symbols in strings can lead to command injection, log forging, or malformed protocol messages.

### CRSS-7.1.6 - Language and locale configuration

-   **Category**: Internationalization and Configuration
-   **Type**: Process
-   **Profiles**:
    -   Core: MAY
    -   Strict: SHOULD
-   **Scope**: `all_code`

Projects that support multiple locales or languages (for example Chinese, Japanese, right-to-left scripts) shall:
- document supported locales in the Safety Baseline,
- include tests that exercise these locales in critical paths,
- verify that storage, transmission, and rendering preserve text meaning and structure.

**Rationale**

Explicitly documenting and testing supported locales avoids surprises when deployments encounter languages or encodings that were never considered.

### CRSS-7.2.1 - Avoid platform-specific hardcoded paths

-   **Category**: Portability
-   **Type**: Static
-   **Profiles**:
    -   Core: SHOULD
    -   Strict: SHOULD
-   **Scope**: `all_code`

### CRSS-7.2.2 - Third-party dependency documentation

-   **Category**: External Interfaces
-   **Type**: Process
-   **Profiles**:
    -   Core: SHOULD
    -   Strict: MUST
-   **Scope**: `all_code`

All third-party components must be documented with:
- Name and exact version
- Supplier / source
- Communication interfaces (protocol, channel, data schema)
- Safety relevance
- Failure modes and assumptions

### CRSS-7.2.3 - Interface schema verification

-   **Category**: Validation / Robustness
-   **Type**: Static
-   **Profiles**:
    -   Core: SHOULD
    -   Strict: MUST
-   **Scope**: `all_code`

For every external interface:
- The data schema shall be explicitly defined
- The implementation shall validate incoming data against that schema
- Any mismatch shall trigger a safe-fault or rejection

**Important Clarification**:
The standard validates the application, not the third-party internals.
We assume the third party behaves within its documented contract; we defend against violations.

### CRSS-7.6.1 - Explicit architecture definition

-   **Category**: Architecture and Design
-   **Type**: Process
-   **Profiles**:
    -   Core: SHOULD
    -   Strict: MUST
-   **Scope**: `all_code (phase-aware)`

Projects shall maintain an explicit architecture definition that documents:
- the set of services, processes, and modules,
- their responsibilities and boundaries,
- inter-service communication channels (for example HTTP, gRPC, message queues),
- data flows and trust boundaries,
- known single points of failure and mitigations.

Architecture documentation shall be kept under version control and updated when significant structural changes are made.

### CRSS-7.6.2 - Architecture Decision Records (ADR)

-   **Category**: Architecture Governance
-   **Type**: Process
-   **Profiles**:
    -   Core: SHOULD
    -   Strict: MUST
-   **Scope**: `all_code (phase-aware)`

Significant architectural decisions (for example choice of database, message bus, microservice partitioning, key third-party dependencies) shall be recorded as Architecture Decision Records (ADRs) including:
- context and problem statement,
- options considered,
- the chosen solution and rationale,
- expected impact on safety, security, and reliability,
- approval authority.

ADRs shall live alongside source code in the same repository or a tightly linked configuration repository.

### CRSS-7.6.3 - Avoidance of single point of failure for critical paths

-   **Category**: Availability and Fault Tolerance
-   **Type**: Design / Process
-   **Profiles**:
    -   Core: MUST
    -   Strict: MUST
-   **Scope**: `all_code`

For safety-critical functions, the architecture shall be designed so that no single runtime instance or external dependency can cause an uncontrolled unsafe failure.

Where a single instance is unavoidable, the Safety Baseline must document:
- why redundancy is not feasible, and
- what safe-failure behavior is implemented (for example system falls back to a defined safe state).

### CRSS-7.6.4 - Bounded retries and timeouts for network calls

-   **Category**: Robustness and Networking
-   **Type**: Static / Process
-   **Profiles**:
    -   Core: SHOULD
    -   Strict: MUST
-   **Scope**: `all_code (phase-aware)`

All network interactions (for example HTTP, gRPC, SFTP, database over TCP, message queues) shall:
- use explicit timeouts (no infinite waits),
- use bounded retry policies (maximum attempts and overall time),
- handle timeouts and connection failures explicitly,
- fail in a controlled, safe manner when retries are exhausted.

Unbounded retries or blocking calls without timeouts are forbidden in Strict code.

### CRSS-7.6.5 - Idempotent semantics for retried operations

-   **Category**: Microservices / Network Semantics
-   **Type**: Design
-   **Profiles**:
    -   Core: SHOULD
    -   Strict Level A: MUST
-   **Scope**: `all_code (phase-aware)`

Where network calls may be retried, side-effecting operations (writes, updates, commands) should be designed to be idempotent or to include safe deduplication mechanisms (for example operation IDs).

If idempotency is not feasible, the design and its compensating measures must be documented in ADRs and the Safety Baseline.

### CRSS-7.6.6 - Architecture responsibility and approval roles

-   **Category**: Governance
-   **Type**: Process
-   **Profiles**:
    -   Core: SHOULD
    -   Strict: MUST
-   **Scope**: `all_code`

For each critical architectural area (data storage, microservice topology, external dependencies, date/time policy, numeric precision), the project shall define:
- a responsible owner (role or person),
- an approval authority for changes,
- a documented review process.

These roles and processes shall be referenced in the Safety Baseline and kept up to date.

### CRSS-7.7.1 - No unmanaged global single connection for shared resources

-   **Category**: Resource Management
-   **Type**: Design / Static
-   **Profiles**:
    -   Core: SHOULD-NOT
    -   Strict: MUST-NOT
-   **Scope**: `all_code (phase-aware)`

Strict code shall not rely on a single, long-lived global connection (for example one database or SFTP connection) for the entire application lifecycle. Instead, it shall use connection pools or well-defined connection lifecycles per operation or transaction.

### CRSS-7.7.2 - Connection health check before use

-   **Category**: Resource Management / Robustness
-   **Type**: Static / Process
-   **Profiles**:
    -   Core: SHOULD
    -   Strict: MUST
-   **Scope**: `all_code (phase-aware)`

Before executing operations on external connections (database, SFTP, message brokers, and similar), Strict code shall:
- verify that the connection is open and valid, or
- attempt to re-establish the connection in a bounded, controlled way, and
- handle connection failures explicitly (for example by raising an error or transitioning to a safe state).

Blindly assuming a connection is valid is forbidden in Strict code.

### CRSS-7.7.3 - Bounded reconnect policies

-   **Category**: Resource Management
-   **Type**: Process
-   **Profiles**:
    -   Core: SHOULD
    -   Strict: MUST
-   **Scope**: `all_code (phase-aware)`

Reconnection logic for external dependencies shall:
- define maximum attempts,
- use backoff with an upper bound,
- stop retrying after a defined time or attempt limit,
- trigger a safe-failure path when reconnection fails.

### CRSS-7.7.4 - Safe file transfer preconditions

-   **Category**: I/O Robustness and Safety
-   **Type**: Static / Process
-   **Profiles**:
    -   Core: SHOULD
    -   Strict: MUST
-   **Scope**: `all_code (phase-aware)`

Before uploading or downloading critical data over SFTP/FTP/HTTP or similar protocols, Strict code shall:
- validate the target endpoint (host, port, path),
- verify the connection status,
- check that the target directory or bucket exists and is writable (where possible),
- detect and handle partial or failed transfers, ensuring they do not appear as successful.

**Rationale**

Implicit assumptions about persistent connections and successful transfers lead to data loss, corruption, or silent operational failures.

---
### CRSS-7.8.1 - Stable service contracts and versioning

-   **Category**: Microservices / Contracts
-   **Type**: Design / Process
-   **Profiles**:
    -   Core: SHOULD
    -   Strict: MUST
-   **Scope**: `all_code`

Services exposed over the network (HTTP, gRPC, message queues, etc.) shall have:

- explicit API contracts (schemas or IDLs),
- versioning strategy (for example `v1`, `v2` paths or explicit version fields),
- defined backward-compatibility guarantees.

Breaking changes to contracts must be documented in ADRs and must not be applied to deployed safety-critical consumers without a coordinated migration plan.

**Rationale**
Uncontrolled API evolution leads to silent breakage between microservices and inconsistent behavior in production.

---

### CRSS-7.8.2 - Bounded payload sizes and rates

-   **Category**: Network Robustness
-   **Type**: Static / Process
-   **Profiles**:
    -   Core: SHOULD
    -   Strict: MUST
-   **Scope**: `all_code (phase-aware)`

All externally visible endpoints and consumers shall enforce:

- maximum request payload sizes,
- maximum response sizes (or streaming semantics),
- rate limits for critical endpoints.

Oversized or excessively frequent requests must be rejected or throttled in a controlled manner.

**Rationale**
Unbounded payloads and traffic can cause memory exhaustion, timeouts, or denial-of-service.

---

### CRSS-7.8.3 - Circuit breakers and backpressure for critical dependencies

-   **Category**: Fault Tolerance / Microservices
-   **Type**: Design / Process
-   **Profiles**:
    -   Core: SHOULD
    -   Strict: MUST
-   **Scope**: `all_code (phase-aware)`

Where a service calls external dependencies (databases, third-party services, internal microservices) in its critical path, the design should include:

- circuit breakers for failing or overloaded dependencies,
- backpressure mechanisms (queue limits, rejection under load),
- clear behavior when dependencies are unavailable (degraded mode, fail-safe).

**Rationale**
Without circuit breakers and backpressure, failure in a single dependency can cascade and destabilize the entire system.

---

### CRSS-7.8.4 - Latency budgets for critical network operations

-   **Category**: Performance / Timing
-   **Type**: Design / Process
-   **Profiles**:
    -   Core: SHOULD
    -   Strict: MUST
-   **Scope**: `all_code (phase-aware)`

For safety-relevant network interactions (for example control commands, health checks, supervisory decisions), the design shall:

- define maximum acceptable end-to-end latency, and
- ensure network timeouts and retry policies align with these limits.

[Test and measurement evidence] must confirm that typical and worst-case latencies remain within these bounds under expected load.

**Rationale**
Unbounded latency can cause stale decisions and unsafe behavior in distributed systems.

---

## 14. Big Data and Large Dataset Handling

> [⬆ Back to Table of Contents](#toc)

### CRSS-7.8.5 - Distributed cache consistency for critical data

-   **Category**: Microservices / Caching
-   **Type**: Design / Process
-   **Profiles**:
-   **Scope**: `all_code (phase-aware)`
    -   Core: SHOULD
    -   Strict Level A/B: MUST

If a distributed cache (e.g. Redis, Memcached, cluster cache) is used to share state between services:
- the consistency model must be documented (eventual, strong, session, etc.),
- safety-critical decisions must be designed to tolerate that model (e.g. no assumption of instantaneous propagation),
- cache inconsistency MUST NOT be able to cause contradictory safety decisions in different services.

If consistent view is required, this must be enforced via design (e.g. single writer, transactional store as source of truth).

### CRSS-7.8.6 - Cache is never the source of truth

-   **Category**: Architecture / Data Semantics

-   **Type**: Design

-   **Profiles**:
-   **Scope**: `all_code (phase-aware)`

    -   Core: SHOULD

    -   Strict: MUST

Caches SHALL NEVER be treated as the “source of truth” for critical state.

The authoritative state must live in non-cached, durable systems (databases, configuration stores, verified sensors, etc.).

Cache contents must be considered ephemeral, potentially missing or stale at any time.

**Rationale**
When cache becomes the implicit source of truth, cache failures or evictions create correctness bugs that are very difficult to reproduce.

6. Caching and Sensitive Data

### CRSS-7.8.7 - Explicit HTTP caching directives

-   **Category**: Web / HTTP

-   **Type**: Static / Design

-   **Profiles**:
-   **Scope**: `all_code (phase-aware)`

    -   Core: SHOULD

    -   Strict: MUST for HTTP APIs

For HTTP-based APIs that handle:

safety-relevant data, or

sensitive data,

the system MUST:

set explicit cache-control headers (e.g. Cache-Control: no-store for sensitive responses, or clearly bounded max-age for safe-cacheable data),

avoid relying on default proxy/browser caching behavior,

treat incorrectly cached responses (e.g. stale) as faults when detected.

**Rationale**
Implicit caching by browsers or intermediate proxies can serve stale or cross-user data in unexpected ways.

## 15. Sensitive Data Handling

> [⬆ Back to Table of Contents](#toc)

### CRSS-7.9.1 - Strict JSON parsing and schema validation

-   **Category**: Data Parsing / Validation
-   **Type**: Static / Process
-   **Profiles**:
    -   Core: SHOULD
    -   Strict: MUST
-   **Scope**: `all_code (phase-aware)`

When loading JSON from external sources, Strict code shall:

- use robust JSON parsers that validate syntax,
- validate parsed data against a defined schema or contract,
- reject or quarantine payloads with unexpected types, missing required fields, or extra fields when not tolerated.

Special attention must be given to unusual characters, deeply nested structures, and large payloads (depth and size limits).

---


### CRSS-7.9.2 - Explicit CSV dialect and header handling

-   **Category**: Data Parsing / CSV
-   **Type**: Static / Process
-   **Profiles**:
    -   Core: SHOULD
    -   Strict: MUST
-   **Scope**: `all_code (phase-aware)`

When parsing CSV or similar delimited formats from external sources, Strict code must:

- explicitly configure the expected delimiter, quote character, and escape rules,
- validate header rows (names, order, presence),
- handle inconsistent row lengths as errors or quarantined data.

Relying on parser defaults without documenting expected dialect is forbidden for critical data flows.

---


### CRSS-7.9.3 - Handling malformed or binary-like text input

-   **Category**: Robustness / Encoding
-   **Type**: Static / Process
-   **Profiles**:
    -   Core: SHOULD
    -   Strict: MUST
-   **Scope**: `all_code (phase-aware)`

When ingesting text that may contain unusual or binary characters (including from third parties):

- decoding errors must be handled explicitly (for example `errors='strict'` with error reporting),
- control characters and non-printable sequences must be handled safely,
- inputs that fail decoding/validation must not be treated as valid text.

**Rationale**
Malformed or hostile text input can break parsers, pollute logs, or trigger unexpected behavior.

---

### CRSS-7.9.4 - Detection of partial network writes and reads

-   **Category**: Robustness / IO
-   **Type**: Static / Process
-   **Profiles**:
    -   Core: SHOULD
    -   Strict: MUST
-   **Scope**: `all_code (phase-aware)`

For HTTP, file uploads, SFTP transfers, and similar operations, Strict code shall:

- verify completion via explicit success indicators (status codes, response bodies, completion callbacks),
- compare expected sizes (for example Content-Length vs bytes sent/received) where applicable,
- treat truncated or partial operations as failures, not as partial success.

---

### CRSS-7.9.5 - Integrity checks for critical transfers

-   **Category**: Data Integrity
-   **Type**: Design / Process
-   **Profiles**:
    -   Core: SHOULD
    -   Strict Level A: MUST
-   **Scope**: `all_code (phase-aware)`

For safety-critical file or data transfers, the design should include integrity verification (for example checksums, hashes, signatures) and validation on the receiving side.

---

### CRSS-7.9.6 - Safe behavior on mid-operation disconnection

-   **Category**: Robustness / Failure Handling
-   **Type**: Design / Static
-   **Profiles**:
    -   Core: SHOULD
    -   Strict: MUST
-   **Scope**: `all_code (phase-aware)`

If network disconnection occurs mid-operation (for example during an HTTP PUT, a database transaction over the network, or a file transfer), Strict code must:

- ensure that partially applied operations are either rolled back or clearly marked incomplete,
- avoid leaving ambiguous or corrupted state that could be interpreted as successful completion,
- prefer transactional or “temp file then rename” patterns for critical writes.

---

## 16. Key Exchange and Cryptographic Material

> [⬆ Back to Table of Contents](#toc)

### CRSS-7.10.1 - Restricted operating system interaction

-   **Category**: OS Interaction / Safety
-   **Type**: Design / Static
-   **Profiles**:
    -   Core: SHOULD
    -   Strict: MUST
-   **Scope**: `all_code (phase-aware)`

Strict code may interact with the OS only through:

- well-defined file IO,
- time and monotonic clock APIs,
- networking primitives as needed for the architecture.

Use of APIs that enumerate processes, manipulate other processes, access raw devices, modify system-wide configuration, or run shell commands is forbidden except where explicitly approved and confined to non-critical tooling.

(This complements the existing rules that prohibit `subprocess`-based shell invocation.)

---

### CRSS-7.10.2 - Environment variables as configuration inputs

-   **Category**: Configuration Management
-   **Type**: Static / Process
-   **Profiles**:
    -   Core: SHOULD
    -   Strict: MUST
-   **Scope**: `all_code (phase-aware)`

Environment variables may be used as configuration inputs, but:

- required variables must be validated at startup, with clear failures if missing or malformed,
- their values must be parsed and validated (for example enums, integers, URLs),
- secrets in environment variables must be treated as sensitive data (not logged or echoed).

Strict systems must not change their behavior unpredictably based on unvalidated environment variables.

---

### CRSS-7.10.3 - No hidden behavior toggles in environment

-   **Category**: Configuration / Safety
-   **Type**: Static / Process
-   **Profiles**:
    -   Core: SHOULD-NOT
    -   Strict: MUST-NOT
-   **Scope**: `all_code`

Critical safety behavior shall not be controlled by undocumented environment flags. All safety-relevant configuration:

- must be documented,
- must be part of the Safety Baseline,
- must be tested across its supported configurations.

---

### CRSS-7.11.0 - Regex Usage in Critical Phases

- **Category**: Robustness and External Input
- **Type**: Static
- **Profiles**:
  - Core: MUST-NOT (in critical regions)
  - Strict: MUST-NOT
- **Scope**: `critical`

In any code that is part of a **critical phase** (`@critical` or otherwise
designated as critical core logic):

- The `re` module SHALL NOT be imported.
- No regular expression operations (compile, match, search, findall, split,
  substitute, fullmatch, etc.) SHALL appear directly or indirectly.
- No wrapper APIs that internally use regex SHALL be called.

If pattern matching is required in a critical phase, it MUST be implemented
using:

- simple bounded loops,
- explicit character checks, and
- deterministic finite-state parsing logic.

**Rationale**
Regex engines typically rely on complex backtracking algorithms.
Even “safe-looking” patterns can cause unpredictable runtime if used across
large inputs or edge cases.
Strict determinism in critical phases requires that **no regex engine** is
invoked.

---

### CRSS-7.11.1 - Bounded Input for Regex Operations

- **Category**: Robustness and External Input
- **Type**: Static + Behavioral
- **Profiles**:
  - Core: SHOULD
  - Strict: MUST
- **Scope**: `non_critical`

All strings passed to regex APIs **MUST** be explicitly bounded in length
before use, especially when:

- they originate from external sources (network, files, user input, logs), or
- they may grow over time (log aggregation, big data ingestion).

Projects SHALL:

- define a **maximum input length** per regex usage context,
- enforce it before calling any `re.*` function, and
- reject or truncate inputs that exceed the bound.

For **Strict-Level-A** non-critical units, bounding is **mandatory**.

**Non-compliant**

```python
import re

RE_ID = re.compile(r"[A-Z0-9]+")

def find_ids(payload: str) -> list[str]:
    # payload comes from network, no length bound
    return RE_ID.findall(payload)
```

**Compliant**

```python
import re

MAX_PAYLOAD_LEN = 8192
RE_ID = re.compile(r"[A-Z0-9]+")

def find_ids(payload: str) -> list[str]:
    if len(payload) > MAX_PAYLOAD_LEN:
        return []  # or raise a handled error
    return RE_ID.findall(payload)
```

---

### CRSS-7.11.2 - Prohibited High-Complexity Regex Patterns

- **Category**: Robustness and External Input
- **Type**: Static
- **Profiles**:
  - Core: SHOULD-NOT
  - Strict: MUST-NOT
- **Scope**: `non_critical`

The following classes of regex patterns SHALL NOT be used in Strict profile
and SHOULD-NOT be used in Core (and are **forbidden** in any Core-critical
unit):

- Nested quantifiers:
  - `(a+)+`
  - `(.+)+`
  - `(.*)+`
- Ambiguous “match anything” constructs with catastrophic backtracking:
  - `(.|\n)*` combined with additional `.*`/`.+` patterns
  - patterns where large overlapping alternatives cause exponential backtracking
- Any pattern known or shown (via analysis or test) to exhibit **super-linear**
  or **exponential** time complexity on certain classes of input.

If a project needs a complex pattern, it MUST be rewritten as:

- a set of simpler, independent regexes, or
- explicit parsing logic with deterministic complexity.

**Non-compliant**

```python
import re

# Catastrophic pattern - exponential backtracking

RE_BAD = re.compile(r"^(a+)+$")
```

---

### CRSS-7.11.3 - User-Supplied or Dynamic Regex Patterns

- **Category**: Robustness and External Input
- **Type**: Static + Behavioral
- **Profiles**:
  - Core: SHOULD-NOT
  - Strict: MUST-NOT
- **Scope**: `non_critical`

Regex patterns **MUST** be **constant literals** defined in code or in
configuration that is:

- version-controlled,
- validated, and
- part of the safety baseline.

The following practices are forbidden in Strict and strongly discouraged in
Core:

- constructing regex patterns from user input or external data,
- allowing users to submit arbitrary regex for evaluation,
- building patterns dynamically using string interpolation or concatenation
  from untrusted sources.

**Non-compliant**

```python
import re

def filter_lines(pattern_from_user: str, text: str) -> list[str]:
    # arbitrary user-supplied regex
    reg = re.compile(pattern_from_user)
    return [line for line in text.splitlines() if reg.search(line)]
```

**Compliant (Strict, non-critical)**

```python
import re

EMAIL_RE = re.compile(
    r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$"
)

def is_valid_email(raw: str) -> bool:
    if len(raw) > 128:
        return False
    return EMAIL_RE.match(raw) is not None
```

---

### CRSS-7.11.4 - Regex Testing and Worst-Case Behavior

- **Category**: Testing, Coverage and Process
- **Type**: Process
- **Profiles**:
  - Core: SHOULD
  - Strict: MUST
- **Scope**: `non_critical`

All regex usage in safety-relevant code MUST be accompanied by explicit tests
that cover:

1. **Normal inputs**
2. **Malformed / invalid inputs**
3. **Near-miss worst-case inputs** (long strings that “almost match”)

For **Strict**:

- Tests SHALL demonstrate **bounded execution time** under worst-case inputs
  considered within the domain.
- Regex operations SHALL NOT appear in tight loops that affect timing budgets
  for safety decisions.

For **Strict-Level-A**:

- Since regex is forbidden in `@critical` (see CRSS-7.11.0), tests shall
  verify that no critical unit imports or uses `re`.

---

### CRSS-7.11.5 - SCEM Evidence for Regex Safety

- **Category**: SCEM and Compliance
- **Type**: Process
- **Profiles**:
  - Core: SHOULD
  - Strict: MUST
- **Scope**: `non_critical`

Projects using regex MUST include the following in their **SCEM**:

1. **Regex Pattern Audit Table**
   - List of all regex patterns used (file, symbol, pattern).
   - Classification of each pattern as: simple / moderate / complex.
   - Confirmation that no forbidden constructs (CRSS-7.11.2) are present.

2. **Bounded Input Strategy**
   - Documentation of max-length bounds for all regex inputs (see CRSS-7.11.1).
   - Evidence that these limits are enforced and tested.

3. **Critical Path Declaration**
   - Evidence that **no regex** is used in any `@critical` function or critical
     unit (CRSS-7.11.0).

For **Strict-Level-A**, all three items above are **mandatory** for
certification acceptance.

**Non-Compliant Example**

```python
import re

# Catastrophic pattern - exponential backtracking

RE_BAD = re.compile(r"^(a+)+$")

def validate(data: str) -> bool:
    # data is external and unbounded
    return RE_BAD.match(data) is not None
```

Issues:

- unsafe pattern
- unbounded input
- unsafe for Core B/A and Strict (all levels)
- strictly forbidden inside critical path

---

**Compliant Example** (Strict Non-Critical)

```python
import re

MAX_LEN = 128
EMAIL_RE = re.compile(r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$")

def is_valid_email(raw: str) -> bool:
    if len(raw) > MAX_LEN:
        return False  # bounded input

    return EMAIL_RE.match(raw) is not None
```

Why compliant:

- bounded input
- simple character classes
- deterministic pattern
- non-critical code only

## 17. Python Versioning and Tooling Compatibility

> [⬆ Back to Table of Contents](#toc)

### CRSS-10.1.1 - Declare target Python version range

-   **Category**: Versioning and Tooling
-   **Type**: Process / Static
-   **Profiles**:
    -   Core: MUST
    -   Strict: MUST
-   **Scope**: `all_code`

Each project using CRSS-Python must declare a **target Python version
range** (for example, `>=3.10,<3.13`) in configuration, such as:

-   `pyproject.toml` (`requires-python`)
-   `setup.cfg` / `setup.py`
-   or a dedicated CRSS config file.

**Rationale**

A clear target range is necessary to reason about available language
features, standard library behavior, and deprecations.

### CRSS-10.1.2 - Static analysis uses the declared target version

-   **Category**: Versioning and Tooling
-   **Type**: Process / Static
-   **Profiles**:
    -   Core: SHOULD
    -   Strict: MUST
-   **Scope**: `all_code`

Static analysis tools (including `pycodereview`, linters, and type checkers)
must parse and analyze the code using the **syntax and semantics of the
declared target Python version range**.

If the analysis tool runs under a different interpreter version, it must
still be configured to emulate the target version (where supported).

**Rationale**

Running analysis under a different Python version than production can hide
syntax issues, deprecations, or subtle behavioral changes.

### CRSS-10.1.3 - No usage of features newer than the minimum supported version

-   **Category**: Versioning and Portability
-   **Type**: Static
-   **Profiles**:
    -   Core: SHOULD-NOT
    -   Strict: MUST-NOT
-   **Scope**: `all_code`

Code must not rely on language or standard-library features that are
**newer** than the declared minimum Python version, unless guarded by:

-   explicit version checks, or
-   a documented compatibility layer.

**Rationale**

Using features not available in the lowest supported Python version leads
to runtime failures that static analysis might miss.

**Example**

For `requires-python = ">=3.9"`:

-   Using `match`/`case` (Python 3.10) without guards is non-compliant.

### CRSS-10.1.4 - No use of removed or deprecated-in-target features

-   **Category**: Versioning and Portability
-   **Type**: Static / Process
-   **Profiles**:
    -   Core: SHOULD-NOT
    -   Strict: MUST-NOT
-   **Scope**: `all_code`

Code must not use language constructs or standard-library APIs that are:

-   removed in any version within the supported range, or
-   officially deprecated for that range without a clear migration plan.

**Rationale**

Relying on deprecated or removed features harms long-term maintainability
and can make upgrades unsafe.

**Examples**

-   Using `asyncio.get_event_loop()` patterns that are deprecated in newer
    versions without migration.
-   Using the legacy `imp` module instead of `importlib`.

### CRSS-10.2.1 - Analysis Python version may differ, but must be documented

-   **Category**: Versioning and Tooling
-   **Type**: Process
-   **Profiles**:
    -   Core: SHOULD
    -   Strict: MUST
-   **Scope**: `all_code`

The Python version used to run analysis tools (linters, `pycodereview`,
type checkers) may differ from the production runtime, but:

-   it must be documented, and
-   CI must ensure tests are executed on **all supported runtime versions**
    in the declared target range.

**Rationale**

Safety comes from the combination of static analysis and actual runtime
testing across the supported versions.

### CRSS-10.2.2 - Feature usage must be consistent with the declared profile

-   **Category**: Versioning and Profiles
-   **Type**: Static / Process
-   **Profiles**:
    -   Core: MUST
    -   Strict: MUST
-   **Scope**: `all_code`

For each module or project:

-   the selected profile(s) (Core, Strict) and
-   the target Python version range

must be kept consistent. Upgrading the Python version, or enabling a
stricter profile, may require **re-evaluating**:

-   which rules are applicable,
-   which features are allowed, and
-   whether new checks (e.g. for newer syntax) are needed.

**Rationale**

Profiles and Python versions interact. CRSS compliance is only meaningful
when both are explicitly aligned.

### CRSS-10.3.1 - Frozen interpreter and OS configuration

-   **Category**: Versioning and Toolchain
-   **Type**: Process
-   **Profiles**:
    -   Core: SHOULD
    -   Strict: MUST
-   **Scope**: `all_code`

For safety-critical deployments:
the exact CPython version, build configuration, OS version, and critical C library dependencies must be:
- documented,
- under configuration control, and
- treated as part of the safety baseline.

Any change to interpreter, OS, or core libraries requires:
- impact analysis,
- re-run of the conformance test suite (see CRSS-10.3.2),
- re-approval in the safety case.

**Rationale**

Models Python as a controlled COTS component, similar to a compiler or RTOS.

### CRSS-10.3.2 - Interpreter conformance test suite for CRSS subset

-   **Category**: Tool Qualification
-   **Type**: Process / Dynamic
-   **Profiles**:
    -   Core: SHOULD
    -   Strict: MUST
-   **Scope**: `all_code`

Projects using Strict for high-criticality must maintain a CRSS subset conformance test suite that:
- exercises all allowed features of the CRSS-Core and CRSS-Strict profiles,
- verifies behavior declared target_python,
- is executed on the actual target hardware/OS before release.

Test results must be part of the safety evidence.

**Rationale**

Provides evidence that CPython behaves as assumed within the defined usage domain.

### CRSS-10.4.1 - No automated updates in deployed environments

-   **Category**: Configuration Management
-   **Type**: Process
-   **Profiles**:
    -   Core: SHOULD
    -   Strict: MUST
-   **Scope**: `all_code`

Deployed systems shall not perform automatic updates of:
- Application code
- Database
- Python libraries
- Python interpreter
- System dependencies
- Containers or base images

Updates require:
1. Re-execution of the compliance process
2. Regression tests
3. Documentation of change impact
4. Formal approval

No exceptions for Level A.

### CRSS-10.4.2 - Frozen dependency set

-   **Category**: Configuration Management
-   **Type**: Process
-   **Profiles**:
    -   Core: SHOULD
    -   Strict: MUST
-   **Scope**: `all_code`

All project dependencies (including transitive dependencies, installer tools like pip, build tools, and setup utilities) must be:
- Fully pinned to exact versions
- Recorded in a single authoritative manifest (e.g., requirements.txt or lockfile)

Any version change triggers:
- Re-approval
- Re-testing
- Updated compliance evidence

**Rationale**

ASIL/SIL standards demand repeatable, deterministic builds.

### CRSS-10.4.3 - Interpreter immutability

-   **Category**: Toolchain Qualification
-   **Type**: Process
-   **Profiles**:
    -   Core: SHOULD
    -   Strict: MUST
-   **Scope**: `all_code`

The Python interpreter (CPython version, build flags, distribution) shall not change during the lifecycle of a certified release.
Any change constitutes a new baseline requiring full re-evaluation.

### CRSS-10.5.1 - Frozen container images

-   **Category**: Deployment and Packaging
-   **Type**: Process
-   **Profiles**:
    -   Core: SHOULD
    -   Strict: MUST
-   **Scope**: `all_code`

If containers (e.g., Docker) are used:
- The base image, OS, Python build, libraries, and system tools must be frozen and version-pinned.
- Images must be immutable.
- Rebuilding an image with any changed dependency requires re-approval and re-testing.

### CRSS-10.5.2 - Single-purpose containers for Strict execution

-   **Category**: Architecture
-   **Type**: Process
-   **Profiles**:
    -   Core: SHOULD
    -   Strict: MUST
-   **Scope**: `all_code`

Strict components must run in isolated containers containing only:
- Required runtime dependencies
- No compilers, package managers, or update utilities

This prevents runtime mutation.

### CRSS-12.0.1 - Compliance Process Requirement

-   **Category**: Process Integrity
-   **Type**: Process
-   **Profiles**:
    -   Core: SHOULD
    -   Strict: MUST (non-deviable for Level A)
-   **Scope**: `all_code`

All projects claiming CRSS compliance shall execute the full Compliance Process as defined in the Configuration and Deployment Integrity Specification.
A project is not compliant until all required artifacts have been produced, approved, versioned, and linked to a Safety Baseline.

### CRSS-12.0.2 - Safety Baseline Establishment

-   **Category**: Baseline Management
-   **Type**: Process
-   **Profiles**:
    -   Core: SHOULD
    -   Strict: MUST
-   **Scope**: `all_code`

All Strict releases shall define a **Safety Baseline**, consisting of:
- Source code commit hash
- Requirements version
- Test evidence package
- Interpreter and OS versions
- Dependency manifest
- Build and configuration flags
- Deployment architecture
- Platform characteristics
- Compliance artifacts (RCR, TEP, CBM, CC)

The baseline shall be immutable.

### CRSS-12.0.3 - Artifact Versioning

-   **Category**: Configuration Management
-   **Type**: Process
-   **Profiles**:
    -   Core: SHOULD
    -   Strict: MUST
-   **Scope**: `all_code`

All compliance artifacts (RCR, TEP, CBM, CC, Safety Baseline Report) shall:
- Be versioned
- Reference the same release identifier
- Be stored together
- Be cryptographically or checksum-protected against modification

Partial versioning is forbidden.

### CRSS-12.0.4 - Mandatory Artifact Completeness

-   **Category**: Verification Evidence
-   **Type**: Process
-   **Profiles**:
    -   Core: SHOULD
    -   Strict: MUST
-   **Scope**: `all_code`

A release is non-compliant unless all required artifacts are present and complete:
- RCR
- TEP
- CBM
- CC
- Safety Baseline Report (SBR)

Missing artifacts invalidate compliance.

### CRSS-12.0.5 - Artifact-to-Baseline Linkage

-   **Category**: Traceability
-   **Type**: Process
-   **Profiles**:
    -   Core: SHOULD
    -   Strict: MUST
-   **Scope**: `all_code`

Each artifact must:
- Reference the baseline identifier
- Reference all other artifacts in the baseline
- Reference the source commit hash

This creates a closed, traceable chain.

### CRSS-12.0.6 - Re-Approval Requirement

-   **Category**: Change Control
-   **Type**: Process
-   **Profiles**:
    -   Core: SHOULD
    -   Strict: MUST
-   **Scope**: `all_code`

Any change to any baseline element:
- Code
- Dependencies
- Interpreter
- OS
- Infrastructure
- Hardware
- Test suite

invalidates compliance and requires full re-approval.

No partial or incremental acceptance is allowed.

### CRSS-12.0.7 - Private Dependency Repository

-   **Category**: Supply Chain Integrity
-   **Type**: Process
-   **Profiles**:
    -   Core: SHOULD
    -   Strict: MUST
-   **Scope**: `all_code`

All dependencies shall be stored in a controlled, backed-up private repository.
Reliance on public registries (e.g., PyPI) at build time is prohibited.

### CRSS-12.0.8 - Reproducible Build Requirement

-   **Category**: Build Integrity
-   **Type**: Process
-   **Profiles**:
    -   Core: SHOULD
    -   Strict: MUST
-   **Scope**: `all_code`

The Safety Baseline must enable a build that can be reproduced to produce identical functionality and behavior using only baseline artifacts.
Missing information invalidates compliance.

### CRSS-12.0.9 - Interpreter Version Range with Single-Baseline Freeze

-   **Category**: Build Integrity
-   **Type**: Process
-   **Profiles**:
    -   Core: SHOULD
    -   Strict: MUST
-   **Scope**: `all_code`

The CRSS standard defines an allowed interpreter range (e.g., 3.9-3.12), BUT:
- Each project baseline shall select exactly one interpreter version from the allowed range.
- That version SHALL be frozen in the CBM.
- Changing the interpreter to another version inside the allowed range requires full re-approval and a new baseline.

### CRSS-12.1.1 - Unified Versioning

-   **Category**: Traceability
-   **Type**: Process
-   **Profiles**:
    -   Core: SHOULD
    -   Strict: MUST
-   **Scope**: `all_code`

All artifacts must:
- Share the same version number
- Be stored together
- Be approved together
- Never be separated

### CRSS-12.1.2 - Interpreter Version Range with Single-Baseline Freeze

-   **Category**: Controlled Upgrade Process
-   **Type**: Process
-   **Profiles**:
    -   Core: SHOULD
    -   Strict: MUST
-   **Scope**: `all_code`

**Phase 1 - Change Proposal**
- Document requested change
- Identify affected baseline elements
- Classify change (code, dependency, interpreter, OS, hardware)

**Phase 2 - Impact Analysis**
- Identify safety impact
- Reassess hazards
- Update risk analysis

**Phase 3 - Test Requalification**
- Re-run full TEP
- Re-run platform matrix
- Re-run performance and reliability tests

**Phase 4 - New Baseline Creation**
- Create new CBM
- Update RCR, TEP, SBR
- Assign new Baseline ID

**Phase 5 - Approval and Release**
- Independent approval
- Issue new Compliance Certificate

**Key Principles**:
- No “delta approval”
- No partial acceptance
- No auto-updates

Any change leads automatically to a new baseline.

### CRSS-12.1.3 - Emergency Release

-   **Category**: Controlled Upgrade Process
-   **Type**: Process
-   **Profiles**:
    -   Core: SHOULD
    -   Strict: MUST
-   **Scope**: `all_code`

A critical defect may trigger an Emergency Release, which:
- MUST follow the full Compliance Process
- MAY use accelerated execution paths

MUST produce:
- New CBM
- New TEP (focused but complete)
- New SBR
- New CC
- New Release ID

### CRSS-12.1.4 - Scope Limitation

-   **Category**: Controlled Upgrade Process
-   **Type**: Process
-   **Profiles**:
    -   Core: SHOULD
    -   Strict: MUST
-   **Scope**: `all_code`

Emergency Releases:
- SHALL contain only the minimal change required to correct the issue
- SHALL NOT introduce new functionality
- SHALL NOT update dependencies unless safety-justified

### CRSS-12.1.5 - Backport Requirement

-   **Category**: Controlled Upgrade Process
-   **Type**: Process
-   **Profiles**:
    -   Core: SHOULD
    -   Strict: MUST
-   **Scope**: `all_code`

Emergency fixes MUST be integrated back into:
- Next planned release
- Development branches
- Future baselines

No divergence.

---

## 18. Phase-Aware Interpretation Rules

> [⬆ Back to Table of Contents](#toc)

This section defines **normative phase-aware interpretation rules** for CRSS-Python.
They specify which operations are permitted during **Critical** and **Non-Critical**
execution phases.

A **Critical Phase** corresponds to execution of:
- `@critical` functions or methods,
- Strict safety-relevant logic,
- any computation whose behavior must be deterministic, bounded, and analyzable.

A **Non-Critical Phase** includes:
- initialization,
- I/O,
- configuration loading,
- validation,
- aggregation,
- interaction with external systems.

Unless explicitly stated otherwise, **Critical Phase rules take precedence**.

---

### 18.1. Collections, Allocation and Resource Management  
*(CRSS-5.4.1 / CRSS-5.4.2 / CRSS-5.4.3)*

#### Critical Phase
- Collections, large objects, and object pools used by critical code **MUST NOT grow**.
- They **MUST NOT** be mutated, resized, extended, pruned, or reallocated.
- Maximum size, structure, and membership **MUST be fixed or provably bounded** before entering the critical phase.
- No new entries may be added or removed during critical execution.

#### Non-Critical Phase
- Collections and pools MAY be populated, cleared, resized, rebuilt, or reset.
- Conditions:
  - explicit upper bounds **MUST** be enforced,
  - lifecycle management **MUST** be deterministic,
  - all state required by critical code **MUST** be fully initialized, validated, and bounded **before** critical execution begins.

---

### 18.2. Bulk Data Processing and Queries  
*(CRSS-5.5.2 / CRSS-5.5.3)*

#### Critical Phase
- Critical code **MUST NOT** perform:
  - chunked or streamed I/O,
  - pagination,
  - database queries,
  - distributed datastore access.
- All required data **MUST** be:
  - pre-filtered,
  - pre-aggregated,
  - pre-validated,
  - stored in bounded in-memory structures.

#### Non-Critical Phase
- Chunked I/O, pagination, and query-based processing MAY occur.
- Conditions:
  - per-operation volume **MUST** be explicit and bounded,
  - failures **MUST** follow CRSS robustness rules,
  - only reduced, bounded, validated results may be forwarded to critical computation.

---

### 18.3. Cache Semantics and Safety  
*(CRSS-5.6.1 / 5.6.2 / 5.6.3 / 7.8.5 / 7.8.6)*

#### Critical Phase
- Critical code **MUST NOT**:
  - insert into caches,
  - evict from caches,
  - mutate cache entries.
- It MAY read from caches **only if** they are:
  - pre-populated,
  - bounded,
  - deterministic.
- Behavior on missing or stale cache entries **MUST** be deterministic and lead to a defined safe outcome.

#### Non-Critical Phase
- Cache population, eviction, and refresh cycles MAY occur.
- Conditions:
  - cache size **MUST** be bounded,
  - lifetimes and eviction policies **MUST** be documented,
  - caches **MUST NOT** become a single source of truth for safety decisions,
  - updates **MUST NOT** violate invariants required by critical code.

---

### 18.4. Network, Microservices and Distributed Interaction  
*(CRSS-7.6.4 / 7.6.5 / 7.7.x / 7.8.2-7.8.4 / 7.9.4-7.9.6)*

#### Critical Phase
- Critical code **SHALL NOT** perform:
  - network calls,
  - remote API queries,
  - microservice RPCs,
  - retries,
  - circuit-breaker logic.
- Safety decisions **MUST** rely solely on:
  - already-available,
  - validated,
  - bounded local data.
- If data is stale or unavailable, a **fail-safe fallback** MUST be used.

#### Non-Critical Phase
- Network I/O, microservice interaction, retries, and circuit breakers MAY be used.
- Conditions:
  - strict latency budgets and timeout bounds,
  - partial-failure detection,
  - explicit status propagation,
  - critical code **MUST** tolerate no-response or stale-data conditions.

---

### 18.5. Parsing, Validation and Transfer Integrity  
*(CRSS-7.9.1-7.9.3 / 7.9.5)*

#### Critical Phase
- Critical code **MUST NOT**:
  - perform JSON/CSV/XML parsing,
  - perform schema validation,
  - execute integrity checks (CRC, checksum, signature),
  - stream or reassemble partial data.
- It may only consume data that is:
  - validated,
  - normalized,
  - bounded,
  - integrity-checked before entering the critical phase.

#### Non-Critical Phase
- Non-critical code **MUST** implement:
  - strict parsing,
  - schema validation,
  - malformed-input defenses,
  - checksum, hash, or signature verification.
- Only validated outputs may enter critical paths.

---

### 18.6. OS and Environment Interaction  
*(CRSS-7.10.1 / 7.10.2)*

#### Critical Phase
- Critical code **MUST NOT**:
  - read environment variables,
  - inspect the filesystem,
  - perform OS-level introspection,
  - query dynamic configuration sources.
- All required configuration **MUST** be:
  - resolved,
  - validated,
  - normalized,
  - frozen before entering the critical phase.

#### Non-Critical Phase
- Non-critical code MAY:
  - read environment variables,
  - load configuration files,
  - inspect limited OS information.
- Conditions:
  - all values **MUST** be validated,
  - all safety-relevant configuration **MUST** be frozen before critical execution,
  - dynamic configuration **MUST NOT** affect deterministic critical logic.

## 19. Summary
> [⬆ Back to Table of Contents](#toc)

This strengthens CRSS for:

- microservices and heavy network usage,
- big-data and streaming scenarios,
- sensitive data and cryptographic key handling,
- robustness against malformed input, index/key errors, and partial network operations,
- interaction with the underlying OS and environment variables.

These rules are designed to be **strict but realistic**: 
- they constrain unsafe patterns while allowing modern DevOps, microservices, and data-heavy architectures when carefully engineered.
