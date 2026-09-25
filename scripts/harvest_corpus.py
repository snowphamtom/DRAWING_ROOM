#!/usr/bin/env python3
"""Concatenate owned public text for MeetLM. Class C. Not a product."""
from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "artifacts" / "corpus.txt"
SOURCES = [
    ROOT / "docs" / "concepts.json",
    ROOT / "docs" / "STANDING.md",
    ROOT / "docs" / "index.html",
    ROOT / "README.md",
    ROOT / ".cursor" / "rules" / "locks.mdc",
    ROOT / "scripts" / "meet_lm.py",
]


def main() -> int:
    chunks: list[str] = []
    for path in SOURCES:
        if path.is_file():
            chunks.append(f"# {path.relative_to(ROOT)}\n{path.read_text(encoding='utf-8', errors='ignore')}")
    OUT.parent.mkdir(parents=True, exist_ok=True)
    text = "\n\n".join(chunks).strip() + "\n"
    OUT.write_text(text, encoding="utf-8")
    print(f"wrote {OUT} chars={len(text)} files={len(chunks)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
