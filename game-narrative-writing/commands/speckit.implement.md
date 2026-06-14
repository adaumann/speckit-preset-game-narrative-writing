---
description: Execute the next uncompleted task from tasks.md — research, outline, draft, review, or any speckit command. When invoked without arguments, reads tasks.md, identifies the first uncompleted task of any type, dispatches to the appropriate handler (speckit.research, speckit.outline, internal draft logic, etc.), and marks the task completed. For draft tasks, generates engine-native node files (Twee for SugarCube, Ink for Ink, etc.) directly. Use --draft-direct to skip outline requirement and draft from task description only. For known engines (sugarcube/ink), run speckit.export to scaffold boilerplate (init, widgets, UI), then speckit.compile for playable output.
handoffs:
  - label: Scaffold boilerplate & compile
    agent: speckit.export
    prompt: Scaffold boilerplate (init, widgets, UI) for the engine, then compile to playable output
    send: true
  - label: Continue executing tasks
    agent: speckit.implement
    prompt: Run the next uncompleted task from tasks.md
    send: true
  - label: Review outlines again
    agent: speckit.outline
    prompt: I want to review or regenerate the outlines before drafting
    send: false
---

# speckit.implement

Execute the next uncompleted task from `tasks.md`. Reads the task, determines its type (research, outline, draft, review, quality gate, etc.), dispatches to the appropriate handler, and marks the task as completed. When a NODE_ID is given directly, behaves as a draft command: generates engine-native node files (Twee, Ink, etc.) from approved outlines.

**Output format** (draft tasks): Engine-specific (Twee for SugarCube, Ink for Ink, etc.) — not markdown. This eliminates round-trip translation and produces engine-native code immediately.

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
- `--draft-direct` – skip outline requirement; draft directly from task description in `tasks.md` (prompts for confirmation)
- *(no argument)* – read `tasks.md`, find the first uncompleted task of any type, dispatch to the appropriate handler, and mark it completed

## Pre-Execution Checks

**Check for extension hooks (before drafting)**:
- Check if `.specify/extensions.yml` exists in the project root
- If it exists, read it and look for entries under the `hooks.before_implement` key
- Process as standard hook block (Optional/Mandatory). Skip silently if absent.

Then:

**If no NODE_ID was given (task executor mode):**

1. Check if `specs/[FEATURE_DIR]/tasks.md` exists. If not, halt: "No tasks.md found. Run `speckit.tasks --update` or specify NODE_ID manually."
2. Scan tasks.md for the first uncompleted task (any row with `- [ ]` checkbox in any phase table).
3. If no uncompleted task is found, halt: "All tasks completed in tasks.md. Run `speckit.tasks --update` to refresh."
4. Parse the task description to determine its type and dispatch (see **Task Dispatch** section below).
5. After the dispatched handler completes, mark the task as done by replacing `- [ ]` with `- [x]` in tasks.md.

**If a NODE_ID was given (draft mode):**

**Extract engine from constitution.md** (before required checks):
- Read `.specify/memory/constitution.md` YAML frontmatter
- Look for `engine` (single value) or `export_engines` (list) key
- If `engine: sugarcube` or `export_engines` includes `sugarcube`: Set `SESSION.engine = "sugarcube"`
- If `engine: ink` or `export_engines` includes `ink`: Set `SESSION.engine = "ink"`
- Otherwise: Set `SESSION.engine = "generic"` (output engine-agnostic markdown)
- Store `SESSION.engine` — all conditional steps below branch on this value

**Required checks for each target node:**
1. Confirm `specs/[FEATURE_DIR]/outline/` and `.specify/memory/constitution.md` exist
2. For each requested node, verify an outline file exists at `outlines/[NODE_ID].md`
   - **If outline is missing and `--draft-direct` is set**: Prompt user: "No outline found for [NODE_ID]. Draft directly from task description? [y/N]"
     - If yes: skip outline validation; derive beat summary and choices from the task's description and `plan.md` node entry
     - If no: skip this node and report it as skipped
3. Verify outline status is `APPROVED` (skip nodes marked `DRAFT` or `SKIP`) — unless `--force` is set
   - **If `--draft-direct` was confirmed above, this check is bypassed**
