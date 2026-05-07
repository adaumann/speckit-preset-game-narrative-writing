---
description: Detect and resolve ambiguity and open design questions in the narrative design doc or game bible � branch logic gaps, mechanic coherence, variable states, and unresolved OQ-NNN items.
handoffs:
  - label: Rewrite Narrative Design Doc
    agent: speckit.specify
    prompt: Major concept changes emerged during clarification. Please rewrite the narrative design doc.
  - label: Generate Game Bible
    agent: speckit.constitution
    prompt: All open questions are resolved. Generate the game bible.
---

# speckit.clarify

Detect and reduce ambiguity or missing decision points in the narrative design document or game bible, then write resolved answers directly back into the relevant files.

## User Input

```text
$ARGUMENTS
```

You **MUST** consider the user input before proceeding (if not empty). Accepted input:
- A specific open question reference (e.g. "resolve OQ-003")
- A topic area (e.g. "clarify branch structure" or "clarify engine target")
- No input � runs a full structured ambiguity scan across all scoped files

Optional flags:
- `--scope narrative` � scan `specs/spec.md` only
- `--scope constitution` � scan `.specify/memory/constitution.md` only
- `--all` � resolve all open questions in sequence (interactive mode)

## Pre-Execution Checks

**Check for extension hooks (before clarification)**:
- Check if `.specify/extensions.yml` exists in the project root.
- If it exists, read it and look for entries under the `hooks.before_clarify` key.
- Process as standard hook block (Optional/Mandatory). Skip silently if absent.

**RPG context detection**:
- Read `.specify/memory/constitution.md` and extract `[PLATFORM]` (Tabletop / Computer Game) and `[RULESET]` (D&D 5e / Pathfinder / Shadowrun / Generic).
- Store these for use in the ambiguity scan and clarification prompts below.

Then:
1. Locate `specs/spec.md` – if absent, suggest running `speckit.specify` first.
2. Count all `[NEEDS CLARIFICATION]` and `OQ-NNN` markers in scoped files.
3. Report: "Found [N] open questions. Proceeding to resolution. (Platform: [PLATFORM], Ruleset: [RULESET])"

## Outline

**Goal**: Detect and reduce ambiguity or missing decision points in the active spec files, then write the answers directly back into the relevant file.

**Note**: This clarification workflow should run BEFORE `speckit.plan`. If the user explicitly skips it, warn that downstream rework risk increases � then proceed.

### Execution Steps

1. **Setup**: Run `{SCRIPT}` from repo root if available and parse JSON for spec file paths.

2. **Load spec files**: Read `spec.md` (and `constitution.md` if in scope). Identify all `[NEEDS CLARIFICATION]` and `OQ-NNN` markers.

