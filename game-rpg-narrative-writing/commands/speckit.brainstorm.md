---
description: Interactive brainstorming session for any game narrative topic � spec, plan, characters, branches, endings, mechanics, world-building, variables, or series. Loads existing files as context, asks probing questions in a loop, and produces a brainstorm notes file, a patch to the topic file, or nothing if cancelled. Supports challenge mode and quick/standard/deep session lengths.
handoffs:
  - label: Create Narrative Design Doc
    agent: speckit.specify
    prompt: Use these brainstorm notes to create the narrative design doc
    send: true
  - label: Build Plan
    agent: speckit.plan
    prompt: Use these brainstorm notes to build the plan and act structure
    send: true
  - label: Clarify Open Questions
    agent: speckit.clarify
    prompt: Clarify the narrative design doc using these brainstorm insights
    send: true
  - label: Generate Node Outline
    agent: speckit.outline
    prompt: Use these brainstorm notes to outline the target node
    send: true
---

# speckit.brainstorm

Run an interactive, question-driven brainstorming session on any aspect of the game narrative. Produces a notes file, applies findings to an existing spec file, or does nothing if cancelled. All file writes happen only at session end.

## User Input

```text
$ARGUMENTS
```

You **MUST** consider the user input before proceeding (if not empty). Accepted arguments:
- A topic name (e.g. `branches`, `characters`, `endings`) � skip the topic prompt
- `node NODE-003` � pre-fill node ID as the brainstorm target
- `npc [name]` � pre-fill NPC name as the brainstorm target
- `world-map` â€“ pre-fill topic as world map spatial design (RPG only)
- `challenge` ï¿½ activate Challenge Mode: questions stress-test existing file decisions
- A session length flag: `quick`, `standard`, or `deep` ï¿½ skip the session length prompt
- Any combination (e.g. `endings challenge quick`, `world-map challenge deep`)

## Pre-Execution Checks

**Extract Platform & Ruleset** (auto-detect RPG context):
- Read `.specify/memory/constitution.md` YAML frontmatter and extract `[PLATFORM]` and `[RULESET]`
- If `[PLATFORM]` = "Tabletop" or "Computer Game": Set `SESSION.is_rpg = true` and store detected platform/ruleset
- If neither detected: Set `SESSION.is_rpg = false` (generic game preset)
- Store `SESSION.platform` and `SESSION.ruleset` for conditional topic menu and question bank selection

**Check for extension hooks (before brainstorming)**:
- Check if `.specify/extensions.yml` exists in the project root.
- If it exists, read it and look for entries under the `hooks.before_brainstorm` key.
- Process as standard hook block (Optional/Mandatory). Skip silently if absent.

---

## Step 1 � Topic Selection

If no topic was provided as an argument, display the topic menu:

```
---------------------------------------------
  BRAINSTORM � Topic Selection
---------------------------------------------

  What do you want to brainstorm?

   1  spec           � Game concept, premise, dramatic question
   2  plan           � Act structure, branches, node graph
   3  characters     � NPC cast, arcs, trust dynamics
   4  npc            � A single specific NPC (you name them)
   5  branches       � Choice design, branch alternatives, gate logic
   6  endings        � Ending conditions, reachability, emotional payoff
   7  mechanics      � Hook types, mechanic applications, variable design
   8  world-building � Setting rules, locations, factions, ambient states
   9  variables      � Variable registry, carry-over design, state logic
  10  series         � Series arc, carry-over canon, entry-to-entry continuity
  11  glossary       � In-world terms, proper nouns, variable naming
  [RPG-SPECIFIC TOPICS – shown if RPG preset detected]
  12  factions       – Faction system, reputation mechanics, faction conflicts
  13  encounters     – Combat encounter design, CR calibration, difficulty scaling
  14  companion-arcs – Companion recruitment, approval gates, romance, fates
  15  difficulty-curve – Difficulty scaling progression, accessibility options
  16  mechanics-rpg  – RPG-specific mechanics, house rules, custom hooks
  17  world-map      – Spatial layout, Region/Area/Location design, travel connections
  Type a number, a topic name, or a custom topic.
  Type  q  to quit without doing anything.
---------------------------------------------
```

