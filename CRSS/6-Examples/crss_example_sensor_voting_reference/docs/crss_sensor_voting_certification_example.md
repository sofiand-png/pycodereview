# CRSS-Python Certification Example - Sensor Voting Reference

**Version:** v1.0.0
**Status:** Informative (Reference Example)
**Maturity:** Stable
© 2025 Sofian Daghsen - All rights reserved
Distributed under CC BY-NC-ND 4.0 - see LICENSE-CRSS.

---

> **Important:** This document is an example of the evidence structure for
> a CRSS-compliant component. It is not an official certificate from
> any authority.

<a id="toc"></a>
## Table of Contents

- [1. Component Identification](#1-component-identification)
- [2. Applicable Standard](#2-applicable-standard)
- [3. Evidence](#3-evidence)
- [4. Summary Assessment (Example)](#4-summary-assessment-example)


## 1. Component Identification

> [⬆ Back to Table of Contents](#toc)


- **Name**: CRSS Python Sensor Voting Reference Example
- **Version**: 1.0.0
- **Language**: Python 3.11.x
- **Function**: Cooling temperature supervision (3-channel sensor voting + safety envelope)
- **Domain**: Safety-critical software example (architecture compatible with automotive/avionics-style safety thinking)

## 2. Applicable Standard

> [⬆ Back to Table of Contents](#toc)


- **Standard**: CRSS-Python (Core + Strict profiles)
- **Profiles used**:
  - Strict-A: safety kernel (controller, voting, envelope, actuator interface)
  - Strict-B: configuration model, sensor interfaces
  - Core-B/C: orchestration, simulation, I/O, logging

## 3. Evidence

> [⬆ Back to Table of Contents](#toc)


The following artefacts are available:

- **Specifications & design**:
  - Sensor voting use case specification (cooling temperature)
  - Safety baseline: `docs/crss_sensor_voting_safety_baseline.md`
- **Rule compliance**:
  - CRSS compliance report: `docs/crss_sensor_voting_compliance_report.md`
- **Testing & coverage**:
  - Test suite: unit, MC/DC-style, and integration tests in `tests/`
  - Coverage report: `reports/coverage_report.md` (statement and branch coverage)
- **Fault injection**:
  - Fault injection report: `reports/fault_injection_report.md`
  - Fault model implemented in simulation + status inconsistencies.
- **SCEM artefacts**:
  - Modes and allocation: `scem/mar.yaml`
  - Test & evidence plan: `scem/tep.yaml`
  - Build & environment metadata: `scem/cbm.json` (if present)
  - Rule compliance summary: this document + compliance report.

## 4. Summary Assessment (Example)

> [⬆ Back to Table of Contents](#toc)


Based on the artefacts listed above:

- Strict-A safety logic (`safety_logic.*`, `actuator.interface`) adheres to:
  - deterministic, bounded control flow,
  - explicit safe defaults,
  - clear separation from non-critical I/O,
  - high coverage unit and MC/DC-style testing.
- Non-critical harness modules are clearly identified and excluded from
  the certified safety kernel scope.

This structure is suitable as a template for an actual certification dossier
for real-world projects that extend this example.