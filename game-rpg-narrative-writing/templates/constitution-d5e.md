---
title: "[CAMPAIGN_NAME]"
template: "d5e"
author_name: "[AUTHOR_NAME]"
studio_name: "[STUDIO_NAME]"
language: "en"
tone: "dramatic-urgent"
copyright: "[YEAR] [STUDIO_NAME]. All rights reserved."
dramatic_question: "[DRAMATIC_QUESTION]"
genre: "fantasy-adventure"
narrative_mode: "branching"
style_mode: "humanized-ai"
prose_profile: "dialogue-heavy"
game_system: "D&D 5e"
campaign_type: "[CAMPAIGN_TYPE]"
party_level_range: "[LEVEL_START]-[LEVEL_END]"
session_count: "[SESSION_COUNT]"
estimated_playtime: "[PLAYTIME_HOURS] hours"
export_engines:
  - ink
  - sugarcube
player_perspective: "third-person"
pov_variable: "party_perspective"
target_audience: "adult"
series_position: "standalone"
game_bible_version: "1.0"
---

<!-- TEMPLATE: d5e (D&D 5e Campaign) -->
<!-- Generated: [CREATION_DATE] -->
<!-- Sync Impact: New project initialization from d5e template -->

# [CAMPAIGN_NAME] — D&D 5e Campaign Bible

This governing document configures the entire campaign. All nodes, NPCs, encounters, and narrative choices reference this constitution.

---

## Campaign Overview

**Campaign Name:** [CAMPAIGN_NAME]  
**Game System:** D&D 5e  
**Campaign Type:** [CAMPAIGN_TYPE] (Political Intrigue | Exploration | Combat-Heavy | Mystery | Custom)  
**Party Level Range:** [LEVEL_START] to [LEVEL_END]  
**Sessions:** [SESSION_COUNT]  
**Estimated Playtime:** [PLAYTIME_HOURS] hours  
**Tone:** [TONE]

---

## Campaign Themes (Rule-Set Specific)

### D&D 5e Recommended Campaign Themes

D&D 5e emphasizes **combat encounters, skill checks, and dungeon crawling**. Choose a theme that fits your party's interests:

| Theme | Focus | Key Mechanics | NPC Types | Encounter Mix | Example Goals |
|---|---|---|---|---|---|
| **Dungeon Delving** | Exploration + Combat | Room exploration, trap solving, monster combat | Dungeon masters, treasure hoarders | 60% combat, 30% exploration, 10% social | Retrieve artifact, clear dungeon, rescue prisoner |
| **Monster Hunt** | Combat + Investigation | Tracking, creature knowledge, confrontation | Hunters, rangers, beast experts | 50% combat, 30% investigation, 20% social | Slay creature, collect bounty, protect settlement |
| **Political Intrigue** | Social + Investigation | Persuasion, deception, faction rep | Noble houses, merchants, spies | 30% combat, 50% social, 20% exploration | Uncover conspiracy, broker power, prevent betrayal |
| **Heist** | Planning + Social + Combat | Stealth, deception, infiltration | Criminal masterminds, guards, targets | 40% combat, 40% social/stealth, 20% exploration | Steal artifact, liberate prisoner, expose secrets |
| **Investigation** | Social + Investigation + Combat | Clues, skill checks, interrogation | Witnesses, suspects, allies | 20% combat, 60% investigation, 20% social | Solve murder, uncover conspiracy, find culprit |
| **Curse Breaking** | Exploration + Combat + Magic | Arcane knowledge, magic item use, ritual | Sages, mages, cursed NPCs | 40% combat, 40% exploration, 20% social | Lift curse, free victims, stop magical threat |
| **Defense** | Combat + Community | Fortification, waves of enemies, morale | Allies, soldiers, refugees | 70% combat, 20% community management, 10% strategy | Defend settlement, survive siege, rally troops |
| **Mixed/Open-Ended** | All equal | Everything available | All types mixed | 30% combat, 30% social, 30% exploration, 10% custom | Player-directed goals |

### How Theme Affects Constitution

**By selecting a theme, you configure:**

1. **Encounter Balance**
   - Dungeon Delving: CR scaling emphasizes mob encounters (2-4 creatures per combat)
   - Heist: Stealth checks favored over direct combat; combat is high-risk
   - Investigation: Combat is reactive (enemies seek party out)

2. **NPC Types & Dialogue**
   - Political Intrigue: NPCs have conflicting loyalties, multiple dialogue options
   - Monster Hunt: NPCs speak about creature biology, tracking methods
   - Curse Breaking: NPCs speak about magic, rituals, mystical threats

