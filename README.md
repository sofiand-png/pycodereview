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
Runs on a single file and outputs a concise CSV report you can diff, gate in CI, or share with a teammate.

---

## Why pycodereview?

Most static analysis tools (like **pylint**, **flake8**, or **ruff**) focus on **style rules and PEP8/typing**.  
**pycodereview** is different: it’s designed for **human code review augmentation**, not just linting.

It aims to:

- Group findings by impact rather than rule ID.  
  You get concise categories (Correctness, Security, Robustness, etc.) with human-readable explanations.
- Bridge readability and auditability.  
  The CSV format and per-issue “potential impact” line make it easy to share with QA/auditors/PMs.
- Highlight **risky patterns**, not just style issues (mutable defaults, unsafe deserialization, misuse of assert, etc.).
- Run with zero setup (no configs, no rule IDs); just point it at a file.
- Stay lightweight (built on Python’s `ast`/`tokenize`).

---

## What it checks

- **Error Handling**: catch-alls, empty `except`, exception re-raise quality.  
- **Correctness**: mutable defaults, misuse of `assert`, identity vs equality, undefined names, return vs annotation mismatches.  
- **Security**: `eval/exec`, unsafe `subprocess`/`os.system`, unsafe YAML/Pickle.  
- **Resource Management**: missing context managers, mode/encoding mismatches.  
- **Maintainability & Style**: wildcard imports, shadowing builtins, naming conventions, missing docstrings (for public API), non-Pythonic loops, `len(...)` comparisons.  
- **Process**: TODO/FIXME markers.

Each finding has **category**, **priority**, **impacted lines**, **potential impact**, and **description**.

---

## Installation

Users of the tool:
```bash
pip install pycodereview
```

> No extra dependencies are required for normal use.

---

## Quick start

Analyze a file:
```bash
pycodereview path/to/file.py
```

Write a CSV report:
```bash
pycodereview path/to/file.py --out review_report.csv
```

Show only MEDIUM and higher:
```bash
pycodereview path/to/file.py --min-priority MEDIUM
```

Merge identical issues across multiple lines:
```bash
pycodereview path/to/file.py --merge-issues
```

Limit displayed impacted lines (cap to 600 lines):
```bash
pycodereview path/to/file.py --max-lines 600
```

> One-off usage without install is also possible:
> ```bash
> python -m pycodereview.code_review path/to/target.py
> ```

---

## Local development

**These steps are only needed if you want to run unit tests or contribute.** Regular users can ignore this section.

Clone and set up a virtual environment:
```bash
python -m venv .venv
# Windows:
# .venv\Scripts\activate
# POSIX:
. .venv/bin/activate

python -m pip install -U pip
pip install -r requirements-dev.txt   # pytest + pytest-cov only
# optional, to import from the local src/ tree:
pip install -e .
```

Run tests:
```bash
pytest -q
pytest --cov=pycodereview --cov-report=term --cov-report=html
# open htmlcov/index.html
```

---

## CLI options

```
pycodereview FILE [options]

Options:
  --out OUT                    Output CSV path (semicolon-delimited). Default: review_report.csv
  --log LOG                    Optional path to write a short text log (e.g., analysis.log).
  --min-priority {LOW,MEDIUM,HIGH}
                               Only report issues at or above this priority. Default: LOW
  --fail-on {LOW,MEDIUM,HIGH}  Exit with code 2 if any issue at/above this priority is found.
  --max-lines N                Cap the displayed impacted lines for very noisy issues (default: 1200)
  --merge-issues               Merge identical issues across multiple lines into a single row.
  --version                    Show version and exit
  -h, --help                   Show help and exit
```

---

## Links

- PyPI: https://pypi.org/project/pycodereview/
- Pepy downloads: https://pepy.tech/project/pycodereview
- PyPI project stats: https://pypistats.org/packages/pycodereview
- Codecov: https://app.codecov.io/

---

## License

MIT. See LICENSE.
