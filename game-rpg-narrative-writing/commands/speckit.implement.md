---
description: Draft narrative prose for nodes from approved outlines. When invoked without NODE_ID, reads tasks.md to find the next uncompleted draft task. After drafting, marks the corresponding task as completed in tasks.md. Prose is generated engine-agnostic (markdown), then exported to engine-specific formats (Twee for SugarCube, Ink, etc.) via speckit.export.
handoffs:
  - label: Export to engines
    agent: speckit.export
    prompt: Export drafted markdown nodes to engine-specific formats (SugarCube, Ink, etc.)
    send: true
  - label: Compile to playable output
    agent: speckit.compile
    prompt: Compile exported engine files to playable HTML/JSON
    send: true
  - label: Review outlines again
    agent: speckit.outline
    prompt: I want to review or regenerate the outlines before drafting
    send: false
---

# speckit.implement

Draft narrative prose for nodes from approved outlines. Generates engine-agnostic markdown node files, preserving all outline information (variables, choices, mechanical consequences) in structured format.

## User Input

```text
$ARGUMENTS
```

Accepted arguments:
- `[NODE_ID]` – draft a single node (e.g. `NODE-001`)
- `[NODE_ID] [NODE_ID] ...` – draft a list of nodes
- `--act [N]` – draft all nodes for a given act
- `--all` – draft all approved nodes that don't yet have draft files
- `--force` – regenerate an existing draft (overwrite)
- *(no argument)* – read `tasks.md` to find the next uncompleted `[P] Draft:` or `Draft:` task, then draft that node

## Pre-Execution Checks

**Extract Platform, Ruleset & Engine** (auto-detect from constitution.md):
- Read `.specify/memory/constitution.md` YAML frontmatter
- Extract `[PLATFORM]` and `[RULESET]`:
  - If `[PLATFORM]` = "Tabletop": Set `SESSION.is_rpg = "tabletop"` and load Tabletop prose model
  - If `[PLATFORM]` = "Computer Game": Set `SESSION.is_rpg = "computer"` and load Computer Game prose model
  - If neither: Set `SESSION.is_rpg = false` (generic prose model)
- Extract `export_engines` (list) or `engine` (single value):
  - If `sugarcube` is the target engine: Set `SESSION.engine = "sugarcube"` — **output `.twee` files directly; skip speckit.export**
  - If `ink` is the target engine: Set `SESSION.engine = "ink"` — **output `.ink` files directly; skip speckit.export**
  - Otherwise: Set `SESSION.engine = "generic"` — output engine-agnostic `.md` draft files
- Store `SESSION.platform`, `SESSION.ruleset`, `SESSION.engine` for all conditional steps below

**Check for extension hooks (before drafting)**:
- Check if `.specify/extensions.yml` exists in the project root
- If it exists, read it and look for entries under the `hooks.before_implement` key
- Process as standard hook block (Optional/Mandatory). Skip silently if absent.

**If no NODE_ID was given:**
1. Check if `specs/[FEATURE_DIR]/tasks.md` exists
2. If it exists, scan for the first uncompleted `[P] Draft:` or `Draft:` task (check for `- [ ]` checkbox in Phase 2/4/6 task tables)
3. Extract the NODE_ID from the task's Node column
4. If no uncompleted draft task is found, halt: "No uncompleted draft tasks in tasks.md. Run `speckit.tasks --update` or specify NODE_ID manually."

Then:
1. Confirm `specs/[FEATURE_DIR]/outline/` and `specs/[FEATURE_DIR]/constitution.md` exist
2. For each requested node, verify an outline file exists at `outlines/[NODE_ID].md`
   - **Exception**: If `[NODE_ID]` matches the pattern `LOC-{ShortName}` (e.g. `LOC-Tavern`, `LOC-VaultEntry`), switch to **Hub Passage mode** (see Step 1b below) — no outline file is required for LOC-xxx IDs
3. Verify outline status is `APPROVED` (skip nodes marked `DRAFT` or `SKIP`) — unless `--force` is set
4. Confirm `specs/[FEATURE_DIR]/variables.md` exists — hooks declared in outlines must resolve
5. Confirm `specs/[FEATURE_DIR]/characters.md` exists — dialogue and NPC references must resolve
6. Confirm `specs/[FEATURE_DIR]/constitution.md` exists — prose_profile and engine settings needed
7. **If RPG detected**: Confirm `specs/[FEATURE_DIR]/mechanics-[ruleset].md` exists — skill checks, approval gates, faction reps must resolve

## Execution Steps

### Phase 0 — Infrastructure Generation *(SugarCube only; skip for Ink / Generic)*

**Run once per project before generating any node prose.** Check whether the infrastructure files already exist before generating. If they exist, skip and proceed to Step 1.

Infrastructure files live in `draft/sugarcube/infra/`. Generate each file that is absent:

| File | Source template | When needed |
|---|---|---|
| `infra/StoryInit.twee` | All template `[*-block-merge-into-existing]` blocks merged | Always (first project run) |
| `infra/AllWidgets.twee` | All template `[widget]` passages merged | Always |
| `infra/CharacterSheet.twee` | `sugarcube-character-sheet-template.twee` `CharacterSheet` passage | Always |
| `infra/QuestJournal.twee` | `sugarcube-quest-journal-template.twee` `QuestJournal` passage | If quest mechanic active |
| `infra/PartyRoster.twee` | `sugarcube-companion-template.twee` `PartyRoster` passage | If companion mechanic active |
| `infra/WorldMap.twee` | `sugarcube-world-map-template.twee` `WorldMap` passage | If `world_map_fog` is set |
| `infra/CombatUI.twee` + `CombatBody.twee` | `sugarcube-combat-template.twee` | If combat mechanic active |
| `infra/LootContainer.twee` + `LootContainerUI.twee` | `sugarcube-loot-template.twee` | If loot mechanic active |
| `infra/CraftUI.twee` + `CraftResultUI.twee` | `sugarcube-crafting-template.twee` | If craft mechanic active |
| `infra/RestUI.twee` | `sugarcube-rest-template.twee` | If rest mechanic active |
| `infra/TravelEncounterTransition.twee` | `sugarcube-travel-encounter-template.twee` | If `travel_encounters: encounter_table` |
| `infra/InventoryUI.twee` | `sugarcube-equipment-ui-template.twee` `InventoryUI` passage | Always |
| `infra/ShopUI.twee` | `sugarcube-shop-template.twee` `ShopUI` passage | If shop mechanic active |
| `infra/StoryMenu.twee` | `sugarcube-character-sheet-template.twee` `StoryMenu` stub | Always |
| `infra/StoryCaption.twee` | Merged from char/quest/companion StoryCaption stubs | Always |
| `infra/StoryStylesheet.twee` | `sugarcube-theme-minimal.css` (or dark/light per constitution) | Always |

**How to generate `StoryInit.twee`:**
1. Read `constitution.md ## VI-B` (randomness model) and `## Companion System`
2. Read `variables.md` — every declared variable becomes a `<<set $varname to initialValue>>` line, grouped by section
3. Read `quests.md` — generate `$quest_[id]_state`, `$quest_[id]_stage`, and `$quest_registry` array
4. Read `world-map.md` — generate `$region_*`, `$area_*`, `$loc_*` spatial variables
5. Merge all template `[*-merge-into-existing]` StoryInit blocks, filling placeholders from spec files
6. Emit the merged result as a single `:: StoryInit` passage

**How to generate `AllWidgets.twee`:**
1. Collect every `[widget]`-tagged passage from all active supplementary templates
2. Merge into a single `:: AllWidgets [widget]` passage
3. Replace placeholders in widget code (`[COMPANION_1]`, `[PASSAGE_NAME]`, etc.) with project-specific values from spec files

**Compile command** (output at end of Phase 0):
```bash
tweego -o draft/sugarcube/[PROJECT_NAME].html \
  draft/sugarcube/infra/StoryInit.twee \
  draft/sugarcube/infra/AllWidgets.twee \
  draft/sugarcube/infra/CharacterSheet.twee \
  draft/sugarcube/infra/QuestJournal.twee \
  draft/sugarcube/infra/CombatUI.twee \
  draft/sugarcube/infra/CombatBody.twee \
  draft/sugarcube/infra/WorldMap.twee \
  draft/sugarcube/infra/*.twee \
  draft/sugarcube/LOC-*.twee \
  draft/sugarcube/NODE-*.twee
```

