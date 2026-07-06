#!/usr/bin/env python3
"""Bump the version in a modlet's ModInfo.xml.

With no bump option, the patch level is incremented.
"""

import argparse
import re
import sys
from pathlib import Path


def next_version(current, args):
    major, minor, patch = (int(part) for part in current.split("."))

    if args.major is not None:
        return f"{args.major}.{args.minor or 0}.{args.patch or 0}"
    if args.minor is not None:
        return f"{major}.{args.minor}.{args.patch or 0}"
    if args.patch is not None:
        return f"{major}.{minor}.{args.patch}"
    return f"{major}.{minor}.{patch + 1}"


def main():
    parser = argparse.ArgumentParser(
        prog="vbump", description="Bump a modlet's ModInfo.xml version")
    parser.add_argument("-M", "--major", metavar="VERSION", help="Bump to this MAJOR")
    parser.add_argument("-m", "--minor", metavar="VERSION", help="Bump to this MINOR")
    parser.add_argument("-p", "--patch", metavar="VERSION", help="Bump to this PATCH")
    parser.add_argument("-v", "--verbose", action="count", default=0, help="Run verbosely")
    parser.add_argument("--modlet", help="The modlet to bump")
    parser.add_argument("--pretend", action="store_true", help="Don't actually write anything")
    parser.add_argument("modlet_arg", nargs="?", help=argparse.SUPPRESS)
    args = parser.parse_args()

    modlet = args.modlet or args.modlet_arg
    if not modlet:
        sys.exit("Please provide a modlet to inspect")

    modinfo = Path(modlet) / "ModInfo.xml"
    modlet_name = Path(modlet).name
    if not modinfo.is_file():
        sys.exit(f"Invalid modlet (could not find a ModInfo.xml file for {modlet_name})")

    contents = modinfo.read_text()
    match = re.search(r'<Version value="(.+)"\s+\w', contents)
    if not match:
        sys.exit(f"Could not find a Version in {modinfo}")
    current = match[1]

    version = next_version(current, args)

    if args.verbose > 0:
        print(f"Bumping version for {modlet_name} to {version}")
    if args.verbose > 1:
        print(f"From version {current}")

    contents = re.sub(r'<Version value="\d+\.\d+\.\d+', f'<Version value="{version}', contents)

    if not args.pretend:
        modinfo.write_text(contents)


if __name__ == "__main__":
    main()
