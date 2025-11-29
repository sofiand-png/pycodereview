
# CRSS-Python Repository & Publication Standard  
Version: v3.0.0  
Status: Normative – Governance Layer  
© 2025 Sofian Daghsen – All rights reserved  

---

## 0. Purpose

This specification defines **how the CRSS-Python standard itself is structured, versioned, and published**, so that:

- Implementers and auditors can **find the right documents quickly**.
- Tooling can **parse and integrate** the specifications reliably.
- Changes to the standard are **controlled, traceable, and reviewable**.
- Safety claims based on CRSS-Python are **repeatable over time**.

It covers:

- Repository layout  
- Document taxonomy (normative vs informative)  
- Versioning & change control  
- Rule ID stability & deprecation policy  
- Publication and release practices  

This standard applies to the **CRSS-Python specification repository itself**, and is **recommended** for projects that create their own internal profiles or extensions.

---

## 1. Document Taxonomy

### 1.1 Normative vs Informative

All official CRSS-Python documents MUST be classified as:

- **Normative** – defines requirements, rules, criteria, or mandatory processes.  
- **Informative** – provides guidance, examples, explanations, or rationale.

Normative documents define **compliance**.  
Informative documents **support** compliance, but do not change it.

### 1.2 Core Normative Documents (v3.x)

At minimum, the following normative documents MUST exist in the repository:

1. **crss_python_unified_safety_spec_v3.x.x.md**  
   – Modes, Profiles, Levels, Critical/Non-Critical, propagation, enforcement.

2. **crss_python_compliance_master_v3.x.x.md**  
   – Compliance phases, acceptance criteria, enforcement logic.

3. **crss_python_SCEM_master_v3.x.x.md**  
   – Safety Case Evidence Model, SCEM annexes, Safety Maturity Model.

4. **crss_python_tooling_automation_master_v3.x.x.md**  
   – Tool requirements, automation, TCA, templates.

5. **crss_python_deployment_release_baseline_master_v3.x.x.md**  
   – Deployment, Release, CBM, zero-drift policy.

6. **crss_python_standard_levels_v3.x.x.md** (or equivalent)  
   – Applicability mapping to ASIL/SIL/DO-178C/IEC 62304, under v3 model.

7. **crss_python_governance_compliance_master_v3.x.x.md**  
   – Governance-level consolidation (if maintained separately from Compliance Master).

Any additional normative documents MUST follow the same naming pattern:

```text
crss_<scope>_<topic>_vMAJOR.MINOR.PATCH.md
```

### 1.3 Informative Documents

Examples of informative documents:

- Example implementations  
- Tutorial guides  
- FAQ / rationale  
- Internal discussion notes  

MUST be clearly labeled as:

```text
Status: Informative
```

and MUST NOT introduce new MUST / MUST-NOT requirements.

---

## 2. Repository Layout

A CRSS-Python standard repo SHOULD follow this structure:

```text
/
├─ specs/
│  ├─ normative/
│  │  ├─ crss_python_unified_safety_spec_v3.0.0.md
│  │  ├─ crss_python_compliance_master_v3.0.1.md
│  │  ├─ crss_python_SCEM_master_v3.0.0.md
│  │  ├─ crss_python_tooling_automation_master_v3.0.0.md
│  │  ├─ crss_python_deployment_release_baseline_master_v3.0.0.md
│  │  ├─ crss_python_standard_levels_v3.0.0.md
│  │  └─ ...
│  └─ informative/
│     ├─ crss_examples_overview.md
│     ├─ crss_rationale_notes.md
│     └─ ...
├─ rules/
│  ├─ core_rules_catalog.yaml
│  ├─ strict_rules_catalog.yaml
│  └─ deviations_matrix.yaml
├─ schemas/
│  ├─ mar_schema.yaml
│  ├─ cbm_schema.yaml
│  ├─ scem_schema.yaml
│  └─ tooling_output_schema.yaml
├─ examples/
│  ├─ safety_controller_example/
│  └─ ...
├─ tools/
│  ├─ reference_analyzer/
│  └─ scripts/
├─ changelog/
│  ├─ CHANGELOG_v3.x.md
│  └─ retired_rules.md
└─ README.md
```

This structure is **recommended** and **tool-friendly**.

---

## 3. Versioning Policy

### 3.1 Semantic Versioning (Specs)

All CRSS-Python specifications MUST use a semantic-like versioning scheme:

```text
MAJOR.MINOR.PATCH
```

- **MAJOR** – breaking conceptual changes (e.g., v2 → v3).  
- **MINOR** – backward-compatible additions or clarifications.  
- **PATCH** – typo fixes, editorial corrections, non-behavioral clarifications.

### 3.2 Alignment Across Documents

For a **coherent standard release**, the following MUST hold:

- All core normative docs MUST share the same MAJOR version.  
- A **“v3.0 baseline”** is defined as the set of all normative docs where `MAJOR = 3` and `MINOR = 0`, even if PATCH differs slightly.

Example:

- Unified Safety Spec: v3.0.0  
- Compliance Master: v3.0.1  
- SCEM Master: v3.0.0  
- Tooling Master: v3.0.0  
- Deployment Master: v3.0.0  

All belong to the **3.0 baseline**.

### 3.3 Python Version Support Declaration

The standard itself may declare a supported Python version range (e.g., 3.9–3.12).  
HOWEVER:

> 🧷 Every **project** and every **CBM** MUST specify exactly **one concrete Python version**.  
> Supporting another Python version requires a new project baseline.

This rule is normative and MUST appear consistently in all relevant specs.

---

## 4. Rule Catalog & Rule IDs

