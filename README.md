# pycodereview <p align="right">
  <img src="https://raw.githubusercontent.com/sofiand-png/pycodereview/main/assets/logo.png" width="110" alt="pycodereview logo">
</p>

[![pycodereview](https://img.shields.io/pypi/v/pycodereview.svg?label=pycodereview&logo=python)](https://pypi.org/project/pycodereview/)
[![Python versions](https://img.shields.io/pypi/pyversions/pycodereview)](https://pypi.org/project/pycodereview/)
[![downloads](https://img.shields.io/pypi/dm/pycodereview.svg)](https://pycodereview.org/packages/pycodereview)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![CI](https://github.com/sofiand-png/pycodereview/actions/workflows/ci.yml/badge.svg)](https://github.com/sofiand-png/pycodereview/actions/workflows/ci.yml)
[![Codecov](https://codecov.io/gh/sofiand-png/pycodereview/branch/main/graph/badge.svg)](https://app.codecov.io/gh/sofiand-png/pycodereview)
[![Security scan](https://github.com/sofiand-png/pycodereview/actions/workflows/security-scan.yml/badge.svg)](https://github.com/sofiand-png/pycodereview/actions/workflows/security-scan.yml)

Static checks for common Python code risks and hygiene issues.  
Runs on a single file and outputs concise, review-ready reports in **CSV** or **JSON**.

---

## Why pycodereview?

Most static analysis tools (like **pylint**, **flake8**, or **ruff**) are great at **style compliance** and large rule catalogs.

**pycodereview** is different: it’s built to support **human code review** with clear, impact-based findings.

It aims to:

- Group findings by **impact** (Correctness, Security, Robustness, etc.) instead of cryptic rule codes.
- Bridge readability and auditability (messages explain *why it matters*).
- Stay lightweight and dependency-free (built on Python’s `ast` / `tokenize`).
- Highlight **risky patterns**, not just style issues (mutable defaults, unsafe deserialization, misuse of `assert`, etc.).
- Produce reports you can share in CSV/JSON for CI gates, audits, and review discussions.

---

## Quick Start

Install:

```bash
pip install pycodereview
```

Run analysis on a file:

```bash
pycodereview path/to/file.py
```

Write a CSV report:

```bash
pycodereview path/to/file.py --out review_report.csv
```

Generate JSON output:

```bash
pycodereview path/to/file.py --json-output review.json
```

Example **JSON output**:

```json
[
  {
    "file": ".\\tests\\data\\sample_cases.py",
    "category": "Correctness",
    "priority": "HIGH",
    "impacted_lines": "65",
    "potential_impact": "Shared mutable state across calls; surprising behavior.",
    "description": "sample_cases.py: Mutable default in function \"bad_defaults_a\"."
  },
  {
    "file": ".\\tests\\data\\sample_cases.py",
    "category": "Correctness",
    "priority": "HIGH",
    "impacted_lines": "70",
    "potential_impact": "Shared mutable state across calls; surprising behavior.",
    "description": "sample_cases.py: Mutable default in function \"bad_defaults_b\"."
  }
]
```

---

## What it checks

pycodereview focuses on **review-relevant risks** that commonly slip into production.

### Error Handling
- Catch-alls and empty `except`
- Improper exception re-raise losing traceback/context

### Correctness
- Mutable default args
- Misuse of `assert` for runtime validation
- Identity vs equality pitfalls
- Undefined variables / shadowing hazards
- Return annotation mismatches and suspicious flows

### Security
- `eval` / `exec`
- Unsafe `subprocess` or `os.system`
- Insecure YAML / Pickle loads
- Weak hashes (md5, sha1)
- Hardcoded secrets/tokens (basic signals)
- Unsafe HTTP patterns (`verify=False`, etc.)

### Concurrency (lightweight signals)
- Import-time multiprocessing hazards
- Misuse patterns around tasks/lifecycle
- Blocking calls inside async functions (e.g. `time.sleep`)

### Resource Management
- Missing context managers (`with open(...)`)
- File mode mismatches and missing encoding
- Unsafe tempfile patterns (e.g. `mktemp()`)

### Robustness
- Unguarded dict/key access patterns
- Common len/type footguns
- Fragile reliance on ordering assumptions

### Maintainability & Hygiene
- Wildcard imports
- Unused imports/variables
- Missing docstrings for public API (where applicable)
- Debug prints and noisy markers
- Non-Pythonic loops / suspicious constructs
- Magic literals (heuristic)

### Process
- TODO/FIXME markers (review surfacing)

---

## Output Formats

### CSV
Columns:
1. Category
2. Priority
3. Impacted lines
4. Potential impact
5. Description

### JSON
Each finding is a JSON object with keys:
- `file`
- `category`
- `priority`
- `impacted_lines`
- `potential_impact`
- `description`

---

## CLI

```
pycodereview FILE [options]

Options:
  --out OUT              Output CSV path. Default: review_report.csv
  --json-output PATH     Write JSON-formatted report.
  --min-priority {LOW,MEDIUM,HIGH}
                         Only report issues at or above this priority.
  --merge-issues         Merge identical issues across multiple lines.
  --max-lines N          Cap the number of lines listed per issue (default: 1200)
  --version              Show version and exit
  -h, --help             Show help message and exit
```

---

## Relationship to CRSS-Python

**pycodereview** is the reference static-analysis engine for the **CRSS-Python Standard** — a safety-oriented subset of Python inspired by MISRA-style discipline and certification expectations.

**CRSS-Python (Certifiable Reliability Safety Standard - Python)** is an original safety and reliability standard for Python,
authored by **Sofian Daghsen**. It defines two profiles:
- **CRSS-Core** – a pragmatic profile for general Python code.
- **CRSS-Strict** – a constrained, analyzable subset for critical units

**CRSS-Python** makes Python suitable for:
- Automotive safety systems
- Industrial control
- Medical devices
- Critical monitoring systems
- High-assurance automation
- Mission-critical supervisory logic


### What you can do today (no CRSS required)
You can use pycodereview as a lightweight review tool:

```bash
pycodereview file.py
```

No config required. It produces impact-based findings you can use in reviews and CI.

### What CRSS adds (standard + structured compliance)
CRSS introduces:
- Stable **rule IDs** (e.g., `CRSS-3.1.5`, `CRSS-6.2.1`, `CRSS-9.1.4`)
- Two profiles:
  - **Core** → pragmatic baseline for most Python code
  - **Strict** → analyzable subset for `@critical` / high-integrity logic
- Deviation handling, compliance reporting, and evidence structure
- Import / inheritance policies and certification-facing artifacts

### Where the CRSS documents live in this repo
(Repository paths)

- `CRSS/1-Specifications/Profiles/crss_python_core_spec.md`
- `CRSS/1-Specifications/Profiles/crss_python_strict_spec.md`
- `CRSS/1-Specifications/Master/crss_python_standard_safety_master.md`
- `CRSS/0-Overview/crss_python_overview_landing.md`

CRSS and pycodereview are versioned separately so projects can adopt CRSS progressively.

---

## Roadmap: toward full CRSS-aware enforcement

Planned additions (without breaking the current default experience):

1. **Profile-aware analysis**
   ```
   pycodereview myfile.py --profile core
   pycodereview myfile.py --profile strict
   ```
   - `default` remains today’s lightweight behavior.

2. **Rule-ID mapping**
   - Findings carry CRSS IDs where applicable.

3. **Project configuration (`crss.toml`)**
   - Declared profiles, critical zones, Python version range, deviation policy, requirements mapping.

4. **Safety-style reports**
   - Guideline compliance summaries, deviation logs, requirement traceability outputs.

5. **Advanced verification (planned / exploratory)**
   - MC/DC reporting for critical logic (where required)
   - Path exploration / bounded analysis experiments

---

## Local development

```bash
pip install -r requirements-dev.txt
pytest --cov=src/pycodereview --cov-report=term --cov-report=html
```

---

## Limitations

- Not a replacement for full linters/type-checkers (ruff, flake8, mypy).
- Some security checks are conservative; false positives are possible.
- Reports only; no auto-fixes.

---

## Contributing

PRs welcome. Please:
- add unit tests for new rules,
- keep messages concise and actionable,
- document new options in the README,
- run formatting/linting before committing.

---

## Licensing

### pycodereview software
The **pycodereview** software (source code, binaries, and package artifacts) is licensed under the **MIT License** (see `LICENSE`).

### CRSS-Python standard text (specifications)
The CRSS-Python specification documents (Core, Strict, and all specifications) are licensed under the
**Creative Commons Attribution–NonCommercial–NoDerivatives 4.0 International License (CC BY-NC-ND 4.0)**.

You are free to:
- Share — copy and redistribute the material in any medium or format

Under the following terms:
- Attribution — You must give appropriate credit.
- NonCommercial — You may not use the material for commercial purposes.
- NoDerivatives — You may not distribute modified versions.

This license applies **only** to the standard text located under:
- CRSS/

(Repository note: in this repository layout, CRSS documents live under `CRSS/` and are distributed with the same stated terms in their headers.)