3. **Skill Check Emphasis**
   - Combat-Heavy: Attack rolls, saving throws > social checks
   - Investigation: Insight, Investigation, Perception checks emphasized
   - Political Intrigue: Persuasion, Deception, Insight emphasized

4. **Mechanic Hooks Priority**
   - Dungeon Delving: VISITED (locations), INVENTORY (treasure), TIMER (dungeon collapses)
   - Political Intrigue: TRUST (NPC approval), COUNTER (faction rep), FLAG (conspiracy discovered)
   - Heist: INVENTORY (target items), TIMER (guard patrol), COUNTER (heist prep score)

5. **Ending Structure**
   - Combat-Heavy: Endings determined by defeated/alive enemies
   - Political Intrigue: Endings determined by faction standings
   - Investigation: Endings determined by conspiracy resolution method

---

### Campaign Themes Across Rule Sets

**Different game systems support different themes:**

| Theme | D&D 5e | PBTA | FATE | Blades in Dark |
|---|---|---|---|---|
| **Dungeon Delving** | ✅ (core) | ❌ (no dungeons) | ✅ (Pulp Adventure) | ⚠️ (modified) |
| **Monster Hunt** | ✅ (ideal) | ✅ (ideal - Monster Hunter) | ✅ (Pulp) | ⚠️ (creatures as complications) |
| **Political Intrigue** | ✅ (good) | ✅ (good - Apocalypse World politics) | ✅ (ideal - investigative) | ✅ (faction politics) |
| **Heist** | ✅ (good) | ✅ (good - prep focused) | ✅ (good) | ✅ (ideal - core mechanic) |
| **Investigation** | ✅ (good) | ✅ (good - clue gathering) | ✅ (ideal - mystery focused) | ✅ (good - score design) |
| **Curse Breaking** | ✅ (good - magic focus) | ✅ (supernatural) | ⚠️ (modified) | ✅ (good) |
| **Defense** | ✅ (good) | ✅ (ideal - survival) | ✅ (epic warfare) | ❌ (incompatible) |
| **Romance/Relations** | ⚠️ (add-on) | ✅ (ideal - core) | ✅ (relationship arcs) | ✅ (good) |

**Legend:**
- ✅ Ideal for this system (mechanics deeply support theme)
- ⚠️ Possible but modified (requires house rules or adjustments)
- ❌ Incompatible with system design

---

### How to Use Campaign Themes in This Constitution

1. **Select theme** from D&D 5e table above
2. **Note the Encounter Mix** percentages
3. **Review key mechanics** affected
4. **Update sections:**
   - Section III (Encounters): Adjust CR mix
   - Section VI (Narrative Mechanics): Emphasize appropriate skill checks
   - Section VII-VIII (Companions/Factions): Adjust relationship importance
   - Section IX (Endings): Customize gates for theme
   - Section XII (Craft Rules): Add theme-specific rules

---

## I. Party Composition

### Player Characters (Party of [PARTY_SIZE])

```
Character Slot 1: [CLASS_1] (Primary Ability: [ABILITY])
  - Race: [RACE_1]
  - Background: [BACKGROUND_1]
  - Hit Points: [HP] at level [LEVEL_START]
  - Key Skills: [SKILLS]
  - Class Features: [FEATURES]

Character Slot 2: [CLASS_2] (Primary Ability: [ABILITY])
  - Race: [RACE_2]
  - Background: [BACKGROUND_2]
  - Hit Points: [HP] at level [LEVEL_START]
  - Key Skills: [SKILLS]
  - Class Features: [FEATURES]

Character Slot 3: [CLASS_3] (Primary Ability: [ABILITY])
  - Race: [RACE_3]
  - Background: [BACKGROUND_3]
  - Hit Points: [HP] at level [LEVEL_START]
  - Key Skills: [SKILLS]
  - Class Features: [FEATURES]

Character Slot 4: [CLASS_4] (Primary Ability: [ABILITY])
  - Race: [RACE_4]
  - Background: [BACKGROUND_4]
  - Hit Points: [HP] at level [LEVEL_START]
  - Key Skills: [SKILLS]
  - Class Features: [FEATURES]
```

### Party-Wide Mechanics

```
Party Level:           [LEVEL_START]
Proficiency Bonus:     +2 (scales +1 per 4 levels)
Party Hit Points:      [Total HP across party]
Party XP Pool:         0 (starts at session 1)
Party Gold:            [STARTING_GOLD] gp
Party Status Effects:  none (updated during combat)
```

---

## II. D&D 5e Ability & Skill System

### Ability Score Modifiers (Auto-calculated)

