---
title: [GAME_TITLE]
author_name: [AUTHOR_NAME]
studio_name: [STUDIO_NAME]
language: [LANGUAGE]
tone: [TONE]
copyright: [COPYRIGHT]
dramatic_question: [DRAMATIC_QUESTION]
genre: [GENRE]
narrative_mode: [NARRATIVE_MODE]
style_mode: [STYLE_MODE]
prose_profile: [PROSE_PROFILE]
# STYLE_MODE: author-sample | humanized-ai
# PROSE_PROFILE: dialogue-heavy | environmental | action-forward | atmospheric | minimalist
export_engines:
  - generic
  - sugarcube
# 'generic' outputs annotated Markdown with hook blocks.
# Specify one or more engines to produce during implementation.
player_perspective: [PLAYER_PERSPECTIVE]
pov_variable: [POV_VARIABLE]
target_audience: [TARGET_AUDIENCE]
series_position: [standalone]
game_bible_version: [GAME_BIBLE_VERSION]
# RPG RULESET CONFIGURATION
ruleset: [RULESET]
# RULESET: D&D 5e | Pathfinder 2e | Shadowrun 6e | Generic
platform: [PLATFORM]
# PLATFORM: Tabletop | Computer Game
game_system: [GAME_SYSTEM]
campaign_type: [CAMPAIGN_TYPE]
# CAMPAIGN_TYPE: Political Intrigue | Exploration | Combat-Heavy | Mystery | Heist | Custom
party_level_range: [LEVEL_START]-[LEVEL_END]
session_count: [SESSION_COUNT]
estimated_playtime: [PLAYTIME_HOURS] hours
# RPG MAP CONFIGURATION (if applicable)
map_format: [json | hex | asset | none]
map_scale: [5ft | 10ft | custom]
player_maps_needed: [true | false]
map_directory: specs/maps/
---

<!-- SYNC IMPACT: (populated by speckit.constitution on each update)
     Format: v[OLD] → v[NEW] | Changed: [summary] | Affected: [files] | Action required: [action] -->

# [GAME_TITLE] Game Bible
<!-- Your game's governing document. This overrides all writing prompts and templates. -->

---

## Campaign Overview
<!-- Populated by speckit.constitution from spec.md and user prompts.
     For non-RPG or generic projects, leave ruleset-specific fields as [N/A]. -->

**Campaign Name:** [GAME_TITLE]
**Game System:** [GAME_SYSTEM]
**Ruleset:** [RULESET]
**Platform:** [PLATFORM]
**Campaign Type:** [CAMPAIGN_TYPE]
**Party Level Range:** [LEVEL_START] to [LEVEL_END]
**Sessions:** [SESSION_COUNT]
**Estimated Playtime:** [PLAYTIME_HOURS] hours
**Tone:** [TONE]
**Dramatic Question:** [DRAMATIC_QUESTION]

---

## Style Mode

**[STYLE_MODE]**
<!-- Set to ONE of the following values:
     - author-sample   → Your own representative game passage defines the voice (Section I-A)
     - humanized-ai    → Use the Humanized AI Prose principles (Section I-B)
     Set this first. The AI will use whichever section matches your choice
     and treat the other as inactive reference material. -->

---

<!-- ═══════════════════════════════════════════════════════════════════
     MODE A: AUTHOR VOICE SAMPLE
     Paste 500–2000 words from a key scene that represents
     the exact voice, rhythm, NPC dialogue style and description
     you want for this game.
     The AI will use this text as the authoritative style reference
     and extract the markers below from it.
     ═══════════════════════════════════════════════════════════════════ -->

## I-A. Author Voice Sample
<!-- ACTIVE when STYLE_MODE: author-sample | Ignored otherwise -->

[AUTHOR_VOICE_SAMPLE]
<!-- Paste your reference text here. Guidelines:
     - Minimum 500 words for reliable style extraction
     - Choose a passage that contains both NPC dialogue AND narration
     - Include at least one moment of emotional or narrative intensity
     - This text defines: sentence rhythm, vocabulary register,
       POV distance, dialogue style, description density, and tone
     The AI will populate the Extracted Style Markers below
     when running speckit.constitution for the first time. -->

### Extracted Style Markers
<!-- Populated automatically by speckit.constitution from your sample.
     Override manually if the inference is wrong. -->

