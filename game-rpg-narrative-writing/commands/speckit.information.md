---
description: Information flow analyzer — map NPC dialogue trees, player knowledge vs NPC knowledge gaps, secrets and hidden content. Combines former speckit.dialogue + speckit.asymmetry + speckit.secrets.
handoffs:
  - label: Revise Information
    agent: speckit.revise
    prompt: Some information flows need fixing based on the information audit.
    send: true
  - label: Check Narrative Arc
    agent: speckit.narrative-arc
    prompt: After information analysis, verify character arcs and subplot resolution.
    send: false
---

# speckit.information

Information flow analyzer — map **NPC dialogue trees, information asymmetry between player and NPCs, and secret/hidden content**. Formerly three separate commands (`speckit.dialogue` + `speckit.asymmetry` + `speckit.secrets`).

## Principles

**Healthy asymmetry** = Player and NPCs have different (but plausible) information → creates tension, enables deception, gives advantage.  
**Good secrets** = Discoverable for attentive players; optional; rewarding; properly documented.  
**Dialogue consistency** = NPC speech matches their trust level, state, and relationship arc.

### Problems detected

- Dialogue trust-gap (NPC has register defined but no lines written for that trust level)
- Unreachable dialogue (condition can never be satisfied by any branch path)
- Unreachable secret (unlock condition impossible in practice)
- Impossible-to-discover secret (no hint anywhere)
- Contradictory unlock (two conditions that can't both be true)
- Player knows too much (information should be NPC-exclusive)
- Player knows too little (can't make informed choice)
- NPC knows future information (reacts before reveal)
- Secret undocumented (exists in code but not in any FAQ/guide)

## User Input

```text
$ARGUMENTS
```

Accepted input:
- Nothing — full analysis across all NPCs and secrets
- Character name (e.g., `Marcus`) — analyze one character's dialogue + knowledge
- `--faction [NAME]` — analyze information known to entire faction
- `--node [NODE-ID]` — extract information from one node only
- `--secret [SECRET_ID]` — analyze one secret only

- `--strict` — flag all asymmetries for review; fail on undocumented secrets
- `--show-gaps` — visualize information gaps with ASCII charts
- `--show-unlock-paths` — display all ways to unlock each secret
- `--check-realism` — flag NPC knowledge that's narratively implausible
- `--unreachable` — focus report on unreachable dialogue lines and secrets
- `--craft` — add craft audit for dialogue (on-the-nose, said-bookisms, etc.)
- `--difficulty-map` — categorize secrets by unlock difficulty
- `--mermaid` — output dialogue tree as Mermaid diagram

## Pre-Execution Checks

1. Load `specs/characters.md`: NPC voice specs, trust tables, register definitions, state machines
2. Load `specs/plan.md`: Node sequence, which NPCs appear where
4. Load `specs/variables.md`: Variables that track information and unlock secrets
5. Load `specs/secrets-template.md` or extract from spec.md: Secret registry
6. Load `specs/constitution.md`: Prose profile, POV, tense

## Execution Steps

### 1. Extract Dialogue Inventory

Scan every node. For each dialogue line:

```
Node: NODE-010 | Speaker: Marcus
Line: "What do you want?"
Condition: trust >= 26 (cautious or higher)
Trust level: cautious (26–49)
```

Group by character, sort by node order within each trust level.

### 2. Map Trust & State Coverage

```
CHARACTER: Marcus
| Trust Level | Lines | Condition Correct | Gap |
|-------------|-------|-------------------|-----|
| hostile     | 3     | ✅                | —   |
| cautious    | 5     | ✅                | —   |
| neutral     | 0     | —                 | ⚠️  |
| friendly    | 4     | ✅                | —   |
| ally        | 2     | ✅                | —   |

| State | Lines | Reachable? |
|-------|-------|------------|
| alive | 14    | ✅         |
| dead  | 0     | ⚠️ NO LINES |
```

### 3. Track Information Per Character

```
INFO: "Victor is militia spy"
Who knows when:
  Player: NODE-025 (revelation scene)
  Marcus: NODE-005 (detective work)
  Victor: Always (his identity)
  Sera: NODE-030 (Marcus tells her)

Timeline:
  Before NODE-025: Player unaware ✅ HEALTHY TENSION
  After NODE-025: All know ✅ INFORMATION REVEALED
```

### 4. Analyze Secret Registry

```
HID-001 "Victor's Letter":
  Unlock: Ending A + relationship_marcus > 75 + secret passage
  Discoverability: MODERATE (hint: Marcus mentions safehouse)
  Reachable? ❌ — secret passage has no in-game hint or mechanic
  Fix: Add passage hint in NODE-030 prose
```

### 5. Detect Problems

#### 🔴 Unreachable Dialogue
`Marcus` ally line condition `trust >= 90`, but no path raises trust above 75 before NODE-009. Fix condition or add trust path.

#### 🔴 Secret Unreachable
`HID-001`: Secret passage has no in-game hint or mechanic. Add discovery hint.

#### 🔴 Player Knows Too Much (Unrealistic)
Player hears "Victor is spy" in tavern rumor before detective discovers it. Either add source or change timing.

#### 🟡 Player Knows Too Little (Unfair)
Choice at NODE-015 requires knowing Sera's location, but player has no way to learn it. Add info-gathering scene before choice.

#### 🟡 NPC Knows Future
Victor says "I know what you're planning" before player has revealed their plan. Either move line after reveal or add explanation.

#### 🟡 Contradictory Secret Unlock
`HID-002` requires `relationship > 50` but betrayal path leads to `25`. Change condition to `relationship < 50`.

#### 🟠 Secret Required for Main Content
"True Ending" requires 5 hidden scenes + 3 collectibles, making players feel Ending A is incomplete. Mark as optional or reduce requirements.

### 6. Generate Audit Report

Output `information-audit.md` with:
- Dialogue coverage tables per character (trust/state gaps)
- Information gap chart (who knows what, when)
- Secret inventory (achievements, hidden content, easter eggs)
- Problem list (unreachable lines/secrets, contradictory conditions, unrealistic knowledge)
- If `--show-gaps`: Timeline visualization of information reveals
- If `--show-unlock-paths`: Unlock path trees per secret
- If `--difficulty-map`: Difficulty tier breakdown
- If `--mermaid`: Dialogue tree diagrams

## Important Notes

**Asymmetry is not bad**: Information gaps create tension and player agency. The goal is intentional, plausible gaps.

**Balance discoverability**: Mix of obvious and obscure secrets keeps players engaged. All-easy is boring; all-impossible is frustrating.

**NPC behavior must match knowledge**: If NPC doesn't know something, their dialogue shouldn't reveal it.

**Document everything**: Even hidden secrets should be documented in FAQ/guide for players who want to find them.

**Factions have collective knowledge**: When NPCs communicate, faction knowledge spreads. Track this.
