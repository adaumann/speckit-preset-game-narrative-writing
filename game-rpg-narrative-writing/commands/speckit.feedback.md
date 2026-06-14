---
description: Ingest playtest feedback — categorize issues by type, map to node IDs, assign severity, generate prioritized revision tasks in tasks.md. For RPG campaigns (tabletop D&D/Pathfinder/Shadowrun and computer game), tracks companion loyalty feedback, faction reputation edge cases, session pacing issues, playstyle route problems, and accessibility variant consistency. Closes the playtest round as a proper workflow step.
handoffs:
  - label: Start Revisions
    agent: speckit.revise
    prompt: Begin targeted revisions for the CRITICAL issues from the playtest feedback log
    send: true
  - label: Run Continuity Check
    agent: speckit.continuity
    prompt: Run a full continuity check to cross-reference feedback against known continuity issues
    send: true
  - label: Run Node Checklists
    agent: speckit.checklist
    prompt: Run quality checklists for the nodes flagged in the feedback log
    send: true
  - label: Check Project Status
    agent: speckit.status
    prompt: Show current project status and outstanding tasks
    send: true
---

# speckit.feedback

Ingest playtest feedback, categorize issues, assign severity, and generate revision tasks in `tasks.md`. The feedback log becomes the audit trail for the playtest round.

**🎮 RPG Campaign Support**: Detects companion loyalty issues (tabletop: incorrect loyalty changes, state tracking problems, recruitment gate failures), faction reputation feedback (quest gating, reputation persistence), session/chapter pacing (tabletop: session length, encounter balance; computer: route pacing, accessibility in route choices), and playstyle route isolation (computer: route-exclusive content leakage, accessibility variant consistency).

## User Input

```text
$ARGUMENTS
```

You **MUST** consider the user input before proceeding (if not empty). Accepted arguments:
- A file path or quoted block of raw playtest notes to ingest
- A tester name (e.g. `"Alice"`) for labeling the feedback log
- `--session [LABEL]` — label the playtest session
- `--tester [ID]` — tester identifier (use "anonymous" if not specified)
- `--target [sugarcube|ink]` — which export was tested
- `--resolve [FB-NNN]` — mark an issue as resolved
- `--summary` — print summary of open issues without ingesting new ones
- `triage` — re-run triage only on an existing feedback log without regenerating tasks
- `tasks` — generate tasks from an already-triaged feedback log

## Pre-Execution Checks

**Extract Platform & Ruleset** (auto-detect RPG context):
- Read `.specify/memory/constitution.md` YAML frontmatter and extract `[PLATFORM]` and `[RULESET]`
- If `[PLATFORM]` = "Tabletop": Set `SESSION.is_rpg = "tabletop"` and enable Tabletop feedback categories (TR-*)
- If `[PLATFORM]` = "Computer Game": Set `SESSION.is_rpg = "computer"` and enable Computer feedback categories (CR-*)
- If neither detected: Set `SESSION.is_rpg = false` (generic feedback model)
- Store `SESSION.platform` and `SESSION.ruleset` for RPG feedback classification

**Load RPG-Specific Documents** (if platform detected):
- **Tabletop**: Load `specs/companions.md` (for companion loyalty feedback), `specs/factions.md` (for faction reputation feedback), `specs/mechanics-[ruleset].md` (for ruleset-specific mechanical issues)
- **Computer**: Load `specs/variables.md` (for route isolation issues), `specs/accessibility.md` (for accessibility consistency feedback)

**Check for extension hooks (before feedback processing)**:
- Check if `.specify/extensions.yml` exists in the project root.
- If it exists, read it and look for entries under the `hooks.before_feedback` key.
- Process as standard hook block (Optional/Mandatory). Skip silently if absent.

---

## Steps

### Step 1 — Setup

Run `{SCRIPT}` from repo root. Load `nodes/` file list (required to validate node IDs referenced in feedback).

### Step 2 — Identify the Feedback Source

- If `$ARGUMENTS` contains a file path → read that file as raw notes
- If `$ARGUMENTS` contains quoted text → use it directly
- If a `feedback/` directory exists → list existing feedback log files; ask which to process or process all unprocessed ones
- If `--summary` → skip to Step 7 (display open issues, no ingestion)
- If `--resolve [FB-NNN]` → skip to Step 6
- If nothing provided → ask: "Paste the playtest notes, or provide a file path."