| Marker | Extracted Value |
|---|---|
| POV & Distance | [NEEDS CLARIFICATION] |
| Tense | [NEEDS CLARIFICATION] |
| Sentence rhythm | [NEEDS CLARIFICATION] |
| Vocabulary register | [NEEDS CLARIFICATION] |
| Dialogue style | [NEEDS CLARIFICATION] |
| Description density | [NEEDS CLARIFICATION] |
| Tone | [NEEDS CLARIFICATION] |
| Anti-patterns to avoid | [NEEDS CLARIFICATION] |

---

<!-- ═══════════════════════════════════════════════════════════════════
     MODE B: HUMANIZED AI PROSE PRINCIPLES
     A detailed craft ruleset for engaging game writing that
     avoids AI clichés, achieves psychological depth in dialogue,
     and maintains consistent NPC characterization.
     ═══════════════════════════════════════════════════════════════════ -->

## I-B. Mission
<!-- ACTIVE when STYLE_MODE: humanized-ai | Ignored otherwise -->

[STORY_MISSION]
<!-- State the core creative intent for this game. Example:
     "Create an immersive branching narrative that avoids AI clichés,
     delivers distinct NPC voices, emphasizes player agency consequences,
     and maintains consistent world logic." -->

---

## I-C. Prose Profile
<!-- ACTIVE when STYLE_MODE: humanized-ai | Ignored otherwise
     The Prose Profile tunes HOW the universal craft principles are weighted.
     It does not override or relax any universal rule — NPC Voice Integrity,
     Dialogue Subtext, and Anti-AI Filter apply in all profiles.

     Set to ONE of the following values:
       dialogue-heavy    → NPC banter dominates; environmental description is sparse
       environmental     → world-building and descriptions are equal weight with dialogue
       action-forward    → choices drive pacing; description is functional, sparse
       atmospheric       → setting and mood establish tone; dialogue is sparse and loaded
       minimalist        → bare-bones prose; every word earns its place

     Full profile definitions and all craft rules (Sections II–VI) live in
     `.specify/memory/craft-rules.md`, generated by speckit.constitution.
     Commands that draft or evaluate prose load craft-rules.md directly. -->

**[PROSE_PROFILE]**

---

## II. NPC Voice & Dialogue
<!-- Full rules in `.specify/memory/craft-rules.md §II`.
     Loaded by: speckit.implement, speckit.checklist. -->

---

## III. Description & World Coherence
<!-- Full rules in `.specify/memory/craft-rules.md §III`.
     Loaded by: speckit.implement, speckit.checklist. -->

---

## IV. Choice Integrity & Consequence
<!-- Full rules in `.specify/memory/craft-rules.md §IV`.
     Loaded by: speckit.implement, speckit.checklist. -->

---

## V. Scene Integrity
<!-- Full rules in `.specify/memory/craft-rules.md §V`.
     Loaded by: speckit.implement, speckit.checklist. -->

---

## IX. Map Configuration
<!-- Configure map format, scale, and requirements for this campaign -->

### Map Settings

```yaml
map_format: [json]        # json | hex-grid | asset-layer | none
map_scale: [5ft]          # 5ft (D&D default) | 10ft | custom
player_maps_needed: true  # Generate player-facing simplified maps?
map_directory: specs/maps # Where maps are stored
```

**Map Inventory by Type**:

| Type | Purpose | Session(s) | Status |
|------|---------|-----------|--------|
| Regional Map | Campaign travel, exploration | S1–S10 | [TBD] |
| Battle Map 1 | [ENCOUNTER_NAME] | S3 | [TBD] |
| Battle Map 2 | [ENCOUNTER_NAME] | S5–S6 | [TBD] |
| Location Map | [LOCATION_NAME] | S4 | [TBD] |
| Player Handout | Simplified travel map | S1 | [TBD] |

**JSON Map File Structure** (per map):

```json
{
  "name": "Battle Map - Goblin Hideout",
  "type": "battle",
  "session": 3,
  "scale": "5ft",
  "width": 20,
  "height": 20,
  "tiles": [
    {"x": 0, "y": 0, "type": "grass", "difficulty": 0},
    {"x": 10, "y": 10, "type": "tree", "difficulty": 2, "occupies": "1x1"}
  ],
  "tokens": [
    {"id": "goblin-1", "name": "Goblin Scout", "x": 5, "y": 5, "cr": "1/8"}
  ],
  "encounters": ["ENC-015"],
  "lighting": "daylight",
  "music_track": "combat-tense.ogg",
  "notes": "Secret door at (8, 12), requires DC 15 Perception"
}
```

