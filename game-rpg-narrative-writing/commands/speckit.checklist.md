---
description: Run the quality checklist for one or more node files. Checks structural integrity, craft rules, hook declarations, choice design, and game bible compliance. "Unit tests for nodes." Saves a checklist file per node and produces a weighted PASS/FAIL verdict.
handoffs:
  - label: Fix Checklist Failures
    agent: speckit.revise
    prompt: Fix the failures flagged by the checklist for this node
    send: true
  - label: Run Continuity Check
    agent: speckit.continuity
    prompt: Per-node checks have passed � run a full continuity check now
    send: true
---

# speckit.checklist

**CRITICAL CONCEPT**: Node checklists are **quality gates for node files** � unit tests that validate whether a drafted node fulfils its structural and craft obligations.

**NOT for verifying story events**:
- ? NOT "Does this node match the plan?"
- ? NOT "Is the plot logical here?"

**FOR node quality validation**:
- ? "Are all choice targets valid node IDs?" (structural integrity)
- ? "Are all variables declared in variables.md?" (hook compliance)
- ? "Is prose coherent without hook blocks?" (craft)
- ? "Do choice labels avoid meta-language?" (player experience)
- ? "Are prohibited phrases absent?" (game bible compliance)

**Metaphor**: If your node is a unit of player experience, the checklist is its test suite � verifying the node works structurally, the prose works as prose, and the mechanic hooks work as intended.

## User Input

```text
$ARGUMENTS
```

You **MUST** consider the user input before proceeding (if not empty). Accepted arguments:
- A node ID (e.g. `NODE-003`) � run checklist for that node
- A list of node IDs � run checklist for each
- `--act [N]` � check all nodes in the specified act
- `--all` � check all nodes with status DRAFT or APPROVED
- `--strict` � also validate Tier 2 stub hooks for completeness
- Nothing � check the most recently modified node file

## Pre-Execution Checks

**Extract Platform & Ruleset** (auto-detect RPG context):
- Read `.specify/memory/constitution.md` YAML frontmatter and extract `[PLATFORM]` and `[RULESET]`
- If `[PLATFORM]` = "Tabletop": Set `SESSION.is_rpg = "tabletop"` and activate Tabletop RPG checks
- If `[PLATFORM]` = "Computer Game": Set `SESSION.is_rpg = "computer"` and activate Computer Game RPG checks
- If neither detected: Set `SESSION.is_rpg = false` (generic game checklist)
- Store `SESSION.platform` and `SESSION.ruleset` for conditional check selection

**Check for extension hooks (before checklist generation)**:
- Check if `.specify/extensions.yml` exists in the project root.
- If it exists, read it and look for entries under the `hooks.before_checklist` key.
- Process as standard hook block (Optional/Mandatory). Skip silently if absent.

---

## Execution Steps

### Step 1 � Setup

Run `{SCRIPT}` from repo root. Determine target node(s) from `$ARGUMENTS`.

For each target node:
- Confirm the node file exists in `nodes/`.
- Read the node file (YAML frontmatter + prose body).
- If the node has status SKIP, skip it and note in the report.

### Step 2 � Load Context

Load the following (required):
- `.specify/memory/constitution.md` – POV, tone, Prose Style Mode (Section VII), `style_mode`, `prose_profile`, **PLATFORM, RULESET**
- `.specify/memory/craft-rules.md` – craft rules (NR-NNN, PR-NNN per active prose profile), prohibited phrases, anti-AI clichés filter
- `specs/variables.md` – declared variable registry for NR-003 / NR-006
- `specs/mechanics.md` – valid hook types and syntax for MC checks

Load the following (if present):
- `specs/characters/` – NPC profiles for trust range and dialogue register checks (dialogue style per prose profile)
- `outlines/[NODE_ID].md` – node outline for outline-gate compliance check
- `specs/plan.md` – for upstream path analysis (NR-006)

**RPG-Specific Context** (if `SESSION.is_rpg = true`):
- `specs/mechanics-[ruleset].md` – skill DC ranges, approval thresholds, faction rep ranges, system-specific mechanics
- `specs/npc-roster.md` – companion profiles with approval ranges and class/level (if Tabletop)
- `specs/quests.md` – quest structure and session context (if Tabletop)
- `specs/locations.md` – location profiles with difficulty scaling notes (if Computer Game)
- `specs/bestiary.md` – enemy CR/difficulty profiles (if Tabletop)

