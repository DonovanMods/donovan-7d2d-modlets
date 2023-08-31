# Donovan Mods CHANGELOG

*NOTE: This log was only started with mod version v21.0.5, please refer to [Github releases] for any previous version information.*

Also, if you want to see what's coming up, check out the [Develop] branch.

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
[develop]: https://github.com/DonovanMods/donovan-7d2d-modlets/tree/develop
[v21.1.4]: https://github.com/DonovanMods/donovan-7d2d-modlets/compare/v21.1.3...v21.1.4
[v21.1.3]: https://github.com/DonovanMods/donovan-7d2d-modlets/compare/A21.1.2...v21.1.3
[v21.1.2]: https://github.com/DonovanMods/donovan-7d2d-modlets/compare/A21.1.1...A21.1.2
[v21.1.1]: https://github.com/DonovanMods/donovan-7d2d-modlets/compare/A21.0.5...A21.1.1
[v21.0.5]: https://github.com/DonovanMods/donovan-7d2d-modlets/compare/A21.0.4...A21.0.5