- Accept both number and name as valid input.
- If the user types `4` or `npc`, immediately ask: `Which NPC? (name or ID)` and store as `NPC_NAME`.
- If the user types `node NODE-NNN`, store the node ID as the brainstorm target.
- If the user types a number from RPG topics (12-17) while `SESSION.is_rpg = false`: display `? RPG topics only available for RPG presets.` and return to topic menu.
- Free-form topics not on the list are accepted as custom topics.
- `q` exits with: `Brainstorm cancelled. No files were changed.`

---

## Step 2 � Context Load

Run `{SCRIPT}` from repo root and parse JSON for spec file paths.

Resolve the **canonical file path** for the selected topic:

| Topic | Candidate file paths (check in order) |
|---|---|
| `spec` | `specs/spec.md` |
| `plan` | `specs/plan.md` |
| `characters` | `specs/characters/` (directory index) |
| `npc` | `specs/characters/[NPC_NAME].md`, then fuzzy-match in `specs/characters/` |
| `branches` | `specs/plan.md`, then target node's `outlines/[NODE_ID].md` |
| `endings` | `specs/endings.md` |
| `mechanics` | `specs/mechanics.md` |
| `world-building` | `specs/world-building.md` |
| `world-map` | `specs/world-map.md` (create from `templates/world-map-template.md` if absent) |
| `variables` | `specs/variables.md` |
| `series` | `series/series-bible.md` |
| `glossary` | `specs/glossary.md` |
| `(custom)` | No canonical file � blank-slate topic |

**Resume check**: look for `specs/brainstorm-[topic].md` (or `specs/brainstorm-npc-[NPC_NAME].md`).
- Found: offer `(r) Resume` or `(n) New session`. If `r`: load prior notes into `SESSION.prior_log`.
- Not found: proceed.

**Branch on file existence**:
- **File found**: read it. Set `SESSION.has_context = true`. Summarise in 2�3 bullets so the user can confirm the AI read it correctly.
- **File not found**: set `SESSION.has_context = false`. Display: `? No [filename] found � starting from scratch.`

Load these **secondary context files** silently (use only to avoid re-asking settled facts and to surface cross-topic conflicts):

| Topic | Secondary files |
|---|---|
| `spec` | `.specify/memory/constitution.md`, `specs/mechanics-[ruleset].md` (if RPG) |
| `plan` | `specs/spec.md`, `specs/endings.md`, `specs/quests.md` (if RPG) |
| `characters` / `npc` | `specs/spec.md`, `specs/plan.md`, `specs/npc-roster.md` (if RPG) |
| `branches` | `specs/spec.md`, `specs/variables.md`, `specs/mechanics.md` |
| `endings` | `specs/plan.md`, `specs/variables.md` |
| `mechanics` | `.specify/memory/constitution.md`, `specs/variables.md`, `specs/mechanics-[ruleset].md` (if RPG) |
| `world-building` | `specs/spec.md`, `specs/variables.md` |
| `variables` | `specs/plan.md`, `specs/mechanics.md`, `specs/mechanics-[ruleset].md` (if RPG) |
| `series` | `specs/spec.md`, `specs/endings.md` |
| `glossary` | `specs/world-building.md`, `specs/variables.md` |
| `factions` (RPG) | `specs/spec.md`, `specs/variables.md`, `specs/mechanics-[ruleset].md` |
| `encounters` (RPG) | `specs/spec.md`, `specs/mechanics.md`, `specs/quests.md`, `specs/bestiary.md` (if Tabletop) |
| `companion-arcs` (RPG) | `specs/spec.md`, `specs/characters/`, `specs/variables.md`, `specs/npc-roster.md` |
| `difficulty-curve` (RPG) | `specs/spec.md`, `specs/plan.md`, `specs/mechanics-[ruleset].md` |
| `mechanics-rpg` (RPG) | `.specify/memory/constitution.md`, `specs/variables.md`, `specs/mechanics-[ruleset].md` |
| `(custom)` | None |

---

## Step 3 � Session Start

If session length not set via argument, ask:
```
How deep do you want to go?
  q  quick    � ~5 questions, highest-priority gaps only
  s  standard � ~10 questions, core coverage  (default)
  d  deep     � unlimited, follow every thread
```

