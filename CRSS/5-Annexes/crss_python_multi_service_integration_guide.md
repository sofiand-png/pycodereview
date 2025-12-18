# CRSS Multi-Service Integration Guide

**Version:** v1.0.0
**Status:** Informative
**Maturity:** Stable
© 2025 Sofian Daghsen – All rights reserved
Distributed under CC BY-NC-ND 4.0 — see LICENSE-CRSS.

**Domain:** Multi-Component System Interaction  
**Audience:** Architects, Integration Engineers

---

## 1. Purpose
Provide a model-level description of how CRSS components interact safely in:
- distributed systems
- multi-node systems
- cloud/edge mixed deployments
- vehicle gateways
- industrial automation contexts

---

## 2. System Interaction Topology
A typical topology using an orchestrator:
- Sensors → Core-C Gateway → Strict-B Fusion → Strict-A Controller → Core-C Output Gateway → Actuators

Additional optional:
- Supervisor UI (Core-C)
- Data recorder (Core-C)
- Offline analytics (Core-C)

---

## 3. Interactions and Contracts

### 3.1 Core-C Gateway → Core-B Fusion
Payloads:
- bounded arrays
- validated numeric lists
- deterministic shape

### 3.2 Core-B Fusion → Strict-A Controller
Strict-A input must be:
- fixed-length numeric arrays
- pre-sanitized
- pre-bounded
- plausibility-filtered

### 3.3 Strict-A Controller → Core-C Output Gateway
Output consists only of:
- float command
- status enum
- reason code

No timestamps, no JSON, no strings.

---

## 4. Fault Containment

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
CRSS supports real multi-node architectures through strict interface contracts and critical-path isolation.

