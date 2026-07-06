#!/usr/bin/bash

scripts/mkprofile.sh >profile.txt
python3 scripts/mk_mod_schematic_recipes.py >modlets/donovan-modschematics/Config/recipes.xml
python3 scripts/mk_parts_recipes.py >modlets/donovan-craftableparts/Config/recipes.xml
scripts/mkaio.sh
python3 scripts/ck_versions.py
scripts/mkzips.sh
