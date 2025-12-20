# CRSS Distributed System Design Guide

**Version:** v1.0.0
**Status:** Informative
**Maturity:** Stable
© 2025 Sofian Daghsen - All rights reserved
Distributed under CC BY-NC-ND 4.0 - see LICENSE-CRSS.

**Domain:** Multi-Component CRSS Architectures
**Audience:** System Architects, Integrators, Safety Engineers

---

<a id="toc"></a>
## Table of Contents
- [CRSS Distributed System Design Guide](#crss-distributed-system-design-guide)
  - [Table of Contents](#table-of-contents)
  - [1. Purpose](#1-purpose)
  - [2. Distributed System Layers](#2-distributed-system-layers)
  - [3. Allowed Interactions](#3-allowed-interactions)
    - [3.1 Strict-A Allowed Inputs](#31-strict-a-allowed-inputs)
    - [3.2 Strict-A Outputs](#32-strict-a-outputs)
  - [4. Message-Passing Contracts](#4-message-passing-contracts)
    - [4.1 Core-C → Strict-A Contract](#41-core-c-strict-a-contract)
    - [4.2 Strict-A → Core-C Contract](#42-strict-a-core-c-contract)
  - [5. Fault Propagation Rules](#5-fault-propagation-rules)
    - [5.1 Critical Path Isolation](#51-critical-path-isolation)
    - [5.2 Failsafe Guarantees](#52-failsafe-guarantees)
  - [6. Scaling Up to Multiple Controllers](#6-scaling-up-to-multiple-controllers)
  - [7. Mixed-Criticality Bus Interactions](#7-mixed-criticality-bus-interactions)
  - [8. Conclusion](#8-conclusion)

---

## 1. Purpose

> [⬆ Back to Table of Contents](#toc)

This document explains **how CRSS-compliant components can coexist in a distributed architecture** while maintaining full compliance with strict determinism and mixed-criticality rules.

This guide is *model-level only* (no implementation).

---

## 2. Distributed System Layers

> [⬆ Back to Table of Contents](#toc)


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

> [⬆ Back to Table of Contents](#toc)


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

> [⬆ Back to Table of Contents](#toc)


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

> [⬆ Back to Table of Contents](#toc)


### 5.1 Critical Path Isolation
Faults from Core-C must not enter Strict-A.

### 5.2 Failsafe Guarantees
Strict-A fallback is **purely local**:
- ignores external timing
- ignores JSON issues
- uses deterministic fallback

---

## 6. Scaling Up to Multiple Controllers

> [⬆ Back to Table of Contents](#toc)

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

> [⬆ Back to Table of Contents](#toc)

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

> [⬆ Back to Table of Contents](#toc)

This document defines the model-level guidance needed to scale CRSS to distributed, multi-component systems without compromising Strict-A determinism.

