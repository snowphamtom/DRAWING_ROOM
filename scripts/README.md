# DRAWING_ROOM scripts

Class C only. Not a product. Not MAGPIE. Not a fifth builder.

`verify.py` scans an artifact against `.cursor/rules/locks.mdc` and `.cursor/agents/verifier.md`.

```bash
python3 scripts/verify.py path/to/artifact.md
python3 scripts/test_verify.py
```

Exit 0 = PASS. Exit 2 = REFUSE. Pending / asked-not-granted language is interior.
