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

