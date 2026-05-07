---
description: Choice consequence mapper — visualize how each choice branches story into different outcomes. Track consequences across all branches, detect orphaned choice branches, map consequence chains. For RPG campaigns (tabletop D&D/Pathfinder/Shadowrun and computer game), validates companion loyalty branches, faction reputation decisions, playstyle route-exclusive consequences, and accessibility consistency across variants.
handoffs:
  - label: Check Agency
    agent: speckit.agency
    prompt: After mapping consequences, verify choices actually have meaningful consequences.
    send: true
  - label: Revise Consequences
    agent: speckit.revise
    prompt: Some choice consequences are unclear. Please strengthen outcome differentiation.
    send: true
---

# speckit.consequences

Choice consequence mapper — visualize **how each choice branches into different outcomes**. Tracks consequences across all branches, detects orphaned choices, maps consequence chains (choice → intermediate effect → ending state).

**🎮 RPG Campaign Support**: Validates companion loyalty branches (tabletop: loyalty ±5 gates, faction reputation ±100 payoffs, NPC recruitment timing), playstyle route-exclusive consequences (computer: route variables gated, accessibility consistency across variants), and session/chapter consequence persistence.

## Consequence Principle

**Clear consequences** = Each choice visibly affects story outcome; player can predict/understand result.

**Unclear consequences include**:
- ❌ Choice made, but outcome is identical to other choices
- ❌ Consequence appears late (5+ nodes after choice)
- ❌ Chain of consequences so complex player can't trace it
- ❌ Choice branch leads to dead end (orphaned consequence)
- ❌ Consequence contradicts prior setup (feels arbitrary)

**Valid consequences include**:
- ✅ Immediate effect (visible within 1–2 nodes)
- ✅ Traced chain (choice → NODE-1 change → NODE-3 payoff)
- ✅ Multiple outcome paths (same choice, different consequences per branch)
- ✅ Cumulative consequences (compound across multiple choices)
- ✅ Latent consequences (delayed but foreshadowed)

## User Input

```text
$ARGUMENTS
```

Accepted input:
- Nothing — map all choice consequences across all branches
- Choice ID (e.g., `CH-001`) — trace one choice's consequences
- `--choice-point [NODE_ID]` — analyze all choices at a specific node
- `--branch [BRANCH_ID]` — trace consequences in one branch only

Optional flags:
- `--strict` — flag any consequence appearing >3 nodes after choice
- `--orphaned-only` — show only dead-end branches (no payoff)
- `--show-chains` — display multi-step consequence chains
- `--consequence-only` — ignore neutral branches (show only meaningful differences)

## Pre-Execution Checks

**Extract Platform & Ruleset** (auto-detect RPG context):
- Read `.specify/memory/constitution.md` YAML frontmatter and extract `[PLATFORM]` and `[RULESET]`
- If `[PLATFORM]` = "Tabletop": Set `SESSION.is_rpg = "tabletop"` and load Tabletop consequence model
- If `[PLATFORM]` = "Computer Game": Set `SESSION.is_rpg = "computer"` and load Computer Game consequence model
- If neither detected: Set `SESSION.is_rpg = false` (generic consequence model)
- Store `SESSION.platform` and `SESSION.ruleset` for conditional consequence validation

**Load RPG-Specific Documents** (if platform detected):
- **Tabletop**: Load `specs/companions.md` (loyalty bounds, recruitment gates), `specs/factions.md` (reputation ±100 bounds, faction consequences), `specs/mechanics-[ruleset].md` (approval gates, skill DCs)
- **Computer**: Load `specs/variables.md` (route-specific variable prefixes: $stealth_*, $combat_*, $diplomacy_*), `specs/accessibility.md` (accessibility variant tracking per route)

Proceed with:
1. Load `specs/plan.md`: Branch structure, choice points
2. Load `specs/variables.md`: Variables affected by choices
3. Load all `draft/[ENGINE]/NODE-*.md` files
4. Parse for choice syntax (Ink `*[]`, SugarCube `[[]]`, etc.)
5. Extract variable mutations per branch
6. Identify choice points and their outcomes

