# CRSS Toolchain Hardening Guide

**Version:** v1.0.0
**Status:** Informative
**Maturity:** Stable
© 2025 Sofian Daghsen – All rights reserved
Distributed under CC BY-NC-ND 4.0 — see LICENSE-CRSS.

**Domain:** CI/CD, Build System, DevSecOps  
**Audience:** DevOps, Toolchain Maintainers, Safety Engineers

---

## 1. Purpose
Define a hardened toolchain strategy that ensures:
- reproducible builds
- controlled dependencies
- deterministic environments
- evidence collection
- verification traceability

---

## 2. Interpreter Hardening

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

### 4.1 MC/DC Reporting
- custom MC/DC collector
- required coverage thresholds stored in artifacts

### 4.2 Fault Injection Evidence
- simulator logs stored as artifacts
- tests covering frozen/stuck-drift modes

---

## 5. Evidence Aggregation

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
This annex provides a hardened, reproducible, certifiable toolchain template for CRSS projects.