**Tabletop-Only Context** (if `SESSION.is_rpg = "tabletop"`):
- `draft/campaign-guide.md` – verify campaign context exists (first-node check)
- `draft/SESSION-[N]/outlines/` – verify node is in correct session group

**Computer Game-Only Context** (if `SESSION.is_rpg = "computer"`):
- `specs/accessibility-features.md` – verify accessibility compliance (if present)

### Step 3 � Clarifying Questions (=2)

Ask at most 2 targeted questions if the node file or loaded context leaves a check ambiguous:
- Only ask what cannot be resolved from the files
- Focus on: intended trust state at this node, whether a specific prohibited phrase is intentional dialect, whether a Tier 2 stub is expected to remain unimplemented

Skip if the node and context provide enough information to run all checks without ambiguity.

### Step 4 � Run Checks

For each node, evaluate all items in the four sections below using `templates/checklist-template.md` as the output structure. Mark each item ? / ? / ??.

**NR � Node Rules** (structural integrity)
- NR-001: Non-terminal nodes have = 2 choices in `## Choices`
- NR-002: All choice targets are valid node IDs (exist in `outlines/` or `nodes/`)
- NR-003: All variables in `variables_read` and `variables_set` are declared in `variables.md`
- NR-004: All mechanic hook blocks use valid syntax and registered hook types (per `mechanics.md`)
- NR-005: Tier 2 hook stubs include `// TIER 2 STUB` comment
- NR-006: No variable is read that cannot be set on any upstream path leading to this node
- NR-007: Ending nodes have no outgoing choices
- NR-008: Trust score changes are within the declared NPC range (per `characters/` profile)
- NR-009: Choices use the export-required format: `- [Label](NODE_ID) <!-- condition -->` under `## Choices` heading