## Execution Steps

### 1. **Map Choice Points**

Identify all player choices and their branches:

```
CHOICE POINTS:

CH-001: NODE-010 "Help or Betray Victor?"
  Option A: "Help Victor escape"    → NODE-015 [Branch A]
  Option B: "Betray Victor"         → NODE-016 [Branch B]
  Option C: "Flee without helping"  → NODE-017 [Branch C]

CH-002: NODE-015 "Violent or Stealth?" (Branch A only)
  Option A1: "Use force"            → NODE-020A [Branch A1]
  Option A2: "Sneak approach"       → NODE-020B [Branch A2]

CH-003: NODE-025 "Keep or Release Victor?" (Branch A only)
  Option A1a: "Keep him locked up"  → NODE-030A [Branch A1a]
  Option A1b: "Release him"         → NODE-030B [Branch A1b]
```

### 2. **Track Consequences Per Choice**

For each choice, map immediate and delayed consequences:

```
CH-001 CONSEQUENCES:

Option A (Help Victor):
  ├─ Immediate (NODE-015):
  │  • victor_status = "escaped"
  │  • relationship_marcus += 10
  │  • reputation += 2
  │
  ├─ Short-term (NODE-020):
  │  • city_under_siege = true
  │  • militarization_level = 3
  │
  ├─ Medium-term (NODE-025):
  │  • Ending condition: relationship_marcus > 75 (available)
  │  • Victor appears as ally in NODE-030
  │
  └─ Ending (NODE-FINAL):
     • Ending A: "Redemption" (Victor escaped, city stabilizes)

Option B (Betray Victor):
  ├─ Immediate (NODE-016):
  │  • victor_status = "captured"
  │  • relationship_marcus -= 15
  │  • reputation -= 5 (if betrayal is known)
  │
  ├─ Short-term (NODE-021):
  │  • militia_influence = 5
  │  • player_regarded_as "collaborator"
  │
  ├─ Medium-term (NODE-025):
  │  • Ending condition: relationship_marcus < 50 (available)
  │  • Victor's allies seek revenge
  │
  └─ Ending (NODE-FINAL):
     • Ending B: "Tragedy" (Victor imprisoned, player isolated)

Option C (Flee):
  ├─ Immediate (NODE-017):
  │  • victor_status = "abandoned"
  │  • relationship_marcus = 50 (neutral)
  │  • reputation -= 1 (cowardice)
  │
  ├─ Short-term (NODE-022):
  │  • Safe outside city
  │  • But never resolve Victor's story
  │
  └─ Ending (NODE-FINAL):
     • Ending C: "Escape" (Survive, but unresolved threads)
```

### 3. **Analyze Consequence Clarity**

Measure how clear each consequence is:

```
CLARITY METRICS:

Consequence: choice_A → victor_status="escaped"
  Visibility: Explicit (NODE-015 prose: "Victor flees into darkness")
  Immediacy: 0 nodes (happens immediately)
  Traceability: High (choice → direct result, no intermediate steps)
  Clarity: ✅ EXCELLENT

Consequence: choice_A → reputation += 2
  Visibility: Implicit (only shown in variable, no prose)
  Immediacy: 0 nodes (hidden change)
  Traceability: Medium (player might not realize choice affected reputation)
  Clarity: ⚠️  MODERATE (consider adding prose hint)

Consequence: choice_A → ending_A becomes available
  Visibility: Implicit (only know ending exists when reached)
  Immediacy: 15+ nodes (NODE-015 choice, NODE-FINAL ending)
  Traceability: Complex (multiple choices compound to reach ending)
  Clarity: ⚠️  LOW (add foreshadowing or signpost about ending)
```

### 4. **Detect Consequence Problems**

#### 🔴 **PROBLEM: Identical Outcomes**
Multiple choices lead to the same story state.