Confirm: `✓ Phase 0 complete — [N] infrastructure files generated in draft/sugarcube/infra/`

---

### 1. Load Required Documents

For each target node, load:
- **Required**: Outline file `outlines/[NODE_ID].md` (Beat Summary, Variables, Choices, Mechanic Hooks)
- **Required**: `constitution.md` (prose_profile, default POV, tone, style_mode, platform, ruleset)
- **Required**: `spec.md` (research notes, world rules, context)
- **Required**: `variables.md` (variable declarations for type checking)
- **Required**: `characters.md` (NPC profiles, dialogue registers, relationship states)
- **Required**: `mechanics.md` (hook schemas for translating mechanics to engine syntax)
- **Optional**: `craft-rules.md` (if style_mode is humanized-ai — guides beat language register)
- **Optional**: `glossary.md` (for consistent terminology in prose)
- **Optional**: `locations.md` (for sensory anchors and location-specific rules)
- **Optional**: `themes.md` (for thematic resonance and motif placement)
- **Optional**: `player-classes.md` (RPG tabletop & computer: player character classes, abilities, starting gear)
- **RPG-Only**: `mechanics-[ruleset].md` (skill DC ranges, approval thresholds, faction reps, Tabletop session structure)
- **Tabletop-Only**: `quests.md`, `npc-roster.md` (quest context, NPC stat blocks if any)
- **Computer Game-Only**: `npc-roster.md`, `locations.md` (playstyle routing hints, difficulty scaling)

**Engine-specific node template** (loaded when `SESSION.engine` is set):
- `SESSION.engine = "sugarcube"` — load `templates/node-outline-d5e-sugarcube.md` as the **structural reference** for all generated `.twee` passages. The generated output must follow the passage layout, macro patterns, skill check structure, and variable handling shown in that template. Load `templates/node-start-twee-template.twee` for the frontmatter comment block format.
- `SESSION.engine = "ink"` — load `templates/node-outline-d5e-ink.md` as the structural reference for all generated `.ink` knots.
- `SESSION.engine = "generic"` — load `templates/node-outline-template.md` as the structural reference for all generated `.md` drafts.

**SugarCube supplementary templates** — load each only when the node requires it (check `scene_type` and mechanic hooks from the outline):

| Template | Load when |
|---|---|
| `sugarcube-skill-checks-template.twee` | Outline has any skill-check mechanic hook (`[MECHANIC:SKILL_CHECK]` or `skill_check` hook type) |
| `sugarcube-combat-template.twee` | `scene_type: combat` or outline has a combat mechanic hook |
| `sugarcube-faction-reputation-template.twee` | Outline mutates any `$faction_*` or `$rep_*` variable |
| `sugarcube-character-sheet-template.twee` | First node in a project (StoryInit setup) or any node using `$partyLevel`, `$playerHP`, ability modifiers |
| `sugarcube-equipment-ui-template.twee` | Outline has an inventory mechanic hook (`add`/`remove` item) |
| `sugarcube-shop-template.twee` | `scene_type: shop` |
| `sugarcube-quest-journal-template.twee` | `scene_type: quest_event` or outline sets a quest-stage variable |
| `sugarcube-loot-template.twee` | `scene_type: combat` post-combat drop, outline has a container/chest interaction, or a quest completion payout |
| `sugarcube-rest-template.twee` | `scene_type: rest` node, or project uses `container_respawn: long_rest` / `quest_availability: random_pool` |
| `sugarcube-crafting-template.twee` | Outline has a `MECHANIC:CRAFT` hook or `inventory_combine: yes` is set in `constitution.md ## II` |
| `sugarcube-travel-encounter-template.twee` | `travel_encounters: encounter_table` in constitution and the node has `scene_type: travel` |
| `sugarcube-companion-template.twee` | Outline contains a `MECHANIC:COMPANION` block or constitution.md lists at least one companion in `## Companion System` |
| `sugarcube-spells-template.twee` | Outline has a spell-slot mechanic hook or spell cast event |
| `sugarcube-spatial-init-template.twee` | First node in a project (StoryInit setup) or when `--all` / `--act 1` is used |
| `sugarcube-world-map-template.twee` | WorldMap passage is requested, or project has `specs/world-map.md` and no WorldMap passage exists yet |
| `sugarcube-hub-passage-template.twee` | Node ID matches `LOC-{ShortName}` pattern (see Step 1b) |

For each loaded supplementary template: use its widget definitions (`<<widget ...>>`) inline in the generated `.twee` exactly as shown — **do not rewrite widget logic from scratch**.

### 1b. Hub Passage Mode (LOC-xxx IDs only)

> **Trigger**: If the requested node ID matches the pattern `LOC-{ShortName}` (from `specs/locations.md`), this mode replaces the standard drafting flow. Skip Steps 2–6 for this node; return here.

Hub passages are navigation aggregation points. They do not carry story prose — they let the player see the current Location's scenes, NPCs, and exits.

**Load from `specs/locations.md`**:
- Location name, description, parent area, parent region
- Scene IDs for all nodes in this Location (and their `scene_type`)
- Hub Passage ID (should equal the requested `LOC-xxx`)

**Load from `specs/world-map.md`** (if present):
- Adjacent Locations reachable from this Location (travel connections)

**Generate hub passage per engine**:

**SugarCube** (`draft/sugarcube/LOC-{ShortName}.twee`):

> **CRITICAL: Follow `templates/sugarcube-hub-passage-template.twee` exactly.**
> Copy its `:: LOC-[ShortName] [hub location]` passage structure and populate from `locations.md` and `world-map.md`.
> Use the `<<hubScene>>` and `<<hubTravel>>` widgets defined in `HubWidgets` (from that template — merge once into the project WidgetPassage).
> Do not invent a different passage layout.

Key rules from the template:
- First-visit `<<if not $loc_{ShortName}_visited>>` trigger block at top
- Location state guard (`<<if $loc_{ShortName}_state eq "abandoned">>` etc.) if `$loc_{ShortName}_state` is used
- `<h2>[Location Name]</h2>` header
- One `<<hubScene "NODE-xxx_Name" "Label">>` per scene in this Location (from `locations.md` Scene IDs)
- State-gated scenes use third argument: `<<hubScene "NODE-xxx" "Label" "$condition">>`
- One `<<hubTravel "LOC-Adjacent" "Label">>` per travel exit (from `world-map.md` travel connections)
- At least one unconditional travel exit; flag WARNING if all exits are gated

**Ink** (`draft/ink/LOC-{ShortName}.ink`):
```ink
=== LOC_{ShortName} ===
[Location Name]
[Brief 1–2 sentence sensory description]

Where do you want to go?
+ [{Scene label A}] -> NODE_{seq}_{Name}
+ [{Scene label B}] -> NODE_{seq}_{Name}
+ [Travel to {Adjacent Location}] -> LOC_{AdjacentShortName}
- -> LOC_{ShortName}
```
Rules:
- Hub label uses `=== LOC_{ShortName} ===` (underscores, no hyphens — Ink identifier constraint)
- Scene choices use `->` diverts to scene knots by NODE_ID
- Travel choices divert to other LOC_ labels
- Loop back (`-> LOC_{ShortName}`) so player can choose again after returning

**Tabletop / GM Reference** (`draft/tabletop/LOC-{ShortName}.md`):
```markdown
## [Location Name] — GM Hub Reference

> [Boxed text for first arrival — 2–3 sentences of sensory/atmospheric description]

**Location ID**: LOC-{ShortName} | **Parent Area**: AREA-{AreaName} | **Parent Region**: REGION-{RegionName}

### Scenes at this location
| Scene | Node | Type | Notes |
|---|---|---|---|
| [Scene Name] | NODE-xxx | [scene_type] | [When triggered / conditions] |

### NPC Roster
| NPC | Status | Role |
|---|---|---|
| [Name] | Present / Optional / Gone if $loc_xxx_state = "cleared" | [Role] |

### Travel exits
| Destination | Direction | Condition |
|---|---|---|
| [Location Name] | [North / Port / etc.] | [Open / requires $area_xxx_cleared] |
```

