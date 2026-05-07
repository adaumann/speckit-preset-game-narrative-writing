---
description: Research tracking command for game narrative. Four modes � add (log a new research item or source finding), resolve (mark an item answered and capture the finding), check (scan drafted nodes for claims not backed by research.md), and status (research dashboard showing open items ranked by project risk). Drives task generation in speckit.tasks. Run any time from first concept through export.
handoffs:
  - label: Generate Writing Tasks
    agent: speckit.tasks
    prompt: Regenerate writing tasks to reflect the latest resolved research findings
    send: true
  - label: Run Continuity Check
    agent: speckit.continuity
    prompt: Run a continuity check to verify research findings are correctly applied in drafted nodes
    send: true
  - label: Brainstorm Research Topic
    agent: speckit.brainstorm
    prompt: Brainstorm open research questions for this game
    send: true
  - label: Continue Drafting
    agent: speckit.implement
    prompt: Continue drafting � research phase complete
    send: true
---

## User Input

```text
$ARGUMENTS
```

You **MUST** consider the user input before proceeding (if not empty).

Accepted arguments:
- *(no argument)* � display the research status dashboard (same as `status`)
- `add [topic]` � open an interactive session to log a new research item (e.g. `add Cold War submarine hierarchy`)
- `add [topic] --source "[source]"` � log a finding directly with a source (skips interactive prompts)
- `resolve [R-ID]` � mark a research item resolved and capture findings (e.g. `resolve R003`)
- `resolve [R-ID] --finding "[text]" --source "[source]"` � resolve inline
- `check` � scan all drafted nodes for factual or world-rule claims not backed by any research item (read-only)
- `check [NODE_ID]` � scope the check to a specific node
- `status` � display the research dashboard
- `status --open` � show only OPEN items
- `status --resolved` � show only RESOLVED items

---

## Purpose

`speckit.research` keeps the factual and world-building grounding of a game narrative explicit, traceable, and integrated with the drafting workflow. It manages `research.md` as a living document that:

1. Records every domain knowledge gap before it becomes a prose or consistency error
2. Captures source findings and maps them to specific nodes and branches
3. Drives research task generation in `speckit.tasks` (tasks are generated from R-items, not static placeholders)
4. Scans drafted nodes for unsupported factual or world-rule claims after writing begins

**Research scope for game narrative** includes:
- **World/setting accuracy**: historical, technical, cultural, geographic details the game world draws on
- **Reference games**: comparable IF titles, engine-specific conventions, genre expectations
- **Mechanic design**: how similar mechanics are implemented in reference games; player psychology research
- **NPC authenticity**: professional roles, speech registers, social dynamics that need grounding
**Research scope for RPG campaigns** (if `SESSION.is_rpg = true`):
- **Tabletop TR (Tabletop Research)**: NPC profession/hierarchy accuracy, session pacing standards, faction reputation mechanics, companion relationship tropes, encounter design standards for the ruleset
- **Computer CR (Computer Research)**: Playstyle balance (how do reference games handle Combat/Dialogue/Exploration equity), accessibility standards (WCAG, colorblind parity, motor accessibility), narrative routing conventions
- **Ruleset Research** (DR = D&D 5e, PR2 = Pathfinder 2e, SR = Shadowrun 6e):
  - **D&D 5e DR**: Challenge Rating (CR) calculation from DMG (p.82), NPC stat block conventions, spell balance, feat interaction precedents, multiclass balance
  - **Pathfinder 2e PR2**: Encounter building (XP budget vs. 4-player avg level), degree of success implementation (critical success/failure), action economy, trait interactions
  - **Shadowrun 6e SR**: Dice pool calculation conventions, hacker/rigger balance, magic vs. tech balance, run structure standards, NPC karma calculations
**Scope of this command**:
- Only reads/writes `research.md` and (in `check` mode) reads node files.
- Does not revise prose � use `speckit.revise` to fix nodes where findings require changes.
- `check` is strictly read-only.

---

## Pre-Execution Checks
**RPG Platform & Ruleset Detection** (NEW for RPG support):
- Extract `[PLATFORM]` from `constitution.md` § III (Platform-Genre Binding):
  - `PLATFORM: tabletop` → Set `SESSION.is_rpg = true`, `SESSION.platform = "tabletop"`
  - `PLATFORM: computer` → Set `SESSION.is_rpg = true`, `SESSION.platform = "computer"`
  - Otherwise → Set `SESSION.is_rpg = false`
- Extract `[RULESET]` from `constitution.md` § VIII (System & Ruleset):
  - If present: Set `SESSION.ruleset = "[D&D 5e|Pathfinder 2e|Shadowrun 6e]"` for conditional guidance
  - If not present (generic narrative): `SESSION.ruleset = null` (skip ruleset-specific checks)
