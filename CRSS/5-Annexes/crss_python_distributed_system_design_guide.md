# CRSS Distributed System Design Guide

**Version:** v1.0.0
**Status:** Informative
**Maturity:** Stable
© 2025 Sofian Daghsen – All rights reserved
Distributed under CC BY-NC-ND 4.0 — see LICENSE-CRSS.

**Domain:** Multi-Component CRSS Architectures
**Audience:** System Architects, Integrators, Safety Engineers

---

## 1. Purpose
This document explains **how CRSS-compliant components can coexist in a distributed architecture** while maintaining full compliance with strict determinism and mixed-criticality rules.

This guide is *model-level only* (no implementation).

---

## 2. Distributed System Layers

A CRSS multi-component architecture typically includes:

1. **Sensor Gateway (Core-C)**  
   Responsible for ingesting data from hardware, simulation, or vehicle buses.

2. **Preprocessing / Fusion Node (Core-B)**  
   Performs bounded mathematical transformations.

3. **Strict-A Deterministic Controller**  
   The safety-critical path.

4. **Actuator Gateway / Safety Filter (Core-C)**  
   Sends commands to external systems.

5. **Supervisory Components (Core-C)**  
   Logging, visualization, remote monitoring.

---

## 3. Allowed Interactions

### 3.1 Strict-A Allowed Inputs
- Validated, sanitized numeric values (bounded arrays / sets)
- Previous actuator output
- Deterministic config
- Pre-structured envelopes

Strict-A **cannot** receive:
- raw messages
- JSON
- timestamps
- strings
- exceptions
- None values

### 3.2 Strict-A Outputs
- Numeric command
- Status enum
- Safe_default_used flag
- Reason code

No metadata, no timestamps.

---

## 4. Message-Passing Contracts

### 4.1 Core-C → Strict-A Contract
- Flat arrays
- All numeric values validated before entry
- Arrays with fixed length
- No undefined/null/NaN

### 4.2 Strict-A → Core-C Contract
- Command + status
- No embedded types
- No unbounded payloads

---

## 5. Fault Propagation Rules

### 5.1 Critical Path Isolation
Faults from Core-C must not enter Strict-A.

### 5.2 Failsafe Guarantees
Strict-A fallback is **purely local**:
- ignores external timing
- ignores JSON issues
- uses deterministic fallback

---

## 6. Scaling Up to Multiple Controllers
Examples:
- multiple actuation surfaces
- multiple sensor clusters
- multiple voting blocks
- hierarchical supervision

Rules:
- Each Strict-A block must remain independent.
- Fusion layers must not increase criticality beyond Core-B.
- Gateways must be deterministic in size and shape.

---

## 7. Mixed-Criticality Bus Interactions
CRSS supports integration with:
- CAN/LIN (through Core-C gateways)
- TCP (example)
- Serial/RS-485
- IPC or shared memory

Gateways must:
- enforce bounded payloads  
- sanitize data  
- apply plausibility checks  

---

## 8. Conclusion
This document defines the model-level guidance needed to scale CRSS to distributed, multi-component systems without compromising Strict-A determinism.