Display session header:
```
---------------------------------------------
  BRAINSTORM SESSION
  Topic    : [topic]  [? loaded from file | ? new topic]
  Mode     : [With context | Blank slate | Challenge]
  Depth    : [Quick � Standard � Deep]  RPG Mode : [Yes – Platform: [Tabletop/Computer], Ruleset: [D&D 5e/Pathfinder 2e/Shadowrun 6e] | No]  Resuming : [Yes � [N] prior insights loaded | No]
---------------------------------------------
Commands available at any time:
  done        � end session and choose what to do with notes
  cancel / q  � discard everything and exit
  switch      � change topic (current insights preserved)
  summary     � show running insight summary
  !skip       � skip this question
---------------------------------------------
```

Initialise an **Insight Log** � ordered list of Q&A pairs plus derived insight and any conflict flags.

---

## Step 4 � Brainstorm Loop

Runs until the user types `done`, `cancel`, or `switch`.

### 4a � Select the next question

**Depth gate**: if `quick` and N = 5, or `standard` and N = 10, surface a stopping point before continuing.

**Challenge mode**: lead with questions that stress-test the most confident decisions in the loaded file. Frame as: *"Your [element] is [current value] � what is the strongest argument this is wrong?"*

**Normal priority order**:
1. **Tension probe**: if the previous answer introduced a contradiction with the loaded file or a prior answer, probe that tension first.
2. **Gap probe**: identify the most important unanswered dimension for this topic (see question banks) and ask about it.
3. **Depth probe**: if a previous answer was vague, follow up by naming the narrative or mechanical function the element must serve.
4. **Wildcard**: once core gaps are covered, draw from the Wildcard bank.

Never repeat a question or ask about something definitively answered in the loaded file (except in Challenge mode).

### 4b � Ask the question

```
[Q{N}]  {question text}

(done � cancel � switch � summary � !skip)
```

After the user answers:
- Acknowledge in 1�2 sentences. The acknowledgement **must name at least one** of:
  - The **narrative or mechanical function** this element serves
  - The **tension it creates** with another locked decision
  - A **specific node, variable, or spec section** it will affect
  Do not produce generic filler.
- Log the Q&A pair and derived insight into the Insight Log.
- If the answer conflicts with the loaded file or a prior answer:
  ```
  ?  Conflict with [filename / Q{N}] � [brief description].
     Logged as Change Candidate [K].
  ```

### 4c � Mid-loop commands

| Command | Action |
|---|---|
| `done` | End loop. Go to Step 5. |
| `cancel` / `q` | Discard all data. Exit: `Brainstorm cancelled. No files were changed.` |
| `switch` | Return to Step 1. Prior insights preserved and labelled. |
| `summary` | Display current Insight Log. Return to loop after. |
| `!skip` | Skip question; doesn't count toward depth limit. |

---

## Question Banks

Select the most valuable questions based on what is already known � do not ask all.

### `spec`
- What is the central dramatic question � the one sentence the whole game answers?
- What is the player's core agency in this story � what can they actually change?
- What genre conventions does this game follow � and which does it subvert?
- What is the emotional promise to the player? (e.g. tension, catharsis, discovery)
- What must the ending feel like � not what happens, but what it resolves?

### `plan`
- What is the shape of the branch graph � wide-then-narrow, tree, parallel paths?
- Where is the point of no return � the node where all paths converge?
- Are there nodes the player is likely to miss entirely � is that intentional?
- How does the act structure create escalating stakes across the node graph?
- Which branches are purely cosmetic vs. which create genuinely different story outcomes?

### `characters` / `npc`
- What does this NPC want from the player � and what do they actually need?
- What is the lie this NPC believes about themselves or the world?
- How does this NPC's behaviour change based on trust level?
- What is the most surprising thing this NPC would do under pressure?
- How does this NPC speak differently from every other character in the game?
- What state change for this NPC has the most downstream narrative impact?

### `branches`
- What makes choice A genuinely different from choice B � not just cosmetically?
- What is the player actually trading off when they pick each option?
- Is there an obviously dominant choice � and if so, how do you rebalance it?
- What information does the player need to make this choice meaningfully?
- What are the downstream consequences that make this branch matter two acts later?
- Are there conditional choices here � what variable gates them and why?

