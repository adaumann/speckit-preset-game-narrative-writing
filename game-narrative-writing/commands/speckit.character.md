---
description: Character development auditor — review character traits, arcs, consistency, and distinctiveness across nodes. Detects flat characters, unearned growth, and adjective-stuffed description.
handoffs:
  - label: Check Dialogue
    agent: speckit.dialogue
    prompt: After reviewing characters, audit how they express themselves through dialogue.
    send: true
  - label: Check Tone
    agent: speckit.tone
    prompt: Validate emotional beats align with character states.
    send: true
  - label: Revise Characters
    agent: speckit.revise
    prompt: Some characters need deeper development. Please revise prose to reveal character through action and dialogue rather than description.
    send: true
---

# speckit.character

Character development auditor — review **traits, arcs, consistency, and distinctiveness** for all named characters. Detects flat characterisation, unearned growth, adjective stuffing, and characters who sound identical.

## Character Craft Principles

**Show, don't tell** — Reveal character through *action, choice, and dialogue*. Never state a trait directly if you can dramatise it.

| ❌ Telling | ✅ Showing |
|---|---|
| "He was greedy." | "He reached for the bread before anyone had sat down." |
| "She was brave." | "She stepped forward when everyone else stepped back." |
| "He was dishonest." | "He answered a different question than the one she asked." |

**Arc vs. static** — Not every character needs an arc. Antagonists, mentors, and comic foils may be static by design. But the *protagonist* must change — or deliberately fail to change for thematic reasons.

**Distinctiveness** — Two characters should never be interchangeable. Each must have at least:
- A distinct *voice* (word choice, sentence rhythm, what they avoid saying)
- A distinct *want* (conscious goal)
- A distinct *need* (what they actually lack, often hidden from themselves)
- A distinct *flaw* that creates friction

**Adjective stuffing** — A list of adjectives is not characterisation. Replace with a moment that demonstrates the trait.

## User Input

```text
$ARGUMENTS
```

Accepted input:
- Nothing — audit all named characters across all nodes
- Character name (e.g., `Mira`) — audit one character only
- `--arc` — focus on character arc and growth only
- `--voice` — focus on dialogue distinctiveness only
- `--first-appearance` — review how each character is introduced

Optional flags:
- `--strict` — flag any direct trait statement (not just obvious adjective stuffing)
- `--show-wants` — display want/need/flaw table for each character

## Pre-Execution Checks

1. Load `specs/constitution.md`: Character list, POV, tone
2. Load `specs/characters.md` if present: Stated traits, arcs, relationships
3. Load all `draft/[ENGINE]/NODE-*.md` files: Extract all character appearances
4. Load `specs/plan.md`: Which nodes each character appears in

## Execution Steps

### 1. **Build Character Appearance Map**

For each named character, list:
- Every node they appear in
- Their role in that node (POV, speaking, mentioned, absent)
- Any stated trait, emotional state, or descriptive phrase used

### 2. **Trait Analysis**

For each character, identify:
- All **stated traits** (adjective stuffing candidates): flag for revision
- All **demonstrated traits** (actions, choices, dialogue): confirm these exist
- **Trait consistency**: Does the character behave consistently with established traits across nodes? Flag contradictions unless explained by arc

### 3. **Arc Analysis**

For the protagonist (or any character flagged as having an arc in `constitution.md`):
- Identify the **wound or need** at story start
- Trace **pressure points** where the arc is tested
- Confirm a **transformation moment** exists (or that absence is intentional)
- Flag if growth is *told* rather than *shown*

### 4. **Distinctiveness Check**

Compare named characters pairwise:
- Do any two characters use identical speech patterns? → Flag for voice differentiation
- Do any two characters want the same thing for the same reason? → Flag for want differentiation
- Are any characters purely functional (only exist to deliver information)? → Flag as candidates for elevation or merging

### 5. **First Appearance Check** (if `--first-appearance` or general audit)

For each character's first node:
- Is their introduction a *doing* or a *describing*? Prefer doing
- Does the reader immediately understand something specific and memorable about them?
- Is their core want or flaw legible within their first scene?

### 6. **Produce Character Sheet Summary**

For each character, output a summary table:

```
CHARACTER: [Name]
Nodes: [list]
Want: [conscious goal]
Need: [unconscious lack]
Flaw: [what creates friction]
Arc: [static / growth / fall / ambiguous]
Voice markers: [distinct speech patterns]
Issues found: [list or "none"]
```

### 7. **Flag Issues**

For each issue found, output:

```
⚠️  [NODE-ID] — [Character Name]
Issue: [description]
Example: "[offending line or passage]"
Suggestion: [concrete revision direction]
```

Categories of issues to flag:
- `ADJECTIVE-STUFFING` — direct trait statement with no demonstration
- `INCONSISTENCY` — behaviour contradicts established trait (unexplained)
- `UNEARNED-ARC` — character changes without sufficient pressure or scene work
- `VOICE-BLEED` — two characters sound identical in dialogue
- `FUNCTIONAL-ONLY` — character exists solely to deliver plot information
- `WEAK-INTRO` — first appearance describes rather than dramatises

## Output Format

```
# Character Audit — [Game Title]

## Character Summary Table
[per character: want / need / flaw / arc / issues]

## Issues Found
[flagged issues with node references]

## Recommendations
[prioritised list of revision actions]
```

If no issues are found: confirm each character is well-drawn and note any standout strengths.