### Step 3 — Create or Locate the Feedback Log File

- Target: `feedback/[tester-slug]-[YYYY-MM-DD].md` (slugify tester name)
- Use `templates/feedback-template.md` structure
- Fill Metadata table from `$ARGUMENTS` values and context
- Paste raw notes verbatim into the **Raw Notes** section

### Step 4 — Triage

Parse raw notes and populate the per-category issue tables.

**Category classification rules** (Generic):

| Keyword signals | Category |
|---|---|
| "dead end", "can't get to", "wrong node", "missing option", "branch doesn't appear" | BR — Branch |
| "variable not set", "wrong value", "flag missing", "trust didn't change", "hook didn't fire" | VA — Variable |
| "dragged", "rushed", "too long here", "tension dropped", "pacing off" | PA — Pacing |
| "confused", "lost track", "unclear choice", "didn't understand", "needed more context" | CL — Clarity |
| "obvious choice", "no trade-off", "trivial", "one option dominates", "mechanic felt useless" | BA — Balance |
| "contradicts earlier", "NPC wrong state", "world rule broken", "remembered wrong" | CO — Continuity |
| "crashed", "syntax error", "output broken", "wrong passage name", "unsupported tag" | EX — Export |

**Category classification rules** (RPG-Specific, if platform detected):

| Keyword signals | Category | Platform |
|---|---|---|
| "companion didn't trust", "loyalty didn't change", "shouldn't have recruited yet", "loyalty reset" | TR-CL — Companion Loyalty | Tabletop |
| "companion disappeared", "NPC state broken", "recruitment failed", "companion out of sync" | TR-CS — Companion State | Tabletop |
| "faction rep didn't change", "faction quests still available after betrayal", "rep didn't persist" | TR-FR — Faction Reputation | Tabletop |
| "session too long", "encounters too easy/hard", "pacing felt off across session", "session didn't resolve tension" | TR-SP — Session Pacing | Tabletop |
| "mechanic didn't work", "DC felt wrong", "hero points not triggering", "essence calculation wrong" | TR-ME — Ruleset Mechanics | Tabletop |
| "route bleed-through", "could access combat nodes in stealth", "route variable leaked", "got both route rewards" | CR-RI — Route Isolation | Computer |
| "stealth route is too slow", "combat has way more content", "diplomacy felt incomplete", "route felt unfair" | CR-RB — Route Balance | Computer |
| "colorblind mode broken in diplomacy", "audio cues missing in combat", "motor accessibility only in one route" | CR-AX — Accessibility Consistency | Computer |
| "chapter pacing felt off", "didn't know which chapter I was in", "escalation didn't build" | CR-CP — Chapter Pacing | Computer |

**Node ID mapping**: when the tester references a passage name, scene label, location name, or description, map to the closest `NODE-NNN`, `LOC-{ShortName}` (hub passage), `AREA-{ShortName}` (area-level feedback), `SESSION-N-NODE-NNN` (for tabletop), or `CHAPTER-N-NODE-NNN` (for computer) by cross-referencing node file titles, `specs/plan.md`, `specs/locations.md`, and `specs/world-map.md`. When no node is identifiable, mark as `NODE-UNKNOWN`.

**Severity assignment** (Generic):
- CRITICAL: blocks progression, crashes export, breaks variable state, or creates unwinnable state
- HIGH: significantly degrades experience (major confusion, obvious dominant choice, NPC state contradiction)
- MEDIUM: noticeable but non-blocking; addressable in polish
- LOW: minor style preference or "nice to have"

**Severity assignment** (RPG-Specific additions):

| Issue Type | Severity Bump |
|---|---|
| Companion loyalty choice doesn't change loyalty (any value) | CRITICAL (blocks entire companion system) |
| Faction rep choice doesn't persist to next session | CRITICAL (breaks campaign continuity) |
| Route-exclusive content accessible in wrong route | CRITICAL (breaks route commitment) |
| Accessibility variant broken in any route | HIGH (violates accessibility promise) |
| Session too short/long by 30%+ vs. planned pacing | HIGH (affects campaign structure) |
| Ruleset mechanical DC/bonus calculated incorrectly | HIGH (undermines system credibility) |

**Positive notes**: extract any explicit "this worked well" or "keep this" comments into the POS section. Do not revise these away.

### Step 5 — Resolve Duplicates

If multiple testers flagged the same node for the same category, merge into one issue entry with "N testers" noted in the Description. Increment severity if ≥ 2 testers independently raised the same issue.

