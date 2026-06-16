---
description: Targeted node revision — rewrites only the failing passages identified by speckit.verify, speckit.analyze, or speckit.continuity without touching passing content. Produces a versioned node file with a diff summary.
handoffs:
  - label: Re-run Verification
    agent: speckit.verify
    prompt: Re-run verification on the revised node
    send: true
  - label: Run Continuity Check
    agent: speckit.continuity
    prompt: Re-run continuity check after variable changes
    send: true
  - label: Continue Drafting
    agent: speckit.implement
    prompt: Continue drafting the next approved node
    send: true
---

# speckit.revise

Revise a node file to address quality failures, structural issues, or authorial feedback. Rewrites only failing passages � does not touch passing content.

## User Input

```text
$ARGUMENTS
```

You **MUST** consider the user input before proceeding (if not empty). Accepted formats:
- `NODE-003` � revise the node; auto-load its most recent checklist failures
- `NODE-003 NR-001 PR-004` � revise specific failure codes only
- `NODE-003 FB-007` � revise a specific feedback issue from `feedback.md`
- `NODE-003 "dead-end branch after choice B"` � revise from a quoted description
- *(no argument)* � revise the node with the most recent open checklist failure

- `--checklist` � auto-load all open checklist failures for the node
- `--feedback [ID]` � load a specific feedback issue from `feedback.md`
- `--full` � full redraft (not targeted revision); requires confirmation

## Pre-Execution Checks

**Extract Platform & Ruleset** (auto-detect RPG context):
- Read `.specify/memory/constitution.md` YAML frontmatter and extract `[PLATFORM]` and `[RULESET]`
- If `[PLATFORM]` = "Tabletop": Set `SESSION.is_rpg = "tabletop"` and activate Tabletop RPG revision guidance
- If `[PLATFORM]` = "Computer Game": Set `SESSION.is_rpg = "computer"` and activate Computer Game RPG revision guidance
- If neither detected: Set `SESSION.is_rpg = false` (generic game revision)
- Store `SESSION.platform` and `SESSION.ruleset` for conditional revision strategy selection

**Check for extension hooks (before revision)**:
- Check if `.specify/extensions.yml` exists in the project root.
- If it exists, read it and look for entries under the `hooks.before_revise` key.
- Process as standard hook block (Optional/Mandatory). Skip silently if absent.

## Operating Constraints

**SURGICAL SCOPE**: Only modify prose, hooks, or choices that directly cause a flagged failure. Do not improve or tighten surrounding content. Scope creep corrupts the isolation of what changed and undermines the versioning model.

**CONSTITUTION AUTHORITY**: `.specify/memory/constitution.md` governs all prose and mechanic decisions. If a revision cannot fix the failure without violating the constitution, STOP and report the conflict � do not silently violate the constitution to pass a checklist item.

**OUTLINE AUTHORITY**: `outlines/[NODE_ID].md` is authoritative for the node's structural intent: beat sequence, choice set, and variable contract must remain intact. Only the *execution* changes.

**PLAN AUTHORITY**: `specs/plan.md` is authoritative for target node IDs. A revision must not add or remove choices that change the branch graph without a corresponding `plan.md` update.

## Execution Steps

1. **Setup**: Run `{SCRIPT}` from repo root and parse JSON for spec file paths.

2. **Identify the revision target**:
   - Parse `$ARGUMENTS` for node ID. Resolve to `draft/[ENGINE]/[NODE_ID].[EXT]` (auto-detect engine from the first existing file).
   - If no argument: scan `checklists/` for the most recently modified file with open failures � use its linked node as the target.
   - Abort with a clear error if the node file does not exist or has no valid YAML frontmatter header.

