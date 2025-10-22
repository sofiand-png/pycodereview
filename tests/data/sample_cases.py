"""
Test file exercising the static-analysis rules.

This module intentionally contains many anti-patterns, code smells, and
incorrect constructs for the purpose of verifying the checker.
"""

import csv  # unused
import glob  # unused
from math import *  # wildcard
from random import *  # wildcard

# Simulate “relative before absolute” ordering problem (your tool treats this textually)
# NOTE: this may not import in your real project; it's only to trigger the rule.
try:
    from . import local_mod              # relative before absolute (will be flagged)
except Exception:
    pass
import os                                # absolute after relative (block order)
import subprocess
import pickle
import yaml
from typing import TYPE_CHECKING, Optional, Any, Dict, List, Tuple

if TYPE_CHECKING:
    from .types import T1, T2  # type-only (for CircularImportRule signal)

def takes_builtins(list: list, dict: dict) -> None:  # shadows built-ins
    pass

len = 10  # shadow built-in
id = "abc"  # shadow built-in

Source = "bad_name"  # Variable not snake_case
NotSnake = 1
AnotherNotSnake = 2

def add_dateTime(x):  # not snake_case
    return x

class badClass:  # not CamelCase
    def MethodBad(self, Group):  # not snake_case params / method
        return Group

def FuncBadName(ParamBad):  # not snake_case / param
    return ParamBad


DEPRECATED_COLUMN = "x"  # unused
FIELD_TYPE_HYGIENE = "y"  # unused
UNDEFINED_VARIABLE = "z"  # unused
UNDEFINED_CHOICE = "w"  # unused
UNDEFINED_FUNCTION = "f"  # unused
UNDEFINED_FIELD_TYPE = "t"  # unused
MISSING_LANGUAGE_CODE = "m"  # unused
action = "noop"  # unused
column_name = "col"  # unused
function_name = "fn"  # unused
variable_name = "vn"  # unused
parent = None  # unused
entries = []  # unused
current = 0  # unused
cv = "cv"  # unused

def bad_defaults_a(x=[], y={}):
    x.append(1)
    y["a"] = 1
    return x, y

def bad_defaults_b(flags=set()):
    flags.add("x")
    return flags

def bad_defaults_c(vals=[1, 2]):
    return vals

def loops_and_len(samples: List[int], d: Dict[str, int]):
    for i in range(len(samples)):
        _ = samples[i]
    for k in d.keys():
        _ = d[k]
    if len(samples) > 0:
        pass
    if len(d) == 0:
        pass
    if len(samples) != 0:
        pass

def identity_equality(x):
    if x is True:
        pass
    if x == False:
        pass
    if x == True:
        pass
    if x is not None:
        pass

# TypeCheckRule (type(x)==T), DangerousTokenMagicNumbers
def type_checks(tok):
    if type(tok) == int:
        pass
    if type(tok) == str:
        pass
    if getattr(tok, "type", 0) == 54:
        return True
    if getattr(tok, "type", 0) == 5:
        return False
    return None

def parse_csv_like(s: str):
    for row in s.split(","):
        pass
    for row in s.split(";"):
        pass
    for row in s.split("\t"):
        pass

# EvalExecUse, DangerousFunctions (os.system, subprocess shell=True, yaml.load, pickle.load)
def dangerous_bits(cmd: str, data_b, yml):
    eval("1+2")
    exec("print('x')")
    os.system(cmd)
    subprocess.Popen(cmd, shell=True)
    subprocess.call(cmd, shell=True)
    pickle.loads(data_b)
    yaml.load(yml, Loader=None)  # intentionally unsafe
    yaml.load(yml)               # intentionally unsafe

def file_ops(path):
    f = open(path, "w")   # no encoding + later read
    f.read()
    g = open(path, "r")   # no encoding + later write
    g.write("x")
    h = open(path)        # default text mode, no encoding
    _ = h.read()

def printing(a=1, b=2):
    print("debug:", a, b)
    print("value is {a} and {b}")  # f-string likely intended

print("top-level print not ideal for libs")
print("another {bad} format string without f-prefix")

def may_exit(flag):
    if flag:
        exit(1)
    else:
        quit()

def another_exit():
    import sys
    sys.exit(2)

# UndefinedNameRule (deduped via your rule)—appear once, not twice
def uses_undefined():
    return third_missing + not_defined1 + also_missing  # noqa: F821