4. Confirm `specs/[FEATURE_DIR]/variables.md` exists — hooks declared in outlines must resolve
5. Confirm `specs/[FEATURE_DIR]/characters.md` exists — dialogue and NPC references must resolve
6. Confirm `.specify/memory/constitution.md` exists — prose_profile and engine settings needed

## Task Dispatch (when invoked without arguments)

When `speckit.implement` finds an uncompleted task in `tasks.md`, parse the **Task** column to determine the task type and dispatch to the appropriate handler.

### Task Type Mapping

| Task pattern in tasks.md | Handler | Action |
|---|---|---|
| `Research: [topic]` | `speckit.research` | Run `speckit.research` with the topic from the task description |
| `Generate variables.md` | `speckit.specify` | Note: "Run `speckit.specify --force variables.md` to generate" (or auto-run if available) |
| `Generate mechanics.md` | `speckit.mechanics` | Run `speckit.mechanics` |
| `Generate endings.md` | `speckit.endings` | Run `speckit.endings` |
| `Write NPC profile` | `speckit.character` | Run `speckit.character` with the NPC name from description |
| `Write glossary` | Manual / `speckit.specify` | Prompt user or delegate to `speckit.specify` |
| `Document world-building` | Manual | Note: populate world-building.md from spec.md |
| `Outline: [title]` | `speckit.outline` | Run `speckit.outline [NODE_ID]` using the NODE_ID from the task's Node column |
| `Draft:` or `[P] Draft:` | Internal draft logic | Execute the full draft pipeline below (Steps 1-10) using the NODE_ID from the Node column |
| `Run speckit.analyze` | `speckit.analyze` | Run `speckit.analyze` |
| `Run speckit.checklist` | `speckit.checklist` | Run `speckit.checklist` |
| `Review & approve` | Manual | Print: "Manual step. Review and set status to APPROVED, then re-run speckit.implement." Mark task done after confirmation prompt. |
| `speckit.X` (any other command) | That command | Run `speckit.X` with extracted arguments |
| `Document final variable state log` | `speckit.statemap` | Run `speckit.statemap` |

### Dispatch Execution

For each dispatched handler:
1. Announce: "Executing task [TXXX]: [task description]"
2. Run the handler (either call the sub-command or execute internal logic)
3. If the handler succeeds, mark the task as completed in tasks.md
4. If the handler fails, halt with the error and do not mark the task as done
5. After marking done, print: "✓ Task [TXXX] completed. Re-run `speckit.implement` for the next task."

## Execution Steps (Draft Mode)

The following steps apply only when drafting nodes (either via NODE_ID argument or when a Draft task is dispatched).

### 1. Load Required Documents (Draft Mode Only)

These documents are loaded only when drafting a node. Dispatched tasks (research, outline, etc.) load their own documents per their respective command specs.

For each target node, load:
- **Required** (unless `--draft-direct`): Outline file `outlines/[NODE_ID].md` (Beat Summary, Variables, Choices, Mechanic Hooks). When `--draft-direct` is active, derive beat summary and choices from the task description in `tasks.md` and the node entry in `plan.md`.
- **Required**: `.specify/memory/constitution.md` (prose_profile, default POV, tone, style_mode)
- **Required**: `spec.md` (research notes, world rules, context)
- **Required**: `variables.md` (variable declarations for type checking)
- **Required**: `characters.md` (NPC profiles, dialogue registers, relationship states)
- **Required**: `mechanics.md` (hook schemas for translating mechanics to engine syntax)
- **Required** (if it exists): `tasks.md` — to find the next draft task and mark it complete
- **Optional**: `.specify/memory/craft-rules.md` (if style_mode is humanized-ai — guides beat language register)
- **Optional**: `glossary.md` (for consistent terminology in prose)
- **Optional**: `locations.md` (for sensory anchors and location-specific rules)
- **Optional**: `themes.md` (for thematic resonance and motif placement)

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
- Uses the prose_profile (style, register, tone) from `.specify/memory/constitution.md`
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
3. Mechanic hooks: Insert engine-native mechanic syntax inline (see **Inline Mechanic Hooks** section below — format depends on `SESSION.engine`)
4. Choices: Terminal choices section with all outlined choices (format depends on `SESSION.engine`)