3. **Load failure context**:
   - If a checklist file is auto-detected or specified: read all items marked FAIL or WARNING plus any Top Revision Priorities list.
   - If `$ARGUMENTS` contains failure codes (e.g. `NR-001 PR-004`): treat those as the failure scope.
   - If `$ARGUMENTS` contains a quoted description from `speckit.continuity` or `speckit.analyze` (CRITICAL issue text): use that as the failure scope.
   - If `--feedback [ID]` is set: load the specified issue from `feedback.md`.
   - If none of the above: list FAIL/WARNING items from the most recent checklist for this node and ask the user to confirm scope before proceeding.
   - **Failure scope is fixed at this step.** Do not expand it during revision.

4. **Load required context**:
   - Read `draft/[ENGINE]/[NODE_ID].[EXT]` in full (prose + YAML frontmatter)
   - Read `.specify/memory/constitution.md` � POV rules, prohibited phrases, tone, Prose Style Mode (Section VII), `style_mode`, `prose_profile`
   - Read `.specify/memory/craft-rules.md` � craft rules (NR-NNN, PR-NNN per active prose profile), anti-AI clich�s filter, prohibited phrases
   - Read `outlines/[NODE_ID].md` � beat sequence, choices table, variable contract, Dialogue Tree field (if present)
   - Read `specs/variables.md` � declared variables with types and value ranges
   - Read `specs/characters/[NPC_ID].md` for each NPC present � dialogue style (profile-tuned), trust thresholds, state values, Section VIII Dialogue Register by Trust State
   - **Optional (if dialogue revisions needed)**: Read `specs/relationships.md` for multi-party dialogue consistency
   - **Optional (if glossary revisions needed)**: Read `specs/glossary.md` Section V (Usage Rules) for term definitions and rejected variants
   - **Optional (if location revisions needed)**: Read `specs/locations.md` for sensory anchors and location rules

   **RPG-Specific Context** (if `SESSION.is_rpg = true`):
   - `specs/mechanics-[ruleset].md` – skill DC ranges, approval thresholds, faction rep ranges, system-specific mechanics
   - `specs/npc-roster.md` – companion profiles with approval ranges and class/level (if Tabletop)
   - `specs/quests.md` – quest structure and session context (if Tabletop)
   - `specs/bestiary.md` – enemy CR/difficulty profiles (if Tabletop)
   
   **Tabletop-Only Context** (if `SESSION.is_rpg = "tabletop"`):
   - `draft/campaign-guide.md` – campaign overview, house rules, party composition, companion system, player contract
   - `draft/SESSION-[N]-BRIEFING.md` – session-specific player introduction
   - `outlines/[NODE_ID].md` – **encounter_type** and **session** fields mandatory for Tabletop revisions
   
   **Computer Game-Only Context** (if `SESSION.is_rpg = "computer"`):
   - `specs/locations.md` – difficulty scaling notes (if revising encounter)
   - `specs/accessibility-features.md` – accessibility requirements (if present)

5. **Scope confirmation** � for each item in the failure scope, identify the exact passage or element responsible:
   - Quote the specific sentence(s), hook block, or choice line that causes the failure
   - State which item / issue each one violates and why
   - If failure is due to *absence* (e.g. no VISITED hook declared), note what must be *added* and where
   **For RPG Revisions** (if `SESSION.is_rpg = true`):
   - **Tabletop TR/CR failures**: Include session context (which session, which encounter_type)
   - **Ruleset-specific failures** (DR/PR2/SR): Include system mechanics references (e.g., "DC 14 exceeds D&D 5e maximum of 20")
   - **Campaign prep failures**: If revising campaign-guide.md or SESSION-N-BRIEFING.md, note scope impact ("affects player introduction to ruleset house rules")
   Present to the user:
   ```
   ## Revision Scope Confirmation

   | Item | Failing element / what's missing | Root cause | Revision type |
   |---|---|---|---|
   | PR-002 | "She felt the weight of the moment..." | Emotion named directly | Prose |
   | PR-010 | "The room felt cold and sterile" | Sensory inconsistent with Sanctuary location profile | Sensory detail |
   | DI-001 | "asked nervously" | Said-bookism with adverb on attribution | Dialogue prose |
   | DIAL-002 | Corvus dialogue uses high register | Trust state is hostile (expects low register) | Dialogue register |
   | GLOSS-001 | "Temporal Flux" used 3 times, "Time Flux" once | Glossary has "Time Flux" as rejected variant | Glossary consistency |
   | LOC-001 | Door described as "sealed" in NODE-005, "open" in NODE-012 | Timeline gap, state change not explained | Location state |
   | NR-001 | Choice B targets NODE-099 | NODE-099 does not exist in plan.md | Structural |
   | MH-003 | Missing [MECHANIC:VISITED set=...] | Variable visited_NODE-003 never set | Hook |
   | FB-007 | Trust delta in TRUST hook: +30 | Exceeds max single-node trust delta per constitution.md | Mechanic |
   ```

   **Stop and wait for user confirmation** before writing any revisions. Allow the user to:
   - Approve the scope as-is
   - Remove items ("skip FB-007, I'll fix it manually")
   - Add items ("also fix PR-004")
   - Provide a direction note ("for NR-001: retarget choice B to NODE-047 instead")

