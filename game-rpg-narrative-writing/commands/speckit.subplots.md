---
description: Subplot resolution tracker — verify all subplots are started AND resolved in each branch. Detects dangling plot threads and incomplete arcs across different playthroughs. For RPG campaigns (tabletop D&D/Pathfinder/Shadowrun and computer game), tracks companion quests, faction storylines, playstyle route branches, and campaign continuity.
handoffs:
  - label: Check Continuity
    agent: speckit.continuity
    prompt: After verifying subplot resolution, check cross-node continuity.
    send: true
  - label: Revise Subplots
    agent: speckit.revise
    prompt: Some subplots are unresolved. Please add resolution nodes.
    send: true
---

# speckit.subplots

Subplot resolution tracker — verify all subplots are **started, developed, and resolved** (not abandoned) across all branches and endings. Ensures no playthrough feels unfinished due to dropped threads.

**RPG Campaign Support**: Adapts subplot tracking for tabletop (companion quests, faction storylines, session-based arcs with campaign prep integration) and computer game (playstyle routes with accessibility consistency).

## Subplot Principle

A **subplot** is a secondary story arc (distinct from main plot). 

**Well-executed subplot**:
- ✅ Introduced clearly (player understands a thread exists)
- ✅ Developed (plot progresses, stakes raised)
- ✅ Resolved (thread tied off, tension released)
- ✅ Consistent across branches (same subplot handled similarly in all paths)

**Failed subplot**:
- ❌ Started but never mentioned again (dangling thread)
- ❌ Resolved prematurely (anticlimactic)
- ❌ Resolved differently per branch (inconsistent handling)
- ❌ Only resolved in some branches (abandoned in others)

## User Input

```text
$ARGUMENTS
```

Accepted input:
- Nothing — audit all subplots across all branches
- Subplot ID (e.g., `SUB-001`) — audit one subplot only
- `--branch [BRANCH_ID]` — audit subplots in one story branch only
- `--unresolved-only` — show only subplots with missing resolutions

Optional flags:
- `--strict` — flag unresolved subplots in any branch as failures (not warnings)
- `--show-threads` — display introduction → development → resolution for each subplot
- `--consistency-check` — verify subplot handling is consistent across branches

## Pre-Execution Checks

**Auto-detect platform and ruleset** (for RPG campaigns):
- Load `constitution.md`
- Extract `[PLATFORM]` (tabletop/computer) and `[RULESET]` (D&D 5e/Pathfinder 2e/Shadowrun 6e)
- Set SESSION object: `{platform: [PLATFORM], ruleset: [RULESET], mechanics: [MECHANICS]}` for downstream checks
- If no platform found: treat as generic interactive fiction (no RPG-specific logic)

**Standard Pre-Execution**:
1. Load `specs/subplots-template.md` if present (or create from spec.md secondary arcs)
2. Confirm `specs/plan.md` exists with branch/route structure
3. Load all `draft/[ENGINE]/NODE-*.md` files
4. Parse plan.md to identify branch divergence points (or playstyle routes for Computer)
5. Map which nodes are reachable per branch/route
6. For RPG: Load `mechanics-[RULESET].md`, `companions.md`, `factions.md` (if applicable)

## Execution Steps

### 1. **Define Subplots**

Subplots come from `specs/subplots-template.md` or extracted from spec.md secondary story arcs. Each subplot has:
- **SUB-ID**: Unique identifier
- **Name**: Subplot title (e.g., "The Heist with Victor")
- **Type**: Generic / Companion Quest (tabletop) / Faction Storyline (tabletop) / Playstyle Route (computer) / Accessibility Variant (computer)
- **Start node**: Where subplot is introduced
- **Key scenes**: Development beats
- **Resolution nodes**: Where subplot concludes (may vary per branch/route)
- **RPG Integration** (if applicable):
  - Tabletop: Associated companion(s), faction(s), session range, campaign prep doc impact
  - Computer: Associated playstyle route(s), accessibility variants, route-exclusive flag

**Example RPG Subplot Definitions**:

**Tabletop - Companion Quest**:
```
SUB-002: Sir Theron's Redemption
  Type: Companion Quest
  Companion: Sir Theron (Knight, joins Session 3)
  Sessions: 3-8
  Introduction: SESSION-3, NODE-005 (Theron reveals shame from past defeat)
  Development:
    • SESSION-4, NODE-010: Theron's old enemy appears in tavern
    • SESSION-6, NODE-015: Must choose: help Theron face enemy or avoid
    • SESSION-7, NODE-018: Trial by combat OR negotiation
  Resolution:
    • Path A (combat): NODE-020 (Theron defeats enemy; honor restored; loyalty +3)
    • Path B (diplomacy): NODE-022 (Enemy revealed not evil; reconciliation; loyalty +2)
    • Path C (avoided): NODE-025 (Theron leaves party in shame; loyalty -5)
  Campaign Impact: 
    - Updates campaign-guide.md with Theron's arc
    - Affects party composition (if Path C, lost companion)
    - May trigger follow-up faction quests
  Ruleset Mechanics (D&D 5e): 
    - Trial uses Intelligence save DC 15 (negotiation check) or STR save DC 12 (combat)
    - Victory grants: +1 to Theron's next saving throw, +250 XP party bonus
```

**Tabletop - Faction Storyline**:
```
SUB-003: Temple of Light Ascension
  Type: Faction Storyline
  Faction: Temple of Light (reputation tracker)
  Sessions: 1-12 (continuous arc across campaign)
  Introduction: SESSION-1, NODE-005 (Priestess recruits party for cause)
  Development:
    • SESSION-4: Faction Quest 1: Rescue temple artifact (reputation +2)
    • SESSION-7: Faction Quest 2: Expose heresy in temple (reputation +1 or +2 depending on approach)
    • SESSION-10: CHOICE POINT: purge heretics or offer redemption
  Resolution:
    • Path A (purge): NODE-030 (Temple strengthened; faction quests end; reputation +5)
    • Path B (redemption): NODE-032 (Temple split; new faction splinter; reputation +3)
    • Path C (ignore faction): NODE-025 (Temple destroyed by heresy; reputation -5)
  Campaign Impact: 
    - Affects available quests from SESSION-11 onward
    - Determines NPC availability in later modules
    - Updates faction reputation table in series-bible.md
  Ruleset Mechanics (D&D 5e):
    - Heresy detection: Religion check DC 16
    - Faction quest rewards scale with party level (scales from 2nd to 5th level)
    - Reputation bonuses affect faction NPC behavior (charisma advantage on persuasion vs faction NPCs)
```

**Computer - Playstyle Route (Stealth)**:
```
SUB-004: The Infiltration - Stealth Route
  Type: Playstyle Route
  Route: Stealth
  Chapters: 2-4
  Introduction: CHAPTER-2, NODE-005 (Objective: Enter Tower undetected)
  Development:
    • CHAPTER-2: Bypass 3 guard encounters (Stealth checkpoints)
    • CHAPTER-3: Puzzle: Find key in captain's quarters (Silent approach required)
    • CHAPTER-4: Boss encounter: escape with scroll (Stealth + timed movement)
  Resolution: NODE-020 (Exit successful; "Silent Infiltrator" achievement unlocked)
  Accessibility: Colorblind mode includes patrol patterns (diamonds for alert, lines for searching)
  Route-Exclusive: Yes (not available in Combat or Diplomacy routes)
  Playstyle Balance: 85 points (3 encounters + 1 puzzle + 1 boss)
```

**Computer - Accessibility Variant (Colorblind Mode)**:
```
SUB-005: Colorblind Mode - All Routes
  Type: Accessibility Variant
  Variant: Colorblind (Deuteranopia/Protanopia)
  Applies To: All routes, all chapters
  Changes:
    • Guard indicators: Color + pattern (red circles = alert, blue squares = searching)
    • Light/shadow distinction: Added texture overlay (not color-dependent)
    • Obstacle markers: Shape + label combinations (not color coding)
    • UI elements: Contrast ratio verified WCAG AA 4.5:1
  Testing: Verified with Color Blind Simulator (Deuteranopia, Protanopia, Tritanopia)
  Campaign Impact: Available from game start; no gameplay impact
```

### 2. **Trace Subplots Through Branches / Routes**

For each subplot, trace through ALL possible story branches (generic / tabletop) or playstyle routes (computer):

**Branch A (help Victor)**:
```
NODE-005 → SUB-001 STARTS
  victor_status = "needs_help"
  
NODE-010 → SUB-001 DEVELOPS
  player_knows: victor_daughter = "Lily"
  
NODE-015 → SUB-001 CHOICE
  Choice: "Help Victor" → victor_status = "escaped"
  
NODE-020 → SUB-001 RESOLVES
  "Victor embraces you. 'Lily will never forget this.'"
  ✅ SUBPLOT COMPLETE
```

