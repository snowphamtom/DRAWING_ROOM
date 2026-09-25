#!/usr/bin/env python3
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent))
from verify import check

PASS_TEXT = """
Monsters Ink LLC capability brief.
MAGPIE is U.S. App. 19/658,750 pending. Asked for, not granted.
Headroom is 64/150,688. Separate A-object.
CeilingGate already live on Convex. Do not rebuild.
CAGE 24VL0 and UEI R9SQEQR51E46 are registration facts.
Lab prototype. Not installed on a fielded vehicle.
"""

REFUSE_GRANT = "Our MAGPIE patent was granted this morning at 5:01."
REFUSE_WELD = "MAGPIE Headroom and CeilingGate are now one product."
REFUSE_AWARD = "SAM.gov Active means we were selected for the award."


def main() -> int:
    assert check(PASS_TEXT)["status"] == "PASS", check(PASS_TEXT)
    assert check(REFUSE_GRANT)["status"] == "REFUSE"
    assert check(REFUSE_WELD)["status"] == "REFUSE"
    assert check(REFUSE_AWARD)["status"] == "REFUSE"
    print("test_verify PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