### `endings`
- What variable states does this ending require � and can they all be achieved on one path?
- What is the emotional register of this ending � how should the player feel?
- Is this ending clearly distinguishable from the others � what makes it unique?
- What does this ending say about the player's choices throughout the game?
- Is this ending reachable by a player who isn't trying to find it?
- What is the minimum set of choices that locks this ending in vs. others?

### `mechanics`
- What narrative experience does this mechanic create � what does it feel like to the player?
- Is this mechanic Tier 1 (export-ready) or Tier 2 (requires custom implementation)?
- How does this mechanic interact with the player's sense of agency and consequence?
- What is the failure mode of this mechanic � what breaks if it's misapplied?
- Are there nodes where this mechanic would feel forced or gamey � how do you avoid them?

### `world-building`
- What is the single most important rule of this world � what happens when it breaks?
- What does everyday life look like for the people who live here?
- What history do the characters not fully know but that shapes their reality?
- What does this world cost its inhabitants � what is the everyday price of living here?
- Which world rule has the most impact on the branch structure and variable design?

### `variables`
- Is this variable tracking player behaviour, world state, or NPC relationship � are those categories clean?
- What is the default value for this variable on a fresh playthrough � is it the right narrative assumption?
- Are there variable combinations that produce contradictions or unreachable nodes?
- Which variable has the most downstream impact on ending conditions?
- Is any variable doing double duty � tracking two things at once � that should be split?

### `series`
- What variable states must carry over to Entry N+1 � and what is the canonical default for a fresh start?
- What world rule established in this entry must not be contradicted in later entries?
- Which NPC survival or state has the most downstream impact on series continuity?
- What series-level question does this entry open without answering?
- Are there contradictions between this entry's endings and the series bible?

### `glossary`
- What invented terms appear in node prose that a player would not intuitively understand?
- Are there in-world variable names visible to the player that need consistent spelling?
- Which term is most likely to be used inconsistently across a long set of nodes?
- Are there terms that appear in choice labels � do they feel natural and unambiguous?

### Wildcard bank

- Which node are you most unsure about � what is the design question it hasn't answered yet?
- What would the player do if they could break one rule in this world?
- Which ending is currently least satisfying � what would make it feel earned?
- What mechanic are you avoiding implementing because it feels too complex � is the complexity actually worth it?
- What is the one NPC relationship that has the most unrealised narrative potential?
- Which branch currently feels like a trap rather than a choice � and why?
- What does this game have to say that no similar game has said in quite this way?

---
## RPG-Specific Question Banks

**Used when `SESSION.is_rpg = true` to surface RPG design concerns.** These augment standard banks for the selected `[PLATFORM]` and `[RULESET]`.

### `spec` (with RPG focus)

**If Tabletop**:
- What is the recommended party size, and what level/class diversity matters most to your story?
- How many sessions do you expect? (This drives encounter count, companion arcs, and variable scope.)
- What is the expected character progression arc – do players hit high-level spells/powers mid-campaign?
- What happens to characters who die – do they respawn, retire, or create new ones?

**If Computer Game**:
- What difficulty modes should exist (e.g., Story/Normal/Hard)? How much does each scale encounters and reduce rewards?
- What is the target playtime from start to ending? (This gates encounter density, side quest count, and progression speed.)
- What playstyles do you want to support (Combat/Dialogue/Exploration) and should they converge or diverge?

### `plan` (with RPG focus)

**If Tabletop**:
- How many sessions does each act take – does pacing match table expectations (2-4 hours per session)?
- Where do companions recruit, and do they follow the player immediately or join later?
- Which ending is locked into which session range – can players reach it via multiple paths in Session 3-12?

**If Computer Game**:
- How many chapters/playable hours until difficulty spikes or new systems unlock?
- Where do playstyle routes reconverge – do solo combat players and solo dialogue players reach the same climax?
- Which story beats are mandatory vs. optional – can players miss entire questlines?

### `mechanics` (with RPG focus)

- How do skill check alternatives work – if not Combat, what other paths resolve this encounter (Social, Stealth, Puzzle)?
- What resource economy matters most (Hit Points, Mana, Supplies, Morale) – which is closest to the story?
- What variable state at the ending defines success – is it faction reputation, companion survival, or character resources?

