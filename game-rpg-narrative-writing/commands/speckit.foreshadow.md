---
description: Foreshadowing & payoff tracker — verify clues are placed before revelations, detect orphaned foreshadowing and premature payoffs, ensure mysteries feel fair (not random or cheap). For RPG campaigns (tabletop D&D/Pathfinder/Shadowrun and computer game), validates companion loyalty foreshadowing, faction reputation hints, playstyle route clues, and session-to-session mystery continuity.
handoffs:
  - label: Check Continuity
    agent: speckit.continuity
    prompt: After verifying foreshadowing payoff, check cross-node consistency.
    send: true
  - label: Revise Mysteries
    agent: speckit.revise
    prompt: Some clues need better placement. Please adjust pacing.
    send: true
---

# speckit.foreshadow

**RPG Campaign Support**: Adapts foreshadowing validation for tabletop (companion loyalty foreshadowing across sessions, faction reputation hints building over time, ruleset-specific mechanical foreshadowing) and computer game (playstyle route clues, accessibility variant hints, chapter-to-chapter mystery continuity, route-exclusive payoffs).

Foreshadowing & payoff tracker — verify that all **payoffs have prior setups** and all **mysteries feel fair** rather than random or cheap. Ensures player has enough information to solve puzzles or predict twists before they happen.

## Foreshadowing Principle

**Fair mystery** = Clues are placed before revelation; player could theoretically solve mystery if attentive.  
**Cheap twist** = Revelation appears random because clues were absent or placed too late.

**Valid foreshadowing includes**:
- ✅ Explicit clue ("The vase has a hairline crack")
- ✅ Implicit hint ("Why does Marcus always leave at sunset?")
- ✅ Symbolic foreshadowing (red herring used for flavor; real clue elsewhere)
- ✅ Character behavior (NPC avoids certain topics, suggesting secrets)

**Invalid foreshadowing includes**:
- ❌ Orphaned foreshadowing (clue placed but never paid off; confusion)
- ❌ Premature payoff (revelation before clue is placed; unfair)
- ❌ Inaccessible clue (locked behind missed branch; unsolvable)
- ❌ Contradiction (clue conflicts with later revelation; feels arbitrary)

## User Input

```text
$ARGUMENTS
```

Accepted input:
- Nothing — audit entire game for clue-payoff pairs
- Mystery ID (e.g., `MYS-001`) — audit one mystery only
- `--branch [BRANCH_ID]` — audit clues in one story branch only
- `--clue-only` — show only placement issues (ignore payoff timing)

Optional flags:
- `--strict` — flag any clue not placed before payoff (even if obvious)
- `--show-paths` — display clue → payoff chain for each mystery
- `--check-accessibility` — verify clues reachable in all branches

## Pre-Execution Checks

**Auto-detect platform and ruleset** (for RPG campaigns):
- Load `constitution.md`
- Extract `[PLATFORM]` (tabletop/computer) and `[RULESET]` (D&D 5e/Pathfinder 2e/Shadowrun 6e)
- Set SESSION object {platform, ruleset, mechanics}
- If RPG: Load `companions.md`, `factions.md`, `mechanics-[RULESET].md`, `plan.md` (for session/chapter structure)

**Standard checks**:
1. Load `specs/foreshadow-template.md` or extract from spec.md (mysteries, plot twists)
2. Confirm `specs/plan.md` exists with node sequence
3. Load all `draft/[ENGINE]/NODE-*.md` files to locate clue text and payoff moments
4. Parse for clue keywords (names, objects, behaviors)
5. Identify payoff moments (reveals, twists, puzzle solutions)

## Execution Steps

### 1. **Define Mysteries & Payoffs**

Extract from spec.md or foreshadow template:

**Example mysteries**:
```
MYS-001: Who is Marcus really?
  Genre: Betrayal twist
  Setup: NODE-005 (Marcus introduced as ally)
  Clues:
    • NODE-010: Marcus asks suspicious questions
    • NODE-015: Marcus is never present at night
    • NODE-020: Marcus carries a militia ring
  Payoff: NODE-025 (Revealed: Marcus is undercover militia spy)

MYS-002: What happened to Sera?
  Genre: Loss/mystery
  Setup: NODE-007 (Sera disappears between scenes)
  Clues:
    • NODE-012: Found Sera's locket near the docks
    • NODE-017: Heard rumors of kidnapping
    • NODE-022: Marcus hints he knows something
  Payoff: NODE-025 (Revealed: Sera was taken by militia to pressure you)

MYS-003: Where is the hidden treasure?
  Genre: Puzzle
  Setup: NODE-003 (Old map discovered)
  Clues:
    • NODE-008: "X marks the spot" — painting in tavern
    • NODE-014: Innkeeper mentions cellar lock
    • NODE-019: "Three paces north" — carved on bench
  Payoff: NODE-023 (Treasure found in cellar: 3 paces north from painting)
```

### 2. **Map Clue Placement vs. Payoff**

For each mystery, create a timeline:

```
MYS-001: Who is Marcus really?

Clue: "Marcus asks about your supply routes"
  Placed in: NODE-010 (page 15)
  Payoff: NODE-025 (page 40)
  Gap: 10 nodes / ~25 pages
  ✅ SUFFICIENT: Player has 25 pages to notice pattern

Clue: "Marcus carries militia insignia ring"
  Placed in: NODE-020 (page 35)
  Payoff: NODE-025 (page 40)
  Gap: 1 node / 5 pages
  ✅ DIRECT: Last-minute clue before payoff (reinforces theory)

Clue: "Marcus is never present at night"
  Placed in: NODE-015 (page 25)
  Payoff: NODE-025 (page 40)
  Gap: 10 nodes / 15 pages
  ✅ SUFFICIENT: Clear pattern before payoff

Analysis:
  Clue placement: ✅ All clues before payoff
  Distribution: ✅ Spread across 15 pages (not all at end)
  Sufficiency: ✅ Player has ample time to notice
  Fairness: ✅ Attentive player could solve before NODE-025
  Status: ✅ FAIR MYSTERY
```

### 3. **Detect Foreshadowing Violations**

#### 🔴 **VIOLATION: Premature Payoff**
Revelation happens before clue is placed.

```
MYS-002: What happened to Sera?

Payoff (revelation): NODE-022
  "Sera was kidnapped by militia"
  
Clues (placed after):
  • Locket found: NODE-024 (2 nodes AFTER reveal!)
  • Militia mention: NODE-025
  • Marcus hint: NODE-026
  
Problem: Player learns Sera was kidnapped at NODE-022,
         but proof appears in NODE-024, NODE-025, NODE-026
         This feels backward—reveals before evidence
         
Status: ❌ UNFAIR MYSTERY
Fix: Either:
  1. Move clues to NODE-015—NODE-021 (before reveal)
  2. Change payoff node to NODE-026 (after all clues)
  3. Add immediate clue at NODE-022 to justify the reveal
```

**Report**:
```
MYS-002: Premature Payoff
  Revelation: NODE-022
  First supporting clue: NODE-024 (2 nodes AFTER)
  
  Status: ❌ UNFAIR
  Impact: Player can't predict this reveal
  Fix: Reorganize clues to precede payoff by at least 3 nodes
```

#### 🟡 **VIOLATION: Orphaned Foreshadowing**
Clue placed but never paid off; confuses player.

```
MYS-003: Where is the hidden treasure?

Clue: "The innkeeper mentions a cellar lock"
  Placed in: NODE-014
  Payoff: NONE (treasure is found in attic, not cellar)
  
Problem: Player hears about cellar lock but it's irrelevant
         Feels like abandoned plot thread
         Confuses intended mystery solving
         
Status: ⚠️  ORPHANED CLUE
Options:
  1. Move treasure to cellar (pay off the clue)
  2. Remove cellar mention (don't introduce fake clue)
  3. Explain cellar lock later (reveal it was red herring intentionally)
```

**Report**:
```
MYS-003: Orphaned Foreshadowing
  Clue: "Innkeeper mentions cellar lock"
  Placed: NODE-014
  Payoff: NONE
  
  Status: ⚠️  ORPHANED
  Impact: Confusing to player; feels like plot hole
  Fix: Either pay off (move treasure to cellar) or remove (edit NODE-014)
```