3. **Run a structured ambiguity scan** across these domains � look for gaps or contradictions, not just explicit markers:

   | Domain | Questions to ask |
   |---|---|
   | **Branch logic** | Are all branch conditions fully specified? Do any branches lead to dead ends or unreachable nodes? Are merge points and convergence conditions documented? |
   | **Player agency** | Is the player's decision scope clearly bounded? Do choices have distinct, meaningful consequences? Are illusion-of-choice moments deliberately marked? |
   | **Variable states** | Are all tracked variables (flags, counters, relationship scores) defined with their valid ranges? Are there state combinations that produce contradictions or unreachable content? |
   | **Character consistency** | Do NPC motivation anchors hold across all branches? Are self-deception patterns or behavioral blind spots defined per major NPC? Could an NPC behave differently in two branches in ways that break characterisation? |
   | **World rules** | Are world-building rules implied by the narrative but not yet documented as WR-NNN? Are there location or faction details that could contradict each other across scenes? |
   | **Mechanic coherence** | Are narrative mechanics aligned with the gameplay systems described in the spec? Are pacing requirements compatible with engine or platform constraints? |
   | **Endings & arcs** | Is each ending's prerequisite path clearly traceable from the branch map? Are thematic arcs resolved consistently across all major ending variants? |
   | **Continuity** | Are there timeline gaps or scene-order contradictions? Do introduced story elements (Chekhov items) have documented pay-off scenes? |
   | **Export / platform** | Are there engine, platform, or toolchain constraints that affect narrative structure but aren't yet captured in the spec? |
   | **RPG-specific: Factions** (Tabletop only) | Are all faction rules clearly documented? (triggering reputation changes, minimum rep thresholds for actions, ending gates per faction, NPC faction affiliations). Can a party reach contradictory rep states? Do party choices consistently affect rep? |
   | **RPG-specific: Companions** (Tabletop only) | Is each companion's recruitment node unambiguous? Are approval thresholds defined per companion? Are companion conditional outcomes and ending fates documented? Can companion arcs progress independently, or do they require party actions? |
   | **RPG-specific: Encounters** (Tabletop only) | Is the session-by-session encounter structure clear? (count, CR targets, enemy composition, treasure type). Do encounter choices meaningfully affect later sessions? Is encounter difficulty calibrated to the party's expected level? |
   | **RPG-specific: Party agency** (Tabletop only) | Is party decision scope clearly bounded? (skills that replace encounters, dialogue that bypasses combat, skill check DCs per check). Are ruling-ambiguities resolved per check type (Charisma checks that unlock social branches, Stealth checks that bypass encounters)? |
   | **RPG-specific: Character progression** (Computer Game only) | Is protagonist/party level progression clear? (XP sources, level-up structure, ability unlocks per level). Do difficulty settings scale opponent stats consistently? Are skill check difficulty levels consistent across all branches? |
   | **RPG-specific: Playstyle distribution** (Computer Game only) | Are % estimates for combat vs dialogue vs exploration vs puzzles accurate? Do all playstyles reach all major story beats, or do some styles lock out content? Are there skill checks that replace entire encounter types? |
   | **RPG-specific: Ruleset mechanics** (D&D 5e only) | Are encounter CRs calibrated to party level? Are spell/ability uses limited per encounter or per rest? Are skill check DCs set to reasonable probabilities (DC 10 easy, 15 moderate, 20 hard)? Is magic item treasure distribution aligned with D&D 5e rarity tables? |

4. **Select ≤5 questions** – the highest-value targeted clarifications. Prioritize:
   - Questions that block planning or branch-map work (structural ambiguity)
   - Variable state contradictions (breaks implementation)
   - Character consistency gaps across branches
   - Missing world rules implied by existing content
   - Endings with untraceable prerequisite paths
   - **For Tabletop RPGs**: Faction reputation contradictions, companion approval gate contradictions, encounter CR calibration gaps
   - **For Computer Game RPGs**: Difficulty scaling inconsistencies, playstyle-gated content that breaks paths, character progression XP source contradictions
   - **For D&D 5e**: Spell/ability use limits per encounter, skill check DC reasonableness, magic item treasure distribution alignment

   Do NOT ask about things resolvable from context. Do NOT ask generic questions.

5. **Present questions to the user** � one at a time, or as a numbered list if the user prefers batch mode. Wait for answers.

6. **Write answers back into the relevant file**:
   - Replace `[NEEDS CLARIFICATION: ...]` markers with clarified content
   - Remove resolved `OQ-NNN` markers and record the resolution inline
   - If a resolution creates new constraints, add a world rule (`WR-NNN`) entry
   - If a new branch condition is implied, add a `[NEEDS BRANCH SPEC]` note to the plan section
   - **For Tabletop RPGs**: If resolving faction, companion, or encounter clarifications:
     - Update factions table with reputation ranges and ending gates per faction
     - Update companions table with approval thresholds and recruitment conditions
     - Update sessions structure with CR targets and encounter count per session
   - **For Computer Game RPGs**: If resolving character progression or playstyle clarifications:
     - Update character progression table with XP sources and ability unlock levels
     - Update playstyle % distribution and note any content locked to specific playstyles
     - Update skill check result spectrum (fail / success / critical success outcomes)
   - **For D&D 5e**: If resolving ruleset-specific clarifications:
     - Add spell/ability use limits (per encounter / per short rest / per long rest)
     - Add skill check DC table with examples per ability
     - Add magic item treasure distribution by session/chapter
   - Group remaining unresolved items by category: design, world-building, mechanic, export, research, RPG-mechanics

7. **Report**: "Resolved [N] of [N] questions. [N] remain."
   - If all resolved: "All open questions resolved. Run `speckit.constitution` to generate the game bible."

