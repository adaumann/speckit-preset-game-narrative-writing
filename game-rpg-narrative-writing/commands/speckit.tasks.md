---
description: Generate the full node authoring task list (tasks.md) from the flowmap and narrative spec files. Covers all phases from spec setup through export (Phases 0�9).
handoffs:
  - label: Fix Story Structure
    agent: speckit.plan
    prompt: The flowmap is incomplete or the act structure is unclear. Please review and fix it.
    send: true
  - label: Generate Node Outlines
    agent: speckit.outline
    prompt: Begin outlining Phase 1 nodes
    send: true
  - label: Start Drafting
    agent: speckit.implement
    prompt: Begin drafting nodes in phase order
    send: true
  - label: Polish Nodes
    agent: speckit.polish
    prompt: Polish all drafted nodes to completion
    send: true
  - label: Verify Continuity
    agent: speckit.continuity
    prompt: Run continuity checks on all nodes
    send: true
  - label: Compile Story
    agent: speckit.compile
    prompt: Compile nodes to story files for each target engine
    send: true
---

# speckit.tasks

Generate or update `tasks.md` � the complete phased task list for node authoring, QA, and export.

## User Input

```text
$ARGUMENTS
```

You **MUST** consider the user input before proceeding (if not empty). Accepted input:
- Nothing � generate from `specs/plan.md` and `specs/spec.md`
- `--update` � add new tasks or update status of existing tasks
- `--phase [N]` � regenerate a specific phase only

- `--update` � revise existing `tasks.md` without regenerating completed tasks
- `--phase [0�9]` � scope regeneration to a single phase

## Pre-Execution Checks

**Check for extension hooks (before task generation)**:
- Check if `.specify/extensions.yml` exists in the project root.
- If it exists, read it and look for entries under the `hooks.before_tasks` key.
- Process as standard hook block (Optional/Mandatory). Skip silently if absent.
**Extract RPG context** (if this is an RPG preset):
- Read `.specify/memory/constitution.md` and extract `[PLATFORM]` and `[RULESET]` from YAML frontmatter
- If `[PLATFORM]` = "Tabletop": Add tabletop-specific task phases and validation tasks
- If `[PLATFORM]` = "Computer Game": Add computer game-specific task phases and validation tasks
- If `[RULESET]` = "D&D 5e": Add D&D 5e-specific validation tasks (CR calibration, skill DC checks, spell/ability limits)
- Store platform/ruleset for conditional task generation (see Phase 3.5 RPG Validation)
Then:
1. Confirm `specs/plan.md` exists � tasks cannot be generated without a node graph.
2. Confirm `.specify/memory/constitution.md` exists.
3. If `tasks.md` exists and neither `--update` nor `--phase` is set: ask user to confirm overwrite.

## Outline

**Goal**: Generate `tasks.md` � a fully scoped, phased task list driven by actual flowmap and spec content, not generic placeholders.

### Execution Steps

1. **Setup**: Run `{SCRIPT}` from repo root and parse JSON for spec file paths.

2. **Load spec documents**: Read from `specs/`:
   - **Required**: `plan.md` (node graph, branch structure, act breakdown), `spec.md` (NPCs, variables, research gaps)
   - **Required if generating Phase 0**: `constitution.md` (mechanic schemas, world rules, ending conditions)
   - **Optional**: `characters/` profiles, `world-building.md`, `variables.md`   - **RPG-specific optional** (if platform detected): `items.md`, `bestiary.md`, `quests.md`, `locations.md`, `npc-roster.md`, `puzzles.md`   - Note which optional documents are missing � affected tasks may be marked `[BLOCKED: needs <document>]`

3. **Generate Phase 0 setup tasks** from actual spec content (do NOT copy static placeholders from `tasks-template.md`):
   - Read all research gaps and `OQ-NNN` items from `spec.md`
   - Generate one research task per domain gap or open question that blocks Act 1 drafting
   - Mark parallelizable setup tasks with `[P]` where they cover independent domains
   - Use actual NPC names from the Key NPCs table for profile tasks

4. **Generate node tasks per act** from `plan.md`:
   - Count all nodes per act
   - Identify nodes that can be outlined/drafted in parallel (`[P]`) � independent branches with no causal dependency on each other
   - Identify sequentially dependent nodes � mark without `[P]`
   - **RPG Marker Validation** (if platform=RPG): Parse node graph for RPG markers (`[ENCOUNTER: CR-X]`, `[SKILL-CHECK: ability, DC-X]`, `[FACTION: faction-name]`, `[APPROVAL: companion-name]`, `[SESSION-X]`). Note missing markers for later validation tasks.
   - **Step-Phasing**: Generate outline tasks for all nodes in the act first, followed by draft tasks for that act. This ensures the structural logic of the act is approved before prose is generated.