#### 🟠 **VIOLATION: Inaccessible Clue**
Clue locked behind branch player might not visit; payoff unsolvable.

```
MYS-004: Who killed the mayor?

Clue: "Weapon found in Marcus's room"
  Placed in: NODE-015 (BRANCH A only)
  
Branch B (alternative path):
  NODE-015: Takes different route (never visits Marcus's room)
  NODE-025: Payoff — "Marcus killed the mayor"
  
Problem: Branch B players never see evidence
         Mystery feels unsolvable in Branch B
         Same payoff without clue = unfair mystery
         
Status: ⚠️  INACCESSIBLE CLUE
Fix: Either:
  1. Add alternate clue in Branch B (different evidence)
  2. Move main clue to common node before branch (NODE-010)
  3. Only pay off mystery in Branch A (B players don't learn truth)
```

**Report**:
```
MYS-004: Inaccessible Clue in Branch B
  Clue: "Weapon in Marcus's room"
  Placed: NODE-015 (Branch A only)
  Payoff: NODE-025 (both branches)
  
  Status: ⚠️  UNFAIR IN BRANCH B
  Impact: Mystery feels random in Branch B
  Fix: Add alternate clue reachable in Branch B before NODE-025
```

#### 🔵 **VIOLATION: Contradicting Clue**
Multiple clues point to different conclusions.

```
MYS-005: Is Marcus trustworthy?

Clue 1: "Marcus volunteers to help without payment"
        Interpretation: Trustworthy (aligned with your cause)
        Placed: NODE-010

Clue 2: "Marcus asks detailed questions about your network"
        Interpretation: Spy (suspicious interest)
        Placed: NODE-015

Payoff: NODE-025
  "Marcus was gathering intelligence for militia"
  
Analysis: 
  Clue 1 suggests innocence, Clue 2 suggests guilt
  Without additional context, player can't determine which is true
  Feels like contradiction rather than misdirection
  
Status: ⚠️  AMBIGUOUS
  If intentional misdirection: ✅ OK (red herring)
  If unintentional contradiction: ❌ Unfair
  
Question: Is the voluntary help meant to mask ulterior motives?
         Should be explicit if so.
```

**Report**:
```
MYS-005: Contradicting Clues (Review Needed)
  Clue 1 interpretation: Trustworthy
  Clue 2 interpretation: Suspicious
  
  Status: ⚠️  AMBIGUOUS
  Verdict: Is this intentional misdirection or accident?
  Recommendation: Add clarifying beat showing Marcus's true motivation
                 (e.g., his "kindness" is calculated strategy)
```

#### ✅ **VALID: Fair Mystery**
Clues placed strategically; payoff feels earned.

```
MYS-001: Who is Marcus really?

Timeline:
  NODE-010: Clue 1 (Marcus asks suspicious questions)
  NODE-015: Clue 2 (Marcus absent at night)
  NODE-020: Clue 3 (Militia ring)
  NODE-025: Payoff (Marcus is spy)
  
Clue distribution: Spread across 15 pages
Clue quantity: 3 clues (sufficient for player awareness)
Clue clarity: Each clue independently points toward "spy" interpretation
Payoff timing: 5 pages after last clue (reinforcement before reveal)
Player prediction: Attentive reader could predict "Marcus is spy" at NODE-015 or NODE-020

Status: ✅ FAIR MYSTERY
Quality: Excellent (enough clues, good distribution, satisfying payoff)
```

### 4. **Generate Foreshadowing Audit Report**

Create `specs/foreshadow-audit.md`:

```markdown
## Foreshadowing & Payoff Audit

**Game**: [NAME]
**Date**: [ISO]

### Mystery Fairness Table

| Mystery ID | Name | Clue Count | Placement | Distribution | Payoff | Status |
|------------|------|-----------|-----------|--------------|--------|--------|
| MYS-001 | Marcus spy? | 3 | Early | Spread | Fair | ✅ PASS |
| MYS-002 | Sera fate? | 2 | Late | Clustered | Unfair | ⚠️ REVIEW |
| MYS-003 | Treasure loc? | 3 | Optimal | Well-spaced | Fair | ✅ PASS |
| MYS-004 | Mayor killer? | 1 | Branch-only | Inaccessible | Unfair | ⚠️ FIX |

### Violations

**🔴 Premature Payoffs** (1):
- MYS-002 (Sera): Reveals at NODE-022; clues appear NODE-024+
  Fix: Move clues to NODE-015—NODE-021

**🟡 Orphaned Clues** (1):
- MYS-003: Cellar lock mentioned but treasure in attic
  Fix: Move treasure to cellar OR remove cellar reference

**🟠 Inaccessible Clues** (1):
- MYS-004: Branch B can't access weapon clue
  Fix: Add alternate clue in Branch B

**🔵 Contradicting Clues** (0):
- None found

### Fair Mysteries

**✅ PASS** (2):
- MYS-001: Well-distributed clues; fair payoff
- MYS-003: Good pacing; solvable with attention

### Recommendations

**Priority 1 (Fix before release)**:
1. MYS-002: Reorganize clue timing relative to payoff
2. MYS-004: Add Branch B alternate clue

**Priority 2 (Polish)**:
1. MYS-003: Add one more cellar reference to strengthen foreshadowing OR move treasure
```

### 5. **Show Paths** (optional with --show-paths)

Display full clue chain for each mystery:

```
MYS-001: Who is Marcus really?

Clue Chain:
  NODE-010 → "Marcus asks about supply routes"
    └─ Suggests: He's gathering intelligence
  
  NODE-015 → "Marcus disappears at night"
    └─ Suggests: Secret activity
    └─ Combined with previous: Intelligence gathering
  
  NODE-020 → "Marcus carries militia insignia"
    └─ Suggests: Military connection
    └─ Combined: Marcus is military agent
  
  NODE-025 → PAYOFF: "Marcus is militia spy"
    └─ Confirmed by all three clues
    └─ Player could have deduced this at NODE-020

Player prediction timeline:
  NODE-010: "Something's odd about Marcus" (1 clue, weak signal)
  NODE-015: "Marcus is definitely hiding something" (2 clues, pattern emerges)
  NODE-020: "Marcus is a military agent" (3 clues, solution obvious)
  NODE-025: Payoff (confirmation)
```

### 6. **Accessibility Check** (optional with --check-accessibility)

Verify clues are reachable in all branches:

```
MYS-001: Marcus spy?

Branch A path:
  NODE-005 (common)
  NODE-010 ✅ Clue 1 found
  NODE-015 ✅ Clue 2 found
  NODE-020 ✅ Clue 3 found
  NODE-025 ✅ Payoff
  Status: ✅ All clues accessible

Branch B path:
  NODE-005 (common)
  NODE-007 (diverges)
  NODE-015 ⚠️ Different path, doesn't visit NODE-010/NODE-015
  NODE-022 (reconverges)
  NODE-025 ✅ Payoff
  
  Problem: Branch B misses Clues 1 & 2
  Solution: Add alternate clues in Branch B path (NODE-007, NODE-014)
```

### 7. **Report**

Output `foreshadow-audit.md` with:
- Mystery fairness table (clue count, placement, distribution)
- Violation list (premature, orphaned, inaccessible, contradicting)
- Specific recommendations per mystery
- If `--show-paths`: Full clue chain for each mystery
- If `--check-accessibility`: Branch-by-branch accessibility analysis

### 7A. **RPG Campaign Foreshadowing Validation** (if [PLATFORM] detected)