6. **Revise each failing element**:
   For each item in the confirmed scope, in the order they appear in the node file (top to bottom):
   - **Prose failures (PR-001�PR-008)**: rewrite only the failing passage; apply craft rules, POV, prohibited phrase check
   - **Sensory detail failures (PR-009, PR-010, PR-011)**: add/revise sensory descriptions to match location profile and NPC context; ensure emotional subtext is shown through environment/action not explicitly named
   - **Dialogue register failures (DIAL-NNN, DI-NNN)**: rewrite NPC dialogue to use correct register from `specs/characters/[NPC_ID].md` Section VIII per current trust state; fix said-bookism and adverb-on-attribution issues
   - **Dialogue tree consistency failures (DIAL-MULTI)**: if multi-party dialogue contradicts relationship arc or NPC information, revise one NPC's response to align with established dynamic
   - **Glossary failures (GLOSS-NNN)**: correct spelling/capitalization per `specs/glossary.md`; replace rejected variants with canonical terms; align meaning with glossary definition
   - **Location state failures (LOC-NNN)**: update sensory descriptions to match location profile; note timeline if state has changed; add brief explanation if location state differs from previous node
   - **Structural failures**: fix target node IDs, correct choice count, update branch logic
   - **Hook failures**: correct hook syntax, fix variable names or deltas, add missing hook declarations
   - **Feedback items**: implement the suggested change or propose an alternative with rationale
   - **Polish-stage failures (from speckit.polish audit)**: apply line-edit fixes (sentence rhythm, word repetition, filter words, weak verbs, voice register, em-dash count, dialogue attribution)

   **RPG-Specific Revision Guidance**:

   **Tabletop RPG Failures** (if `SESSION.is_rpg = "tabletop"`):
   - **TR-001 (session/encounter context)**: Add session # and encounter_type to frontmatter; add GM Notes section with session context
   - **TR-003 (skill check DC)**: Validate DC falls within ruleset range (D&D 5e: 5-20, PF2e: 10-50+, SR6e: documented pools); revise if out of range
   - **TR-005 (companion approval)**: Revise approval deltas to stay within ±100; add NPC acknowledgment of approval change
   - **TR-006 (faction rep)**: Revise to announce faction reputation change in NPC dialogue (not silent variable shift)
   - **TR-007 (CR balance)**: If combat CR out of ±2 tolerance: revise encounter difficulty (reduce NPC count, lower AC/damage, or increase party resources)
   - **TR-008 (combat narrative)**: Add foreshadowing or narrative justification for combat encounter
   - **Campaign Prep (Tabletop first session)**: If SESSION-1 first node: generate/revise `draft/campaign-guide.md` Introduction section with ruleset house rules, party composition, companion system overview; also update `draft/SESSION-1-BRIEFING.md` for player introduction

   **Computer Game RPG Failures** (if `SESSION.is_rpg = "computer"`):
   - **CR-001 (playstyle routing)**: Document which playstyles (Combat/Dialogue/Exploration) reach this node
   - **CR-002 (playstyle convergence)**: If node is branch point, revise to ensure all playstyles reconverge within 2 nodes to same story beat
   - **CR-003 (difficulty scaling)**: Add Easy/Normal/Hard variants (distinct NPC counts, AC, loot)
   - **CR-004 (accessibility)**: If timed challenge/puzzle: add accessibility variants (colorblind mode, audio cues, motor simplification, cognitive variant)
   - **CR-005 (skill check branching)**: Revise to branch explicitly (success→NODE-X, failure→NODE-Y; not both same target)
   - **CR-007 (difficulty lock)**: Remove any Hard mode-only content lock; all story progression must be possible on all difficulties

   **Ruleset-Specific Revisions**:
   - **D&D 5e failures (DR-NNN)**: DC validation (5-20), ability balance, magic item rarity by level, faction rep tracking (±25 max per node)
   - **Pathfinder 2e failures (PR2-NNN)**: DC validation (10-50+), degree of success outcomes (crit success/success/failure/crit fail), hero point opportunities, ancestry implications
   - **Shadowrun 6e failures (SR-NNN)**: Dice pool notation with [Skill+Attribute], Street/Matrix/Astral routing balance, karma/nuyen/street cred economy consistency

   - After each revision, note: which item it addresses and how

