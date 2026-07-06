#!/usr/bin/env python3
"""Regenerate the modschematics recipes from the game's items.xml.

Writes the recipes XML to stdout; mkall.sh redirects it into
modlets/donovan-modschematics/Config/recipes.xml.
"""

import re
import sys
from pathlib import Path

from lxml import etree

# The repo's Config symlink points at the game's Data/Config directory
config_dir = Path(__file__).resolve().parent.parent / "Config"
items_file = config_dir / "items.xml"

if not config_dir.is_dir():
    sys.exit(f"{config_dir} Does not exist")

items = etree.parse(str(items_file))

configs = etree.Element("configs")
append = etree.SubElement(configs, "append", xpath="/recipes")

for item in items.xpath("//item"):
    schematic_name = item.get("name", "")

    if not re.search(r"mod.*Schematic", schematic_name):
        continue
    if item.xpath("string(property[@name='CreativeMode']/@value)") != "Player":
        continue

    recipe = etree.SubElement(
        append, "recipe",
        name=schematic_name, count="1",
        craft_area="workbench", tags="workbenchCrafting")

    unlocks = item.xpath("string(property[@name='Unlocks']/@value)")
    etree.SubElement(recipe, "ingredient", name=unlocks, count="1")
    etree.SubElement(recipe, "ingredient", name="resourcePaper", count="50")
    etree.SubElement(recipe, "ingredient", name="resourceGlue", count="5")
    etree.SubElement(recipe, "ingredient", name="resourceLeather", count="2")

etree.indent(configs, space="  ")
print(etree.tostring(configs).decode())
