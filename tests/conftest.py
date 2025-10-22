# Ensure local src/ is importable even if the package is not installed
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
SRC = REPO_ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

# Keep tests/data from being collected as tests
collect_ignore_glob = ["data/*"]
