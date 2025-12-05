# Integration with V-Model and ASPICE

**Version:** v1.0.0
**Status:** Informative
**Maturity:** Stable
© 2025 Sofian Daghsen — All Rights Reserved
Distributed under CC BY-NC-ND 4.0

---

This section is informative. It describes how the CRSS compliance lifecycle aligns with a classical V-model and ASPICE process landscape.

- **System & Software Requirements (V-model left side / ASPICE SYS.x, SWE.1):**  
  Safety goals, hazards, and system-level safety requirements are defined outside CRSS. CRSS begins once requirements have been allocated to software components. Mode Assignment (MAR) then encodes these allocations into Safety Levels A/B/C.

- **Software Design & Implementation (SWE.2, SWE.3):**  
  CRSS Phase 2 (Static Analysis) and the CRSS Mode & Safety Model govern how design and implementation are constrained (profiles, modes, critical / non-critical, import and inheritance rules).

- **Verification & Validation (SWE.4, SWE.5):**  
  CRSS Phase 3 (Dynamic & Behavioral Analysis) and SCEM-D4 define test evidence, coverage targets, MC/DC expectations, fault injection and determinism validation.

- **Configuration & Change Management (SUP.x):**  
  CBM, one-version Python policy, and drift-prevention rules define configuration and environment integrity.

- **Safety Case & Assessment:**  
  SCEM (D1–D6) plus Phase 5 (Independent Approval & Release) provide the structured evidence used as the software part of the safety case for an external assessment or certification program.

Organizations MAY attach their internal ASPICE mapping tables and safety management processes to this section without modifying CRSS requirements.