```
CH-001 Comparison:

Option A (Help Victor):
  • NODE-015: relationship_marcus = 80
  • NODE-025: victor_status = "escaped"
  • ENDING: Ending A

Option B (Betray Victor):
  • NODE-016: relationship_marcus = 80 ???
  • NODE-025: victor_status = "escaped" ???
  • ENDING: Ending A ???

Problem: Both choices lead to SAME state
         Choice feels illusory (doesn't matter)
         Player won't understand difference between help/betray
         
Status: 🔴 ILLUSORY CHOICE

Fix: Ensure each option has distinguishing consequence
     E.g., Option B should have:
       • relationship_marcus = 35 (not 80)
       • victor_status = "captured" (not "escaped")
       • ENDING B (not A)
```

#### 🟡 **PROBLEM: Delayed Consequence**
Consequence appears so late that choice-outcome connection is unclear.

```
CH-001 (NODE-010): Help Victor

Consequence appears:
  NODE-010: Choice made (Help)
  NODE-015: No visible effect
  NODE-020: No visible effect
  NODE-025: Victor appears (5 nodes later!)
  
Problem: Player chooses to help at NODE-010
         Doesn't see Victor again until NODE-025 (15 nodes later)
         By then, has made other choices (might forget original choice)
         Connection is weak
         
Status: 🟡 DELAYED CONSEQUENCE

Standard guideline:
  • 0–1 nodes: Immediate ✅ (player clearly sees result)
  • 2–3 nodes: Short-term ✅ (still feels connected)
  • 4–5 nodes: Medium ⚠️  (connection getting tenuous)
  • 6+ nodes: Long-term ❌ (feels disconnected; foreshadow needed)

Fix: Either:
  1. Add immediate hint at NODE-015 (Victor's absence is absence felt)
  2. Add intermediate consequence (allies mention Victor at NODE-020)
  3. Move Victor's appearance to NODE-015 or NODE-020
```

#### 🟠 **PROBLEM: Orphaned Choice Branch**
Choice leads to dead-end with no payoff or reconnection.

```
CH-001: "Help or Leave?"

Option A (Help):
  NODE-015 → NODE-020 → NODE-025 → ENDING
  ✅ Leads to ending

Option B (Leave):
  NODE-016 → NODE-021 → NODE-026 → ???
  No ENDING node after NODE-026
  NODE-026: Dead end

Problem: Players who choose B get stuck
         No way forward to ending
         Branch is incomplete
         
Status: 🟠 ORPHANED BRANCH

Fix: Either:
  1. Add NODE-027 (ENDING for this branch)
  2. Merge NODE-026 back to main story (reconvergence)
  3. Make NODE-026 itself a final ending node
```

#### 💨 **PROBLEM: Consequence Chain Too Complex**
Multiple steps between choice and payoff; hard to trace.

```
CH-001: Help Victor

Chain:
  NODE-010: Help Victor chosen
    → victor_status = "escaped"
    → alertness_level += 1
    → city_security += 2
  
  NODE-015: (automatic consequence)
    → IF alertness_level > 0: militia_patrols spawn
    → IF city_security > 1: additional checkpoints
    → IF victor_status = "escaped": THEN bounty_hunters_hired
  
  NODE-020: (cascading consequence)
    → IF bounty_hunters_hired: THEN relationship_marcus affected
    → IF relationship_marcus < 50: THEN Marcus becomes hostile
    → IF Marcus hostile: THEN NODE-025 changes completely
  
  NODE-025: (final consequence)
    → Outcome depends on 3 prior conditional variables

Problem: Help choice → 7 variable mutations across 4 nodes
         With 3 IF statements creating branching logic
         Player can't trace: "Did I cause this by helping, or other choices?"
         
Status: 💨 OVERCOMPLICATED

Fix: Simplify chain
     • Direct: choice → 2–3 immediate consequences (max)
     • Transparent: each consequence clearly labeled
     • Optional: add intermediate consequences IF explicitly called out
```

#### 🟢 **PROBLEM: Consequence Contradicts Setup**
Consequence doesn't match foreshadowing or logical expectation.

