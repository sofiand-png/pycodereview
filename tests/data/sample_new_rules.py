# sample_new_rules.py
# Purpose: exercise the NEW rules recently added to pycodereview.
# This file intentionally contains bad patterns for detector testing.

import os
import json
import hashlib
import random
import tempfile
import subprocess
import time
import asyncio
import requests  # type: ignore

# --- WeakHashRule ------------------------------------------------------------
def weak_hash_usage(data: bytes) -> str:
    # md5/sha1 should be flagged
    h1 = hashlib.md5(data).hexdigest()
    h2 = hashlib.sha1(data).hexdigest()
    return h1 + h2

# --- HardcodedSecretRule -----------------------------------------------------
API_KEY = "AKIA1234567890EXAMPLE"   # looks like a key
SECRET_TOKEN = "secret-token-123"    # obvious secret
PASSWORD = "P@ssw0rd!"               # hardcoded password

def uses_secret():
    return SECRET_TOKEN

# --- InsecureHTTPRule --------------------------------------------------------
def insecure_http_call():
    requests.get("http://example.com/api")  # insecure scheme

# --- TempFileSecurityRule ----------------------------------------------------
def bad_tempfile_usage():
    # Predictable tmp path & mktemp() should be flagged.
    tmp1 = tempfile.mktemp(prefix="myapp_")
    open(os.path.join(tempfile.gettempdir(), "myapp_tmp.txt"), "w").write("x")
    return tmp1

# --- RandomForCryptoRule -----------------------------------------------------
def gen_token_bad(n: int = 16) -> str:
    # random for "token" generation should be flagged (use secrets instead)
    alphabet = "abcdefghijklmnopqrstuvwxyz0123456789"
    tok = ""
    for _ in range(n):
        tok += random.choice(alphabet)  # flagged
    return tok

# --- JSONOrderRelianceRule ---------------------------------------------------
def json_order_reliance(s: str) -> bool:
    obj = json.loads(s)
    # Assuming stable key order in JSON objects is not portable across producers
    keys = list(obj.keys())
    return len(keys) > 0 and keys[0] == "first"  # flagged

# --- DictOrderRelianceRule ---------------------------------------------------
def dict_order_reliance() -> bool:
    d = {"alpha": 1, "beta": 2, "gamma": 3}
    # Relying on first key being 'alpha' should be flagged
    return list(d)[0] == "alpha"  # flagged

# --- SubprocessReturnCodeRule -----------------------------------------------
def run_subprocess_ignoring_rc():
    # No check=True and return code/result ignored -> flagged
    subprocess.run(["python", "--version"])  # flagged

# --- BlockingCallInAsyncRule -------------------------------------------------
async def async_blocking():
    # Blocking call in async function (use asyncio.sleep instead)
    time.sleep(0.1)  # flagged
    return 42

# --- InefficientStringConcatInLoopRule --------------------------------------
def concat_in_loop(items) -> str:
    s = ""  # flagged; prefer ''.join(map(str, items))
    for it in items:
        s += str(it)
    return s

# --- ReraiseLosesTracebackRule ----------------------------------------------
def reraise_without_context(x):
    try:
        int(x)
    except Exception as e:
        # Raising a new exception without 'from e' loses context
        raise ValueError("Bad integer")  # flagged


# Light runtime path to ensure the file is runnable if you want to execute it
if __name__ == "__main__":
    print(weak_hash_usage(b"abc"))
    print(uses_secret())
    insecure_http_call()
    print(bad_tempfile_usage())
    print(gen_token_bad())
    print(json_order_reliance('{"first":1,"second":2}'))
    print(dict_order_reliance())
    run_subprocess_ignoring_rc()
    asyncio.run(async_blocking())
    print(concat_in_loop(range(5)))
    try:
        reraise_without_context("x")
    except ValueError:
        pass
