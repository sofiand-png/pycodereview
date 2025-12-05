import textwrap
from pathlib import Path
from pycodereview.code_review import run_on_file


def write(tmp_path: Path, name: str, code: str) -> Path:
    p = tmp_path / name
    p.write_text(textwrap.dedent(code), encoding="utf-8")
    return p


def extract_texts(issues):
    return " | ".join(i.description for i in issues)


# ---------------------------------------------------------------------
#  SECURITY
# ---------------------------------------------------------------------

def test_weak_hash_rule(tmp_path):
    code = """
    import hashlib
    def f(x):
        return hashlib.md5(x).hexdigest() + hashlib.sha1(x).hexdigest()
    """
    f = write(tmp_path, "weak_hash.py", code)
    issues = run_on_file(str(f), min_priority="LOW", max_lines=None)
    texts = extract_texts(issues)
    assert "hashlib.md5" in texts or "hashlib.sha1" in texts


def test_hardcoded_secret_rule(tmp_path):
    code = """
    PASSWORD = "secret123"
    TOKEN = "abc123"
    def f(): return PASSWORD
    """
    f = write(tmp_path, "secrets.py", code)
    issues = run_on_file(str(f), min_priority="LOW", max_lines=None)
    texts = extract_texts(issues)
    assert "hardcoded secret" in texts.lower()


def test_insecure_http_rule(tmp_path):
    code = """
    import requests
    def f():
        requests.get("http://example.com")
        requests.post("https://example.com", verify=False)
    """
    f = write(tmp_path, "insecure_http.py", code)
    issues = run_on_file(str(f), min_priority="LOW", max_lines=None)
    texts = extract_texts(issues)
    assert "HTTP URL" in texts or "verify=False" in texts


def test_tempfile_mktemp_rule(tmp_path):
    code = """
    import tempfile
    def f():
        tempfile.mktemp()
    """
    f = write(tmp_path, "mktemp.py", code)
    issues = run_on_file(str(f), min_priority="LOW", max_lines=None)
    assert any("tempfile.mktemp" in i.description for i in issues)


def test_random_for_crypto_rule(tmp_path):
    code = """
    import random
    def f():
        return random.choice("abc") + str(random.randint(0, 9))
    """
    f = write(tmp_path, "random_for_crypto.py", code)
    issues = run_on_file(str(f), min_priority="LOW", max_lines=None)
    assert any("random." in i.description for i in issues)


# ---------------------------------------------------------------------
#  ROBUSTNESS / CORRECTNESS
# ---------------------------------------------------------------------

def test_json_order_reliance_rule(tmp_path):
    code = """
    import json
    def f():
        obj = json.loads('{"a":1,"b":2}')
        first = list(obj.keys())[0]
        return first == "a"
    """
    f = write(tmp_path, "json_order.py", code)
    issues = run_on_file(str(f), min_priority="LOW", max_lines=None)
    assert any("JSON" in i.description or "order" in i.description for i in issues)


def test_dict_order_reliance_rule(tmp_path):
    code = """
    def f():
        d = {"alpha": 1, "beta": 2, "gamma": 3}
        first = next(iter(d))
        return first == "alpha"
    """
    f = write(tmp_path, "dict_order.py", code)
    issues = run_on_file(str(f), min_priority="LOW", max_lines=None)
    assert any("dict" in i.description.lower() or "order" in i.description.lower() for i in issues)


def test_subprocess_return_code_rule(tmp_path):
    code = """
    import subprocess
    def f():
        subprocess.run(["echo", "hi"])
    """
    f = write(tmp_path, "subprocess_rc.py", code)
    issues = run_on_file(str(f), min_priority="LOW", max_lines=None)
    assert any("subprocess.run" in i.description for i in issues)


# ---------------------------------------------------------------------
#  CONCURRENCY / ASYNC
# ---------------------------------------------------------------------

def test_blocking_call_in_async_rule(tmp_path):
    code = """
    import time
    import asyncio
    async def f():
        time.sleep(0.1)
    """
    f = write(tmp_path, "async_blocking.py", code)
    issues = run_on_file(str(f), min_priority="LOW", max_lines=None)
    assert any("Blocking" in i.description for i in issues)


# ---------------------------------------------------------------------
#  STYLE / PERFORMANCE / MAINTAINABILITY
# ---------------------------------------------------------------------

def test_inefficient_string_concat_in_loop_rule(tmp_path):
    code = """
    def f(xs):
        s = ""
        for x in xs:
            s = s + str(x)   # ensure explicit concat
        return s
    """
    f = write(tmp_path, "string_concat.py", code)
    issues = run_on_file(str(f), min_priority="LOW", max_lines=None)
    assert any("concat" in i.description.lower() or "join" in i.description.lower() for i in issues)



# ---------------------------------------------------------------------
#  ERROR HANDLING
# ---------------------------------------------------------------------

def test_reraise_loses_traceback_rule(tmp_path):
    code = """
    def f():
        try:
            int("x")
        except Exception as e:
            raise ValueError("oops")
    """
    f = write(tmp_path, "reraise_traceback.py", code)
    issues = run_on_file(str(f), min_priority="LOW", max_lines=None)
    assert any("traceback" in i.description for i in issues)
