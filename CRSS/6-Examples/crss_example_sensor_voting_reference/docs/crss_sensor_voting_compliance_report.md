# CRSS Compliance Report — Sensor Voting Reference Example

- **Project**: CRSS Python Sensor Voting Reference Example
- **Version**: 1.0.0
- **Language**: Python 3.11.x
- **CRSS Profiles Used**:
  - Strict-A: safety controller (voting + envelope)
  - Strict-B: config model, sensor interfaces
  - Core-B: orchestrators (offline step, TCP client)
  - Core-C: simulation, TCP server, logging, JSON I/O

## 1. Scope

This report covers:

- `crss_example_sensor_voting.safety_logic.*`
- `crss_example_sensor_voting.config.*`
- `crss_example_sensor_voting.actuator.*`
- `crss_example_sensor_voting.crss_phase.markers`
- `crss_example_sensor_voting.io.json_protocol`
- `crss_example_sensor_voting.app.main_loop` (offline)
- Unit, MC/DC-style, and integration tests in `tests/`

Non-critical I/O helpers (TCP server/client, simulation, logging) are excluded from
Strict-A compliance and coverage metrics; they are treated as **Core-C test harness**.

## 2. Rule Mapping Summary


### 2.1 Strict-A Deterministic Control Logic

| Rule ID      | Title (short)                                      | Module(s)                                           | Compliance |
|-------------|------------------------------------------------------|-----------------------------------------------------|-----------|
| CRSS-5.4.x  | Deterministic triple-sensor voting                  | `safety_logic.voting.compute_voted_value`          | **YES**   |
| CRSS-5.4.y  | Defined behaviour for missing / invalid readings    | `safety_logic.voting.compute_voted_value`          | **YES**   |
| CRSS-5.5.x  | Monotonic safety envelope (clamp + rate limit)      | `safety_logic.envelope.apply_safety_envelope`      | **YES**   |
| CRSS-5.5.y  | Bounded state and no unvalidated feedback           | `safety_logic.controller.SafetyController._previous_value` | **YES** |
| CRSS-3.1.1  | No runtime code generation                          | Entire Strict-A set                                 | **YES**   |
| CRSS-3.2.x  | No unbounded loops in Strict-A logic                | Entire Strict-A set                                 | **YES**   |

**Notes:**

- `compute_voted_value` uses a fixed algorithm:
  - length check (`len(values) != 3` -> fail-safe default)
  - deterministic pairwise plausibility
  - deterministic fallback (`SAFE_DEFAULT`) when no valid pair.
- No randomness, no I/O, no mutable global state in Strict-A modules.

### 2.2 Phase-Aware Boundaries & Data Flow

| Rule ID      | Title (short)                               | Module(s)                                      | Compliance |
|-------------|-----------------------------------------------|------------------------------------------------|-----------|
| CRSS-7.1.x  | Critical / non-critical boundary via markers | `crss_phase.markers`, `safety_logic.*`, `app.*`| **YES**   |
| CRSS-7.2.x  | Only pure data crosses the critical boundary | TCP JSON client ↔ `SafetyController.step`      | **YES**   |
| CRSS-7.3.x  | No exceptions/I/O inside Strict-A            | `safety_logic.*`, `actuator.interface`         | **YES**   |

**Notes:**

- `critical_phase` and `non_critical_phase` decorators are semantics-preserving and used as markers.
- Strict-A classes accept/return pure Python primitives / dataclasses (`ActuatorCommand`).
- All socket and JSON handling is done in non-critical `app.tcp_controller_client` / `app.tcp_sensor_server`.

### 2.3 Configuration & Safe Defaults

| Rule ID      | Title (short)                     | Module(s)                   | Compliance |
|-------------|------------------------------------|-----------------------------|-----------|
| CRSS-4.x.x  | Explicit SAFE_DEFAULT             | `config.model.SAFE_DEFAULT` | **YES**   |
| CRSS-4.x.y  | Config is static and typed        | `config.model.SafetyConfig` | **YES**   |
| CRSS-4.x.z  | Safe initial output / previous    | `SafetyConfig.initial_output`, `SafetyController` | **YES** |

**Notes:**

- `SAFE_DEFAULT` = `0.0` used as fail-safe.
- `SafetyConfig` is a frozen dataclass (immutable at runtime).

### 2.4 JSON I/O & Validation (Non-critical)

| Rule ID      | Title (short)                             | Module(s)                             | Compliance |
|-------------|--------------------------------------------|---------------------------------------|-----------|
| CRSS-6.x.x  | JSON protocol is explicit and validated    | `io.json_protocol`, `schemas/*.json` | **YES**   |
| CRSS-6.x.y  | Inconsistent sensor metadata is surfaced   | `io.json_protocol.validate_sensor_frame` | **YES** |

**Notes:**

- `SensorFrame` and `ActuatorRequest` have JSON Schema files in `schemas/`.
- `validate_sensor_frame` logs warnings on:
  - value out-of-range but status `OK`
  - status `ERROR` but value inside range
  - source status inconsistent with per-sensor statuses.

### 2.5 Deviations

```markdown
## 3. Deviations

- None identified for Strict-A modules in this example.
- Non-critical TCP server/client are treated as test harness only; they are
  outside the scope of the certified safety kernel and documented as such.