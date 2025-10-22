
import csv
import json
import os
import runpy
import sys
import textwrap
from pathlib import Path

import pycodereview.code_review as cr


VALID_PRI = {"LOW", "MEDIUM", "HIGH"}


def _sig_from_json(item):
    return (
        item.get("category", ""),
        item.get("priority", ""),
        item.get("impacted_lines", ""),
        os.path.basename(item.get("file", "")),
    )


def _sig_from_csv_row(row):
    # CSV columns: category;priority;impacted lines;potential impact;description
    if len(row) < 5:
        return None
    category = row[0].strip()
    priority = row[1].strip().upper()
    impacted = row[2].strip()
    desc = row[4].strip()
    # Skip headers/invalid rows by whitelist on priority
    if priority not in VALID_PRI:
        return None
    file_base = desc.split(":", 1)[0] if ":" in desc else ""
    return (category, priority, impacted, file_base)


def test_json_vs_csv_parity(tmp_path: Path):
    code = """
    import os, subprocess, yaml, pickle, io
    class badclass: pass
    def f(a=list(), d={}):
        assert True
        if len(a) == 0: pass
        for i in range(len(a)): pass
        os.system("echo hi")
        subprocess.run("echo 1", shell=True)
        try: yaml.load("x")
        except Exception: pass
        try: pickle.load(io.BytesIO(b""))
        except Exception: pass
        return d["k"]
    """
    target = tmp_path / "t.py"
    target.write_text(textwrap.dedent(code), encoding="utf-8")

    issues = cr.run_on_file(str(target), "LOW", None)
    items = [(str(target), i) for i in issues]

    csv_path = tmp_path / "report.csv"
    json_path = tmp_path / "report.json"
    cr.write_csv(items, str(csv_path))
    assert hasattr(cr, "write_json")
    cr.write_json(items, str(json_path))

    # Load CSV with defensive filtering
    csv_sigs = []
    with csv_path.open("r", encoding="utf-8") as f:
        reader = csv.reader(f, delimiter=";")
        for row in reader:
            sig = _sig_from_csv_row(row)
            if sig:
                csv_sigs.append(sig)

    # Load JSON
    with json_path.open("r", encoding="utf-8") as f:
        j_items = json.load(f)
    json_sigs = [_sig_from_json(x) for x in j_items]

    assert len(csv_sigs) == len(json_sigs)
    assert sorted(csv_sigs) == sorted(json_sigs)


def test_cli_writes_json_output(tmp_path: Path):
    code = """
    def f(a=list()):
        assert True
        return 1
    """
    target = tmp_path / "u.py"
    target.write_text(textwrap.dedent(code), encoding="utf-8")

    out_csv = tmp_path / "out.csv"
    out_json = tmp_path / "out.json"

    argv_bak = sys.argv[:]
    try:
        sys.argv = ["pycodereview", str(target), "--out", str(out_csv), "--json-output", str(out_json)]
        try:
            runpy.run_module("pycodereview.__main__", run_name="__main__")
        except SystemExit as e:
            assert e.code in (0, 2, None)
    finally:
        sys.argv = argv_bak

    assert out_csv.exists(), "CSV not written by CLI"
    assert out_json.exists(), "JSON not written by CLI"
