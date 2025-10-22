import textwrap
from pathlib import Path
from pycodereview.code_review import run_on_file

def write(tmp_path: Path, name: str, code: str) -> Path:
    p = tmp_path / name
    p.write_text(textwrap.dedent(code), encoding="utf-8")
    return p

def test_mutable_defaults_and_assert(tmp_path):
    code = '''
    def bad(a=[], b={}):
        assert a is not None
        return a, b
    '''
    f = write(tmp_path, "a.py", code)
    issues = run_on_file(str(f), min_priority="LOW", max_lines=None)
    texts = " | ".join(i.description for i in issues)
    assert "Mutable default in function" in texts
    assert "Avoid assert for runtime validation" in texts

def test_open_without_with_and_mode_mismatch(tmp_path):
    code = '''
    def f(p):
        h = open(p, "w")
        h.read()
        g = open(p, "r")
        g.write("x")
    '''
    f = write(tmp_path, "b.py", code)
    issues = run_on_file(str(f), min_priority="LOW", max_lines=None)
    texts = " | ".join(i.description for i in issues)
    assert "Use 'with open" in texts
    assert ("opened read-mode" in texts) or ("opened write/append" in texts)

def test_security_risky_calls(tmp_path):
    code = '''
    import os, subprocess, yaml, pickle
    def g(cmd, y):
        os.system(cmd)
        subprocess.call(cmd, shell=True)
        pickle.loads(b"xyz")
        yaml.load(y)
    '''
    f = write(tmp_path, "c.py", code)
    issues = run_on_file(str(f), min_priority="LOW", max_lines=None)
    descs = [i.description for i in issues]
    assert any("os.system" in d for d in descs)
    assert any("shell=True" in d for d in descs)
    assert any(("pickle.load" in d) or ("pickle.loads" in d) for d in descs)
    assert any("yaml.load()" in d for d in descs)

def test_undefined_name_and_identity_vs_equality(tmp_path):
    code = '''
    def h(x):
        if x == None:
            return foo + 1
        return 0
    '''
    f = write(tmp_path, "d.py", code)
    issues = run_on_file(str(f), min_priority="LOW", max_lines=None)
    descs = [i.description for i in issues]
    assert any('Use "is (not) None"' in d for d in descs)
    assert any("might be undefined" in d for d in descs)

def test_return_annotation_mismatch(tmp_path):
    code = '''
    def a() -> None:
        return 1
    def b() -> str:
        return None
    '''
    f = write(tmp_path, "e.py", code)
    issues = run_on_file(str(f), min_priority="LOW", max_lines=None)
    texts = " | ".join(i.description for i in issues)
    assert ("returns a value but annotation is None" in texts) or            ("returns None but annotation is" in texts)