```
Strength (STR):        [SCORE] → [MOD]
Dexterity (DEX):       [SCORE] → [MOD]
Constitution (CON):    [SCORE] → [MOD]
Intelligence (INT):    [SCORE] → [MOD]
Wisdom (WIS):          [SCORE] → [MOD]
Charisma (CHA):        [SCORE] → [MOD]
```

### Skill Check Formula

```
Skill Check = d20 + Ability Modifier + (Proficiency Bonus if trained)

DC Scale (Difficulty Class):
  DC 5:   Very Easy      (open an unlocked door)
  DC 10:  Easy           (spot a hidden object)
  DC 12:  Medium         (persuade a skeptical guard)
  DC 15:  Hard           (intimidate a veteran soldier)
  DC 18:  Very Hard      (convince a devoted zealot)
  DC 20:  Nearly Impossible (move immovable object)

Advantage/Disadvantage:
  Advantage:      roll 2d20, take HIGHEST
  Disadvantage:   roll 2d20, take LOWEST
```

### Saving Throws

```
[CLASS_1] Saving Throws:  [ABILITY] +[MOD], [ABILITY] +[MOD]
[CLASS_2] Saving Throws:  [ABILITY] +[MOD], [ABILITY] +[MOD]
[CLASS_3] Saving Throws:  [ABILITY] +[MOD], [ABILITY] +[MOD]
[CLASS_4] Saving Throws:  [ABILITY] +[MOD], [ABILITY] +[MOD]
```

---

## III. Encounter System

### Encounter Difficulty by CR

```
CR 0–1:   Trivial    (25–75 XP)
CR 2–3:   Easy       (75–150 XP)
CR 4–5:   Medium     (150–300 XP)
CR 6–7:   Hard       (300–500 XP)
CR 8–9:   Very Hard  (500–1000 XP)
CR 10+:   Deadly     (1000+ XP)
```

### XP Awards (D&D 5e by CR)

```
CR 0:     10 XP
CR 1/8:   25 XP
CR 1/4:   50 XP
CR 1/2:   100 XP
CR 1:     200 XP
CR 2:     450 XP
CR 3:     700 XP
CR 4:     1,100 XP
CR 5:     1,800 XP
CR 6:     2,300 XP
CR 7:     2,900 XP
CR 8:     3,900 XP
```

### Level-Up Thresholds

```
Level 2:  300 XP
Level 3:  900 XP
Level 4:  2,700 XP
Level 5:  6,500 XP
Level 6:  14,000 XP
Level 7:  23,000 XP
Level 8:  34,000 XP
Level 9:  48,000 XP
Level 10: 64,000 XP
```

---

## IV. Monsters & Encounters

### Core Encounter Types

| Encounter Type | Purpose | Typical CR | XP Reward |
|---|---|---|---|
| [MONSTER_TYPE_1] | [PURPOSE] | [CR] | [XP] |
| [MONSTER_TYPE_2] | [PURPOSE] | [CR] | [XP] |
| [MONSTER_TYPE_3] | [PURPOSE] | [CR] | [XP] |

### Monster Stat Block Template

```
[MONSTER_NAME] (CR [N])
  Type: [humanoid/beast/undead/etc], [size], [alignment]
  AC: [AC]  |  HP: [HP]  |  Speed: [SPEED]
  
  Abilities: STR [SCORE] (+[MOD]), DEX [SCORE] (+[MOD]), CON [SCORE] (+[MOD]), 
             INT [SCORE] (+[MOD]), WIS [SCORE] (+[MOD]), CHA [SCORE] (+[MOD])
  
  Saving Throws: [SAVE] +[MOD], [SAVE] +[MOD]
  Skills: [SKILL] +[MOD], [SKILL] +[MOD]
  Senses: [SENSE] (passive Perception [N])
  
  Actions:
    - [ACTION_NAME]: +[BONUS] to hit, [DAMAGE] damage
    - [SPELL_NAME]: DC [DC] [SAVE] save, [EFFECT]
  
  Loot: [GOLD] gp, [ITEMS]
  
  Narrative Consequence:
    [if defeated] → [STORY_IMPACT]
    [if escaped] → [ALTERNATE_IMPACT]
```

---

## V. Loot & Treasure

### Loot Tables by CR

```
CR 1–2: 25–75 gp, maybe 1 common magic item
CR 3–4: 75–150 gp, 1 uncommon magic item
CR 5–6: 150–300 gp, 1 rare magic item
CR 7–8: 300–500 gp, 1–2 rare items
CR 9+:  500–2000 gp, 2–3 rare items
```

### Quest-Critical Items