### Step 6 — Resolve Flow (if `--resolve`)

- Confirm the issue ID exists in the feedback log
- Mark issue as RESOLVED
- Add resolution description and node version where fix was applied
- Update summary counts

### Step 7 — Generate Revision Tasks (unless `triage` mode)

Scan `tasks.md` for existing `## Playtest Round` sections. Determine the next round number: if none exist, use Round 1; if one or more exist, use highest N + 1 **only if the current tester's feedback file was not already processed** (check whether any `[tester-slug·` task IDs already appear in tasks.md — if so, skip task generation and report: `ℹ️ Tasks for this tester already exist in tasks.md. Use the triage argument to re-triage only.`).

Add a section to `tasks.md` under `## Playtest Round [N]` with sub-header: `### [tester-name] — [YYYY-MM-DD] ([target])`

**Per-issue task generation**:
- One task per CRITICAL and HIGH issue:
  ```
  - [ ] [FEEDBACK] [tester-slug·BR-001] NODE-007 — Dead end reached from NODE-004 via choice B (2 testers)
  - [ ] [FEEDBACK] [tester-slug·VA-002] NODE-012 — trust_mira not set before read at NODE-012
  ```
- MEDIUM issues: one grouped task per category:
  ```
  - [ ] [FEEDBACK] [MEDIUM-CL] Clarity polish pass — 3 medium clarity notes (see feedback/alice-2026-04-27.md)
  ```
- LOW issues: do NOT add to tasks.md. Preserved in feedback log only.
- Fill the **Revision Tasks Generated** table in the feedback log.

### Step 8 — Update Feedback Log Status

Update `Status` field in the log Metadata table to `tasks generated`.

### Step 9 — Report

```
✅ Feedback processed

| Metric          | Value                                              |
|---|---|
| Tester          | [name]                                             |
| Session         | [label]                                            |
| Export target   | [sugarcube / ink]                                  |
| Raw notes       | [N] items                                          |
| Issues found    | [N] (CRITICAL: N, HIGH: N, MEDIUM: N, LOW: N)      |
| Tasks generated | [N] (added to tasks.md Playtest Round [N])         |
| Log saved       | feedback/[tester-slug]-[YYYY-MM-DD].md             |
```

If any CRITICAL issues were found:
```
⚠ CRITICAL issues require immediate attention before next playtest:
  [FB-NNN] NODE-NNN — [brief description]
```

---

## RPG Campaign Feedback Integration

### Tabletop Campaign Feedback

#### Companion Loyalty Feedback (TR-CL)

**Detect these issues**:
- "Loyalty didn't change after [choice]" → Variable not set properly
- "Companion said [dialogue] but I never recruited them" → Recruitment gate failed
- "Companion disappeared after [session]" → State not persisting across sessions
- "[Companion name] reacted wrongly to my prior choice" → Loyalty state incorrect or foreshadowing missed

**Example feedback entry**:
```
FB-TR-CL-001: SESSION-3 NODE-012, "Trust Mira with secret"
  Tester said: "I chose to trust Mira, but in Session 4 she acted like I didn't tell her anything."
  Issue: mira_loyalty should increase by +3, but SESSION-4 node not checking loyalty value
  Severity: HIGH (loyalty choice invisible; companion feels unresponsive)
```

**Task generation**:
- If loyalty variable not set: `- [ ] [FEEDBACK] [TR-CL-001] Fix mira_loyalty increment in SESSION-3-NODE-012`
- If loyalty state not persisting: `- [ ] [FEEDBACK] [TR-CL-001] Update SESSION-4-BRIEFING.md to reflect Mira's current loyalty state`

**Campaign impact**:
- Affects: `campaign-guide.md` (companion relationship section needs updating)
- Affects: `SESSION-N-BRIEFING.md` (companion state at session start)
- Affects: Later recruitment gates (if loyalty tracking is broken, recruitment becomes impossible)

#### Faction Reputation Feedback (TR-FR)

**Detect these issues**:
- "I helped the Temple, but temple quests still blocked" → Reputation gate not applied
- "Faction reputation didn't carry to next session" → State reset or not persisted
- "[Faction name] treated me wrong for my prior choice" → Reputation state incorrect at session start

