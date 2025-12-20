# CRSS Multi-Service Integration Guide

**Version:** v1.0.0
**Status:** Informative
**Maturity:** Stable
© 2025 Sofian Daghsen - All rights reserved
Distributed under CC BY-NC-ND 4.0 - see LICENSE-CRSS.

**Domain:** Multi-Component System Interaction  
**Audience:** Architects, Integration Engineers

---

<a id="toc"></a>
## Table of Contents
- [CRSS Multi-Service Integration Guide](#crss-multi-service-integration-guide)
  - [Table of Contents](#table-of-contents)
  - [1. Purpose](#1-purpose)
  - [2. System Interaction Topology](#2-system-interaction-topology)
  - [3. Interactions and Contracts](#3-interactions-and-contracts)
    - [3.1 Core-C Gateway - Core-B Fusion](#31-core-c-gateway-core-b-fusion)
    - [3.2 Core-B Fusion - Strict-A Controller](#32-core-b-fusion-strict-a-controller)
    - [3.3 Strict-A Controller - Core-C Output Gateway](#33-strict-a-controller-core-c-output-gateway)
  - [4. Fault Containment](#4-fault-containment)
    - [4.1 Isolation Rules](#41-isolation-rules)
    - [4.2 State Recovery](#42-state-recovery)
  - [5. Integration Requirements Checklist](#5-integration-requirements-checklist)
    - [Mandatory](#mandatory)
    - [Recommended](#recommended)
  - [6. Conclusion](#6-conclusion)

---

## 1. Purpose

> [⬆ Back to Table of Contents](#toc)

Provide a model-level description of how CRSS components interact safely in:
- distributed systems
- multi-node systems
- cloud/edge mixed deployments
- vehicle gateways
- industrial automation contexts

---

## 2. System Interaction Topology

> [⬆ Back to Table of Contents](#toc)

A typical topology using an orchestrator:
- Sensors → Core-C Gateway → Strict-B Fusion → Strict-A Controller → Core-C Output Gateway → Actuators

Additional optional:
- Supervisor UI (Core-C)
- Data recorder (Core-C)
- Offline analytics (Core-C)

---

## 3. Interactions and Contracts

> [⬆ Back to Table of Contents](#toc)


### 3.1 Core-C Gateway - Core-B Fusion
Payloads:
- bounded arrays
- validated numeric lists
- deterministic shape

### 3.2 Core-B Fusion - Strict-A Controller
Strict-A input must be:
- fixed-length numeric arrays
- pre-sanitized
- pre-bounded
- plausibility-filtered

### 3.3 Strict-A Controller - Core-C Output Gateway
Output consists only of:
- float command
- status enum
- reason code

No timestamps, no JSON, no strings.

---

## 4. Fault Containment

> [⬆ Back to Table of Contents](#toc)


### 4.1 Isolation Rules
A failure in:
- TCP  
- gateway  
- simulator  
- JSON parsing  

must NEVER propagate into Strict-A.

### 4.2 State Recovery
Strict-A always produces safe output via safe_default.

---

## 5. Integration Requirements Checklist

> [⬆ Back to Table of Contents](#toc)


### Mandatory
- fixed schemas
- bounded message sizes
- deterministic format
- loss of message does NOT break Strict-A

### Recommended
- heartbeats
- supervision channel
- state reflection

---

## 6. Conclusion

> [⬆ Back to Table of Contents](#toc)

CRSS supports real multi-node architectures through strict interface contracts and critical-path isolation.

