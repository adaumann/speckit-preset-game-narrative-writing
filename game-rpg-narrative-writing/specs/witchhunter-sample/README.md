# The Witchhunter's Road — speckit Sample Project

A minimal but complete D&D 5e computer-game RPG demonstrating all speckit-rpg systems:
**combat · loot · crafting · rest · quests · companion · travel encounters · world map · spatial hierarchy**

---

## What's in the sample

| System | Demonstrated by |
|---|---|
| Character sheet (Fighter L3) | StoryInit, CharacterSheet, HP bar in sidebar |
| Spatial hierarchy | Region: Thornwood → Area: Riverside → LOC-Thorngate, LOC-DrunkGriffin |
| World map (fog: visited) | WorldMap passage, `<<wmLoc>>` calls in LOC passages |
| Quest journal (main + side) | NODE-003 (accept), NODE-004 (advance), NODE-007 (complete + reward) |
| Companion (Mira, approval) | NODE-003 (recruit), approval deltas in NODE-004 and NODE-007 |
| Travel encounter table | NODE-001 (road to Thorngate, goblin patrol / discovery / hazard) |
| Combat (goblins) | NODE-004 (2× Goblin, CR 1/4) |
| Loot (weighted drop) | NODE-004 post-combat → goblin_sack container |
| Crafting (alchemy bench) | NODE-005 (Healing Poultice recipe) |
| Long rest (inn) | NODE-006 (full recovery, day counter +1) |
| Inventory + equipment UI | Sidebar, InventoryUI passage |
| Shop (stub) | LOC-DrunkGriffin → Elara's Sundries (stub passage) |

---

## File structure

```
witchhunter-sample/
├── README.md                         ← you are here
├── witchhunter-init.twee             ← StoryData + StoryTitle + StoryInit (all systems merged)
├── witchhunter-ui.twee               ← StoryMenu, StoryCaption, StoryStylesheet, all UI passages
├── witchhunter-widgets.twee          ← AllWidgets [widget] — all macro implementations
├── witchhunter-locations.twee        ← LOC-Thorngate, LOC-DrunkGriffin
└── witchhunter-nodes.twee            ← NODE-001 through NODE-007
```

---

## How to compile

**Prerequisites**: [tweego](https://www.motoslave.net/tweego/) installed and on PATH.

```bash
cd game-rpg-narrative-writing/specs/witchhunter-sample

tweego -o witchhunter.html \
  witchhunter-init.twee \
  witchhunter-widgets.twee \
  witchhunter-ui.twee \
  witchhunter-locations.twee \
  witchhunter-nodes.twee
```

Open `witchhunter.html` in any browser. No server required.

---

## Scene flow

```
NODE-001_RoadToThorn  (travel — encounter roll: goblin patrol / trap / discovery)
  └─→ LOC-Thorngate              (hub: village gate)
        ├─→ NODE-002_TavernMira  (dialogue + quest accept + companion recruit)
        │     └─→ LOC-DrunkGriffin (hub: tavern)
        │           ├─→ NODE-003_GoblinAmbush  (combat → loot drop)
        │           │     ├─→ NODE-004_AlchemyBench  (crafting)
        │           │     └─→ NODE-005_InnRest       (long rest)
        │           └─→ NODE-006_QuestComplete (quest reward + companion reaction)
        └─→ [WorldMap] → [CharacterSheet] → [QuestJournal] → [PartyRoster]
```

---

## Design spec cross-references

| Doc | What it specifies |
|---|---|
| `constitution-template.md` | Platform: Computer Game · Ruleset: D&D 5e · Engine: sugarcube · VI-B randomness model |
| `world-map-template.md` | REGION-Thornwood → AREA-Riverside → LOC-Thorngate, LOC-DrunkGriffin |
| `variables-d5e.md` | All `$partyLevel`, `$mira_approval`, `$quest_*`, `$loot_*` etc. |
| `quests-template.md` | clear_goblin_lair (main), alchemist_reagents (side) |
| `characters-template.md` | Mira Ashveil, Elder Henne, Elara the Alchemist |
| `mechanics-d5e.md` | Goblin stat blocks, alchemy bench recipe, DC tables |
