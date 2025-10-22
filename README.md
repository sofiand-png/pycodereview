# pycodereview

Static checks for common Python code risks and hygiene issues.
Runs on a single file and outputs a concise CSV report you can diff, gate in CI, or share with a teammate.

[![Python versions](https://img.shields.io/pypi/pyversions/pycodereview)](https://pypi.org/project/pycodereview/)
[![PyPI downloads](https://img.shields.io/pypi/dm/pypistats.svg)](https://pypistats.org/packages/pycodereview)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Codecov](https://codecov.io/gh/hugovk/pycodereview/branch/main/graph/badge.svg)](https://codecov.io/gh/hugovk/pypistats)
[![GitHub stars](https://img.shields.io/github/stars/sofiand-png/pycodereview?style=flat)](https://github.com/sofiand-png/pycodereview/stargazers)
[![GitHub forks](https://img.shields.io/github/forks/sofiand-png/pycodereview?style=flat)](https://github.com/sofiand-png/pycodereview/network/members)
[![GitHub issues](https://img.shields.io/github/issues/sofiand-png/pycodereview)](https://github.com/sofiand-png/pycodereview/issues)



## Why pycodereview?

Most static analysis tools (like **pylint**, **flake8**, or **ruff**) focus on **style compliance, lint rules, and PEP8/typing**.  
**pycodereview** is different. It’s designed for **human code review augmentation**, not just linting.

It aims to:

- Group findings by impact rather than rule ID.
  You get concise categories (Correctness, Security, Robustness, etc.) with human-readable explanations instead of cryptic codes.

- Bridge readability and auditability.
  The CSV format and per-issue "potential impact" line make it easy to share results with non-developers (QA, auditors, project managers).

- Highlight "risky patterns," not just style issues.
  For example: mutable default arguments, missing joins on threads, unsafe deserialization, misuse of assert.

- Run with zero setup.
  No configs, plugins, or rule IDs needed; just point it to a file and go.

- Stay lightweight.
  Uses Python's built-in ast and tokenize, no heavy dependencies.

- Complement other tools.
  Meant to run alongside type checkers and formatters, catching logic and lifecycle issues they miss.

---

## What it checks

- **Error Handling**: catch-alls, empty `except`, exception re-raise quality.
- **Correctness**: mutable default args, misuse of `assert`, identity vs equality, undefined names, magic token numbers, ignored returns, return/annotation mismatches, premature exits.
- **Security**: `eval/exec`, unsafe `subprocess`, `os.system`, unsafe YAML/Pickle loads.
- **Concurrency**: thread/process lifecycle, import-time multiprocessing, shared mutable globals.
- **Resource Management**: `open()` without context manager, read/write mode mismatches, missing encodings.
- **Robustness**: brittle CSV parsing, unguarded dict/key access, potential type/len pitfalls.
- **Maintainability & Style**: wildcard imports, unused imports/variables, naming conventions, docstrings (optional), print statements, non-Pythonic loops, len comparisons, import order, magic literals.
- **Portability**: hardcoded platform paths.
- **Process**: TODO/FIXME markers.

Each finding has **category**, **priority**, **impacted lines**, **potential impact**, and **description**.

---

## Installation

```bash
pip install pycodereview
```

Optional virtualenv for local development:

```bash
python -m venv .venv
# Windows:
# .venv\Scripts\activate
# POSIX:
. .venv/bin/activate
pip install -U pip
pip install -e .
```

### One-off usage (no install)
```bash
python -m pycodereview.code_review path/to/target.py
```

---

## Quick start

Analyze a single file:

```bash
pycodereview path/to/file.py
```

Write CSV report:

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

Limit displayed impacted lines for very noisy issues (cap to 600 lines):

```bash
pycodereview path/to/file.py --max-lines 600
```

### Batch a directory (workaround)

Directory scanning is not implemented in v0.1.x.
You can batch files using your shell.

POSIX:

```bash
mkdir -p reports
find ./src -name "*.py" -print0 | while IFS= read -r -d '' f; do
  out="reports/$(basename "$f").csv"
  pycodereview "$f" --merge-issues --out "$out"
done
```

PowerShell:

```powershell
New-Item -ItemType Directory -Force -Path reports | Out-Null
Get-ChildItem -Recurse -Filter *.py .\src | ForEach-Object {
  $out = "reports\$($_.BaseName).csv"
  pycodereview $_.FullName --merge-issues --out $out
}
```

---

## CLI options

```
pycodereview FILE [options]

Options:
  --out OUT                    Output CSV path (semicolon-delimited). Default: review_report.csv
  --log LOG                    Optional path to write a short text log/summary (e.g., analysis.log).
  --min-priority {LOW,MEDIUM,HIGH}
                               Only report issues at or above this priority. Default: LOW
  --fail-on {LOW,MEDIUM,HIGH}  Exit with code 2 if any issue at/above this priority is found.
  --max-lines N                If an issue lists many impacted lines, cap the shown count to N (default: 1200)
  --merge-issues               Merge identical issues across multiple lines into a single row.
  --version                    Show version and exit
  -h, --help                   Show this help message and exit
```

---

## Output format (CSV)

Columns:

1. category of issue
2. priority of issue
3. impacted lines (single line, range a-b, or comma-separated list)
4. potential impact
5. description (<file>: <message>)

Example:

```
Correctness;MEDIUM;257,332,380,396,401,426;"Asserts can be stripped with -O; critical checks may disappear.";"testfile.py: Avoid assert for runtime validation; raise exceptions instead."
```

---

## Example CI

GitHub Actions:

```yaml
name: Static review
on: [push, pull_request]
jobs:
  review:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with: { python-version: '3.11' }
      - run: pip install pycodereview
      - run: pycodereview ./src/main.py --min-priority MEDIUM --merge-issues --out review_report.csv
```

---

## Links

- PyPI: https://pypi.org/project/pycodereview/
- Pepy downloads: https://pepy.tech/project/pycodereview
- PyPI Stats: https://pypistats.org/packages/pycodereview

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

MIT. See LICENSE.
