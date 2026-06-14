---
description: Generate editable node outline files from plan.md. Authors review and approve each outline before AI drafting begins, or mark SKIP to write their own prose.
handoffs:
  - label: Start Drafting
    agent: speckit.implement
    prompt: Draft nodes from approved outlines
    send: true
  - label: Check Branch Structure First
    agent: speckit.plan
    prompt: Node targets or branch logic conflict with the flowmap. Please review and fix it.
    send: true
---

# speckit.outline

Generate a node outline (`outlines/NODE-NNN.md`) for one or more nodes. Outlines must be reviewed and approved before `speckit.implement` will draft the node.

## User Input

```text
$ARGUMENTS
```

You **MUST** consider the user input before proceeding (if not empty). Accepted arguments:
- `[NODE_ID]` � generate outline for a single node (e.g. `NODE-003`)
- `[NODE_ID] [NODE_ID] ...` � generate outlines for a list of nodes
- `--act [N]` � outline all nodes for a given act
- `--force` � regenerate an existing outline (overwrite)
- `--batch` / `--all` — generate outlines for ALL nodes listed in `plan.md` that do not yet have an outline- `--mode rpg` — include RPG-specific outline sections (skill checks, companion interactions, faction effects, ending gates)- *(no argument)* — outline the next unoutlined node from `plan.md`

## Pre-Execution Checks

**Check for extension hooks (before outline generation)**:
- Check if `.specify/extensions.yml` exists in the project root.
- If it exists, read it and look for entries under the `hooks.before_outline` key.
- Process as standard hook block (Optional/Mandatory). Skip silently if absent.

Then:
1. Confirm `specs/[FEATURE_DIR]/plan.md` and `.specify/memory/constitution.md` exist.
2. For each requested node, verify it appears in `plan.md` — warn if not found.
3. **Skip any node that already has an outline file with `status: APPROVED` or `status: SKIP`** � never overwrite approved or skipped outlines unless `--force` is set.
4. Confirm `specs/[FEATURE_DIR]/variables.md` exists � hooks cannot be declared without it.

## Outline

**Goal**: Generate structured, decision-complete node outlines in `outlines/` that give the author all the information needed to approve the node before drafting begins.
**Language Rule**: All node outlines MUST be generated in English (`en`) by default, regardless of any `[LANGUAGE]` setting in the constitution. This stage remains in English to facilitate author review against project specifications.

### Execution Steps

1. **Setup**: Run `{SCRIPT}` from repo root and parse JSON for spec file paths.

2. **Load source documents**:
   - **Required**: `specs/plan.md` (node graph, branch dependencies, act breakdown), `specs/spec.md` (NPC profiles, variable registry, research gaps)
   - **Required**: `.specify/memory/constitution.md` (enabled mechanics list, world rules, tone, target platform, `prose_profile`)
   - **Required**: `specs/mechanics.md` (hook schemas, tier levels, translations, parameter definitions for all declared hooks including newly added ones)
   - **Required**: `specs/endings.md` (ending IDs, variable gates, thematic statements) -- needed to validate all choice targets
   - **Required**: `specs/characters.md` index + `specs/characters/` profiles (NPC trust thresholds, state behaviors, bark lines, dialogue consistency)
   - **Required if style_mode is humanized-ai**: `.specify/memory/craft-rules.md` (to tune beat language and dialogue register per active prose profile)
   - **Optional**: `specs/variables.md` (declared variables with types and value ranges) -- validate Variables Read and Variables Set sections
   - **Optional**: `specs/glossary.md` (terminology registry) -- load if present; check outline for any terminology that should be flagged for consistency checking during drafting
   - **Optional**: `specs/locations.md` (sensory anchors, location rules) -- load if present; populate location context in outline if this node takes place in a key location
   - **Optional**: `specs/themes.md` -- load if present; use to populate the Thematic work field in the outline Beat Summary: match the node's act to the Thematic Arc by Act table, and check whether any registered motif (MO-NNN) or symbol has a planned occurrence in this node
   - **Optional**: `specs/world-building.md` (location sensory anchors, world rules)   - **Optional (if quest mechanics enabled)**: `specs/world/locations.md` (location index), `specs/world/[location-name]/passages.md` (available passages/encounters at each location), `specs/world/[location-name]/[quest-id]/` (quest outlines organized by location)   - Note any missing required documents -- abort with clear error if `specs/endings.md` or `specs/characters.md` missing
   - Note any missing optional documents � affected outline sections are marked `[TBD � populate <document>]`

