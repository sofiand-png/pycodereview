# CRSS Toolchain Baseline & Qualification Notes

**Version:** v1.0.0
**Status:** Informative
**Maturity:** Stable
© 2025 Sofian Daghsen – All rights reserved
Distributed under CC BY-NC-ND 4.0 — see LICENSE-CRSS.

---

## 1. Purpose
- Explain why toolchain stability matters for safety

## 2. Python Runtime Baseline
- Supported ranges
- Micro-version policy
- Reproducibility constraints

## 3. Test Tooling Baseline

### 3.1 pytest (pinned version)

### 3.2 coverage (pinned version)

### 3.3 MC/DC tooling

### 3.4 Test runners (Linux + Windows)

## 4. Static Analysis Baseline

### 4.1 Ruff / Mypy / Pyright

### 4.2 Strictness levels

### 4.3 Qualification considerations

## 5. Build & Packaging Tools

### 5.1 setuptools / wheel versions

### 5.2 Constraints on upgrades

## 6. Logging & Diagnostics Tools
- Approved libraries
- Security considerations

## 7. Tool Qualification Guidance

### 7.1 ISO 26262 TCL guidance

### 7.2 DO-330 (if applicable)

### 7.3 Evidence the toolchain already provides

### 7.4 Evidence integrators must provide

## 8. Deviations & Exception Handling

## 9. Toolchain Update Process
