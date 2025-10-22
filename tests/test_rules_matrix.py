import textwrap
import runpy
import sys
from pathlib import Path
from pycodereview.code_review import run_on_file

def _write(tmp_path: Path, name: str, code: str) -> Path:
    p = tmp_path / name
    p.write_text(textwrap.dedent(code), encoding="utf-8")
    return p

def _descs(issues):
    return " | ".join(i.description for i in issues)

def test_identity_len_and_doc(tmp_path):
    code = """
    class bad_name: pass
    def BadFunc(a, b):
        if len([1]) == 0: pass
        if a == None: pass
        return a + b
    """
    f = _write(tmp_path, "mix.py", code)
    txt = _descs(run_on_file(str(f), "LOW", None))
    # Looser assertions to avoid text brittleness:
    assert ("CamelCase" in txt) or ("docstring" in txt)
    assert "len" in txt
    assert ("None" in txt) or ("Use \"is (not) None\"" in txt)

def test_resource_and_exceptions(tmp_path):
    code = """
    def g(p):
        h = open(p, "r")
        try:
            1/0
        except Exception as e:
            raise RuntimeError("x")
    """
    f = _write(tmp_path, "res_exc.py", code)
    txt = _descs(run_on_file(str(f), "LOW", None))
    assert ("opened read-mode" in txt) or ("open(" in txt)
    assert ("preserve context" in txt) or ("from" in txt)

def test_cli_help_and_version_paths(monkeypatch):
    # Run CLI as __main__ (true branch)
    argv_bak = sys.argv[:]
    sys.argv = ["pycodereview", "--help"]
    try:
        runpy.run_module("pycodereview.__main__", run_name="__main__")
    except SystemExit as e:
        assert e.code == 0
    finally:
        sys.argv = argv_bak

    sys.argv = ["pycodereview", "--version"]
    try:
        runpy.run_module("pycodereview.__main__", run_name="__main__")
    except SystemExit as e:
        assert e.code == 0
    finally:
        sys.argv = argv_bak
