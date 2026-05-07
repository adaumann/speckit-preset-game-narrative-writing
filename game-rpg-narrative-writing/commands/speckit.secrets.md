---
description: Secret content tracker — map achievements, hidden content, easter eggs. Verify all secrets are discoverable, reachable, and properly documented.
handoffs:
  - label: Check Agency
    agent: speckit.agency
    prompt: After mapping secrets, verify secret choices have meaningful consequences.
    send: true
  - label: Revise Secrets
    agent: speckit.revise
    prompt: Some secrets need better discovery hints. Please add foreshadowing.
    send: true
---

# speckit.secrets

Secret content tracker — map **achievements, hidden content, easter eggs, secret endings, RPG-specific secrets**. Verify all secrets are discoverable, reachable, properly documented, and balanced in unlock difficulty.

## Secrets Principle

**Good secrets** = Discoverable for attentive players; optional (not required); rewarding to find; properly documented in external guide if needed.

**For RPG campaigns** (Tabletop & Computer):
- Secrets must respect session/route pacing (Tabletop) or playstyle balance (Computer)
- Achievement unlocks should feel rewarding without breaking campaign flow
- Hidden scenes must fit companion/faction/ruleset context
- Easter eggs should reward deep engagement with world or mechanics

**Bad secrets include**:
- ❌ Impossible to discover (no hint anywhere)
- ❌ Inaccessible by design (requires code modification)
- ❌ Required for "real" ending (frustrates players who miss them)
- ❌ Undocumented (players don't know they exist)
- ❌ Unfair locks (achievement requires frame-perfect timing)
- ❌ [Tabletop] Breaks session structure (secret spanning 10 sessions disrupts pacing)
- ❌ [Computer] Inaccessible on one playstyle route (Combat players miss entirely)

**Valid secrets include**:
- ✅ Hinted but non-obvious (attentive player might find)
- ✅ Optional alternate content (doesn't gate main story)
- ✅ Multiple unlock paths (can reach same secret via different choices)
- ✅ Proportional reward (difficulty matches value)
- ✅ Discoverable in new game+ (if design supports replay)

## User Input

```text
$ARGUMENTS
```

Accepted input:
- Nothing — map all secrets (achievements, hidden content, easter eggs)
- `--achievement` — list only achievements
- `--hidden-content` — list only hidden scenes/endings
- `--easter-eggs` — list only easter eggs and references
- `--secret [SECRET_ID]` — analyze one secret only

Optional flags:
- `--reachability` — verify each secret can be unlocked
- `--hints-check` — verify each secret has clue to unlock
- `--difficulty-map` — categorize secrets by unlock difficulty
- `--show-unlock-paths` — display all ways to unlock each secret

## Pre-Execution Checks

**RPG Platform & Ruleset Detection** (NEW for RPG support):
- Extract `[PLATFORM]` from `constitution.md` § III (Platform-Genre Binding):
  - `PLATFORM: tabletop` → Set `SESSION.is_rpg = true`, `SESSION.platform = "tabletop"`
  - `PLATFORM: computer` → Set `SESSION.is_rpg = true`, `SESSION.platform = "computer"`
  - Otherwise → Set `SESSION.is_rpg = false`
- Extract `[RULESET]` from `constitution.md` § VIII (System & Ruleset):
  - If present: Set `SESSION.ruleset = "[D&D 5e|Pathfinder 2e|Shadowrun 6e]"` for conditional guidance
  - If not present (generic narrative): `SESSION.ruleset = null`

**RPG Secret Context** (conditional on `SESSION.is_rpg = true`):
- **Tabletop**: Load `specs/plan.md` (session structure), `specs/mechanics-[RULESET].md` (ruleset secrets like stat blocks), campaign-pacing-guide.md (where secrets fit in campaign arc)
- **Computer**: Load `specs/locations.md`, `specs/characters/[PLAYSTYLE]` (how secrets affect route progression), accessibility-features.md (secret accessibility)

1. Load `specs/secrets-template.md` or extract from spec.md (Secret Registry)
2. Load `specs/plan.md`: Branch structure for reachability
3. Load all `draft/[ENGINE]/NODE-*.md` files
4. Load `specs/variables.md`: Variables that unlock secrets
5. Parse for conditions that trigger hidden content

## Execution Steps

### 0. **RPG Secret Categories** (if `SESSION.is_rpg = true`)

**Tabletop RPG Secrets** (if `SESSION.platform = "tabletop"`):
- **Session Achievements**: Unlock within a single session (e.g., "Perfect Encounter" = no party damage in combat)
- **Campaign Achievements**: Multi-session unlocks (e.g., "Faction Champion" = reach +100 faction rep by S8)
- **Companion Secrets**: Hidden scenes/branching based on companion approval levels or relationship milestones
- **Ruleset Easter Eggs**: References to ruleset mechanics (D&D 5e: crit table reference, PF2e: degree of success joke, SR6e: hacker slang)
- **Secret Loot/Encounters**: Hidden enemies, items, or locations only accessible via specific actions
- **Campaign-Prep Secrets**: Information revealed in campaign-guide.md or SESSION-N-BRIEFING.md that adds depth (house rule implications)

**Computer Game Secrets** (if `SESSION.platform = "computer"`):
- **Route-Exclusive Secrets**: Hidden in only one playstyle (e.g., Combat-only dialogue with a general, Exploration-only hidden shrine)
- **Playstyle Achievements**: Balance achievements across routes (e.g., "Diplomat" = complete Dialogue route with 0 combat deaths)
- **Accessibility Secrets**: Reward players who use accessibility features (e.g., "Colorblind Mode Master" = discover all colored items using colorblind descriptions)
- **Convergence Point Secrets**: Hidden scenes at story convergence points (unlocked via specific previous choices)
- **Difficulty Scaling Secrets**: Unlock only on Hard mode or only on Easy mode
- **Speedrun/Challenge Secrets**: Achievement for completing without using certain mechanics

### 1. **Define Secret Registry** (Generic + RPG)

From template or spec, categorize all secrets:

```
SECRET REGISTRY:

ACHIEVEMENTS:
  ACH-001: "Redeemed Victor"
    Unlock: Reach Ending A (Victor escaped + relationship_marcus > 75)
    Reward: Achievement badge
    Description: "Helped Victor escape and earned Marcus's respect"
  
  ACH-002: "Betrayer"
    Unlock: Reach Ending B (Victor captured)
    Reward: Achievement badge
    Description: "Betrayed Victor to the militia"
  
  ACH-003: "Speedrunner"
    Unlock: Complete game in <20 minutes
    Reward: Achievement badge
    Description: "Completed the game in record time"

HIDDEN CONTENT (scenes):
  HID-001: "Victor's Letter"
    Unlock: Ending A + check specific location (NODE-030 secret passage)
    Reward: Additional scene (1,000 words)
    Description: "Discover a letter Victor left for you"
    Gating: Optional; doesn't affect main ending
  
  HID-002: "Marcus Betrayal"
    Unlock: Ending B + high militia_influence
    Reward: Alternate scene NODE-025 (different dialogue)
    Description: "Marcus confronts you about your betrayal"

EASTER EGGS:
  EGG-001: "Hidden NPC"
    Unlock: Find specific item in NODE-020, examine it
    Reward: Cameo appearance of developer
    Description: "Developer appears as background NPC"
  
  EGG-002: "Tribute Reference"
    Unlock: Name your character after [AUTHOR]
    Reward: Dialogue reference
    Description: "NPCs recognize your name (developer tribute)"
  
  EGG-003: "Speed Run Reference"
    Unlock: Visit specific nodes in order NODE-005 → 010 → 015 → 020
    Reward: Easter egg dialogue
    Description: "NPC acknowledges your 'efficiency'"

SECRET ENDINGS:
  END-SEC-001: "True Ending"
    Unlock: Reach Ending A + unlock HID-001 + find secret item
    Reward: Final alternate ending (3,000 words)
    Description: "Discover what really happened"
    Gating: Requires multiple secrets
```

### 2. **Analyze Secret Discoverability**

Rate how easy each secret is to find:

```
DISCOVERABILITY SCALE:

1. OBVIOUS (Explicitly mentioned)
   → Player will find it
   
2. CLEAR (Strong hint provided)
   → Attentive player will find it
   
3. MODERATE (Subtle hint exists)
   → Player might find it on 2nd playthrough
   
4. OBSCURE (Requires experimentation)
   → Player must explore to find
   
5. IMPOSSIBLE (No hint)
   → Requires guide or luck

Example secrets:

ACH-001 (Redeemed Victor):
  Hint: Constitution describes "Redemption ending" as goal
  Discoverability: 2 (CLEAR)
  Expected finder rate: 70%+ of players

HID-001 (Victor's Letter):
  Location: NODE-030 secret passage (not labeled)
  Hint: Marcus mentions "checking the old safehouse"
  Discoverability: 3 (MODERATE)
  Expected finder rate: 30–40% of attentive players

EGG-002 (Name Reference):
  Unlock: Name character "Stephen King"
  Hint: None (pure Easter egg)
  Discoverability: 5 (IMPOSSIBLE without guide)
  Expected finder rate: 1–5% (accidental)
```

### 3. **Verify Reachability**

Trace whether each secret can actually be unlocked:

```
SECRET: HID-001 "Victor's Letter"

Unlock condition: 
  Ending A (Help Victor) 
  + relationship_marcus > 75
  + Discover secret passage NODE-030

Reachability analysis:

Path to Ending A:
  NODE-010: Help Victor ✅ (choice available)
  NODE-015: Violent approach ✅ (choice available)
  NODE-020: Execute escape ✅ (NODE exists)
  NODE-025: Victory achieved ✅ (NODE exists)
  Ending A reached ✅ POSSIBLE

Path to relationship_marcus > 75:
  NODE-010: Help Victor (+15) → 65 total
  NODE-015: No change → 65 total
  NODE-020: Execute perfectly (+10) → 75 total
  CHECK: relationship_marcus = 75 ✅ REACHED

Path to NODE-030 secret passage:
  NODE-025 → NODE-030 ✅ NODE exists
  BUT: Passage marked as [SECRET - no description]
  Question: Is passage actually discoverable in-game?
  
Investigation:
  • NODE-030 prose: "The safe house is empty."
  • No indication of passage
  • No mechanic to "examine walls"
  • No NPC dialogue mentions it
  
Verdict: 🔴 UNREACHABLE (hidden too well; player can't find)

Fix: Either:
  1. Add passage hint in NODE-030 prose
  2. Add examine mechanic (if game supports it)
  3. Have Marcus mention it at NODE-025
  4. Mark as 6/10 difficulty (requires guide)
```

**Tabletop RPG Reachability** (if `SESSION.is_rpg = true` and `SESSION.platform = "tabletop"`):

For Tabletop secrets, trace through the session structure and ruleset mechanics:

```
SECRET: "Faction Champion" achievement
Unlock: Faction_Reputation ≥ 100 by end of Session 8

Reachability check:
  Session 2: +15 reputation → 15 total
  Session 4: +20 reputation → 35 total
  Session 5: +25 reputation → 60 total (choice point: can branch to -20 if player betrays)
  Session 7: +30 reputation → 85–90 total (depends on S5 choice)
  Session 8: +10 reputation → 95–100 total (tight requirement)

Verdict: BARELY REACHABLE (requires good choices in S5 and S7)
         Player must reach S8 in campaign. Not accessible if campaign ends early.
```

**Computer Game Reachability** (if `SESSION.is_rpg = true` and `SESSION.platform = "computer"`):

For Computer secrets, verify they're accessible on all playstyle routes:

```
SECRET: "Diplomat" achievement
Unlock: Complete Dialogue route with 0 combat deaths

Reachability per route:
  ✅ Dialogue route: Can complete without combat → REACHABLE
  ❌ Combat route: Forced combat encounters → UNREACHABLE
  ❌ Exploration route: Some puzzles trigger combat → UNREACHABLE
  
Verdict: ROUTE-EXCLUSIVE (only Dialogue players can get this)
         Is this intentional? If not: Add dialogue-only path to other routes
```

### 4. **Detect Secret Problems**

#### 🔴 **PROBLEM: Impossible to Discover**
Secret has no hint; requires blind luck or guide.

```
EGG-001: "Hidden NPC"
  Unlock: Find NPC in NODE-020 crowd
  Description: Examine 50 background NPCs to find developer cameo
  
Problem: 
  • No hint that Easter egg exists
  • No indication which NPC is special
  • Requires guide or exhaustive testing
  • Player won't discover organically
  
Status: 🔴 IMPOSSIBLE (requires guide)

Assessment: Is this acceptable?
  ✅ YES if: You've documented it in FAQ/guide
  ❌ NO if: You expect players to find it themselves
```

#### 🟡 **PROBLEM: Inaccessible by Design**
Secret requires mechanical action game doesn't support, or is locked behind unwinnable state.

```
HID-002: "Marcus Betrayal" alternate scene

Unlock: Ending B + relationship_marcus > 50

But trace the variables:
  NODE-010: Betray Victor → relationship_marcus = 35
  NODE-016: Continued betrayal → relationship_marcus = 30
  NODE-021: Final betrayal → relationship_marcus = 25
  
Final state: relationship_marcus = 25

Unlock requires: relationship_marcus > 50
Final state is: 25

Problem: Impossible to satisfy both conditions
         To reach Ending B, you must betray (lowering relationship)
         To unlock secret, you need high relationship
         These are contradictory
         
Status: 🟡 INACCESSIBLE (contradictory conditions)

Fix: Either:
  1. Change unlock: Ending B + relationship_marcus < 50 (matches betrayal)
  2. Add alternate path: Ending B + high militia_influence (different variable)
  3. Allow neutral path to Ending B (don't lower relationship)
```

#### 🟠 **PROBLEM: Required for Main Content**
Secret is gated behind obscure unlock; players think they're missing "real" ending.

```
END-SEC-001: "True Ending" secret

Description: "Real story is revealed only in True Ending"
Unlock: Reach Ending A + unlock 5 hidden scenes + find 3 collectibles

Problem:
  • Players reach Ending A (think they're done)
  • Realize there's a "True Ending" (feels incomplete)
  • Must unlock 5 hidden scenes (significant replay burden)
  • Feels mandatory, not optional
  
Status: 🟠 GATING ISSUE

Question: Is this design intentional?
  ✅ YES if: Game is designed as collectathon; players expect this
  ✅ YES if: Documentation clearly indicates "True Ending is bonus"
  ❌ NO if: Players think Ending A is "the" ending and feel cheated

Fix: Either:
  1. Clearly mark in opening: "There are 3+ endings; collect secrets to unlock all"
  2. Make "True Ending" fully optional (doesn't invalidate Ending A)
  3. Reduce unlock requirements (make it less burdensome)
```

#### 💨 **PROBLEM: Secret Not Documented**
Developer knows about secret, but hasn't documented it for guide/wiki.

```
Secret: "Alternative NODE-020 scene if you find hidden item"

Status:
  • Secret exists in code
  • Discoverable by player (with effort)
  • BUT: Not in FAQ, guide, or achievement list
  • Player doesn't know it exists even after finding it
  
Impact:
  • Player thinks they found a bug
  • Posts about it online ("Is this intentional?")
  • Community speculates on meaning
  • Developer confusion: "Yes, that's a secret!"
  
Status: 💨 UNDOCUMENTED

Fix: Add to FAQ or create "Secrets & Easter Eggs" wiki page
```

#### 🟢 **PROBLEM: Unfair Unlock**
Secret requires mechanical execution that's frustrating or frame-perfect.

```
ACH-003: "Speedrunner"
  Unlock: Complete game in <20 minutes

Implementation:
  • Requires skipping all dialogue
  • Mandatory cinematics total 2 minutes
  • Combat encounters have no skip
  • Result: Actual speedrun requires ~24 minutes
  • Speedrunner achievement: Impossible with current design
  
Status: 🟢 UNFAIR (requires external tools or code modification)

Fix: Either:
  1. Adjust timer: <25 minutes (realistic with skips)
  2. Add speedrun mode (skip cutscenes)
  3. Remove if achievement isn't core to design
```

#### 🟣 **PROBLEM (Tabletop): Secret Breaks Session Flow**

```
SECRET: "Perfect Session" achievement
Description: No party member takes damage in combat across entire session
Problem:
  • Session 5 has 3 challenging combat encounters
  • "Perfect" = extremely difficult, feels punitive
  • Breaks session pacing (players overly cautious)
  • Unlocked only by top-tier optimized builds
  
Status: 🟣 SESSION FLOW ISSUE (Tabletop)

Verdict: Is this intentional?
  ✅ YES if: Hardcore players love optimization challenges
  ❌ NO if: Casual players feel excluded

Fix: Either:
  1. Change to "No NPC deaths" (more forgiving)
  2. Add to Newgame+ only (doesn't affect first playthrough)
  3. Make optional difficulty setting (challenge mode)
```

#### 🟠 **PROBLEM (Computer): Route Exclusivity**

```
SECRET: "Hacker Master" achievement
Description: Unlock all hacker-specific skills in one playthrough
Problem:
  • Hacker skills only appear in Matrix route
  • Combat/Exploration routes have no access to hacker skills
  • Achievement impossible for 2/3 of playstyles
  
Status: 🟠 ROUTE EXCLUSIVITY (Computer)

Question: Is this designed as route-exclusive?
  ✅ YES if: Marketing says "Each route has unique secrets"
  ❌ NO if: Players expect achievements accessible to all playstyles

Fix: Either:
  1. Document in game: "Route-exclusive achievements exist"
  2. Create equivalent achievements per route (Hacker Master, Combat Master, Explorer Master)
  3. Make skills accessible across routes (via tutorial or optional training)
```

#### 🔵 **PROBLEM (RPG): Companion/Faction Requirements**

#### 🔵 **PROBLEM (RPG): Companion/Faction Requirements**

```
SECRET: "True Companion" hidden scene
Unlock: Companion joins by Session 3 + approval reaches 100 by Session 5

Problem trace (Tabletop):
  Companion joins Session 3 ✅
  Approval starts at 0
  Available approval gain: S3 (+20), S4 (+30), S5 (+40) = 90 total
  Required: 100 by S5
  
Verdict: 🔵 BARELY UNREACHABLE (10 points short by design)
         Players can reach 90 only. Feels like bug ("Almost there!")

Check: Did designer intend this as impossible for first playthrough?
  If game has Newgame+ with carryover: ✅ Acceptable (unlock in NG+)
  If not: ❌ Fix by adding +10 approval source or lowering requirement to 90
```

```
SECRET: "Faction Betrayer" alternative ending
Unlock: Faction reputation < -50

Problem trace (Tabletop):
  Session 2: Faction intro +0 (neutral state)
  Session 3: Player can choose to help enemy faction (-30)
  Session 4: -20 penalty for warehouse sabotage
  Session 5: Campaign ends
  
Result: Minimum rep = -50 exactly
        Secret requires < -50 (strictly less than)
        Unlocked: Never (requires extra betrayal)
        
Status: 🔵 OFF-BY-ONE ERROR

Verdict: Change unlock to "≤ -50" or add one more betrayal opportunity
```

### 5. **Analyze Unlock Paths** (Generic + RPG)

Map multiple ways to reach same secret:

```
SECRET: HID-001 "Victor's Letter"

Unlock path 1 (Primary):
  NODE-010: Help Victor
  → NODE-015: Violent approach
  → NODE-020: Perfect execution
  → Ending A (relationship > 75)
  → NODE-030: Find secret passage
  
Unlock path 2 (Alternate):
  NODE-010: Help Victor
  → NODE-015: Stealth approach
  → NODE-020: Perfect execution
  → Ending A (relationship > 75)
  → NODE-030: Find secret passage
  
Unlock path 3 (New Game+):
  (If game supports carry-over)
  Second playthrough: Skip to NODE-025
  → Ending A (relationship automatically high)
  → NODE-030: Find secret passage

Analysis:
  • 2–3 discovery paths (good)
  • All require Ending A (single main path)
  • Secret passage is bottleneck (same location every time)
  
Accessibility: MODERATE (not too easy, not impossible)
```

**Tabletop RPG Unlock Path Analysis** (if `SESSION.is_rpg = true` and `SESSION.platform = "tabletop"`):

```
SECRET: "Faction Champion" achievement
Faction_Reputation ≥ 100

Unlock paths by session:
  Path A: All helper actions (S2→S8 consistently +faction)
    Result: 100+ reputation by S8, possibly earlier
    
  Path B: Balanced choices (S2 help, S4 neutral, S5 help)
    Result: 60–80 reputation by S7, need S8 to finish
    
  Path C: Antagonistic→Redemption (S2–S4 oppose, S5–S8 help)
    Result: Harder recovery, reaches 100 only if all S6–S8 choices are correct
    
Analysis:
  • Path A (pure helper): Easiest, ~3 playstyles out of 5 discover
  • Path B (mixed): Moderate, ~2 playstyles
  • Path C (redemption): Hardest, <1 playstyle (designed as "rare")
  
Balancing: Check that achievement is reachable across multiple party builds
           (e.g., Combat-focused vs. Dialogue-focused characters)
```

**Computer Game Unlock Path Analysis** (if `SESSION.is_rpg = true` and `SESSION.platform = "computer"`):

```
SECRET: "All Routes" achievement
Unlock: Complete Dialogue, Combat, and Exploration routes in one playthrough

Unlock paths:
  Path 1: Dialogue→Combat (converge at final choice)
    Can reach both routes via different S4–S7 choices
    Then: Exploration branch locks out Combat reqs
    
  Path 2: Exploration→Dialogue (converge earlier)
    Can reach both via S2–S4 choices
    Then: Combat route locked by item availability
    
Analysis:
  • Mutually exclusive routes: Can player actually unlock all three?
  • Or: Designed for Newgame+ with carryover?
  
Verdict: If exclusive → Achievement impossible in single playthrough (verify design intent)
         If carryover exists → Mark as Newgame+ challenge
```

### 6. **Tabletop Campaign Secret Model** (if `SESSION.is_rpg = true` and `SESSION.platform = "tabletop"`)

This model integrates secrets into the campaign progression and creates player-facing documentation:

**Campaign Secret Impact Tracking**:
- Secrets that affect SESSION-N-BRIEFING.md (players see hints about what's possible)
- Secrets that lock behind faction reputation (announced in campaign-guide.md house rules)
- Secrets that require companion approval thresholds (companion system details in campaign-guide.md)
- Secrets that gatekeep alternative encounters (appear in encounter CR calibration)

Example integration:

```
SECRET: "Betrayal Ending" alternative conclusion
Triggers: Faction_Reputation < -50 by final session

Campaign Documentation Impact:
  • campaign-guide.md § VI (Faction Mechanics): "Extreme faction opposition changes final encounter"
  • SESSION-9-BRIEFING.md: "Warning: Your faction standing critically low. Final scene differs based on reputation"
  • Encounter CR sheet: Mark final encounter with [FACTION_DEPENDENT: +2 CR if rep < -50]
  
Player prep required:
  • GM notes in SESSION-9 should telegraph faction consequences
  • Party should know "faction actions have endings impact"
```

**Secret Timeline Integration**:
- Map each secret to the session(s) in which it becomes discoverable
- Verify no secret requires >4 sessions of play (exceeds typical campaign commitment)
- Flag secrets that span 10+ sessions as "campaign-arc-long" (rare design choice)

### 7. **Computer Game Secret Model** (if `SESSION.is_rpg = true` and `SESSION.platform = "computer"`)

This model routes secrets across playstyle routes and enforces accessibility:

**Route-Gated Secret Tracking**:
- Secrets accessible only to Combat route (e.g., "General's Strategy" dialogue)
- Secrets accessible only to Dialogue route (e.g., "Motive Revelation")
- Secrets accessible only to Exploration route (e.g., "Hidden Shrine")
- Secrets accessible to multiple routes (e.g., item discovery visible in all)

**Playstyle Balance Check** (route imbalance limit: <3×):
```
Route Secret Count:
  Combat: 12 secrets
  Dialogue: 8 secrets
  Exploration: 5 secrets
  
Imbalance: 12÷5 = 2.4× (acceptable, under 3× limit)

If imbalance > 3×: Add more secrets to under-represented route
```

**Accessibility-First Secret Unlocks**:
- All timed secret challenges must have non-timed alternative (puzzle mode, exploration mode)
- Color-based secrets must have alternative reveals (symbol-based, audio description)
- Fine motor secrets (multi-tap, rapid input) must have simplified unlock
- Cognitive accessibility: Secrets must be discoverable without perfect memory

Example accessible secret:

```
SECRET: "Color Prism" item (unlocks color-specific path)

Base discovery (Combat route): 
  Timed challenge: Dodge 5 colored attacks in 10 seconds
  
Accessibility variants:
  • Colorblind mode: Symbol detection (triangle, square, circle) instead of colors
  • Audio accessibility: Beep patterns indicate attack type instead of colors
  • Motor accessibility: Single-tap vs. rapid-tap option (removes speed requirement)
  • Cognitive accessibility: Hint system shows next attack 2 seconds early
  
Result: All playstyles and accessibility modes can discover "Color Prism"
```

### 8. **Generate Secrets Audit Report** (Generic + RPG) (Generic + RPG)

Create `specs/secrets-audit.md`:

```markdown
## Secret Content Audit

**Game**: [NAME]
**Date**: [ISO]

### Secret Inventory

| Secret | Type | Unlock Difficulty | Discoverable? | Reachable? | Documented? | Status |
|--------|------|------------------|---------------|-----------|------------|--------|
| ACH-001 | Achievement | Easy | ✅ Clear | ✅ Yes | ✅ Yes | ✅ Pass |
| HID-001 | Hidden Scene | Hard | ⚠️ Moderate | ❌ No | ✅ Yes | ❌ Fail |
| EGG-002 | Easter Egg | Impossible | ❌ Impossible | ✅ Yes | ❌ No | ⚠️ Warn |
| END-SEC-001 | Secret Ending | Very Hard | ⚠️ Moderate | ✅ Yes | ⚠️ Partial | ⚠️ Warn |

### Discoverability Analysis

**Tier 1 (Obvious — 70%+ find)**:
- ACH-001: Clear from marketing/constitution

**Tier 2 (Clear — 40–70% find)**:
- ACH-002: Logical consequence of betrayal

**Tier 3 (Moderate — 20–40% find)**:
- HID-001: Requires exploration; moderate hint
- HID-002: Requires specific variable combo

**Tier 4 (Obscure — 5–20% find)**:
- END-SEC-001: Requires multiple unlocks; documented but complex

**Tier 5 (Impossible — <5% find)**:
- EGG-002: No hint; pure Easter egg

### Reachability Issues

**🔴 Unreachable** (1):
- HID-001 secret passage: No in-game hint or mechanic to find
  Fix: Add passage hint in NODE-030 prose

**🟡 Contradictory** (1):
- HID-002: Unlock requires relationship > 50, but Ending B path leads to 25
  Fix: Change unlock condition to relationship < 50

**✅ Reachable** (3):
- ACH-001, ACH-002, EGG-002 all reachable with conditions

### Documentation

**Well documented**:
- ACH-001, ACH-002, HID-001 (in FAQ)

**Partially documented**:
- END-SEC-001 (in spec.md but not README)

**Undocumented**:
- EGG-002 (No documentation; pure Easter egg)

### Recommendations

**Priority 1 (Fix before release)**:
1. Add discovery hint for HID-001 secret passage
2. Fix contradictory unlock for HID-002 (change condition)

**Priority 2 (Enhancement)**:
1. Add EGG-002 to FAQ (mark as secret Easter egg)
2. Clarify in opening that END-SEC-001 is optional "True Ending"

**Priority 3 (Balance)**:
1. Consider adding 1–2 more easy secrets (Tier 1–2)
   Currently top-heavy on hard secrets

**[Tabletop RPG] Priority 1 (Campaign Integration)**:
1. Verify all campaign secrets fit within 10-session limit
2. Check faction/companion unlock requirements are reachable with all party builds
3. Add campaign-prep documentation impact (which secrets update campaign-guide.md or SESSION-N-BRIEFING.md)
4. Ensure secret achievements don't require off-session prep (must be unlockable during play)

**[Tabletop RPG] Priority 2 (Ruleset Mechanics)**:
1. Verify ruleset-specific secrets use correct terminology (D&D 5e DC ranges, PF2e degree of success, SR6e dice pools)
2. Check that hidden stat blocks match ruleset difficulty targets (CR balance, XP budgets)
3. Confirm companion stat increases fit ruleset progression curve

**[Computer Game] Priority 1 (Accessibility)**:
1. Verify all route-exclusive secrets have accessibility variants
2. Check color-based secrets have symbol/audio alternatives
3. Confirm timed challenges have non-timed discovery paths
4. Test all secrets discoverable across all playstyle routes (or document as route-exclusive)

**[Computer Game] Priority 2 (Route Balance)**:
1. Verify no route has >3× more secrets than others
2. Check secrets don't create difficulty imbalance (<1.5× on Hard vs. Easy)
3. Ensure convergence point secrets are accessible regardless of route taken

### Secret Content Summary (Generic Report)

- Total secrets: 6 (2 achievements, 2 hidden scenes, 1 Easter egg, 1 secret ending)
- Average difficulty: Hard (mostly Tier 3–4)
- Documentation: 67% documented (4/6)
- Reachability: 67% reachable without fixes (4/6)

Status: ⚠️ GOOD baseline; fix 2 reachability issues before release
```

### 7. **Show Unlock Paths** (optional with --show-unlock-paths)

Display all ways to discover each secret:

```
SECRET: HID-001 "Victor's Letter"

Primary discovery path:
  1. Choose "Help Victor" (NODE-010)
  2. Choose Violent approach (NODE-015)
  3. Execute perfectly (NODE-020 checks)
  4. Reach Ending A (NODE-025)
  5. Examine secret passage (NODE-030)
  
Alternate discovery path:
  1. Choose "Help Victor" (NODE-010)
  2. Choose Stealth approach (NODE-015)
  3. Execute perfectly (NODE-020 checks)
  4. Reach Ending A (NODE-025)
  5. Examine secret passage (NODE-030)

New Game+ path (if supported):
  1. Start 2nd playthrough with carry-over
  2. Jump to NODE-025 (relationship pre-loaded as high)
  3. Go to NODE-030
  4. Examine secret passage

All paths converge at: NODE-030 secret passage discovery
Estimated player who find: 15–25% (requires multiple correct choices)
```

### 8. **Difficulty Map** (optional with --difficulty-map)

Categorize secrets by unlock complexity:

```
DIFFICULTY TIER BREAKDOWN:

Tier 1 (Easy — <5 minutes replay time):
  ACH-001: "Redeemed Victor" — Natural consequence of main path

Tier 2 (Moderate — 5–15 minutes):
  ACH-002: "Betrayer" — Alternate main ending
  HID-002: "Marcus Betrayal" — Specific variable combo

Tier 3 (Hard — 15–45 minutes):
  HID-001: "Victor's Letter" — Requires exploration + multiple choices
  EGG-002: "Name Reference" — Requires custom naming

Tier 4 (Very Hard — 45+ minutes):
  END-SEC-001: "True Ending" — Requires 5+ hidden scene unlocks
  ACH-003: "Speedrunner" — Requires optimized playthrough

Tier 5 (Extreme — Requires guide):
  None currently

Difficulty distribution:
  • Tier 1–2 (Easy): 50% of secrets ✅ Good (accessible to casual players)
  • Tier 3–4 (Hard): 50% of secrets ✅ Good (content for completionists)
  • Tier 5 (Impossible): 0% ✅ Good (all secrets are discoverable)
```

### 9. **Report**

Output `secrets-audit.md` with:
- Secret inventory (all achievements, hidden content, easter eggs)
- Discoverability analysis (tier by findability)
- Reachability verification (can each secret be unlocked?)
- Unlock path analysis (how many ways to find?)
- Documentation status (which secrets are documented?)
- If `--show-unlock-paths`: Full unlock path trees per secret
- If `--difficulty-map`: Difficulty tier breakdown

---

## Important Notes

**Balance Discoverability**: Mix of obvious and obscure secrets keeps players engaged. All-easy is boring; all-impossible is frustrating.

**Document Everything**: Even if secret is meant to be hidden, document it in FAQ/guide. Players deserve to know what exists.

**Test Secret Unlock Paths**: It's easy to accidentally make secrets unreachable. Trace every unlock condition through your variables and branches.

**Easter Eggs Are Different**: Easter eggs can be harder to find since they're fun surprises. Achievements and hidden content should be more discoverable (or have hints).

**Optional Is Key**: Secrets should never gate core story or required endings. If secret is needed for "real" ending, make that explicit in opening warning.

**New Game+ Extends Replayability**: If designing for replay, secrets unlocked in later playthroughs extend the "want to play again" factor significantly.

---

## RPG-Specific Report Sections

### Tabletop RPG Campaign Secret Report (if `SESSION.is_rpg = true` and `SESSION.platform = "tabletop"`)

**Session Distribution**:
- Session(s) where secrets become discoverable (map by session)
- Secrets discoverable only in final 3 sessions (potential miss if campaign ends early)
- Secrets tied to specific encounter types (combat-only, roleplay-only, skill-check-only)

**Companion & Faction Integration**:
| Secret | Type | Unlock Mechanic | Session(s) | Campaign Doc Impact | Status |
|--------|------|-----------------|------------|-------------------|--------|
| Betrayal Ending | Hidden Ending | Faction ≤ -50 | 8–10 | Campaign Guide, S9 Briefing | ✅ Reachable |
| Companion Romance | Hidden Scene | Companion +100 approval | 5–8 | Campaign Guide companion rules | ⚠️ Barely reachable |
| Secret NPC Reveal | Hidden Encounter | Find item + specific dialogue | 3–7 | SESSION briefing (spoiler flag) | ✅ Clear |

**Ruleset-Specific Secret Mechanics**:
```
D&D 5e Secrets:
  - Stat blocks verified to match CR targets
  - Deception/Persuasion DCs between 10–20
  - Hidden loot follows PHB rarity progression

Pathfinder 2e Secrets:
  - Encounter XP budgets verified
  - Degree of success language consistent (critically succeeds/succeeds/fails/critically fails)
  - 4-degree success affects secret unlock (e.g., "critically succeed Investigation to discover" vs. "succeed Investigation to reveal")

Shadowrun 6e Secrets:
  - Hacker access via dice pools (not immediate reveal)
  - Street slang consistent (authentic vs. generic), distinguishes decker jargon
  - NPC karma points reflect secret value (complex secrets worth more karma)
```

**Campaign Prep Documentation Status**:
- Secrets documented in campaign-guide.md § VI (Faction/Companion/House Rules): 3/5 ✅
- Secrets flagged in SESSION-N-BRIEFING.md for player prep: 2/5 ⚠️
- Secrets missing documentation: 0/5 ✅

### Computer Game RPG Secret Report (if `SESSION.is_rpg = true` and `SESSION.platform = "computer"`)

**Route-Exclusive Secret Distribution**:
| Secret | Combat Route | Dialogue Route | Exploration Route | Accessibility |
|--------|------------|--------------|-----------------|-----------------|
| Enemy Weakness | ✅ Available | ⚠️ Discovered differently | ❌ No access | ✅ Colorblind variant |
| NPC Motivation | ❌ No access | ✅ Dialogue-only | ⚠️ Found via journal | ✅ Audio summary |
| Hidden Shrine | ❌ No access | ❌ No access | ✅ Exploration-only | ✅ Text description |

**Playstyle Balance**:
- Combat secrets: 8 total
- Dialogue secrets: 7 total
- Exploration secrets: 5 total
- Imbalance ratio: 8÷5 = 1.6× (acceptable, under 3× limit) ✅

**Accessibility Secret Coverage**:
- Timed challenges with non-timed alternative: 3/4 secrets ⚠️
  Missing: "Quick Reflex" achievement (60-second challenge, no alternative)
- Color-based secrets with accessible variants: 2/2 ✅
- Motor-accessibility variants: 5/6 secrets ⚠️
  Missing: "Perfect Combo" (multi-tap, no single-tap option)
- Cognitive accessibility (memory aids/hints): 6/7 secrets ⚠️
  Missing: "Memory Master" (10-item recall, no hint system)

**Route Convergence & Secret Discovery**:
- Secrets discoverable before convergence (route-specific): 12 secrets
- Secrets discoverable at convergence points: 3 secrets
- Secrets locked after convergence (no carryover): 2 secrets

Convergence seamlessness check:
- "Motivation Revelation" same in all routes: ✅ Seamless prose
- "Betrayal Alternative" tone shifts between routes: ❌ Needs revision (Combat=terse, Dialogue=flowery)

