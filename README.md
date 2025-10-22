# pycodereview <p align="right">
  <img src="assets/logo.svg" width="110" alt="pycodereview logo">
</p>

[![pycodereview](https://img.shields.io/pypi/v/pycodereview.svg?label=pycodereview&logo=python)](https://pypi.org/project/pycodereview/)
[![Python versions](https://img.shields.io/pypi/pyversions/pycodereview)](https://pypi.org/project/pycodereview/)
[![downloads](https://img.shields.io/pypi/dm/pycodereview.svg)](https://pycodereview.org/packages/pycodereview)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![CI](https://github.com/sofiand-png/pycodereview/actions/workflows/ci.yml/badge.svg)](https://github.com/sofiand-png/pycodereview/actions/workflows/ci.yml)
[![Codecov](https://codecov.io/gh/sofiand-png/pycodereview/branch/main/graph/badge.svg)](https://app.codecov.io/gh/sofiand-png/pycodereview)
[![Security scan](https://github.com/sofiand-png/pycodereview/actions/workflows/security-scan.yml/badge.svg)](https://github.com/sofiand-png/pycodereview/actions/workflows/security-scan.yml)

Static checks for common Python code risks and hygiene issues.
Runs on a single file and outputs concise reports in **CSV** or **JSON** format.

## Why pycodereview?

Most static analysis tools (like **pylint**, **flake8**, or **ruff**) focus on **style compliance** and **lint rules**.
**pycodereview** is different. It's built to support **human code review** with clear, impact-based findings.

It aims to:

- Group findings by **impact** (Correctness, Security, Robustness, etc.) instead of rule codes.
- Bridge readability and auditability.  
- Be lightweight and dependency-free (built on Python’s `ast`/`tokenize`).
- Highlight **risky patterns**, not just style issues (mutable defaults, unsafe deserialization, misuse of assert, etc.).
- Provide reports you can share in CSV or JSON for auditing or CI review.

---

## What it checks

- **Error Handling**: catch-alls, empty `except`, exception re-raise quality.  
- **Correctness**: mutable defaults, misuse of `assert`, identity vs equality, undefined names, return vs annotation mismatches.  
- **Security**: `eval/exec`, unsafe `subprocess`/`os.system`, unsafe YAML/Pickle.  
- **Resource Management**: missing context managers, mode/encoding mismatches.  
- **Maintainability & Style**: wildcard imports, shadowing builtins, naming conventions, missing docstrings (for public API), non-Pythonic loops, `len(...)` comparisons.  
- **Process**: TODO/FIXME markers.

---

## Installation

```bash
pip install pycodereview
```

For local development and testing:

```bash
pip install -r requirements-dev.txt
```

---

## Quick Start

Run analysis on a file:

```bash
pycodereview path/to/file.py
```

Write CSV report:

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
    "file": ".\tests\data\sample_cases.py",
    "category": "Correctness",
    "priority": "HIGH",
    "impacted_lines": "65",
    "potential_impact": "Shared mutable state across calls; surprising behavior.",
    "description": "sample_cases.py: Mutable default in function \"bad_defaults_a\"."
  },
  {
    "file": ".\tests\data\sample_cases.py",
    "category": "Correctness",
    "priority": "HIGH",
    "impacted_lines": "70",
    "potential_impact": "Shared mutable state across calls; surprising behavior.",
    "description": "sample_cases.py: Mutable default in function \"bad_defaults_b\"."
  }
]
```

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

## Example CLI options

```
pycodereview FILE [options]

Options:
  --out OUT            Output CSV path. Default: review_report.csv
  --json-output PATH   Write JSON-formatted report.
  --min-priority {LOW,MEDIUM,HIGH}
                       Only report issues at or above this priority.
  --merge-issues       Merge identical issues across multiple lines.
  --max-lines N        Cap the number of lines listed per issue (default: 1200)
  --version            Show version and exit
  -h, --help           Show help message and exit
```

---

## Example Local Testing

Run all unit tests with coverage:

```bash
pip install -r requirements-dev.txt
pytest --cov=src/pycodereview --cov-report=term --cov-report=html
```

---

## Limitations

- Static checks are not a replacement for full linters or type checkers (ruff, flake8, mypy).
- Some security rules are conservative; false positives are possible.
- Reports only; no auto-fixes.

---

## Contributing

PRs welcome. Please:
- add unit tests for new rules,
- keep messages concise and actionable,
- document new options in the README,
- run black and ruff before committing.

---

## License

MIT License. See LICENSE for details.