---
description: Generate a game story brief from a game concept or high-level brief.
handoffs:
  - label: Clarify Design Elements
    agent: speckit.clarify
    prompt: Clarify the open questions in this game story brief
    send: true
  - label: Build Game Bible
    agent: speckit.constitution
    prompt: Generate the game bible from the approved game story brief
---

# speckit.specify

Turn a game concept brief into a structured game story brief (`spec.md`).

## User Input

```text
$ARGUMENTS
```

You **MUST** consider the user input before proceeding (if not empty).

Optional flags:
- `--update` — revise an existing `spec.md` in the `specs/` directory rather than generating from scratch

## Pre-Execution Checks

**Check for extension hooks (before narrative design doc creation)**:
- Check if `.speckit/extensions.yml` exists in the project root.
- If it exists, read it and look for entries under the `hooks.before_specify` key.
- If the YAML cannot be parsed or is invalid, skip hook checking silently and continue normally.
- Filter out hooks where `enabled` is explicitly `false`. Treat hooks without an `enabled` field as enabled by default.
- For each remaining hook with no `condition` field or a null/empty `condition`, output the appropriate hook block (Optional or Mandatory), then wait for mandatory hook results before continuing.
- If no hooks are registered or `.speckit/extensions.yml` does not exist, skip silently.

**Document checks**:
1. Does a `.specify/memory/constitution.md` already exist?
   - If yes: warn — "A game bible exists. Run `speckit.specify --update` to revise the story brief; avoid contradicting approved world rules."
   - **RPG-specific**: Read the constitution to extract `[PLATFORM]` (Tabletop/Computer Game) and `[RULESET]` (D&D 5e/Pathfinder/etc.). Store these for use in section 5.
2. Does a `specs/` directory already contain a `spec.md` anywhere?
   - Check both `specs/spec.md` (flat — incorrect placement from a previous failed run) and `specs/*/spec.md` (correct subdirectory placement).
   - If either exists and `--update` not set: ask user to confirm overwrite or use `--update`.
   - If `specs/spec.md` exists (flat): warn — "spec.md is in the wrong location. It must be inside a named subdirectory (e.g. specs/001-hollow-crown/spec.md). This run will create the correct subdirectory and write there."

## Outline

1. **Generate a concise short name** (2–4 words) for the game being specified:
   - Use action-noun or noun-noun format when possible (e.g., `hollow-crown`, `last-signal`, `iron-veil`)
   - Preserve setting terms and genre keywords
   - Keep it short enough to serve as a directory reference

2. **Create the spec subdirectory** (REQUIRED — never write spec.md directly into `specs/`):
   - Ensure `specs/` exists; create it if absent.
   - Read `.speckit/init-options.json` if it exists and check the `branch_numbering` field.
   - **Default Naming**: Scan `specs/` for existing numbered directories (format `NNN-`) and use the next sequential number (zero-padded to 3 digits). Also check current git branches for the highest number used. Use the higher of the two + 1. If `specs/` is empty and no git branches indicate a number, use `001`.
   - **Timestamp Override**: Only use `YYYYMMDD-HHMMSS` as a prefix if `branch_numbering` is explicitly `"timestamp"` or `TIMESTAMP`.
   - **Series naming**: if `specs/series-bible.md` already exists and this game is non-standalone, incorporate the entry number into the directory name: `specs/<prefix>-game-<N>-<short-name>/` (e.g., `specs/002-game-2-iron-veil/`). Infer N from the next empty row in `## Games in Series`, or ask the user if the table is not yet populated.
   - Create directory `specs/<prefix>-<short-name>/` (e.g., `specs/001-hollow-crown/`).
   - **CRITICAL**: The spec file MUST be written to `specs/<prefix>-<short-name>/spec.md`. Writing to `specs/spec.md` (without a subdirectory) is WRONG and must never happen.

3. **Copy the game story brief template**:
   - Locate `spec-template.md` using the preset template resolution order
   - Copy it to `specs/<prefix>-<short-name>/spec.md` (inside the subdirectory created in step 2)
   - **Language Rule**: The game story brief MUST be generated in English (`en`) by default, regardless of any `[LANGUAGE]` setting in the constitution.