def dict_access(d: dict, parts, language, names, row, row_names, results, errors, surveys):
    _ = d["Group"]
    _ = d["choices"]  # unguarded
    _ = d["dict"]     # unguarded
    _ = d["wb"]       # unguarded
    _ = d["row"]      # unguarded
    _ = d["r"]        # unguarded
    _ = d["list"]     # unguarded
    _ = d["tuple"]    # unguarded
    _ = d["row_names"]
    _ = d["language"]
    _ = d["results"]
    _ = d["errors"]
    _ = d["surveys"]
    if len(parts) > 3:
        pass
    if len(parts) == 0:
        pass

def more_dict_access(x):
    _ = x["dict"]
    _ = x["list"]

def ret_mismatch_val() -> None:
    return 1

def ret_mismatch_none() -> str:
    return None

def ret_mismatch_mix() -> None:
    if True:
        return "str"
    return None

# Error Handling: BareOrBroadExcept + the new ones:
def broad_except_examples():
    try:
        1 / 0
    except:
        pass  # empty body (pass)

    try:
        {}["x"]
    except Exception:
        ...  # empty body (ellipsis)

    try:
        int("x")
    except Exception as e:
        raise ValueError("lost context")  # missing "from e"

    try:
        float("x")
    except Exception:
        raise RuntimeError("hidden") from None  # suppresses chaining

def assert_runtime():
    assert 1 == 1
    assert isinstance(2, int)
    assert True
    assert len([1]) > 0

def assert_runtime_two(x):
    assert x is not None
    assert type(x) == int  # also trips TypeCheckRule

def more_type_checks(x):
    if type(x) == list:
        return x

def more_parsing(s: str, wb, row):
    for r in s.split(";"):
        pass
    _ = wb["sheet"]
    _ = row["col"]

p1 = "C:\\temp\\file.txt"
p2 = "C:/temp/other.txt"
p3 = "/usr/local/bin/app"

# ConcurrencyRule + ThreadSafetyRule
from threading import Thread
from multiprocessing import Pool, Process

GLOBAL_LIST = []
GLOBAL_DICT = {}

def thread_target():
    GLOBAL_LIST.append(1)

def thread_target2():
    GLOBAL_DICT["k"] = 2

t1 = Thread(target=thread_target)
t1.start()  # not joined
t2 = Thread(target=thread_target2)
t2.start()  # not joined

def thread_cases():
    t1 = Thread(target=thread_target)
    t2 = Thread(target=thread_target2)
    t1.start()  # not joined
    t2.start()  # not joined

p_import1 = Pool()  # multiprocessing object at import time
p_import2 = Pool()  # again import time

def process_target():
    pass

pr1 = Process(target=process_target)
pr1.start()  # not joined
pr2 = Process(target=process_target)
pr2.start()  # not joined

def process_cases():
    pr1 = Process(target=process_target)
    pr2 = Process(target=process_target)
    pr1.start()  # not joined
    pr2.start()  # not joined

MAG_OK = 42  # defined constant OK

def magic_literals_a(x):
    if x == 7:
        return 13
    return x

def magic_literals_b():
    y = 99
    if y > 3 and y != 2:
        return y

def public_no_doc():  # missing docstring
    return 1

class PublicNoDoc:    # missing docstring
    def method_ok(self):
        """Method ok docstring"""
        return 2

def too_complex(a, b, c):
    r = 0
    for i in range(3):
        if a:
            r += 1
        if b:
            r += 1
        if c:
            r += 1
        r += sum(j for j in range(5) if j % 2 == 0)
        if a and b or c:
            r += 1
    try:
        if a:
            r += 1
    except Exception:
        r -= 1
    return r

class BigClass:
    def f1(self, n):
        total = 0
        for i in range(n):
            if i % 2 == 0:
                total += i
            else:
                total -= i
        if total and (n > 10):
            total += 1
        return total

def compute_value():
    return 123

def find_item():
    return "k"

def ignored_a():
    compute_value()  # ignored
    find_item()      # ignored

def ignored_b():
    res = compute_value()  # used (OK)
    return res

# CircularImportRule (imports within function; TYPE_CHECKING handled above)
def local_import_in_func():
    from .subpkg import thing   # local/relative inside function
    import mypkg.module         # dotted import inside function

def open_no_encoding_a(p):
    f = open(p, "w")   # missing encoding
    f.close()

def open_no_encoding_b(p):
    with open(p, "rt") as fh:  # missing encoding
        _ = fh.read()

def more_broad():
    try:
        1 / 0
    except Exception:
        print("swallowed")  # still broad
    try:
        {}["x"]
    except BaseException:
        print("too broad base")

def more_prints():
    print("one")
    print("two")
    print("three {nope}")  # f-string missing again

# Keep any execution in a guarded main block so importing this file is safe
if __name__ == "__main__":
    # do nothing; we don't actually run the bad constructs
    pass
