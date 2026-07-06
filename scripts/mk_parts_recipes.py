#!/usr/bin/env python3
"""Regenerate the craftableparts recipes from the game's items.xml.

Writes the recipes XML to stdout; mkall.sh redirects it into
modlets/donovan-craftableparts/Config/recipes.xml.
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
    recipe_name = item.get("name", "")

    if not re.search(r"(?:armor|gun|melee).*Parts$", recipe_name):
        continue

    metal = ("resourceForgedIron" if re.search(r"T[1-2].*Parts$", recipe_name)
             else "resourceForgedSteel")
    parts = ("resourceElectricParts" if re.search(r"(Robotics|StunBaton)Parts$", recipe_name)
             else "resourceMechanicalParts")

    recipe = etree.SubElement(
        append, "recipe",
        name=recipe_name, count="1",
        craft_area="workbench", tags="workbenchCrafting")

    etree.SubElement(recipe, "ingredient", name=metal, count="1")
    etree.SubElement(recipe, "ingredient", name="resourceDuctTape", count="5")
    etree.SubElement(recipe, "ingredient", name=parts, count="10")

etree.indent(configs, space="  ")
print(etree.tostring(configs).decode())
