# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Overview

This repository contains XML modlets for the game "7 Days to Die". Modlets use the game's XPath DSL to patch game XML files at runtime without modifying original files.

## Repository Structure

- `modlets/donovan-aio/` - All-in-One bundle containing recommended mods combined into a single modlet
- `modlets/a-la-carte/` - Individual modlets that are included in AiO (can be used standalone)
- `modlets/` (top-level) - Standalone modlets not included in AiO
- `ZIPs/` - Pre-packaged ZIP files for distribution
- `Config/` - **SYMLINK to original game XML files. NEVER modify these files.**

## Modlet Structure

Each modlet follows this structure:
```
modlet-name/
├── ModInfo.xml          # Metadata: name, version, author, description
├── Config/              # XPath patch files (named to match game files)
│   ├── items.xml
│   ├── blocks.xml
│   ├── recipes.xml
│   └── ...
├── README.md            # Modlet-specific documentation
└── (optional) localization.txt
```

## XPath Modding Syntax

The game uses a simplified XPath syntax. Common operations:

```xml
<!-- Set a value -->
<set xpath="//item[@name='example']/property[@name='Value']/@value">newValue</set>

<!-- Append new content -->
<append xpath="//item[@name='example']">
  <property name="NewProp" value="123"/>
</append>

<!-- Remove content -->
<remove xpath="//item[@name='example']/property[@name='OldProp']"/>

<!-- CSV operations for comma-separated values -->
<csv xpath="//item[@name='example']/property[@name='Tags']/@value" delim="," op="add">newTag</csv>
```

XPath reference documentation:
- https://7daystodie.fandom.com/wiki/XPath_Explained
- https://community.thefunpimps.com/threads/xpath-modding-explanation-thread.7653/

## AiO Bundle Management

The `donovan-aio` modlet aggregates content from all `a-la-carte` modlets. **Do not manually edit donovan-aio** - it is auto-generated.

To rebuild the AiO bundle after modifying a-la-carte modlets:
```bash
bash scripts/mkaio.sh
```

This runs `mkbundle.py` which:
1. Reads all modlets listed in `aio-modlist.txt`
2. Merges their Config files with `<!-- Included from modlet-name -->` comments
3. Writes combined files to `modlets/donovan-aio/Config/`

## Build Scripts

Located in `scripts/`:

| Script | Purpose | Dependencies |
|--------|---------|--------------|
| `mkall.sh` | Runs the full pipeline: profile, recipe generators, AiO, version check, ZIPs | bash |
| `mkbundle.py` | Combines a-la-carte modlets into donovan-aio | Python 3, lxml (colorama optional) |
| `mkaio.sh` | Regenerates aio-modlist.txt and runs mkbundle.py | bash |
| `mkzips.sh` | Recreates distribution ZIP files from scratch | bash, zip or bsdtar |
| `mk_mod_schematic_recipes.py` | Regenerates modschematics recipes from game items.xml | Python 3, lxml |
| `mk_parts_recipes.py` | Regenerates craftableparts recipes from game items.xml | Python 3, lxml |
| `mkprofile.sh` | Regenerates profile.txt (GitHub links per modlet) | sh |
| `ck_versions.py` | Bumps ModInfo of modlets modified without a version change | Python 3 |
| `vbump.py` | Version bumping utility | Python 3 |
| `xmlvalidate.py` | Validates every modlet xpath against the game XML (run via `validate.sh`) | Python 3, lxml |
| `validate.sh` | Runs xmlvalidate.py against the repo's `Config` symlink | bash |

The recipe generators and `xmlvalidate.py` read the game XML through the repo's `Config` symlink, so they track whatever game version is installed. Run `bash scripts/validate.sh` after any game update to find broken xpaths.

### Dependencies

Python (via pacman on Arch):
```bash
sudo pacman -S python-lxml
```

## Versioning

- Version numbers in `ModInfo.xml` use the `compat` attribute to indicate game version compatibility
- Current game version: 3.0.0 (check README.md for updates)
- Modlet versions match the game version they target (e.g. 3.0.0 for game V 3.0)
- Modlet version: stored in each `ModInfo.xml` and should match across the bundle

## Testing Changes

First run the static validator, which checks every xpath in every modlet against the installed game's XML:

```bash
bash scripts/validate.sh
```

Then test in-game:

1. Copy the modlet to the game's Mods directory:
   ```bash
   cp -r modlets/donovan-aio /data/SteamLibrary/steamapps/common/7\ Days\ To\ Die/Mods/
   ```

2. Launch the game and wait for it to reach the main menu (XML parsing happens during load)

3. Check logs for XPath errors:
   ```bash
   grep -E "WRN XML patch" ~/.local/share/7DaysToDie/logs/output_log_client__*.txt | tail -20
   ```

### Log File Location

- Linux: `~/.local/share/7DaysToDie/logs/output_log_client__<timestamp>.txt`
- Log files are timestamped; check the most recent one after launching

### Common Error Patterns

| Log Pattern | Meaning |
|-------------|---------|
| `WRN XML patch ... did not apply` | XPath expression found no matching elements |
| `ERR XML` | XML syntax error in modlet file |

When XPath patches fail, the game structure has likely changed. Compare the modlet's XPath against the actual game XML in `Config/` (symlinked to game files) to identify the mismatch.

## Game Paths (Linux)

- Game install: `/data/SteamLibrary/steamapps/common/7 Days To Die/` (the repo's `Config` symlink points at its `Data/Config/`)
- Game data/config: `<game>/Data/Config/`
- Mods directory: `<game>/Mods/`
- User data/logs: `~/.local/share/7DaysToDie/`
