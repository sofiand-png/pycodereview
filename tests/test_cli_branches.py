
from pathlib import Path
from pycodereview.code_review import merge_same_issue_across_lines, Issue


import runpy, sys
def _run_cli(args):
    argv_bak = sys.argv[:]
    try:
        sys.argv = ["pycodereview"] + list(args)
        try:
            runpy.run_module("pycodereview.__main__", run_name="__main__")
        except SystemExit as e:
            return e.code
    finally:
        sys.argv = argv_bak
    return 0

def test_fail_on_low(tmp_path):
    src = tmp_path / "bad.py"
    src.write_text("def f(a=[]):\n    return 1\n", encoding="utf-8")
    code = _run_cli([str(src), "--fail-on", "LOW"])
    assert code == 2

def test_max_lines_and_merge(tmp_path):
    src = tmp_path / "many.py"
    lines = ["def f(a=[]): return 1" for _ in range(50)]
    src.write_text("\n".join(lines), encoding="utf-8")
    out = tmp_path / "m.csv"
    code = _run_cli([str(src), "--out", str(out), "--merge-issues", "--max-lines", "5", "--min-priority", "LOW"])
    assert code in (0, 2)
    assert out.exists()

def test_merge_same_issue_api():
    a = Issue("Cat","LOW","1","Impact","x")
    b = Issue("Cat","LOW","2","Impact","x")
    merged = merge_same_issue_across_lines([("f.py", a), ("f.py", b)])
    assert merged[0][1].impacted_lines in {"1-2", "1,2"}
