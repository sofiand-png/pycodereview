# tests/conftest.py
"""
Pytest configuration.

Ensures src/ is on sys.path so tests can import
crss_example_sensor_voting without manual PYTHONPATH tweaks.
"""

import os
import sys

PROJECT_ROOT = os.path.dirname(os.path.dirname(__file__))
SRC_DIR = os.path.join(PROJECT_ROOT, "src")

if SRC_DIR not in sys.path:
    sys.path.insert(0, SRC_DIR)
