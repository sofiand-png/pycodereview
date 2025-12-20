# CRSS-Python Common Mistakes and How to Avoid Them

**Version:** v1.0.0
**Status:** Informative
**Maturity:** Stable
© 2025 Sofian Daghsen - All rights reserved
Distributed under CC BY-NC-ND 4.0 - see LICENSE-CRSS.

---

<a id="toc"></a>
## Table of Contents
- [CRSS-Python Common Mistakes and How to Avoid Them](#crss-python-common-mistakes-how-to-avoid-them)
  - [Table of Contents](#table-of-contents)
- [1. Mixing Critical and Non-Critical Code](#1-mixing-critical-and-non-critical-code)
- [2. Forgetting that Strict-A is Zero Tolerance](#2-forgetting-that-strict-a-is-zero-tolerance)
- [3. Using Threads in Critical Logic](#3-using-threads-in-critical-logic)
- [4. Relying on Hotfixes or Quick Patches](#4-relying-on-hotfixes-or-quick-patches)
- [5. Runtime Installation or Updates](#5-runtime-installation-or-updates)
- [6. Unbounded Loops or Recursion](#6-unbounded-loops-or-recursion)
- [7. Large Critical Functions](#7-large-critical-functions)
- [8. Direct External Input in Critical Code](#8-direct-external-input-in-critical-code)
- [9. Dynamic Behavior](#9-dynamic-behavior)
- [10. Ignoring the One-Python-Version Rule](#10-ignoring-the-one-python-version-rule)
- [11. Untested Edge Cases](#11-untested-edge-cases)
- [12. Skipping Documentation Early](#12-skipping-documentation-early)
- [13. Overusing Shared State](#13-overusing-shared-state)
- [14. Assuming Compliance = Safety](#14-assuming-compliance-safety)
- [15. Trying to Jump Directly to Strict-A](#15-trying-to-jump-directly-to-strict-a)
- [Summary](#summary)

---

# 1. Mixing Critical and Non-Critical Code

**Mistake:**
Putting critical and non-critical logic in the same function.

**Fix:**
Use `@critical` and `@non_critical_phase` to separate code cleanly.

---

# 2. Forgetting that Strict-A is Zero Tolerance

**Mistake:**
Assuming Strict-A allows minor deviations.

**Fix:**
Strict-A `@critical` = **zero violations**, zero exceptions.

---

# 3. Using Threads in Critical Logic

**Mistake:**
Relying on Python threads for timing-sensitive logic.

**Fix:**
Use single-threaded deterministic execution in `@critical`.

---

# 4. Relying on Hotfixes or Quick Patches

**Mistake:**
Fixing issues directly in production.

**Fix:**
New change = new release + new CBM + new compliance cycle.

---

# 5. Runtime Installation or Updates

**Mistake:**
Installing packages at runtime.

**Fix:**
Freeze dependencies and use private repositories.

---

# 6. Unbounded Loops or Recursion

**Mistake:**
Using loops without clear bounds or recursion in critical paths.

**Fix:**
Use bounded loops and iterative logic only.

---

# 7. Large Critical Functions

**Mistake:**
Packing too much logic into `@critical` functions.

**Fix:**
Keep them **small, pure, deterministic**.

---

# 8. Direct External Input in Critical Code

**Mistake:**
Feeding raw input to safety-critical logic.

**Fix:**
Validate, sanitize, and range-check BEFORE entering `@critical`.

---

# 9. Dynamic Behavior

**Mistake:**
Using dynamic imports, reflection, monkeypatching, or exec/eval.

**Fix:**
Avoid dynamic constructs; use static, explicit designs.

---

# 10. Ignoring the One-Python-Version Rule

**Mistake:**
Trying to support multiple Python versions in one project.

**Fix:**
One project = one Python version = frozen in CBM.

---

# 11. Untested Edge Cases

**Mistake:**
Only testing happy paths.

**Fix:**
MC/DC, boundary testing, fault injection, platform matrix tests.

---

# 12. Skipping Documentation Early

**Mistake:**
Leaving documentation for the end.

**Fix:**
Build MAR, RCR, SCEM progressively.

---

# 13. Overusing Shared State

**Mistake:**
Passing mutable state across components.

**Fix:**
Prefer immutable data, message-passing, and clear interfaces.

---

# 14. Assuming Compliance = Safety

**Mistake:**
Thinking passing rules means the system is safe.

**Fix:**
Safety also depends on:
- System design
- Hardware
- Redundancy
- Validation
- Human factors

CRSS-Python covers **software integrity**, not full system safety.

---

# 15. Trying to Jump Directly to Strict-A

**Mistake:**
Starting at the highest rigor immediately.

**Fix:**
Grow gradually:
Core → Strict → Strict-B → Strict-A

---

# Summary

Most mistakes come from:

- Mixing concerns
- Overcomplicating critical logic
- Ignoring determinism
- Treating deployments as mutable

Avoid these, and compliance becomes far smoother and safer.

---