4. **Parse the concept brief** from `$ARGUMENTS` or user input:
   - Extract: premise, tone, genre, setting, player arc shape, approximate node count, target endings, known NPCs
   - **RPG-specific fields**: Also extract:
     - **For Tabletop**: Party composition (classes, count), level range (start–end), session count, campaign theme (Dungeon Delving, Political Intrigue, etc.), faction count, companion count, difficulty curve
     - **For Computer Game**: Protagonist/party composition, character progression system (level-based, attribute-based, skill-based), expected playstyle (combat-heavy, dialogue-heavy, exploration-heavy, mixed)
   - Flag any missing mandatory fields as `[NEEDS CLARIFICATION: reason]`

5. **Fill spec.md** working through each section systematically:

   - **Logline**: One sentence capturing player character + central goal + primary obstacle + stakes.

   - **Premise**: ~100 words. The dramatic situation and central tension. End with: "The central question: [question]?"

   - **Opening Node Hook**: What the player MUST know, feel, and suspect by the end of Node 1. Plus what is deliberately withheld.

   - **Player Arc (P1)**: 
     - **For Tabletop**: Party's collective arc — shared false belief / wound, collective want vs need, transformation arc across campaign, how party agency is expressed (through skill checks, decisions, combat tactics)
     - **For Computer Game**: Protagonist or party internal wound / false belief, want, need, transformation range (from ? to per ending direction), player agency expression, key contradiction
     - **Ruleset note**: For D&D 5e, key contradiction may involve class mechanics (e.g., rogue's stealth vs honor code)

   - **NPC Arcs (P2/P3)**: Categorize NPCs by type for RPGs:
     - **Recruitable Companions** (Tabletop: party joiners; Computer: characters who can be recruited):
       - Internal wound / false belief, want, need, transformation arc
       - Approval/trust hook name (variable that tracks relationship: -100 to +100 range, recruitment threshold, romance threshold)
       - Conditional outcomes (if alive, if approved ≥ threshold, etc.)
       - Independent arc test (does NPC arc advance even if player ignores them?)
     
     - **Faction Leaders** (NPCs representing major factions):
       - Faction they lead or represent
       - Reputation hook name (variable tracking faction standing)
       - Their personal arc (separate from faction reputation mechanics)
       - Ending impact (which endings require faction rep thresholds?)
     
     - **Quest-Givers & Encounter NPCs** (contextual NPCs):
       - Quest they offer or scene they serve
       - Whether they have a recurring arc or appear once
       - Any approval/reputation hooks they trigger
     
     - **Antagonists / Opposing Forces**:
       - Their arc and transformation (do they change if player befriends them?)
       - Which endings are locked by defeating/sparing them?

   - **Key Relationship Arcs**: Load-bearing player–NPC or NPC–NPC relationships. For each: opens as, stress point, closes as, function (what wound does it force to the surface?).

   - **Branch Structure Overview**: Choose from enum:
     - `linear-with-branches` — single path with local divergence, converges at acts
     - `branching-remerging` — meaningful choice diverges and re-merges at key nodes
     - `fully-branching` — each major choice opens a distinct path to end
     - `hub-and-spoke` — central hub with explorable spokes, returns to hub
     Include: act map (act count, rough node distribution per act, major beat at each act boundary).

   - **Endings Map**: 3–6 planned endings with:
     - Type: `good` / `bad` / `neutral` / `secret` / `true`
     - Rough condition notes (variables / flags that gate this ending)
     - Thematic statement this ending makes

   - **Key Scenes / Nodes**: 5–10 pivotal moments using Given/When/Then format. Each labeled with:
     - Arc served, act placement, branch conditions (if any), variable set
     - These are narrative obligations — they MUST appear in the final game.

   - **RPG-Specific Parameters** (populated based on `[PLATFORM]` and `[RULESET]` from constitution):
     
     **If Platform = Tabletop:**
     - **Party Composition**: Classes/roles and count (e.g., 4 players: Fighter, Rogue, Cleric, Wizard)
     - **Level Progression**: Starting level → ending level (e.g., Level 5 → Level 8)
     - **Session Structure**: Planned session count, average playtime per session, encounters per session
     - **Campaign Theme**: Selected theme (Dungeon Delving, Monster Hunt, Political Intrigue, Heist, Investigation, Curse Breaking, Defense, Mixed). From [campaign-themes-by-system.md](templates/campaign-themes-by-system.md), describe how theme affects encounter types, NPC emphasis, and skill check priorities.
     - **Faction System**: Faction count, reputation tracking (e.g., "3 factions: Guard, Thieves' Guild, Temple; rep range -100 to +100"), ending gates per faction (which endings require faction thresholds?)
     - **Companion System**: Recruitable companion count, approval range, recruitment nodes, conditional outcomes
     - **Difficulty Curve**: Act-by-act difficulty progression (beginner → intermediate → expert), CR target by act (D&D 5e specific)
     - **Ruleset-Specific Mechanics** (if D&D 5e):
       - Encounter CR scaling and XP budget per session
       - Skill check DC distribution and which abilities are emphasized
       - Magic item distribution plan
       - Spell/ability balancing notes
     
     **If Platform = Computer Game:**
     - **Protagonist/Party**: Single protagonist or party of N? Character progression system (level, attribute points, skill trees, class advancement?)
     - **Expected Playstyle**: Distribution estimate (% combat : % dialogue : % exploration : % puzzle-solving). Examples: "60% combat, 20% dialogue, 15% exploration, 5% puzzles"
     - **Player Agency Mechanics**: How do stats, skills, items affect outcomes? Do attribute checks replace narrative choices in any branches? (e.g., "High Charisma may unlock social branch; low Strength may lock combat branch")
     - **Ruleset-Specific Mechanics** (if D&D 5e):
       - Combat difficulty scaling (how does difficulty setting affect enemy AC, HP, damage?)
       - Skill check result spectrum (fail → success → critical success paths)
       - Equipment/spell availability by chapter
     
     **If Ruleset = D&D 5e** (in addition to above):
     - Add table: Expected CR progression by session (Session 1-5: CR 1–3; Session 6-10: CR 4–6; Session 11-15: CR 7–9)
     - Campaign theme implications: "If theme is Political Intrigue, expect 50% social encounters, 30% investigation, 20% combat. If theme is Dungeon Delving, expect 60% combat, 30% exploration, 10% social."

   - **Design Requirements**: Events that MUST exist for this to be this game. Use MUST language. Mark unknowns as `[NEEDS CLARIFICATION: reason]`.
     - **For Tabletop**: Include session structure (e.g., "MUST have 15 sessions; MUST recruit 3 companions by Session 8; MUST reach political climax by Session 12")
     - **For Computer Game**: Include progression gates (e.g., "MUST unlock second party member by Chapter 2; MUST have skill check that bypasses combat encounter")
     - **For D&D 5e**: Include encounter design requirements (e.g., "MUST include at least 2 lair encounters; MUST use at least one faction-specific encounter type")

   - **Act Boundaries & Structural Beats**: Map design requirements to act beats. Include pacing intent.

   - **Key Entities**:
     - Characters table (name, role, first node, arc priority)
       - **For Tabletop**: Add columns for NPC type (Companion / Faction Leader / Quest-Giver / Antagonist), approval/reputation hooks, recruitment node
       - **For Computer Game**: Add column for recruitment/unlocking mechanic
     - Locations table (name, atmosphere note, acts present, notable nodes)
       - **For Tabletop**: Add column for encounter type(s) expected and typical CR
     - Key items table (introduced at, narrative/mechanical payoff, payoff node)
       - **For Tabletop**: Add column for mechanical use (quest item / combat use / skill check modifier)
     - World rules table (inviolable facts — physics, social, technical, mechanical, geography)
     - Research domains table (accuracy requirement per domain)
     - **For Tabletop RPGs only**:
       - Factions table (name, starting reputation, ending reputation ranges, ending gates, key faction NPCs)
       - Companions table (name, recruitment node, approval thresholds, conditional outcomes, ending fates)
     - **For Computer Game RPGs**:
       - Character progression table (name, unlocking mechanic, class/role options, key abilities/skills, level cap or progression path)

   - **World Structure** (RPG-specific — always generate for RPG platform):
     > This section defines the spatial hierarchy: World → Region → Area → Location → Scene.
     > It becomes the seed for `world-map.md` generated by `speckit.plan`.
     > Every named location in the Locations table above must appear in the Region/Area hierarchy below.
     
     - **Spatial Model**: Identify which model applies:
       - `Linear` — Regions unlock in fixed sequence per act (most story-driven RPGs)
       - `Hub-and-Spoke` — Central hub Region with radiating optional Regions (tavern-based adventure, city-hub RPG)
       - `Open-World` — Regions accessible by player choice, gated by content/level
     
     - **Region Table** (one row per top-level Region):
       | Region ID | Region Name | Theme | Acts Present | Unlock Condition | Area Count |
       |---|---|---|---|---|---|
       | REGION-[ShortName] | [Name] | [3-word theme] | Act [N]–[N] | [start / after event] | [N] |
     
     - **Area Table** (one row per Area within each Region):
       | Area ID | Area Name | Parent Region | Area Type | Location Count | Unlock Condition |
       |---|---|---|---|---|---|
       | AREA-[ShortName] | [Name] | REGION-[ShortName] | [dungeon/wilderness/urban] | [N] | [start / quest X] |
     
     - **Initial Spatial Hierarchy sketch** (tree format — expand in `speckit.plan`):
       ```
       REGION-[Name] (unlock: [condition])
       └── AREA-[Name] ([type])
           ├── LOC-[Name] ([location type], [N] scenes)
           └── LOC-[Name] ([location type], [N] scenes)
       ```
     
     - **Notes for planner**: Flag any region with no rest location, any area with no entry route, any location mentioned in the narrative but not yet placed in the hierarchy.

   - **Map Inventory** (NEW for RPG campaigns — if `constitution.md` has `map_format` set to `json` or other):
     
     **Tabletop RPG Maps**:
     - Regional map (travel, faction territories, safe locations): Session(s) intro-end, scope
     - Battle maps (combat encounters): Encounter ID, session, grid size, special terrain, tokens
     - Location maps (investigation, puzzle, social encounters): Location name, session(s), layout notes
     - Player handouts (simplified versions for sharing): Which map(s) simplified, distribution node
     
     **Computer Game RPG Maps** (asset/level layouts):
     - Level/area layouts (environment design): Level name, playstyles accessing (Combat/Dialogue/Exploration), player progression within area
     - Route maps (showing playstyle-specific routes): Which routes merge/diverge, convergence nodes
     - Secret locations (hidden areas): Discovery mechanic, accessibility requirements
     
     Table format (populate for this game):
     
     | Map ID | Name | Type | Session(s) | Size/Grid | Encounters/Locations | Tokens | Player Handout? | Status |
     |--------|------|------|-----------|-----------|-----|--------|-------------|--------|
     | MAP-001 | Goblin Warren | Battle | S3 | 20×20, 5ft | ENC-015 | 8 goblins | Yes (simplified) | [TBD] |
     | MAP-002 | Regional Campaign | Regional | S1–S10 | 120×80, 10mi | Factions, NPCs | 15+ | Yes (player copy) | [TBD] |
     | MAP-003 | City District Investigation | Location | S5–S6 | 30×30, 5ft | Investigation nodes | NPCs | No | [TBD] |

   - **Player Experience Goals**: What the player MUST feel, discover, or experience. Measurable and testable. Use MUST language.

   - **Assumptions & Scope**: What this game IS and is NOT. Additionally:
     - **RPG-specific scope**:
       - **For Tabletop**: "This is a [N]-session campaign for [N] players using [RULESET]. It is [NOT a one-shot / sandbox / railroad]. Combat encounters emphasize [theme]. Skill checks favor [abilities]."
       - **For Computer Game**: "This is a [single-player / multiplayer / co-op] RPG with [combat / dialogue / exploration] as primary mechanical pillar. Player progression is [level-based / stat-based / skill-tree] with [N] companions / class options."
       - **Mechanics scope**: "Character builds [can / cannot] trivialize encounters. Skill checks [are / are not] alternative to combat. Dialogue trees [affect / do not affect] all narrative branches."
     - Check whether `specs/series-bible.md` exists in the workspace.
     - If it **exists**: read `## Series Parameters` and pre-fill Series title. Read `## Games in Series` to determine the next entry number and pre-fill Series position (e.g., `game 2 of 3`). Set Series bible path to `specs/series-bible.md`. Emit: `?? Existing series detected — series title and position pre-filled from specs/series-bible.md. Confirm or override.`
     - If it **does not exist** and this is non-standalone: add a note — `?? specs/series-bible.md does not yet exist — speckit.series will create it when this game is planned.`
     - If series position is `standalone`: leave Series title and Series bible path fields blank.
     - Target node count, target endings count, target audience, engine preference (if known).

   - **Open Questions (OQ-NNN)**: Unresolved design decisions that block proceeding. Numbered sequentially.

6. **Output**
   - List all OQ-NNN items as a summary block at the end of `specs/<prefix>-<short-name>/spec.md`
   - Report the full path created and any items left as `[NEEDS CLARIFICATION]`
   - Suggest: "Run `speckit.clarify` to resolve open questions, or `speckit.constitution` to generate the game bible."

7. **Update search index** (optional — large projects):
   - If `.speckit/index/` exists, run: `python scripts/python/index.py update` from the project root.
   - This indexes the new `specs/<prefix>-<short-name>/spec.md` so `speckit.constitution` can query it for genre, tone, and mechanics inference.
   - If the command fails or the index does not exist, skip silently.