- Store in SESSION object for use in research item categorization and check scanning

**RPG Research Context** (conditional on `SESSION.is_rpg = true`):
- **Tabletop**: Read `specs/npc-roster.md`, `specs/mechanics-[RULESET].md`, `specs/encounters.md` (if present)
- **Computer**: Read `specs/characters/[Combat|Dialogue|Exploration]`, accessibility-features.md, reference-games.md
- **Ruleset**: Load DMG (D&D 5e CR table), Pathfinder 2e Core Rulebook (encounter building), Shadowrun 6e Run structure standards
**Check for extension hooks**:
- Check if `.specify/extensions.yml` exists in the project root.
- If it exists, read it and look for entries under the `hooks.before_research` key.
- Process as standard hook block (Optional/Mandatory). Skip silently if absent.

**Search index** (large projects � optional):
- For `add` mode: after logging a new research item, check whether `.specify/index/` exists. If so, run `python scripts/python/index.py update` to keep the index current.
- For `check` mode: if `.specify/index/` exists, you MAY query the index to surface node passages that may contain unresearched claims:
  > `python scripts/python/index.py query "[claim text]" --type node --top 5`
  Use results as supplementary input � do not replace the full `check` scan.

---

## Step 1 � Setup and Mode Resolution

Run `{SCRIPT}` from repo root and parse `FEATURE_DIR`.

Locate `FEATURE_DIR/research.md`. If the file does not exist:
- For `add` mode: create it from `templates/research-template.md`. Populate `## Research Scope` from `specs/spec.md` and `.specify/memory/constitution.md` if present (setting, technical domains, reference games, cultural context). Emit: `? Created research.md from template. Proceeding to add first item.`
- For `resolve`, `check`, or `status` modes: abort with `? research.md not found. Run speckit.research add [topic] to create it.`

Parse `$ARGUMENTS` for mode and any inline flags. Resolve mode:
- `add �` ? **Mode: Add**
- `resolve �` ? **Mode: Resolve**
- `check �` ? **Mode: Check**
- `status �` or *(empty)* ? **Mode: Status**

---

## Mode: Add

**Purpose**: Log a new research item � a knowledge gap that needs answering before or during drafting.

### Add Step 1 � Parse topic

If `$ARGUMENTS` contains a topic after `add`: use it as the item title. Otherwise prompt:
> `What topic needs research? (e.g. "Cold War submarine officer hierarchy", "symptoms of radiation exposure", "how Ink handles nested conditions")`

### Add Step 2 � Context questions

Ask the following. Accept inline flags if provided (`--source`, `--finding`). Skip any question already answered by `$ARGUMENTS`:

1. **Why does this matter?**
   > `Which node, branch, or mechanic requires this knowledge? (e.g. "NODE-2003 � player must give correct orders in the control room")`

2. **Specific questions to answer** (ask for up to 3):
   > `What specific factual questions need answers? Enter each on a new line:`
   Accept free-form text. Each non-empty line becomes one bullet in the `Questions to answer` list.

3. **Research category** (if `SESSION.is_rpg = true`):
   > `Category? (TR=Tabletop, CR=Computer, D&D/PF2e/SR6e for ruleset, or leave blank for general)`
   - Sets the R-item prefix: `TR-NNN`, `CR-NNN`, `DR-NNN`, `PR2-NNN`, `SR-NNN`, or `R-NNN` (generic)

4. **Authenticity risk** – is this an expert-visible error?
   > `Would a specialist player or reader catch it if this is wrong? (y/n)`
   If yes: add it to the `## Authenticity Flags` table with a risk description.

4. **Node impact** (if a node was named in question 1):
   > `How will the findings change the prose, dialogue, choices, or mechanic logic? (leave blank if unknown)`   - **For Tabletop**: Will this inform campaign-guide.md, SESSION-N-BRIEFING.md, or encounter design?
   - **For Computer**: Will this affect playstyle routing or accessibility variants?
5. **Existing source** (if `--source` was passed, skip this):
   > `Do you have a source already? If yes, paste or describe it. (leave blank to skip)`
   If a source is provided with a finding: jump to **Add Step 4** (resolve immediately).

### Add Step 3 � Write the item

Auto-assign the next ID (highest existing ID + 1):
- **Generic**: `R-NNN` 
- **Tabletop RPG**: `TR-NNN` 
- **Computer RPG**: `CR-NNN` 
- **Ruleset-specific**: `DR-NNN`, `PR2-NNN`, `SR-NNN`

Append with `**Category**` field. If RPG: category is TR/CR/D&D/PF2e/SR6e.

Append the new item to `research.md ## Research Items`:

```markdown
### R[NNN] � [Topic Name]
**Why this matters**: [node/branch reference + explanation]
**Questions to answer**:
- [question 1]
- [question 2]
**Findings**: OPEN
**Sources**: �
**Node impact**: [text or TBD]
```