7. **Assemble the revised node**:
   - Replace only the revised elements in the original full node
   - **Do not alter** any content outside the confirmed revision scope
   - Reset `status` to `DRAFT` in YAML frontmatter if it was `APPROVED` (revision requires re-approval)
   - If `polished: [date]` exists: remove it (revision of prose means polish is invalidated)
   - Update `variables_read` / `variables_set` in frontmatter if changed
   - Increment `version` field (e.g. `version: 1` ? `version: 2`); add if absent
   - Add `revised: [YYYY-MM-DD]` field to the YAML frontmatter

8. **Write output**:
   - **Revised node**: save as `draft/[ENGINE]/[NODE_ID]_v[N].[EXT]` (e.g. `draft/ink/NODE-003_v2.ink`)
   - **Keep the original** `draft/[ENGINE]/[NODE_ID].[EXT]` unchanged � it is the v1 record
   - **Revision notes**: append a `<!-- REVISION NOTES` comment block at the top of the revised file (after YAML frontmatter):
     ```
     <!-- REVISION NOTES v[N]
          Revised: [YYYY-MM-DD]
          Revision scope: [list of item codes fixed]
          Based on: [checklist file / speckit.analyze report / speckit.continuity report / speckit.polish audit / manual scope]
          Revision types: [Prose|Sensory detail|Dialogue register|Dialogue consistency|Glossary|Location state|Structural|Hook|Mechanic|Polish]

          Changes:
          - [ITEM] ([TYPE]): [brief description of what changed and why]
          - [ITEM] ([TYPE]): [brief description]

          Prose validity: [unchanged from v[N-1] outside revision scope]
          Polish status: [invalidated - requires re-polish]
     -->
     ```

