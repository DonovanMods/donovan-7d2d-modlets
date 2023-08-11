#!/usr/bin/bash

scripts/mkprofile.sh >profile.txt
ruby scripts/mk_lessgrind.rb
ruby scripts/mk_mod_schematic_recipes.rb >modlets/optional/donovan-modschematics/config/recipes.xml
ruby scripts/mk_parts_recipes.rb >modlets/optional/donovan-craftableparts/config/recipes.xml
scripts/mkaio.sh