**Style rules**:
- POV: Use `.specify/memory/constitution.md` default POV (second-person, third-person, first-person) or node-level override
- Tone: Match `.specify/memory/constitution.md` tone (dramatic, comedic, dark, uplifting, etc.)
- Register: If style_mode is humanized-ai, use `.specify/memory/craft-rules.md` to tune beat language and dialogue

### 5. Inline Mechanic Hooks

Insert mechanic hooks in engine-native syntax at the narrative moment they occur. The format depends on `SESSION.engine`.

**Inline rules (all engines)**:
- Prose must read coherently if all mechanic blocks are removed
- Each hook block must be isolated — no mixing multiple hooks in one block unless they fire simultaneously
- The prose surrounding the hook should justify why the mechanic fires (e.g., "Mira smiles" before the trust increase)
- Variable mutations fire at the narrative moment they occur, not batched at end

**If `SESSION.engine = "sugarcube"`** — write SugarCube macros directly:

```twee
<<-- FLAG: set a boolean flag -->>
<<set $flag_letter_read to true>>
You remember the letter's contents clearly.

<<-- INVENTORY: add / remove / check items -->>
<<run $inv.push("rusty_key")>>
A rusty key — it might be useful.
<<run $inv.delete("old_letter")>>
You discard the now-useless letter.

<<-- VISITED: mark location as seen -->>
<<set $loc_chamber_visited to true>>
You've been here before — the熟悉 shadows confirm it.

<<-- TRUST: NPC relationship delta -->>
Mira smiles at you warmly, her trust deepening.
<<set $miraTrust += 5>>

<<-- COUNTER: increment / decrement integer -->>
<<set $escape_attempts += 1>>
You count this as your third attempt.

<<-- CURRENCY: gain / spend money -->>
<<set $gold += 50>>
The merchant counts out fifty gold pieces.
<<set $gold -= 10>>
You pay the toll and pass through.

<<-- ATTRIBUTE: modify player stat -->>
<<set $character.wisdom += 1>>
A moment of insight — you understand the pattern now.

<<-- CHOICE_MEMORY: record a dialogue choice -->>
<<set $player_loyalty to "helped_mira">>
You remember: you chose to help Mira earlier.

<<-- NPC_STATE: change NPC condition -->>
<<set $priestess_state to "grateful">>
The priestess's demeanor softens.

<<-- ENDING_CONDITION: progress toward an ending -->>
<<set $just_ruler_score += 10>>
Your just actions bring you closer to the throne.

<<-- TIMER: start / stop / advance a countdown -->>
<<set $torch_timer to 5>>
The torch sputters — you have five turns of light remaining.
<<set $torch_timer -= 1>>
One fewer turn. The darkness presses in.

<<-- RANDOM: random outcome (1d20 style) -->>
<<set $clue_roll to random(1, 6)>>
<<if $clue_roll >= 4>>
  You spot a hidden glyph on the wall.
<<else>>
  Nothing here but dust.
<</if>>

<<-- CLUE: discover an investigation clue -->>
<<set $clue_symbolic_glyph to true>>
<<run $inv.push("clue_glyph_rubbing")>>
A glyph rubbing joins your notes — this is the third symbol.

<<-- QUEST: advance / complete quest stages -->>
<<advanceQuestStage "quest_shrine_blessing">>
The priestess guides you forward. You've completed this stage of her teachings.

<<completeQuest "quest_shrine_blessing">>
The priestess grants you her final blessing. Your quest is complete.
```

**If `SESSION.engine = "ink"`** — write Ink syntax directly:

```ink
// FLAG: set a boolean flag
~ flag_letter_read = true
You remember the letter's contents clearly.

// INVENTORY: add / remove items
~ inv("rusty_key")
A rusty key — it might be useful.
~ inv("old_letter", false)
You discard the now-useless letter.

// VISITED: mark location as seen
~ loc_chamber_visited = true
You've been here before — the familiar shadows confirm it.

// TRUST: NPC relationship delta
Mira smiles at you warmly, her trust deepening.
~ miraTrust += 5

// COUNTER: increment / decrement integer
~ escape_attempts += 1
You count this as your third attempt.

// CURRENCY: gain / spend money
~ gold += 50
The merchant counts out fifty gold pieces.
~ gold -= 10
You pay the toll and pass through.

// ATTRIBUTE: modify player stat
~ character.wisdom += 1
A moment of insight — you understand the pattern now.

// CHOICE_MEMORY: record a dialogue choice
~ player_loyalty = "helped_mira"
You remember: you chose to help Mira earlier.

// NPC_STATE: change NPC condition
~ priestess_state = "grateful"
The priestess's demeanor softens.

// ENDING_CONDITION: progress toward an ending
~ just_ruler_score += 10
Your just actions bring you closer to the throne.

// TIMER: start / advance a countdown
~ torch_timer = 5
The torch sputters — you have five turns of light remaining.
~ torch_timer -= 1
One fewer turn. The darkness presses in.

// RANDOM: random outcome
~ temp_clue_roll = RANDOM(1, 6)
{temp_clue_roll >= 4:
  You spot a hidden glyph on the wall.
- else:
  Nothing here but dust.
}

// CLUE: discover an investigation clue
~ clue_symbolic_glyph = true
~ inv("clue_glyph_rubbing")
A glyph rubbing joins your notes — this is the third symbol.

// QUEST: advance / complete quest stages
~ quest_shrine_blessing_stage += 1
The priestess guides you forward. You've completed this stage of her teachings.

~ quest_shrine_blessing_complete = true
The priestess grants you her final blessing. Your quest is complete.
```

**If `SESSION.engine = "generic"`** — use `[MECHANIC:...]` token blocks (translated to engine syntax later by speckit.export):

```markdown
[MECHANIC:FLAG set=letter_read]
You remember the letter's contents clearly.

[MECHANIC:INVENTORY add=rusty_key]
A rusty key — it might be useful.
[MECHANIC:INVENTORY remove=old_letter]
You discard the now-useless letter.

[MECHANIC:VISITED set=visited_chamber]
You've been here before — the familiar shadows confirm it.

[MECHANIC:TRUST npc=mira delta=+5]
Mira smiles at you warmly, her trust deepening.

[MECHANIC:COUNTER variable=escape_attempts delta=+1]
You count this as your third attempt.

[MECHANIC:CURRENCY add=50]
The merchant counts out fifty gold pieces.
[MECHANIC:CURRENCY remove=10]
You pay the toll and pass through.

[MECHANIC:ATTRIBUTE modify=wisdom delta=+1]
A moment of insight — you understand the pattern now.

[MECHANIC:CHOICE_MEMORY variable=player_loyalty value="helped_mira"]
You remember: you chose to help Mira earlier.

[MECHANIC:NPC_STATE npc=priestess set=grateful]
The priestess's demeanor softens.

[MECHANIC:ENDING_CONDITION variable=just_ruler_score delta=+10]
Your just actions bring you closer to the throne.

[MECHANIC:TIMER start=torch_timer duration=5]
The torch sputters — you have five turns of light remaining.
[MECHANIC:TIMER tick=torch_timer]
One fewer turn. The darkness presses in.

[MECHANIC:RANDOM range=1-6 target=clue_roll threshold=4]
You spot a hidden glyph on the wall. (On failure: Nothing here but dust.)

[MECHANIC:CLUE set=symbolic_glyph]
[MECHANIC:INVENTORY add=clue_glyph_rubbing]
A glyph rubbing joins your notes — this is the third symbol.

[MECHANIC:QUEST advance=quest_shrine_blessing]
The priestess guides you forward. You've completed this stage of her teachings.

[MECHANIC:QUEST complete=quest_shrine_blessing]
The priestess grants you her final blessing. Your quest is complete.
```

### 5b. Location-Based Quest Passages (if quest mechanics enabled)

If this node is organized under `specs/world/[location-name]/[quest-id]/stage-N.md`, follow these additional rules. Mechanic syntax must match `SESSION.engine` (see Step 5 for engine-specific formats).

- **Passage opening** MUST include quest context: remind the player what stage they are in and what location they are at
  - Example: "You return to the Shrine, seeking the priestess's guidance. She awaits you."
