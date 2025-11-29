
# CRSS-Python Common Mistakes & How to Avoid Them
Version: v3.0.0  
Status: Informative  
© 2025 Sofian Daghsen – All rights reserved  

---

# ✅ 1. Mixing Critical and Non-Critical Code

**Mistake:**  
Putting critical and non-critical logic in the same function.

**Fix:**  
Use `@critical` and `@non_critical_phase` to separate code cleanly.

---

# ✅ 2. Forgetting that Strict-A is Zero Tolerance

**Mistake:**  
Assuming Strict-A allows minor deviations.

**Fix:**  
Strict-A `@critical` = **zero violations**, zero exceptions.

---

# ✅ 3. Using Threads in Critical Logic

**Mistake:**  
Relying on Python threads for timing-sensitive logic.

**Fix:**  
Use single-threaded deterministic execution in `@critical`.

---

# ✅ 4. Relying on Hotfixes or Quick Patches

**Mistake:**  
Fixing issues directly in production.

**Fix:**  
New change = new release + new CBM + new compliance cycle.

---

# ✅ 5. Runtime Installation or Updates

**Mistake:**  
Installing packages at runtime.

**Fix:**  
Freeze dependencies and use private repositories.

---

# ✅ 6. Unbounded Loops or Recursion

**Mistake:**  
Using loops without clear bounds or recursion in critical paths.

**Fix:**  
Use bounded loops and iterative logic only.

---

# ✅ 7. Large Critical Functions

**Mistake:**  
Packing too much logic into `@critical` functions.

**Fix:**  
Keep them **small, pure, deterministic**.

---

# ✅ 8. Direct External Input in Critical Code

**Mistake:**  
Feeding raw input to safety-critical logic.

**Fix:**  
Validate, sanitize, and range-check BEFORE entering `@critical`.

---

# ✅ 9. Dynamic Behavior

**Mistake:**  
Using dynamic imports, reflection, monkeypatching, or exec/eval.

**Fix:**  
Avoid dynamic constructs; use static, explicit designs.

---

# ✅ 10. Ignoring the One-Python-Version Rule

**Mistake:**  
Trying to support multiple Python versions in one project.

**Fix:**  
One project = one Python version = frozen in CBM.

---

# ✅ 11. Untested Edge Cases

**Mistake:**  
Only testing happy paths.

**Fix:**  
MC/DC, boundary testing, fault injection, platform matrix tests.

---

# ✅ 12. Skipping Documentation Early

**Mistake:**  
Leaving documentation for the end.

**Fix:**  
Build MAR, RCR, SCEM progressively.

---

# ✅ 13. Overusing Shared State

**Mistake:**  
Passing mutable state across components.

**Fix:**  
Prefer immutable data, message-passing, and clear interfaces.

---

# ✅ 14. Assuming Compliance = Safety

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

# ✅ 15. Trying to Jump Directly to Strict-A

**Mistake:**  
Starting at the highest rigor immediately.

**Fix:**  
Grow gradually:
Core → Strict → Strict-B → Strict-A

---

# ✅ Summary

Most mistakes come from:

❌ Mixing concerns  
❌ Overcomplicating critical logic  
❌ Ignoring determinism  
❌ Treating deployments as mutable  

Avoid these, and compliance becomes far smoother and safer.

---
