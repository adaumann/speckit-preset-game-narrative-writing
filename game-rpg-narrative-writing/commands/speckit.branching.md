---
description: Branch structure analyzer — detect exponential branching, validate choice consequences, audit player agency. Combines former speckit.complexity + speckit.consequences + speckit.agency.
handoffs:
  - label: Revise Branches
    agent: speckit.revise
    prompt: Some branches need fixing based on the branching audit findings.
    send: true
  - label: Check Readability
    agent: speckit.readability
    prompt: After analyzing branch structure, check pacing and tone across branches.
    send: false
---

# speckit.branching

Branch structure analyzer — **measure complexity, trace choice consequences, and validate player agency** across all branches. Formerly three separate commands (`speckit.complexity` + `speckit.consequences` + `speckit.agency`).

## Principles

**Sustainable branching** = Each choice is meaningful; maintenance scales linearly.  
**Clear consequences** = Each choice visibly affects story outcome; player can predict results.  
**True agency** = Player choice determines outcome state, not just cosmetic text.

### Problems detected

- Exponential explosion (every node spawns multiple branches; combinations grow uncontrollably)
- Uncontrolled depth (branches diverge without convergence; maintenance impossible)
- Unnecessary parallelism (multiple branches do the same thing)
- Orphaned branches (branch has no convergence back to main story)
- Identical outcomes (different choices lead to same state)
- Illusory/forced choices (all options lead to identical state and ending)
- Delayed consequences (payoff appears 5+ nodes after choice, connection lost)
- Consequence contradicts setup (outcome doesn't match foreshadowing)
- Cosmetic-only choices (affect dialogue text but not game state)
- Unreachable ending states (some endings blocked by branch design)

## User Input

```text
$ARGUMENTS
```

Accepted input:
- Nothing — analyze all branches, consequences, and agency
- Choice ID (e.g., `CH-001`) — trace one choice's consequences
- `--choice-point [NODE_ID]` — analyze all choices at a specific node
- `--branch [BRANCH_ID]` — scope to one branch

- `--strict` — flag any node with >2 branches as risky; fail on cosmetic-only consequences
- `--show-tree` — ASCII tree of branch structure
- `--show-paths` — display all possible endpoints from each choice
- `--show-chains` — display multi-step consequence chains
- `--convergence-map` — show where branches merge
- `--orphaned-only` — show only dead-end branches
- `--estimate-nodes` — calculate total node count needed for all branches
- `--maintenance` — estimate work per branch variant

## Pre-Execution Checks

1. Load `specs/plan.md`: Branch structure, choice points, node sequence
2. Load `specs/variables.md`: All variables affected by choices
3. Load `specs/endings.md`: All registered ending IDs
4. Load all `specs/[FEATURE_DIR]/draft/[ENGINE]/NODE-*.md` files
5. Parse for choice syntax and extract variable mutations per branch
6. Identify divergence points and convergence points

## Execution Steps

### 1. Map Branch Structure

From plan.md, create branch topology:

```
NODE-001 [START]
│
├─ NODE-010 [Help Victor?]
│  ├─ YES → NODE-015 [BRANCH A: Redemption]
│  │  ├─ Violent → NODE-020A [END A1]
│  │  └─ Stealth → NODE-020B [END A2]
│  │
│  └─ NO → NODE-016 [BRANCH B: Betrayal] → NODE-021 → NODE-026 [END B]
│
└─ NODE-011 [Flee?] → NODE-017 [BRANCH C: Escape] → NODE-022 → NODE-027 [END C]

Depth: 4 levels | Breadth at NODE-010: 3 branches | Total endings: 4
```

### 2. Analyze Branch Depth & Breadth

```
Longest path: 6 nodes
Max depth: 6 (moderate, sustainable)
Branching factor: 3 at main choice, 2 at sub-choice (A only)
Total possible paths: 4 combinations
Shared content: 45% ✅ Reasonable
```

### 3. Map Choice Consequences

```
CH-001: "Help or Betray Victor?"
  Option A (Help):
    Immediate: victor_status=escaped, relationship_marcus+=10
    Short-term: city_under_siege=true
    Ending: Ending A "Redemption"
  
  Option B (Betray):
    Immediate: victor_status=captured, relationship_marcus-=15
    Short-term: militia_influence=5
    Ending: Ending B "Tragedy"

Clarity: ✅ CONSEQUENCES VISIBLE (immediate variable changes)
```

### 4. Detect Branching Problems

#### 🔴 Exponential Explosion
3^N where N=4 choices = 81 paths → 405 nodes needed → REDUCED BRANCHING

#### 🔴 Forced/Illusory Choice
`NODE-020`: Both options lead to identical variable state and same ending. Add differentiating consequences or remove the choice.

#### 🟡 Delayed Consequence
`CH-001` Help choice: Victor payoff appears 5 nodes later. Add intermediate hint at NODE-015.

#### 🟠 Orphaned Branch
`CH-001` Flee: NODE-026 is dead-end with no way forward. Add ending node or reconverge.

#### 🟠 Unnecessary Parallelism
3 hide-spot options that all lead to same node with same outcome. Combine into 1 node with flavor variants.

### 5. Validate Agency

Calculate **Agency Ratio** = Branching choices / Total choices:

```
Total choice nodes: 45
Fully branching: 38 (84%) ✅ Strong agency
Forced: 3 (7%) — fix priority 1
Cosmetic: 2 (4%) — acceptable in moderation
```

### 6. Estimate Maintenance Effort

```
E = S + (B × V × C)
S (shared): 10 nodes × 2 hrs = 20 hrs
B (branch-specific): 12 nodes × 2 hrs = 24 hrs
V (variants): 4 × 0.5 hrs = 2 hrs
C (complexity): 3 branches, 6 choice points = 18 test combos
Total: ~46 hrs initial, ~3-5x per shared edit
Risk: MEDIUM
```

### 7. Generate Audit Report

Output `branching-audit.md` with:
- Branch topology map (depth, breadth, total paths)
- Complexity metrics table
- Choice-consequence map (all choices, all options)
- Agency ratio and endpoint diversity
- Problem list (exponential, forced, delayed, orphaned, unnecessary)
- Maintenance effort estimate
- If `--show-tree`: ASCII branch structure
- If `--show-paths`: Full outcome states per choice
- If `--show-chains`: Multi-step consequence chains
- If `--convergence-map`: Merge point compatibility analysis

## Important Notes

**Branching isn't inherently bad**: Games like Disco Elysium have hundreds of nodes. The issue is whether you can maintain it.

**Convergence is your friend**: Branches that reconverge reduce exponential growth.

**Agency ≠ different endings**: A choice has agency if it changes state, even if branches reconverge.

**Cosmetic choices are OK** in moderation (<10%). Not every choice needs mechanical weight.

**Foreshadow delayed consequences**: If payoff appears 5+ nodes after choice, have an NPC mention it.

**Linear with side branches**: Consider linear main story with optional side quests as a sustainable pattern.