- **Passage closing** MUST signal the quest stage advancement: include prose that clarifies when this stage ends, with the engine-appropriate quest advancement syntax
  - SugarCube: `<<advanceQuestStage "quest_shrine_blessing">>` with prose like "The priestess grants you her blessing. Your task here is complete."
  - Ink: `~ quest_shrine_blessing_stage += 1` with matching prose
  - Generic: `[MECHANIC:COUNTER variable=quest_shrine_blessing_stage delta=+1]`
- **Location returns** (if `revisit_allowed: true` in `.specify/memory/constitution.md`): include passage condition comments showing when this passage is available again
  - Example (generic/SugarCube): `<!-- Available: if $quest_shrine_blessing_stage < 2 OR ($quest_shrine_blessing_stage == 2 and $character.wisdom > 8) -->`
  - Example (Ink): `// Available: if quest_shrine_blessing_stage < 2`
- **Quest gating** (if `failed_quests: true`): include failure paths as choices in engine-appropriate format

### 5c. Quest Widget Usage (if quest mechanics enabled)

If your narrative includes multi-stage quests or quest tracking, use quest widgets to display and advance quests. The syntax depends on `SESSION.engine`.

**SugarCube** (`SESSION.engine = "sugarcube"`):

Quest Widgets:

| Widget | Purpose | Example |
|---|---|---|
| `<<questList>>` | Display all quests grouped by status (active/completed/failed) | In a dedicated QuestUI passage |
| `<<questProgress "quest_id">>` | Show current stage/status of single quest | Mid-passage to show progress to player |
| `<<advanceQuestStage "quest_id">>` | Increment quest stage | Direct SugarCube widget call |
| `<<completeQuest "quest_id">>` | Mark quest as completed | Direct SugarCube widget call |
| `<<failQuest "quest_id">>` | Mark quest as failed | Direct SugarCube widget call |

Quest variables: `$quest_[id]_status`, `$quest_[id]_stage`

```twee
<<if not $quest_shrine_blessing_status>>
  <<set $quest_shrine_blessing_status to "active">>
  [[Ask priestess for guidance|NODE-002-Dialogue]] /* Effect: Begin Shrine Blessing quest */
<</if>>

<<link "Accept the blessing" "END-A_Blessed">><</link>>
/* Effect: Complete quest */
/* <<completeQuest "quest_shrine_blessing">> */

<<link "Leave without the blessing" "END-B_Departed">><</link>>
/* Effect: Quest remains active (can retry on revisit) */
```

Quest display in prose:
```twee
You have been following the priestess's teachings. 

<<questProgress "quest_shrine_blessing">>

This passage has been enlightening, but there is more to learn...

<<advanceQuestStage "quest_shrine_blessing">>
<<set $quest_shrine_blessing_stage to 2>>
You feel yourself progressing on this spiritual journey.
```

UI Integration:
- Add `<<link "Quests" "QuestUI">><</link>>` to StoryMenu
- Create `QuestUI` passage with `<<questList>>`
- Display active quest count in HUD via StoryCaption

**Ink** (`SESSION.engine = "ink"`):

```ink
{not quest_shrine_blessing_status:
~ quest_shrine_blessing_status = "active"
+ [Ask priestess for guidance] -> NODE_002_Dialogue
}
+ [Accept the blessing] -> END_A_Blessed
+ [Leave without the blessing] -> END_B_Departed
```

Quest display in prose:
```ink
You have been following the priestess's teachings.
~ quest_shrine_blessing_stage += 1
You feel yourself progressing on this spiritual journey.
```

**Generic** (`SESSION.engine = "generic"`):

```markdown
- [Ask priestess for guidance](NODE-002-Dialogue)
  <!-- Effect: Begin Shrine Blessing quest -->
  <!-- Mechanic: <<set $quest_shrine_blessing_status to "active">> -->

- [Accept the blessing](END-A_Blessed)
  <!-- Effect: Complete quest -->

- [Leave without the blessing](END-B_Departed)
  <!-- Effect: Quest remains active -->
```

Quest display in prose:
```markdown
[MECHANIC:QUEST advance=quest_shrine_blessing]
You feel yourself progressing on this spiritual journey.
```

### 6. Terminal Choices Section