If the item is an Authenticity Flag: also append a row to `## Authenticity Flags`:

```markdown
| [FLAG description] | [NODE_ID or branch] | [Risk if Wrong] |
```

Confirm:
```
? Added: R[NNN] � [Topic Name]   Status: OPEN
  Authenticity flag: [Yes / No]
  Next step: run `speckit.research resolve R[NNN]` when you have findings.
             Or: add it to tasks.md as a research task via `speckit.tasks`.
```

### Add Step 4 � Immediate resolve (if source was provided)

If a source AND finding were provided in Add Step 2: call **Mode: Resolve** for this item inline. Do not prompt again.

---

## Mode: Resolve

**Purpose**: Mark a research item answered and record the finding.

### Resolve Step 1 � Locate item

Parse `[PREFIX]-ID` or `R-ID` from `$ARGUMENTS` (e.g., `TR-005`, `CR-003`, `DR-007`, `R-011`). Find the matching `### [PREFIX]-[NNN]` block in `research.md`. If not found, abort:
```
? [PREFIX]-[NNN] not found in research.md.
  Run `speckit.research status` to see all item IDs.
```

If the item already has `Status: RESOLVED`, warn and ask: `[PREFIX]-[NNN] is already resolved. Update the finding? (y/n)`

### Resolve Step 2 � Gather findings

If `--finding` and `--source` were passed in `$ARGUMENTS`: use them directly.

Otherwise prompt:

1. > `What did you find? (paste or summarise your research finding)`
2. > `Source? (book title + page, URL, expert source, reference game, etc.)`
3. > `Does this change anything in specs/plan.md, the spec, or drafted nodes?`
   - If yes: prompt for a brief note. Append it to the finding block as `**Flowmap impact**: [note]` � this is not automatically applied; it is a flag for the author to act on.

### Resolve Step 3 � Update research.md

In the `### R[NNN]` block:
- Replace `**Findings**: OPEN` with `**Findings**: [finding text]`
- Replace `**Sources**: �` with `**Sources**: [source text]`
- Add or update `**Flowmap impact**: [note]` if applicable

Move the block from `## Research Items` to `## Resolved Research` table:

| R[NNN] | [Topic] | [one-sentence finding summary] | [source] |

If the item was in `## Authenticity Flags`: mark it as resolved by appending ` ?` to its Flag column value.

Confirm:
```
? Resolved: R[NNN] � [Topic Name]
  Finding logged. Source: [source summary]
  [Plan impact: (note) � review specs/plan.md and consider running speckit.continuity if nodes are drafted]
  Remaining OPEN items: [N]
```

---

## Mode: Check

**Purpose**: Scan drafted nodes for specific, verifiable factual or world-rule claims that are not backed by a resolved R-item in `research.md`. Read-only.

**RPG Enhancement**: Check mode identifies TR (Tabletop), CR (Computer), and ruleset-specific (DR/PR2/SR) claims in addition to generic world-rule claims. Reports are organized by category.

### Check Step 1 � Load assets

Load `research.md`. Build two lists:
- **RESOLVED claims**: collect all findings from the `## Resolved Research` table. For each, extract: topic, node reference, key factual assertions from the finding text.
- **OPEN items**: collect all `R-NNN` blocks with `Findings: OPEN`. Note their node references.

Determine the node scope:
- If `$ARGUMENTS` contains a NODE_ID: load only that node file from `nodes/`.
- Otherwise: scan all `nodes/*.md` files.

If no node files exist, abort: `? No node files found in nodes/. Run speckit.implement to generate drafts first.`

### Check Step 2 � Scan for unsupported claims

For each node in scope, identify **specific factual or world-rule claims** � statements that assert:
- A real-world historical, technical, cultural, or geographic detail
- A professional role, procedure, or institution that requires domain knowledge
- A world rule stated as fact that should be backed by explicit design decision in `specs/world-building.md` or `.specify/memory/constitution.md`
- A reference game mechanic or IF convention stated as normative
**RPG-Specific Claims** (if `SESSION.is_rpg = true`):
- **Tabletop TR-claims**: Encounter CR assignments, NPC stat block references, session structure claims, faction reputation mechanics
- **Computer CR-claims**: Playstyle routing assertions (e.g., "Combat route takes 15 min, Dialogue takes 45 min"), accessibility descriptions, difficulty scaling claims
- **Ruleset DR/PR2/SR-claims**: Ability score/skill check DC values, degree of success language, dice pool notation, action economy statements
For each detected claim:

1. Check whether a RESOLVED R-item covers it (topic match, node reference match, or finding text directly addresses the claim).
   - **Covered** ? no flag
2. Check whether an OPEN R-item references the same node or topic.
   - **Open research pending** ? flag as `PENDING`