3. **Determine target nodes**:
   - If `$ARGUMENTS` is `--batch` or `--all`: find ALL nodes in `plan.md` that do not yet have an outline file and process them in order.
   - If `$ARGUMENTS` is empty: find the first node in `plan.md` that has no outline file yet.
   - If `$ARGUMENTS` is a node ID or list: use those nodes.
   - If `$ARGUMENTS` is `--act N`: use all nodes in that act without an existing outline file.
   - Skip any node already outlined with `status: APPROVED` or `status: SKIP` (unless `--force`).

4. **For each target node, generate an outline file**:

   **Output path**: `outlines/[NODE_ID].md`

   Use `templates/node-outline-template.md` as the base structure. Populate each section from the source documents:

   **Frontmatter** — pull from `plan.md` node entry:
   - `node_id`, `title`, `act`, `status: DRAFT`, `pov` (from `.specify/memory/constitution.md` default or node override)

   **Beat Summary** � derive from the flowmap node entry:
   - 2�4 sentences: what happens in this node, what the player is doing or deciding
   - Narrative purpose: `decision / consequence / revelation / setup / hub / transition / climax / ending`
   - Tension level: 1�10 with brief rationale

   **Variables Read** � derive from flowmap branch conditions into this node:
   - Each variable used as a gate or prose condition, with expected value and source node
   - Flag any variable not yet declared in `variables.md` with `[UNDECLARED]`

   **Variables Set** — derive from flowmap annotations and `.specify/memory/constitution.md` hook schemas:
   - Each variable changed by this node, with hook type, new value/delta, and trigger condition
   - Flag any variable not yet declared in `variables.md` with `[UNDECLARED]`

   **Choices** — derive all outgoing edges from `plan.md`:
   - Minimum 2 choices for non-terminal nodes; 0 for ending nodes
   - Each choice: label, condition (if conditional), target node ID, narrative consequence
   - Default path if no conditional choices are met

   **Dialogue Tree** — *only if node is flagged `(dialogue-centric)` or `(mixed)` in plan.md*:
   - Structure player dialogue options and NPC responses within the node
   - Each dialogue choice includes: player phrase, NPC responses by character, gating/variable effects
   - Include all NPCs present in this node; each NPC uses their correct dialogue register from `specs/characters/[NPC_ID].md` Section VIII
   - Multi-party reactions: both/all NPCs respond to the player's dialogue choice (shown in sequence)
   - Dialogue sub-branches: indicate if a dialogue choice continues in-node or branches to a different node
   - If no structured dialogue tree is needed, mark as `None`

   **Mechanic Hooks Summary & Checklist** — Identify all mechanics relevant to this node:
   
   1. **First, derive explicit hooks** from `specs/mechanics.md` and flowmap annotations:
      - All hooks already triggered: type, tier (1 or 2), variable, action, timing
      - Include any custom hooks added via `speckit.mechanics declare`

   2. **Then, use the Mechanic Hooks Checklist** (in template) to identify forgotten mechanics:
      
      For each node type, prompt the author through these common patterns:
      - **Dialogue-centric** (dialogue-heavy prose_profile or dialogue-centric flag):
        - ✓ CHOICE_MEMORY (record which dialogue option player chose)
        - ✓ TRUST (dialogue choice should affect NPC trust by ±N)
        - ✓ NPC_STATE (dialogue can change NPC mood or relationship tier)
        - ✓ FLAG (dialogue might reveal secrets or flag new knowledge)
        
      - **Quest/Task hub** (setup or hub narrative purpose):
        - ✓ COUNTER (track active quests, attempts, or rounds)
        - ✓ INVENTORY (check prerequisites, award completion items)
        - ✓ VISITED (mark location explored)
        
      - **Investigative/Mystery** (contains clue discovery or evidence gathering):
        - ✓ CLUE (discover evidence piece)
        - ✓ INVENTORY (collect physical evidence)
        - ✓ COUNTER (track evidence collected, theories tested)
        
      - **Timed challenge** (tension level 7+, obstacle or puzzle):
        - ✓ TIMER (start countdown or ticking timer)
        - ✓ COUNTER (track attempts or rounds remaining)
        - ✓ ENDING_CONDITION (major success/failure consequence)
        
      - **Choice consequence** (decision node with multiple paths):
        - ✓ TRUST (choice affects NPC relationships)
        - ✓ FLAG (choice unlocks/locks paths)
        - ✓ NPC_STATE (NPC reacts to choice)
        - ✓ ENDING_CONDITION (choice pushes toward specific ending)
        
      - **Any node with player resources (items, money, health)**:
        - ✓ INVENTORY (track items acquired/lost)
        - ✓ CURRENCY (track resources spent/gained)

   3. **Populate the template's Mechanic Hooks Checklist**: 
      - Check the boxes for all mechanics that should apply to this node
      - Fill in the summary table at the top with the concrete hooks
      - Reference "Common Hook Combinations" section if uncertain

   **Branch Logic Notes** � pull from flowmap annotations:
   - Any complex gate logic, reachability conditions, or POV overrides
   - If this node is only reachable via specific upstream variable states, document them here

   **Game Bible Compliance Notes** — scan `.specify/memory/constitution.md` for:
   - Any mechanic or hook constraints relevant to this node
   - Platform/engine limits on choice count or variable types
   - POV rules or tone requirements that apply

   **Deviations from plan.md** — default to `None`. Only populate if the outline generation process identified an inconsistency (e.g. a variable read in this node that no upstream node sets).

   **Ending Gate Validation** — derive from `specs/endings.md`:
   - For each choice in the Choices table:
     - If the target node ID is a terminal node: verify it maps to a valid `END-NNN` entry in `specs/endings.md`
     - Flag any choice target that is not in `plan.md` as `[MISSING NODE]`
     - Flag any ending node reference that has no corresponding `END-NNN` in `specs/endings.md` as `[UNREGISTERED ENDING]`

   **Location & Sensory Context** — load from `specs/locations.md` if present:
   - If this node's title or POV mentions a location, find that location in `specs/locations.md`
   - Populate a new **Setting Anchors** field in the outline with sensory and rule details from the location profile
     - E.g., "Sanctuary Station: sterile white walls, hum of life support, restricted entry"
   - If location is absent from locations.md, mark as `[LOCATION PROFILE NEEDED]`

   **Quest-Based Location Passages** — if quest mechanics enabled in `.specify/memory/constitution.md`:
   - Check if this node appears in `specs/world/[location-name]/passages.md` or `specs/world/[location-name]/[quest-id]/stage-N.md`
   - If yes: populate a **Quest Context** field in the outline showing:
     - Which quest(s) this node belongs to (e.g., QUEST-guild-contract)
     - Which stage(s) of the quest (e.g., Stage 2 of 3)
     - Opening condition (what must be true before this passage is available, e.g., `$quest_guild_contract_stage == 1 and $character.intelligence >= 6`)
     - Closing condition (what becomes true after this passage completes, e.g., `$quest_guild_contract_stage = 2`)
   - Mark any quest dependencies that are not yet registered in `variables.md` as `[QUEST VAR UNDECLARED]`
   - This field is optional for non-quest nodes; omit if this node is not part of a quest

   **Terminology Cross-Check** — load from `specs/glossary.md` if present:
   - Scan beat summary and choice labels for any specialized terminology
   - If any term appears in both the outline and `specs/glossary.md`, cross-reference the definition in the Glossary section of the outline
   - Flag any term used that is not in the glossary (for writer awareness during drafting) as `[GLOSSARY NOTE]`