**For Tabletop RPG**:
- Companion loyalty foreshadowing: Verify companion behavior clues are placed before major loyalty shifts (e.g., if Theron's loyalty drops sharply, behavior hints should precede the decision)
- Faction reputation foreshadowing: Verify faction hints about their goals/values appear before major faction reputation choices
- Session-to-session continuity: Verify SESSION-N foreshadowing carries through to SESSION-(N+1) payoff (clues don't reset between sessions)
- NPC backstory hints: Verify NPC secrets are hinted before revelations (companion origin story should have hints before full backstory reveal)
- Ruleset-specific foreshadowing: (D&D 5e) Spell/condition foreshadowing placed before mechanical effects; (Pathfinder 2e) Critical outcome hints before critical rolls; (Shadowrun 6e) Karma/Edge scarcity hints before resource-critical decisions

**For Computer Game**:
- Route clues: Verify each playstyle route has early hints about route commitment before CHAPTER-2 choice (Stealth hints: shadows, sneaking NPCs; Combat hints: combat encounters, weapon focus; Diplomacy hints: dialogue options, NPC relationships)
- Route-exclusive payoffs: Verify route-specific mysteries only have clues accessible in that route
- Accessibility variant hints: If accessibility mode affects story interpretation, hint at accessibility consideration early (e.g., if colorblind mode changes visual puzzle solutions, hint that vision might matter)
- Chapter-to-chapter carry-over: Verify CHAPTER-N foreshadowing carries through CHAPTER-(N+1) payoff (clues don't reset between chapters)
- Cross-route fairness: Verify each route has similarly fair mystery solving difficulty (not one route with obvious clues, another with obscure clues)

---

## RPG Campaign Foreshadowing Notes

### Tabletop Campaign Foreshadowing Considerations

**Companion Loyalty Foreshadowing**:
- Companion personality clues should appear before major loyalty shifts
- Example: If Theron's loyalty will drop when party chooses to help Thieves Guild, his strong Temple alignment should be shown in SESSION-2-3 dialogue
- Red flags:
  - Loyalty shift happens without preceding personality/value hints
  - Companion suddenly cares about something never mentioned before
  - No dialogue opportunity to predict companion reaction to choice
- Testing approach: For each major loyalty shift, identify 2-3 sessions of personality clues before the decision

**Faction Reputation Foreshadowing**:
- Faction goals and values should be hinted before major reputation choices
- Example: If Temple has strict code against stealing, this value should be established in SESSION-1-2 encounters before SESSION-3 theft dilemma
- Red flags:
  - Faction suddenly opposes action that contradicts values established earlier
  - Faction's stance feels arbitrary (no prior indication of their principles)
  - Multiple factions with identical values (no way to predict which will approve/disapprove)
- Testing approach: For each faction, ensure their core values are shown in dialog before reputation-affecting choices

**Session-to-Session Mystery Continuity**:
- Mysteries that span multiple sessions need clue reinforcement in each session
- Example: "Who is Marcus working for?" mystery introduced SESSION-2 should have reinforcing clues in SESSION-3, SESSION-4 (not just SESSION-2)
- Red flags:
  - Mystery introduced SESSION-2, clues only in SESSION-2, revelation SESSION-9 (too long between clue and payoff)
  - SESSION-5 players might forget SESSION-2 clues; needs reminder
- Testing approach: For multi-session mysteries, verify clues appear in at least 3 different sessions, not just introduction session

**NPC Backstory Foreshadowing**:
- NPC secrets should have hints before major reveal
- Example: If companion is secretly nobility in hiding, hints about refined manners/speech patterns should appear in SESSION-2-4 before SESSION-8 revelation
- Red flags:
  - NPC backstory reveal feels like surprise with no prior hints
  - Hints exist but are vague (requires replay to notice)
  - Hints contradict revealed backstory (e.g., hints at wealth but revealed as peasant)
- Testing approach: For each NPC with significant backstory, place 3+ contextual hints before major reveal

**Ruleset-Specific Foreshadowing**:

**D&D 5e**:
- Spell mechanics should be hinted before critical spell usage
- Example: If "Hold Person" spell will be crucial in final boss, an NPC should mention being "paralyzed by magic" in earlier encounter
- Condition effects should be shown in minor form before major consequences
- Example: If "Frightened" condition becomes key in final boss mechanics, show NPC briefly frightened in SESSION-5 scene

**Pathfinder 2e**:
- Critical success/failure importance should be foreshadowed
- Example: If final negotiation requires critical success, earlier negotiations should show critical successes changing outcomes dramatically
- Persistent conditions should be hinted before becoming major obstacles
- Example: If "Drained" condition limits resources, show brief "drained" state in SESSION-5 quest

**Shadowrun 6e**:
- Karma scarcity should be foreshadowed early
- Example: If Karma will be limited by SESSION-6, show resource pressure in SESSION-3-4 (tough choices about spending limited Karma)
- Edge pool management should be shown as critical mechanic
- Example: If Edge pool saves final mission, show earlier missions where Edge usage matters

### Computer Game Route Foreshadowing Considerations

**Route Clues Before CHAPTER-2 Commitment**:
- Players should see hints about playstyle options before committing to route
- Stealth hints: Shadowy areas, NPC using stealth successfully, locks that could be picked
- Combat hints: Combat encounters, weapon acquisition opportunities, strong NPC fighters
- Diplomacy hints: Dialogue-heavy scenes, NPC relationships mattering, peaceful resolutions
- Example: CHAPTER-1 should include:
  - Stealth route: Shadow passage visible but unexplored, NPC mentions "sneaking past guards worked"
  - Combat route: Combat encounter with satisfying victory, loot from defeated enemies
  - Diplomacy route: Negotiation that prevents conflict, NPC praising your words
- Red flags:
  - One route has obvious foreshadowing, others don't (creates bias toward that route)
  - Route hints don't appear until CHAPTER-2 (too late, player already confused)
  - Route commitment feels random (no prior context about what each route offers)

**Route-Exclusive Foreshadowing**:
- Mysteries that only resolve in one route should have hints only accessible in that route
- Example: Stealth route mystery "How to infiltrate undetected?" should have lock-picking clues, vent locations, timing hints (don't have those in Combat route)
- Red flags:
  - Combat route can solve Stealth-only mystery (confusing, blurs route distinctions)
  - Mystery hinted in all routes but only solvable in one (unfair)

**Accessibility Variant Foreshadowing**:
- If accessibility modes are meant to provide alternative interpretations, hint at this early
- Example: If colorblind mode shows different visual puzzle solutions, CHAPTER-1 should have scene acknowledging visual variants exist
- Red flags:
  - Accessibility mode treated as "cheat" rather than valid interpretation
  - No foreshadowing that accessibility modes exist
  - Accessibility mysteries too obscure without prior hints

**Chapter-to-Chapter Carry-Over**:
- CHAPTER-2 foreshadowing should carry through CHAPTER-3-4 payoffs
- Example: If CHAPTER-2 hints at NPC betrayal, CHAPTER-3-4 should reinforce suspicion (not let player forget)
- Red flags:
  - CHAPTER-2 clues never mentioned again in CHAPTER-3-4
  - Major revelation in CHAPTER-4 lacks clues from CHAPTER-2-3
  - Player could forget CHAPTER-2 foreshadowing by CHAPTER-4 payoff

**Cross-Route Fairness**:
- Each route should have similarly solvable mysteries (not one route obvious, another obscure)
- Example:
  - Stealth route mystery: "Guard patrol timing?" (clues: light changes, NPC mentions schedule, clock shows times) — solvable
  - Combat route mystery: "Guard strength?" (clues: earlier encounters show similar guards, equipment visible, NPC mentions rank) — equally solvable
  - Diplomacy route mystery: "Guard commander's fears?" (clues: dialogue reveals worries, NPC background hints, previous conversation shows vulnerabilities) — equally solvable
- Red flags:
  - Stealth route mysteries obvious, Combat route mysteries obscure
  - One route has 5+ clues per mystery, another has 1-2
  - Different routes require different "player skill" to solve (not fair comparison)

---

## Important Notes

**Clue Quantity**: 2–3 well-placed clues is ideal for subtle mysteries. 4+ clues risks being heavy-handed. 1 clue risks being missable.

**Clue Distribution**: Spread clues across ~10+ nodes / pages before payoff. Clustering all clues right before payoff feels like info-dump (unfair surprise).

**Accessibility Across Branches**: If same mystery pays off in multiple branches, ensure clues are accessible in all branches (or provide branch-specific alternate clues).

**Red Herrings Are OK**: Intentional false clues add depth. Mark them in foreshadow template so you don't confuse them with actual clues. (e.g., "Clue 2B [RED HERRING]: Marcus's midnight disappearances are explained later as insomnia, not spying.")

**Player Attention**: Assume moderate player attention. Don't expect players to notice subtle clues, but do expect them to catch direct statements and obvious behavioral patterns.

**Mystery Genre Matters**: Whodunits need more clues; character-driven games need fewer. Adjust clue density based on game genre and player expectations.

