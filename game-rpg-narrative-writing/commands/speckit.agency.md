---
description: Validate player agency — verify choices have consequences and aren't illusory. Detects dead choices, forced branches, and choice-outcome impact via variable state tracking. For RPG campaigns (tabletop D&D/Pathfinder/Shadowrun and computer game), validates companion loyalty choices, faction reputation decisions, and playstyle route branches with accessibility consistency.
handoffs:
  - label: Revise Branches
    agent: speckit.revise
    prompt: Some choices are forced or illusory. Please revise to add real consequences.
    send: true
  - label: Check Endings
    agent: speckit.endings
    prompt: After validating choice agency, check if all endings are satisfying.
    send: true
---

# speckit.agency

Validate player agency — ensure player choices **meaningfully affect outcomes** rather than being illusory or forced.

**RPG Campaign Support**: Adapts agency validation for tabletop (companion loyalty consequences, faction reputation changes, campaign-level decision impact) and computer game (playstyle route commitment, accessibility variant consistency, route-exclusive consequences).

## Agency Principle

**True agency** = Player choice determines outcome state. **False agency** = Choice appears to matter but leads to same endpoint regardless of selection.

This command validates:
- ✅ Each choice branches to meaningfully different outcomes
- ✅ Chosen branch leads to different ending(s) than unchosen branches
- ✅ Variable state diverges based on choice selection
- ✅ No "forced branches" (all paths reconverge to identical state before reaching ending)
- ✅ Choice consequences are **meaningful** (not cosmetic text differences only)