5. **Outline quality rules**:
   - Every beat must be one sentence � no prose
   - If a `[NEEDS CLARIFICATION]` marker is present in the flowmap entry, propagate it into the outline � do not invent a resolution
   - A variable listed in Variables Read must be set by at least one upstream node in `plan.md` — flag otherwise
   - No choice may target a node ID not present in `plan.md`
   - The outline is a brief, not a draft � no narrative prose, no dialogue text

6. **Report**: List all outline files created with their output paths and `status: DRAFT`. Include a per-node summary: `[NODE_ID] [title] — [N] beats, [N] choices, [N] variables set, [ending gates], act [N]`. Flag any:
   - `[UNDECLARED]` variables
   - `[MISSING NODE]` choice targets
   - `[UNREGISTERED ENDING]` terminal nodes
   - `[LOCATION PROFILE NEEDED]` locations not in locations.md
   - `[GLOSSARY NOTE]` terminology not in glossary.md
   - Propagated `[NEEDS CLARIFICATION]` markers
   
   Remind the author to:
   - Review each outline file and edit beats, choices, and variable tables as needed
   - **Complete the Mechanic Hooks Checklist** for each node — check all applicable hook types (dialogue-centric nodes should include CHOICE_MEMORY + TRUST + NPC_STATE; quest hubs should include COUNTER + INVENTORY; timed challenges should include TIMER; etc.)

