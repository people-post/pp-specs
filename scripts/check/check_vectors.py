#!/usr/bin/env python3
"""vectors/manifest.json lists every vectors/*_vectors.json with its sha256, and nothing else: a vector file changes
only with its manifest line in the same pull request, where the change is plain to see."""
import hashlib
import json
import os
import sys

manifest = json.load(open("vectors/manifest.json", encoding="utf-8"))
listed = {e["file"]: e["sha256"] for e in manifest["files"]}
present = {f for f in os.listdir("vectors") if f.endswith("_vectors.json")}
bad = 0
for f in sorted(present - listed.keys()):
    print(f"::error file=vectors/{f}::not in vectors/manifest.json")
    bad += 1
for f in sorted(listed.keys() - present):
    print(f"::error file=vectors/manifest.json::lists {f}, which is not in vectors/")
    bad += 1
for f in sorted(present & listed.keys()):
    digest = hashlib.sha256(open(f"vectors/{f}", "rb").read()).hexdigest()
    if digest != listed[f]:
        print(f"::error file=vectors/{f}::sha256 {digest} is not the manifest's {listed[f]}")
        bad += 1
print(f"check_vectors: {len(present)} files, {bad} problems")
sys.exit(1 if bad else 0)