**Output file naming**: `draft/[ENGINE]/LOC-{ShortName}.twee` / `.ink` / `.md`
**Do not create an outline file** for LOC-xxx hub passages.

---

### 2. Parse Outline Choices & Consequences

**This is the critical step for preserving consequences:**

From the outline's **Choices table**, extract:
- Column 1: Choice letter (A, B, C...)
- Column 2: **Label** (player-visible choice text)
- Column 3: **Condition** (optional gate like `$trust_mira >= 50`)
- Column 4: **Target Node** (NODE_ID or END_ID)
- Column 5: **Narrative Consequence** (description of what changes if this choice is made)

**Store the narrative consequence** as a comment in the drafted node's Choices section:
```markdown
- [CHOICE_LABEL](TARGET_NODE) <!-- Effect: [Narrative Consequence from outline] -->
```

**If condition exists**, include both condition and consequence:
```markdown
- [CHOICE_LABEL](TARGET_NODE) <!-- requires: $trust_mira >= 50; Effect: Mira remembers your loyalty -->
```

### 3. Extract Variables & Mechanics

From the outline:
- **Variables Read**: Variables this node checks as conditions
- **Variables Set**: Variables this node changes (from Mechanic Hooks Summary)
- **Mechanic Hooks**: All hooks and their configuration (type, tier, variable, action, timing)

Populate the node frontmatter:
```yaml
variables_read: [var1, var2]  # From outline's "Variables Read" section
variables_set: [var3, var4]   # From outline's "Variables Set" section
```

### 4. Draft Narrative Prose