---

## I. Export Configuration

| Parameter | Value |
|---|---|
| Export Engines | [EXPORT_ENGINES] |
| Narrative Mode | [NARRATIVE_MODE] |
| Player Perspective | [PLAYER_PERSPECTIVE] |
| POV Variable | [POV_VARIABLE] |
| Language | [LANGUAGE] |
| Tone | [TONE] |
| Studio / Author | [STUDIO_NAME] / [AUTHOR_NAME] |

<!-- EXPORT_ENGINES: List of engines to produce during implementation
     Example: [generic, sugarcube] will produce both .md and .twee files
     PLAYER_PERSPECTIVE: second-person | third-person | first-person | switching
     POV_VARIABLE: name of the variable used when switching (e.g. $pov) — leave blank if not switching -->

---

## II. Active Mechanics

<!-- List all mechanic hooks used in this project.
     Hooks not declared here will trigger a validation error in speckit.checklist.
     Tier 1 hooks are fully exported. Tier 2 hooks export with a warning comment. -->

### Tier 1 Hooks (v1.0 — fully exported)

| Hook | Enabled | Notes |
|---|---|---|
| `flag` | [yes/no] | |
| `counter` | [yes/no] | |
| `visited` | [yes/no] | |
| `inventory` | [yes/no] | |
| `timer` | [yes/no] | |
| `trust` | [yes/no] | |
| `currency` | [yes/no] | |
| `npc_state` | [yes/no] | |
| `ending_condition` | [yes/no] | |

### Tier 2 Hooks (v1.x — stubs, export with warning)

| Hook | Enabled | Notes |
|---|---|---|
| `knowledge` | [yes/no] | |
| `faction` | [yes/no] | |
| `location_state` | [yes/no] | |
| `object_state` | [yes/no] | |
| `choice_memory` | [yes/no] | |
| `clue` | [yes/no] | |


| Hook | Enabled | Notes |
|---|---|---|
| `verb` | [yes/no] | Examine/Interact/Talk modes |
| `move` | [yes/no] | Character navigation/walking |
| `hotspot` | [yes/no] | UI visibility tracking |
| `audio` | [yes/no] | Scripted SFX triggers |
| `inventory_combine` | [yes/no] | Item crafting/merging |
| `gated_choice` | [yes/no] | Timed decisions |

---

## III. Inventory Configuration
<!-- Only fill when Hook: inventory is enabled -->

```yaml
inventory:
  type: array          # array | slots
  capacity: [N]        # max items; 0 = unlimited
  persistence: save    # save | session (session = resets on load)
  weight_system: false # true = items have weight values in glossary.md
```

---

## IV. Timer Configuration
<!-- Only fill when Hook: timer is enabled -->

```yaml
timer:
  type: turns          # turns | countdown
  unit: turns          # turns | seconds (seconds: Sugarcube JS only)
  failure_node: [NODE_ID]   # node reached when timer expires
  warning_threshold: [N]    # turns remaining when warning fires
```

---

## V. Attribute Configuration
<!-- Fill for RPG-style numeric attributes tracked as counters or trust hooks -->

| Attribute | Variable Name | Range | Default | Hook Type |
|---|---|---|---|---|
| [NAME] | [VAR_NAME] | [MIN–MAX] | [DEFAULT] | counter / trust |
| [NAME] | [VAR_NAME] | [MIN–MAX] | [DEFAULT] | counter / trust |

---

## VI. Currency Configuration
<!-- Only fill when Hook: currency is enabled -->

```yaml
currency:
  name: [CURRENCY_NAME]   # e.g. gold, credits, favors
  variable: [VAR_NAME]    # e.g. $gold
  starting_amount: [N]
  minimum: 0              # can go negative? set to -999 if yes
```

---

## VI-B. Randomness & Economy Model
<!-- Configured by speckit.constitution. Read by speckit.compile, speckit.implement,
     and speckit.checklist to validate loot, enemy, and container authoring.
     All fields have defaults — only override when the project departs from them. -->

