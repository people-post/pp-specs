#!/usr/bin/env python3
"""Every relative link in a tracked Markdown file names a file that exists, and an anchor that exists in it
(GitHub's heading ids). Absolute URLs are not fetched."""
import os
import re
import subprocess
import sys

LINK = re.compile(r"\]\(([^)\s]+)\)")


def slug(heading):
    text = re.sub(r"[`*_]|<[^>]+>", "", heading.strip().lower())
    text = re.sub(r"[^\w\- ]", "", text)
    return text.replace(" ", "-")


def anchors(path, cache={}):
    if path not in cache:
        seen, out = {}, set()
        for h in re.findall(r"^#{1,6} (.*)$", open(path, encoding="utf-8").read(), re.M):
            s = slug(h)
            n = seen.get(s, 0)
            out.add(s if n == 0 else f"{s}-{n}")
            seen[s] = n + 1
        cache[path] = out
    return cache[path]


files = subprocess.run(["git", "ls-files", "*.md"], capture_output=True, text=True, check=True).stdout.split()
bad = 0
for path in files:
    text = open(path, encoding="utf-8").read()
    for target in LINK.findall(text):
        if re.match(r"^[a-z][a-z0-9+.-]*:", target):  # http:, https:, mailto:
            continue
        file_part, _, anchor = target.partition("#")
        dest = os.path.normpath(os.path.join(os.path.dirname(path), file_part)) if file_part else path
        if not os.path.exists(dest):
            print(f"::error file={path}::link to a missing file: {target}")
            bad += 1
        elif anchor and dest.endswith(".md") and anchor not in anchors(dest):
            print(f"::error file={path}::link to a missing heading: {target}")
            bad += 1
print(f"check_links: {len(files)} files, {bad} problems")
sys.exit(1 if bad else 0)