---

## RPG-Specific Outline Extension (--mode rpg)

**When activated**: If `--mode rpg` or `.specify/memory/constitution.md` declares `game_system: "d5e"` (or other RPG system), populate these additional outline sections:

### RPG Beat Summary (D&D 5e / PBTA / FATE / Blades)

Add to the standard Beat Summary:

- **Session:** Which of 15 sessions (for campaign-length RPGs)
- **Story Phase:** Act 1/2/3, campaign checkpoint
- **Pacing:** Combat / Social / Exploration / Investigation (estimated %)

### Skill Checks (RPG-Specific)

**For each skill check available in this node:**

| Skill | DC | Ability | Success Outcome | Failure Outcome |
|---|---|---|---|---|
| [SKILL_NAME] | [N] | [ABILITY] | [2-3 word consequence] | [2-3 word consequence] |

Example:
| Insight | 12 | Wisdom | guard_opens_up | guard_distrusts_party |
| Persuasion | 14 | Charisma | persuaded | combat_triggered |

**Validation**: 
- Every skill check DC must be 5-20 (D&D scale) or 0-4 (PBTA scale) or match system defaults
- Every skill check must actually affect story (not just "gain information you already have")

### Companion Interactions (RPG-Specific)

**If any companion NPCs are present or referenced:**

| Companion | Approval Gate | Reaction | Effect |
|---|---|---|---|
| [NAME] | if_approval_ge_[N] | [reaction_text] | [story_consequence] |

Example:
| Thorne | if_approval >= 50 | "This could work..." | thorne_suggests_alternative |
| Sister Mercy | if_approval < 0 | "I can't support this" | sister_mercy_leaves_party |

**Validation**:
- Approval gates must fall within companion's -100 to +100 range (D&D 5e standard)
- Romance gates (if applicable) should use thresholds from `.specify/memory/constitution.md`
- Each companion should have a potential approval change for this node (+/- N)

### Faction Effects (RPG-Specific)

**If any faction reputation changes occur:**

| Faction | Base Rep | Change Trigger | Rep Change | Effect |
|---|---|---|---|---|
| [FACTION] | [N] | if_[choice] | +/-[N] | [story consequence] |

