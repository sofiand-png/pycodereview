import textwrap
import runpy
import sys
from pathlib import Path
from pycodereview.code_review import run_on_file


def _write(tmp_path: Path, name: str, code: str) -> Path:
    """Helper to write a temporary file."""
    p = tmp_path / name
    p.write_text(textwrap.dedent(code), encoding="utf-8")
    return p


def _descs(issues):
    return " | ".join(i.description for i in issues)


def test_identity_and_type_checks(tmp_path):
    code = """
    def f(x):
        if x == None:
            return 1
        if x is True:
            return 2
        if type(x) == int:
            return 3
        return 0
    """
    fpath = _write(tmp_path, "eq.py", code)
    txt = _descs(run_on_file(str(fpath), "LOW", None))
    assert "None" in txt or "True" in txt or "isinstance" in txt


def test_len_and_dict_patterns(tmp_path):
    code = """
    def g(xs, d):
        if len(xs) == 0:
            pass
        for i in range(len(xs)):
            pass
        for k in d.keys():
            pass
    """
    fpath = _write(tmp_path, "len.py", code)
    txt = _descs(run_on_file(str(fpath), "LOW", None))
    assert "len" in txt and "keys" in txt


def test_docstrings_and_naming(tmp_path):
    code = """
    class bad_name:
        pass
    def BadFunc(a, b):
        return a + b
    """
    fpath = _write(tmp_path, "names.py", code)
    txt = _descs(run_on_file(str(fpath), "LOW", None))
    assert "CamelCase" in txt or "docstring" in txt


def test_resource_and_encoding(tmp_path):
    code = """
    def h(p):
        f = open(p, "r")
        f.write("x")
        g = open(p, "w")
        g.close()
    """
    fpath = _write(tmp_path, "io.py", code)
    txt = _descs(run_on_file(str(fpath), "LOW", None))
    assert "open" in txt


def test_exception_patterns(tmp_path):
    code = """
    def e1():
        try:
            1/0
        except:
            pass
    def e2():
        try:
            1/0
        except Exception as e:
            raise RuntimeError("x")
    """
    fpath = _write(tmp_path, "exc.py", code)
    txt = _descs(run_on_file(str(fpath), "LOW", None))
    assert "except" in txt or "raise" in txt


def test_cli_version_and_help(monkeypatch):
    """Run the CLI entrypoint via runpy and ensure --version/--help exit cleanly."""
    argv_bak = sys.argv[:]
    sys.argv = ["pycodereview", "--version"]
    try:
        runpy.run_module("pycodereview.__main__", run_name="__main__")
    except SystemExit as e:
        assert e.code == 0
    finally:
        sys.argv = argv_bak

    sys.argv = ["pycodereview", "--help"]
    try:
        runpy.run_module("pycodereview.__main__", run_name="__main__")
    except SystemExit as e:
        assert e.code == 0
    finally:
        sys.argv = argv_bak


def test_cli_non_py_file(tmp_path):
    """CLI should exit when given a non-Python file."""
    badfile = tmp_path / "x.txt"
    badfile.write_text("not python", encoding="utf-8")

    argv_bak = sys.argv[:]
    sys.argv = ["pycodereview", str(badfile)]
    try:
        runpy.run_module("pycodereview.__main__", run_name="__main__")
        assert False, "Expected SystemExit"
    except SystemExit:
        pass
    finally:
        sys.argv = argv_bak
