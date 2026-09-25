#!/usr/bin/env python3
"""Thin wrapper: harvest if present, then meet_lm.py. Class C. Not a product."""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent


def main() -> int:
    harvest = HERE / "harvest_corpus.py"
    if harvest.is_file():
        subprocess.call([sys.executable, str(harvest)])
    cmd = [sys.executable, str(HERE / "meet_lm.py"), *sys.argv[1:]]
    print("RUN", " ".join(cmd))
    return subprocess.call(cmd)


if __name__ == "__main__":
    raise SystemExit(main())