```
Setup: NODE-005
  Dialogue: "Marcus is a city detective. He values honesty above all."
  (Implies: betrayal would anger him)

Choice: NODE-010
  "Betray Victor to Marcus"
  Expected consequence: Marcus respects your honesty, relationship ↑
  Logical expectation: Since Marcus values honesty → should like you more

Actual consequence: NODE-016
  relationship_marcus = 35 (decreased!)
  Dialogue: "You're a monster. I don't want to see you again."
  
Problem: Consequence contradicts setup
         If Marcus values honesty, why does he hate you for being honest?
         Feels arbitrary/punitive
         
Status: 🟢 SETUP CONTRADICTION

Fix: Either:
  1. Change setup: Marcus doesn't value honesty → betrayal is fine
  2. Change consequence: Betrayal earns Marcus's respect (honesty was right choice)
  3. Add context: Marcus values honesty WITH Victor, not betrayal OF Victor
     → Change dialogue to: "You betrayed him. He trusted you."
     → Now contradiction resolved (honesty != betrayal of trust)
```

### 4b. **RPG Campaign Consequence Validation** (if platform detected)

#### Tabletop RPG: Companion Loyalty Branches

**Validate companion loyalty consequences**:
- Check each choice affecting companion loyalty (`loyalty(name)` ±1–5 changes)
- Verify loyalty gates appear only after choice (no retroactive loyalty gates)
- Confirm recruitment moments (loyalty ≥ 70) follow companion trust arc
- Validate betrayal consequences (loyalty ≤ -50) appear within 2–3 sessions
- Ensure loyalty changes show prose reaction (NPC dialogue, action change, stat impact)

**Example validation**:
```
SESSION-2: Choice "Trust Mira with secret?"
  Option A: "Tell her everything"
    ├─ mira_loyalty = +3 (now 65)
    ├─ NODE-201: Mira dialogue confirms trust ✅ (immediate)
    └─ SESSION-4: Mira recruitment available (SESSION-4 > SESSION-2, valid delay)

  Option B: "Keep secret"
    ├─ mira_loyalty = 0 (now 62)
    ├─ NODE-202: Mira notices your hesitation ✅ (prose reaction)
    └─ SESSION-4: Mira still available for recruitment (loyalty still 62 ≥ 70? No! 🔴)
    
Problem: Loyalty 62 < 70 recruitment gate, but no consequence choice to break loyalty
         Mira recruitment becomes unreachable after this choice
         
Status: 🔴 LOYALTY GATE UNREACHABLE

Fix: Either:
  1. Lower Mira recruitment gate to 60
  2. Add later choice to increase loyalty back to 70+
  3. Add alternative recruitment path for this branch
```

#### Tabletop RPG: Faction Reputation Branches

**Validate faction reputation consequences** (faction_reputation(name) ±10–100 changes):
- Verify reputation changes align with choice magnitude (small favor = ±10, major alliance = ±50)
- Check faction gates (reputation ≥ 100 for reward, ≤ -100 for enemy status)
- Ensure reputation consequences affect node availability (quest nodes gated by faction rep)
- Validate multiple faction choices don't contradict (can't be +100 with both Mages Guild and Shadow Cabal)

**Example validation**:
```
SESSION-1: Choice "Help Mage Guild infiltrate warehouse?"
  Option A: "Agree to help"
    ├─ faction_reputation(mages_guild) = +50 (now 150)
    ├─ faction_reputation(shadow_cabal) = 0 (unchanged at 50)
    └─ SESSION-2 NODE-203: Mage Guild reward node available ✅

  Option B: "Help Shadow Cabal instead"
    ├─ faction_reputation(shadow_cabal) = +50 (now 100)
    ├─ faction_reputation(mages_guild) = -25 (now 75)
    └─ SESSION-2 NODE-203: Mage Guild reward node still available ⚠️
    
Problem: Choosing Shadow Cabal reduces Mage Guild rep by 25
         But reward node still gates on faction_reputation(mages_guild) ≥ 100
         Node is still reachable (75 < 100) but feels unmeaning
         
Status: ⚠️ WEAK FACTION GATE

Fix: Either:
  1. Increase faction penalty: -50 instead of -25 (now 75, blocks node)
  2. Lower gate threshold: ≥ 75 instead of ≥ 100
  3. Alternative reward node: For Shadow Cabal faction instead
```