```yaml
randomness_model:

  # ── Loot drops ────────────────────────────────────────────────────────────
  # How item drops from enemies and containers are resolved at runtime.
  #
  #   fixed         — every item in a container's pool is always granted (weight ignored).
  #                   Use for handcrafted narrative loot (key items, story rewards).
  #   weighted      — each item has an independent % chance (weight 1–100).
  #                   Default model for combat drops and explorable containers.
  #   d100_table    — one roll picks a row from an ordered CR/tier table.
  #                   Use when you want classic TTRPG-style "roll on the treasure table" feel.
  #
  loot_model: weighted          # fixed | weighted | d100_table

  # ── Gold scale ────────────────────────────────────────────────────────────
  # Multiplier applied to the baseline CR→gold range in the Loot & Treasure table.
  # 1.0 = default 5e table values. 0.5 = half gold (grittier). 2.0 = generous.
  gold_scale: 1.0

  # ── Currency tiers ────────────────────────────────────────────────────────
  # Which denominations are active. Inactive tiers are not tracked as variables.
  # speckit.compile only emits StoryInit lines for active tiers.
  currency_tiers:
    copper: false               # 1 cp = 0.01 gp
    silver: false               # 1 sp = 0.1 gp
    gold: true                  # primary currency
    platinum: false             # 1 pp = 10 gp

  # ── Enemy spawns ──────────────────────────────────────────────────────────
  # Whether enemy groups in combat encounters are fixed or can vary in count.
  #
  #   scripted      — exact enemy list is always set by the author in the node.
  #   variant_range — author declares min/max; runtime picks count in that range.
  #                   Format in node: <<set $combat_enemies to _spawnGroup("goblin_patrol", 2, 4)>>
  #                   _spawnGroup is emitted by speckit.compile from the encounter definition.
  #
  enemy_spawn_model: scripted   # scripted | variant_range

  # ── Container respawn ─────────────────────────────────────────────────────
  # When (if ever) a looted container refills. Applies to <<lootContainer>> containers.
  # "never" is strongly recommended for story-driven games to preserve consequence.
  #
  #   never         — $loot_opened_[id] stays true forever. Container shows "Empty."
  #   long_rest     — container refills after the party takes a long rest
  #                   ($rest_count increments; speckit.compile emits the reset hook).
  #   in_game_day   — refills each new in-game day ($day_counter changes).
  #
  container_respawn: never      # never | long_rest | in_game_day

  # ── Quest rewards ─────────────────────────────────────────────────────────
  # Whether quest completion payouts (XP, gold, items) are fixed or scaled.
  #
  #   fixed         — reward values are authored verbatim in quests-template.md.
  #   level_scaled  — base reward × (party_level / design_level) clamped to [0.5, 2.0].
  #                   Useful for open-world games where quest order varies.
  #
  quest_reward_model: fixed     # fixed | level_scaled

  # ── Quest availability ────────────────────────────────────────────────────
  # Whether optional/side quests all appear in every playthrough or are culled.
  #
  #   all           — all quests declared in quests-template.md are always available
  #                   (subject to their own trigger conditions).
  #   random_pool   — side/optional quests are drawn from a pool each playthrough.
  #                   Set pool_size to how many are offered per act.
  #                   speckit.compile emits a StoryInit pool-draw block.
  #   faction_gated — only quests whose faction matches the player's highest-rep
  #                   faction at quest-unlock time are shown (no random element).
  #
  quest_availability: all       # all | random_pool | faction_gated
  quest_pool_size: 3            # used only when quest_availability: random_pool
                                # number of side quests drawn per act

  # ── World map travel encounters ───────────────────────────────────────────
  # Whether moving between Areas/Regions on the world map can trigger random events.
  #
  #   none          — travel is always safe; only scripted travel scenes fire.
  #   encounter_table — each travel link may trigger an encounter drawn from a
  #                     per-region table (see world-map.md ## Travel Encounter Tables).
  #                     Roll: d20 + $region_[name]_danger vs. encounter_dc.
  #                     speckit.compile emits the <<travelRoll>> call in travel nodes.
  #   scripted_only — same as none but makes the intent explicit.
  #
  travel_encounters: none       # none | encounter_table | scripted_only
  travel_encounter_dc: 12       # DC for d20+danger roll; used only when encounter_table

  # ── World map fog of war ──────────────────────────────────────────────────
  # Whether Locations on the world map are hidden until the player discovers them.
  #
  #   none          — all Locations visible from the start (classic hub map).
  #   visited       — Location appears on map only after the player has been there.
  #   region_unlock — Location appears when its parent Region is unlocked
  #                   (via <<regionUnlock>> from sugarcube-spatial-init-template.twee).
  #
  world_map_fog: none           # none | visited | region_unlock
```

