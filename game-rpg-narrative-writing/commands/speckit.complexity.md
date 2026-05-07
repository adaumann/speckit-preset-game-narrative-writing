---
description: Branch complexity analyzer — detect exponential growth, warn on unsustainable branching patterns, estimate maintenance effort per branch depth. For RPG campaigns (tabletop D&D/Pathfinder/Shadowrun and computer game), analyzes session branching complexity, companion loyalty state combinations, playstyle route branching, and accessibility variant combinations.
handoffs:
  - label: Check Replayability
    agent: speckit.replayability
    prompt: After analyzing branch complexity, measure unique content per playthrough.
    send: true
  - label: Review Planning
    agent: speckit.plan
    prompt: Branch complexity is high. Consider consolidating or scoping.
    send: true
---

# speckit.complexity

**RPG Campaign Support**: Adapts branch complexity analysis for tabletop (session branching, companion loyalty state combinations, faction reputation decision trees, campaign module interdependencies) and computer game (playstyle route branching, accessibility variant combinations, route-exclusive content explosion, feature complexity per route).

Branch complexity analyzer — detect **exponential branch growth**, warn on unsustainable branching patterns, estimate maintenance effort. Helps prevent "branching hell" (250+ nodes with 2^N combinations).

## Complexity Principle

**Sustainable branching** = Each choice is meaningful; maintenance effort scales linearly or sub-exponentially.

