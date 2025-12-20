# CRSS-Python Safety Standard Mapping Annex

**Version:** v1.0.0
**Status:** Normative
**Maturity:** Stable
© 2025 Sofian Daghsen - All Rights Reserved
Distributed under CC BY-NC-ND 4.0

---

<a id="toc"></a>
## Table of Contents
- [CRSS-Python Safety Standard Mapping Annex](#crss-python-safety-standard-mapping-annex)
  - [Table of Contents](#table-of-contents)
  - [0. Purpose](#0-purpose)
  - [1. Safety Requirements and Levels](#1-safety-requirements-and-levels)
    - [1.1 CRSS Safety Levels vs Industry Notions](#11-crss-safety-levels-vs-industry-notions)
    - [1.2 Safety Goals Mapping To CRSS Safety Levels](#12-safety-goals-mapping-to-crss-safety-levels)
  - [2. CRSS Artifacts vs Safety Case Artifacts](#2-crss-artifacts-vs-safety-case-artifacts)
    - [2.1 High-Level Mapping](#21-high-level-mapping)
  - [3. Process Alignment V Model and ASPICE](#3-process-alignment-v-model-and-aspice)

---

## 0. Purpose

> [⬆ Back to Table of Contents](#toc)


This annex explains how **CRSS-Python** concepts map onto the terminology and expectations of common safety standards:

- ISO 26262 (automotive)
- DO-178C / DO-278A (avionics / ground)
- IEC 61508, EN 50128 / 50657 (industrial, rail)
- IEC 62304 (medical)
- ASPICE (process capability)

It is **non-normative**: it does not change any CRSS requirements, but helps auditors and system safety engineers interpret CRSS artifacts in familiar terms.

---

## 1. Safety Requirements and Levels

> [⬆ Back to Table of Contents](#toc)


### 1.1 CRSS Safety Levels vs Industry Notions

CRSS Safety Levels are internal abstractions:

- Level A - highest criticality  
- Level B - elevated risk  
- Level C - low/limited safety impact  

They conceptually correspond to:

- ISO 26262: ASIL D ≈ Level A, ASIL C/B ≈ Level B, ASIL A/QM ≈ Level C  
- DO-178C: DAL A/B ≈ Level A/B, DAL C/D ≈ Level B/C, DAL E ≈ outside scope  
- IEC 62304: Class C ≈ Level A/B, Class B ≈ Level B/C, Class A ≈ Level C  

**Note:** This is a *conceptual alignment* only. Final mapping remains a system-level responsibility.

### 1.2 Safety Goals Mapping To CRSS Safety Levels

System-level **safety goals / hazards / safety requirements** are NOT defined by CRSS.  
Instead:

- Safety goals and hazards are defined at system level (e.g. ISO 26262 Part 3/4).  
- The resulting safety requirements are allocated to software components.  
- CRSS Safety Levels (A/B/C) are then assigned to **code units** according to those allocations and recorded in the **Mode Assignment Register (MAR)** (SCEM-D1). :contentReference[oaicite:5]{index=5}  

---

## 2. CRSS Artifacts vs Safety Case Artifacts

> [⬆ Back to Table of Contents](#toc)


### 2.1 High-Level Mapping

| CRSS Concept / Artifact   | Typical Safety-Standard Equivalent                |
|---------------------------|---------------------------------------------------|
| SCEM                      | Safety case / structured assurance argument       |
| RTM (Requirements Traceability Matrix) | Traceability from HARA/HLR to LLR/tests |
| MAR (Mode Assignment Register) | Safety integrity allocation to code units   |
| CBD (Critical Boundary Declaration) | Definition of safety-critical execution boundary |
| RCR (Rule Compliance Report) | Coding standard compliance report (MISRA-like) |
| TEP (Test Evidence Package) | Verification evidence package (coverage, robustness, fault injection) |
| CBM (Configuration Baseline Manifest) | Baseline/configuration item definition |
| CRC (Certification Readiness Checklist) | Internal safety readiness review      |

These artifacts are already defined normatively in the SCEM and Compliance Master specifications; this annex simply explains their role in external safety arguments.   

---

## 3. Process Alignment V Model and ASPICE

> [⬆ Back to Table of Contents](#toc)


CRSS compliance phases map onto a V-model / ASPICE-style lifecycle as follows:

- CRSS Phase 0-1 -> Concept, system and software requirements, planning (ASPICE SYS.x / SWE.1)  
- CRSS Phase 2 -> Design and implementation constraints + static compliance (SWE.2-SWE.3)  
- CRSS Phase 3 -> Verification and validation (SWE.4, SWE.5)  
- CRSS Phase 4 -> Integration of evidence into a single SCEM package (SUP.x, SYS.4)  
- CRSS Phase 5 -> Independent assessment and release decision (SUP.1, safety management roles) :contentReference[oaicite:7]{index=7}  

Organizations can attach their own ASPICE mapping tables to this annex, referencing the same CRSS artifacts.