"""Filesystem paths used by application."""

import sys
from pathlib import Path

if getattr(sys, 'frozen', False):
    PROJECT_ROOT = Path(sys.executable).resolve().parent
else:
    PROJECT_ROOT = Path(__file__).resolve().parents[2]

TASK_PATH = PROJECT_ROOT / 'tasks.json'
if not TASK_PATH.exists():
    TASK_PATH.touch()