**PR � Prose Rules** (craft and voice)
- PR-001: POV is consistent with `constitution.md` `player_perspective` (or has an approved override)
- PR-002: No prohibited phrases from `constitution.md` appear in prose
- PR-003: Choice labels use active verb phrases and avoid meta-language (e.g. "Ask about the key" not "Select dialogue option")
- PR-004: Dialogue register matches NPC trust state at this node's variable value
- PR-005: Prose coheres without hook blocks (narrative reads as complete if mechanic blocks are removed)
- PR-006: At least one concrete sensory detail (sound, smell, texture, temperature � not visual only)
- PR-007: No choice or action is trivialized or telegraphed by the prose (player's decision space is respected)
- PR-008: Prose tense, sentence rhythm, and vocabulary register are consistent with Prose Style Mode (Section VII of `constitution.md`); anti-AI filter patterns are absent
- PR-009: Location atmosphere is established through sensory detail or description (from `specs/locations.md` Setting Anchors field if present)
- PR-010: Sensory details are consistent with the location or NPC context (e.g., a sterile facility has clinical smells/sounds, not organic ones)
- PR-011: Emotional subtext is shown through character reaction or environmental description, not explicitly named (e.g., "tension hung in the air" not "I felt tense")

**MC � Mechanic Compliance** (hook balance and fairness)
- MC-001: Every trust-shifting choice has narrative justification in prose
- MC-002: No single choice dominates trivially � all choices are meaningful trade-offs
- MC-003: Timer failure conditions are handled in a downstream node (or flagged as `[NEEDS NODE]`)
- MC-004: If `--strict`: Tier 2 stub hooks include a `// TODO:` comment describing expected implementation
- MC-005: No mechanic hook reads a variable not listed in `variables_read` in the frontmatter
- MC-006: Every `MECHANIC:CURRENCY` hook includes `variable=` and that variable is declared as `type: currency` in `variables.md`; flag missing or wrong-type declaration as CRITICAL

**GB � Game Bible Compliance** (spec authority)
- GB-001: Node tone is consistent with the genre and emotional register defined in `constitution.md`
- GB-002: Any NPC appearing in this node is consistent with their character profile (voice, state, goal)
- GB-003: World-rule constraints (from `world-building.md`) are not violated in prose or choice outcomes
- GB-004: Engine target constraints are respected (no unsupported syntax for the declared export target)

### SP – Spatial Integrity Checks *(skip if `specs/world-map.md` absent)*

- SP-001: Node frontmatter includes `parent_location: LOC-{ShortName}` — flag missing as WARNING
- SP-002: The `parent_location` value is registered in `specs/locations.md` — flag unknown LOC-ID as CRITICAL
- SP-003: If `scene_type: travel`, node has both `origin_location` and `destination_location` — flag missing as CRITICAL
- SP-004: If node is a hub passage (`LOC-xxx` ID): provides ≥3 navigation destinations (scenes + travel links combined) — flag fewer as WARNING
- SP-005: Every Area in `world-map.md` has ≥1 Location with a `scene_type: rest` node — flag missing as CRITICAL
- SP-006: Every Area in `world-map.md` has ≥1 `scene_type: travel` node as its entry point — flag missing as CRITICAL
- SP-007: Hub passages use `LOC-{ShortName}` ID format (not `NODE-NNN`) — flag wrong format as WARNING
- SP-008: Every `<<wmLoc passage=...>>` call and hub `[[link|PassageName]]` must resolve to a `passage_name:` field in the corresponding node outline — flag unresolved passage name as CRITICAL (broken Twine navigation)
- SP-009: `parent_area` in node frontmatter must be registered as a child of `parent_region` in `specs/world-map.md`, and `parent_location` must be registered as a child of `parent_area` — flag chain mismatch as CRITICAL (node placed in wrong part of hierarchy)

### LT – Loot & Economy Checks *(skip if `loot` hook is not in `constitution.md ## II. Active Mechanics`)*

Read `constitution.md ## VI-B. Randomness & Economy Model` for the active model. Apply the matching rules:

- LT-001: Every combat node with `scene_type: combat` has a post-combat loot resolution — a `<<lootDrop>>`, `<<lootFixed>>`, or explicit "no loot" comment — flag absent as WARNING
- LT-002: Every `container_id` referenced by `<<lootDrop>>` or `<<lootContainer>>` exists in `$loot_table_registry` (StoryInit) — flag unknown ID as CRITICAL
- LT-003: Every item `item_variable` in any loot table entry is declared in `variables.md ## Inventory` — flag undeclared items as CRITICAL
- LT-004: If `loot_model: fixed` — flag any loot table item with `weight < 100` as WARNING (weight is ignored but inconsistent)
- LT-005: If `loot_model: weighted` — flag any container whose entire item pool has `weight: 100` on every item as NOTE (effectively fixed; consider `loot_model: fixed`)
- LT-006: Quest completion nodes (`scene_type: quest_event` + final stage) must call `<<questReward>>` or `<<lootGold>>` — flag absent payout as WARNING
- LT-007: `<<lootGold>>` and `<<lootFixed>>` must NOT be called inside an already-handled `<<questReward>>` call (double-grant risk) — flag as WARNING
- LT-008: If `container_respawn: never` — flag any node that manually sets `$loot_opened_[id]` to `false` as WARNING (breaks one-shot guarantee)
- LT-009: If `enemy_spawn_model: scripted` — flag any combat node with no `<<set $combat_enemies to [...]>>` before `<<combatStart>>` as CRITICAL
- LT-010: Currency mutations must use `<<lootGold>>`, `<<shopBuy>>`, or `<<questReward>>` — flag direct `<<set $gold to ...>>` writes in node passages as WARNING (bypasses economy tracking)
- LT-011: If `quest_availability: random_pool` — flag any side/optional quest trigger that assumes the quest is always present (no `<<if $quest_pool.includes("quest_name")>>` guard) as WARNING
- LT-012: If `travel_encounters: encounter_table` — flag any `scene_type: travel` node with no `<<travelRoll>>` call as WARNING; verify a `## Travel Encounter Tables` section exists in `specs/world-map.md`
- LT-013: If `world_map_fog: visited` — flag any `<<wmLoc>>` call that doesn't check `_visited` before rendering the link as WARNING; if `region_unlock` — flag Locations whose region has no `<<regionUnlock>>` call in any reachable node as CRITICAL

---

### RT – Rest System Checks *(skip if `rest` hook is not in `constitution.md ## II. Active Mechanics`)*

- RT-001: Every `scene_type: rest` node must contain a `MECHANIC:REST` block or a `/* milestone rest */` comment — flag absent as WARNING
- RT-002: `MECHANIC:REST type=long` must include `return=[NODE-ID]` — flag absent as CRITICAL (long rest has no exit)
- RT-003: `MECHANIC:REST type=milestone` must NOT contain `<<shortRestScene>>` or `<<longRestScene>>` calls — flag as WARNING (milestone has no mechanical recovery)
- RT-004: Do NOT use `<<shortRest>>` or `<<longRest>>` directly in node passages — always use `<<shortRestScene>>` or `<<longRestScene>>` — flag bare calls as WARNING
- RT-005: `<<longRestScene>>` must be the last statement before a passage boundary — flag any `[[link]]` or `<<goto>>` after it as WARNING (it handles navigation itself)
- RT-006: If `container_respawn: long_rest` in constitution — verify `<<restReset "long">>` is called inside `<<longRestScene>>` (it is by template; flag if manually removed) as CRITICAL
- RT-007: If `container_respawn: in_game_day` — verify `<<restReset "day">>` is called at every day-boundary node (nodes with `$day_counter` increment) as WARNING
- RT-008: Long rest nodes must have matching narrative prose for the waking moment in their `return=` passage — flag absent wake-up prose as NOTE
- RT-009: `$rest_count` must not be written manually — it is incremented by `<<longRestScene>>` — flag direct `<<set $rest_count ...>>` writes as WARNING

---

### CF – Crafting System Checks *(skip if `inventory_combine` is not `yes` in `constitution.md ## II`)*

- CF-001: Every `MECHANIC:CRAFT station=` reference must match a `$craft_station_[id]_unlocked` variable in StoryInit — flag unknown station_id as CRITICAL
- CF-002: Every `MECHANIC:CRAFT recipe=` reference must match a recipe `id` in `$craft_registry` — flag unknown recipe_id as CRITICAL
- CF-003: Every ingredient `item` in `$craft_registry` must be declared in `variables.md ## Inventory` — flag undeclared item as CRITICAL
- CF-004: Every `result_item` in `$craft_registry` must be declared in `variables.md ## Inventory` — flag undeclared item as CRITICAL
- CF-005: Scripted craft nodes (`MECHANIC:CRAFT recipe=`) must branch on `$last_craft_success` in prose — flag absent branch as WARNING (silent failure)
- CF-006: `<<craftStation>>` must be the last statement in a node before a passage boundary — flag any link or `<<goto>>` after it as WARNING
- CF-007: A station can only be used if `$craft_station_[id]_unlocked` is set — flag `<<craftStation>>` calls with no preceding `<<craftUnlockStation>>` anywhere in the node graph as CRITICAL
- CF-008: If a recipe has `skill_check` set — verify `sugarcube-skill-checks-template.twee` is loaded in the project (CF checks `SkillWidgets` passage exists) — flag absent as WARNING
- CF-009: Recipes with `on_fail_consume: true` must have matching failure prose after `<<craftAttempt>>` — flag absent failure branch as WARNING (player loses ingredients silently)

---

### TE – Travel Encounter Checks *(skip if `travel_encounters` is not `encounter_table` in `constitution.md ## VI-B`)*

- TE-001: Every `scene_type: travel` node must contain a `MECHANIC:TRAVEL_ENCOUNTER` block — flag absent as WARNING (travel node has no encounter roll)
- TE-002: `MECHANIC:TRAVEL_ENCOUNTER` must be the last mechanic in its node — flag any `[[link]]` or `<<goto>>` after `<<travelRoll>>` as CRITICAL (navigation conflict)
- TE-003: Every `region=` value must be a valid REGION-ID registered in `specs/world-map.md ## Region Registry` — flag unknown ID as CRITICAL
- TE-004: Every region referenced by `MECHANIC:TRAVEL_ENCOUNTER` must have a corresponding table entry in `specs/world-map.md ## Travel Encounter Tables` — flag missing table as WARNING
- TE-005: Every REGION-ID listed in `world-map-template.md ## Travel Encounter Tables` must have at least one encounter entry (non-empty table) — flag empty table as NOTE
- TE-006: Encounter entries of `type: combat` must cross-reference valid enemy definitions in `encounters-d5e.md` — flag unrecognised enemy key as WARNING
- TE-007: Encounter entries of `type: event` must reference a passage that exists in the project (authored as a `NODE-xxx` or named passage) — flag missing passage as CRITICAL
- TE-008: Encounter entries with `loot_id` set must have a matching entry in `$loot_table_registry` (from `world-map-template.md ## Loot Tables` or `mechanics-template.md`) — flag unknown loot_id as WARNING
- TE-009: `$region_[ShortName]_danger` must be initialised in StoryInit for every region with an encounter table — flag uninitialised as CRITICAL
- TE-010: If `travel_encounters: none` in constitution — flag any node containing `MECHANIC:TRAVEL_ENCOUNTER` or `<<travelRoll>>` as WARNING (hook active without config)

---

### CM – Companion Management Checks

- CM-001: Every companion `id=` value in `MECHANIC:COMPANION` must be registered in `constitution.md ## Companion System` — flag unknown ID as CRITICAL
- CM-002: Approval deltas must be signed integers (`+10` or `-15`) — flag bare unsigned numbers as WARNING (ambiguity; assumed positive)
- CM-003: `action=recruit` must appear before any `approval=` delta for the same companion across the full outline — flag out-of-order as WARNING (approval on unrecruited companion)
- CM-004: `action=recruit` must appear exactly once per companion — flag duplicate recruits as WARNING (double-join)
- CM-005: `action=leave reason=death` may only appear in a node with `scene_type: combat` or `scene_type: cutscene` — flag in other scene types as NOTE (narrative plausibility)
- CM-006: `react threshold=` must be a numeric value between -100 and 100 — flag out-of-range as CRITICAL
- CM-007: `react` blocks must have both `approve=` and `reject=` strings — flag missing branch as CRITICAL (widget crashes)
- CM-008: Companion approval changes must have at least one sentence of prose immediately before `<<companionApproval>>` — flag bare widget call as WARNING (player has no narrative context)
- CM-009: Companions with `ending_locked` in constitution must have `$[id]_alive` checked in the relevant ending node — flag absent check as WARNING (ending may trigger incorrectly)
- CM-010: Every companion listed in constitution.md must have `$[id]_recruited`, `$[id]_approval`, and `$[id]_alive` initialised in StoryInit — flag missing init as CRITICAL

---

## RPG-Specific Check Sections

**Activated based on `SESSION.is_rpg` and `SESSION.ruleset` values.**

### TR – Tabletop RPG Checks (if `SESSION.is_rpg = "tabletop"`)

- TR-001: Node frontmatter includes `session: [N]` and `encounter_type` (Combat CR-X / Social / Investigation / Puzzle / Hybrid)
- TR-002: GM Notes section is present with session #, NPC list, encounter type, key variables
- TR-003: All skill checks include explicit success/failure outcome narration (DC range documented)
- TR-004: All skill check DCs are appropriate to ruleset (D&D 5e: 5-20; PF2e: 10-50+; SR6e: documented pool)
- TR-005: If companion present: approval reactions documented; approval deltas within -100 to +100 range
- TR-006: If faction reputation changes: NPC acknowledges change explicitly (not silent variable shift)
- TR-007: If combat encounter: CR is appropriate to outlined party level (not >±2 CR variance)
- TR-008: Combat is narratively justified (not arbitrary); setup/foreshadowing present in prose
- TR-009: Session pacing estimate: node should fit in 30-120 minutes of typical 2-4 hour session
- TR-010: All NPCs use names and voices consistent with `npc-roster.md` Tabletop section

### CR – Computer Game RPG Checks (if `SESSION.is_rpg = "computer"`)

- CR-001: Routing section documents which playstyles (Combat/Dialogue/Exploration) reach this node
- CR-002: All three playstyles (Combat/Dialogue/Exploration) eventually converge to same story beat within 2 nodes
- CR-003: Difficulty scaling variants documented (Easy/Normal/Hard with distinct NPC counts, AC values, or loot)
- CR-004: If timed challenge or puzzle: accessibility features documented (colorblind, audio, motor, cognitive)
- CR-005: All skill check consequences branch explicitly (success→NODE-X, failure→NODE-Y)
- CR-006: Companion approval gates documented; if crossed, dialogue/narration changes
- CR-007: Difficulty setting does NOT lock story progression (all content completable on all difficulties)
- CR-008: No single playstyle route takes 3× longer than others (check estimated playtime per route)
- CR-009: All NPCs use names consistent with `npc-roster.md` Computer Game section
- CR-010: If dialogue-heavy: branches manageable (<10 immediate dialogue options); sub-branches lead to fewer options

### DR – D&D 5e-Specific Checks (if `SESSION.ruleset = "D&D 5e"`)

- DR-001: All skill check DCs fall within range 5-20 (5-9 Easy, 10-12 Easy, 13-15 Medium, 16-18 Hard, 19-20 Very Hard)
- DR-002: Companion approval changes are within -100 to +100 range; recruitment typically requires approval ≥ -50 or ≥ 0
- DR-003: Spell or magical ability references include proper notation and mechanical implication (e.g., "magical illusion [requires Arcana DC 14]")
- DR-004: Magic item rarity matches party level (Common/Uncommon for Levels 1-4, Rare for 5-10, Very Rare+ for 11+)
- DR-005: If multiple skill check paths: at least one uses non-Combat ability (Str/Dex/Con/Int/Wis/Cha balanced)
- DR-006: All stat block references (if NPC has AC/HP) come from `npc-roster.md` D&D 5e section
- DR-007: Ending gates track faction rep cumulatively (no single node exceeds ±25 rep per faction)

### PR2 – Pathfinder 2e-Specific Checks (if `SESSION.ruleset = "Pathfinder 2e"`)

- PR2-001: All skill check DCs fall within range 10-50+ per PF2e scale (10-11 Easy, 12-15 Medium, 16-20 Hard, 21-30 Very Hard, 31+ Extreme)
- PR2-002: Degree of Success outcomes documented for all skill checks (Critical Success / Success / Failure / Critical Failure narration)
- PR2-003: Hero Point spending opportunities documented if available (player can spend for reroll or bonus action)
- PR2-004: Ancestry/background implications acknowledged (e.g., Dwarven character recognizes stonework; Halfling has size-based perspective)
- PR2-005: Companion recruitment requires realistic approval threshold (typically ≥ 0 approval before recruitment possible)
- PR2-006: All stat block references come from `npc-roster.md` Pathfinder 2e section

### SR – Shadowrun 6e-Specific Checks (if `SESSION.ruleset = "Shadowrun 6e"`)

- SR-001: All dice pool checks documented with [Skill + Attribute] notation and threshold noted
- SR-002: Street / Matrix / Astral routing options all genuinely available (not forced specialization)
- SR-003: Success/failure outcomes distinct across all three routing options; rewards roughly equivalent (Nuyen, Karma, info)
- SR-004: Glitch risk noted for critical rolls (2+ ones = glitch regardless of successes)
- SR-005: Karma spending tracked across node (no excessive single-node Karma dumps; Karma economy cumulative)
- SR-006: Street Cred / Contact opportunities clearly documented if contact recruitment or networking present
- SR-007: Matrix hacking vs. Street legwork vs. Astral magic paths have equivalent difficulty and time to reach same outcome

---
### Step 5 � Score and Verdict

Calculate the weighted **RTG � Overall Rating**:

**Generic / Computer Game**:

| Section | Weight | Item Count |
|---|---|---|
| Node Rules (NR) | 30% | 9 items |
| Prose Rules (PR) | 25% | 11 items |
| Mechanic Compliance (MC) | 25% | 6 items |
| Game Bible Compliance (GB) | 20% | 4 items |

**Tabletop RPG** (replaces above):

| Section | Weight | Item Count |
|---|---|---|
| Node Rules (NR) | 20% | 9 items |
| Prose Rules (PR) | 20% | 11 items |
| Mechanic Compliance (MC) | 20% | 6 items |
| Game Bible Compliance (GB) | 10% | 4 items |
| Tabletop RPG (TR) | 15% | 10 items |
| Ruleset-Specific (D&D 5e/PF2e/SR6e) | 15% | 6-7 items |

**Computer Game RPG** (adds to generic):

| Section | Weight | Item Count |
|---|---|---|
| Node Rules (NR) | 25% | 9 items |
| Prose Rules (PR) | 20% | 11 items |
| Mechanic Compliance (MC) | 20% | 6 items |
| Game Bible Compliance (GB) | 15% | 4 items |
| Computer Game RPG (CR) | 10% | 10 items |
| Ruleset-Specific (D&D 5e/PF2e/SR6e) | 10% | 6-7 items |

Score each section 1–10 based on items passed. Apply weights. A weighted total **≥ 7** is required to pass.

**Hard-fail gates** (FAIL regardless of weighted score):
- Any NR-002 failure (unknown choice target – export will break)
- Any NR-006 failure (unreadable variable – runtime error)
- Any NR-009 failure (wrong choices format – `export.py` will drop all choices)

**Platform-Specific Hard-Fail Gates**:
- **Tabletop**: TR-001 failure (missing session # or encounter type – GM can't prepare)
- **Tabletop**: TR-007 failure (CR out of range by >2 – encounter impossible to balance)
- **Computer**: CR-007 failure (difficulty locks progression – player stuck)
- **Computer**: CR-004 failure (accessibility missing from timed challenge – fails compliance)

### Step 6 � Write Checklist File

Save to `checklists/[NODE_ID]-checklist.md` using `templates/checklist-template.md`.

Confirm: `? Saved: checklists/[NODE_ID]-checklist.md`

### Step 7 � Report
Output per node varies by platform:

**Tabletop RPG Node**:
```
[NODE_ID] – SESSION [N]  [PASS / FAIL]  (score: [N.N] / 10)
  NR [N/9]  PR [N/11]  MC [N/6]  GB [N/4]  TR [N/10]  [RULESET] [N/6-7]
  Encounter: [Type CR-X]
```

**Computer Game RPG Node**:
```
[NODE_ID] – [PASS / FAIL]  (score: [N.N] / 10)
  NR [N/9]  PR [N/11]  MC [N/6]  GB [N/4]  CR [N/10]  [RULESET] [N/6-7]
  Routes: [Combat/Dialogue/Exploration]  Accessibility: [Y/N]
```

**Generic Node**:
```
[NODE_ID] – [PASS / FAIL]  (score: [N.N] / 10)
  NR [N/9]  PR [N/11]  MC [N/6]  GB [N/4]
```

All include: Failures list, hard-fail gates, top 3 revision priorities.

If FAIL: `Run speckit.revise [NODE_ID] to fix failures before this node can be approved.`

Summary table for multiple nodes shows: Node | Score | Verdict | Type | Hard-fail? | Top failure
Output per node:

```
[NODE_ID] � [PASS / FAIL]  (score: [N.N] / 10)

  NR  [N passed / 9]   PR  [N passed / 11]   MC  [N passed / 6]   GB  [N passed / 4]

  Failures:
    [RULE_CODE]  [brief description]
      ? [quoted offending line or frontmatter value]

  Hard-fail gates:
    NR-002  ? / ?
    NR-006  ? / ?
    NR-009  ? / ?

  Top revision priorities:
    1. [Highest-impact item]
    2. [Second priority]
    3. [Third priority if applicable]
```

If FAIL: `Run speckit.revise [NODE_ID] to fix failures before this node can be approved.`

If checking multiple nodes, append a summary table:

```
| Node | Score | Verdict | Hard-fail? | Top failure |
|---|---|---|---|---|
| NODE-003 | 8.1 | PASS | � | � |
| NODE-007 | 5.4 | FAIL | NR-009 | choices format |
```

## Post-Execution Hooks

Check for extension hooks after execution:
- Look for `hooks.after_checklist` in `.specify/extensions.yml`. Process as standard hook block. Skip silently if absent.

---

## Key Principles for RPG Checklist

**Auto-Detection**: No flags required. Checklist automatically detects platform/ruleset from `constitution.md` and activates appropriate checks.

**Platform-Specific Quality Gates**:
- **Tabletop RPG**: Validates session context (encounter CR, GM prep, NPC presence, pacing)
- **Computer Game RPG**: Validates playstyle routing, difficulty scaling consistency, accessibility compliance
- **All RPG Presets**: Validate system-specific mechanics (skill DC ranges, approval/faction rep ranges, ending gates)

**Overlapping Checks**: TR/CR/Ruleset checks add to base NR/PR/MC/GB checks. A Tabletop D&D 5e node is scored on up to 18 checks total.

**Hard-Fail Gates Are Blocking**: Platform-specific hard-fails (TR-001, TR-007, CR-007, CR-004) must pass or node fails regardless of weighted score.

**Ruleset-Specific Thresholds**:
- D&D 5e: DC 5-20, approval/faction ±100, magic item rarity by level
- Pathfinder 2e: DC 10-50+, degree of success outcomes, hero points
- Shadowrun 6e: Dice pool notation, Street/Matrix/Astral routing balance

**Campaign Prep Validation** (Tabletop first run): Checklist validates campaign-guide.md and SESSION-0-BRIEFING.md exist on first session node.

