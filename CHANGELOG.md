# Donovan Mods CHANGELOG

## [Unreleased]

### Changed

- ModSchematics (3.0.1): recipes regenerated for v3.0 — drops schematics for the removed InsulatedLiner/CoolingMesh armor mods and adds the new v3.0 mods (e.g. drone stun weapon, vehicle storage)
- Build scripts updated for the v3.0 repo layout: retired the lessgrind script library, recipe generators and the xpath validator now read the game XML through the repo's `Config` symlink, `xmlvalidate.py` validates subdirectories (e.g. `XUi_InGame`) and no longer requires colorama
- All Ruby build scripts converted to Python (output verified identical); the repo's only dev dependencies are now Python 3 + lxml, and mise/nokogiri are no longer needed

*NOTE: This log was only started with mod version v21.0.5, please refer to [Github releases] for any previous version information.*

Also, if you want to see what's coming up, check out the [Develop] branch.

## [v3.0.0]

Modlet versions now match the game version they target (starting with game V 3.0).

### Removed

Game v3.0 introduced native Sandbox Options and HUD improvements that made these modlets unnecessary (see the README's migration table for the equivalent settings):

- LessGrind (use `Harvesting/Mining/Scrapping Output` and `Crafting Time/Input/Output`)
- MoreBooks / MegaBooks (use `Crafting Magazines Loot Count`)
- MoreLootbags / MegaLootbags (use `Loot Bag Chance`)
- MorePerks / MegaPerks (use `Skill Points Per Level`)
- MoreHorde (Mutated zombies now appear in Blood Moon hordes natively)
- Donovan UI (food/water bars, day/time display, and loot slot locking are now native)
- The `modlets/optional` folder (all of its modlets were retired)

### Added

- New Modlet: **Preset** - adds a "Donovan" Sandbox Options preset to the new game menu, replicating the retired modlets' settings

### Changed

- All modlets updated and verified for game version 3.0
- BigBackpack/MegaBackpack: updated for the new `XUi_InGame` UI config layout
- The Wraith: updated spawning for the new entity group format

## [v1.2.0]

- Convert all modlets to Game Version 1.2
- Make LessGrind slightly less OP

## [v21.1.6]

### Added

- All modlets now have individual ZIP files in the `ZIPs` folder

### Changed

- Minor restructuring of the folders
  moved modlets that weren't specifically overwrites for AiO out of the `optional` folder
- Updated the READMEs to reflect the new folder structure

## [v21.1.5]

### Changed

- Updated some READMEs to clarify content

### Fixed

- Fixed a bug in bundle recipes for MegaStacks that was causing them to craft more than intended

## [v21.1.4]

### Added

- New Modlet (AiO): Better Brawler - makes Knuckles and Brawler perk more useful
- New Modlet (Optional): Better Start - removes the starting quests and gives you basic resources
- Added elevation data to the Compass in `donovan-ui`

### Changed

- Moved `donovan-wraith` out of AiO and into `modlets` (if you liked having The Wraith, be sure to add it separately)

### Fixed

- Fixed a compatibility bug when independently applying BetterCollectors along with LessGrind (Issue #57)

## [v21.1.3]

### Added

- Modlet installation instructions added to the README

### Changed

- Reduced the cloth requirements on some recipes (notable: Duct Tape is now 2:1)
- Reworked crafting times in `donovan-lessgrind` for the AdvancedEngineering perk (10%, 20%, 30%, 40%, 50%)
- The Wraith will now spawn in some POIs too

### Fixed

- NV Helmet Mod no longer increases sneak

### Removed

- `donovan-levelfaster` has been removed from the list of modlets (no longer needed)

## [v21.1.2]

### Added

- New Modlet (AiO): Better Traps - Blade Traps have more health and do slightly more damage
- New Modlet (AiO): Night Vision Helmet Mod - add a NVG helmet mod (found on Military and Swat Helmets)
- New Modlet (Optional): Craftable Dukes - craft Dukes from Brass + Iron in the Forge

### Changed

- Moved `donovan-morelootbags` into AiO (A21.1 severely reduces the prob of loot bags drops)
- Reorganized the folder structure for the modlets
  - All modlets now live under `modlets`
  - `modlets/a-la-carte` contains the modlets that are included in `donovan-aio`
  - `modlets/optional` contains the modlets that are **not** included in `donovan-aio`

## [v21.1.1]

### Added

- New Modlet: Better Batons (AiO) -- makes Batons on par with Spears

### Fixed

- Verify support for A21.1

## [v21.0.5]

### Added

- The Wraith (AiO) -- a new zombie that spawns at night and/or anytime in the wasteland. It's creepy and spooky, it's CROOKY!

### Fixed

- Various bugfixes for A21.0

<!-- Versions -->
[github releases]: https://github.com/DonovanMods/donovan-7d2d-modlets/releases
[v3.0.0]: https://github.com/DonovanMods/donovan-7d2d-modlets/compare/v1.2.0...v3.0.0
[develop]: https://github.com/DonovanMods/donovan-7d2d-modlets/tree/develop
[v21.1.6]: https://github.com/DonovanMods/donovan-7d2d-modlets/compare/v21.1.5...v21.1.6
[v21.1.5]: https://github.com/DonovanMods/donovan-7d2d-modlets/compare/v21.1.4...v21.1.5
[v21.1.4]: https://github.com/DonovanMods/donovan-7d2d-modlets/compare/v21.1.3...v21.1.4
[v21.1.3]: https://github.com/DonovanMods/donovan-7d2d-modlets/compare/A21.1.2...v21.1.3
[v21.1.2]: https://github.com/DonovanMods/donovan-7d2d-modlets/compare/A21.1.1...A21.1.2
[v21.1.1]: https://github.com/DonovanMods/donovan-7d2d-modlets/compare/A21.0.5...A21.1.1
[v21.0.5]: https://github.com/DonovanMods/donovan-7d2d-modlets/compare/A21.0.4...A21.0.5
