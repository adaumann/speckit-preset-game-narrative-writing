---
description: Validate variable state consistency across all branches, map state transitions, detect unreachable states and dead-end variable combos. Combines former speckit.continuity + speckit.statemap.
handoffs:
  - label: Fix Continuity
    agent: speckit.revise
    prompt: Fix nodes with continuity failures or state transition issues.
    send: true
  - label: Check Series
    agent: speckit.series
    prompt: For series carry-over validation specifically.
    send: false
---

# speckit.continuity

Run a full continuity and state analysis across all node files. Validates variable state consistency on all paths, state space reachability, POV drift, NPC state transitions, and series carry-over variables. Now includes state mapping (formerly `speckit.statemap`).

## User Input

```text
$ARGUMENTS
```

Accepted input:
- Nothing — full continuity + state mapping across all nodes
- `--check [types]` — run only specific checks (comma-separated: variables, pov, npc, state, series, timeline, locations, thematic)
- `--act [N]` — scope to a single act
- `--branch [BRANCH_ID]` — map state transitions in one branch only
- `--variable [NAME]` — track state transitions of one variable

- `--strict` — flag any variable change not explicitly set in node; require all nodes to have `polished: [date]` before continuity check
- `--report` — write output to `continuity-report.md`
- `--show-graph` — ASCII state transition graph
- `--show-paths` — display variable state for each branch path
- `--check-convergence` — verify branch merge points have compatible states
- `--reachability-check` — verify all theoretical states are reachable

## Pre-Execution Checks

1. Confirm `draft/` contains node files to analyze
2. Load `variables.md` — authoritative variable registry with types, ranges, initial values
3. Load `plan.md` — branch structure, node sequence, merge points
4. Load `constitution.md` — POV, craft rules, prose profile
5. Load `characters/` — NPC state machines, trust thresholds
6. Load optional docs: series-bible.md, themes.md, relationships.md, timeline.md, locations.md, glossary.md
7. If `--strict`: verify all node files have `polished: [date]` in frontmatter

## Execution Steps

### 1. Variable State Consistency

Simulate all reachable paths from NODE-001 through each ending. For each path, track variable state at each node:

```
PATH [A→C→E]: $trust_mira = 130 at NODE-012 (exceeds max 100)
PATH [B→D]: $flag_met_victor read at NODE-010 but never set on this path
```

Detect: read before set, value outside declared range, counter exceeding max, flag set twice without clear.

### 2. State Space Mapping

From variables.md, define all possible variable states and track per branch:

```
VARIABLE: relationship_marcus (0–100, initial: 50)
Reachable values: 35, 50, 65, 80, 90
Unreachable: 0–34, 36–49, 51–64, 66–79, 81–89, 91–100

BRANCH A state progression:
  NODE-005: freed / 50 / safe
  NODE-010: freed / 65 / safe            [relationship +15]
  NODE-015: freed / 65 / under_siege     [city upgraded]
  NODE-020: freed / 80 / under_siege     [relationship +15]
  NODE-025: escaped / 80 / locked_down
  ENDING:   escaped / 90 / locked_down
```

### 3. POV Drift Check

Load `player_perspective` from constitution.md. Scan all node prose:
- Second-person project: flag any `he/she/they` referring to the player
- Third-person project: flag any `you` addressing the player
- Switching project: verify `$pov` variable is set before each POV-dependent passage

### 4. NPC State Transition Validation

For each NPC: verify trust score changes applied at correct nodes, dialogue register matches trust state, and NPC state (alive/dead/hostile) is consistent:
```
[NPC] speaks in NODE-[N] but is dead on PATH [A–B–N]
```

### 5. Series Carry-Over Validation (if series-bible.md exists)

Verify all carry-over variables declared in variables.md, each ending's snapshot achievable on at least one path, no carry-over variable never set before the ending.

### 6. Detect State Space Problems

#### 🔴 Unreachable State
Variable combo possible by definition but no branch reaches it.
```
relationship_marcus=75: No branch reaches this value despite being in range
```
Fix: Add path or tighten variable range definition.

#### 🟡 Dead-End State
State reached, but next content requires incompatible state.
```
NODE-020 requires relationship > 75, but max reachable is 65 on this path
```
Fix: Add alternate path from this state.

#### 🔵 Untracked Mutation
Variable changes but no node explicitly sets it.
```
relationship_marcus drops 15 points between NODE-015 and NODE-020 with no explicit assignment
```
Fix: Add explicit assignment or dialogue hint.

#### 🟢 Convergence Conflict
Two branches merge with incompatible variable states.
```
Branch A: relationship=80, Branch B: relationship=35 — can't merge at NODE-025
```
Fix: Keep branches separate or add conditional logic.

### 7. Additional Checks (run conditionally)

- **Thematic drift**: Verify registered motifs appear in 3+ nodes; flag acts with no thematic work
- **NPC relationship consistency**: Verify relationship beats match variable values
- **Timeline constraints**: Verify no node violates before/after rules
- **Dialogue continuity**: Verify NPC dialogue uses correct trust register
- **Glossary validation**: Verify term spelling and meaning consistency
- **Location state consistency**: Verify sensory details match across nodes
- **Multi-party dialogue**: Verify NPC pair interactions match relationship arcs

### 8. Generate Report

Output `continuity-report.md` with:
- Per-path variable tracking with violations
- State space overview (reachable vs theoretical)
- Branch state trajectories per node
- State problem list (unreachable, dead-end, untracked, convergence)
- POV drift instances with quotes
- NPC state violations
- Series carry-over issues
- Convergence point analysis
- If `--show-graph`: ASCII state transition graph
- If `--show-paths`: Full state for each branch per node
- If `--check-convergence`: Merge point compatibility

## Important Notes


**Convergence is optional**: Branches don't need to merge. Running parallel is valid design.

**Every variable change should be visible**: "Silent" changes are debugging nightmares. Use explicit assignment comments.

**Dead ends are design failures**: If a reachable state leads to incompatible requirements, fix it or make the state unreachable.
