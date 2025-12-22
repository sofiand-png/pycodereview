# CRSS-Python External Assessment Protocol (EAP)

**Version:** v1.0.0
**Status:** Normative
**Maturity:** Stable
© 2025 Sofian Daghsen - All rights reserved
Distributed under CC BY-NC-ND 4.0 - see LICENSE-CRSS.

---

<a id="toc"></a>
## Table of Contents
- [CRSS-Python External Assessment Protocol (EAP)](#crss-python-external-assessment-protocol-eap)
  - [Table of Contents](#table-of-contents)
  - [0. Purpose](#0-purpose)
  - [1. Definitions](#1-definitions)
    - [1.1 Rule Compliance Report (RCR)](#11-rule-compliance-report-rcr)
    - [1.2 Compliance Certificate (CC)](#12-compliance-certificate-cc)
    - [1.3 Release Certificate (RC)](#13-release-certificate-rc)
    - [1.4 Assessment Report (AR)](#14-assessment-report-ar)
    - [1.5 Deployment Snapshot](#15-deployment-snapshot)
    - [1.6 Third-Party Register (TPR)](#16-third-party-register-tpr)
    - [1.7 Baseline ID](#17-baseline-id)
    - [1.8 Release ID](#18-release-id)
    - [1.9 Non-Conformance (NC)](#19-non-conformance-nc)
  - [2. Assessment Inputs](#2-assessment-inputs)
  - [3. Assessment Stages](#3-assessment-stages)
    - [3.1 Stage0 Intake and Eligibility](#31-stage0-intake-and-eligibility)
    - [3.2 Stage1 Structural Completeness](#32-stage1-structural-completeness)
    - [3.3 Stage2 Evidence and RCR Verification](#33-stage2-evidence-and-rcr-verification)
    - [3.4 Stage3 Technical Deep-Dive Sampling](#34-stage3-technical-deep-dive-sampling)
    - [3.5 Stage4 Decision and Reporting](#35-stage4-decision-and-reporting)
    - [3.6 Interpretation of Conditional Stage Outcomes](#36-interpretation-of-conditional-stage-outcomes)
  - [4. Non-Conformance Handling](#4-non-conformance-handling)
  - [5. Revocation and Reassessment](#5-revocation-nd-reassessment)
  - [6. Summary of Enhancements](#6-summary-of-enhancements)

---

## 0. Purpose

> [⬆ Back to Table of Contents](#toc)


The **CRSS-Python External Assessment Protocol (EAP)** defines how independent assessors shall:

- Evaluate CRSS-Python compliant systems
- Review safety cases and compliance evidence
- Validate rule compliance outcomes, thresholds, and assumptions
- Judge conformance against CRSS profiles (Core, Strict, Strict Level A)
- Decide certification, non-certification, and revocation
- Ensure every term, artifact, and component is unambiguously defined

This version introduces:

- Explicit inclusion of the **Rule Compliance Report (RCR)** as a mandatory input
- Definitions for all referenced terms not previously defined
- Formal linkage: **RCR -> Compliance Certificate -> Release Certificate -> EAP decision**

EAP is mandatory for all projects claiming **CRSS-Strict Level A** and recommended for all CRSS-Strict deployments.

---

## 1. Definitions

> [⬆ Back to Table of Contents](#toc)


To eliminate ambiguity, all terms used in EAP are defined below.

### 1.1 Rule Compliance Report (RCR)

A formal document generated during the Compliance Process containing:

- Pass/fail status for every applicable rule
- MUST/SHOULD classification outcomes
- List of violations and justifications
- Compliance thresholds applied
- Test or tooling evidence references
- Approval signatures and timestamps

RCR is **objective evidence** of rule-level compliance.

### 1.2 Compliance Certificate (CC)

A signed declaration that:

- All compliance requirements have been met
- RCR and supporting evidence are complete
- The project is being formally submitted for assessment

The CC does **not** prove compliance; it requests approval.

### 1.3 Release Certificate (RC)

A signed declaration that:

- The approved baseline is authorized for deployment
- No changes may occur post-certification
- The Release ID matches the Configuration Baseline

### 1.4 Assessment Report (AR)

The final output of EAP documenting:

- Findings and non-conformances
- Assessment outcomes
- Approval signatures
- Final certification status (CERTIFIED / NOT CERTIFIED)

### 1.5 Deployment Snapshot

A frozen image containing:

- OS
- Interpreter
- Dependencies
- Configuration
- Containers/VMs
- Hardware spec
- Hashes

Used to confirm zero drift.

### 1.6 Third-Party Register (TPR)

A list of:

- External components
- Versions
- Communication interfaces
- Safety relevance
- Risk assessment status

### 1.7 Baseline ID

A unique identifier referencing a frozen Safety Baseline:

- Source code hash
- Environment versions
- Dependency hashes
- Test results
- Evidence versions

### 1.8 Release ID

Unique identifier for a deployed release, always linked to a Baseline ID.

### 1.9 Non-Conformance (NC)

Any deviation from:

- Rules
- Policies
- Baseline
- Evidence requirements
- Approved assumptions

Classified NC-0 to NC-3.

---

## 2. Assessment Inputs

> [⬆ Back to Table of Contents](#toc)


The External Assessor SHALL receive, at minimum:

1. **Certification Readiness Kit (CRK)**, including:
   - Safety Case (SCEM)
   - Configuration Baseline Manifest (CBM)
   - Hazard Log (HLG)
   - FMEA
   - Test Evidence Package (TEP)
   - Performance and Timing Report (PTR)
   - Architecture Decision Records (ADR)
   - Third-Party Register (TPR)
   - Deployment Snapshot
   - Certified Artifact (.whl) exists and hash matches CBM.

2. **Rule Compliance Report (RCR) - Mandatory**
   - Must be complete, signed, hashed, and versioned.
   - Must cover all MUST and SHOULD rules.
   - Must reference all supporting evidence.

3. **Acceptance Rules Addendum**
   - Defines MUST/SHOULD thresholds.

4. **Toolchain Confidence Assessment (TCA)**

5. **Deployment and Configuration Policy**

6. **Release Management Records**
   - Baseline ID
   - Release ID
   - Draft Compliance Certificate (CC)
   - Draft Release Certificate (RC)

If RCR is missing or incomplete, the assessment MUST be recorded as **“NOT ASSESSABLE.”**

---

## 3. Assessment Stages

> [⬆ Back to Table of Contents](#toc)


EAP defines a **5-stage assessment sequence**:

1. **Stage 0 - Intake and Eligibility Check**
2. **Stage 1 - Structural Completeness Review**
3. **Stage 2 - Evidence and RCR Verification**
4. **Stage 3 - Technical Deep-Dive Sampling**
5. **Stage 4 - Decision and Reporting**

Each stage has explicit status codes (PASS / CONDITIONAL / FAIL) to keep the assessment outcome objective and traceable.

- **PASS-Sx** - Stage x fully satisfied
- **COND-Sx** - Stage x conditionally satisfied, minor issues remediable without full restart
- **FAIL-Sx** - Stage x not satisfied; assessment cannot proceed until corrected

For Strict Level A, certification SHALL ONLY be granted if all applicable stages reach PASS-Sx.
Any unresolved COND-Sx SHALL result in NOT CERTIFIED.
---

### 3.1 Stage0 Intake and Eligibility

EA SHALL:

- Verify CRK completeness
- Confirm declared CRSS profile (Core / Strict / Strict Level A)
- Validate that profile matches system safety level (ASIL/SIL/Class)

**Outcome codes**

- **PASS-S0** - Inputs received, scope consistent
- **FAIL-S0** - Missing CRK, missing basic artifacts, or profile/scope mismatch

If **FAIL-S0**, the system is marked **NOT ASSESSABLE**; no further stages are executed.

---

### 3.2 Stage1 Structural Completeness

EA SHALL confirm:

- All required artifacts exist (SCEM, HLG, FMEA, TEP, PTR, CBM, TPR, Deployment Snapshot, RCR, CC draft, RC draft)
- All artifacts have hashes, signatures, and versions
- Release ID ↔ Baseline ID alignment is consistent

**Outcome codes**

- **PASS-S1** - Structurally complete, no missing or inconsistent artifacts
- **COND-S1** - Minor inconsistencies (for example, missing non-critical annotation) that can be corrected without altering code or baseline
- **FAIL-S1** - Missing mandatory artifacts, inconsistent IDs, or untraceable elements

Strict Level A: any **COND-S1** must be resolved to **PASS-S1** before final approval.

---

### 3.3 Stage2 Evidence and RCR Verification

EA SHALL validate:

- RCR exists, is signed, hashed, and versioned
- 100% of MUST rules are passed
- SHOULD-rule violations are within thresholds for the claimed profile (Core/Strict); for Strict Level A, no SHOULD violations are permitted
- Each violation is documented and justified, with risk assessment and approval where applicable
- Evidence referenced in the RCR (tests, analysis, reviews) exists and is traceable
- Acceptance Rules Addendum has been properly applied

**Outcome codes**

- **PASS-S2** - RCR is internally consistent, thresholds are satisfied, and evidence fully supports the reported compliance status
- **COND-S2** - Minor documentation gaps (for example, missing rationale text for a justified SHOULD violation) that do not change the compliance outcome but must be corrected
- **FAIL-S2** - Any missing RCR, failed MUST rules, exceeded SHOULD thresholds, unjustified violations, or missing evidence references

Strict Level A: any **COND-S2** must be resolved to **PASS-S2**. Any **FAIL-S2** mandates rework of compliance and evidence before reassessment.

---

### 3.4 Stage3 Technical Deep-Dive Sampling

EA SHALL:

- Sample code modules from critical areas (Strict Level A components)
- Confirm that key RCR findings match actual implementation
- Verify that automated tooling (static analysis, coverage tools, CI checks) has been correctly configured and executed
- Cross-check sampled behavior against TEP and PTR

**Outcome codes**

- **PASS-S3** - Samples confirm that claimed processes and evidence match reality; no systemic inconsistencies detected
- **COND-S3** - Minor discrepancies in sampled modules that can be corrected with targeted fixes and follow-up evidence, without invalidating the overall process
- **FAIL-S3** - Evidence of systemic misalignment (for example, tools misconfigured, rules routinely ignored, or RCR materially inconsistent with actual code)

Strict Level A: conditional passes (**COND-S3**) require remediation and re-sampling; final approval requires **PASS-S3**.

---

### 3.5 Stage4 Decision and Reporting

The External Assessor SHALL synthesize S0-S3 outcomes into a final decision:
- **CERTIFIED**
- **NOT CERTIFIED**


The assessment MAY remain in a PENDING state while conditional findings are being remediated.
A system in PENDING state is NOT CERTIFIED and SHALL NOT be deployed under CRSS claims.

Certification SHALL only be granted once all conditional findings are resolved
and all applicable stages reach PASS-Sx.


The Assessment Report (AR) MUST:

- Record all stage outcomes (PASS-Sx / COND-Sx / FAIL-Sx)
- Reference the RCR explicitly
- List all non-conformances with NC levels

### 3.6 Interpretation of Conditional Stage Outcomes

Conditional stage outcomes (COND-Sx):

- indicate that the assessment MAY continue,
- do NOT constitute approval,
- do NOT authorize deployment,
- do NOT imply partial certification.

A system with any unresolved COND-Sx SHALL be considered NOT CERTIFIED.


---

## 4. Non-Conformance Handling

> [⬆ Back to Table of Contents](#toc)


NC rules are unchanged:

- NC-0: Informational
- NC-1: Minor
- NC-2: Major
- NC-3: Critical

For Strict Level A:

- Any NC affecting MUST rules -> BLOCKER
- Any NC-1 or higher -> BLOCKER

---

## 5. Revocation and Reassessment

> [⬆ Back to Table of Contents](#toc)


Certification SHALL be revoked if:

- Drift is detected
- RCR was found inaccurate
- New hazards emerge
- Artifacts are altered post-certification

---

## 6. Summary of Enhancements

> [⬆ Back to Table of Contents](#toc)


- RCR added as a mandatory input
- RCR verification added to Stage 2 and Stage 3
- All undefined terms formally defined
- End-to-end traceability clarified

This closes the compliance loop:

**RCR -> CC -> RC -> EAP -> AR**