At the end of the node, create a choices section in the format matching `SESSION.engine`.

**If `SESSION.engine = "sugarcube"`** — use Twee wiki-links or `<<link>>` macros with consequence comments:

```twee
[[Look around carefully|NODE-002_LookAround]] /* Effect: You gain awareness of the chamber */
[[Check the equipment|NODE-003_Equipment]] /* Effect: You discover a tool that might help */
<<if $flag_danger_sense>>
  [[Leave immediately|NODE-004_Escape]] /* requires: $flag_danger_sense; Effect: You escape */
<</if>>
```

**If `SESSION.engine = "ink"`** — use Ink divert syntax:

```ink
+ [Look around carefully] -> NODE_002_LookAround
+ [Check the equipment] -> NODE_003_Equipment
+ {flag_danger_sense} [Leave immediately] -> NODE_004_Escape
```

**If `SESSION.engine = "generic"`** — use markdown links with HTML comments:

```markdown
## Choices

- [Look around carefully](NODE-002) <!-- Effect: You gain awareness of the chamber -->
- [Check the equipment](NODE-003) <!-- Effect: You discover a tool that might help -->
- [Leave immediately](NODE-004) <!-- requires: $flag_danger_sense == true; Effect: You escape -->
```

**Rules (all engines)**:
- Each choice must match exactly one row from the outline's Choices table
- Label MUST be verbatim from outline (or close synonym if prose uses simpler language)
- Target node MUST match outline target
- Include condition gate if outlined choice had one
- Include consequence annotation from the outline
- Minimum 2 choices for non-terminal nodes; omit entirely for ending nodes

**For ending nodes**: Single choice pointing to the ending (engine-appropriate format).

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

Generate the output file in engine-native format based on `SESSION.engine`.

#### If `SESSION.engine = "sugarcube"`

Output path: `draft/sugarcube/NODE-{seq}_{Name}.twee`

```twee
:: NODE-001-shrine-entrance [header]
  {- Node ID: NODE-001 -}
  {- Act: 1 -}
  {- Variables Read: [$character.intelligence] -}
  {- Variables Set: [$visited_shrine] -}
  {- Drafted: YYYY-MM-DD -}
  {- Outline: outlines/NODE-001.md -}

  You stand before an ancient shrine, its stones worn by centuries.
  <<set $loc_chamber_visited to true>>
  The priestess looks up from her prayers.
  
  <<if $character.intelligence >= 5>>
    [[Ask about the shrine's history|NODE-002-history]]
  <</if>>
  [[Donate to the shrine|NODE-003-donate]]
  [[Search the grounds|NODE-004-search]]
```

All mechanics use SugarCube macro syntax (`<<set>>`, `<<if>>`, `<<link>>`, widgets) directly — no `[MECHANIC:...]` tokens. No export step needed; hand directly to `speckit.compile`.

#### If `SESSION.engine = "ink"`

Output path: `draft/ink/NODE-{seq}_{Name}.ink`

```ink
=== NODE_001_ShrineEntrance ===
// Node ID: NODE-001
// Act: 1
// Variables Read: [character.intelligence]
// Variables Set: [loc_chamber_visited]
// Drafted: YYYY-MM-DD
// Outline: outlines/NODE-001.md

You stand before an ancient shrine, its stones worn by centuries.
~ loc_chamber_visited = true
The priestess looks up from her prayers.

{character.intelligence >= 5:
  + [Ask about the shrine's history] -> NODE_002_History
}
+ [Donate to the shrine] -> NODE_003_Donate
+ [Search the grounds] -> NODE_004_Search
```

All mechanics use Ink syntax (`~ var = value`, `{condition}`, `+ [label] -> target`). No export step needed; hand directly to `speckit.compile`.

#### If `SESSION.engine = "generic"`

Output path: `draft/NODE-{seq}_{Name}.md`

```markdown
---
node_id: NODE-001
title: Shrine Entrance
act: 1
status: DRAFT
pov: second-person
variables_read: [$character.intelligence]
variables_set: [$visited_shrine]
drafted: YYYY-MM-DD
outline_ref: outlines/NODE-001.md
---

You stand before an ancient shrine, its stones worn by centuries.

[MECHANIC:VISITED set=visited_shrine]
The priestess looks up from her prayers.

## Choices

- [Ask about the shrine's history](NODE-002)
- [Donate to the shrine](NODE-003)
- [Search the grounds](NODE-004)
```