#### Tabletop RPG: Campaign Session Continuity

**Validate consequences persist across sessions**:
- Check companion loyalty states carry forward (SESSION-1 loyalty → SESSION-2 initial value)
- Verify faction reputation persists (SESSION-1 rep → SESSION-2 initial value)
- Ensure SESSION-N-BRIEFING.md reflects all prior consequences (who's on your side, who's hostile)
- Validate no "resets" between sessions (loyalty/rep don't reset to 0)

#### Computer Game: Route-Exclusive Consequence Branches

**Validate playstyle route consequences**:
- Check each choice uses route-prefixed variables ($stealth_*, $combat_*, $diplomacy_*)
- Verify route-exclusive consequences don't affect other routes (no $stealth_choice affecting combat route)
- Ensure route-gating is applied correctly (stealth choice blocks combat-only nodes, etc.)
- Validate exclusive consequences persist until CHAPTER-N COMMITMENT lock

**Example validation**:
```
CHAPTER-2: Choice "Infiltrate or fight the guards?"
  Option A: "Sneak in (Stealth route)"
    ├─ $stealth_infiltration_success = true
    ├─ $stealth_guard_alarm = false
    └─ playthrough_route = "STEALTH" ✅ (locked after CHAPTER-2)

  Option B: "Combat (Combat route)"
    ├─ $combat_guards_defeated = true
    ├─ $combat_noise_level = 3
    └─ playthrough_route = "COMBAT" ✅ (locked after CHAPTER-2)

Validation:
  • NODE-304 (CHAPTER-3): "Reinforcements arrive?"
    - Stealth route: IF $stealth_guard_alarm = false: NO reinforcements ✅
    - Combat route: IF $combat_noise_level ≥ 2: reinforcements spawn ✅
    - No cross-route contamination ✅
```

#### Computer Game: Accessibility Variant Consistency

**Validate accessibility variants preserve route consequences**:
- Colorblind mode: Route indicators visible beyond color (shape, pattern, label)
- Audio mode: Route audio cues match text descriptions
- Motor mode: Route commits don't require time-limited inputs or precision actions
- Cognitive mode: Route summary available before final commit

**Example validation**:
```
CHAPTER-2 Route Commit: "Choose your approach"
  
Standard view (all routes):
  [🟢 Green circle] "Stealth approach"
  [🔴 Red circle] "Combat approach"
  [💬 Dialogue bubble] "Diplomatic approach"
  
Colorblind mode:
  [■ Square] "Stealth approach" ✅ (not color-dependent)
  [▲ Triangle] "Combat approach" ✅ (not color-dependent)
  [● Circle] "Diplomatic approach" ✅ (not color-dependent)
  
Audio mode:
  Beep-beep (2 tones) "Stealth approach" ✅ (matches colorblind: 2-sided)
  Beep-beep-beep (3 tones) "Combat approach" ✅ (matches colorblind: 3-sided)
  Beep (1 tone) "Diplomatic approach" ✅ (matches colorblind: round)
  
Motor mode:
  ⚠️ Button timing: 3 seconds to choose ⚠️ (some motor disabilities can't react in time)
  
Status: 🟡 MOTOR MODE NEEDS ADJUSTMENT

Fix: Increase timeout to 10 seconds, or allow keyboard nav without timer
```

### 5. **Generate Consequence Map Report**

Create `specs/consequence-audit.md`:

```markdown
## Choice Consequence Audit

**Game**: [NAME]
**Date**: [ISO]

### Choice Consequence Map

| Choice | Option | Consequence | Immediacy | Clarity | Status |
|--------|--------|-------------|-----------|---------|--------|
| CH-001 | Help | victor=escaped, relationship+10 | 0 nodes | ✅ Explicit | ✅ Pass |
| CH-001 | Betray | victor=captured, relationship-15 | 0 nodes | ✅ Explicit | ✅ Pass |
| CH-001 | Flee | victor=abandoned, reputation-1 | 0 nodes | ⚠️ Implicit | ⚠️ Review |
| CH-002A | Violent | militia_alert+2 | 1 node | ✅ Explicit | ✅ Pass |
| CH-002A | Stealth | militia_alert+0 | 1 node | ✅ Explicit | ✅ Pass |

### Consequence Problems

**🔴 Identical Outcomes** (0):
- None found

**🟡 Delayed Consequences** (1):
- CH-001 Help: Victor payoff appears 5 nodes after choice
  Fix: Add intermediate hint at NODE-015

**🟠 Orphaned Branches** (1):
- CH-001 Flee: NODE-026 leads to dead-end
  Fix: Add NODE-027 or reconverge to main story

**💨 Overcomplicated Chains** (0):
- None found

**🟢 Setup Contradictions** (0):
- None found

### Recommendations

Priority 1: Fix orphaned NODE-026
Priority 2: Add intermediate consequence hint for CH-001 Help
Priority 3: Consider making reputation consequence more explicit
```

### 6. **Show Chains** (optional with --show-chains)

Display multi-step consequence chains:

```
CH-001 HELP: Consequence Chain

NODE-010: Choice "Help Victor"
  ↓ [Direct consequence]
NODE-015: 
  ├─ victor_status = "escaped"
  ├─ relationship_marcus += 10 (now 65)
  ├─ reputation += 2
  │
  └─ [Triggers at NODE-020]
    ├─ Marcus suspicious of you helping prisoner escape
    ├─ IF reputation >= 50: militia doesn't pursue
    ├─ IF reputation < 50: militia pursues
    │
    └─ [Ends at NODE-025]
      ├─ IF militia pursued: bounty on your head → different ending path
      ├─ IF militia didn't pursue: Victor sends message → ally path
      │
      └─ ENDING A or A'
         (Different because of NODE-020 reputation check)

Chain length: 4 nodes (NODE-010 → 015 → 020 → 025 → ENDING)
Complexity: Medium (1 conditional fork)
Clarity: ✅ GOOD (each step builds logically)
```

### 7. **Report**

Output `consequence-audit.md` with:
- Choice-consequence map (all choices, all options, visible consequences)
- Immediacy analysis (how many nodes before consequence appears?)
- Clarity assessment (is connection obvious to player?)
- Problem list (identical, delayed, orphaned, overcomplicated, contradictions)
- If `--show-chains`: Full consequence chains with conditional branches
- If `--orphaned-only`: Only dead-end branches

---

## RPG Campaign Consequence Notes

### Tabletop Campaign Consequences

#### 1. Companion Loyalty as Branching Consequence

Companion loyalty is not a linear slider but a branching consequence system:

**Loyalty Thresholds & Story Impact**:
- **loyalty < -50**: Companion hostile, actively opposes party, may attack
- **-50 ≤ loyalty < -20**: Companion refuses to cooperate, leaves party, may work with enemies
- **-20 ≤ loyalty < 20**: Companion unreliable, follows party but won't take risks, minimum help in combat
- **20 ≤ loyalty < 50**: Companion cooperative, follows orders, standard participation
- **50 ≤ loyalty < 70**: Companion engaged, offers tactical advice, moderate risk-taking
- **70 ≤ loyalty < 100**: Companion loyal, maximum risk-taking, recruitment gates unlock, offers personal quests
- **loyalty ≥ 100**: Companion devoted, personal questline unlocks, relationship endgame available

**Key insight**: Loyalty branches should map to recruitment thresholds, not arbitrary numbers. Design choices that create meaningful loyalty moments (±5–10 per choice), not constant grinding (±1 per choice).

#### 2. Faction Reputation as Gating Mechanism

Faction reputation consequences gate entire questlines:

**Reputation Gates**:
- Mages Guild quest available only if faction_reputation(mages) ≥ 100
- Shadow Cabal quest available only if faction_reputation(shadow) ≥ 80
- City Watch quests unavailable if faction_reputation(watch) ≤ -50 (hostile)

**Design principle**: Each choice affecting faction rep should update affected quest availability. Use faction reputation consequences to signal which questlines are now locked/unlocked.

**Example SESSION-1 to SESSION-2 consequence chain**:
```
SESSION-1 Choice: "Support Mage Guild against Shadow Cabal?"

Consequence: 
  faction_reputation(mages) = +100 (now active: 150)
  faction_reputation(shadow) = -50 (now hostile: 30)

SESSION-2 BRIEFING should state:
  "Mage Guild sees you as ally. Shadow Cabal considers you enemy."

SESSION-2 available quests:
  ✅ Mage Guild: "Guard Mage Tower"
  ❌ Shadow Cabal: "Steal artifact" (reputation too low)
  ✅ City Watch: "Patrol streets" (neutral)
```

#### 3. NPC Recruitment as Consequence Payoff

Companion recruitment should feel like a payoff for prior loyalty-building choices:

**Bad design**: Companion joins after single loyalty choice
- SESSION-1: Choose "Trust companion with secret" → loyalty +5
- SESSION-2: Companion recruited

**Problem**: Player doesn't feel investment; feels random

**Good design**: Companion joins after loyalty arc (3–5 choices building trust)
- SESSION-1: "Share your fears" → loyalty +5 (now 55)
- SESSION-2: "Defend them from suspicion" → loyalty +10 (now 65)
- SESSION-3: "Tell them secret" → loyalty +5 (now 70) → Recruitment available
- SESSION-4: Companion joins with dialogue acknowledging trust arc

**Key**: Make recruitment consequences feel earned, not random.

#### 4. Session-to-Session Consequence Persistence

Ensure no "resets" between sessions:

**Bad design**: Companion loyalty resets between sessions
```
SESSION-1 Choice: "Trust companion"
  → loyalty = +10 (now 65)

SESSION-2 NPC dialogue:
  "I barely know you." (as if loyalty was reset to 0)
  
Problem: Consequence doesn't persist; player feels betrayed
```

**Good design**: Loyalty carries forward with prose acknowledgment
```
SESSION-1 Choice: "Trust companion"
  → loyalty = +10 (now 65)

SESSION-2 NPC dialogue:
  "After what you told me, I know I can trust you."
  (Acknowledges prior loyalty choice)
```

#### 5. Campaign-Level Consequences (Multi-Session Impact)

Some consequences span entire campaign:

**Example**: Killing a key NPC in SESSION-2
- Immediate (SESSION-2): NPC is dead, questline blocked
- Short-term (SESSION-3): Their allies are hostile
- Medium-term (SESSION-4): Bounty hunters pursue party
- Long-term (SESSION-5+): Ending variations based on who was killed

**Best practice**: Design choice consequences across 3–5 sessions, not within single session.

### Computer Game Route Consequences

#### 1. Route-Exclusive Consequences Using Prefixed Variables

Each route should have isolated consequences using prefixed variables:

**Stealth Route**:
```
$stealth_alert_level = 0 (cameras don't see you)
$stealth_noise = low
$stealth_shortcuts_unlocked = true
```

**Combat Route**:
```
$combat_alarm_triggered = false
$combat_reinforcements_count = 0
$combat_difficulty_level = 2
```

**Diplomacy Route**:
```
$diplomacy_reputation(npc_name) = +50
$diplomacy_guard_bribed = true
$diplomacy_alternative_exit = true
```

**Design principle**: Use prefixed variables so consequences can't leak between routes. A stealth choice never affects `$combat_alarm_triggered`.

#### 2. Route Commitment as Consequence Lock

After CHAPTER-2, route choice should be irreversible:

```
CHAPTER-1: Can still switch routes (variables are exploratory)
  - $stealth_alert_level can change
  - $combat_difficulty can adjust
  - $diplomacy_reputation can shift

CHAPTER-2: Final choice commits to route
  - playthrough_route = "STEALTH" (locked)
  - All subsequent chapters use route-specific consequences

CHAPTER-3+: No switching allowed
  - Stealth route: consequences only use $stealth_* variables
  - Combat route: consequences only use $combat_* variables
  - Diplomacy route: consequences only use $diplomacy_* variables
```

#### 3. Accessibility Variant Consistency

Accessibility variants must preserve route consequences:

**Colorblind mode**: Route choices visible via text labels, not just colors
**Audio mode**: Route audio cues (beeps/tones) consistent with text (e.g., 3 tones = 3rd route option)
**Motor mode**: Route commits don't require time-limited inputs
**Cognitive mode**: Route summaries available before commit

**Example consequence that fails accessibility**:
```
CHAPTER-2 Route Choice:
  [🟢 Green box] Stealth (color-coded, fails colorblind)
  [🔴 Red box] Combat (color-coded, fails colorblind)
  Timer: 3 seconds (fails motor, fails cognitive)

Fixed version:
  [■ STEALTH] (shape + text, passes colorblind)
  [▲ COMBAT] (shape + text, passes colorblind)
  [NO TIMER] (passes motor, passes cognitive)
```

#### 4. Route Convergence Consequences

Some consequences bring routes back together:

```
CHAPTER-1: Three routes diverge
  - Stealth: Avoid guards, take secret path
  - Combat: Fight guards, take main path
  - Diplomacy: Bribe guards, take guarded path

CHAPTER-2: Routes converge at same location (but with different states)
  - Stealth: No one knows you entered
  - Combat: Everyone knows you're here
  - Diplomacy: Guards are watching but not hostile

CHAPTER-3: Converged point leads to same ending, but with route-specific consequences
  - Stealth consequence: [Play as undetected quest]
  - Combat consequence: [Respond to hostility]
  - Diplomacy consequence: [Pay bribe or negotiate]
```

**Design principle**: Converging routes is OK if each has meaningful branch consequences leading into convergence point.

### Best Practices

**Immediate Consequences (0–1 nodes)**:
- Use for obvious cause-effect (choose help → person helped)
- Make explicit in dialogue or visible game state change
- Player immediately sees result of their choice

**Short-term Consequences (2–3 nodes)**:
- Introduce new challenges or opportunities
- Foreshadow with NPC dialogue or narrative hint
- Still feels clearly connected to original choice

**Medium-term Consequences (4–5 nodes)**:
- Require foreshadowing or intermediate callback
- Introduce new choices that build on original consequence
- "Compound" consequences work here (choice A + choice B = new outcome)

**Long-term Consequences (6+ nodes)**:
- Must be heavily foreshadowed
- Use intermediate consequences to maintain connection
- Consider "echo" moments (NPC reminds player of original choice)

**Consequence Visibility**:
- ✅ Explicit consequences: Shown in prose, NPC dialogue, or gameplay change
- ⚠️ Implicit consequences: Only in variables, not visible to player
- ❌ Hidden consequences: Player never learns about it

**Consequence Chains**:
- Keep to <4 steps (choice → effect → effect → payoff)
- Each step should be traceable by player
- Limit conditional branches (max 2–3 IF statements per chain)



**Consequences Should Be Visible**: Players won't feel agency if consequences happen "under the hood." Make them explicit in prose, NPC dialogue, or gameplay changes.

**Timing Matters**: 0–2 nodes after choice = feels like direct consequence. 5+ nodes = feels like coincidence.

**Consequences Can Be Conditional**: Same choice can have different outcomes per branch (e.g., Help Victor → escapes if militia alert is low, captured if alert is high). This is valid; just ensure each possibility is traceable.

**Cumulative Consequences**: Different choices can compound (choice A + choice B = different outcome than A alone or B alone). This is good design; just keep chains to <4 steps so players can follow.

**Foreshadow Delayed Consequences**: If a consequence appears 5+ nodes after choice, foreshadow it. Have an NPC mention it, or show the setup for it, so player understands the connection.