**Example feedback entry**:
```
FB-TR-FR-002: SESSION-4 NODE-010 choice affects SESSION-5 NODE-020
  Tester said: "I sided with the Temple in Session 4, but in Session 5 the Temple quests were still locked."
  Issue: faction_temple_reputation should be +100 after SESSION-4, unlocking quests at SESSION-5-NODE-020
  Severity: CRITICAL (faction choice has zero visible impact)
```

**Task generation**:
- If gate not applied: `- [ ] [FEEDBACK] [TR-FR-002] Add reputation gate check to SESSION-5-NODE-020 temple quests`
- If not persisting: `- [ ] [FEEDBACK] [TR-FR-002] Verify faction_temple_reputation carries in SESSION-5-BRIEFING.md`

**Campaign impact**:
- Affects: `campaign-guide.md` (faction ally/enemy status section)
- Affects: `SESSION-N-BRIEFING.md` (faction availability and NPC reactions per session)
- Affects: Multiple quest chains (gates depend on faction rep)

#### Session Pacing Feedback (TR-SP)

**Detect these issues**:
- "Session ran over 4 hours, felt dragged" → Session content too much
- "Finished in 45 minutes, anticlimactic" → Session too short
- "Encounter was trivial" or "Encounter was impossible" → DC/enemy balance per ruleset
- "Session didn't resolve the tension" → Pacing structure wrong (no climax/resolution moment)

**Example feedback entry**:
```
FB-TR-SP-003: SESSION-3 total length
  Tester said: "We spent 3.5 hours and only got through half the content. Felt exhausting."
  Issue: Planned pacing ~2 hours, actual ~3.5 hours (75% overrun)
  Severity: HIGH (affects entire campaign pacing plan)
```

**Task generation**:
- `- [ ] [FEEDBACK] [TR-SP-003] Trim SESSION-3 encounters: remove 1 side encounter or consolidate 2 into 1`

**Campaign impact**:
- Affects: `campaign-pacing-guide.md` (session structure and time estimates)
- Affects: Future session planning (if SESSION-3 overruns, SESSION-4 pacing may need adjustment)

#### Ruleset Mechanical Feedback (TR-ME)

**Detect these issues**:
- "DC 25 is impossible for level 3 characters" → DC wrong for ruleset
- "Hero points didn't work as expected" → Mechanical implementation wrong
- "[Ruleset] rule applied incorrectly" → System-specific mechanics broken

**Example feedback entry**:
```
FB-TR-ME-004: SESSION-2-NODE-015, "Escape the guards" (D&D 5e, level 3)
  Tester said: "DC 20 Stealth check is impossible with level 3 modifier +3. Nobody could pass."
  Issue: D&D 5e level 3 max Stealth modifier ~5 (DEX 16 + proficiency 2). DC 20 is 15 points too hard.
  Fix: Reduce to DC 10 (moderate difficulty) or DC 15 (hard but possible with +5 mod)
  Severity: HIGH (encounter unwinnable with proper mechanics)
```

**Task generation**:
- `- [ ] [FEEDBACK] [TR-ME-004] Fix SESSION-2-NODE-015 DC: change from 20 to 15 (per D&D 5e level 3 guidelines)`

**Campaign impact**:
- Affects: `mechanics-[ruleset].md` (mechanical guidelines for future sessions)
- Affects: `campaign-guide.md` (house rules if any adjustments are made)

### Computer Game Feedback

#### Route Isolation Feedback (CR-RI)

**Detect these issues**:
- "I could access stealth content in my combat playthrough" → Route variable not checked
- "Got rewards from both routes" → Route gates not enforced
- "Could use stealth ability in combat route" → Route-exclusive mechanics leaking

**Example feedback entry**:
```
FB-CR-RI-001: CHAPTER-3 route gates
  Tester said: "I chose combat route, but could still pick the stealth sneak-attack ability from the other route."
  Issue: $player_playstyle gate not applied to CHAPTER-3 ability node
  Severity: CRITICAL (route commitment not enforced)
```

**Task generation**:
- `- [ ] [FEEDBACK] [CR-RI-001] Add $player_playstyle == "combat" gate to CHAPTER-3 node offering stealth abilities`

#### Route Balance Feedback (CR-RB)

**Detect these issues**:
- "Stealth route had way more dialogue choices" → Uneven route content
- "Combat felt way too short compared to diplomacy" → Route length disparity
- "[Route name] was boring/trivial" → Route feels incomplete or underdeveloped