5. **Generate `tasks.md`**: Use `templates/tasks-template.md` as structure, fill with:
   - Correct game title and spec paths from `spec.md`
   - Actual node IDs, titles, and act groupings from `plan.md`
   - Accurate `[P]` markers where node drafts are genuinely parallelizable
   - Specific Phase 0 checkpoint items matching the actual variables, mechanics, and endings in the spec
   - Phase 7 QA tasks scoped to the node count

6. **Task generation rules**:
   - Every node in `plan.md` MUST have at least one outline task and one draft task
   - Phase 0 setup tasks are generated from actual spec content � never copied from template placeholders
   - No draft task may be `[P]` with a node it causally depends on (check branch dependencies in `plan.md`)
   - Phase 6b Polish tasks: one task per node marked `status: APPROVED` in draft/[ENGINE]/. Can be `[P]` if nodes are independent.
   - **Phase 3.5 RPG Validation** (if platform=RPG, inserted after Phase 3 outlines): 
     - Tabletop-specific: CR calibration validation, Faction consistency check, Companion arc validation, Skill check coverage audit
     - Computer Game-specific: Playstyle routing validation, Difficulty scaling consistency check
     - D&D 5e-specific: Spell/ability limits audit, Magic item distribution check, Skill DC reasonableness validation
     - All tasks sequential (dependency chain: CR calibration → Faction consistency → Companion validation → Skill audit)
   - Phase 7a Readability tasks: sequential `speckit.readability` across all branches
   - Phase 7b Branching tasks: sequential `speckit.branching` across all branches
   - Phase 7c Information tasks: sequential `speckit.information` for all NPCs and secrets
   - Phase 7d Narrative Arc tasks: sequential `speckit.narrative-arc` for all characters, subplots, and endings
   - Phase 7e Continuity Verify tasks: sequential checks for dialogue, glossary, locations, NPC state, variables, series, timeline, thematic. Re-polish tasks for failures.
   - Phase 8 Compilation tasks: sequential compile for each target engine (SugarCube, Ink, Ren'Py, etc.) from themes to story files
   - Phase 9 Export tasks: sequential validation of compiled output, version tagging, release preparation
   - QA and export tasks (Phases 3.5, 7–9) are always sequential, never parallel
   - If `--update` is set, only add tasks for nodes not already present � never remove completed tasks
   - Blocked tasks must carry a `[BLOCKED: reason]` note

7. **Report**: Total tasks, tasks per act, parallel vs. sequential ratio, number of unresolved OQ-NNN items gating Phase 0 checkpoint, recommended MVP scope (minimum nodes to complete Act 1).
   - **RPG-specific report** (if platform detected): Include Phase 3.5 task count, RPG validation checkpoints, critical blocking items (missing RPG markers, unresolved faction contradictions, soft-lock companions), recommended ruleset-specific prep items before Phase 3.5 starts

## Phase Definitions

**Phase 0: Research & Setup**
- Research gaps and open questions (OQ-NNN) from spec.md
- Character profile completion for all Key NPCs
- World-building documentation (glossary, locations, timeline if applicable)
- **Spatial documentation** (RPG-specific — always required before Phase 1):
  - `world-map.md`: Region registry, Area list, travel connections, spatial variable registry — verify all Regions/Areas in spec.md World Structure section are registered
  - `locations.md`: One entry per Location with LOC-ID, parent Region, parent Area, Hub Passage, Scene IDs — verify every Location listed in spec.md has an entry with `parent_area:` and `parent_region:` filled
  - Spatial checkpoint: All Locations registered; every Area has at least one rest Location and one entry travel scene planned; no Location is in `locations.md` without a parent Area in `world-map.md`
- Mechanic schema verification from constitution.md
- Checkpoint: All OQ-NNN items resolved or explicitly deferred; profiles, glossary, locations complete; spatial hierarchy registered

**Phases 1�5: Narrative Structure** (per act)
- Phase 1: Outline all nodes in Act 1
- Phase 2: Draft all nodes in Act 1 (after outlines approved)
- Phase 3: Outline all nodes in Act 2
- **Phase 3.5: RPG Validation** (if platform detected as RPG; inserted after Phase 3 outlines before Phase 4 drafts):
  - **Tabletop-specific validation tasks** (sequential chain):
    - Encounter CR Calibration: Verify all encounters with `[ENCOUNTER: CR-X]` markers are within expected challenge range (±2 CR from party level)
    - Faction Reputation Consistency: Audit faction rep tables for impossible combinations or contradictions; verify all `[FACTION: faction-name, impact: ±N]` markers align
    - Companion Arc Validation: Verify all `[APPROVAL: companion-name, ±N]` markers follow recruitment → progression → fate progression; no approval gates that create soft-locks
    - Skill Check Coverage Audit: Verify `[SKILL-CHECK: ability, DC-X]` markers have alternative solutions or progression paths; no encounter-trivializing checks
  - **Computer Game-specific validation tasks** (sequential chain):
    - Playstyle Routing Validation: Verify all quests/encounters support multiple completion paths (combat/dialogue/exploration) leading to same beat progression
    - Difficulty Scaling Consistency: Audit Easy/Normal/Hard variants across all encounters; verify scaling is proportional and no playstyle is locked out by difficulty
  - **D&D 5e-specific validation tasks** (sequential, integrated into above):
    - Spell/Ability Limits Audit: Verify all spell/ability uses in encounters document per-encounter or per-rest limits; no infinite resource exploitation
    - Magic Item Distribution Check: Verify item rarity aligns with acquisition level (Common→Uncommon at low levels, Rare/Very Rare at mid/high)
    - Skill DC Reasonableness: Verify all skill check DCs fall within 8–30 range and scale appropriately with party level (DC +1–2 per 4 levels)
  - Checkpoint: All CR validations pass; faction paths are logically consistent; companion arcs have no soft-locks; skill checks have documented alternatives; difficulty scaling is balanced

- Phase 4: Draft all nodes in Act 2 (after outlines AND Phase 3.5 RPG validation approved)
- Phase 5: Outline and draft remaining acts (Acts 3+)
- Each phase pairs outline ? draft to ensure structural approval before prose generation
- Checkpoint per act: All node drafts reach `status: APPROVED` per verify

**Phase 6b: Polish**
- One task per node in draft/[ENGINE]/ with `status: APPROVED`
- Tasks can be `[P]` if nodes are independent of each other
- Each node must be polished to completion: `polished: [YYYY-MM-DD]` field added
- Checkpoint: All nodes have `polished: [date]` in frontmatter; no FAIL status on polish audit

**Phase 7a: Readability**
- Run `speckit.readability` across all branches (sequential)
- Create revision tasks for flagged pacing/tone issues via `speckit.revise`
- Re-run `speckit.readability` after fixes until clean
- Checkpoint: All branches pass readability audit

**Phase 7b: Branching**
- Run `speckit.branching` across all branches (sequential)
- Create revision tasks for forced choices, orphaned branches, or agency issues via `speckit.revise`
- Re-run `speckit.branching` after fixes until clean
- Checkpoint: All choices have meaningful consequences; no forced branches

**Phase 7c: Information**
- Run `speckit.information` for all NPCs and secrets (sequential)
- Create revision tasks for dialogue gaps, unrealistic NPC knowledge, or unreachable secrets via `speckit.revise`
- Re-run `speckit.information` after fixes until clean
- Checkpoint: All NPC dialogue reachable; secrets discoverable; information asymmetry healthy

**Phase 7d: Narrative Arc**
- Run `speckit.narrative-arc` for all characters, subplots, and endings (sequential)
- Create revision tasks for flat characters, dangling subplots, or unsatisfying endings via `speckit.revise`
- Re-run `speckit.narrative-arc` after fixes until clean
- Checkpoint: All characters have arcs; all subplots resolve; endings satisfy criteria

**Phase 7e: Continuity Verify**
- Run `speckit.continuity --check dialogue,glossary,locations,npc,variables,series,timeline,thematic` (sequential)
- For each failed check, create revision task(s) via `speckit.revise`
- After revisions pass verify, run `speckit.polish` again to re-polish
- Checkpoint: All continuity checks pass; nodes re-polished after any revisions

**Phase 8: Compilation**
- Generate or verify theme files (story.css for SugarCube, ink-theme-*.html for Ink)
- Compile for each target engine via `speckit.compile --engine [ENGINE]` (sequential per engine)
- Validate output structure in draft/[ENGINE]/ and story/ directories
- Checkpoint: All target engines compile without errors; draft/[ENGINE]/story.* and story/ files present

**Phase 9: Export & Release**
- Test compiled output in each engine environment (Twine player for SugarCube, Ink web player for Ink, etc.)
- Version tagging and changelog updates
- Package final distribution (playable files, theme assets, README)

---

## RPG-Specific Task Generation (Tabletop & Computer Game)

If `[PLATFORM]` is detected as "Tabletop" or "Computer Game" in constitution.md, apply the following additional task generation rules:

### Tabletop RPG Task Generation

**Phase 3.5 Task Creation:**
1. **Encounter CR Calibration**: For each node with `[ENCOUNTER: CR-X]` marker, generate task:
   - Read node's enemy composition and expected party level from NODE data
   - Compare CR vs party level (should be ±2 of expected party level)
   - If CR out of range: task status `[ALERT: CR out of range]`, suggests revision
   - If balanced: task status `PASS`

2. **Faction Reputation Consistency**: Read all factions from spec.md, generate task:
   - Audit faction rep thresholds in spec/variables.md and spec/mechanics.md
   - Scan all `[FACTION: faction-name, impact: ±N]` markers in plan.md
   - Verify no faction can reach impossible reputation combinations (e.g., +100 to two mutually hostile factions)
   - Flag any rep gates that create soft-locks (e.g., requiring ≥50 with Faction A AND ≤-50 with Faction B simultaneously)
   - Generate revision task if inconsistencies found

3. **Companion Arc Validation**: For each recruitable companion in spec.md, generate sequential task:
   - Verify recruitment node exists and has `[APPROVAL: companion-name, +N]` marker
   - Trace approval progression through nodes to verify clear path to ending gates
   - Verify no soft-lock (e.g., requiring ≥75 approval but only 3 approval-gaining nodes total = impossible)
   - Verify betray/break-up paths are clearly marked if applicable
   - Flag any missing bridges between approval tiers

4. **Skill Check Coverage Audit**: Generate task:
   - Count all `[SKILL-CHECK: ability, DC-X]` markers in plan.md
   - Verify each has documented alternative solution (social/stealth/magical bypass, or unavoidable encounter)
   - Verify DC distribution covers 10–20 range (no trivial or impossible checks)
   - Verify no skill check trivializes an encounter (e.g., Persuasion DC 10 bypassing a CR 5 combat)
   - Generate revision task if coverage gaps found

### Computer Game Task Generation

**Phase 3.5 Task Creation:**
1. **Playstyle Routing Validation**: Generate task:
   - Read all quests/locations from specs/quests.md and specs/locations.md
   - Verify each quest stage has multiple completion paths documented (combat/dialogue/exploration)
   - Verify all paths lead to same beat progression (no "dialogue path misses loot" unfairly)
   - Verify no playstyle is locked out from major story beats
   - Generate revision task if routing is unbalanced

2. **Difficulty Scaling Consistency**: Generate task:
   - Read all encounters from specs/bestiary.md and specs/puzzles.md
   - Verify Easy/Normal/Hard variants exist for all combat encounters
   - Verify scaling is proportional (Hard ≠ just "+50% HP", consider action economy, enemy count, loot)
   - Verify difficulty settings don't create progression gates (e.g., Hard puzzle unsolvable by design)
   - Generate revision task if scaling is inconsistent

### D&D 5e-Specific Task Generation

**Phase 3.5 Task Creation** (integrated into above):
1. **Spell/Ability Limits Audit**: For each encounter with spellcasters, generate task:
   - Verify all spell uses document restrictions (per encounter, per short rest, per long rest)
   - Flag any unlimited ability use that could trivialize encounters
   - Verify spell slot counts align with creature CR and assumed caster level
   - Generate revision task if limits are missing or excessive

2. **Magic Item Distribution Check**: Generate task:
   - Read all item acquisitions from specs/items.md
   - Verify rarity progression: Common/Uncommon at levels 1–4, Rare at 5–10, Very Rare at 11–16, Legendary 17+
   - Verify no attunement slots overload (max 3 per character typically)
   - Verify magic item utility doesn't trivialize core encounter mechanics
   - Generate revision task if distribution is unbalanced

3. **Skill DC Reasonableness**: Generate task:
   - Audit all `[SKILL-CHECK: ability, DC-X]` markers
   - Verify DCs follow D&D 5e guidelines: DC 10 (Easy), 12 (Medium), 15 (Hard), 20 (Very Hard), 25+ (Nearly Impossible)
   - Verify DC progression scales with party level (+1–2 per 4 party levels expected)
   - Verify no check is unachievable without magic items or specific feat combos
   - Generate revision task if DCs are unreasonable

### Task Numbering & Ordering

- Phase 3.5 tasks are always sequential (Tabletop: CR → Faction → Companion → Skill; Computer: Playstyle → Difficulty; D&D 5e: Spell/Item/DC)
- Phase 3.5 tasks are **blocking**: Phase 4 drafting cannot start until Phase 3.5 validation passes
- If Phase 3.5 detects issues, generate linked `speckit.revise` tasks; party must resolve before proceeding
- Task IDs: `RPG-CAL-001` (CR calibration), `RPG-FAC-001` (Faction), `RPG-CMP-001` (Companion), `RPG-SKL-001` (Skill), etc.

### Conditional Subtasks

- If no encounters exist with RPG markers: Skip CR calibration task (mark `[SKIPPED: no marked encounters]`)
- If fewer than 2 recruitable companions: Skip companion arc validation (mark `[SKIPPED: < 2 companions]`)
- If no `[SKILL-CHECK]` markers in plan: Skip skill audit (mark `[SKIPPED: no skill checks]`)
- If platform=Tabletop but ruleset=Generic: Skip D&D 5e-specific tasks; substitute with generic ruleset checks
- If platform=Computer but genre includes "tabletop simulator": Include session prep validation from Tabletop rules