| Item | Found In | Effect | Narrative Gate |
|---|---|---|---|
| [ITEM_NAME] | NODE-[N] | [EFFECT] | [GATE_CONDITION] |
| [ITEM_NAME] | NODE-[N] | [EFFECT] | [GATE_CONDITION] |

### Treasure Division

```
party_gold_pool = total_loot_gp
per_player_share = party_gold_pool / party_size

Magic Items:
  Party votes or DM awards based on character need/class relevance
```

---

## VI. Narrative Mechanics Integration

### Skill Checks in Dialogue (DC-Gated Choices)

```
Example Node Structure:

Guard: "What brings you to the gate?"

[if player_charisma > 10]
  * "I'm on official business."
    success_dc = 12
    [if charisma_check >= 12]
      ✓ Guard believes you
      reputation_change = +5
    [else]
      ✗ Guard remains suspicious
      combat_initiated = true

[if player_insight > 12]
  * "You seem troubled. What's wrong?"
    success_dc = 14
    [if insight_check >= 14]
      ✓ Guard confides in you
      information_gained = "conspiracy_hint"
    [else]
      ✗ Guard withdraws
      reputation_change = -5
```

### Combat → Dialogue Flow

```
Combat Encounter
  ↓
[if party_defeats_enemies]
  → Combat Ends
  → Award XP & Loot
  → Trigger Aftermath Node (e.g., NODE-045: Enemy Surrender/Interrogation)
  → Dialogue with skill checks determines consequences

[if party_defeats_enemies_with_mercy]
  → Defeated enemy becomes ally/information source
  → Different dialogue options available

[if party_retreats]
  → Combat Ends (Inconclusive)
  → Enemies may pursue
  → Reputation changes (cowardice or tactical retreat)
```

---

## VII. Companion System (Optional)

### Recruitable NPCs

```
[COMPANION_NAME_1]
  - Class: [CLASS]
  - Alignment: [ALIGNMENT]
  - Approval: -100 to +100
  - Romance Gate: +[N]
  - Leaves if: approval < -[N]
  - Ending Locked: "[ENDING_NAME]"
  - Combat Role: [ROLE]

[COMPANION_NAME_2]
  - Class: [CLASS]
  - Alignment: [ALIGNMENT]
  - Approval: -100 to +100
  - Romance Gate: +[N]
  - Leaves if: approval < -[N]
  - Ending Locked: "[ENDING_NAME]"
  - Combat Role: [ROLE]
```

### Companion Variables

```
[COMPANION_NAME]_approval:      current approval score (-100 to +100)
[COMPANION_NAME]_recruited:     boolean flag (true/false)
[COMPANION_NAME]_alive:         boolean flag (true/false)
[COMPANION_NAME]_in_party:      boolean flag (true/false)
```

---

## VIII. Faction System (Optional)

### Factions & Reputation

| Faction | Start Rep | Ending Gate | Conflict | Notes |
|---|---|---|---|---|
| [FACTION_1] | [N] | >[N] unlocks [ENDING] | [FACTION_2] | [NOTES] |
| [FACTION_2] | [N] | >[N] unlocks [ENDING] | [FACTION_1] | [NOTES] |
| [FACTION_3] | [N] | >[N] unlocks [ENDING] | none | [NOTES] |

### Reputation Tracking

```
faction_rep_start:        0 to +100 range
faction_rep_change:       +/-5 to +/-25 per encounter
faction_rep_ending_gate:  >50, >70, etc. to unlock specific endings

Example:
  guard_rep = 0 (neutral)
  guard_rep += 20 (party protects town guard)
  guard_rep += 10 (party returns stolen goods to guard captain)
  guard_rep = 30 (enough for "Allied" status dialogue)
```

---

## IX. Ending Conditions

### Multiple Endings

| Ending Name | Requirements | Companions | Factions | Conditions |
|---|---|---|---|---|
| [ENDING_1] | [REQ_1] | [COMP] | [FACS] | [CONDS] |
| [ENDING_2] | [REQ_2] | [COMP] | [FACS] | [CONDS] |
| [ENDING_3] | [REQ_3] | [COMP] | [FACS] | [CONDS] |

---

## X. Campaign Variables

### Ability Scores (Immutable)

```
barbarian_str:         [N]
barbarian_dex:         [N]
barbarian_con:         [N]
rogue_dex:             [N]
rogue_int:             [N]
cleric_wis:            [N]
wizard_int:            [N]
```

### Combat State (Mutable During Encounters)

```
[CLASS_1]_hp:           current HP
[CLASS_1]_status:       null | "unconscious" | "poisoned" | "paralyzed"
[CLASS_2]_hp:           current HP
[CLASS_2]_status:       null
... (for each party member)
```

### Treasure (Mutable)

