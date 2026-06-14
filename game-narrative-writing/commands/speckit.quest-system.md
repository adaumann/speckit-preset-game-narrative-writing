# Quest System Integration — Speckit Guide

This guide explains how to use the optional quest system in speckit's game-narrative-writing preset.

## Overview

When `quest: enabled` in your `constitution.md`, speckit's planning, outlining, and implementation commands generate a **location-based world structure** for organizing multi-stage narratives.

**Key principle**: Quests are optional spatial narratives. They organize nodes by location and stage, making it easier to design interconnected quest lines that players can revisit and explore non-linearly.

---

## When to Use Quests

Use the quest system when:
- ✅ Your game has **multiple locations** (shrine, tavern, guild, etc.)
- ✅ Players can **revisit locations** and encounter different scenes based on progress
- ✅ You have **multi-stage objectives** (talk to NPC → gather items → return → complete task)
- ✅ Different quests can happen **in the same location**

Don't use the quest system if:
- ❌ Your game is a **single linear path** (A → B → C → end)
- ❌ Scenes are **temporally ordered** but not spatially organized
- ❌ You don't need location revisits

---

## Workflow

### 1. Constitution: Enable Quests

In `specs/[FEATURE_DIR]/constitution.md`:

```yaml
enabled_mechanics:
  - quest: true

quest_system:
  tracking_style: stages          # stages | milestones | steps
  location_based: true             # Quests tied to locations?
  revisit_allowed: true            # Can player return after quest?
  failed_quests: false             # Can quests fail?
```

### 2. Plan: Generate World Structure

Run `speckit.plan` with quests enabled:

```bash
speckit.plan
```

This generates:
```
specs/[FEATURE_DIR]/world/
├── locations.md                  # Index of all locations
└── [location-name]/
    ├── passages.md               # Scenes at this location
    └── [quest-id]/
        └── overview.md           # Quest outline
```

**Output checklist**:
- ✓ `world/locations.md` created with all location entries
- ✓ `world/[location-name]/passages.md` created for each location
- ✓ `world/[location-name]/[quest-id]/overview.md` created for each quest
- ✓ Variables registered in `specs/variables.md` (e.g., `$quest_shrine_blessing_stage`)

### 3. Outline: Create Location-Based Outlines

For quest-based nodes, use the location structure:

**Option A**: Outline directly from location passages
```bash
speckit.outline quest-shrine-blessing
```

This creates outlines in `outlines/[NODE_ID].md` with location context pre-filled from `world/shrine/passages.md`.

**Option B**: Outline from `--all` (automatic)
```bash
speckit.outline --all
```

Speckit recognizes nodes that belong to quests and populates the **Quest Context** field automatically.

**Outline shows**:
- Opening condition (what must be true before this passage appears)
- Quest stage (which stage of the quest this node fulfills)
- Closing condition (what becomes true after node completes)

### 4. Implement: Draft Location Passages

When drafting quest nodes, prose should include:

**Opening**: Remind player of quest context
```markdown
You return to the Shrine for the second time. The Priestess is waiting.
```

**Closing**: Signal stage advancement
```markdown
[MECHANIC:COUNTER variable=quest_shrine_blessing_stage delta=+1]
The Priestess grants you her blessing. Your task here is complete.
```

**Choices**: Include quest gates as conditions
```markdown
- [Accept the blessing](END-A_Blessed) 
  <!-- requires: $character.wisdom >= 6; Effect: Receive blessing -->

- [Leave respectfully](END-B_Departed)
  <!-- Effect: Depart with priestess's thanks -->
```

---

## Data Structures

### Location Registry (world/locations.md)

```yaml
| Location ID | Name | Description | Acts | Passages | Quests |
|---|---|---|---|---|---|
| LOC-shrine | The Shrine | Ancient stone... | 1-2 | 3 | Seeking the Blessing (optional) |
```

Each location includes:
- Sensory anchors (visual, audio, smell, touch)
- Internal rules (time-of-day effects, revisit rules)
- Passage list (nodes at this location)
- Quest list (quests available here)

### Passages (world/[location]/passages.md)

```yaml
| Passage ID | Title | Quest | Stage | Opening Condition | Type |
|---|---|---|---|---|---|
| PASS-shrine-001 | Shrine Entrance | — | — | Always available | Intro |
| PASS-shrine-002 | Priestess Dialogue | Seeking the Blessing | 1 | First visit | Encounter |
```

Each passage shows:
- Which quest it belongs to (if any)
- Which stage (e.g., Stage 2 of 3)
- When it's available (opening condition)
- When it completes (closing condition)

### Quest Overview (world/[location]/[quest-id]/overview.md)

