# CRSS ML / Pandas / Numpy Safety Annex

**Version:** v1.0.0
**Status:** Informative
**Maturity:** Stable
© 2025 Sofian Daghsen - All rights reserved
Distributed under CC BY-NC-ND 4.0 - see LICENSE-CRSS.

**Domain:** Data Processing, ML Pipelines
**Audience:** ML Engineers, Data Engineers, Architects

---

<a id="toc"></a>
## Table of Contents
- [CRSS ML / Pandas / Numpy Safety Annex](#crss-ml-pandas-numpy-safety-annex)
  - [Table of Contents](#table-of-contents)
  - [1. Purpose](#1-purpose)
  - [2. ML in Safety Context](#2-ml-in-safety-context)
    - [2.1 Strict-A: Fully Forbidden](#21-strict-a-fully-forbidden)
    - [2.2 Core-B: Allowed With Restrictions](#22-core-b-allowed-with-restrictions)
    - [2.3 Core-C: Fully Allowed](#23-core-c-fully-allowed)
  - [3. Pandas / Numpy](#3-pandas-numpy)
    - [Allowed:](#allowed)
    - [Forbidden in Strict-A:](#forbidden-in-strict-a)
    - [Allowed in Core-B:](#allowed-in-core-b)
  - [4. ML Safety Patterns](#4-ml-safety-patterns)
    - [4.1 ML-Assisted Monitoring Layer](#41-ml-assisted-monitoring-layer)
  - [5. Conclusion](#5-conclusion)

---

## 1. Purpose

> [⬆ Back to Table of Contents](#toc)

Provide guidance for using popular data libraries (NumPy, Pandas, ML frameworks) **safely** under CRSS.

---

## 2. ML in Safety Context

> [⬆ Back to Table of Contents](#toc)


### 2.1 Strict-A: Fully Forbidden
No ML inference allowed in Strict-A.

### 2.2 Core-B: Allowed With Restrictions
ML/inference may be used for:
- non-safety-critical advisory
- sensor quality estimation
- optional confidence scoring

But:
- must not influence Strict-A deterministic path directly
- ML results must be treated as **soft hints**, never commands

### 2.3 Core-C: Fully Allowed
Model training, analytics, and offline pipelines.

---

## 3. Pandas / Numpy

> [⬆ Back to Table of Contents](#toc)


### Allowed:
- preprocessing
- statistical checks
- sensor drift analysis
- batch fusion
- test data generation

### Forbidden in Strict-A:
All Pandas/Numpy operations due to:
- allocations
- unpredictable runtime
- hidden loops

### Allowed in Core-B:
Only with:
- shape validation
- bounded arrays
- deterministic operations
- no chained operations that reallocate

---

## 4. ML Safety Patterns

> [⬆ Back to Table of Contents](#toc)


### 4.1 ML-Assisted Monitoring Layer
ML can suggest:
- sensor fault likelihood
- system degradation
- abnormal patterns

Strict-A must not rely on ML outputs.

---

## 5. Conclusion

> [⬆ Back to Table of Contents](#toc)

ML can coexist safely with CRSS if confined to non-critical paths and treated as advisory information.

