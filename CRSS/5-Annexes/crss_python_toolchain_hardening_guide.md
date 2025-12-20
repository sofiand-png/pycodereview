# CRSS Toolchain Hardening Guide

**Version:** v1.0.0
**Status:** Informative
**Maturity:** Stable
© 2025 Sofian Daghsen - All rights reserved
Distributed under CC BY-NC-ND 4.0 - see LICENSE-CRSS.

**Domain:** CI/CD, Build System, DevSecOps  
**Audience:** DevOps, Toolchain Maintainers, Safety Engineers

---

<a id="toc"></a>
## Table of Contents
- [CRSS Toolchain Hardening Guide](#crss-toolchain-hardening-guide)
  - [Table of Contents](#table-of-contents)
  - [1. Purpose](#1-purpose)
  - [2. Interpreter Hardening](#2-interpreter-hardening)
    - [2.1 Pin Python Version](#21-pin-python-version)
    - [2.2 Disable Sources of Nondeterminism](#22-disable-sources-of-nondeterminism)
  - [3. Build Hardening](#3-build-hardening)
    - [3.1 Reproducible Installations](#31-reproducible-installations)
    - [3.2 Dependency Whitelisting](#32-dependency-whitelisting)
  - [4. Testing Pipeline Improvements](#4-testing-pipeline-improvements)
    - [4.1 MC/DC Reporting](#41-mcdc-reporting)
    - [4.2 Fault Injection Evidence](#42-fault-injection-evidence)
  - [5. Evidence Aggregation](#5-evidence-aggregation)
    - [Mandatory](#mandatory)
  - [6. Conclusion](#6-conclusion)

---

## 1. Purpose

> [⬆ Back to Table of Contents](#toc)

Define a hardened toolchain strategy that ensures:
- reproducible builds
- controlled dependencies
- deterministic environments
- evidence collection
- verification traceability

---

## 2. Interpreter Hardening

> [⬆ Back to Table of Contents](#toc)


### 2.1 Pin Python Version
Pinned:
- interpreter version
- patch version
- hash seed

### 2.2 Disable Sources of Nondeterminism
- environment-dependent randomness
- varying system locale
- external entropy sources

---

## 3. Build Hardening

> [⬆ Back to Table of Contents](#toc)


### 3.1 Reproducible Installations
Use:
- `pip install --no-deps --require-hashes`
- frozen requirements (`python_version == "3.11"`)

### 3.2 Dependency Whitelisting
Only allow:
- cryptographically pinned versions
- deterministic packages
- safety-validated libraries

---

## 4. Testing Pipeline Improvements

> [⬆ Back to Table of Contents](#toc)


### 4.1 MC/DC Reporting
- custom MC/DC collector
- required coverage thresholds stored in artifacts

### 4.2 Fault Injection Evidence
- simulator logs stored as artifacts
- tests covering frozen/stuck-drift modes

---

## 5. Evidence Aggregation

> [⬆ Back to Table of Contents](#toc)


### Mandatory
- unit test coverage
- MC/DC
- integration test logs
- SCEM/MAR/CRC
- requirement/code traceability
- code review results
- configuration baseline

---

## 6. Conclusion

> [⬆ Back to Table of Contents](#toc)

This annex provides a hardened, reproducible, certifiable toolchain template for CRSS projects.