9. **Report**:
   ```
   ## Revision Report

   | Item | Type | Status | Change summary |
   |---|---|---|---|
   | PR-002 | Prose | Fixed | Named emotion ? involuntary physical reaction |
   | PR-010 | Sensory detail | Fixed | Updated sensory descriptions to match Sanctuary profile (sterile, cold) |
   | DIAL-001 | Dialogue register | Fixed | Corvus dialogue shifted to low-register; trust state is hostile |
   | GLOSS-001 | Glossary | Fixed | Replaced "Time Flux" with canonical "Temporal Flux" (3 instances) |
   | LOC-001 | Location state | Fixed | Clarified door state: "sealed in NODE-005, remains sealed via backdoor route, opened via main atrium" |
   | NR-001 | Structural | Fixed | Choice B retargeted: NODE-099 ? NODE-047 |
   | MH-003 | Hook | Fixed | Added [MECHANIC:VISITED set=visited_NODE-003] after prose |
   | FB-007 | Fixed | TRUST delta reduced: +30 ? +10 |

   Revised node: draft/ink/NODE-003_v2.ink
   Status reset to DRAFT � polish invalidated (revise removes polished: field); re-review and set status: APPROVED before next drafting run.
   Recommendations: (1) Run `speckit.verify NODE-003` on the revised node to confirm all items pass. (2) Run `speckit.polish NODE-003` to re-polish after structural revisions complete. (3) Run `speckit.continuity --check dialogue,glossary,locations` if any dialogue/glossary/location changes made.
   ```
   **RPG-Specific Report Notes** (if `SESSION.is_rpg = true`):
   - **Tabletop**: If TR/DR/PR2/SR items fixed, note session # and encounter impact; if campaign-guide.md updated, note "Player introduction revised: ruleset house rules updated"
   - **Computer**: If CR items fixed, note playstyle routes affected and difficulty scaling variant changes; if accessibility updated, list which accessibility variants were added
   - Example report line:
     ```
     | TR-007 | Structural | Fixed | Combat CR 6→4 (party level 9, within ±2 tolerance) | Session 3 encounter updated |
     | CR-004 | Accessibility | Fixed | Timed puzzle: added colorblind + audio variants | NODE-087 |
     ```
   If any item could **not** be fixed without violating the game bible or outline, report as BLOCKED:
   ```
   | NR-002 | BLOCKED | Fixing this requires adding a third choice, which changes the branch
                         graph. Update specs/plan.md for NODE-003 first, then re-run revision. |
   ```

   If `specs/plan.md` was affected (target node IDs changed or dialogue tree modified): note:
   ```
   ?? plan.md may need updating � choice targets or dialogue options changed. Run speckit.analyze to verify branch integrity.
   ```

   If glossary, location, or dialogue tree changes made: note:
   ```
   ?? Glossary/Location/Dialogue changes made. Run speckit.continuity --check glossary,locations,dialogue to validate cross-node consistency.
   ```

10. **Check for extension hooks (after revision)**: check `hooks.after_revise`.

---

## Key Principles for RPG Revision


**Tabletop Campaign Introduction Model**:
- On first SESSION-1 node revision: Generate/update `draft/campaign-guide.md` with:
  - **Introduction section**: Ruleset system (D&D 5e/PF2e/SR6e), house rules summary, party composition guidance, companion system overview, player contract
  - **Player-Facing Tone**: Welcoming, clear mechanics summary, no spoilers for campaign
- Update `draft/SESSION-1-BRIEFING.md` for player character creation guidance (level, starting equipment, house rules relevant to level 1)
- All Tabletop revisions should note impact on session pacing (does revision extend/reduce typical 2-4 hour session time?)

**Platform-Specific Revision Scope**:
- **Tabletop**: Focus on encounter balance (CR), NPC consistency (voice/approval), skill check mechanics (DC, outcomes), combat narrative justification
- **Computer Game**: Focus on playstyle routing (all routes viable), difficulty scaling consistency, accessibility completeness, no difficulty locks

**Surgical Revision Philosophy**:
- Only fix failures in confirmed scope; do not expand scope
- If fix requires violating constitution/outline/plan, STOP and report BLOCKED
- If revision crosses document boundaries (e.g., NPC voice requires characters.md update), note as downstream dependency

**Ruleset Mechanics Validation**:
- **D&D 5e**: DC 5-20, approval/faction ±100, magic item rarity by level, ability balance
- **Pathfinder 2e**: DC 10-50+, degree of success outcomes, hero point opportunities
- **Shadowrun 6e**: Dice pool notation, routing balance (Street/Matrix/Astral equivalence), karma/contact economy

**Campaign Prep Impact** (Tabletop-specific):
- Any change to house rules, party composition, or companion system should update `draft/campaign-guide.md`
- Any SESSION-N session-wide change (new NPC, faction shift, companion milestone) should update `draft/SESSION-N-BRIEFING.md`
- Player-facing docs maintained separately from narrative prose (no spoilers in introductions)