```
party_gold:             0 gp (scales as campaign progresses)
party_copper:           0 cp
magic_items_acquired:   []
consumables:            []
```

### Spell Resources (Mutable)

```
[SPELLCASTER_1]_spell_slots_1st:    [N]
[SPELLCASTER_1]_spell_slots_2nd:    [N]
[SPELLCASTER_2]_spell_slots_1st:    [N]
```

### Plot Progression (Mutable)

```
[STORY_MILESTONE_1]:           false → true
[STORY_MILESTONE_2]:           false → true
[CONSPIRACY_DISCOVERED]:       false → true
[MAJOR_NPC]_status:            "alive" | "dead" | "ally" | "enemy"
```

---

## XI. Prose Profile

**Profile:** dialogue-heavy

<!-- D&D campaigns are dialogue-driven:
     - NPCs voice their motivations and secrets
     - Skill checks trigger spoken outcomes
     - Combat is narrated through action descriptions
     - World-building is minimal (assumed setting knowledge)
-->

---

## XII. Craft Rules for D&D

### Universal Node Rules (D&D Campaign)

| Rule ID | Rule | Scope |
|---|---|---|
| NR-001 | Every non-combat node must offer at least 2 skill check options (or combat) | per node |
| NR-002 | Skill check DCs must be transparent to players ("This seems like a DC 15 Persuasion check") | per node |
| NR-003 | No illusory choices — each dialogue option must have a distinct mechanical or narrative outcome | per node |
| NR-004 | Companion reactions must reference their approval state explicitly | per node |
| NR-005 | Faction reputation changes must be announced ("City Guard approves +5") | per node |
| NR-006 | Combat rewards must be explicit (XP, loot, reputation) | per encounter |
| NR-007 | All endings must show which companions survived and which factions favor the party | per ending |

### NPC Voice Rules (D&D)

| Rule ID | Rule | Scope |
|---|---|---|
| VR-001 | NPCs must have distinct speaking patterns (formal, casual, arcane, colloquial) | per NPC |
| VR-002 | Antagonists must have believable motivations (not pure evil) | per NPC |
| VR-003 | Companion dialogue must reflect current approval state (cold, neutral, warm) | per companion |
| VR-004 | No fourth-wall breaks ("this is a game mechanic") | per node |

---

## XIII. Content & Sensitivity Policy

| Category | Level | Notes |
|---|---|---|
| Target Audience | [TARGET_AUDIENCE] | adult / new-adult / young-adult |
| Violence | moderate | Combat, creature deaths, betrayal |
| Death Mechanics | [DEATH_RULE] | permanent / resurrection available / checkpoint |
| Horror Content | mild | Undead enemies, eerie locations |
| Sexual Content | fade-to-black | Companion romance options fade to black |
| Reader Advisory | [WARNINGS] | list content warnings for players |

---

## XIV. Export Configuration

| Parameter | Value |
|---|---|
| Export Engines | Ink, SugarCube |
| Format | `.ink` (Ink), `.twee` (SugarCube) |
| Mechanic Hooks | flag, counter, trust, npc_state, ending_condition, currency |
| Prose Style | third-person past tense, dialogue-heavy |
| POV | Party perspective (rotating) |

---

## XV. Bible Version & Sync

| Field | Value |
|---|---|
| Template | d5e (D&D 5e Campaign) |
| Version | 1.0 |
| Created | [CREATION_DATE] |
| Last Updated | [CREATION_DATE] |
| Ratified | [NEEDS CLARIFICATION] |

---

## XVI. Quick Reference Checklist

Before starting campaign design:

- [ ] Party composition defined (classes, races, backgrounds)
- [ ] Starting level & XP pool set
- [ ] Campaign tone & dramatic question clarified
- [ ] Main antagonist(s) defined
- [ ] 2–3 factions identified
- [ ] 1–3 recruitable companions sketched
- [ ] 3–5 planned endings outlined
- [ ] Loot tables customized by campaign region
- [ ] Skill check DCs calibrated for party level
- [ ] Session count & playtime estimated
- [ ] Companion approval mechanics agreed upon
- [ ] Faction reputation starting positions set

**Start designing nodes once this checklist is complete.**

---

## Usage with Spec Kit

```bash
# After constitution is ratified:
speckit.plan                          # Create campaign acts & plot structure
speckit.outline --all                 # Generate node outlines with skill checks
speckit.implement --all               # Draft node prose with NPC dialogue
speckit.checklist                     # Validate node structure
speckit.consequences                  # Verify choice branching & reputation changes
speckit.continuity                    # Check cross-branch consistency
speckit.compile --engine ink          # Export to Ink for Unity
```