### `factions` (RPG-specific topic)

- How many factions matter to the story – can the player align with all, some, or none?
- What is the reputation range (-100 to +100 typical) – at what thresholds do factions become allies/enemies?
- Do faction choices create mutual exclusivity (siding with Faction A locks out Faction B) or independence?
- What is the minimum viable reputation to recruit each companion or unlock each ending?
- Are there nodes where multiple factions' representatives meet – how do they react to each other?

### `encounters` (RPG-specific topic – Tabletop-focused)

- How does this encounter fit the party's level – what is the expected CR or difficulty rating?
- What are the 2-3 alternative paths through this encounter (Combat, Social, Stealth, Puzzle)?
- Does combat have environmental hazards, reinforcements, or escape routes – or is it straightforward?
- How many rounds of combat do you expect – too long encounters (10+ rounds) break table pacing?
- What loot drops here – does it serve future encounters or story progression?

### `companion-arcs` (RPG-specific topic)

- At what approval threshold does this companion recruit – does the player choose or is recruitment automatic?
- What approval events trigger during the campaign – do companions have scenes at key sessions/chapters?
- Is there a romance arc – at what approval threshold do romance options open?
- What are the companion's possible fates (survives, dies, betrays, leaves) – are they all reachable?
- How does this companion react to player choices – do they support, oppose, or remain neutral by default?

### `difficulty-curve` (RPG-specific topic – Computer-focused)

- Does difficulty scale per chapter/region, or is it global?
- At what point do new mechanics unlock (e.g., spells, abilities, vehicles) – does difficulty spike then?
- Are there "difficulty locks" where Hard mode becomes impossible (certain bosses unbeatable, story gates unreachable)?
- How does XP/Loot scale across difficulties – do Hard players earn 2× XP or stay equivalent?
- What accessibility options exist (colorblind mode, adjustable timers, difficulty-independent story gates)?

### `mechanics-rpg` (RPG-specific topic)

- What house rules diverge from the base ruleset (D&D 5e, Pathfinder 2e, Shadowrun 6e)?
- Are critical successes and critical failures more dramatic than normal successes/failures?
- How do you handle skill checks where multiple party members could attempt (do all roll, or one per character)?
- What variables track system-specific resources (Karma in Shadowrun, Hero Points in Pathfinder 2e, Spell Slots in D&D 5e)?
- Are there mechanics that feel forced or gamey – can they be cut or simplified?

### `world-map` (RPG-specific topic)

**Spatial model & structure**:
- What is the top-level spatial model — Linear (fixed Region sequence), Hub-and-Spoke (central hub with radiating Regions), or Open-World (all Regions accessible from start)?
- How many Regions does the world have — and does the number create variety without becoming overwhelming?
- Do Regions unlock by act, quest completion, faction alignment, or player decision?
- Is there a Region the player can permanently miss or be locked out of — is that intentional?

**Region & Area design**:
- What distinct atmosphere or theme makes each Region feel different from the others (terrain, faction, tone)?
- How many Areas does each Region contain — do Areas feel like meaningful sub-divisions or are they arbitrary?
- What Area types exist (dungeon, wilderness, urban, sea, underground) — is there enough variety?
- Does any Area feel too large or too combat-dense — where might players get fatigued?

**Location & hub design**:
- What Locations serve as rest points in each Area — is there always a safe place the player can reach without forced combat?
- How many scenes does each Location contain — is the scene count consistent with the Location's narrative weight?
- Do hub passages (LOC-xxx) offer at least 3 meaningful navigation choices (scenes + travel exits)?
- Are there Locations that exist in the design but have no scenes yet — what's blocking them?

**Travel & connections**:
- Which travel connections are one-way — and does the player have enough warning before crossing a point of no return?
- Are travel scenes (scene_type: travel) interesting in themselves, or are they pure corridor transitions?
- Do fast-travel options undermine exploration — should fast travel be gated behind discovery?
- Are there any "orphan" Locations with no travel entry scene — how does the player first reach them?