Example:
| Guard | 20 | if_party_helps | +10 | guard_rep_30_unlocks_allied_dialogue |
| Temple | 10 | if_party_hides_evidence | -15 | temple_rep_-5_damages_recruitment |
| Syndicate | 0 | if_party_investigates | -5 | syndicate_rep_-5_increases_heat |

**Validation**:
- All reputation changes must be cumulative across 15 sessions (sum to realistic totals)
- Ending gates (e.g., "Just Ruler" requires guard_rep >= 50) must be reachable
- No single node should give more than +/-25 reputation per faction

### Ending Gate Status (RPG-Specific)

**Current ending gate viability for this node:**

| Ending Name | Active? | Gate Requirements | Status After This Node |
|---|---|---|---|
| Just Ruler | Yes | guard_rep >= 50, temple_rep >= 60, syndicate_rep < 20 | On track (guard +10 this node) |
| Shadow Broker | Yes | syndicate_rep >= 70, guard_rep < 0 | Off track (syndicate -5 this node) |

**Validation**:
- At least 2-3 endings must remain viable through midgame (Session 8)
- No ending should be made impossible until Session 13+
- Each ending must require distinct choice combinations (not just random gates)

### RPG Quality Checklist

When `--mode rpg` is active, add to outline validation:

- ✓ All referenced variables exist in variables-d5e.md (or system-specific variables file)
- ✓ All skill check DCs fall within system range (5-20 for D&D, 0-4 for PBTA, etc.)
- ✓ All companion approvals fall within -100 to +100 range
- ✓ All faction reps fall within -100 to +100 range
- ✓ Ending gates are reachable (no impossible combinations)
- ✓ Reputation changes are cumulative and realistic for 15-session arc
- ✓ Combat encounters (if any) have CR appropriate to party level at this session
- ✓ Skill checks match session-appropriate DC progression
- ✓ No companion can be recruited twice or appear after death without resurrection

### RPG-Mode Warnings

Flag for author review:

- ⚠️ `[UNBALANCED SKILL CHECKS]` — Node has only Charisma or only Strength checks (should diversify)
- ⚠️ `[COMPANION TIMELINE CONFLICT]` — Companion has approval gate but hasn't been recruited yet
- ⚠️ `[ENDING GATE UNREACHABLE]` — This ending can no longer be reached after this node's reputation changes
- ⚠️ `[REPUTATION SPIKE]` — Single node changes faction rep by > +25 or < -25
- ⚠️ `[SKILL CHECK DISCONNECT]` — Skill check result doesn't actually change story (purely informational)

7. **Check for extension hooks** (after generation): check `hooks.after_outline`.

---

## SugarCube/Twine Considerations

When the target engine is SugarCube (from `.specify/memory/constitution.md` `engine: sugarcube`), apply these additional outline rules to ensure generated outlines produce draftable Twee passages:

### ✅ DO

- **Use simple, linear dialogue** — SugarCube handles branching well; avoid deeply nested conditions
- **Keep choice gates to 1-2 attributes max** — e.g., `requires: $character.wisdom >= 6` is clear; `requires: ($character.wisdom >= 6 AND $character.power <= 4 AND not $flags.x)` gets hard to read and test
- **Use inventory checks sparingly** — Each check adds UI complexity in SugarCube inventory widgets
- **Group related choices together** — SugarCube renders best with 2-4 choices per node
- **Document variable changes clearly** — Outline should show `$character.wisdom +1`, `$inventory.gold -5`, etc.

### ❌ DON'T

- **Use attribute ranges that change mid-conversation** — SugarCube doesn't support dynamic range recalculation; write gates based on current-value checks
- **Create more than 1 level of dialogue nesting** — Twee doesn't handle complex nested dialogue trees well; use separate nodes for deep branches
- **Use variables with spaces or special characters** — Stick to `snake_case` (e.g., `$flags.priestess_spoken_to`, not `$flags."priestess spoken to"`)
- **Gate choices on more than 2 unrelated variables** — Players can't mentally track complex multi-variable gates; simplify or merge conditions