**Branch B (flee Victor)**:
```
NODE-005 → SUB-001 STARTS
  victor_status = "needs_help"
  
NODE-010 → SUB-001 DEVELOPS
  player_knows: victor_daughter = "Lily"
  
NODE-015 → SUB-001 CHOICE
  Choice: "Flee" → victor_status = "abandoned"
  
NODE-022 → SUB-001 RESOLVED DIFFERENTLY
  "Later, you hear Victor was caught. Lily was placed in foster care."
  ✅ SUBPLOT COMPLETE (different variant)
```

**Branch C (never meet Victor)**:
```
NODE-005 → SUB-001 SKIPPED (this branch doesn't encounter Victor)
  
NODE-003 → ALTERNATE PATH (no Victor)

NODE-025 → ENDING REACHED
  SUB-001 never mentioned
  ❌ SUBPLOT ABANDONED
  (This branch has no Victor arc at all)
```

### 3. **Detect Subplot Violations**

#### 🔴 **VIOLATION: Dangling Thread**
Subplot is introduced but never resolved in one or more branches.

```
SUB-002: The Prophecy

Branch A (help Victor):
  NODE-005: Prophet: "You will face three trials"
  NODE-010: First trial appears
  NODE-015: Second trial appears
  NODE-020: ENDING REACHED
  ❌ Third trial never appears; prophecy unresolved

Branch B (flee Victor):
  NODE-005: Prophet: "You will face three trials"
  NODE-010: First trial appears
  NODE-015: Second trial appears
  NODE-022: Third trial appears; prophecy fulfilled
  ✅ Resolved
```

**Report**:
```
SUB-002: The Prophecy
  Branch A: Introduced ✅ → Partial development ✅ → NO RESOLUTION ❌
  Branch B: Introduced ✅ → Full development ✅ → Resolved ✅
  
  Status: ⚠️  INCONSISTENT
  Impact: Branch A playthrough feels unfinished
  Fix: Either add 3rd trial to Branch A, or remove from prophecy
```

#### 🟡 **VIOLATION: Premature Resolution**
Subplot is resolved before proper development.

```
SUB-003: Love Triangle
  NODE-005: Introduce Sera and Marcus as romantic interests
  NODE-010: Hint at tension between them
  NODE-012: ENDING REACHED before love choice is forced
  
  ❌ Subplot introduced but never developed
  Fix: Add at least one "must choose between them" moment before ending
```

#### 🟠 **VIOLATION: Inconsistent Resolution**
Subplot is resolved differently in different branches for no narrative reason.

```
SUB-004: The Artifact

Branch A:
  NODE-005-015: Artifact is important MacGuffin
  NODE-020: Player destroys artifact; magical chaos ensues; chaos averted through effort
  ✅ Consistent with build-up

Branch B:
  NODE-005-015: Artifact is important MacGuffin
  NODE-022: Artifact mentioned once, then forgotten
  NODE-025: Ending reached, artifact never mentioned again
  ❌ Subplot dropped for no reason

Status: ⚠️  INCONSISTENT
Impact: Same subplot handled completely differently despite similar setup
Fix: Either include artifact resolution in Branch B, or explain why it's omitted
```

#### ✅ **VALID: Consistent Multi-Variant**
Subplot resolved in all branches, but with meaningful variations.

```
SUB-005: Trust with Marcus

Branch A (help Marcus):
  NODE-010: Marcus confides secret
  NODE-015: Must prove trust via sacrifice
  NODE-020: "We did it together. I'll never forget this."
  ✅ Resolved with partnership
  
Branch B (betray Marcus):
  NODE-010: Marcus confides secret
  NODE-015: Can exploit secret for gain
  NODE-022: "You have what you wanted. Marcus is ruined."
  ✅ Resolved with betrayal

Branch C (neutral):
  NODE-010: Marcus hints at secret
  NODE-018: Subplot fades; Marcus reassigned
  NODE-025: Brief mention: "Marcus moved on. We never got close."
  ✅ Resolved with distance (intentional ambivalence)

All variants: Subplot initiated, developed, and concluded
Variations: Meaningful based on player choice
Status: ✅ EXCELLENT handling
```

### 3B. **RPG-Specific Subplot Violations** (if [PLATFORM] detected)

**For Tabletop RPG**:

#### 🟠 **VIOLATION: Companion Quest Not Resolved Before Departure**
Companion quest is started but never resolved before companion leaves party or module ends.

```
SUB-002: Theron's Redemption (Companion Quest)

Session 3-5: Quest introduced, enemy appears
Session 6: Party in different location; Theron's quest not addressed
Session 8: Party moves to new town; Theron leaves party without resolution
❌ Quest abandoned (unresolved)

Fix: Either resolve quest before Session 8, or make quest resolution optional (Theron stays if unresolved)
```

