---
description: Narrative arc auditor — review character development, subplot resolution, and ending quality across all branches. Combines former speckit.character + speckit.subplots + speckit.endings.
handoffs:
  - label: Revise Arcs
    agent: speckit.revise
    prompt: Some narrative arcs need fixing based on the arc audit findings.
    send: true
  - label: Check Readability
    agent: speckit.readability
    prompt: After arc analysis, check pacing and tone across branches.
    send: false
---

# speckit.narrative-arc

Narrative arc auditor — review **character development, subplot resolution, and ending quality** across all branches. Formerly three separate commands (`speckit.character` + `speckit.subplots` + `speckit.endings`).

## Principles

**Show, don't tell** — Reveal character through action, choice, and dialogue. Never state a trait directly if you can dramatise it.  
**Subplot integrity** = Every subplot is introduced, developed, and resolved (not abandoned) in every branch that reaches it.  
**Satisfying ending** = Resolves the central dramatic question, shows character change, clarifies stakeholder fates, and provides thematic closure.

### Problems detected

- Flat characterization (traits stated, never shown)
- Unearned character growth (arc change without sufficient build-up)
- Indistinct characters (multiple characters sound/act identically)
- Dangling subplots (started but never mentioned again)
- Subplot resolved prematurely (anticlimactic)
- Subplot inconsistent across branches
- Ending doesn't resolve central dramatic question
- Ending is ambiguous about what happened
- Ending feels manipulative or unearned
- Character outcomes unclear at end

## User Input

```text
$ARGUMENTS
```

Accepted input:
- Nothing — full audit across all characters, subplots, and endings
- Character name (e.g., `Marcus`) — audit one character's arc
- Subplot ID (e.g., `SP-001`) — trace one subplot's resolution
- `--ending [ENDING_ID]` — analyze one ending only
- `--branch [BRANCH_ID]` — scope to one branch
- `--act [N]` — scope to a single act

- `--strict` — require every character to have an arc in every branch they appear
- `--show-arcs` — display character arc visualization
- `--subplot-only` — focus only on subplot resolution
- `--endings-only` — focus only on ending quality
- `--characters-only` — focus only on character development

## Pre-Execution Checks

1. Load `specs/plan.md`: Branch structure, node sequence, act boundaries
2. Load `specs/characters.md` (or equivalent): NPC profiles, traits, arcs
3. Load `specs/endings.md`: All registered endings with requirements
4. Load `specs/constitution.md`: Central dramatic question, theme
5. Load all `specs/[FEATURE_DIR]/draft/[ENGINE]/NODE-*.md` files
6. Identify subplot markers from node content and plan.md
7. Load optional docs: relationships.md, themes.md

## Execution Steps

### 1. Audit Character Development

Review each named character's arc across nodes:

```
MARCUS — Character Arc Audit

Traits defined: Honest, protective, suspicious
Shown through action?
  ✅ NODE-005: Steps between player and threat (protective, shown)
  ✅ NODE-010: Refuses bribe (honest, shown through choice)
  ❌ NODE-015: "He was suspicious by nature." (told, not shown)
  
Growth: Suspicious → Trusting (earned?)
  NODE-005 → NODE-010: Player proves trustworthy (+tension)
  NODE-015: Marcus shares secret (trust breakthrough)
  Growth: ✅ EARNED (preceded by trust-building scenes)

Distinctiveness check:
  Voice: Short sentences, military jargon ✅ Distinct from Victor (poetic)
  Motivations: Protect family ✅ Not same as Sera (seek truth)
  Flaws: Over-protective, jumps to conclusions ✅ Human, not perfect
```

#### 🟡 Flat Character
Traits listed but never dramatised. Replace telling with showing: action, choice, or dialogue.

#### 🟡 Unearned Growth
Marcus goes from hostile to ally in one scene with no intervening trust-building. Add trust-building node(s).

#### 🟡 Indistinct Characters
Marcus and Victor both speak in short, gruff sentences with military jargon. Give each a distinct voice and word choice pattern.

### 2. Track Subplot Resolution

Map each subplot's lifecycle:

```
SP-001: "Sera's kidnapping" (Subplot)
  Introduced: NODE-005 (Marcus mentions missing person)
  Developed: NODE-010 (clues found), NODE-015 (suspect identified)
  Resolved: NODE-025 (Sera rescued ✅) or END-B (Sera unresolved ❌)

Branch A: Introduced → Developed → Resolved ✅
Branch B: Introduced → Developed → ABANDONED ❌
Branch C: Never introduced ✅ (branch avoids this subplot)

Fix: Add resolution for Branch B (even a brief mention that Sera was found off-screen)
```

#### 🔴 Dangling Subplot
Subplot introduced but never resolved in a branch. Add resolution node or off-screen closure mention.

#### 🟡 Premature Resolution
Subplot resolved in 1 node after introduction with no development. Add 1–2 development nodes.

### 3. Evaluate Ending Quality

Score each ending against the rubric:

```
ENDING A: "Redemption" (Victor escaped, relationship > 75)

Resolves central question?
  CDQ: "Can trust survive betrayal?"
  Ending A: Trust flourished → ✅ YES
  
Character change?
  Player: Learned to trust (arc complete) ✅
  
Stakeholder fates clear?
  Victor: Escaped safely, starting new life ✅
  Marcus: Ally, relationship strengthened ✅
  City: Stabilized after siege ✅
  
Thematic resonance?
  Theme: "Trust survives conflict"
  Ending: Trust prevailed → ✅ YES
  
Emotional landing?
  Tone: Warm resolution after earned struggle ✅ Not manipulative

Status: ✅ PASS (all criteria met)
```

#### 🔴 Ending Doesn't Resolve CDQ
Ending B resolves the siege but never addresses whether the player can trust again. Add a line addressing the central dramatic question.

#### 🟡 Stakeholder Fates Unclear
Ending C ends with "you escape" but doesn't mention what happened to Sera, Marcus, or the city. Add epilogue sentences.

### 4. Generate Audit Report

Output `narrative-arc-audit.md` with:
- Character development table (traits shown vs told, growth earned, distinctiveness)
- Subplot lifecycle table (introduced → developed → resolved per branch)
- Ending quality scores per rubric criteria
- Problem list (flat characters, dangling subplots, unresolved endings)
- If `--show-arcs`: Character arc visualization per branch
- Recommendations prioritized by impact

## Important Notes

**Every character needs an arc**: Even minor NPCs should have at least a mini-arc (1 trait change or revelation) if they appear in 3+ nodes.

**Subplots can resolve off-screen**: If a subplot isn't central to a branch, mention passing resolution in narration.

**Endings need stakeholder closure**: Players invested in the world want to know what happened to key characters, not just the protagonist.

**Thematic coherence**: All endings should reinforce or challenge the central theme, not ignore it.

**Not all branches need all subplots**: It's valid for a branch to avoid certain subplots entirely (player chose differently). But introduced subplots must resolve.