**Goal**: Write engaging prose that:
- Matches the beat summary from the outline
- Uses the prose_profile (style, register, tone) from constitution.md
- Reads coherently without the mechanic hook blocks
- Respects the outlined choices (don't create new choices)
- Includes all required variables from outline's Variables Read/Set sections

**Opening line** MUST establish:
- Where (location/context)
- Who (character perspective, NPCs present)
- What (the central decision or situation)

**Prose structure**:
1. Opening: Orient the player (location, stakes, context)
2. Middle: Describe the situation, NPCs, choices available
3. Mechanic hooks: Insert hooks inline (format depends on engine — see Step 5)
4. Choices: Terminal choices section with all outlined choices (format depends on engine)

**Style rules**:
- POV: Use constitution.md default POV (second-person, third-person, first-person) or node-level override
- Tone: Match constitution.md tone (dramatic, comedic, dark, uplifting, etc.)
- Register: If style_mode is humanized-ai, use craft-rules.md to tune beat language and dialogue

**Engine output format** (determined by `SESSION.engine`):

> **SugarCube** (`SESSION.engine = "sugarcube"`)
> Output: `draft/sugarcube/NODE-{seq}_{Name}.twee` — Twee 3 passage format, SugarCube 2.x macro syntax
>
> **CRITICAL: Follow `templates/node-outline-d5e-sugarcube.md` for all structural and macro patterns.**
> The template defines the authoritative layout. Do not invent macro patterns not shown there.
>
> Required passage structure (from template):
> 1. `/* ... */` frontmatter comment block (node_id, title, act, status, pov, variables_read, variables_set, drafted, outline_ref) — format from `node-start-twee-template.twee`
> 2. `:: NODE-{seq}_{Name} [scene]` passage header with correct tags
> 3. Prose opening (HTML paragraphs `<p>...</p>` or plain text per constitution.md prose_profile)
> 4. Skill check sub-passages: each check gets its own `:: NODE-{seq}_{Name}_{CheckType}` passage with `<<set $roll to random(1,20)>>`, `<<set $total to $roll + $mod>>`, `<<if $total gte $dc>>` success/fail blocks — exactly as shown in template
> 5. Variable mutations inline: `<<set $var to value>>` or `<<set $var += delta>>` at the point they occur in narrative, not batched at end
> 6. Companion approval/faction rep mutations: `<<set $companionApproval += N>>` inline after the triggering dialogue, with conditional companion reaction dialogue
> 7. Choices at the end as `[[Label|TARGET_NODE]]` wiki-links or `<<link "Label" "TARGET_NODE">>` macros
> 8. Consequence comments as `/* Effect: ... */` on the same line as the choice
>
> For **hub passages** (LOC-xxx): use `templates/sugarcube-hub-passage-template.twee` instead — see Step 1b.
> - **No speckit.export step required** — hand directly to `speckit.compile sugarcube`
>
> **Ink** (`SESSION.engine = "ink"`)
> Output: `draft/ink/NODE-{seq}_{Name}.ink` — Ink knot format
> **Follow `templates/node-outline-d5e-ink.md` for all structural and divert patterns.**
> - Passage as `=== NODE_{seq}_{Name} ===` knot
> - Variables as `~ var = value` and `{var}` conditionals
> - Choices as `+ [Label] -> TARGET_NODE` diverts
> - **No speckit.export step required** — hand directly to `speckit.compile ink`
>
> **Generic** (`SESSION.engine = "generic"` or not set)
> Output: `draft/NODE-{seq}_{Name}.md` — engine-agnostic markdown
> - Variables and hooks as `[MECHANIC:...]` token blocks (translated by speckit.export later)
> - Choices as markdown links `[Label](TARGET_NODE)`
> - **Requires speckit.export** to convert to engine format before speckit.compile

### 5. Inline Mechanic Hooks

The mechanic hook format depends on `SESSION.engine`. **Do not use `[MECHANIC:...]` tokens when `SESSION.engine = "sugarcube"` or `"ink"`** — those are generic-only tokens for later translation.

**Generic** (`SESSION.engine = "generic"`) — use `[MECHANIC:...]` token blocks:

```markdown
You notice a rusty key on the ground.
[MECHANIC:INVENTORY add=key_rusty]
It might be useful.

[MECHANIC:TRUST npc=mira delta=+5]
Mira smiles at you warmly, her trust deepening.
```

**SugarCube** (`SESSION.engine = "sugarcube"`) — write SugarCube macros directly, following `templates/node-outline-d5e-sugarcube.md`:

```twee
You notice a rusty key on the ground.
<<run $inv.push("key_rusty")>>
It might be useful.

Mira smiles at you warmly, her trust deepening.
<<set $miraTrust += 5>>

<<set $loc_chamber_visited to true>>
You've been here before — you know which shadows to avoid.
```

Skill checks generate their own sub-passage, not an inline block — follow `templates/sugarcube-skill-checks-template.twee`:
```twee
[[Attempt Insight Check|NODE-015_InsightCheck]]

:: NODE-015_InsightCheck
<<set $roll to random(1, 20)>>
<<set $total to $roll + $playerInsightMod>>
<<if $total gte 14>>
  [success prose]
  <<set $conspiracyDiscovered to true>>
  [[Continue|NODE-020_Report]]
<<else>>
  [failure prose]
  [[Try again|NODE-015_GuardInterrogation]]
<</if>>
```

Combat scenes — follow `templates/sugarcube-combat-template.twee` for `<<startCombat>>` / `<<combatResult>>` widget calls.

Faction rep changes — follow `templates/sugarcube-faction-reputation-template.twee` for `<<factionRep>>` widget calls instead of bare `<<set>>`.

Inventory/shop interactions — follow `templates/sugarcube-equipment-ui-template.twee` (`<<pickupItem>>` / `<<dropItem>>`) and `templates/sugarcube-shop-template.twee` (`<<shopOpen>>`).

Quest-stage changes — follow `templates/sugarcube-quest-journal-template.twee` for `<<questUpdate>>` widget calls.

Quest completion payouts — follow `templates/sugarcube-loot-template.twee` for `<<questReward>>`. Call `<<lootGold N>>` first for the gold amount, then `<<questReward "quest_name" xp ["item_var"]>>`. Do NOT call `<<questComplete>>` separately; `<<questReward>>` handles it.

Post-combat loot drops — follow `templates/sugarcube-loot-template.twee`. In the `player_won` branch of the combat return passage:
```twee
<<if $lastCombatOutcome is "player_won">>
  You stand over the fallen enemy.
  <<lootDrop "goblin_chief" "NODE-050_Aftermath">>
<</if>>
```
`<<lootDrop>>` resolves the drop table, grants items + gold, and navigates to `LootContainer` before returning to `NODE-050_Aftermath`. The container must be defined in `$loot_table_registry` (StoryInit).

Searchable containers / chests — use `<<lootContainer>>` instead of `<<lootDrop>>` when the player should browse items individually:
```twee
A battered chest sits in the corner.
<<if not $loot_opened_chest_crypt_1>>
  [[Search the chest|LootContainer]]<<set $loot_active_container to "chest_crypt_1">><<set $loot_return_passage to "NODE-030_AfterSearch">>
<<else>>
  The chest is empty.
<</if>>
```

Fixed key-item grants (no randomness) — use `<<lootFixed>>` directly:
```twee
Among the debris you find the captain's seal.
<<lootFixed "captains_seal" "Captain's Seal">>
```

Rest scenes (`scene_type: rest`) — follow `templates/sugarcube-rest-template.twee`. Do NOT write `<<shortRest>>` or `<<longRest>>` directly; always use the scene-level wrappers:

- **Short rest** — call `<<shortRestScene>>` at the narrative moment the party rests; prose continues in the same passage:
```twee
The party huddles in the alcove. Mira presses bandages against the wound.
<<shortRestScene>>
<<if $playerHitDiceRemaining gte 1>>
  You recover <<= $last_short_rest_heal>> HP.
<<else>>
  You have no hit dice left — the rest does little good.
<</if>>
[[Press on|NODE-045_Corridor]]
```

- **Long rest** — call `<<longRestScene "location" "ReturnPassage">>` as the final statement; it navigates automatically:
```twee
The innkeeper leads you to a modest room. You shed your armour and sleep.
<<longRestScene "inn" "NODE-050_Morning">>
```
Do NOT add any `<<goto>>` or `[[link]]` after `<<longRestScene>>` — it handles navigation.

- **Milestone rest** — write prose only; no widget calls. Add a `/* milestone rest */` comment so speckit.compile and speckit.checklist can identify the node:
```twee
/* milestone rest */
Sleep does not come easily. Faces of the dead drift through your mind —
a warning, or a memory you cannot place.
[[Dawn|NODE-055_Ruins]]
```

- **Interrupted rest** — set `$rest_interruption = true` before interruption prose, then branch:
```twee
The camp is quiet. You close your eyes.
<<longRestScene "camp" "NODE-060_Dawn">>

:: NODE-060_Dawn
<<if $rest_interruption>>
  [interrupted rest aftermath]
<<else>>
  [normal morning prose]
<</if>>
```

Crafting — follow `templates/sugarcube-crafting-template.twee`. Two patterns:

- **Player-driven (station menu)** — call `<<craftStation>>` as the final statement; it navigates to `CraftUI`:
```twee
Mira gestures to the alchemy bench. "Help yourself — the reagents are fresh."
<<craftStation "alchemy_bench" "NODE-040_AfterCraft">>
```
Do NOT add any link or `<<goto>>` after `<<craftStation>>` — it handles navigation.

- **Scripted inline craft** — call `<<craftAttempt>>` at the narrative moment, then branch on `$last_craft_success`:
```twee
You tear the cloth into strips and wind them tight.
<<craftAttempt "bandage_kit">>
<<if $last_craft_success>>
  A serviceable bandage — crude, but it will hold.
<<else>>
  Your hands shake. The cloth unravels. The materials are gone.
<</if>>
[[Continue|NODE-045_Passage]]
```

- **Unlock a station** in a node where the player gains access:
```twee
The smith waves you over. "My forge is yours until dawn."
<<craftUnlockStation "forge">>
[[Talk more|NODE-030_SmithDialogue]] [[Head to the forge|NODE-035_ForgeRoom]]
```

- **Conditional prose** (check before offering): use `<<craftCheck>>` to branch on ingredient availability:
```twee
<<craftCheck "health_potion">>
<<if $craft_can_make>>
  You have everything to brew a health potion here.
  [[Brew it|NODE-040_Brew]]
<<else>>
  You are missing: <<= $craft_missing_items.join(", ")>>.
<</if>>
```

Spell-slot expenditure — follow `templates/sugarcube-spells-template.twee` for `<<castSpell>>` widget calls.

**Inline rules (all engines)**:
- Prose must read coherently without the mechanic blocks
- Variable mutations fire at the narrative moment they occur, not batched at end
- The prose surrounding a mutation should justify it ("Mira smiles" before `$miraTrust += 5`)

Companion approval changes — follow `templates/sugarcube-companion-template.twee`. Four patterns:

- **Approval delta** — call `<<companionApproval>>` at the narrative moment; write justifying prose before it:
```twee
Thorne glances sideways at you, and for the first time allows himself a thin smile.
<<companionApproval "thorne" +10>>
```

- **Recruit** — call `<<companionRecruit>>` once, immediately after the join dialogue:
```twee
"Then we're agreed," Thorne says, shouldering his pack. "Lead on."
<<companionRecruit "thorne">>
```

- **Leave / Death** — call `<<companionLeave>>` with reason; for death set reason to `"death"`:
```twee
Mira slams the door behind her.
<<companionLeave "mira" "betrayal">>
```

- **Inline reaction** — `<<companionReact>>` for short two-branch prose; use `<<if $[id]_tier is "warm">>` blocks for multi-line branching:
```twee
<<companionReact "mira" 50 "Mira nods, impressed." "Mira looks away, unconvinced.">>
```

Approval changes **must** have justifying prose before them — never a bare widget call. Display the delta to the player within the prose (e.g. "Thorne approves" or show a UI pip via StoryCaption — do not use a `<<notify>>` popup unless the project explicitly configures one).

Travel encounter rolls (`scene_type: travel`, `travel_encounters: encounter_table`) — follow `templates/sugarcube-travel-encounter-template.twee`. `<<travelRoll>>` must be the **last** statement in the node — it handles navigation for both safe and triggered outcomes:
```twee
The road through Thornwood narrows. Branches scratch at your armour. Silence.
<<travelRoll "REGION-Thornwood" "NODE-050_ArriveVillage">>
```
Do NOT add `[[links]]` or `<<goto>>` after `<<travelRoll>>`. The node has no explicit exit — the roll decides where the player goes next.

For the combat return passage after a travel encounter, handle the loot drop if `$travel_pending_loot` is set:
```twee
:: NODE-050_ArriveVillage
<<if $lastCombatOutcome is "player_won" and $travel_pending_loot isnot "">>
  <<lootDrop $travel_pending_loot "NODE-050_ArriveVillage">>
<<elseif $lastCombatOutcome is "player_won">>
  You stand over the bodies and move on.
<</if>>
```



### 6. Terminal Choices Section

At the end of the node, write choices in the format matching `SESSION.engine`.

**Generic** (`SESSION.engine = "generic"`):
```markdown
## Choices

- [Look around carefully](NODE-002) <!-- Effect: You gain awareness of the chamber -->
- [Check the equipment](NODE-003) <!-- Effect: You discover a tool that might help -->
- [Leave immediately](NODE-004) <!-- requires: $flag_danger_sense == true; Effect: You escape before being discovered -->
```

**SugarCube** (`SESSION.engine = "sugarcube"`) — wiki-links or `<<link>>` macros, consequence as inline comment:
```twee
[[Look around carefully|NODE-002_LookAround]] /* Effect: You gain awareness of the chamber */
[[Check the equipment|NODE-003_Equipment]] /* Effect: You discover a tool that might help */
<<if $flag_danger_sense>>
  [[Leave immediately|NODE-004_Escape]] /* requires: $flag_danger_sense; Effect: You escape */
<</if>>
```

**Ink** (`SESSION.engine = "ink"`):
```ink
+ [Look around carefully] -> NODE_002_LookAround
+ [Check the equipment] -> NODE_003_Equipment
+ {flag_danger_sense} [Leave immediately] -> NODE_004_Escape
```

**Rules (all engines)**:
- Each choice must match exactly one row from the outline's Choices table
- Label MUST be verbatim from outline (or close synonym)
- Target node MUST match outline target
- Include condition gate if outlined choice had one
- Include consequence comment/annotation from the outline
- Minimum 2 choices for non-terminal nodes; omit entirely for ending nodes

### 7. Validate Against Outline

Before marking node as ready:
- ✓ All variables from outline Variables Read are present in prose or hooks
- ✓ All variables from outline Variables Set have corresponding hook blocks
- ✓ All mechanic hooks from outline are present
- ✓ All choices from outline are present with correct labels and targets
- ✓ All narrative consequences from outline are preserved as comments in Choices section
- ✓ Opening line establishes where/who/what
- ✓ Prose reads coherently without hook blocks

### 8. Output Format

**Generic/Computer Game**:
Create `draft/[ENGINE_NAME]/[NODE_ID].md` (engine-agnostic markdown):

```markdown
---
node_id: NODE-001
title: [Title from outline]
act: [Act number]
status: DRAFT
pov: [POV from constitution or outline override]
variables_read: [list]
variables_set: [list]
drafted: [YYYY-MM-DD]
outline_ref: outlines/[NODE_ID].md
---

# [Node Title]

<!-- Node ID: NODE_ID | Act: [ACT] | Status: DRAFT -->

[PROSE WITH INLINE MECHANICS]

## Choices

- [Label](NODE_TARGET) <!-- Effect: consequence from outline -->
```

**Tabletop RPG**:
Create `draft/SESSION-[N]/[NODE_ID].md` with **GM Notes** section at top:

```markdown
---
node_id: NODE-001
title: [Title from outline]
session: [N]
status: DRAFT
pov: [POV]
encounter_type: [Combat CR-X / Social / Investigation / Exploration]
variables_read: [list]
variables_set: [list]
drafted: [YYYY-MM-DD]
outline_ref: outlines/[NODE_ID].md
---

# [Node Title]

## GM Notes [TABLETOP]

**Session**: Session [N] | **Duration**: ~[minutes] | **Difficulty**: [Easy/Medium/Hard]
**NPCs Present**: [NPC], [NPC]
**Encounter**: [Type CR-X]
**Key Variables**: [var1], [var2]

<!-- Node ID: NODE_ID | Session: [N] | Status: DRAFT -->

[PROSE WITH INLINE MECHANICS AND SKILL CHECKS]

## Choices

- [Label](NODE_TARGET) <!-- Effect: consequence -->
```

### 8b. Update tasks.md

If `specs/[FEATURE_DIR]/tasks.md` exists, mark the drafted node's task as completed:

1. Find the task row for this NODE_ID (look for `Draft: [NODE_TITLE]` matching the drafted node)
2. Replace the `- [ ]` checkbox with `- [x]` in that row
3. If no matching task is found, add a note: "`tasks.md` has no draft entry for `[NODE_ID]`. Run `speckit.tasks --update` to regenerate."

### 9. Report

**Generic/Computer Game**:
List all drafted nodes with:
- `[NODE_ID] [title] — [N] vars, [N] hooks, [N] choices, act [N]`

**Tabletop RPG** (if first-time setup):
List all generated documents:
- ✅ `draft/campaign-guide.md` — Campaign overview + player introduction
- ✅ `draft/SESSION-0-BRIEFING.md` — Session 0 (character creation) briefing
- [NODE_ID] [title] — [N] vars, [N] hooks, [N] choices, session [N]
- (repeat per drafted node)

**All Modes**:
Flag any:
- Missing consequence comments in Choices section
- Undeclared variables
- Outline deviations (new choices, variables, or mechanics not in outline)
- (RPG-specific warnings from Quality Checklist above)
- Tasks updated in `tasks.md`

Remind the author to:
- ✅ **Tabletop**: Share `campaign-guide.md` with players before first session
- Review prose for coherence and tone
- Verify all consequences are documented as comments in Choices section
- Check that all outlined mechanics are present
- **Tabletop**: Verify GM Notes section has session #, NPCs, encounter type
- **Computer**: Verify playstyle routes and difficulty scaling documented
- Change `status: DRAFT` → `status: APPROVED` when satisfied
- **SugarCube/Ink**: Run `speckit.compile` directly — no export step needed
- **Generic**: Run `speckit.export` to convert to engine format, then `speckit.compile`

### 10. Check for Extension Hooks

Check `hooks.after_implement`: run if present.

---

## Key Principles: Outline Fidelity + RPG Awareness

**The implement phase must NOT:**
- Add new choices not in the outline
- Remove outlined choices
- Change choice targets
- Forget narrative consequences (bridge between mechanics and story)
- Skip GM Notes for Tabletop (session context, NPCs, encounter type)
- Miss playstyle routing for Computer Game (all playstyles equally viable)
- Omit skill check success/failure narration for any RPG
- Lose ending gate implications in Choices section

---

## Platform-Specific Implementation Summary

**Tabletop RPG**:
1. Auto-generate `campaign-guide.md` + `SESSION-0-BRIEFING.md` on first run
2. Include GM Notes (session #, NPCs, encounter type, skill checks) in each node
3. Narrate skill checks with explicit success/failure outcomes (system-appropriate DCs)
4. Use NPC names from `npc-roster.md`; show companion approval & faction rep changes
5. Validate: CRs match party level, combat is foreshadowed, session pacing realistic
6. Flag: CR misalignment, unjustified combat, pacing overruns

**Computer Game RPG**:
1. Document playstyle routes (all three paths reach same story beat)
2. Include difficulty scaling (Easy/Normal/Hard variant descriptions)
3. Narrate skill checks with branch outcomes (success leads to NODE-X, failure to NODE-Y)
4. Mark accessibility features (colorblind mode, audio cues, timer adjustments)
5. Validate: All playstyles viable, difficulty is scalable, no difficulty locks, accessibility complete
6. Flag: Playstyle imbalance, difficulty locks, missing accessibility

---

## Check for Extension Hooks

Check `hooks.after_implement`: run if present.

## Tabletop RPG Campaign Prep (AUTO-GENERATED FOR FIRST SESSION)

**Activated when**: `SESSION.is_rpg == "tabletop"` AND no `draft/campaign-guide.md` exists (first-time setup)

**Generate Campaign Guide** (`draft/campaign-guide.md`):

This document introduces the campaign to players before Session 1. Contents:

### Section 1: Campaign Overview
- **Campaign Name**: From `constitution.md`
- **Setting**: From `spec.md` world-building section
- **Tone & Expectations**: From `constitution.md` (e.g., "Heroic, high-stakes adventure with moments of levity")
- **Campaign Length**: "Estimated [N] sessions, [level] to [level]" (from `spec.md` party progression)
- **Playstyle**: "Focus on [combat/roleplay/exploration/intrigue]" (from `constitution.md` emphasis)
- **Content Warnings**: From `constitution.md` if present

### Section 2: House Rules & Mechanical Notes
- System: "[D&D 5e / Pathfinder 2e / Shadowrun 6e / Custom]" (from `constitution.md`)
- **Core Rule Mods**: Key divergences from base system (from `mechanics-[ruleset].md` Section II)
- **Skill Check Difficulty**: "DC 10-12 for common challenges, up to 18+ for legendary deeds" (from `mechanics-[ruleset].md`)
- **Combat Pacing**: "Expect [2-4] combat encounters per session of [2-4] hours" (from `spec.md`)
- **Death & Character Loss**: How is character death handled? (from `constitution.md`)
- **Downtime Between Sessions**: Any gold/crafting/rest mechanics? (from `spec.md` if applicable)

### Section 3: Party Composition & Level
- **Recommended Party Size**: [N] players, [level] characters (from `spec.md`)
- **Recommended Classes/Multiclass**: Any restrictions or encouragements? (from `spec.md`)
- **Starting Level**: [Level] (from `spec.md` / first node level gate)
- **Ending Level**: [Level] (from `spec.md` final boss/ending gates)

### Section 4: NPCs & Factions (Quick Reference)

| NPC Name | Role | Faction | How They React to PCs |
|---|---|---|---|
| [NPC1] | [Quest-giver / Companion / Antagonist] | [Faction] | [Brief personality] |

(From `npc-roster.md` Section I, pick top 5-7 NPCs)

### Section 5: Companion System (if applicable)
- **Companion Recruitment**: Approval gates, how companions join (from `spec.md` companion design)
- **Companion Fates**: Possible outcomes for recruited companions (from `endings.md` if tied to endings)
- **Romance Routes**: Approval thresholds for romance (if applicable, from `spec.md`)

### Section 6: Campaign Questions (What Will You Discover?)
- Q1: [Central dramatic question from `spec.md` Section I]
- Q2: [Major mystery or conflict from `spec.md` Section II]
- Q3: [Personal stakes - how does this affect the party? from `spec.md`]

### Section 7: What's Expected of You (Player Contract)
- Attendance/scheduling expectations
- Communication (how to contact GM)
- In-character vs. out-of-character tone
- Consent & lines (if any content is off-limits)

---

**Generate Campaign Summary** (minimal, ~200 words for session prep):
- Store as `draft/SESSION-0-BRIEFING.md` for Session 0 (character creation session)
- Used by GM to set tone and answer player questions before first play session

---

## Player Character Creation Implementation (Tabletop RPG)

**Activated when**: `SESSION.is_rpg == "tabletop"` AND no `draft/SESSION-0-CHARACTER-SHEET.md` exists (first-time setup)

Generates player-facing character sheet template and character creation walkthrough.

### Generate Character Sheet Template

Create `draft/SESSION-0-CHARACTER-SHEET.md` with sections:

#### D&D 5e Character Sheet

```markdown
# Character Sheet [D&D 5e]

## Basics
- **Name**: _________________
- **Class**: _________________  **Level**: _____
- **Race**: _________________  **Background**: _________________
- **Alignment**: _________________

## Ability Scores

| Ability | Score | Modifier | Saving Throw |
|---------|-------|----------|--------------|
| Strength | ___ | ___ | ___ |
| Dexterity | ___ | ___ | ___ |
| Constitution | ___ | ___ | ___ |
| Intelligence | ___ | ___ | ___ |
| Wisdom | ___ | ___ | ___ |
| Charisma | ___ | ___ | ___ |

## Skills & Proficiencies

**Proficiency Bonus**: +___ (Level ÷ 4, rounded up)

| Skill | Ability | Proficient? | Modifier |
|-------|---------|-------------|----------|
| Acrobatics | DEX | ☐ | ___ |
| Animal Handling | WIS | ☐ | ___ |
| Arcana | INT | ☐ | ___ |
| Athletics | STR | ☐ | ___ |
| Deception | CHA | ☐ | ___ |
| History | INT | ☐ | ___ |
| Insight | WIS | ☐ | ___ |
| Intimidation | CHA | ☐ | ___ |
| Investigation | INT | ☐ | ___ |
| Medicine | WIS | ☐ | ___ |
| Nature | INT | ☐ | ___ |
| Perception | WIS | ☐ | ___ |
| Performance | CHA | ☐ | ___ |
| Persuasion | CHA | ☐ | ___ |
| Religion | INT | ☐ | ___ |
| Sleight of Hand | DEX | ☐ | ___ |
| Stealth | DEX | ☐ | ___ |
| Survival | WIS | ☐ | ___ |

## Hit Points & AC
- **Hit Dice**: [CLASS] d[DICE]
- **HP**: ___ / ___
- **AC**: ___ (from armor/class)
- **Initiative**: +___ (DEX modifier)

## Equipment & Resources
- **Armor**: _________________
- **Weapon 1**: _________________ (damage: ___ + ___)
- **Weapon 2**: _________________ (damage: ___ + ___)
- **Backpack Items**: ________________________
- **Gold**: ___ GP
```

#### Pathfinder 2e Character Sheet

```markdown
# Character Sheet [Pathfinder 2e]

## Basics
- **Name**: _________________
- **Ancestry**: _________________  **Heritage**: _________________
- **Background**: _________________
- **Class**: _________________  **Level**: ___
- **Deity/Cause**: _________________

## Ability Scores

| Ability | Score | Modifier | Spell DC | Class DC |
|---------|-------|----------|----------|----------|
| Strength | ___ | ___ | — | — |
| Dexterity | ___ | ___ | — | — |
| Constitution | ___ | ___ | — | — |
| Intelligence | ___ | ___ | — | — |
| Wisdom | ___ | ___ | — | — |
| Charisma | ___ | ___ | — | — |

## Skills (Proficiency: Untrained / Trained / Expert / Master / Legendary)

| Skill | Ability | Proficiency | Modifier |
|-------|---------|-------------|----------|
| Acrobatics | DEX | ___ | ___ |
| Arcana | INT | ___ | ___ |
| Athletics | STR | ___ | ___ |
| Crafting | INT | ___ | ___ |
| Deception | CHA | ___ | ___ |
| Diplomacy | CHA | ___ | ___ |
| Intimidation | CHA | ___ | ___ |
| Lore: ________________ | INT | ___ | ___ |
| Medicine | WIS | ___ | ___ |
| Nature | WIS | ___ | ___ |
| Occultism | INT | ___ | ___ |
| Performance | CHA | ___ | ___ |
| Religion | WIS | ___ | ___ |
| Society | INT | ___ | ___ |
| Stealth | DEX | ___ | ___ |
| Survival | WIS | ___ | ___ |
| Thievery | DEX | ___ | ___ |

## Combat
- **HP**: ___ / ___
- **AC**: ___ (Armor + DEX cap + [CLASS] bonuses)
- **Armor**: _________________  (**Armor Bonus**: +___, **Check Penalty**: ___)
- **Fortitude**: ___ | **Reflex**: ___ | **Will**: ___
- **Initiative**: +___ (DEX modifier)
- **Hero Points**: ___

## Class Features & Feats
- [ANCESTRY FEAT]: _________________
- [1st LEVEL FEAT]: _________________
- [CLASS FEATURE]: _________________

## Spells (if applicable)
- **Focus Points**: ___ / ___
- **Cantrips**: _________________
- **1st Level Spells**: _________________
```

#### Shadowrun 6e Character Sheet

```markdown
# Character Sheet [Shadowrun 6e]

## Basics
- **Name**: _________________
- **Metatype**: _________________  **Archetype**: _________________
- **Street Name**: _________________

## Attributes (Rating 1-6)

| Attribute | Rating | Modifier |
|-----------|--------|----------|
| Body (BOD) | ___ | +___ |
| Agility (AGI) | ___ | +___ |
| Reaction (RXN) | ___ | +___ |
| Strength (STR) | ___ | +___ |
| Willpower (WIL) | ___ | +___ |
| Logic (LOG) | ___ | +___ |
| Intuition (INT) | ___ | +___ |
| Charisma (CHA) | ___ | +___ |

## Special Attributes
- **Essence**: ___ / 6  (1 per cybernetic implant)
- **Edge**: ___ (Metatype base + bonuses)
- **Magic / Resonance**: ___ (if applicable)

## Skills (Rating 1-12)

| Skill | Attribute | Rating | Specialization | Dice Pool |
|-------|-----------|--------|-----------------|-----------|
| Firearms | AGI | ___ | __________ | ___ |
| Piloting: Vehicles | RXN | ___ | __________ | ___ |
| Hacking | LOG | ___ | __________ | ___ |
| Spellcasting | MAG | ___ | __________ | ___ |
| Summoning | MAG | ___ | __________ | ___ |
| Stealth | AGI | ___ | __________ | ___ |
| Athletics | STR | ___ | __________ | ___ |
| Perception | INT | ___ | __________ | ___ |
| Negotiation | CHA | ___ | __________ | ___ |
| | | | | |

## Combat
- **Initiative**: RXN + INT + modifiers = ___
- **Armor Valor**: ___ (base) + ___ (cybernetics) = ___
- **HP**: 8 + (2 × BOD) = ___
- **Drones / Vehicles**: _________________

## Cybernetics & Augmentations
- _________________  (Cost: ___ Essence)
- _________________  (Cost: ___ Essence)

## Resources & Gear
- **Nuyen (¥)**: _________________
- **Primary Weapon**: _________________  (Damage: ___)
- **Backup Weapon**: _________________  (Damage: ___)
- **Armor**: _________________
- **Gear**: _________________
```

### Generate Character Creation Tutorial

Create `draft/SESSION-0-CREATION-GUIDE.md` with step-by-step instructions:

#### For D&D 5e:

```markdown
# Character Creation Guide [D&D 5e]

## Step 1: Choose Race
- Pick from available races
- Note race-based ability modifiers
- Add racial traits & special abilities

## Step 2: Choose Class
- Pick from available classes
- Note class hit dice & armor proficiencies
- Select class features at 1st level

## Step 3: Assign Ability Scores
Method: [Standard Array / Point Buy / Roll 4d6]

Standard Array: 8, 10, 12, 13, 14, 15
- Assign each score to one ability
- Apply racial modifiers (final scores: 3-18)

Recommended Priority for [CLASS]:
1. [Primary] (target 15-17 with racial bonus)
2. [Secondary] (target 13-15)
3. Constitution (target 13+, essential for HP)

## Step 4: Calculate Modifiers
- Take each ability score
- Subtract 10
- Divide by 2 (round down)
- This is your modifier

## Step 5: Record Saving Throws
- For each ability where your class has proficiency, add your Proficiency Bonus to the modifier

## Step 6: Select Skills (Proficiency Bonus Depends on Level)
- Choose [CLASS-SPECIFIC COUNT] skills to be proficient in
- Add Proficiency Bonus to those skill checks

## Step 7: Choose Equipment & Background
- Pick starting equipment package for your class, OR
- Select individual items (with GM approval)
- Choose a background (gain 2 additional skill proficiencies)

## Step 8: Calculate Final Numbers
- HP: [CLASS_HD] + CON modifier (minimum 1)
- AC: 10 + DEX modifier (or armor + DEX cap)
- Initiative: DEX modifier
- Proficiency Bonus: +2 (1st level)

## Step 9: Create Details
- Personality traits
- Ideals
- Bonds
- Flaws
```

#### For Pathfinder 2e:

```markdown
# Character Creation Guide [Pathfinder 2e]

## Step 1: Choose Ancestry & Heritage
- Pick ancestry (Human, Dwarf, Elf, etc.)
- Apply ancestry ability bonuses (+2 to two abilities, -2 to one if applicable)
- Choose heritage for additional benefits

## Step 2: Choose Background
- Grants 2 trained skills
- Usually provides narrative context

## Step 3: Choose Class
- Records trained & expert skills from class
- Tracks class features & feats

## Step 4: Allocate Ability Scores
All abilities start at 10. Make 4 ability boosts:
- Boost 2 abilities by +2 each (priority: your class's main attributes)
- Boost 1 ability by +2, gain +8 HP (alternative boost)

Final scores usually range 8-18.

## Step 5: Record Skills
- Trained (from background + class): +3 + ability modifier
- Expert (from class): +6 + ability modifier
- Untrained: +0 + ability modifier

## Step 6: Calculate Defenses & HP
- HP: [CLASS_BASE] + 8 + (CON modifier × Level)
- AC: 10 + DEX modifier + armor bonus (capped)
- Fortitude: CON modifier + [CLASS bonuses]
- Reflex: DEX modifier + [CLASS bonuses]
- Will: WIS modifier + [CLASS bonuses]

## Step 7: Select Feats & Abilities
- 1st-level ancestry feat
- 1st-level class feat
- 1st-level general feat

## Step 8: Spellcasting (if applicable)
- Record spells & focus points
- Note spell attack/save DCs

## Step 9: Finalize Equipment & Resources
- Starting wealth: [depends on background]
- Acquire armor, weapons, adventuring gear
- Establish relationships with other PCs
```

#### For Shadowrun 6e:

```markdown
# Character Creation Guide [Shadowrun 6e]

## Step 1: Choose Metatype & Archetype
- Metatype: Human, Elf, Dwarf, Orc, Troll
- Archetype: Street Samurai, Rigger, Decker, Shaman, Sorcerer, Face, Physad

## Step 2: Distribute Priorities
Allocate 5 priorities across categories (A=best, E=worst):

- **Metatype**: A (Troll/Orc power) → E (Human flexibility)
- **Attributes**: A (start 4 in each) → E (start 2 in each)
- **Magic / Resonance**: A (full magic) → E (no magic)
- **Skills**: A (36 points) → E (10 points)
- **Resources**: A (450,000¥) → E (50,000¥)

## Step 3: Set Attributes
Base each attribute at 1. Distribute priority points:
- A: +2 to each (start at 4)
- B: +1 to six attributes, +2 to two attributes
- C: +1 to four attributes, +2 to one
- D: +1 to three attributes
- E: (remain at 2)

Record modifiers for each (Rating - 1).

## Step 4: Select Magic (if not E Priority)
- Mages: Record spells, drain resistance
- Shamans: Select spirit type, summoning
- Adepts: Select powers, power points
- No magic: Skip this step

## Step 5: Distribute Skill Points
Allocate points from priority:
- A: 36 points (max 6 per skill)
- B: 25 points
- C: 16 points
- D: 10 points
- E: 6 points

Choose specializations (+2 to specific skill applications).

## Step 6: Calculate Derived Attributes
- Initiative: RXN + INT (+ mods)
- Armor Rating: base + cybernetics
- HP: 8 + (2 × BOD)
- Essence: 6.0 (reduced by cybernetics)

## Step 7: Select Cybernetics (Resources Priority)
- Street Samurai: cyberware for combat (datajack, reaction enhancer, weapon mount)
- Rigger: vehicle modifications (vehicle control rig)
- Decker: cyberdeck & hacking programs
- Mage: none recommended (essence cost reduces magic)
- Others: situational augmentations

Each point of Essence reduces Magic/Resonance by 0.2.

## Step 8: Acquire Gear & Weapons
- Resources A: Premium gear, vehicle
- Resources B: Good gear, advanced weapon
- Resources C: Standard gear, reliable weapon
- Resources D: Basic gear, budget weapon
- Resources E: Minimal gear, improvised weapon

## Step 9: Calculate Dice Pools
For each skill: Attribute + Skill + specialization (if applicable) = total dice pool
- Success: 1+ hits on d6 rolls (5-6 = hit)
- Glitch: 2+ ones rolled (critical failure if all ones)
```

### Generate Starting Equipment & Resources

Create `draft/SESSION-0-EQUIPMENT-CHECKLIST.md` with:

- Class-specific starting equipment packages
- Suggested gear for first session
- Resource allocation by priority/class
- Carry capacity & weight limits

### Validate Character Build Consistency

Verify:
- ✓ All ability scores within valid range for ruleset
- ✓ All skills use correct ability modifiers
- ✓ Proficiency bonuses applied correctly
- ✓ HP calculated correctly (class hit die + CON mod)
- ✓ AC calculated correctly (armor + DEX cap or class-specific)
- ✓ Spellcasting (if applicable) has correct DC calculations
- ✓ Special abilities match class features (no contradictions)
- ✓ Starting equipment is within budget constraints
- ✓ (Shadowrun 6e): Essence total ≥ 0 after cybernetics

---

**Auto-activated when**: `SESSION.is_rpg == true` (either "tabletop" or "computer")

### RPG Prose Requirements

**TABLETOP RPG Node Context** (Session-Based):

At the top of each drafted node, include **GM Notes**:

```markdown
## GM Notes [TABLETOP]

**Session**: Session [N] | **Duration**: ~[minutes] | **Difficulty**: [Easy/Medium/Hard]
**NPCs Present**: [NPC1] ([Class/Level]), [NPC2] ([Class/Level])
**Encounter**: [Type: Combat CR-[X] / Social / Investigation / Puzzle / Hybrid]
**Key Variables**: [var1], [var2], [var3]
**Skill Checks**: [Skill DC] — Success: [outcome]; Failure: [outcome]
```

**Skill Check Narration** (D&D 5e example):
```markdown
The guard's expression is unreadable.

[MECHANIC:SKILL check=insight dc=12 success_text="He's nervous" fail_text="He maintains composure"]

**DC 12+ (Success)**: His jaw tightens—he's guilty.
**DC < 12 (Failure)**: The captain's face reveals nothing.
```

**Companion Reaction** (if present):
```markdown
[if thorne_approval >= 50]
  THORNE: "This is a good plan." [MECHANIC:TRUST npc=thorne delta=+5]
[elif thorne_approval >= 0]
  THORNE: "I'll follow your lead."
[else]
  THORNE: "I can't support this." [MECHANIC:TRUST npc=thorne delta=-5]
```

**Faction Reputation Announcement**:
```markdown
[MECHANIC:COUNTER variable=guard_faction_rep delta=+10]
The Guard Captain nods. "You've earned our trust."
```

---

**COMPUTER GAME RPG Playthrough Context** (Playstyle-Based):

Each node should indicate playstyle routes:

```markdown
## Routing [COMPUTER]

**Available Paths**:
- Combat: Direct fight → [NODE-045]
- Dialogue: Persuade → [NODE-046]
- Exploration: Sneak → [NODE-047]

**Difficulty Scaling**:
- Easy: 2 enemies, AC 15
- Normal: 3 enemies, AC 17
- Hard: 4 enemies, AC 19
```

**Skill Check Consequences** (branching by success/failure):
```markdown
**Persuasion Check (DC 12 - Dialogue playstyle)**
Success → [NODE-046 PERSUADE]
Failure → [NODE-045 COMBAT]
```

**Companion Approval** (with gate):
```markdown
[COMPANION:THORNE approval=60]
THORNE: "I trust you." [Approval: +5]
```

**Difficulty-Scaled Narration**:
```markdown
[if difficulty == hard]
  Three guards block the passage. A fourth emerges from shadows.
[else]
  Two guards block the passage.

[MECHANIC:ENCOUNTER difficulty_scale=1.2]
```

**Accessibility Flags**:
```markdown
[ACCESSIBILITY: colorblind_mode, audio_cues, timer=adjustable]
Solve the light puzzle (Normal: 60s | Extended: 90s)
```

---

**Ruleset-Specific Prose** (D&D 5e / Pathfinder 2e / Shadowrun 6e):

**D&D 5e**:
- Skill DCs 5-20 with tier labels (Easy 10-12, Hard 16-18, Very Hard 19-20)
- Spell/ability references with proper notation
- Magic item rarity notes (Common, Uncommon, Rare, Very Rare, Legendary)
- Companion class/level if relevant

**Pathfinder 2e**:
- Skill DCs 10-50+ with PF2e tier language
- Degree of Success outcomes (Crit Success / Success / Failure / Crit Fail)
- Hero Point opportunities if available
- Ancestry/background implications for skill checks

**Shadowrun 6e**:
- Dice pools with [Pool size: Skill + Attribute]
- Street / Matrix / Astral routing with distinct mechanics
- Karma / Street Cred / Edge spending opportunities
- Glitch notation for 2+ ones rolled

---

### NPC Dialogue Tags (RPG-Specific)

Use consistent NPC tags matching `npc-roster.md`:

```markdown
[GUARD_CAPTAIN]:
"You're asking the wrong questions."

[THORNE]:
"Let me handle this."

[BRIGAND_LEADER]:
"Kill them now."
```

**Validation**:
- All NPC dialogue tags must match `npc-roster.md` names
- Each NPC uses distinct voice from character profile
- Multi-character scenes show reactions in sequence (primary responder, then others)

---

### Ending Gate Tracking (RPG-Specific)

In Choices section, indicate ending implications:

```markdown
## Choices

- [Help the Guard](NODE-045)
  <!-- Effect: Guard gains trust | guard_rep +10 | Enables: Just Ruler | Blocks: Shadow Broker -->

- [Side with Temple](NODE-046)
  <!-- Effect: Temple gains trust | temple_rep +10 | Enables: Sacred Path | Blocks: Secular Authority -->
```

**Format**: `<!-- Effect: [narrative] | [var delta...] | Enables: [ending] | Blocks: [ending] -->`

---

### RPG Quality Checklist (Platform & Ruleset-Specific)

**All RPG Contexts**:
- ✓ All skill checks have explicit success/failure narration
- ✓ All companion approvals shown when companion present
- ✓ All faction reputation changes announced by NPCs
- ✓ All NPC dialogue uses correct character voice from profile
- ✓ All choices match outline targets and consequences
- ✓ Ending paths are clear (which choice leads where)

**Tabletop-Specific**:
- ✓ GM Notes section present with session #, duration, difficulty
- ✓ Encounter CRs appropriate to outlined party level
- ✓ Skill check DCs fall within system range (D&D 5e: 5-20; PF2e: 10-50+; SR6e: pool size)
- ✓ Combat triggers are foreshadowed, not arbitrary
- ✓ Session pacing: assumes 2-4 hours per session

**Computer Game-Specific**:
- ✓ Playstyle routes documented (all three playstyles reach same beat)
- ✓ Difficulty scaling variants described (Easy/Normal/Hard)
- ✓ Accessibility features documented (colorblind, audio, motor, cognitive)
- ✓ Dialogue branches are manageable (<10 immediate choices)
- ✓ No difficulty locks (all content completable on all difficulties)

**D&D 5e-Specific**:
- ✓ Skill DCs in range 5-20 with clear tier language
- ✓ Spell references accurate and mechanical implications noted
- ✓ Magic item rarity matches party level
- ✓ Companion class/level noted if present

**Pathfinder 2e-Specific**:
- ✓ Skill DCs in range 10-50+ per PF2e scale
- ✓ Degree of Success outcomes documented (all four results)
- ✓ Hero Point usage documented if available
- ✓ Ancestry/background implications acknowledged

**Shadowrun 6e-Specific**:
- ✓ Dice pools documented with Skill + Attribute notation
- ✓ All three routing options (Street/Matrix/Astral) genuinely available
- ✓ Karma economy tracked (no excessive spending in single node)
- ✓ Glitch risk noted for critical rolls

---

### RPG Warnings (Auto-Flagged for Author Review)

**General**:
- ⚠️ `[SKILL CHECK MISSING OUTCOME]` — Skill check present but no success/failure narration
- ⚠️ `[APPROVAL CHANGE NOT ANNOUNCED]` — Approval delta present but NPC doesn't acknowledge
- ⚠️ `[REPUTATION CHANGE NOT ANNOUNCED]` — Rep delta present but NPC doesn't acknowledge
- ⚠️ `[NPC VOICE INCONSISTENT]` — Dialogue doesn't match character profile
- ⚠️ `[CHOICE LACKS ENDING CONTEXT]` — Can't tell which ending this choice enables/blocks

**Tabletop-Specific**:
- ⚠️ `[ENCOUNTER CR MISALIGNED]` — CR doesn't match outlined party level
- ⚠️ `[COMBAT UNJUSTIFIED]` — Combat triggered without narrative setup
- ⚠️ `[SESSION PACING LONG]` — Node may exceed 2-4 hour session assumption

**Computer Game-Specific**:
- ⚠️ `[PLAYSTYLE UNBALANCED]` — One playstyle path takes 3× longer than others
- ⚠️ `[DIFFICULTY LOCKS CONTENT]` — Hard mode makes story progression impossible
- ⚠️ `[ACCESSIBILITY MISSING]` — Puzzle/timed sequence lacks accessibility features

**Ruleset-Specific**:
- ⚠️ `[DC OUT OF RANGE]` — D&D 5e DC > 20, PF2e DC < 10 or > 50+, Shadowrun pool < 2
- ⚠️ `[DEGREE OF SUCCESS INCOMPLETE]` — PF2e skill check missing outcome for one tier
- ⚠️ `[ROUTING NOT BALANCED]` — Shadowrun Street/Matrix/Astral routes have unequal rewards

---

**The implement phase MUST:**
- Preserve all outline information (variables, hooks, choices, consequences)
- Document consequences as comments in the Choices section
- Transfer all mechanic hooks from outline to prose
- Maintain outline structure and gating conditions
- Write prose that matches the beat summary and narrative purpose

Consequences are the **bridge** between mechanical outcome and narrative meaning. They must be preserved.
