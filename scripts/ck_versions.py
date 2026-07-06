#!/usr/bin/env python3
"""Bump the version of any modified modlet whose ModInfo.xml was not updated."""

import re
import subprocess
import sys
from pathlib import Path

modlets = set()
modinfo = set()

changed = subprocess.run(
    ["git", "ls-files", "--modified"],
    capture_output=True, text=True, check=True).stdout

for line in changed.splitlines():
    match = re.match(r"(.*/donovan-\w+)/", line)
    if not match:
        continue
    modlets.add(match[1])
    if "ModInfo.xml" in line:
        modinfo.add(match[1])

vbump = Path(__file__).resolve().parent / "vbump.py"

for modlet in sorted(modlets - modinfo):
    subprocess.run([sys.executable, str(vbump), "-v", "--modlet", modlet], check=True)
