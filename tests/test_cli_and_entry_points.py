import runpy, sys
from pathlib import Path

def test_run_module_entrypoint(tmp_path, monkeypatch):
    # Create a temp file so the CLI has an input
    src = tmp_path / "m.py"
    src.write_text("def f():\n    return 1\n", encoding="utf-8")
    argv_bak = sys.argv[:]
    try:
        sys.argv = ["pycodereview", str(src), "--out", str(tmp_path / "r.csv")]
        try:
            runpy.run_module("pycodereview.__main__", run_name="__main__")
        except SystemExit as e:
            # __main__ typically ends with sys.exit(exit_code): accept 0 as success
            assert e.code == 0
    finally:
        sys.argv = argv_bak
