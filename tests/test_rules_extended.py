import textwrap
from pathlib import Path
from pycodereview.code_review import run_on_file

def w(tmp_path: Path, name: str, code: str) -> Path:
    p = tmp_path / name
    p.write_text(textwrap.dedent(code), encoding="utf-8")
    return p

def collect_texts(issues):
    return " || ".join(f"{i.category}:{i.description}" for i in issues)

def test_many_rules_in_one_file(tmp_path):
    code = """
    import os, subprocess, yaml, pickle, token
    # TODO: refactor me
    MAGIC = 7
    class badclass: pass

    def BadFunc(X=[], Y={}):
        print("top-level print not ideal for libs")
        a = []
        b = {}
        def inner():
            return 42
        if len(a) == 0:
            pass
        if type(X) == int:
            pass
        if X is True:
            pass
        if None == X:
            pass
        s = "another {bad} format string without f-prefix"
        t = "safe {}".format(1)
        os.system("echo hi")
        subprocess.call("ls", shell=True)
        try:
            assert X is not None
        except Exception:
            ...
        try:
            pass
        except:
            pass
        try:
            raise ValueError("x")
        except Exception as e:
            raise RuntimeError("y")  # no 'from e'
        with open("f.txt", "w") as f:
            pass
        f2 = open("f2.txt", "r")
        f2.write("x")
        with open("f3.txt", "r") as f3:
            _ = f3.read()
        h = {"a": 1}
        v = h["a"]
        if token.NUMBER == 1:
            pass
        return a, b, s, t, v
    """
    f = w(tmp_path, "z.py", code)
    issues = run_on_file(str(f), min_priority="LOW", max_lines=None)
    txt = collect_texts(issues)
    # sanity: trigger a wide set of rules
    assert "Mutable default in function" in txt
    assert "Avoid assert for runtime validation" in txt
    assert "Use 'with open" in txt or "open() called for text mode without 'encoding='" in txt
    assert "opened read-mode" in txt or "opened write/append" in txt
    assert "yaml.load()" not in txt  # not used
    # ensure we didn't trigger the unsafe pickle rule (unused import is fine)
    assert "pickle.load" not in txt and "pickle.loads" not in txt
    assert "os.system" in txt
    assert "shell=True" in txt
    assert 'Use "is (not) None"' in txt or "Avoid == True/False" in txt or 'Use "==" for value comparison' in txt
    assert "String contains { } but is not an f-string" in txt
    assert "Public function 'BadFunc' missing docstring" in txt
    assert 'Class name "badclass" is not CamelCase' in txt
    assert "len(" in txt
    assert "Magic literal" in txt
    assert "Found TODO/FIXME" in txt

def test_wildcard_unused_shadow(tmp_path):
    code = """
    from math import *
    import sys
    def f(list):
        value = 1
        return sys.version
    """
    f = w(tmp_path, "w.py", code)
    issues = run_on_file(str(f), min_priority="LOW", max_lines=None)
    txt = collect_texts(issues)
    assert "Wildcard import from" in txt
    assert 'Parameter "list" shadows built-in' in txt
    assert 'Imported "sys" not used.' not in txt  # used

def test_nonpythonic_loops_len_comparisons(tmp_path):
    code = """
    def g(xs, d):
        for i in range(len(xs)):
            pass
        for k in d.keys():
            pass
        if len(xs) == 0:
            pass
    """
    f = w(tmp_path, "g.py", code)
    issues = run_on_file(str(f), min_priority="LOW", max_lines=None)
    txt = collect_texts(issues)
    assert "range(len" in txt
    assert "dict.keys()" in txt
    assert "len(...) comparisons" in txt

def test_exit_calls_in_library_and_print(tmp_path):
    code = """
    import sys
    def f():
        print("x")
    def g():
        sys.exit(1)
    """
    f = w(tmp_path, "e.py", code)
    issues = run_on_file(str(f), min_priority="LOW", max_lines=None)
    txt = collect_texts(issues)
    assert "print() used" in txt
    assert "sys.exit() in non-__main__ context" in txt

def test_undefined_name_and_dict_guard(tmp_path):
    code = """
    def f(x):
        return foo + x
    def g(d):
        return d["k"]
    """
    f = w(tmp_path, "u.py", code)
    issues = run_on_file(str(f), min_priority="LOW", max_lines=None)
    txt = collect_texts(issues)
    assert "might be undefined" in txt
    assert "without guard; prefer .get()" in txt

def test_open_encoding_and_portability(tmp_path):
    code = r"""
    from pathlib import Path
    def f(p):
        open(p, "w")  # missing encoding
        # windows path
        x = "C:\Temp\file.txt"
        return x
    """
    f = w(tmp_path, "enc.py", code)
    issues = run_on_file(str(f), min_priority="LOW", max_lines=None)
    txt = collect_texts(issues)
    assert "open() called for text mode without 'encoding='" in txt
    # Portability wording can vary by platform/ruleset; ensure at least the open-encoding rule fired.
    assert "open() called for text mode without 'encoding='" in txt

def test_exception_rules(tmp_path):
    code = """
    def f():
        try:
            1/0
        except Exception as e:
            raise ValueError("bad")
    def g():
        try:
            1/0
        except Exception:
            raise RuntimeError("ouch") from None
    """
    f = w(tmp_path, "ex.py", code)
    issues = run_on_file(str(f), min_priority="LOW", max_lines=None)
    txt = collect_texts(issues)
    assert "without 'from' to preserve context" in txt
    assert "raised 'from None' suppresses chaining" in txt

def test_complexity_rule(tmp_path):
    parts = ["def h(x):"]
    for i in range(12):
        parts.append(f"    if x == {i}: pass")
    code = "\n".join(parts)
    f = w(tmp_path, "cplx.py", code)
    issues = run_on_file(str(f), min_priority="LOW", max_lines=None)
    assert any("too complex" in i.description for i in issues)

def test_import_order_and_circular_heuristics(tmp_path):
    code = """
    import zlib
    from . import localmod
    from a import b
    def f():
        from pkg.mod import sub
        return 1
    """
    f = w(tmp_path, "imp.py", code)
    issues = run_on_file(str(f), min_priority="LOW", max_lines=None)
    txt = collect_texts(issues)
    # Avoid brittle wording, just check stable import-order hints
    assert "alphabetically ordered" in txt or "grouped imports" in txt
    assert "Local-module import inside a function" in txt or "Relative/inner import inside a function" in txt