**Unsustainable branching includes**:
- ❌ Every node has 3+ branches (exponential explosion)
- ❌ Deep nesting (15+ levels of branching)
- ❌ Reconvergence-free design (all branches stay separate)
- ❌ Poor branch tracking (can't maintain code quality)

**Valid complexity includes**:
- ✅ Early choices create major branches; later consolidate
- ✅ Linear main path with occasional 2-branch splits
- ✅ Deep complexity in limited areas (side quests), linear elsewhere
- ✅ Deliberate branching: each branch has distinct content/mechanics

## User Input

```text
$ARGUMENTS
```

Accepted input:
- Nothing — analyze overall branch complexity
- `--depth` — focus on branch depth (longest path length)
- `--breadth` — focus on branch breadth (# parallel branches at each point)
- `--maintenance` — estimate work per branch variant

Optional flags:
- `--strict` — flag any node with >2 branches as risky
- `--show-tree` — ASCII tree of branch structure
- `--convergence-map` — show where branches merge
- `--estimate-nodes` — calculate total node count needed for all branches

## Pre-Execution Checks

**Auto-detect platform and ruleset** (for RPG campaigns):
- Load `constitution.md`
- Extract `[PLATFORM]` (tabletop/computer) and `[RULESET]` (D&D 5e/Pathfinder 2e/Shadowrun 6e)
- Set SESSION object: `{platform: [PLATFORM], ruleset: [RULESET], mechanics: [MECHANICS]}` for downstream checks
- If no platform found: treat as generic interactive fiction (no RPG-specific logic)

Then:
1. Load `specs/plan.md`: Complete branch structure
2. Load all `draft/[ENGINE]/NODE-*.md` files to count existing nodes
3. Map branch divergence points and convergence points
4. Estimate unwritten nodes per branch
5. If RPG: Load `companions.md`, `factions.md`, `mechanics-[RULESET].md` (if applicable)
6. Calculate maintenance metrics

## Execution Steps

### 1. **Map Branch Structure**

From plan.md, create branch topology:

```
Branch tree structure (ASCII simplified):

NODE-001 [START]
│
├─ NODE-005 [INTRO]
│  │
│  ├─ NODE-010 [Help Victor?]
│  │  ├─ YES → NODE-015 [BRANCH A: Redemption]
│  │  │  ├─ NODE-020
│  │  │  └─ NODE-025 [END A]
│  │  │
│  │  └─ NO → NODE-016 [BRANCH B: Betrayal]
│  │     ├─ NODE-021
│  │     └─ NODE-026 [END B]
│  │
│  └─ NODE-011 [Flee?]
│     └─ NODE-017 [BRANCH C: Escape]
│        ├─ NODE-022
│        └─ NODE-027 [END C]

Topology metrics:
  • Depth: 4 levels (START → choice → content → ending)
  • Breadth at NODE-010: 3 branches (high)
  • Total branches: 3 distinct endings
  • Convergence: Branches don't reconverge (stay separate)
```

**RPG Example - Tabletop Campaign Sessions**:
```
Campaign branch structure (by session):

SESSION-1 → SESSION-2 [Companion Recruitment]
  ├─ Recruit Sir Theron
  │  └─ SESSION-3: Theron's honor quest intro
  │     ├─ SESSION-4: Defend Theron's honor → loyalty += 1
  │     ├─ SESSION-5: Betray Theron → loyalty -= 2
  │     └─ SESSION-8: Theron leaves party if loyalty < 0
  │
  ├─ Recruit Mage Sera
  │  └─ SESSION-3: Sera's magic research quest intro
  │     └─ SESSION-6: Sera's quest concludes
  │
  └─ Recruit neither
     └─ SESSION-3-8: Solo campaign (different encounters)

Complexity factors:
  • Session interconnections: 3 companion paths × 2 loyalty states × 3 sessions = 18 combinations
  • Companion state variables: loyalty(theron) × loyalty(sera) = 2 independent dimensions
  • Campaign impact: Each companion choice affects available quests in Sessions 4-8
  • Module interdependencies: Session 5 content varies based on Session 2 companion choice
  
Status: Medium complexity (manageable with shared main quests)
```

**RPG Example - Computer Game Playstyle Route Branching**:
```
Route branching structure (by chapter):

CHAPTER-1 [Setup] → CHAPTER-2 [Route Commitment]
  ├─ Stealth Route
  │  ├─ CHAPTER-3: Infiltration encounters (5 unique nodes)
  │  ├─ CHAPTER-4: Stealth boss fight (3 unique variants)
  │  └─ ENDING: Stealth-specific ending (2 unique)
  │
  ├─ Combat Route
  │  ├─ CHAPTER-3: Combat encounters (5 unique nodes)
  │  ├─ CHAPTER-4: Combat boss fight (3 unique variants)
  │  └─ ENDING: Combat-specific ending (2 unique)
  │
  └─ Diplomacy Route
     ├─ CHAPTER-3: Negotiation encounters (5 unique nodes)
     ├─ CHAPTER-4: Diplomacy resolution (3 unique variants)
     └─ ENDING: Diplomacy-specific ending (2 unique)

Complexity metrics:
  • Routes: 3 (Stealth, Combat, Diplomacy)
  • Route-exclusive nodes: ~18 per route = 54 nodes total
  • Route variants in bosses: 3 routes × 2 variants = 6 combinations
  • Accessibility variants: 3 accessibility types × 3 routes = 9 variants
  • Total branching combinations: 6 route choices × 2 ending variants = 12 paths
  
Maintenance burden:
  • Each route is self-contained (low cross-pollution)
  • Accessibility variants add 30% content overhead
  • Testing matrix: 3 routes × 2 boss variants = 6 test paths
  
Status: High breadth (3 equal routes), manageable depth (4 chapters each)
```

### 2. **Analyze Branch Depth**

Measure the longest path:

```
Longest path (critical path depth):
  NODE-001 → NODE-005 → NODE-010 → NODE-015 → NODE-020 → NODE-025
  Depth: 6 nodes

Branch A depth: 6 nodes
Branch B depth: 6 nodes
Branch C depth: 6 nodes

Max depth: 6 (moderate)

Complexity assessment:
  • 1–3: Minimal branching (linear story)
  • 4–8: Moderate branching (sustainable)
  • 9–15: Complex branching (intensive)
  • 16+: Exponential (risky, unsustainable)

Status: ✅ MODERATE (depth is sustainable)
```

### 3. **Analyze Branch Breadth**

Measure branching factor at each point:

```
Branching factor (# of branches at each choice point):

NODE-010 [choice point]: 3 branches (Help / Betray / Flee)
  Branching factor: 3
  
NODE-015 [sub-choice within branch A]: 2 branches (Violent / Stealth)
  Branching factor: 2
  
NODE-020 [convergence check]: Do all branches arrive here?
  Branch A: arrives
  Branch B: arrives
  Branch C: arrives
  Convergence: YES
  
Analysis:
  Total branches from NODE-010: 3
  Sub-branches at NODE-015 (A only): 2
  Total possible combinations at NODE-020: 3 × 1 × 2 = 6 combinations

But wait:
  Branch B and C have no NODE-015 sub-choice
  So actual combinations:
    • Branch A: 1 × 2 = 2 combinations (main × sub-choice)
    • Branch B: 1 combination (no sub-choice)
    • Branch C: 1 combination (no sub-choice)
    • Total: 4 combinations (not 6)

Status: ✅ MANAGEABLE (branching is localized to Branch A)
```

### 4. **Calculate Total Node Requirements**

Estimate nodes needed for all branches:

```
Node accounting:

Shared nodes (all branches):
  NODE-001 through NODE-010: 10 nodes × 1 = 10 nodes

Branch A (Help Victor):
  NODE-015 → NODE-020 → NODE-025: 3 nodes
  Sub-choice at NODE-015: × 2 variants
  Total Branch A: 6 nodes (3 nodes × 2 variants)

Branch B (Betray Victor):
  NODE-016 → NODE-021 → NODE-026: 3 nodes × 1 = 3 nodes

Branch C (Flee):
  NODE-017 → NODE-022 → NODE-027: 3 nodes × 1 = 3 nodes

Total: 10 + 6 + 3 + 3 = 22 nodes

Breakdown:
  • Shared: 45% (10/22)
  • Branch-specific: 55% (12/22)
  
Efficiency: ✅ Reasonable ratio (some shared content reduces duplication)
```

### 5. **Detect Complexity Problems**

#### 🔴 **PROBLEM: Exponential Explosion**
Every node spawns multiple branches; combinations grow uncontrollably.

```
Hypothetical design:

NODE-001 [choice point]: 3 branches
NODE-010 [choice point in each branch]: 3 branches × 3 options = 9 paths
NODE-015 [choice point in each path]: 9 paths × 3 options = 27 paths
NODE-020 [choice point in each path]: 27 paths × 3 options = 81 paths

Exponential formula: 3^N where N=4 choices = 81 paths

At 81 paths with 5 unique nodes per path = 405 nodes needed
At average 2 hours per node = 810 hours of writing

Status: 🔴 EXPONENTIAL EXPLOSION
        This is "branching hell"

Red flags:
  • >100 possible paths
  • >200 nodes estimated
  • Writer spending >50% of time on minor branch variations
  
Fix options:
  1. Reduce branching factor (use binary choices, not ternary)
  2. Add convergence points (branches merge after divergence)
  3. Scope branching to specific areas (main story linear, side quests branchy)
  4. Use variable flags instead of node branching (same state, different prose)
```

#### 🟡 **PROBLEM: Uncontrolled Depth**
Branches continue diverging without convergence; maintenance becomes impossible.

```
Design:

NODE-001 → NODE-005 → NODE-010 → NODE-015 → NODE-020 → NODE-025
  (each node diverges into 2 branches, never reconverges)

Paths: 2^6 = 64 possible paths

At 64 paths:
  • Impossible to test all variations
  • Changes to shared content affects all 64 paths
  • Bug in NODE-010 might not manifest until NODE-025
  
Status: 🟡 MAINTENANCE NIGHTMARE
        Not exponential in scope, but high in dependency risk

Red flags:
  • Depth >8 without convergence
  • No "sync points" where branches meet
  • Test matrix is >32 combinations

Fix options:
  1. Add convergence after each divergence (e.g., NODE-010 diverges, NODE-012 reconverges)
  2. Use convergence at story beats (e.g., "all branches meet before act 2")
  3. Limit depth to <5 without reconvergence
```

#### 🟠 **PROBLEM: Unnecessary Parallelism**
Multiple branches do the same thing; duplication instead of branching.

```
Branch A (NODE-010):
  Prose: "You hide behind the boxes."
  Next: NODE-015
  
Branch B (NODE-010):
  Prose: "You duck behind the wall."
  Next: NODE-015
  
Branch C (NODE-010):
  Prose: "You crouch under the table."
  Next: NODE-015
  
All three branches:
  • Accomplish same goal (hide)
  • Lead to same node (NODE-015)
  • Have same outcome (NPC doesn't see you)
  
Status: 🟠 UNNECESSARY BRANCHING
        These are cosmetic flavor variants, not meaningful choices

Problem: Uses 3 node slots for flavor text
         Increases maintenance (changes to NODE-015 need 3 paths updated)

Fix options:
  1. Combine into single node with multiple hide descriptions
  2. Keep as branches only if each has meaningfully different consequences
  3. Use conditional prose (if player_choice=hide_boxes, show that text)
```

#### 💨 **PROBLEM: Orphaned Branches**
Branch has no convergence back to main story; stranded content.

```
NODE-010 [choice point]: Explore / Don't Explore

Explore branch:
  NODE-015 [side quest start]
  NODE-020 [side quest middle]
  NODE-025 [side quest complete]
  NODE-030: ??? (where do players go after quest?)
           No connection back to main story
           Side quest ends in vacuum
  
Don't Explore branch:
  NODE-012 [main story continues]
  NODE-017 [main story]
  NODE-022 [reconverges with Explore branch]
  
Status: 💨 ORPHANED BRANCH
        Explore path leads to NODE-030 (dead end)
        No way back to main story

Problem: Players get stuck after completing side quest
         Design was incomplete at NODE-025

Fix: Either
  1. Merge NODE-030 back to main story (e.g., NODE-030 → NODE-022)
  2. Make NODE-025 ending final (side quest completes game)
  3. Add explicit "return to town" choice at NODE-025
```

### 5B. **Detect RPG Campaign Complexity Problems** (if [PLATFORM] detected)

**For Tabletop RPG**:

#### 🔴 **PROBLEM: Exponential Companion State Combinations**
Multiple companions with loyalty states create testing nightmare.

```
Campaign with 3 companions:

Companion states:
  • Theron: loyalty range -5 to +5 (11 possible values)
  • Sera: loyalty range -5 to +5 (11 possible values)
  • Marcus: loyalty range -5 to +5 (11 possible values)

Total combinations: 11 × 11 × 11 = 1,331 possible states

But party composition branches add more:
  • Theron left party: companion state = "inactive"
  • Sera left party: companion state = "inactive"
  • Marcus left party: companion state = "inactive"

Actual complexity:
  • Possible party configurations: 2^3 = 8 (each companion in/out)
  • For each config, loyalty combinations: varies by config
  • SESSION-5 content branches by: party composition + loyalty states
  
Status: 🔴 EXPONENTIAL EXPLOSION
        Testing all combinations impossible

Red flags:
  • >2 companions with loyalty tracking
  • >4 possible loyalty values per companion
  • Quests that branch by multiple companion states simultaneously
  
Fix options:
  1. Limit companions to 2 (reduce state space)
  2. Group loyalty into tiers: low/neutral/high (3 values instead of 11)
  3. Create "convergence session" where multiple branches meet
  4. Use linear main quest + branch-specific side quests (reduce state interactions)
```

#### 🟡 **PROBLEM: Faction Reputation Decision Tree Explosion**
Multiple factions with reputation tracking create branching complexity.

```
Campaign with 3 factions:

Faction reputations:
  • Temple: -5 to +5 (11 values)
  • Thieves Guild: -5 to +5 (11 values)
  • Militia: -5 to +5 (11 values)

Possible reputation combinations: 11^3 = 1,331 combinations

Each SESSION branching by:
  • Which factions have quests available (depends on reputation)
  • Which NPCs are allies vs enemies (depends on reputation)
  • Available locations (some faction-controlled)
  
Example:
  SESSION-5 quest availability:
    Temple quest available if reputation >= 1
    Thieves quest available if reputation <= -1
    Militia quest available if reputation >= 2
    
  If all combinations accessible:
    ~80% of reputation combos have at least one available quest
    ~1,064 states with quest branches
    
Status: 🟡 MAINTENANCE NIGHTMARE
        Not impossible, but exhausting to manage

Red flags:
  • >2 factions with reputation tracking
  • Quests with faction reputation gates
  • No convergence between faction branches
  
Fix options:
  1. Limit to 2 factions (reduces combinations to 121)
  2. Use binary faction states (allied/hostile) instead of -5 to +5 scale
  3. Create "faction choice session" where party commits to primary faction
  4. Use faction gates only for ending (not for ongoing session branching)
```

#### 🟠 **PROBLEM: Session Module Interdependency Chains**
Session outcomes cascade through later sessions, creating fragile branching.

```
Session dependency chain:

SESSION-2: Recruit companion choice
  → Affects SESSION-3 quest availability
  → Affects SESSION-4 NPC encounters
  → Affects SESSION-5 dialogue options
  → Affects SESSION-6 ending accessibility

Linear chain: S2 → S3 → S4 → S5 → S6

Change at SESSION-2 affects 4 downstream sessions
  • Testing required: S3 (2 companions), S4 (2 x variations), S5 (2 x variations), S6 (2 x variations)
  • Bug in SESSION-2 may not manifest until SESSION-6
  
Status: 🟠 FRAGILE BRANCHING
        Maintenance burden increases exponentially per session

Red flags:
  • >3 sessions of dependent branching
  • Session outcomes cascade without reconvergence
  • No "sync points" between sessions
  
Fix options:
  1. Add convergence points: Session 3 opens, all companion paths reconverge by Session 4
  2. Limit cascade depth: Session 2 choice only affects Sessions 3-4, not 5-6
  3. Use faction/reputation outcomes instead of companion states (simpler to track)
```

**For Computer Game**:

#### 🔴 **PROBLEM: Playstyle Route × Accessibility Variant Explosion**
Routes + accessibility variants create exponential feature combinations.

```
Game with 3 routes and 3 accessibility types:

Simple multiplication:
  Routes: 3 (Stealth, Combat, Diplomacy)
  Accessibility: 3 (Colorblind, Audio, Motor)
  Combinations: 3 × 3 = 9 feature combinations

Per chapter:
  • CHAPTER-3: Stealth + Colorblind variant needed
  • CHAPTER-3: Stealth + Audio variant needed
  • CHAPTER-3: Combat + Colorblind variant needed
  • ... (9 total variants for each chapter)

Over 4 chapters:
  9 variants × 4 chapters = 36 variant implementations

Content explosion:
  • Base route nodes: 3 routes × 15 nodes = 45 nodes
  • Accessibility variants: 36 implementations
  • Total complexity: 45 + 36 = 81 content pieces to maintain
  
Status: 🔴 FEATURE CREEP
        Accessibility variants shouldn't multiply routes

Issue: Accessibility should be orthogonal to routes
       (i.e., colorblind works in all 3 routes, not as separate variants)
       
Mistake: Treating accessibility variants as route variants
         (this makes them optional/secondary instead of universal)

Fix options:
  1. Implement colorblind overlay in ALL routes (1 implementation, used everywhere)
  2. Implement audio cues in ALL routes (not per-route)
  3. Implement motor controls in ALL routes (not per-route)
  4. Result: 45 base nodes + 3 accessibility systems = 48 complexity (not 81)
```

#### 🟡 **PROBLEM: Route-Exclusive Content Imbalance**
Different routes have vastly different content volumes, creating perceived unfairness.

```
Route content analysis:

Stealth route:
  • CHAPTER-3: 8 nodes (infiltration variants)
  • CHAPTER-4: 5 nodes (boss variants)
  • Total: 13 nodes, 40 minutes playtime
  • Unique content: 13 nodes

Combat route:
  • CHAPTER-3: 4 nodes (combat encounters)
  • CHAPTER-4: 3 nodes (boss fight)
  • Total: 7 nodes, 25 minutes playtime
  • Unique content: 7 nodes

Diplomacy route:
  • CHAPTER-3: 5 nodes (negotiation)
  • CHAPTER-4: 4 nodes (resolution)
  • Total: 9 nodes, 30 minutes playtime
  • Unique content: 9 nodes

Content ratio: 13:7:9 (Stealth has 85% more content than Combat)

Status: 🟡 PERCEIVED IMBALANCE
        Stealth players feel they "got more game"
        Combat players feel they "got less"

Red flags:
  • Content volume ratio >3:1 between routes
  • One route has 50% more encounters than others
  • One route has more boss variants than others
  
Fix options:
  1. Rebalance: Add 5 nodes to Combat route (7 → 12)
  2. Or: Remove 4 nodes from Stealth route (13 → 9)
  3. Verify encounter challenge is equivalent (not just node count)
  4. Ensure boss variants are equally satisfying per route
```

### 6. **Estimate Maintenance Effort**

Calculate work per branch variant:

```
Maintenance effort formula:
  E = S + (B × V × C)
  
  S = Shared node work (write once, maintain everywhere)
  B = Branch-specific node work
  V = Variant work (conditional prose, state changes)
  C = Complexity multiplier (testing, debugging)

Example game:

S (shared): 10 nodes × 2 hrs = 20 hrs (written once, impacts all branches)
B (branch-specific): 12 nodes × 2 hrs = 24 hrs
V (variant prose): 4 variants × 0.5 hrs = 2 hrs
C (complexity): 3 branches, 6 choice points = 18 test combinations

Initial effort: 20 + 24 + 2 = 46 hours

Ongoing maintenance cost (per 1-hour edit in shared content):
  • 1 hour edit in shared node = impacts all 3 branches = 3x review time
  • 1 hour edit in branch-specific = 1 hour per branch = 3 hours
  • Regression testing: 18 combinations must be tested = 18 hours

Total maintenance multiplier: 3x–5x per edit in shared content

Risk assessment:
  • Low risk: <5 branches, depth <5, >50% shared content
  • Medium risk: 5–10 branches, depth 5–8, 30–50% shared content
  • High risk: >10 branches, depth >8, <30% shared content
  
This game: 3 branches, depth 6, 45% shared = MEDIUM RISK

RPG Campaign Maintenance (if [PLATFORM] detected):

TABLETOP:
  • Companion state maintenance: E = N_companions × (N_loyalty_levels × N_quests_gated)
    Example: 3 companions × (11 loyalty levels × 3 quests) = 99 state-quest interactions
  • Faction reputation maintenance: E = N_factions × (N_reputation_levels × N_sessions_affected)
    Example: 3 factions × (11 reputation levels × 4 sessions) = 132 state-session interactions
  • Session interdependency multiplier: × (N_sessions - 1) for cascade effects
    Example: 6 sessions = 5x multiplier on all session changes

COMPUTER GAME:
  • Route maintenance: E = N_routes × N_chapters × N_nodes_per_chapter
    Example: 3 routes × 4 chapters × 5 nodes = 60 route-specific nodes
  • Accessibility multiplier: × N_accessibility_types (but should be 1x if properly orthogonal)
    Correct design: 60 nodes + 3 accessibility systems = 63 complexity
    Bad design: 60 nodes × 3 accessibility = 180 nodes (bloated)
  • Route balance testing: N_routes! × combinations of balance metrics
    Example: 3 routes = 6 route comparison permutations
```

### 7. **Generate Complexity Audit Report**

Create `specs/complexity-audit.md`:

```markdown
## Branch Complexity Audit

**Game**: [NAME]
**Platform**: [Generic / Tabletop-D&D5e / Tabletop-Pathfinder2e / Tabletop-Shadowrun6e / Computer-Game]
**Date**: [ISO]

### Complexity Metrics

| Metric | Value | Limit | Status |
|--------|-------|-------|--------|
| Max depth | 6 | 8 | ✅ OK |
| Max breadth | 3 | 5 | ✅ OK |
| Total branches | 3 | 10 | ✅ OK |
| Possible paths | 4 | 50 | ✅ OK |
| Total nodes | 22 | 100 | ✅ OK |
| Shared % | 45% | >30% | ✅ OK |

**RPG Campaign Metrics** (if applicable):
| Metric | Value | Limit | Status |
|--------|-------|-------|--------|
| Companions with loyalty | 3 | 2 | ⚠️ WARN |
| Loyalty levels per companion | 11 | 5 | ⚠️ HIGH |
| Factions with reputation | 3 | 2 | ⚠️ WARN |
| Session interdependency depth | 5 | 3 | ⚠️ HIGH |
| Playstyle routes | 3 | 3 | ✅ OK |
| Accessibility variants | 3 | 3 | ✅ OK |
| Route content ratio | 13:7:9 | <3:1 | ⚠️ IMBALANCED |

### Branch Structure

```
Shared intro (10 nodes)
├─ Branch A: Help Victor (6 nodes, 2 variants)
├─ Branch B: Betray Victor (3 nodes)
└─ Branch C: Flee (3 nodes)
```

Depth: 6 levels
Breadth: 3 parallel paths at main choice
Branching factor: 3 at NODE-010, 2 at NODE-015 (A only)

**RPG Campaign Structure** (if applicable):
```
SESSION-1 (Shared: 2 nodes)
├─ SESSION-2: Companion Choice (3 branches)
│  ├─ Recruit Theron → loyalty tracking -5 to +5
│  ├─ Recruit Sera → loyalty tracking -5 to +5
│  └─ Solo campaign
├─ SESSION-3-8: Dependent branches (loyalty states cascade)
└─ SESSION-9: Convergence (all paths reconverge for ending choice)

Companion state combinations: 3 paths × 11 Theron loyalty × 11 Sera loyalty = 363 states
```

### Maintenance Effort

- Initial development: ~46 hours
- Per 1-hour shared edit: ~3–5 hours ongoing (testing all branches)
- Branch testing: 18 combinations to verify
- Risk level: MEDIUM

**RPG Campaign Maintenance** (if applicable):
- Companion state testing: 363 combinations (high, but most collapsed by gameplay)
- Faction reputation gating: 132 state-quest interactions (medium, manageable with constraints)
- Session interdependency: 5x multiplier on session changes (high risk for bugs)
- Route imbalance review: Required before shipping (balance check: 13:7:9 should be ≤ 3:1)

### Sustainability Assessment

**Current design**: ✅ SUSTAINABLE
- Depth is manageable (6 levels)
- Branching is controlled (3 at main point, 2 sub-branches)
- Convergence exists (no orphaned paths)
- Shared content is >40% (reduces duplication)

**Growth warning**: If you add more than 5 more choice points,
                    or deepen beyond 10 levels,
                    or increase branches to 6+, consider consolidating.

**RPG Campaign Warnings** (if applicable):
- ⚠️ 3 companions is at the upper limit; adding a 4th will explode state space
- ⚠️ Loyalty levels (-5 to +5 = 11 values) is high; consider collapsing to 3 tiers (low/neutral/high)
- ⚠️ Session interdependency depth 5 is risky; add convergence point after SESSION-5
- ⚠️ Route content imbalance 13:7:9 should be rebalanced to <3:1 ratio

### Recommendations

**Current**: No immediate changes needed

**Future expansion**:
1. If adding side quests, keep them shallow (<3 levels) and reconverge
2. If adding sub-choices, limit to 1–2 per main branch
3. Target <100 total nodes to keep testing manageable
4. Maintain >40% shared content to reduce duplication

**Optimization opportunities**:
- NODE-010 choices could be condensed if variants don't differ substantively
- Consider variable flags for flavor choices instead of node duplication
```

### 8. **Show Tree** (optional with --show-tree)

ASCII tree of complete branch structure:

```
BRANCH TREE

START [shared]
├─ INTRO [shared, 10 nodes]
│
└─ NODE-010 CHOICE: Help / Betray / Flee
   │
   ├─ BRANCH A: Help Victor
   │  ├─ NODE-015 SUB-CHOICE: Violent / Stealth
   │  │  ├─ VARIANT A1: Violent approach
   │  │  │  └─ NODE-020 → NODE-025 [END A1]
   │  │  │
   │  │  └─ VARIANT A2: Stealth approach
   │  │     └─ NODE-020 → NODE-025 [END A2]
   │  │
   │  └─ NOTE: Both A1 and A2 converge at NODE-020
   │
   ├─ BRANCH B: Betray Victor
   │  └─ NODE-016 → NODE-021 → NODE-026 [END B]
   │
   └─ BRANCH C: Flee
      └─ NODE-017 → NODE-022 → NODE-027 [END C]

Convergence points: NODE-020 (A variants merge)
Divergence points: NODE-010 (3-way split), NODE-015 (2-way A only)
Dead-ends: NODE-025 (A1), NODE-025 (A2), NODE-026 (B), NODE-027 (C)
```

### 9. **Convergence Map** (optional with --convergence-map)

Show where branches merge:

```
CONVERGENCE POINTS

NODE-010 [divergence]:
  ├─ Branch A (Help)
  ├─ Branch B (Betray)
  └─ Branch C (Flee)
  
NODE-015 [sub-divergence in A only]:
  ├─ A1 (Violent)
  └─ A2 (Stealth)

NODE-020 [convergence]:
  Branches that merge here:
    ✅ A1 arrives (from NODE-025 variant A1)
    ✅ A2 arrives (from NODE-025 variant A2)
  
  Branches that DON'T merge here:
    ❌ B continues separately
    ❌ C continues separately
  
  Convergence quality: PARTIAL (A variants merge, B and C stay separate)

Assessment: B and C don't reconverge with A
            This is intentional (different ending paths)
            Acceptable design
```

### 10. **Report**

Output `complexity-audit.md` with:
- Complexity metrics (depth, breadth, total nodes, paths)
- Branch structure summary
- Maintenance effort estimate
- Sustainability assessment (sustainable / risky / critical)
- If `--show-tree`: ASCII branch tree
- If `--convergence-map`: Where branches merge/diverge
- If `--estimate-nodes`: Projected node count for full implementation

---

## RPG Campaign Branch Complexity Notes

### Tabletop Campaign Complexity Considerations

**Companion Loyalty State Explosion**:
- Each companion with -5 to +5 loyalty = 11 values
- 3 companions = 1,331 possible loyalty combinations
- Most combinations never reached by actual play (players don't access all state combinations)
- Solution: Collapse loyalty into 3 tiers (low/neutral/high) = 27 combinations instead of 1,331
- Session prep burden: At most 6-8 combinations per session should be prepared (use branching logic)

**Faction Reputation Cascades**:
- Faction reputations are multipliers, not independent states
- 3 factions × 11 reputation levels = 1,331 possible combinations
- Reputation affects: quest availability, NPC reactions, location access, ending options
- Complexity is manageable if: reputation only gates content (yes/no gating), not creates unique branches
- Solution: Use binary faction states (allied/hostile/neutral) for main story, track specific reputation only for ending variants

**Session Interdependency Risk**:
- SESSION-2 choice cascades through SESSION-3, SESSION-4, SESSION-5, SESSION-6 (5 downstream sessions)
- Bug in SESSION-2 logic may not manifest until SESSION-6 (hard to debug)
- Testing burden: Each session must be tested with all states from previous session
- Solution: Add "convergence points" (e.g., "All companions meet at the tavern at SESSION-5" reconverges all paths)
- Safe design: Limit cascade depth to 3 sessions max before reconvergence

**Campaign Module Preparation Scope**:
- Each SESSION needs unique preparation: SESSION-N-BRIEFING.md (player intro) + campaign-guide.md (GM reference)
- If 3 companion paths × 5 sessions = 15 unique session scenarios
- Each scenario needs: unique encounters, NPC states, quest availability
- Maintenance effort: 15 session scenarios × 4-6 hours prep per session = 60–90 hours total

**Recommendations for Tabletop Complexity**:
1. Limit companions to 2 (reduces state space by 50%)
2. Use 3-tier loyalty system: low (-1), neutral (0), high (+1)
3. Add convergence point after SESSION-3 or SESSION-4 (all paths meet, then branch again)
4. Reserve faction reputation only for ending variant (SESSION-8/9), not mid-campaign branching
5. Create "session template" where variable states drive unique content without full rewrite

### Computer Game Route Complexity Considerations

**Playstyle Route Isolation**:
- Each route (Stealth/Combat/Diplomacy) should be fully playable without accessing other routes
- Content per route should be balanced: ideally 1:1:1 ratio, acceptable range <3:1
- Route-exclusive variables must use prefix: $stealth_*, $combat_*, $diplomacy_*
- Avoid: one route having 50% more content than others (creates perceived unfairness)

**Accessibility Variant Integration**:
- Accessibility features should be orthogonal: work in ALL routes simultaneously
- Correct design: 3 routes + 3 accessibility systems = 6 components to maintain
- Incorrect design: 3 routes × 3 accessibility = 9 separate implementations (bloated)
- Each component should be independent: colorblind UI works same in Stealth/Combat/Diplomacy
- Testing matrix: 3 routes × 3 accessibility = 9 paths to QA (manageable)

**Chapter-Based Branching Management**:
- Each chapter (CHAPTER-1 through CHAPTER-4) can branch independently
- Route commitment typically at CHAPTER-2 (permanently select one of 3 routes)
- Post-commitment: CHAPTER-3 and CHAPTER-4 are route-specific
- Each route should have similar depth: if Stealth CHAPTER-3 has 8 nodes, Combat and Diplomacy should have 6-10 nodes

**Feature Creep Prevention**:
- Before adding route variant: ask "Does this apply to all routes or just one?"
- If just one route: it's route-specific content (OK, but balance against other routes)
- If all routes: implement as general feature, not variant (simpler to maintain)
- Example: "Colorblind mode" applies everywhere (implement once), "Stealth takedown" applies only to Stealth (route-specific)

**Recommendations for Computer Game Complexity**:
1. Commit route by CHAPTER-2 (earlier commitment = less content explosion)
2. Keep route-specific content volume within 3:1 ratio (test before shipping)
3. Implement accessibility features as universal systems, not per-route variants
4. Convergence approach: All routes meet at final boss, diverge only in approach/dialogue
5. Create route implementation checklist: each route should have [5 nodes] + [3 encounters] + [1 boss variant]

### Ruleset-Specific Branching Impact

**D&D 5e Mechanics**:
- DC ranges 8–20, ability checks determine outcome
- Advantage/disadvantage states (binary: on/off)
- Branching primarily comes from success/failure on rolls, not branching narrative
- Complexity: Design for both success and failure paths
- RPG modular approach: success path = 2-3 nodes, failure path = 2-3 nodes, converge at next decision

**Pathfinder 2e Mechanics**:
- Critical success/failure/success/failure (4-level outcomes per roll)
- Each outcome can branch differently
- More granular branching: 1 roll can create 4 different paths
- Complexity: More branches but more satisfying (granular failure states)
- Design approach: Ensure each outcome has meaningful content

**Shadowrun 6e Mechanics**:
- Karma/edge pool management (resources decline over campaign)
- Matrix vs Physical world separation (choose one path for operation)
- Hit margin calculations (degree of success matters)
- Complexity: Resources force meaningful choices earlier
- Campaign impact: Early resource usage affects later session availability



**Branching Is Not Inherently Bad**: Games like *Disco Elysium* and *Outer Wilds* have hundreds of nodes with complex branching. The issue is whether you can maintain it.

**Test Matrix Grows Exponentially**: 4 binary choices = 16 paths to test. 8 binary choices = 256 paths. Even moderate branching requires systematic testing.

**Convergence Is Your Friend**: Branches that reconverge let you reduce exponential growth. "All paths lead to this scene" is a powerful design pattern.

**Linear With Side Branches**: Consider a linear main story with optional side quests. Main path is manageable; side content is branchy but isolated.

**Scope Branching Deliberately**: Different games support different branching levels:
- Visual novels: Can handle 100+ nodes, high branching
- Parser IF: Often keep to <50 nodes, moderate branching
- Choice-based IF: Usually 20–80 nodes, controlled branching
- Twine games: Highly variable; depends on target

Know your scope before designing branching.