#### 🟠 **VIOLATION: Faction Reputation Inconsistency**
Faction subplot changes reputation differently across sessions/modules for no narrative reason.

```
SUB-003: Temple of Light (Faction)

Module 1: Help temple (+2 reputation)
Module 2: Temple damaged in conflict → reputation -3
Module 3: Party never visits temple → reputation +1 (????)
❌ Reputation tracking inconsistent

Fix: Either continue -3 penalty, or add narrative reason for recovery (+1 needs quest justification)
```

#### 🔴 **VIOLATION: Campaign Prep Doc Not Updated**
Companion arc or faction storyline affects campaign-guide.md but guide not regenerated.

```
SUB-002: Theron's Redemption - Session 8
Theron leaves party in shame (Path C)
Campaign-guide.md still lists Theron as "Active Companion"
❌ Campaign guide out of sync with actual game state

Fix: Regenerate campaign-guide.md after Module 1; remove Theron from Module 2 if left
```

**For Computer Game**:

#### 🟠 **VIOLATION: Route Accessibility Not Consistent**
Subplot available in one playstyle route but missing accessibility variant.

```
SUB-004: Infiltration - Stealth Route
✓ Colorblind variant exists (patterns + labels)
✓ Audio variant exists (guard callouts)
❌ Motor variant missing (can't complete timed sequence with remapped controls)

Fix: Add motor-accessible variant (auto-advance option or extended time window)
```

#### 🟠 **VIOLATION: Route-Exclusive Subplot Breaks Balance**
Playstyle route has exclusive subplot that significantly imbalances content ratio.

```
Routes:
- Stealth: 85 points base + SUB-004 (15 points) = 100 points
- Combat: 78 points base (no exclusive subplot) = 78 points
- Diplomacy: 81 points base (no exclusive subplot) = 81 points

Ratio: 100/78 = 1.28× imbalanced
❌ Stealth route has 22% more content

Fix: Either remove SUB-004 exclusive flag (add to other routes) or reduce by 7 points
```

#### 🔴 **VIOLATION: Variable Pollution from Route-Exclusive Subplot**
Route-exclusive subplot sets variable accessible from other routes.

```
SUB-004: Stealth Route Infiltration
  Sets: $stealth_discovered_tunnel = true
  Later, Combat Route can check: "if $stealth_discovered_tunnel, reveal shortcut"
  
❌ Route-exclusive content leaking to other routes

Fix: Either rename to $stealth_route_discovered_tunnel (make it route-specific) or share subplot with all routes
```

### 4. **Generate Subplot Resolution Report**

Create `specs/subplot-audit.md`:

```markdown
## Subplot Resolution Audit

**Game**: [NAME]
**Date**: [ISO]

### Subplot Status Table

| SUB-ID | Name | Type | Start | Branch A | Branch B | Branch C | RPG Info | Status |
|--------|------|------|-------|----------|----------|----------|----------|--------|
| SUB-001 | Victor | Generic | NODE-005 | ✅ Resolved | ✅ Resolved | N/A | — | ✅ PASS |
| SUB-002 | Theron's Redemption | Companion Quest | NODE-005 | ✅ Resolved | ✅ Resolved | ❌ Abandoned | Companion: Theron (Knight); Sessions: 3-8 | ❌ FAIL |
| SUB-003 | Temple of Light | Faction Storyline | NODE-005 | ⚠️ Inconsistent | ✅ Resolved | ✅ Resolved | Faction: Temple; Reputation tracker | ⚠️ REVIEW |
| SUB-004 | The Infiltration | Playstyle Route | CH-2-005 | ✅ Stealth | ✅ Combat | ✅ Diplomacy | Route: Stealth; Exclusive: Yes | ✅ PASS |
| SUB-005 | Colorblind Mode | Accessibility Variant | All | ✅ All routes | ✅ All routes | ✅ All routes | Variant: Colorblind; Coverage: 100% | ✅ PASS |

**Legend**:
- **Type**: Generic (interactive fiction) | Companion Quest (RPG tabletop) | Faction Storyline (RPG tabletop) | Playstyle Route (RPG computer) | Accessibility Variant (RPG computer)
- **RPG Info**: Relevant campaign tracking (companion name/type, faction name, route name, accessibility type)
- **Branch/Route**: ✅ = Resolved | ⚠️ = Incomplete | ❌ = Abandoned
- **Status**: ✅ PASS = All branches resolved; ⚠️ REVIEW = Inconsistency needs narrative justification; ❌ FAIL = Abandoned or broken rules

**🔴 Abandoned in Branch(es)** (3):
- SUB-002 (Prophecy): Unresolved in Branch A
- SUB-004 (Artifact): Dropped in Branch B entirely
- SUB-007 (Sister's Fate): Not mentioned in Branch C

**🟡 Inconsistent Resolution** (2):
- SUB-003 (Love Triangle): Premature in Branch A, full arc in Branches B/C
- SUB-006 (Rebellion): Different outcomes with no linking narrative

**✅ Consistent & Complete** (3):
- SUB-001 (Victor): Different resolutions per choice, both satisfying
- SUB-005 (Trust with Marcus): Varied per player agency, all conclusive
- SUB-008 (The Mystery): Resolved in all branches

### Recommendations

**Priority 1 (Fix before release)**:
1. SUB-002 (Prophecy): Add 3rd trial to Branch A OR remove from prophecy
2. SUB-004 (Artifact): Either include artifact payoff in Branch B OR justify omission
3. SUB-007 (Sister's Fate): Ensure at least brief mention in Branch C

**Priority 2 (Polish)**:
1. SUB-003 (Love Triangle): Add at least one development beat to Branch A before ending
2. SUB-006 (Rebellion): Add transitional dialogue explaining different outcomes

**Priority 3 (Enhancement)**:
1. Consider expanding SUB-008 to add Branch-specific variant details
```