**Spatial variables & state**:
- What `$region_*` variables track per-Region progression (unlocked, faction dominant, quest stage)?
- What `$area_*` variables track per-Area state (explored, cleared, unlocked, closed)?
- What `$loc_*` variables track per-Location state (visited, intact/damaged/destroyed, NPC roster)?
- Are there campaign-wide (`$world_*`) flags driven by spatial events (e.g., a Region falls, a war zone expands)?

**Challenge mode additions** *(asked if `challenge` flag set)*:
- Pick the Region that would hurt most to cut — now justify why it can't be merged with an adjacent Region.
- Which Area currently has no rest Location — is that a gap or a design choice?
- Which travel connection is the most story-critical — what breaks if that path is removed or blocked?
- Do all Regions have at least one moment where the player feels the Region's theme — or does any feel like filler?

---
## Step 5 � Session End

When the user types `done`:

```
---------------------------------------------
  BRAINSTORM COMPLETE
  Topic    : [topic]
  Questions: [N] asked
  Insights : [M] logged
  Conflicts: [K] flagged
---------------------------------------------

Key findings:
  � [1-sentence insight]
  � ...  (max 6 bullets)

What do you want to do with these results?

  1  Save brainstorm notes      � write notes file alongside the topic file
  2  Update [topic file]        � apply findings and resolve conflicts directly
                                  (only shown if SESSION.has_context = true)
  3  Both                       � save notes AND update the topic file
  4  Merge all topics           � combine notes from every topic this session
                                  (only shown if user used  switch  at least once)
  5  Cancel                     � discard everything, no files written
```

---

## Step 6 � Output

### Option 1 or 3 � Save brainstorm notes

Write to `specs/brainstorm-[topic].md` (or `specs/brainstorm-npc-[NPC_NAME].md`):

```markdown
# Brainstorm Notes � [Topic]

<!-- Generated: [DATE] | Questions: [N] | Insights: [M] -->

## Session Summary

[2�3 sentences on what the session explored and what it surfaced]

## Key Insights

### [Short insight title]
**Question asked**: [Q text]
**Answer**: [verbatim key points]
**Derived insight**: [AI synthesis � what this means for the design]

[repeat block per insight]

## Change Candidates

| # | Existing ([filename]) | Brainstorm suggests | Priority | Status |
|---|---|---|---|---|
| 1 | [current content] | [new direction] | HIGH / MED / LOW | PENDING |

## Open Questions

- [ ] [unresolved question]

## Raw Q&A Log

**Q1**: [question]
**A**: [answer]

[continue for all N questions]
```

### Option 2 or 3 � Update topic file

For each Change Candidate: show proposed edit (old ? new) and ask for confirmation before writing:
```
Change [N] of [K]:
File    : [filename]
Current : [existing text snippet]
Replace : [new text]
Apply this change? (y / n / edit)
```
For new insights that add information without conflict: append to the appropriate section. Do not restructure sections not being changed.

If no topic file exists and the user chose option 2 or 3: offer to create from the appropriate template and populate `[NEEDS CLARIFICATION]` tokens with brainstorm findings. Leave all other placeholders intact.

### Option 4 � Merge all topics

Write `specs/brainstorm-merged-[date].md` with one `## [Topic]` section per topic covered, plus a `## Cross-Topic Connections` section linking insights that affect multiple files (e.g. a variable design decision that changes an ending condition).

---

## Operating Rules

- **Never write any file until Step 6.** The entire loop is non-destructive.
- **One question at a time.** Never present multiple questions in a single turn.
- **No leading the witness.** Questions must be open-ended � do not embed an assumed answer.
- **Honour the loaded file.** Do not contradict or silently ignore existing content. Surface conflicts as Change Candidates.
- **No fabrication.** Do not invent design decisions. Ask, synthesise, and reflect � do not author.
- **Depth is binding.** When the depth limit is reached, surface the stopping point � do not slip in extra questions.
- **Acknowledgements must be specific.** Every post-answer acknowledgement must name a narrative function, a mechanical implication, or an affected node/variable. Generic affirmations are not permitted.
- **Prior session data is read-only.** Prior brainstorm notes inform question selection and conflict detection but cannot be modified by the current session.

## Post-Execution Hooks

Check for extension hooks after execution:
- Look for `hooks.after_brainstorm` in `.specify/extensions.yml`. Process as standard hook block. Skip silently if absent.