> **speckit.compile reads this block** to:
> - Set `loot_model` on the generated `$loot_table_registry` comment header
> - Emit `StoryInit` lines only for active `currency_tiers`
> - Emit `_spawnGroup()` JS helper when `enemy_spawn_model: variant_range`
> - Emit `$rest_count` / `$day_counter` reset hooks when `container_respawn` is not `never`
> - Apply `gold_scale` multiplier when populating container `gold_min` / `gold_max` from CR tables
> - Emit a `$quest_pool` StoryInit draw block when `quest_availability: random_pool`
> - Emit `<<travelRoll>>` calls in travel nodes when `travel_encounters: encounter_table`
> - Set `<<wmLoc>>` widget visibility mode in `sugarcube-world-map-template.twee` based on `world_map_fog`
>
> **speckit.checklist validates**:
> - `loot_model: fixed` → warns if any item in a loot table has weight < 100
> - `enemy_spawn_model: scripted` → CRITICAL if a combat node has no `$combat_enemies` set
> - `container_respawn: never` → warns if a node resets `$loot_opened_*` manually

---

## VII. Prose Style Mode

<!-- Configured by speckit.constitution. Referenced by speckit.implement and speckit.checklist
     for voice consistency validation. Do not edit manually after ratification without
     running speckit.constitution --update. -->

| Field | Value |
|---|---|
| Style mode | [author-sample / humanized-ai] |
| Tense | [past / present] |
| Sentence rhythm | [short-punchy / varied / long-flowing] |
| Vocabulary register | [plain / literary / technical / colloquial] |
| Sensory density | [low / medium / high] |
| Dialogue style | [direct / oblique / subtext-heavy] |
| Anti-AI filter active | [yes / no] |

**Extracted voice markers** *(author-sample mode only — leave blank for humanized-ai)*:
- Signature constructions: [e.g. sentence fragments for tension, em-dash for interruption]
- Recurring imagery patterns: [e.g. light/dark, industrial, organic]
- Words/phrases to avoid: [extracted from sample]
- Sample sentence rhythm: [e.g. "Short declarative. Then longer clause that opens out into something uncertain."]

---

## VIII. Craft Rules

### Universal Node Rules

These rules apply to every node regardless of engine target.

| Rule ID | Rule | Scope |
|---|---|---|
| NR-001 | Every non-terminal node must offer at least 2 meaningful choices | per node |
| NR-002 | Choices must differ in consequence, not just phrasing | per node |
| NR-003 | No choice may be obviously dominant — all options must have narrative cost | per node |
| NR-004 | Dead ends (no outgoing choices, not an ending node) are a validation error | per node |
| NR-005 | Every mechanic hook must be declared in variables.md before use | per project |
| NR-006 | Variables must be set before they are read (no read-before-set) | per branch |
| NR-007 | Ending nodes must be registered in endings.md | per project |
| NR-008 | Prose must cohere without hook blocks (hooks are annotations, not load-bearing) | per node |

### Prose Style Rules

| Rule ID | Rule | Scope |
|---|---|---|
| PR-001 | Player perspective declared in Section I must be consistent across all nodes | per project |
| PR-002 | No on-the-nose emotional labelling ("you feel sad") — show through action/sensation | per node |
| PR-003 | Opening line of each node must orient player: where, who, what is at stake | per node |
| PR-004 | Choice labels must be written in the same person as the node prose | per node |
| PR-005 | Prohibited phrases list (Section VIII) applies to all prose and choice labels | per node |

### Project-Specific Craft Rules

<!-- 3–5 rules unique to this game's voice and design, generated by speckit.constitution.
     Examples: dialogue line length cap, bark line format, cutscene tense convention. -->

| Rule ID | Rule | Scope |
|---|---|---|
| PSR-001 | [STORY_SPECIFIC_PRINCIPLES_1] | [per node / per project] |
| PSR-002 | [STORY_SPECIFIC_PRINCIPLES_2] | [per node / per project] |
| PSR-003 | [STORY_SPECIFIC_PRINCIPLES_3] | [per node / per project] |

### Author Rule Overrides

<!-- Document deliberate overrides here with rationale -->

| Rule ID | Override Rationale | Scope |
|---|---|---|
| | | |

