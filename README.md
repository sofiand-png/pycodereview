# pycodereview

Static checks for common Python code risks and hygiene issues.  
Runs on a single file or an entire tree and outputs a concise CSV report you can diff, gate in CI, or hand to a teammate.

## Why pycodereview?

Most static analysis tools (like **pylint**, **flake8**, or **ruff**) focus on **style compliance, lint rules, and PEP8/typing**.  
**pycodereview** is different — it’s designed for **human code review augmentation**, not just linting.

It aims to:

- **Group findings by impact** rather than rule ID.  
  You get concise categories (Correctness, Security, Robustness, etc.) with human-readable explanations instead of cryptic codes.

- **Bridge readability and auditability.**  
  The CSV format and per-issue “potential impact” line make it easy to share results with non-developers (QA, auditors, project managers).

- **Highlight “risky patterns,” not just style issues.**  
  e.g., mutable default arguments, missing joins on threads, unsafe deserialization, misuse of `assert` — issues ordinary linters often miss.

- **Run with zero setup.**  
  No configs, plugins, or rule IDs needed — just point it to a file and go.

- **Stay lightweight.**  
  Uses Python’s built-in `ast` and `tokenize` — no heavy deps.

- **Complement other tools.**  
  Meant to **run alongside** type checkers and formatters — catching logic and lifecycle issues they miss.

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

### From source (recommended while iterating)
```bash
git clone git@github.com:<you>/pycodereview.git
cd pycodereview

# optional virtualenv
python -m venv .venv
# Windows:
# .venv\\Scripts\\activate
# POSIX:
. .venv/bin/activate

pip install -U pip setuptools wheel
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
pycodereview ./src/test_cases.py
```

Analyze a whole project:
```bash
pycodereview ./src
```

Write CSV report:
```bash
pycodereview ./src > review_report.csv
```

Show only **MEDIUM** and higher:
```bash
pycodereview ./src --min-priority MEDIUM
```

Merge identical issues across multiple lines:
```bash
pycodereview ./src --merge-issues
```

Limit checks for large functions (max 600 lines):
```bash
pycodereview ./src --max-lines 600
```

---

## CLI options

```text
pycodereview [PATH ...] [options]

Options:
  --min-priority {LOW,MEDIUM,HIGH}   Minimum priority to include (default: LOW)
  --max-lines N                      Skip checks in functions longer than N lines (default: 1200)
  --merge-issues                     Merge same issues across multiple lines into a single report row
  --format {csv,table}               Output format (default: csv)
  --version                          Show version and exit
  -h, --help                         Show this help message and exit
```

Multiple files or directories are supported in one run.

---

## Output format (CSV)

Columns:

1. category of issue  
2. priority of issue  
3. impacted lines (single line, range `a-b`, or comma-separated list)  
4. potential impact  
5. description (`<file>: <message>`)

Example:
```text
Correctness;MEDIUM;257,332,380,396,401,426;"Asserts can be stripped with -O; critical checks may disappear.";"testfile.py: Avoid assert for runtime validation; raise exceptions instead."
```

---

## Example integrations

### Pre-commit
```yaml
# .pre-commit-config.yaml
- repo: https://github.com/<you>/pycodereview
  rev: v0.1.1
  hooks:
    - id: pycodereview
      args: [--min-priority, MEDIUM, --merge-issues]
```

### GitHub Actions
```yaml
# .github/workflows/review.yml
name: Static review
on: [push, pull_request]
jobs:
  review:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with: { python-version: '3.11' }
      - run: pip install .
      - run: pycodereview ./src --min-priority MEDIUM --merge-issues > review_report.csv
      - run: grep -q "HIGH" review_report.csv && echo "High issues found" && exit 1 || echo "OK"
```

---

## Limitations

- Static checks can’t replace full linters/type checkers (`ruff`, `flake8`, `mypy`, etc.).
- Some security rules err on the side of caution (false positives possible).
- This tool only reports; no auto-fixes are applied.

---

## Contributing

PRs welcome! Please:
- add unit tests for new rules,
- keep messages concise and actionable,
- document new options in the README,
- run `black` and `ruff` before committing.

---

## License

MIT — see `LICENSE`.
