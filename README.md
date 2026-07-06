# Donovan's 7 Days to Die Modlets

**V3.0 UPDATE!** All modlets have been updated for game version 3.0! Several modlets have been retired because the game now provides their functionality natively — see [Removed in V3.0](#removed-in-v30-use-sandbox-options-instead) for how to reproduce their effects with the new Sandbox Options.

This is a collection of modlets I've made in order to enhance the "fun factor" of 7 Days to Die and most of them I would considered "Quality of Life" changes, but, of course, you're free to define them however you wish.

The modlets are all intended to be used a la carte, so you can freely mix and match the ones _you_ think will make your game more enjoyable. Any exceptions are noted in the descriptions below (some conflict with each other because they alter the same things in different ways).

Please see the README located in each of the modlet's directories for more details.

These are all available individually and are intended to work in unison, so feel free to mix and match to suit your needs, however, pay attention to any conflicts listed in the descriptions.

Verfied under game version: _3.0.0_

## Installation

### Setup

If you haven't already, head over to [releases](https://github.com/DonovanMods/donovan-7d2d-modlets/releases) and download the `source code.zip` file.

1. Unzip that file into a temporary directory.
1. Locate your "7 Days to Die" game folder (usually something like `C:\Program Files (x86)\steamapps\common\7 Days To Die`).
1. If if doesn't already exist, create a `Mods` folder in that directory.

#### Individual ZIP files

If you want to pick and choose the modlets you want, individual ZIP files for each can be found in the `ZIPs` directory.

### Choosing the Modlets you want

All the modlets live under the `modlets` folder in the ZIP file, so navigate there first.

Now you have several choices, and each of the modlets are detailed below. For the best "all around" experience, we recommend you start with `donovan-aio` but you're free to pick and choose.

Look through the descriptions below and find whatever modlets you want to install (e.g. `donovan-aio`) and copy (or move) that entire folder over to the `7 Days to Die\Mods` directory you located or created above.

For this example, we're going to assume you want to install `donovan-aio` and `donovan-wraith`.

Once you copy those folders over, your directory structure should look something like this:

```text
7 Days to Die\
  Mods\
    donovan-aio\
    donovan-wraith\
```

### Notes

All modlets under `a-la-carte` are already included in `donovan-aio`, so there's no need to copy any of them over if you're using `donovan-aio`. However, if there are modlet's included in `donovan-aio` that you _don't_ want, then feel free to pick and choose whatever you like under the `a-la-carte` folder and copy them individually.

## Support

If you find any issues or have a suggestion for improvement, [please open an issue on github](https://github.com/DonovanMods/donovan-8d2d-modlets/issues) or find me on Guppy's 7D2D modding Discord server and I'll look into it ASAP.

## Modlets

All modlets live under the `modlets` folder in the source ZIP file, so navigate there first. Each modlet has it's own README with more details.

Other folders in the ZIP can be safely ignored.

### AiO

The _All In One_ modlet is a bundle of modlets which _I personally_ recommend for the "best" experience, but they are all available individually, so feel free to mix and match should you desire.

Any modlets added after the AiO will overrule what's included in the AiO, esentially replacing the mod with a different one. e.g. `more*` vs `mega*` modlets. So you can start with AiO as your base and add additional ones to customize your experience.

- [All-In-One](modlets/donovan-aio) - My "recommended" modlets all bundled together into a single modlet for convience.

#### Included in AiO

Note that any of these mods can also be used a-la-carte, we just bundle them together for convienence in AiO.

- [BetterBatons](modlets/a-la-carte/donovan-betterbatons) - Increases melee damange on pipe and stun batons (puts them on par with spears/clubs)
- [BetterBlades](modlets/a-la-carte/donovan-betterblades) - Increases melee damange on bladed weapons, spears, and axes
- [BetterBrawler](modlets/a-la-carte/donovan-betterBrawler) - Increases melee damange on knuckle weapons, increasing with the Brawler Perk
- [BetterBridges](modlets/a-la-carte/donovan-betterbridges) - Allows advanced rotation on garage door and drawbridge
- [BetterBuffs](modlets/a-la-carte/donovan-betterbuffs) - Tweaks (de)buffs; i.e. shorter NearDeathTrauma and no more being thirsty/hungry at 190%
- [BetterCement](modlets/a-la-carte/donovan-bettercement) - Create 'Cement Mix' directly in the cement mixer
- [BetterDyes](modlets/a-la-carte/donovan-betterdyes) - Allows all colored dyes to be crafted from paint
- [BetterPowertools](modlets/a-la-carte/donovan-betterpowertools) - Makes the Chainsaw, Auger, and Nailgun way more useful
- [BetterTraps](modlets/a-la-carte/donovan-bettertraps) - Blade Traps have more health and do slightly more damage
- [LongerLootbags](modlets/a-la-carte/donovan-longerlootbags) - Decreases the decay rate on zombie lootbags from 5 to 30 minutes
- [MegaStacks](modlets/a-la-carte/donovan-megastacks) - Vastly increases stack sizes
- [PickMeUp](modlets/a-la-carte/donovan-pickmeup) - Allows for certain blocks to be picked up after placing.

### Other Modlets

- [Preset](modlets/donovan-preset) - Adds a "Donovan" Sandbox Options preset to the new game menu (my recommended settings, replicating the retired modlets below)
- [CraftableDukes](modlets/donovan-craftabledukes) - Allows you to craft Dukes from Brass + Iron in the Forge
- [CraftableParts](modlets/donovan-craftableparts) - Allows you to craft all weapon and armor parts in the workbench.
- [ModSchematics](modlets/donovan-modschematics) - Turn mods into schematics
- [NightFog](modlets/donovan-nightfog) - Thick fog rolls in at night
- [Wraith](modlets/donovan-wraith) - Adds a new zombie type, the Wraith, which is a fast, stealthy, and deadly zombie

#### Inventory Size (only install one of these at at time)

1. [BigBackpack](modlets/donovan-bigbackpack) - Increases the size of the player inventory to 60
2. [MegaBackpack](modlets/donovan-megabackpack) - Increases the size of the player inventory to 120

### Removed in V3.0 (use Sandbox Options instead)

Game version 3.0 introduced a large set of native **Sandbox Options** (new game settings) and HUD improvements that made several of these modlets unnecessary. If you used any of the modlets below, here's how to get the same effect in the vanilla game:

| Removed Modlet | Native V3.0 Replacement |
|---|---|
| LessGrind | Sandbox Options: `Harvesting Output`, `Mining Output`, `Scrapping Output`, `Crafting Time`, `Crafting Input`, `Crafting Output` |
| MoreBooks / MegaBooks | Sandbox Option: `Crafting Magazines Loot Count` |
| MoreLootbags / MegaLootbags | Sandbox Option: `Loot Bag Chance` |
| MorePerks / MegaPerks | Sandbox Option: `Skill Points Per Level` |
| MoreHorde | The game now includes the Mutated zombie family in Blood Moon hordes natively |
| Donovan UI | Food/water bars now sit under health/stamina natively; the compass shows day/time/temperature (`Show Day/Time` option); loot containers have a native slot-locking toggle |

### Outdated/Removed Modlets

- BetterSpears - incorporated into `BetterBlades`
- CraftAcid - Incorporated into `Craftables`
- CraftBeaker - Incorporated into `Craftables`
- CraftSpikes - REMOVED as of A20 (no longer supported by the game)
- BetterBandages - REMOVED as of A21 (now incorporated into the base game!)
- CraftableJail - REMOVED as of A21 (now incorporated into the base game)
- LootCleanup - REMOVED as of A21 (now incorporated into the base game)
- Craftables - REMOVED as of A21 due to compatibility issues with the base game
- LevelFaster - REMOVED as this functionality is now included in game (via Experience %).
- BetterVehicles - REMOVED in v1.0 due to the game's vehicle overhaul
- NVHelmetMod - REMOVED in v1.0 due to the game's overhaul of the armor system
- BetterStart - REMOVED in v1.0 because it interferes with multi-player and, generally speaking, wasn't very useful
- BetterCollectors - REMOVED in v1.0 as it's no longer needed

## Additional Credits

- ["Rain Collectors" mod by khzmusik](https://gitlab.com/karlgiesing/7d2d-a21-modlets) in order to add additional functionality for Dew Collectors

## History

I previously used an excellent XML config replacement made by [SpikeDaddy](https://www.youtube.com/@spikedaddy46), so full credit to him for his work and my inspiration!

With the addition of xpath support to the game architecture, I decided to convert some of his changes along with a few of my own into a series of a-la-carte modlets. The result is this body of work, which will be updated with new ideas and to support future stable versions of 7D2D.

Enjoy!

-- Donovan
