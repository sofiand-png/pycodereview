# CRSS Integration Architecture Annex

**Version:** v1.0.0
**Status:** Informative (Reference Example)
**Maturity:** Stable
© 2025 Sofian Daghsen – All rights reserved
Distributed under CC BY-NC-ND 4.0 — see LICENSE-CRSS.

---

## 1. Purpose
This annex defines how CRSS-compliant Python applications integrate safely with:
- Embedded control hardware
- RTOS environments
- Microcontrollers
- Sensor/actuator buses
- Automotive and medical gateways
- Cloud backends

It ensures that Python components can serve as deterministic, bounded, safety-contained modules inside larger systems.

## 2. Integration Tiers
CRSS defines three integration tiers:

| Tier | Description |
|------|-------------|
| **T1 – Direct Embedded** | Python runs on the same physical controller/ECU |
| **T2 – Gateway-Mediated** | Python app communicates via IPC / TCP / CAN gateway |
| **T3 – Cloud-Supervisory** | Python provides monitoring, analytics, or configuration |

The reference example corresponds to **Tier 2**.

## 3. Integration Boundaries (CRSS-Critical)
CRSS mandates strict separation:

### Strict-A components:
- No direct communication with hardware or OS
- Only operate on validated, deterministic inputs
- No I/O, no threads, no GC, no syscalls
- Pure computational kernel

### Core-B components:
- Minimal deterministic preprocessing
- No nondeterministic effects

### Core-C components:
- JSON/TCP
- File I/O
- Logging
- Hardware wrapping
- External libraries
- Threads allowed

## 4. Hardware Integration Patterns

### 4.1 Gateway Shield (Recommended)
```
Sensors ─► MCU/RTOS ─► Gateway (C/C++/Rust) ─► Python CRSS App
Actuator ◄─ MCU/RTOS ◄─ Gateway ◄─────────── ActuatorRequest
```
Gateway responsibilities:
- Timing
- Deterministic scheduling
- Bus validation
- Rate-limiting
- Encoding data for Python

### 4.2 HAL Wrapper
A native library (C/Rust) exposes a safe ABI.
Python calls via `ctypes` / `cffi` (**Core-C only**).
Strict-A may **not** call HAL.

### 4.3 RTOS Push Model
Native shim sends:
- CAN frames
- GPIO interrupts
- PWM feedback

As JSON to Python.

## 5. Allowed/Forbidden Operations
| Operation | Strict-A | Core-B | Core-C |
|-----------|----------|--------|--------|
| TCP I/O | ❌ | ❌ | ✔ |
| File I/O | ❌ | ❌ | ✔ |
| Logging | ❌ | ❌ | ✔ |
| Dynamic memory | ❌ | Partial | ✔ |
| Floating-point math | ✔ | ✔ | ✔ |
| External libraries | ❌ | Conditional | ✔ |
| Threads | ❌ | ❌ | ✔ |
| GC | ❌ | ❌ | ✔ |

## 6. Safety Timing Model
A CRSS module must publish:
- Execution-time budget
- WCET of Strict-A section
- I/O latency expectations
- Jitter tolerances
- Recovery behavior

Gateways enforce real-time schedule.

## 7. Watchdog Integration
For real systems:
- Python emits heartbeat
- Gateway monitors heartbeat
- Timeout → safe-default actuator state

## 8. Deployment Considerations
Python is **never** flashed onto MCU memory.
Python runs in:
- Containers
- Isolated OS processes
- Supervised schedulers

All dependencies must be pinned.

## 9. Example: Sensor Voting System
Applies directly to reference design:
- Sensors via TCP gateway
- Strict-A evaluates deterministically
- Actuator output bounded
- Gateway logs & validates

Functions as a complete closed-loop test bench.