### 5. **Show Threads** (optional with --show-threads)

For each subplot, display full intro → development → resolution path:

```
SUB-001: Victor's Redemption

BRANCH A (Help Victor):
  NODE-005 [INTRO]
    "A man approaches. His hands shake. 'Please, you have to help me.'"
    → victor_status = "needs_help"
  
  NODE-010 [DEVELOP]
    "Victor shows you a photograph. 'This is Lily. My daughter.'"
    → player_knows["victor_daughter"] = true
  
  NODE-015 [CHOICE POINT]
    "The mob's car turns the corner. Victor looks at you.
     What do you do?"
    Choice A: Help Victor
    Choice B: Run
  
  → IF Choice A:
    NODE-020 [RESOLVE]
    "Victor embraces you. 'Lily will never forget this.'"
    → victor_status = "escaped"
    → relationship["victor"] += 3
    ✅ COMPLETE
  
  → IF Choice B:
    NODE-022 [RESOLVE]
    "Later, you hear Victor was captured.
     His daughter was placed in state care."
    → victor_status = "captured"
    → relationship["victor"] -= 2
    → reputation -= 1
    ✅ COMPLETE (different variant)
```

### 6. **Consistency Check** (optional with --consistency-check)

Compare how same subplot is handled across branches:

```
SUB-002: The Prophecy

Branch A vs Branch B:
  Introduction:
    Both: Prophet appears at NODE-005 ✅ (consistent)
  Development:
    Branch A: 2 of 3 trials ⚠️
    Branch B: All 3 trials ✅
    Consistency: ❌ UNEVEN
  Resolution:
    Branch A: None ❌
    Branch B: Full prophecy fulfilled ✅
    Consistency: ❌ INCONSISTENT
  
  Verdict: Subplots handled inconsistently
  Fix: Either add trial 3 to Branch A OR reduce trial count to 2
```

### 7. **Report**

Output `subplot-audit.md` with:
- Subplot status table (all branches checked)
- Violation list (abandoned, inconsistent, premature)
- Specific recommendations for each issue
- If `--show-threads`: Full intro → dev → resolution paths
- If `--consistency-check`: Branch-by-branch comparison table

---

## Important Notes

**Branch-Specific Variants Are OK**: Same subplot can resolve differently per branch if the variation is **intentional and meaningful**. A subplot can end in triumph in one branch and tragedy in another—that's good interactive narrative design.

**"No subplot" is OK Too**: A subplot can be skipped entirely in a branch if the branch diverges before it's introduced. But if a subplot is *introduced*, it must be *resolved* (even if resolution is "this branch doesn't pursue it").

**Consistency Standard**: All resolved subplots should resolve *approximately* at the same story point. If one subplot resolves in NODE-10 in one branch and NODE-30 in another, flag it as pacing inconsistency (use `speckit.pacing` for details).

**Dangling Threads**: In moderation, a minor unresolved thread can add realism ("not everything wraps up perfectly"). But systematically unresolved subplots across multiple branches = incomplete narrative. Flag anything that feels like unfinished business.

