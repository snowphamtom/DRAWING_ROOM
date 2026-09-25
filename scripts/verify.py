#!/usr/bin/env python3
"""Class C lock scanner. Not a product. Not MAGPIE. Not a fifth builder.

Reads a text artifact and scores it against DRAWING_ROOM locks.mdc / verifier.md.
Exit 0 PASS. Exit 2 REFUSE. Pending / asked-not-granted language is interior.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

INTERIOR_PHRASES = (
    "asked for, not granted",
    "asked, not granted",
    "not granted",
    "pending",
    "do not rebuild",
    "already live",
    "already shipped",
    "registration facts",
    "registration fact",
    "not installed on a fielded vehicle",
    "lab prototype",
    "separate a-object",
)

GRANT_PATTERNS = (
    re.compile(r"\bgranted\b", re.I),
    re.compile(r"\bpatent was granted\b", re.I),
    re.compile(r"\bmy npa was granted\b", re.I),
)

WELD_NEEDLES = ("magpie", "headroom", "ceilinggate")

AWARD_PATTERNS = (
    re.compile(r"\bselected for the award\b", re.I),
    re.compile(r"\breadiness award", re.I),
    re.compile(r"\bsam(?:\.gov)?\s+active\b.*\baward\b", re.I),
    re.compile(r"\bcage\b.*\baward\b", re.I),
    re.compile(r"\buei\b.*\baward\b", re.I),
)

REBUILD_PATTERNS = (
    re.compile(r"rebuild(?:ing)?\s+ceilinggate", re.I),
    re.compile(r"new ceilinggate (?:app|product|site)", re.I),
)

STAR_INTEGER = re.compile(r"\b1\s*\u2605\s*1\s*=\s*2\b")
FIELD_INSTALL = re.compile(r"installed on a fielded vehicle", re.I)
NPA_DUMP = re.compile(r"\bclaim\s+(?:chart|1\.|2\.)\b", re.I)
NEW_NAME = re.compile(
    r"\b(?:introducing|launching|rebrand(?:ed|ing)?)\s+(?:porch|horizon inbox|the daemon)\b",
    re.I,
)


def _scrub(text: str) -> str:
    out = text
    for phrase in INTERIOR_PHRASES:
        out = re.sub(re.escape(phrase), " ", out, flags=re.I)
    return out


def check(text: str) -> dict:
    raw = text or ""
    scrubbed = _scrub(raw)
    reasons: list[str] = []
    low = scrubbed.lower()

    if any(p.search(scrubbed) for p in GRANT_PATTERNS):
        reasons.append("grant theater")
    if all(n in low for n in WELD_NEEDLES) and re.search(r"\bone product\b", low):
        reasons.append("weld MAGPIE+Headroom+CeilingGate")
    if any(p.search(scrubbed) for p in AWARD_PATTERNS):
        reasons.append("CAGE/UEI/SAM-as-award")
    if any(p.search(raw) for p in REBUILD_PATTERNS):
        reasons.append("CeilingGate rebuild")
    if STAR_INTEGER.search(raw) and "interaction" not in low:
        reasons.append("star minted as integer")
    if FIELD_INSTALL.search(scrubbed):
        reasons.append("fielded-install overclaim")
    if NPA_DUMP.search(raw):
        reasons.append("NPA claim-chart dump")
    if NEW_NAME.search(raw):
        reasons.append("new product name")

    if reasons:
        return {"status": "REFUSE", "reasons": reasons}
    return {"status": "PASS", "reasons": []}


def _read_source(argv: list[str]) -> str:
    if len(argv) > 1:
        path = Path(argv[1])
        if not path.exists():
            raise FileNotFoundError(path)
        return path.read_text(encoding="utf-8", errors="replace")
    if not sys.stdin.isatty():
        return sys.stdin.read()
    raise SystemExit("usage: python3 scripts/verify.py path/to/artifact.md")


def main(argv: list[str]) -> int:
    try:
        text = _read_source(argv)
    except FileNotFoundError as err:
        print(f"REFUSE — missing file {err}", file=sys.stderr)
        return 2
    result = check(text)
    if result["status"] == "PASS":
        print("VERIFY PASS")
        return 0
    print("VERIFY REFUSE")
    for reason in result["reasons"]:
        print(f"- {reason}")
    return 2


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