Uses `[MECHANIC:...]` tokens and markdown links. Requires `speckit.export` to convert to engine format before `speckit.compile`.

### 9. Mark Task Completed in tasks.md

If `specs/[FEATURE_DIR]/tasks.md` exists, mark the executed task as completed. This applies both to dispatched tasks (from Task Dispatch) and direct draft calls.

1. Find the task row for this NODE_ID or task ID (look for `Draft: [NODE_TITLE]` matching the drafted node, or the task ID like `TXXX`)
2. Replace the `- [ ]` checkbox with `- [x]` in that row
3. If no matching task is found, add a note: "`tasks.md` has no entry for `[NODE_ID/TXXX]`. Run `speckit.tasks --update` to regenerate."

**Example update:**
```
Before:
| T014 | [P] Draft: Shrine Entrance | NODE-001 | `nodes/NODE-001.md` |

After:
| T014 | [P] Draft: Shrine Entrance | NODE-001 | `nodes/NODE-001.md` |
```

### 10. Report

List all drafted nodes with:
- `[NODE_ID] [title] — [N] vars, [N] hooks, [N] choices, act [N]`

Flag any:
- Missing consequence comments in choice links
- Undeclared variables
- Outline deviations (new choices, variables, or mechanics not in outline)
- Tasks updated in `tasks.md`

Remind the author to:
- Review prose for coherence and tone
- Verify all consequences are documented as comments in choice links
- Check that all outlined mechanics are present
- Verify engine-native syntax is correct (Twee passages, Ink knots, etc.)
- Run `speckit.export` to scaffold full boilerplate (init, widgets, UI)

### 11. Check for Extension Hooks

Check `hooks.after_implement`: run if present.

---

## Key Principle: Preserve Outline Fidelity

**The implement phase must NOT:**
- Add new choices not in the outline
- Remove outlined choices
- Change choice targets
- **Forget the narrative consequences** ← This is the common mistake

**The implement phase MUST:**
- Preserve all outline information (variables, hooks, choices, consequences)
- Document consequences as comments in the Choices section
- Transfer all mechanic hooks from outline to prose
- Maintain outline structure and gating conditions
- Write prose that matches the beat summary and narrative purpose

Consequences are the **bridge** between mechanical outcome and narrative meaning. They must be preserved.

---

## Twee Format Rules (SugarCube)

All generated `.twee` files MUST follow these rules:

### Passage Naming

Every passage header MUST use the `node_id` from frontmatter as the passage name:

```twee
:: NODE-001-start
```

**Never** use human-readable titles as passage names (e.g. `:: Start Node`). The node_id is the canonical identifier — all links in other passages reference it by this name. A mismatch between a passage name and the link target silently breaks navigation.

### Back Navigation

For choices that return the player to the previous passage (e.g. "Go back", "Return", "Cancel"), use the SugarCube history macro:

```twee
<<back "Return">>
```

**Never** use a hardcoded link to the previous node:

```twee
<!-- WRONG: breaks if the player arrived from a different passage -->
<<link "Return" "NODE-001-start">><</link>>
[[Return->NODE-001-start]]
```

`<<back>>` uses the engine's history stack, so it correctly navigates to wherever the player actually came from regardless of which node they visited before.

### When to Use `<<back>>` vs `<<link>>`

| Use case | Macro |
|---|---|
| Player navigates forward to a new scene | `<<link "Label" "NODE-xxx">><</link>>` |
| Player wants to return/cancel/go back | `<<back "Label">>` |
| Non-linear return to a hub passage | `<<link "Label" "LOC-xxx">><</link>>` |

---

## Supplementary Guidance for SugarCube/Twine Drafting

This section provides additional reference material for drafting high-quality narrative nodes in Twee format for SugarCube. All guidance here assumes direct Twee output (the default for SugarCube projects).

### Dialogue Choice Structuring

Structure player dialogue options with inline attribute gates and consequence metadata:

```twee
What do you say?

/* Wisdom gate — only shown to perceptive players */
<<if $character.wisdom gte 6>>
  [[I've noticed the amulet you wear. It's unusual.|NODE-003]] /* Effect: Priestess respects your insight; opens secret dialogue | wisdom +1 */
<</if>>

[[Can I find sanctuary here?|NODE-004]] /* Effect: Safe haven granted | flags.shrine_sanctuary = true */

[[I'll be on my way|NODE-005]] /* Effect: Priestess disappointed; future dialogue colder */
```

**Rules**:
- Keep condition gates to 1-2 variables max (e.g., `$character.wisdom >= 6`). Complex multi-variable gates are hard to test.
- Group related choices together. 2-4 choices per node is the sweet spot for SugarCube.
- Always include a fallback unconditional choice so the player can never be stuck with zero options.
- Use `<<back "Return">>` for "go back" navigation instead of hardcoded links to the previous node.

### Attribute Changes Within Prose

When a dialogue choice or action modifies character attributes, write the mutation inline at the narrative moment:

```twee
You think carefully about her words. The weight of insight settles on you.
<<set $character.wisdom += 1>>
<<run $ui.displayCharacterUpdate("wisdom", "+1")>>
```

Always include justifying prose before the mutation. Never fire a bare `<<set>>` without narrative context.

### Inventory Checks and Updates

**Checking for an item**:
```twee
<<if $inventory.rusty_key>>
  "That key," she whispers. "Where did you find it?"
<</if>>
```

**Adding an item** (use widgets from the equipment template):
```twee
She removes the amulet from around her neck and hands it to you.
<<run $inv.push("amulet_of_protection")>>
```

**Removing an item**:
```twee
You hand over the rusty key.
<<run $inv.delete("rusty_key")>>
```

### Multiple NPCs in One Node

When two or more NPCs are present, structure dialogue with character names prefixed:

```twee
**Priestess:**
"You speak as one who understands the old ways."

**Henne (Guard):**
"Enough mysticism, priestess. We have a practical problem."

**Priestess:**
"Practical and spiritual are not opposites, guard. They are one."

<<link "Side with the priestess" "NODE-006">><</link>>
<<link "Support Henne's pragmatism" "NODE-007">><</link>>
<<link "Suggest a compromise" "NODE-008">><</link>>
```

Validation:
- All NPC dialogue tags must match `characters.md` names
- Each NPC uses a distinct voice matching their character profile
- Multi-character scenes show reactions in sequence (primary responder first, then others)

### Compile & Test Cycle

After implementing nodes:

1. **Scaffold boilerplate** (first run only):
   ```bash
   speckit export --engine sugarcube
   ```
   Generates `StoryInit`, widgets, UI passages in `draft/sugarcube/infra/`.

2. **Compile to HTML**:
   ```bash
   speckit compile --engine sugarcube
   ```
   Produces a playable HTML file with all nodes linked together.

3. **Test in browser**:
   - Open the compiled HTML file
   - Verify prose renders correctly
   - Click dialogue choices; verify branching works
   - Check that attribute changes display in UI
   - Verify inventory changes persist

4. **Iterate**:
   - Edit the `.twee` file directly
   - Re-run `speckit compile`
   - Refresh browser to test changes

### Common Pitfalls & Fixes

| Issue | Cause | Fix |
|---|---|---|
| Dialogue choice doesn't appear | Condition evaluates to false; gate not met | Check attribute value in game UI; verify condition syntax |
| Attribute doesn't change | Missing `<<set>>` statement | Add `<<set $character.[attr] +/-= N>>` before recompile |
| Inventory item missing | Forgot to add via `<<run $inv.push(...)>>` | Add the push statement; recompile |
| NPC dialogue wrong tone | Prose_profile not matching character voice | Review `characters.md` profiles; adjust prose tone |
| Choice leads to wrong node | Node ID typo in link target | Verify target NODE_ID matches outline |
| `<<back>>` returns to wrong passage | No history entry (e.g., arrived from StoryMenu) | Use `<<link>>` for navigation from menus; reserve `<<back>>` for in-scene returns |
| Passage not found at compile time | Missing `.twee` file or typo in filename | Verify file exists in `draft/sugarcube/` and name matches the `:: PassageName` header |
