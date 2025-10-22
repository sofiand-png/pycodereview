
from pathlib import Path
import tempfile, os
import pycodereview.code_review as cr

def test_rule_check_returns_empty_when_tree_none():
    r = cr.Rule()
    out = r.check("x.py", None, "")
    assert out == []

def test_rule_make_tuple_branch():
    r = cr.Rule()
    issue = r.make((3, 7), "tuple range")
    assert issue.impacted_lines == "3-7"

def test_rule_make_iterable_branch():
    r = cr.Rule()
    issue = r.make([9, 2, 9, 3], "iterable set sorted")
    # should become "2,3,9"
    assert issue.impacted_lines == "2,3,9"

def test_iter_py_files_directory_and_single_file(tmp_path):
    # Directory branch
    a = tmp_path / "a.py"
    b = tmp_path / "b.txt"
    a.write_text("x=1", encoding="utf-8")
    b.write_text("not py", encoding="utf-8")
    got = list(cr._iter_py_files(str(tmp_path)))
    assert str(a) in got and all(not p.endswith(".txt") for p in got)
    # Single-file branch
    one = tmp_path / "one.py"
    one.write_text("x=2", encoding="utf-8")
    got_single = list(cr._iter_py_files(str(one)))
    assert got_single == [str(one)]

def test_safe_parse_catches_syntax_error(tmp_path):
    bad = "def f(:\n  pass"
    tree = cr._safe_parse(bad, "bad.py")
    assert tree is None
