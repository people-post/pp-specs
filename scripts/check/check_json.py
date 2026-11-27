#!/usr/bin/env python3
"""Every tracked .json file parses as UTF-8 JSON, has LF line endings and ends with a newline."""
import json
import subprocess
import sys

files = [f for f in subprocess.run(["git", "ls-files", "*.json"], capture_output=True, text=True, check=True).stdout.split()]
bad = 0
for path in files:
    raw = open(path, "rb").read()
    try:
        json.loads(raw.decode("utf-8"))
    except (UnicodeDecodeError, ValueError) as e:
        print(f"::error file={path}::not valid UTF-8 JSON: {e}")
        bad += 1
        continue
    if b"\r\n" in raw:
        print(f"::error file={path}::CRLF line endings")
        bad += 1
    if raw and not raw.endswith(b"\n"):
        print(f"::error file={path}::no newline at the end")
        bad += 1
print(f"check_json: {len(files)} files, {bad} problems")
sys.exit(1 if bad else 0)