### 4.1 Rule Catalog Storage

Rule catalogs MUST be stored in machine-readable format:

- `rules/core_rules_catalog.yaml`  
- `rules/strict_rules_catalog.yaml`

Each rule MUST have:

- Stable ID (e.g. `CRSS-3.1.2`)  
- Short name  
- Description  
- Category (e.g. dynamic features, concurrency, memory)  
- Profiles:
  - Core: MUST/SHOULD/MUST-NOT/SHOULD-NOT/N/A  
  - Strict: same scale  
- Scope: global / phase-scoped (`critical_only`, `any_phase`)  
- References to sections in normative documents.

### 4.2 ID Stability

Rule IDs are **globally stable**:

- IDs MUST NOT be reused.  
- If a rule is retired or superseded:
  - It MUST be marked as `status: retired` in the catalog.
  - A `superseded_by` field SHOULD reference the new rule(s).

### 4.3 Deviations Matrix

A `deviations_matrix.yaml` SHOULD:

- Map rules → acceptable deviation types → applicable Modes  
- Explicitly forbid deviations for:
  - Strict-A `@critical` code (NO deviations allowed)  
- Describe documentation and approval requirements for Strict-A non-critical deviations.

---

## 5. Change Control & Governance

### 5.1 Branching Model

Recommended branching model:

- `main` – latest stable, published standard  
- `develop` – integration of upcoming MINOR/PATCH updates  
- `feature/*` – proposal branches for larger changes

### 5.2 Change Types

| Change Type | Affects | Requires |
|------------|---------|----------|
| Editorial  | Text only, no behavior | PR + 1 reviewer |
| Clarification | Interpretation, no new obligations | PR + 2 reviewers |
| Behavioral (MINOR) | New rules, stronger conditions | PR + 2 reviewers + version bump |
| Breaking (MAJOR) | Model changes, concepts | Governance decision + vX.0.0 |

### 5.3 Governance Roles

At minimum, the standard governance SHOULD define:

- **Spec Owner** – responsible for coherence of the whole standard.  
- **Safety Architect** – responsible for safety soundness of changes.  
- **Tooling Lead** – ensures tools can implement new requirements.  
- **Certification Liaison** – ensures changes remain acceptable in regulated domains.

---

## 6. Publication & Release of the Standard

### 6.1 Standard Releases (Spec-Level)

Each official **Standard Release** MUST:

- Tag the repository (e.g., `v3.0.0-standard`)  
- Include:
  - All normative specs for that baseline.  
  - A `STANDARD_RELEASE_NOTES_v3.0.0.md` file describing changes.  
- Ensure all links and cross-references between documents are valid.

### 6.2 Backward Compatibility Notes

For each release, there MUST be a section:

```markdown
## Backward Compatibility

- Breaking changes:
- Compatible with vX.Y.Z at project-level if:
```

This allows users to determine whether they must re-certify their projects.

### 6.3 Archive Policy

Older standard releases MUST be:

- Archived but kept readable  
- Tagged and not modified afterward  
- Clearly marked as “superseded”

Projects still using a superseded standard MUST state this explicitly in their safety case.

---

## 7. Machine-Readable Schemas

### 7.1 Required Schemas

The `schemas/` directory SHOULD contain:

- `mar_schema.yaml` – Mode Assignment Register format  
- `cbm_schema.yaml` – Configuration Baseline Manifest format  
- `scem_schema.yaml` – SCEM structure  
- `tooling_output_schema.yaml` – minimal fields for RCR, coverage, etc.

These schemas allow:

- Validation of project artifacts  
- Automated compliance checks  
- Tool interoperability

### 7.2 Schema Versioning

Schemas MUST:

- Be versioned in sync with the standard (same MAJOR).  
- Include a `schema_version` field.  
- Provide migration notes when fields are added/removed.

---

## 8. Example Folder Guidance

The `examples/` folder SHOULD contain:

- At least one **Strict-A reference implementation**:
  - With fully annotated Modes and Phases.  
  - With accompanying MAR, CBM, SCEM excerpt.

- Optionally, additional examples for:
  - Microservices  
  - Data processing applications  
  - Network-heavy systems  

All examples MUST:

- Be labeled `Status: Informative`.  
- Not override normative rules in text.  
- Be kept consistent with the latest major version.

---

## 9. Alignment With Design Decisions

This Repository & Publication Standard is explicitly aligned with the following design decisions:

1. **Modes** (Profile × Safety Level) govern enforcement everywhere.  
2. **Critical vs Non-Critical** execution is explicitly modeled as `@critical` and `@non_critical_phase`.  
3. Strict-A uses **Option 2** deviation handling:
   - Zero violations allowed in `@critical`.  
   - Non-critical deviations allowed only with strong governance.  
4. **One Python version per project** is mandatory.  
5. No hidden changes: configuration, tools, or dependencies drifting after CBM invalidate certification.  
6. All rule catalogs, schemas, and examples are machine-readable and tool-friendly.  

Any new or updated document **MUST NOT contradict** these principles.

---

## 10. Summary

This specification:

✅ Defines how CRSS-Python itself is structured, versioned, and published.  
✅ Separates normative vs informative content.  
✅ Provides a clear, extensible repo layout.  
✅ Stabilizes rule IDs and schemas for long-term use.  
✅ Ensures users always know **which version** of the standard they are using.  
✅ Makes it possible to build tools and certification processes on top of CRSS-Python with confidence.

It is strongly recommended that this Repository & Publication Standard be treated as **normative** for the CRSS-Python project itself and closely followed by any organizations maintaining their own internal CRSS-based standards.

---