3. No R-item covers it ? flag as `UNSUPPORTED`

### Check Step 3 � Output report

```
???????????????????????????????????????????????????????
  RESEARCH CHECK REPORT
  Scope  : [NODE_ID or "all drafted nodes"]
  Nodes checked : [N]
  Date   : [YYYY-MM-DD]
???????????????????????????????????????????????????????

### UNSUPPORTED Claims (no R-item covers this)
| Node | Claim | Risk | Suggested R-item |
|---|---|---|---|
| NODE-2003 | "She called out the correct ballast dive order" | HIGH � expert-visible | Add: R[next] � submarine dive order protocols |

### PENDING Claims (OPEN R-item exists but not yet resolved)
| Node | Claim | Linked R-item |
|---|---|---|
| NODE-1004 | "The 1991 coup was announced by radio first" | R004 � Soviet coup announcement sequence |

### COVERED (mention in brief)
N claims checked against resolved research � no issues found.

### Summary
UNSUPPORTED: [N]  PENDING: [N]  COVERED: [N]
Recommended action: [run speckit.research add for each UNSUPPORTED claim / resolve pending R-items before export]
???????????????????????????????????????????????????????
```

---

## Mode: Status

**Purpose**: Research dashboard � live view of all items, coverage, and risk.

```
???????????????????????????????????????????????????????
  RESEARCH STATUS: [GAME_TITLE]
  OPEN: [N]  RESOLVED: [N]  Total: [N]
???????????????????????????????????????????????????????

### Open Research Items  (sorted: Authenticity Flags first, then by node order)
| ID    | Topic                              | Node / Branch     | Authenticity flag |
|-------|------------------------------------|-------------------|-------------------|
| R003  | Submarine dive order protocols     | NODE-2003         | ?? HIGH           |
| R007  | Soviet coup announcement sequence  | NODE-1004         | ?? HIGH           |
| R011  | How Ink handles nested conditions  | All Act 2 gates   | �                 |

### Authenticity Flags (unresolved)
| Flag                              | Node / Branch | Risk if wrong |
|-----------------------------------|---------------|---------------|
| Submarine dive order protocols    | NODE-2003     | Expert players will catch immediately |
�

### Resolved Research Items
| ID    | Topic                             | Finding (summary)          | Source |
|-------|-----------------------------------|----------------------------|--------|
| R001  | Ink passage-name conventions      | [one sentence summary]     | [source] |
�

Recommended action: [clear to draft / resolve HIGH flags before export / run speckit.research check]
???????????????????????????????????????????????????????
```

---

## Post-Execution Hooks

- Check if `.specify/extensions.yml` exists. Look for `hooks.after_research`. Process as standard hook block. Skip silently if absent.

---

## Tabletop RPG Campaign Research Model

**Purpose**: For Tabletop RPGs, research items feed directly into campaign prep documentation (campaign-guide.md and SESSION-N-BRIEFING.md).

**Campaign Prep Impact Tracking** (if `SESSION.is_rpg = true` and `SESSION.platform = "tabletop"`):

When resolving a TR-item (Tabletop Research):
- Check if the finding informs:
  - **campaign-guide.md**: House rules, party composition guidelines, companion mechanics, faction reputation pacing → Note in "Flowmap impact: Updates campaign-guide.md §[Section]"
  - **SESSION-[N]-BRIEFING.md**: Session prep expectations, mechanic clarifications for players → Note in "Flowmap impact: Updates SESSION-[N] player brief"
  - **Encounter design**: Ruleset-specific CR calibration, NPC stat block accuracy → Note in "Flowmap impact: Encounter [NODE-ID] CR verified"

**Example TR-item Lifecycle**:
```
### TR-003 – D&D 5e Challenge Rating calibration
**Why this matters**: Determine CR targets for sessions 4-8 (party levels 3-5)
**Questions to answer**:
- What's the XP budget for 4 medium encounters per session?
- How do deadly vs. hard encounters affect pacing?
**Findings**: OPEN
**Category**: TR (Tabletop, D&D 5e)

[After resolving with DMG table findings...]

**Findings**: Medium encounters = 300-400 XP; Hard = 500-750 XP. Session 4 (party level 3) targets Hard difficulty (~750 XP spread across 2 encounters). 
**Flowmap impact**: Updates campaign-guide.md §House Rules – encounter difficulty targets. Apply to NODE-2001 through NODE-2012 (S4).
```

**Campaign Pacing Guide Integration**:
- TR-items about "Session structure standards" feed into campaign-pacing-guide.md (auto-generated for players)
- TR-items about "Companion relationship tropes" inform SESSION-[N]-BRIEFING.md companion introductions
- TR-items about "Faction reputation mechanics" inform campaign-guide.md faction advancement table

