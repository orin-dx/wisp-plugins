"""Scan Claude Code session transcripts for model refusals and reasoning-field output.

Usage: python3 -I scan-refusals.py <projects-dir> <dir-name-regex>
Example: python3 -I scan-refusals.py ~/.claude/projects 'orin-dx|Projects-pages'

Counts, across every transcript (including subagent transcripts):
  - assistant messages by model
  - stop_reason values (a refusal is recorded as "refusal")
  - mentions of the reasoning_extraction category
  - assistant messages whose text carries a JSON "reasoning" field
Absence of refusals only means something if stop_reason values are being recorded, so those are printed too.
"""

import collections
import glob
import os
import re
import sys

root, pattern = os.path.expanduser(sys.argv[1]), re.compile(sys.argv[2])
models, stop_reasons = collections.Counter(), collections.Counter()
refusals = reasoning_messages = files = 0
for directory in sorted(os.listdir(root)):
    if not pattern.search(directory):
        continue
    for path in glob.glob(f"{root}/{directory}/**/*.jsonl", recursive=True):
        files += 1
        for line in open(path, errors="ignore"):
            if "reasoning_extraction" in line or re.search(r'"stop_reason":\s*"refusal"', line):
                refusals += 1
            match = re.search(r'"stop_reason":(null|"[^"]*")', line)
            if match:
                stop_reasons[match.group(1)] += 1
            if '"type":"assistant"' in line:
                model = re.search(r'"model":"([^"]+)"', line)
                if model:
                    models[model.group(1)] += 1
                if '\\"reasoning\\"' in line or '"reasoning":' in line:
                    reasoning_messages += 1
print("files scanned:", files)
print("refusal hits:", refusals)
print("stop_reason values:", stop_reasons.most_common(6))
print("assistant messages by model:", models.most_common(6))
print("assistant messages containing a reasoning field:", reasoning_messages)
