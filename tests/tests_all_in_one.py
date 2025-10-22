import runpy
import sys
import textwrap
from pathlib import Path
import pycodereview.code_review as cr

# ---------- helpers ----------

def w(tmp_path: Path, name: str, code: str) -> Path:
    p = tmp_path / name
    p.write_text(textwrap.dedent(code), encoding="utf-8")
    return p

def join_desc(issues):
    return " || ".join(i.description for i in issues)

# ---------- core/utility branches ----------

def test_rule_check_none_tree_returns_empty():
    r = cr.Rule()
    assert r.check("x.py", None, "") == []

def test_rule_make_tuple_int_iterable():
    r = cr.Rule()
    assert r.make((3, 5), "x").impacted_lines == "3-5"
    assert r.make(9, "x").impacted_lines == "9"
    assert r.make([9, 2, 9, 3], "x").impacted_lines == "2,3,9"

def test_iter_py_files_dir_and_single(tmp_path):
    (tmp_path / "a.py").write_text("x=1", encoding="utf-8")
    (tmp_path / "b.txt").write_text("nope", encoding="utf-8")
    got = list(cr._iter_py_files(str(tmp_path)))
    assert any(p.endswith("a.py") for p in got)
    one = tmp_path / "one.py"
    one.write_text("x=2", encoding="utf-8")
    got_one = list(cr._iter_py_files(str(one)))
    assert got_one == [str(one)]

def test_safe_parse_catches_syntaxerror():
    tree = cr._safe_parse("def f(:\n  pass", "bad.py")
    assert tree is None

# ---------- rule-specific uncovered paths ----------

def test_bare_broad_tuple_branch(tmp_path):
    code = """
    def f():
        try:
            1/0
        except (ValueError, Exception) as e:
            return 1
    """
    f = w(tmp_path, "tuple_exc.py", code)
    txt = join_desc(cr.run_on_file(str(f), "LOW", None))
    assert "Overly broad exception handler (" in txt

def test_assert_runtime_minimal(tmp_path):
    code = """
    def f(x):
        assert x
    """
    f = w(tmp_path, "asserts.py", code)
    txt = join_desc(cr.run_on_file(str(f), "LOW", None))
    assert "Avoid assert for runtime validation" in txt

def test_eval_exec_and_subprocess_shell(tmp_path):
    code = """
    import subprocess
    def f(x):
        eval("x+1")
        exec("a=1")
        subprocess.run("echo 1", shell=True)
    """
    f = w(tmp_path, "danger.py", code)
    txt = join_desc(cr.run_on_file(str(f), "LOW", None))
    assert "eval(" in txt and "exec(" in txt and "shell=True" in txt

def test_yaml_pickle_and_os_system(tmp_path):
    code = """
    import yaml, pickle, io, os
    def f(y, b):
        try: yaml.load(y)
        except Exception: pass
        try: pickle.load(io.BytesIO(b))
        except Exception: pass
        os.system("echo hi")
    """
    f = w(tmp_path, "iohaz.py", code)
    txt = join_desc(cr.run_on_file(str(f), "LOW", None))
    assert "yaml.load()" in txt and "pickle.load" in txt and "os.system" in txt

def test_identity_len_range_dict_keys(tmp_path):
    code = """
    def g(xs, d, x):
        if len(xs) == 0: pass
        for i in range(len(xs)): pass
        for k in d.keys(): pass
        if x == None: pass
        if x is True: pass
        if type(x) == int: pass
    """
    f = w(tmp_path, "idioms.py", code)
    txt = join_desc(cr.run_on_file(str(f), "LOW", None))
    assert "len(" in txt and "range(len" in txt and "keys()" in txt
    assert ("is (not) None" in txt) or "None" in txt
    assert "True/False" in txt or "Avoid identity with True/False" in txt
    assert "isinstance" in txt or "prefer isinstance" in txt

def test_open_without_with_mode_and_encoding(tmp_path):
    code = """
    def h(p):
        fh = open(p, "r")
        fh.write("x")
        g = open(p, "w")
        g.close()
    """
    f = w(tmp_path, "files.py", code)
    txt = join_desc(cr.run_on_file(str(f), "LOW", None))
    assert "Use 'with open" in txt
    assert ("opened read-mode" in txt) or ("opened write/append" in txt)
    assert "without 'encoding='" in txt

def test_print_and_sys_exit(tmp_path):
    code = """
    import sys
    def f(): print("x")
    def g(): sys.exit(1)
    """
    f = w(tmp_path, "prints.py", code)
    txt = join_desc(cr.run_on_file(str(f), "LOW", None))
    assert "print() used" in txt
    assert "sys.exit() in non-__main__" in txt

