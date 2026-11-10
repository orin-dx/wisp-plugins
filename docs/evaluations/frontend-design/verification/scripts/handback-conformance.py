"""Check recorded gate verdict files against the verdict schemas the repo defines.

Usage: python3 -I handback-conformance.py <directory> [glob]
Example: python3 -I handback-conformance.py ~/projects/pages/docs/specs '*verdict*.json'

Uses the validator from shared/hooks/validate-handback.py (the WP-624 spike). A file counts as
conforming when it validates against verdict@1 or verdict@3. The persisted files were written by
an orchestrator from the gate agents' handbacks, so they approximate, and may not equal, the
handbacks themselves.
"""

import collections
import glob
import importlib.util
import json
import os
import re
import sys
from pathlib import Path

root = Path(__file__).resolve().parents[5]
spec = importlib.util.spec_from_file_location("validate_handback", root / "shared" / "hooks" / "validate-handback.py")
validate_handback = importlib.util.module_from_spec(spec)
spec.loader.exec_module(validate_handback)

directory = os.path.expanduser(sys.argv[1])
pattern = sys.argv[2] if len(sys.argv) > 2 else "*verdict*.json"
schemas = {name: validate_handback.load_schema(name) for name in ("verdict@1", "verdict@3")}
shapes = collections.defaultdict(collections.Counter)
violations = collections.Counter()
lengths = []
files = sorted(glob.glob(os.path.join(directory, pattern)))
for path in files:
    report = json.load(open(path))
    results = {name: validate_handback.validate(report, schema) for name, schema in schemas.items()}
    shape = "verdict@3-shaped" if "verified_scope" in report else "verdict@1-shaped"
    conforms = any(not errors for errors in results.values())
    shapes[shape]["conforming" if conforms else "violating"] += 1
    if not conforms:
        own = results["verdict@3" if shape == "verdict@3-shaped" else "verdict@1"]
        for error in own:
            violations[re.sub(r"\[\d+\]", "[n]", re.sub(r"'[^']+'", "'x'", error.split(": ", 1)[1]))] += 1
    if isinstance(report.get("verdict_summary"), str):
        lengths.append(len(report["verdict_summary"]))
print(f"{len(files)} files")
for shape, counts in shapes.items():
    print(f"  {shape}: {dict(counts)}")
print("violations among non-conforming files:", dict(violations))
if lengths:
    lengths.sort()
    print(f"verdict_summary length: median {lengths[len(lengths) // 2]}, max {max(lengths)}, over 300: {sum(1 for n in lengths if n > 300)}")