---

## IX. Prohibited Phrases

<!-- Phrases that break the voice, betray AI origin, or violate craft rules.
     speckit.checklist and speckit.implement will flag these. -->

| Phrase / Pattern | Reason |
|---|---|
| "Suddenly" | Weak intensifier — let the action speak |
| "You can't help but feel" | Filter phrase — direct address only |
| "As if on cue" | Contrivance marker |
| [ADD PROJECT-SPECIFIC PHRASES] | |

---

## X. Content & Sensitivity Policy

| Category | Level | Notes |
|---|---|---|
| Target audience | [TARGET_AUDIENCE] | adult / new-adult / young-adult / teen / all-ages |
| Violence | [none / mild / moderate / graphic] | |
| Player character death | [permanent / checkpoint / impossible] | |
| Horror content | [none / mild / moderate / extreme] | |
| Sexual content | [none / fade-to-black / explicit] | |

---

## XI. Tooling

```

### Bible Version

| Field | Value |
|---|---|
| Version | 1.0 |
| Ratified | [DATE] |
| Last Updated | [DATE] |
| Updated By | [AUTHOR] |

---

## XII. Series Context
<!-- Populated by speckit.constitution when series_position is not standalone.
     Leave all fields as [TBD] if series-bible.md has not been created yet.
     Validated by speckit.series. -->

| Field | Value |
|---|---|
| Series Title | [SERIES_TITLE] |
| Series Position | [standalone / entry-N] |
| Series Arc Summary | [SERIES_ARC_SUMMARY] |
| Series Tone | [SERIES_TONE] |
| Series Genre | [SERIES_GENRE] |

### Carry-Over Variables
<!-- Variables imported from the previous entry's save state.
     Validated against specs/series-bible.md ## Carry-Over Variable Registry. -->

| Variable | Source Entry | Default (new game+) | Notes |
|---|---|---|---|
| [VAR_NAME] | entry-[N] | [DEFAULT] | |

### Series Variance Log
<!-- Intentional deviations from series-wide defaults (tone, genre, POV, tense).
     Populated by speckit.constitution when a mismatch is detected. -->

| Field | Series Default | This Entry | Reason |
|---|---|---|---|
| | | | |

---

## XIII. D&D 5e Campaign Configuration
<!-- Populated by speckit.constitution when ruleset: D&D 5e.
     Leave blank or remove this section for other rulesets. -->

### Party Composition

```
Character Slot 1: [CLASS_1] (Primary Ability: [ABILITY])
  - Race: [RACE_1] | Background: [BACKGROUND_1]
  - Hit Points: [HP] at level [LEVEL_START] | Key Skills: [SKILLS]

Character Slot 2: [CLASS_2] (Primary Ability: [ABILITY])
  - Race: [RACE_2] | Background: [BACKGROUND_2]
  - Hit Points: [HP] at level [LEVEL_START] | Key Skills: [SKILLS]

Character Slot 3: [CLASS_3] (Primary Ability: [ABILITY])
  - Race: [RACE_3] | Background: [BACKGROUND_3]
  - Hit Points: [HP] at level [LEVEL_START] | Key Skills: [SKILLS]

Character Slot 4: [CLASS_4] (Primary Ability: [ABILITY])
  - Race: [RACE_4] | Background: [BACKGROUND_4]
  - Hit Points: [HP] at level [LEVEL_START] | Key Skills: [SKILLS]