def test_wildcard_and_shadowing(tmp_path):
    code = """
    from math import *
    def f(list): return 1
    """
    f = w(tmp_path, "wild.py", code)
    txt = join_desc(cr.run_on_file(str(f), "LOW", None))
    assert "Wildcard import" in txt
    assert "shadows built-in" in txt

def test_naming_docstring_complexity_todo(tmp_path):
    code = """
    # TODO: later
    class badclass: pass
    def BadFunc(a, b):
        if a==0: pass
        if a==1: pass
        if a==2: pass
        if a==3: pass
        if a==4: pass
        if a==5: pass
        if a==6: pass
        if a==7: pass
        if a==8: pass
        if a==9: pass
        if a==10: pass
        if a==11: pass
        return a + b
    """
    f = w(tmp_path, "style.py", code)
    txt = join_desc(cr.run_on_file(str(f), "LOW", None))
    assert ("CamelCase" in txt) or ("missing docstring" in txt)
    assert "too complex" in txt
    assert "TODO" in txt or "FIXME" in txt

def test_fstring_heuristic_and_token_magic(tmp_path):
    code = """
    import token
    def f(x):
        s = "value {x} not f"
        if token.NUMBER == 1: pass
        return s
    """
    f = w(tmp_path, "fmt.py", code)
    txt = join_desc(cr.run_on_file(str(f), "LOW", None))
    assert "not an f-string" in txt
    assert "Magic literal" in txt or "token" in txt

def test_undefined_and_dict_guard(tmp_path):
    code = """
    def f(d):
        return d["k"]
    def g():
        return foo + 1
    """
    f = w(tmp_path, "undef.py", code)
    txt = join_desc(cr.run_on_file(str(f), "LOW", None))
    assert "without guard; prefer .get()" in txt
    assert "undefined" in txt

def test_inner_import_and_import_order_hint(tmp_path):
    code = """
    import zlib
    from . import localmod  # relative import
    def f():
        from os import path
        return path
    """
    f = w(tmp_path, "imports.py", code)
    txt = join_desc(cr.run_on_file(str(f), "LOW", None))
    assert "Local-module import inside a function" in txt or "Relative/inner import inside a function" in txt
    assert ("alphabetically ordered" in txt) or ("grouped imports" in txt) or ("Relative import" in txt)

def test_annotation_mismatch(tmp_path):
    code = """
    def f() -> None:
        return 1
    def g() -> str:
        return None
    """
    f = w(tmp_path, "ann.py", code)
    txt = join_desc(cr.run_on_file(str(f), "LOW", None))
    assert "annotation is None" in txt or "returns None" in txt

# ---------- CLI/error-path coverage ----------

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

def test_cli_no_args_and_dir_error(tmp_path):
    # no args
    code = _run_cli([])
    assert code != 0
    # directory path
    d = tmp_path / "d"
    d.mkdir()
    code2 = _run_cli([str(d)])
    assert code2 != 0

def test_cli_help_and_version():
    assert _run_cli(["--help"]) == 0
    assert _run_cli(["--version"]) == 0

def test_cli_fail_on_low_and_merge_and_max_lines(tmp_path):
    src = tmp_path / "many.py"
    src.write_text("\n".join("def f(a=[]): return 1" for _ in range(40)), encoding="utf-8")
    out = tmp_path / "out.csv"
    code = _run_cli([str(src), "--out", str(out), "--merge-issues", "--max-lines", "5", "--min-priority", "LOW", "--fail-on", "LOW"])
    assert code in (0, 2)  # 2 if fail-on triggers
    assert out.exists()

# ---------- writer/sorter/merge helpers ----------

def test_sort_findings_and_text_log(tmp_path):
    f = tmp_path / "x.py"
    f.write_text("def f(a=[]): return 1\n", encoding="utf-8")
    issues = cr.run_on_file(str(f), "LOW", None)
    items = [(str(f), i) for i in issues]
    sorted_items = cr.sort_findings(items[:])
    assert len(sorted_items) == len(items)
    log = tmp_path / "a.log"
    cr.write_text_log(sorted_items, str(f), str(log))
    assert log.exists() and log.read_text(encoding="utf-8")

def test_merge_same_issue_and_write_csv(tmp_path):
    # build many identical issues to trigger merging/compression
    a = cr.Issue("Cat","LOW","1","Impact","x")
    b = cr.Issue("Cat","LOW","2","Impact","x")
    merged = cr.merge_same_issue_across_lines([("f.py", a), ("f.py", b)])
    assert merged[0][1].impacted_lines in {"1-2", "1,2"}

    out = tmp_path / "m.csv"
    cr.write_csv(merged, str(out))
    assert out.exists() and ";Cat;" in out.read_text(encoding="utf-8")
