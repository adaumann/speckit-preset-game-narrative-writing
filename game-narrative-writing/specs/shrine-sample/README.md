# Shrine Encounter — Minimal Narrative Design Sample

A **minimal but complete** narrative design sample demonstrating core speckit mechanics for dialogue-driven games.

**Demonstrates:** Dialogue branching · Attribute gating · Inventory checks · Choice consequences · Character profiles

---

## Overview

This sample is **much simpler than Witchhunter** and focuses purely on **narrative design validation**:
- 3 scenes (Shrine entrance → Dialogue with Priestess → Outcomes)
- 1 NPC (Priestess)
- 3 player attributes (Intelligence, Wisdom, Power)
- 1 inventory item (Amulet)
- Multiple endings based on dialogue choice + attributes

**Total scope:** 2-3 hours to design, 30 mins to playtest

---

## What's Included

| Component | File | Purpose |
|---|---|---|
| **Widget reference** | `WIDGETS_GUIDE.md` | Simplified pattern: character profile (read-only), inventory (pickup/check/view) |
| **Widget definitions** | `shrine-widgets.twee` | SugarCube macros for inventory & character display |
| **Story initialization** | `shrine-init.twee` | Character object, inventory array, story metadata |
| **UI chrome** | `shrine-ui.twee` | StoryCaption (HUD), StoryMenu, character/inventory pages |
| **Narrative nodes** | `shrine-nodes.twee` | 3 scenes with dialogue branching + attribute gating |
| **Design specs** | `specs/` | Plan, constitution, characters, outlines |
| **Playable game** | `shrine.html` | Compiled SugarCube (open in browser) |

---

## File Structure

```
shrine-sample/
├── README.md                    ← you are here
├── WIDGETS_GUIDE.md             ← Widget pattern explanation
├── shrine-widgets.twee          ← Widget definitions (charProfile, inventory, hasItem)
├── shrine-init.twee             ← StoryData + character/inventory init
├── shrine-ui.twee               ← StoryCaption, CharacterSheet, InventoryUI
├── shrine-nodes.twee            ← START, AskHistory, Donate, Search, End
├── shrine.html                  ← PLAYABLE GAME (compiled)
└── specs/
    ├── plan.md                  ← Node map (3 scenes)
    ├── constitution.md          ← Mechanics config (attributes, inventory)
    └── characters.md            ← Priestess NPC, player stats (INT 5, WIS 6, PWR 4, GLD 10)
```

---

## How It Works

### Simplified Widget Pattern

**Character Profile (Read-Only)**
- Displays 4 narrative attributes: Intelligence, Wisdom, Power, Gold
- Only changes through `<<set>>` commands in dialogue choices
- **No widget-based stat modifications**

**Inventory System (Minimal)**
- `<<pickupItem>>` — Add item to inventory
- `<<hasItem>>` — Check if player has item (gates dialogue options)
- `<<inventory>>` — Display inventory list
- **No drop/equip/complex mechanics**

(See `WIDGETS_GUIDE.md` for complete reference)

### Scene 1: Shrine Entrance
```
>> Start passage
"You stand before an ancient shrine..."
Choice: [Ask about history] [Donate] [Search]
```

**Narrative outcome:** Sets up character intent

### Scene 2-4: Dialogue Branches

**Ask About History** (Intelligence gate ≥6)
- High INT → Recognize pre-imperial architecture → Wisdom +1
- Low INT → Polite confusion

**Donate** (Gold gate)
- Have ≥5 gold → Generous donation → Wisdom +2
- Have 1+ gold → Small donation → Priestess thanks you
- No gold → Can't donate

**Search** (Inventory action)
- Find Old Book → `<<pickupItem "old_book" "Old Book">>`
- Priestess recognizes it as shrine's grimoire

All branches return to `Start` or end adventure.

---

## Widgets Reference

1. **Open in browser:**
   ```bash
   open shrine.html
   ```
   Or double-click `shrine.html` in Windows Explorer

2. **Read the prose**

3. **Click dialogue choices** — they appear based on your attributes

4. **Watch attribute values change** in the Character widget (top right)

5. **Reach an ending** (3 possible outcomes)

6. **Restart** to try different dialogue choices

---

## Design Documents

If you want to understand how this was created using speckit:

### `specs/plan.md`
```yaml
NODE-001_ShrineEntrance:
  title: "Before the Shrine"
  act: I
  choices:
    - target: NODE-002 (enter shrine)
    - target: END-CowardPath (turn back)

NODE-002_PriestessDialogue:
  title: "Priestess of the Old Ways"
  act: I
  dialogue: priestess-main
  branches:
    - condition: wisdom >= 6
      target: NODE-003-WisdomEnding
    - condition: intelligence >= 7
      target: NODE-003-IntelligenceEnding
    - else:
      target: NODE-003-DefaultEnding
```

