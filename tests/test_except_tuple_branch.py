import textwrap
from pathlib import Path
from pycodereview.code_review import run_on_file

def w(tmp_path: Path, name: str, code: str) -> Path:
    p = tmp_path / name
    p.write_text(textwrap.dedent(code), encoding="utf-8")
    return p

def test_tuple_of_exceptions_branch(tmp_path):
    code = """
    def f():
        try:
            1/0
        except (ValueError, Exception) as e:
            return 1
    """
    fpath = w(tmp_path, "tuple_exc.py", code)
    issues = run_on_file(str(fpath), "LOW", None)
    txt = " | ".join(i.description for i in issues)
    # This forces BareOrBroadExcept to take the tuple branch (lines 112–115).
    assert "Overly broad exception handler (" in txt