```

**Party-Wide Mechanics**

```
Party Level:        [LEVEL_START]
Proficiency Bonus:  +2 (scales +1 per 4 levels)
Party Gold:         [STARTING_GOLD] gp
```

---

### D&D 5e Ability & Skill System

**Skill Check Formula**: `d20 + Ability Modifier + (Proficiency Bonus if trained)`

**DC Scale**: DC 5 Very Easy · DC 10 Easy · DC 12 Medium · DC 15 Hard · DC 18 Very Hard · DC 20 Nearly Impossible

**Advantage/Disadvantage**: roll 2d20, take highest (Advantage) or lowest (Disadvantage)

---

### Encounter System

| Difficulty | CR Range | XP Range |
|---|---|---|
| Trivial | CR 0–1 | 25–75 XP |
| Easy | CR 2–3 | 75–150 XP |
| Medium | CR 4–5 | 150–300 XP |
| Hard | CR 6–7 | 300–500 XP |
| Very Hard | CR 8–9 | 500–1000 XP |
| Deadly | CR 10+ | 1000+ XP |

**Level-Up Thresholds**: L2 300 XP · L3 900 XP · L4 2,700 XP · L5 6,500 XP · L6 14,000 XP · L7 23,000 XP · L8 34,000 XP

---

### Monsters & Encounters

| Encounter Type | Purpose | Typical CR | XP Reward |
|---|---|---|---|
| [MONSTER_TYPE_1] | [PURPOSE] | [CR] | [XP] |
| [MONSTER_TYPE_2] | [PURPOSE] | [CR] | [XP] |
| [MONSTER_TYPE_3] | [PURPOSE] | [CR] | [XP] |

**Monster Stat Block Template**

```
[MONSTER_NAME] (CR [N])
  Type: [humanoid/beast/undead/etc], [size], [alignment]
  AC: [AC]  |  HP: [HP]  |  Speed: [SPEED]
  Actions:
    - [ACTION_NAME]: +[BONUS] to hit, [DAMAGE] damage
  Loot: [GOLD] gp, [ITEMS]
  Narrative Consequence:
    [if defeated] → [STORY_IMPACT]
    [if escaped]  → [ALTERNATE_IMPACT]
```

---

### Loot & Treasure

| CR Range | Gold | Magic Items |
|---|---|---|
| CR 1–2 | 25–75 gp | 1 common |
| CR 3–4 | 75–150 gp | 1 uncommon |
| CR 5–6 | 150–300 gp | 1 rare |
| CR 7–8 | 300–500 gp | 1–2 rare |
| CR 9+ | 500–2000 gp | 2–3 rare |

**Quest-Critical Items**

| Item | Found In | Effect | Narrative Gate |
|---|---|---|---|
| [ITEM_NAME] | NODE-[N] | [EFFECT] | [GATE_CONDITION] |

---

### Companion System

```
[COMPANION_NAME]
  - Class: [CLASS] | Alignment: [ALIGNMENT]
  - Approval: -100 to +100
  - Romance Gate: +[N]  |  Leaves if: approval < -[N]
  - Ending Locked: "[ENDING_NAME]"  |  Combat Role: [ROLE]
```

**Companion Variables**: `[COMPANION]_approval`, `[COMPANION]_recruited`, `[COMPANION]_alive`, `[COMPANION]_in_party`

---

### Faction System

| Faction | Start Rep | Ending Gate | Conflict | Notes |
|---|---|---|---|---|
| [FACTION_1] | [N] | >[N] unlocks [ENDING] | [FACTION_2] | [NOTES] |
| [FACTION_2] | [N] | >[N] unlocks [ENDING] | [FACTION_1] | [NOTES] |

**Reputation Changes**: +/-5 to +/-25 per encounter. Announce changes to player ("City Guard approves +5").

---

### D&D 5e Craft Rules

| Rule ID | Rule | Scope |
|---|---|---|
| NR-D1 | Every non-combat node must offer at least 2 skill check options | per node |
| NR-D2 | Skill check DCs must be transparent to players | per node |
| NR-D3 | No illusory choices — each dialogue option must have a distinct outcome | per node |
| NR-D4 | Companion reactions must reference their approval state explicitly | per node |
| NR-D5 | Faction reputation changes must be announced when they occur | per node |
| NR-D6 | Combat rewards must be explicit (XP, loot, reputation) | per encounter |
| NR-D7 | All endings must show which companions survived and which factions are allied | per ending |

| Rule ID | NPC Voice Rule | Scope |
|---|---|---|
| VR-D1 | NPCs must have distinct speaking patterns (formal, casual, arcane, colloquial) | per NPC |
| VR-D2 | Antagonists must have believable motivations — not pure evil | per NPC |
| VR-D3 | Companion dialogue must reflect current approval state (cold, neutral, warm) | per companion |

---

### Quick Reference Checklist (D&D 5e)

Before starting campaign design:

- [ ] Party composition defined (classes, races, backgrounds, starting level)
- [ ] Campaign tone and dramatic question clarified
- [ ] Main antagonist(s) defined with motivations
- [ ] 2–3 factions identified with starting reputations
- [ ] 1–3 recruitable companions sketched with approval thresholds
- [ ] Ending conditions defined (variable requirements per ending)
- [ ] Export engine(s) confirmed (Ink, Sugarcube, generic)