**Example feedback entry**:
```
FB-CR-RB-002: Route balance across chapters
  Tester said: "Combat route felt like it had half the content of stealth route. Combat done in 2 hours, stealth took 4."
  Issue: Route balance ratio Combat:Stealth = 50:100 (should be 80:100 or better)
  Severity: HIGH (affects replayability and route parity)
```

**Task generation**:
- `- [ ] [FEEDBACK] [CR-RB-002] Expand combat-route content: add 2-3 encounters and dialogue options to balance playtime`

#### Accessibility Variant Consistency Feedback (CR-AX)

**Detect these issues**:
- "Colorblind mode works in stealth but not combat" → Accessibility variant incomplete
- "Audio cues only in diplomatic route" → Accessibility inconsistent across routes
- "Motor accessibility missing in CHAPTER-3" → Accessibility coverage incomplete

**Example feedback entry**:
```
FB-CR-AX-003: Accessibility in combat route
  Tester said: "Colorblind mode shows patterns in stealth route but not in combat route. Confused about enemy status."
  Issue: $accessibility_colorblind gate applied in CHAPTER-2 stealth nodes but not combat nodes
  Severity: HIGH (violates accessibility promise; creates unequal experience)
```

**Task generation**:
- `- [ ] [FEEDBACK] [CR-AX-003] Apply colorblind patterns to combat-route enemy indicators (CHAPTER-2-3 combat nodes)`

#### Chapter Pacing Feedback (CR-CP)

**Detect these issues**:
- "Chapter felt rushed" or "Chapter dragged" → Chapter length/pacing wrong
- "Didn't know I was moving to a new chapter" → Chapter transitions unclear
- "Chapter didn't escalate properly" → Pacing structure/beat progression wrong

**Example feedback entry**:
```
FB-CR-CP-004: CHAPTER-3 pacing and escalation
  Tester said: "Chapter 3 felt like it went on forever. Lots of repeated encounters but no sense of escalation."
  Issue: Chapter 3 too long (8 nodes vs. typical 5-6); missing climactic moment
  Severity: MEDIUM (impacts engagement but not progression)
```

**Task generation**:
- `- [ ] [FEEDBACK] [CR-CP-004] Add climactic node to CHAPTER-3: consolidate 3 side encounters into 1 boss encounter`

### Feedback Integration with Campaign Prep Documents

When processing RPG feedback, note which campaign documents need regeneration or updates:

**For Tabletop Campaigns**:
- **Companion/faction feedback** → Update `campaign-guide.md` companion/faction sections
- **Session pacing feedback** → Update `campaign-pacing-guide.md`
- **Session-specific feedback** → Update `SESSION-N-BRIEFING.md` for affected session
- **Mechanic feedback** → Update `mechanics-[ruleset].md` if house rules changed

**For Computer Games**:
- **Route feedback** → Update `specs/variables.md` if route isolation needs tightening
- **Pacing feedback** → Update chapter structure if chapters too long/short
- **Accessibility feedback** → Update `specs/accessibility.md` coverage matrix

### Best Practices for RPG Feedback

**Session Playtests (Tabletop)**:
- Record feedback immediately after SESSION ends (not days later; memory fades)
- Separately note: companion reactions, faction NPC behavior, enemy encounter difficulty, pacing (felt rushed/slow)
- Track: "Did choices feel meaningful?" "Did companion feel responsive to prior choices?"
- Note: "Any mechanical issues with [RULESET] rules?"

**Route Playtests (Computer)**:
- Have one tester per route (Stealth/Combat/Diplomacy) if possible
- Record: "Did I feel locked into this route?" "Could I access other route content?"
- Test accessibility in at least one route per variant (colorblind, audio, motor)
- Ask: "Would you play another route?" (indicates replayability perception)

**Campaign-Wide Issues**:
- When an issue affects multiple sessions/chapters, escalate severity
- If feedback repeats from multiple testers, mark as CONFIRMED and bump severity
- Session/chapter pacing issues almost always require regenerating campaign prep docs

**Immediate Red Flags** (Always CRITICAL):
- Companion loyalty choices not changing loyalty
- Faction rep choices not gating quests in next session
- Route-exclusive content accessible in wrong route
- Any accessibility variant broken in any route
- Playtest can't progress (unwinnable state, dead end, prerequisite not met)



Check for extension hooks after execution:
- Look for `hooks.after_feedback` in `.specify/extensions.yml`. Process as standard hook block. Skip silently if absent.