## RPG-Specific Clarification Examples

Use these prompts when the ambiguity scan detects gaps in RPG-specific domains:

### For Tabletop RPGs (Platform = Tabletop)

**Faction Clarifications:**
- "For the [Faction Name] faction, what are the minimum reputation thresholds for: (a) recruiting members, (b) unlocking quests, (c) gaining access to areas, (d) reaching favorable/betrayal endings?"
- "If a party gains reputation with Faction A at the expense of Faction B, at what rep difference do they become hostile? (e.g., if Faction A reaches +50 and Faction B reaches -40, does combat trigger automatically?)"
- "Which endings are gated by faction reputation? (e.g., 'Must reach +100 with Guard faction to reach Lawful ending')"

**Companion Clarifications:**
- "For [Companion Name], what is the approval range? (e.g., -100 to +100) What are the thresholds for: (a) recruitment, (b) trust scene, (c) romance/deep bond, (d) betrayal?"
- "Can companions leave the party if approval drops below a threshold? If so, is the companion permanently lost or can they be re-recruited?"
- "Do companion arcs continue if the player ignores them, or are they player-driven only?"

**Encounter Clarifications:**
- "Sessions 1-3: What are the expected party levels and CR targets per session? (e.g., 'Level 5 party, CR 1-2 encounters, 2-3 encounters per session')"
- "If the party uses a skill check (e.g., Stealth check DC 15) to bypass an encounter, what do they miss? (XP? Treasure? Story beats?) How does this affect future sessions?"
- "Are there 'gavage encounters' that reset party resources (short rests, healing, etc.) between major combat encounters?"

**Party Agency Clarifications:**
- "Which encounters can be bypassed via skill checks? For each: What is the DC? Who can roll? What happens on failure vs success?"
- "Are there encounters where non-combat solutions exist? (e.g., Intimidation to scatter enemies, Persuasion to ally with enemy) What do these routes gain/lose compared to combat?"

### For Computer Game RPGs (Platform = Computer Game)

**Character Progression Clarifications:**
- "What are the XP sources? (combat kills, quest completion, exploration, skill checks?) How much XP does each source provide?"
- "At what levels do key abilities unlock? (e.g., 'Fireball spell unlocks at Level 5; second party member joins at Level 7')"
- "Is there a level cap? If so, when do players typically reach it? (by end of Chapter 2, final boss, etc.)"

**Playstyle Clarifications:**
- "Does a player who focuses on dialogue reach all major story beats? Or does dialogue-heavy playstyle lock out combat encounters entirely?"
- "For exploration-heavy players: Are there areas/secrets that only exploration-focused players discover? Do these areas contain story-critical information?"
- "Is there a skill check that can replace an entire combat encounter? If so, what is the DC and what do players miss if they skip it?"

**Difficulty Clarifications:**
- "On Hard difficulty, how do enemy stats scale? (e.g., 'Enemy AC +2, HP +25%, damage +2')"
- "Are skill check DCs difficulty-independent, or do they scale? (e.g., 'On Hard, all DCs +2')"
- "Do story encounters scale with difficulty, or are they fixed?"

### For D&D 5e (Ruleset = D&D 5e)

**Encounter Design Clarifications:**
- "For [Encounter Name], what is the intended CR? What are the constituent enemy types and counts? (e.g., 'CR 4: 1 Ogre + 3 Thugs')"
- "What treasure does this encounter drop? (Coin, magic items, consumables?) Is it aligned with D&D 5e rarity guidance for this level?"

**Spell/Ability Clarifications:**
- "Are spell slots expended per encounter or per rest? (RAW: long rest, but confirm if house rules differ)"
- "Are there spells that trivialize encounters? (e.g., Fly over difficult terrain, Invisibility to bypass combat?) Is this intentional or an oversight?"

**Skill Check Clarifications:**
- "For this skill check, what is the intended DC and why? (e.g., 'Perception DC 12 (moderate) because this clue is hidden but not invisible')"
- "Is this skill check binary (pass/fail), or are there degrees of success? (fail, success, critical success)"
- "What is the probability of success? (DC 10 on d20 ≈ 55% for untrained; confirm if this matches intent)"

