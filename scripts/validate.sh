#!/usr/bin/bash

# The repo's Config symlink points at the game's Data/Config directory
cd "$(dirname "$0")/.." || exit 1

python3 scripts/xmlvalidate.py -c Config -v "$@"