**For RPG Campaigns**:
- ✅ Companion loyalty choices track relationship state (affects party composition, NPC availability)
- ✅ Faction reputation decisions cascade to quest availability and NPC reactions
- ✅ Tabletop campaign choices persist across sessions and modules (not reconverging within same session)
- ✅ Computer playstyle route commitment is enforced (Stealth player can't suddenly switch to Combat)
- ✅ Accessibility variants are consistent across all routes (colorblind variant available in all playstyles)

**NOT validated here** (use other tools):
- ❌ Ending quality (use `speckit.endings`)
- ❌ Emotional impact of choices (use `speckit.tone`)
- ❌ Whether consequences are telegraphed (use `speckit.foreshadow`)
- ❌ Companion quest resolution (use `speckit.subplots`)
- ❌ Campaign continuity across sessions (use `speckit.series`)

## User Input

```text
$ARGUMENTS
```

Accepted input:
- Nothing — audit entire game for all choice nodes
- Node ID (e.g., `NODE-005`) — audit a single node's choices
- `--branch [BRANCH_ID]` — audit all choices in one branch

Optional flags:
- `--strict` — fail on cosmetic-only consequences (not just endpoint differences)
- `--show-paths` — display all possible endpoints from each choice
- `--variable-only` — focus only on variable state divergence (skip dialogue differences)

## Pre-Execution Checks

**Auto-detect platform and ruleset** (for RPG campaigns):
- Load `constitution.md`
- Extract `[PLATFORM]` (tabletop/computer) and `[RULESET]` (D&D 5e/Pathfinder 2e/Shadowrun 6e)
- Set SESSION object: `{platform: [PLATFORM], ruleset: [RULESET], mechanics: [MECHANICS]}` for downstream checks
- If no platform found: treat as generic interactive fiction (no RPG-specific logic)

**Standard Pre-Execution**:
1. Confirm `specs/plan.md` exists with node graph and branch structure
2. Confirm `specs/variables.md` exists with all declared variables
3. Confirm `specs/endings.md` exists with all registered endings
4. Load all `draft/[ENGINE]/NODE-*.md` files to analyze actual choice text and variable reads/sets
5. If RPG: Load `mechanics-[RULESET].md`, `companions.md`, `factions.md` (if applicable)
6. If `--show-paths` flag: load `specs/relationships.md` if present (for NPC state impact)

## Execution Steps

### 1. **Load Spec**
   - Read `plan.md`: node graph, branch structure, ending nodes
   - Read `variables.md`: all variables with type and scope
   - Read `endings.md`: all registered ending IDs
   - Read all node draft files: extract choice syntax and variable operations

### 2. **Map Choice → Outcome**

For each **choice node** in the game:
   - **Parse choice targets**: Where does each option branch?
   - **Trace variable impact**: What variables are read/set in each branch?
   - **Follow to endpoints**: Do both branches lead to the same ending(s)?

**Generic Example**:
```
NODE-005 (choice node):
  Choice A → NODE-007
    Variables set: trust(marcus) = 1, player_suspicion = true
    
  Choice B → NODE-008
    Variables set: trust(marcus) = -1, player_awareness = true
    
  Both → NODE-020 (final node)
```

**RPG Example - Tabletop Companion Loyalty**:
```
SESSION-4, NODE-010 (Companion Loyalty Choice):
  Choice A: "Theron, I believe in your honor"
    → NODE-012: Set loyalty(theron) += 1, trust_threshold_high = true
    → SESSION-5: Theron provides special dialogue option ("I won't let you down")
    → Can unlock: "Theron's Redemption" companion quest (speckit.subplots)
    
  Choice B: "Theron, I doubt your claim"
    → NODE-013: Set loyalty(theron) -= 1, trust_threshold_low = true
    → SESSION-5: Theron distant, offers no special dialogue
    → Session 8: Theron may leave party if loyalty < 0 (speckit.series campaign-guide.md impact)
```

**RPG Example - Computer Playstyle Route Commitment**:
```
CHAPTER-2, NODE-008 (Route Commitment):
  Choice A: "Infiltrate the tower unseen" (Stealth)
    → NODE-010: Set $player_playstyle = "stealth"
    → All Chapter 3-4 nodes: Only Stealth-variant nodes are accessible
    → Cannot retroactively pick: "Use brute force" (Combat) or "Negotiate entry" (Diplomacy)
    → NODE-020+: Stealth-only achievements, Stealth-specific ending branching
    
  Choice B: "Force your way in" (Combat)
    → NODE-011: Set $player_playstyle = "combat"
    → All Chapter 3-4 nodes: Only Combat-variant nodes accessible
    → Different enemy encounters, different resource management
    → NODE-020+: Combat-only achievements, Combat-specific ending branching
```

### 3. **Detect Agency Violations**

#### 🔴 **VIOLATION: Forced Branch**
A choice where all options lead to **identical variable state AND same ending**.

```
NODE-005 (FORCED):
  Choice A → NODE-007 → [set nothing] → NODE-020
  Choice B → NODE-008 → [set nothing] → NODE-020
  
  BOTH lead to ending: ENDING-001 with no variable diff
  → This choice is ILLUSORY
```

**Report**:
```
❌ NODE-005: Forced branch
   Both options reconverge with zero variable divergence
   Impact: Choice is cosmetic only
   Fix: Ensure Choice A and Choice B set different variables or lead to different ending
```

#### 🟡 **VIOLATION: Cosmetic-Only (if --strict)**
A choice where branches diverge in **dialogue/prose** but not in **game state** (variables or endings).

```
NODE-005 (COSMETIC):
  Choice A: "I trust you" → Same dialogue, no variable change
  Choice B: "I doubt you" → Different dialogue, no variable change
  Both → NODE-020 with identical variables
  
  → Choice affects only TEXT, not GAME STATE
```

**Report** (only with `--strict`):
```
⚠️  NODE-005: Cosmetic choice (--strict mode)
   Variables unchanged by either option
   Impact: Choice affects tone but not outcome
   Consider: Add relationship variable to make choice meaningful
```

#### ✅ **VALID: Divergent Outcome**
A choice where branches lead to:
- Different variable state, OR
- Different endpoints, OR
- Different ending(s) with different variable snapshots

```
NODE-005 (VALID):
  Choice A: "Help Marcus" 
    → NODE-007: set trust(marcus) += 1
    → Can reach: ENDING-ALLY or ENDING-RIVAL
    
  Choice B: "Betray Marcus"
    → NODE-008: set trust(marcus) -= 2
    → Can reach: ENDING-ENEMY only
    
  ✅ Different endings reachable based on choice
```

### 3B. **RPG-Specific Agency Violations** (if [PLATFORM] detected)

**For Tabletop RPG**:

#### 🟠 **VIOLATION: Companion Loyalty Forced Choice**
Companion loyalty choice doesn't actually change loyalty variable or NPC behavior.

```
SESSION-3, NODE-005 (Companion Choice - Forced):
  Choice A: "I trust your judgment, Theron"
    → NODE-007: [NO variable set]
    → Theron dialogue: "Thanks for the support"
    
  Choice B: "I need proof of your loyalty"
    → NODE-008: [NO variable set]
    → Theron dialogue: "I understand your doubts"
    
  Both NODE-007 and NODE-008:
    → Set loyalty(theron) = 2 (same for both)
    → Both lead to NODE-010 (identical state)
    
❌ Choice forced (both lead to identical loyalty regardless)

Fix: Choice A should set loyalty(theron) += 1; Choice B should set loyalty(theron) -= 1
```

#### 🟠 **VIOLATION: Faction Reputation Not Tracking**
Faction choice doesn't persist to later sessions or modules; reconverges without consequence.

```
SESSION-4, NODE-010 (Faction Choice):
  Choice A: "Help the Temple defeat heretics"
    → NODE-012: Set faction_temple_reputation += 2
    → NODE-015: (Session 4 end)
    
  Choice B: "Tell the heretics about the Temple plot"
    → NODE-013: Set faction_temple_reputation -= 3
    → NODE-015: (Session 4 end)
    
SESSION-5, NODE-020 (New session, new node):
  [Both SESSION-4 paths reconverge]
  → NODE-020: Check faction_temple_reputation...
  → WAIT: Both options have same quest availability???
  → Temple quests available regardless of reputation choice
  
❌ Reputation choice had no mechanical consequence

Fix: Make quest availability contingent on reputation threshold (reputation >= 1 for quests)
```

#### 🔴 **VIOLATION: Campaign-Level Choice Ignored**
Choice affects campaign-guide.md but guide not regenerated; creates out-of-sync state.

```
SESSION-2, NODE-008 (Party Composition Choice):
  Choice A: "Recruit Sir Theron to the party"
    → NODE-010: Set party_composition += "Theron", Set theron_joined = true
    → Should update: campaign-guide.md § Party Members section
    
  Choice B: "Decline Theron's offer"
    → NODE-010: Set theron_joined = false
    → Should update: campaign-guide.md to remove Theron from roster
    
  PROBLEM: campaign-guide.md still lists Theron in both paths
  ❌ Player guide out of sync with actual game state

Fix: Regenerate campaign-guide.md after Session 2; conditionally include Theron based on $theron_joined
```

**For Computer Game**:

#### 🔴 **VIOLATION: Playstyle Route Forced After Commitment**
Player chooses playstyle route but can still access nodes from other routes.

```
CHAPTER-2, NODE-008 (Route Commitment):
  Choice A: "Infiltrate stealth"
    → NODE-010: Set $player_playstyle = "stealth"
    
  Choice B: "Attack head-on"
    → NODE-010: Set $player_playstyle = "combat"
    
CHAPTER-3, NODE-015 (Later node):
  If $player_playstyle == "stealth":
    → NODE-020-STEALTH accessible
    → NODE-020-COMBAT accessible (WRONG!)
  
❌ Both route nodes accessible; choice not enforced

Fix: Add conditional: NODE-020-COMBAT only accessible if $player_playstyle == "combat"
```

#### 🟠 **VIOLATION: Accessibility Variant Not Consistent Across Routes**
Accessibility choice (e.g., colorblind mode) works in one playstyle route but not others.

```
CHAPTER-1, NODE-005 (Accessibility Choice):
  Choice: "Enable colorblind-friendly UI"
    → Set $accessibility_colorblind = true
    
CHAPTER-2, NODE-010 (Stealth Route):
  If $accessibility_colorblind:
    ✅ Guard alert states shown with patterns (not colors)
    ✅ Implemented consistently
    
CHAPTER-2, NODE-011 (Combat Route):
  If $accessibility_colorblind:
    ❌ Enemy indicators still use red/green only (no patterns)
    ❌ Accessibility choice ignored in this route
    
❌ Accessibility not available in all routes

Fix: Implement colorblind indicators in all route variants (Stealth, Combat, Diplomacy)
```

#### 🟠 **VIOLATION: Route-Exclusive Variable Leakage**
Variable from one route is readable in another route, violating route isolation.

```
CHAPTER-2, NODE-010 (Stealth Route Choice):
  Set $stealth_alarm_state = "silent"  (Only set in Stealth route)
  
CHAPTER-3, NODE-015 (Combat Route):
  If $stealth_alarm_state == "silent":
    → Unlock: "Enemies unprepared" combat bonus
  
❌ Stealth-exclusive variable affecting Combat route outcome

Fix: Either rename to $route_stealth_alarm_state (make explicitly route-specific) 
or share variable across all routes if intended
```

### 4. **Generate Agency Audit Report**

Create `specs/agency-audit.md`:

```markdown
## Agency Audit: [GAME_NAME]

**Date**: [ISO]
**Scope**: [all nodes | NODE-XXX | branch name]
**Platform**: [Generic / Tabletop-D&D5e / Tabletop-Pathfinder2e / Tabletop-Shadowrun6e / Computer-Game]

| Node ID | Choice Type | Option A | Option B | Divergence | RPG Type | Status |
|---------|-------------|----------|----------|-----------|----------|--------|
| NODE-005 | Trust? | Help | Betray | Variables + Endings | Companion Loyalty | ✅ VALID |
| NODE-010 | Path choice | North | South | Variables only | — | ✅ VALID |
| NODE-015 | Dialogue | Agree | Refuse | Dialogue only | — | ⚠️ COSMETIC |
| NODE-020 | Illusory | Accept | Decline | NONE | — | ❌ FORCED |
| SESSION-3-NODE-008 | Loyalty? | Trust Theron | Doubt Theron | Loyalty variable | Companion Quest | ✅ VALID |
| CHAPTER-2-NODE-010 | Route? | Stealth | Combat | $player_playstyle isolation | Playstyle Commitment | ✅ VALID |

**Legend**:
- **RPG Type**: — (not RPG) | Companion Loyalty | Faction Reputation | Campaign Persistence | Playstyle Commitment | Accessibility Variant
- **Divergence**: Variables + Endings | Variables only | Dialogue only | Route isolation | NONE
- **Status**: ✅ VALID | ⚠️ COSMETIC | ❌ FORCED | ❌ VIOLATED

### Violations Found

**🔴 Forced Branches**: 3
- NODE-020: Both options reconverge with zero state change
- NODE-025: "Yes/No" leads to identical ending regardless
- NODE-030: Dialogue differs but no variable impact

**🟡 Cosmetic-Only (--strict)**: 2
- NODE-015: Text flavor choice, no game state impact
- NODE-018: Tone variation, no mechanical consequence

### Summary

- **Total choice nodes**: 45
- **Fully branching choices**: 38 (84%)
- **Forced branches**: 3 (7%)
- **Cosmetic-only**: 2 (4%)
- **Ambiguous**: 2 (5%)

### Recommendations

**Priority 1 (Fix Forced Branches)**:
1. NODE-020: Add variable to differentiate outcomes
2. NODE-025: Split branch to lead to different endings
3. NODE-030: Add trust/relationship variable consequences

**Priority 2 (Enhance Cosmetic Choices)**:
1. NODE-015: Add exploration flag or character knowledge state
2. NODE-018: Link to later NPC reaction or dialogue option

**Priority 3 (Clarify Ambiguous)**:
1. NODE-XXX: Review for hidden variable implications
```

### 5. **Agency Strength Metric**

Calculate and report:

**Agency Ratio** = (Branching choices) / (Total choices)
- 80%+ = Strong agency (player feels empowered)
- 50-79% = Moderate agency (mostly player-driven)
- 20-49% = Weak agency (many forced moments)
- <20% = Weak agency (linear with illusion of choice)

**Endpoint Diversity** = (Unique ending states reachable) / (Theoretical maximum)
- How many of the endings.md entries are actually reachable from the root?
- Are some endings inaccessible due to forced branches blocking paths?

**For RPG Campaigns** (Additional Metrics):

**Tabletop - Companion Choice Coverage**:
- Companion loyalty nodes vs. total companion nodes = What % of companion scenes have agency?
- Acceptable: 60%+ (not every scene needs a choice)
- Issue: <40% (companions feel scripted)

**Tabletop - Faction Persistence**:
- Faction choices that persist across sessions = How many faction decisions carry forward?
- Track: Session A choice affects Session B quest availability?
- Unacceptable: 0% (faction choice impact stops at session end)

**Computer - Route Commitment Enforcement**:
- Node enforcement rate = (Nodes properly gating route-exclusive content) / (Total route-exclusive nodes)
- Must be: 100% (all route decisions must be enforced)
- Issue: <100% = route leakage (playstyle choice not respected)

**Computer - Accessibility Consistency**:
- Coverage % = (Routes with accessibility variant) / (Total routes)
- Acceptable: 100% (accessibility available in all routes)
- Issue: <100% = accessibility choice ignored in some paths

### 6. **Show Paths** (optional with --show-paths)

For each choice node, display all possible outcome states:

```
NODE-005: "Confront or Forgive?"

Path 1: Confront
  → NODE-007 → trust(marcus) = -2
  → NODE-012 → marcus_hostile = true
  → NODE-015 (ending gate)
  → Can reach: ENDING-BETRAYED, ENDING-RIVAL, ENDING-ENEMY

Path 2: Forgive
  → NODE-008 → trust(marcus) = 2
  → NODE-013 → marcus_grateful = true
  → NODE-015 (ending gate)
  → Can reach: ENDING-ALLY, ENDING-NEUTRAL, ENDING-HERO
```

**This helps writers visualize**: 
- Which ending(s) are reachable from which choice
- What variable state must exist to reach specific endings
- Where forced reconvergences happen

### 7. **Report**

Output `agency-audit.md` with:
- Violation count by type (forced, cosmetic, valid)
- Agency strength metrics
- Specific recommendations for fixes
- If `--show-paths`: Full endpoint visualization for each choice

---

## Important Notes

**Agency vs. Outcome**: A choice has **agency** if it changes state, NOT if it changes ending. Some choices can diverge on variables but converge back to the same ending (this is still valid agency — the journey differs).

**Forced Branches**: The enemy of agency. If both paths lead to identical state AND ending with no difference, remove the choice or add consequences.

**Cosmetic Choices**: Acceptable in moderation (flavor decisions). If >10% of choices are cosmetic-only, consider adding mechanical weight to player decisions.

**Reachability**: High agency doesn't matter if all choices lead to the same ending. Use `speckit.endings` to verify multiple endings are actually reachable from the agency nodes you're testing.

**RPG-Specific Notes**:

**Companion Loyalty is Not Optional**:
- Tabletop campaigns with companions MUST have loyalty-affecting choices
- Every meaningful companion scene (3+ per companion) should offer a choice that affects loyalty
- Companions with zero loyalty variance feel scripted (fails TR-006)
- Track loyalty state across entire campaign (not just one session)

**Faction Choices Must Persist**:
- Faction reputation changes in Session N must affect Session N+1+ quest availability
- If a faction choice only matters within the same session, it's effectively cosmetic
- Use speckit.series to verify faction reputation carries through campaign-guide.md updates

**Playstyle Routes Are Commitments**:
- Computer RPG: Once player chooses Stealth/Combat/Diplomacy route, they cannot access nodes from other routes
- This is NOT forced—it's route enforcement (players made the commitment)
- Breaking this (allowing route-exclusive nodes in other routes) violates CR-005
- Use accessibility variants (colorblind, audio, motor) orthogonally to routes (not as alternative routes)

**Campaign Persistence Matters**:
- Choice impact in Module 1 should be visible in Module 3+
- If companion chooses to leave party (Path C), they should not reappear unless explicitly recruited again
- Campaign prep documents (campaign-guide.md, party-roster.md) serve as contract: what guide says is ground truth

**Accessibility is Additive**:
- Accessibility variants (colorblind mode, audio cues, remapped controls) should NOT be treated as playstyle routes
- They should be available in ALL routes simultaneously
- A colorblind Stealth player should get both: route-specific (Stealth encounters) + accessibility-specific (colorblind guard patterns)