```yaml
Quest ID: quest-shrine-blessing
Quest Title: Seeking the Blessing
Location: shrine
Stage Count: 3
Completion Variable: $quest_shrine_blessing_complete
Completable: Yes (always solvable)
```

Each stage includes:
- Objective (what player does at this stage)
- Passage ID (which node fulfills this stage)
- Choices available
- Consequences (attribute changes, items gained, etc.)

---

## Common Patterns

### Multi-Stage Quest at One Location

```
world/shrine/
├── passages.md
│   ├ PASS-shrine-001: Intro (quest stage 1)
│   ├ PASS-shrine-002: Main (quest stage 2)
│   └ PASS-shrine-003: Resolution (quest stage 3)
└── quest-blessing/
    └── overview.md
        ├ Stage 1: Meet priestess
        ├ Stage 2: Choose dialogue path
        └ Stage 3: Receive blessing
```

### Multiple Quests at Same Location

```
world/tavern/
├── passages.md
│   ├ PASS-tavern-001: Entrance
│   ├ PASS-tavern-002: Bartender (QUEST-info-broker, stage 1)
│   ├ PASS-tavern-003: Patron (QUEST-seek-revenge, stage 1)
│   └ PASS-tavern-004: Bard (QUEST-find-song, stage 2)
├── quest-info-broker/
│   └── overview.md
├── quest-seek-revenge/
│   └── overview.md
└── quest-find-song/
    └── overview.md
```

### Revisit Pattern (quest_revisit_allowed: true)

```
world/shrine/passages.md:
PASS-shrine-002 (first visit):
  Opening: $quest_shrine_blessing_stage == 0
  Closing: $quest_shrine_blessing_stage = 1

PASS-shrine-002b (revisit, if wisdom improved):
  Opening: $quest_shrine_blessing_stage == 1 AND $character.wisdom > initial_wisdom
  Closing: $quest_shrine_blessing_stage = 2
  Description: "The priestess greets you again, noting your growth in wisdom"
```

---

## Variables Naming Convention

Quest-related variables follow this pattern:

```
$quest_[location]_[quest_id]_stage       # Integer (1, 2, 3, etc.)
$quest_[location]_[quest_id]_complete    # Boolean (true/false)
$quest_[location]_[quest_id]_[detail]    # Specific quest detail
```

**Examples**:
- `$quest_shrine_blessing_stage` — Current stage (1–3)
- `$quest_shrine_blessing_complete` — Is quest finished?
- `$quest_guild_contract_reward_claimed` — Did player claim reward?
- `$quest_tavern_revenge_target_found` — Was target found?

---

## Export & Compile

When exporting quests to SugarCube:

**SugarCube mechanics**:
- Track stage with `<<set $quest_id_stage to N>>`
- Gate passages with `<<if $quest_id_stage == N>>`
- Display location name: `<< = $location>>`
- Show passage availability based on conditions

**Example Twee**:
```javascript
:: Shrine-MainPassage
<< if $quest_shrine_blessing_stage == 1>>
  [First visit prose]
  <<link "Accept guidance" "Shrine-Stage2">><</link>>
<</if>>

<< if $quest_shrine_blessing_stage == 2>>
  [Second visit prose]
  <<set $quest_shrine_blessing_stage to 3>>
  <<link "Leave" "Shrine-End">><</link>>
<</if>>
```

---

## Shrine Sample Reference

The Shrine sample demonstrates this pattern:

- **One location**: The Shrine
- **One quest**: Seeking the Blessing (3 stages)
- **Three passages**: Entrance → Dialogue → Blessing
- **Multiple branches**: Ask / Donate / Search lead to same conclusion

See:
- `world/locations.md` — Location index
- `world/shrine/passages.md` — Available passages
- `world/shrine/quest-shrine-blessing/overview.md` — Quest outline

---

## Troubleshooting

**Q: When should I use quests vs. plain NODE-IDs?**

A: Use quests if nodes are location-based and revisitable. Use NODE-IDs if nodes are strictly linear.

**Q: Can I mix quest and non-quest nodes?**

A: Yes! Some nodes can be in the `world/` structure (quests), others in `outlines/` (linear). Both export correctly.

**Q: What if a quest happens across multiple locations?**

A: Create separate passage entries in each location. Link them with choices (choices can point across locations).

**Q: How do I prevent a player from returning to a quest location?**

A: Set `$quest_id_complete = true` and gate the passage with `<< if not $quest_id_complete >>`.

---

## Next Steps

1. **Enable quests** in `constitution.md`
2. **Run `speckit.plan`** to generate world structure
3. **Review `world/locations.md`** and update location descriptions
4. **Outline each passage** using `speckit.outline`
5. **Draft prose** with quest stage tracking using `speckit.implement`
6. **Export and test** in SugarCube with `speckit.export`
