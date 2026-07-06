#!/usr/bin/bash

scripts/mkprofile.sh >profile.txt
mise exec -- ruby scripts/mk_mod_schematic_recipes.rb >modlets/donovan-modschematics/Config/recipes.xml
mise exec -- ruby scripts/mk_parts_recipes.rb >modlets/donovan-craftableparts/Config/recipes.xml
scripts/mkaio.sh
mise exec -- ruby scripts/ck_versions.rb
scripts/mkzips.sh