### `specs/characters.md`
**Player Character:**
- Intelligence: 5 (1-10)
- Wisdom: 5 (1-10)
- Power: 5 (1-10)
- Gold: 50 (0-200)

**Priestess (NPC):**
- Respectful but guarded
- Respects wisdom and insight
- Wary of aggression (power-based dialogue)
- Recognizes the Amulet

### `specs/constitution.md`
```yaml
mechanics_enabled:
  - flag: true
  - attribute: true
  - inventory: true
  - dialogue_branching: true

custom_attributes:
  - intelligence: 1-10
  - wisdom: 1-10
  - power: 1-10
  - gold: 0-200
```

---

## Playtest Checklist

When you open the game:

- [ ] Character widget displays starting values (5/5/5, 50 gold)
- [ ] Dialogue choices appear/disappear based on attribute values
- [ ] Clicking a choice leads to the correct next scene
- [ ] Character widget updates when attributes change
- [ ] Three different endings are possible (try all dialogue branches)
- [ ] Amulet in inventory affects Priestess dialogue

---

## How This Relates to Witchhunter

| Aspect | Shrine (Minimal) | Witchhunter (Full) |
|---|---|---|
| **Scope** | 3 nodes, 1 NPC | 7+ nodes, 4+ NPCs |
| **Systems** | Dialogue, attributes, inventory | Combat, quests, companion, loot, rest |
| **Duration** | 5-10 min playthrough | 30+ min campaign |
| **Design time** | 2-3 hours | 40+ hours |
| **Good for...** | Learning narrative design | Reference implementation |

**Use Shrine sample to:** Learn dialogue gating, attribute mechanics, simple branching

---

## Widget Pattern Guide

For detailed documentation on how to use these widgets in your own projects, see **[WIDGETS_GUIDE.md](WIDGETS_GUIDE.md)**.

### Quick Reference

| Widget | Purpose | Example |
|---|---|---|
| `<<charProfile>>` | Display character stats (read-only) | `<<charProfile>>` |
| `<<charAttr "attr">>` | Single stat value inline | `You sense <<charAttr "wisdom">> points...` |
| `<<pickupItem "key" "Name">>` | Add item to inventory | `<<pickupItem "old_book" "Old Book">>` |
| `<<hasItem "key">>` | Check if has item (sets `_hasItem`) | `<<if _hasItem>>You have it<</if>>` |
| `<<inventory>>` | Display all items | `<<inventory>>` |

**Character object:** `$character.intelligence`, `$character.wisdom`, `$character.power`, `$character.gold`

**Inventory array:** `$inventory = [{item, name, qty}, ...]`

For full guide with patterns and export checklist, see [WIDGETS_GUIDE.md](WIDGETS_GUIDE.md).

**Use Witchhunter as:** Reference for complex systems (combat, quests, progression)

---

## Next Steps

After exploring this sample:

1. **Copy the structure** to build your own narrative:
   ```bash
   cp -r shrine-sample my-game-sample
   ```

2. **Edit `specs/characters.md`** — Change NPC, attributes, starting inventory

3. **Edit `specs/plan.md`** — Expand node graph, add more scenes

4. **Edit `outline/*.md`** — Flesh out dialogue trees

5. **Run `speckit export --engine sugarcube`** to generate new `.twee` files

6. **Run `tweego`** to compile to HTML and playtest in browser

---

## File Reference: What Gets Exported to SugarCube

The `.twee` files are what you actually compile. Here's how they map to your narrative design:

**shrine-init.twee** (Init data):
```twee
StoryData
  "ifid": "..."
  
StoryInit
  <<set $character to {
    intelligence: 5,
    wisdom: 5,
    power: 5,
    gold: 50
  }>>
  <<set $inventory to {
    amulet: true
  }>>
```

**shrine-nodes.twee** (Narrative):
```twee
:: NODE-001_ShrineEntrance [act-I]
You stand before an ancient shrine...

[[Enter the shrine|NODE-002_PriestessDialogue]]
[[Turn back|END-CowardPath]]

:: NODE-002_PriestessDialogue [act-I dialogue-heavy]
A priestess looks up from her prayers.

<<if $character.wisdom gte 6>>
  [[Ask about the shrine's purpose|NODE-003-WisdomEnding]]
<</if>>

<<if $character.intelligence gte 7>>
  [[Ask about the amulet|NODE-003-IntelligenceEnding]]
<</if>>

[[Ask for her blessing|NODE-003-DefaultEnding]]
```

---

## Questions?

See the main `speckit-preset-game-narrative-writing` README for:
- Full setup instructions
- How to use `speckit outline` and `speckit implement`
- Exporting to Ink, Ren'Py, or other engines
- Testing with Playwright automation
