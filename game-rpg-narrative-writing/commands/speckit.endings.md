---
description: Ending quality gate — verify endings resolve the central dramatic question, maintain thematic consistency, and provide satisfying closure for player character and stakes. For RPG campaigns (tabletop D&D/Pathfinder/Shadowrun and computer game), validates campaign epilogues, companion/faction outcomes, playstyle route-specific endings, and accessibility consistency across all endings.
handoffs:
  - label: Check Agency
    agent: speckit.agency
    prompt: Before finalizing endings, verify player choices actually lead to different endings.
    send: true
  - label: Review Themes
    agent: speckit.tone
    prompt: Check that endings emotionally land and thematically resolve.
    send: true
---

# speckit.endings

**RPG Campaign Support**: Adapts ending validation for tabletop (campaign epilogues per SESSION, companion fate resolution, faction outcomes, ruleset-specific mechanical resolutions) and computer game (playstyle route-specific endings, accessibility consistency, route variant ending prose, computer epilogue mechanics).

Ending quality gate — verify all registered endings provide **satisfying closure** by resolving the central dramatic question, maintaining thematic consistency, and giving narrative weight to player agency.

## Ending Quality Rubric

An ending is **satisfying** when it:
- ✅ **Resolves the central dramatic question** (from constitution.md §V Dramatic Question)
- ✅ **Player character has changed** (arc closure, not reset)
- ✅ **Stakeholder fates are clear** (key NPCs, supporting cast, world state)
- ✅ **Thematic resonance** (echoes central theme, resolves or ironizes it)
- ✅ **Consequence weight** (player choices matter; stakes have real payoff)
- ✅ **Emotional landing** (tone matches content; doesn't feel cheap or manipulative)
- ✅ **Explicitness** (not ambiguous about what happened and what it means)

**NOT validated here** (use other tools):
- ❌ Whether all endings are reachable (use `speckit.agency`)
- ❌ Pacing/prose quality (use `speckit.polish`)
- ❌ Whether foreshadowing pays off (use `speckit.foreshadow`)

## User Input

```text
$ARGUMENTS
```

Accepted input:
- Nothing — audit all endings in `specs/endings.md`
- Ending ID (e.g., `ENDING-001`) — audit one specific ending
- `--endings-only` — check only ending node files (skip variable/consequence validation)
- `--show-variants` — display all conditional ending variants based on variable state

Optional flags:
- `--strict` — fail on ambiguous or emotionally hollow endings
- `--check-reachability` — verify each ending is actually reachable from root node

## Pre-Execution Checks

**Auto-detect platform and ruleset** (for RPG campaigns):
- Load `constitution.md`
- Extract `[PLATFORM]` (tabletop/computer) and `[RULESET]` (D&D 5e/Pathfinder 2e/Shadowrun 6e)
- Set SESSION object {platform, ruleset, mechanics}
- If RPG: Load `companions.md`, `factions.md`, `mechanics-[RULESET].md`, `campaign-guide.md`

**Standard checks**:
1. Confirm `specs/endings.md` exists with all registered endings
2. Confirm `specs/constitution.md` exists with central dramatic question and theme
3. Confirm `specs/plan.md` exists with ending node identifiers
4. Confirm `draft/[ENGINE]/` contains ending node files for each ending
5. Load `specs/characters.md` if available (for character arc closure)
6. Load `specs/themes.md` if available (for thematic resonance check)
7. If RPG: Verify campaign-guide.md exists (for campaign-level ending context)

## Execution Steps

### 1. **Load Spec Documents**
   - Read `constitution.md`: Extract central dramatic question (§V), theme, ending tone preferences
   - Read `endings.md`: All ending IDs, names, win/loss classification, required variables
   - Read `plan.md`: Ending node IDs (where endings are written)
   - Read ending node files: Extract prose and variable state snapshots

### 2. **Audit Each Ending**

For each registered ending in `endings.md`:

#### A. **Central Question Resolution Check**

**Question**: Does the ending answer the central dramatic question from constitution.md?

**Central Dramatic Question examples**:
- "Can the protagonist overcome their trust issues?"
- "Will the rebellion succeed against the tyranny?"
- "Does love survive conflict?"

**Validation**:
```
Constitution: "Can the protagonist escape their past?"

ENDING-ESCAPE:
  Prose: "You leave the city behind. The ghosts don't follow."
  ✅ YES — Directly answers the question (protagonist escapes)

ENDING-AMNESIA:
  Prose: "You lose your memories. The past no longer haunts you."
  ⚠️  INDIRECT — Answers via memory loss rather than actual escape
  → Flag as "thematic dodge" — is this intentional?

ENDING-RETURN:
  Prose: "You come back home. Your family waits."
  ❌ NO — Doesn't address the question (protagonist doesn't escape)
  → Flag as failure to resolve central question
```

**Report**:
```
ENDING-ESCAPE:
  Central Question: "Can protagonist escape their past?"
  Resolution: ✅ Direct — protagonist leaves
  Status: RESOLVES

ENDING-RETURN:
  Central Question: "Can protagonist escape their past?"
  Resolution: ❌ Avoids — doesn't address escape
  Status: DOES NOT RESOLVE
  Fix: Either reframe question, or rewrite ending to address escape
```

#### B. **Player Character Arc Closure Check**

**Question**: Has the player character changed from start to this ending?

**Arc closure exists when**:
- Character belief shifts (e.g., "I can't trust anyone" → "I can trust selectively")
- Capability increases (learns skill, gains confidence)
- Relationship changes (with mentor, with love interest, with self)
- Stakes are paid (if cost promised, cost is collected; if victory promised, victory achieved)

**Validation**:
```
ENDING-HERO:
  Start state: player_agency = 0, courage = 2, trust = -5
  End state: player_agency = 1, courage = 5, trust = 2
  ✅ ARC EXISTS — Multiple character stats have changed
  
ENDING-RESET:
  Start state: courage = 2, trust = -5
  End state: courage = 2, trust = -5
  ❌ NO ARC — Character unchanged, returns to start
  Fix: Add character change (even if tragic/hollow)
```

**Report**:
```
ENDING-HERO:
  Player arc: courage -2→5, trust -5→2
  Status: ✅ Strong arc with stakes paid

ENDING-RESET:
  Player arc: (no change from start state)
  Status: ❌ No character growth
  Fix: Add at least one variable shift to show change
```

#### C. **Stakeholder Fate Clarity Check**

**Question**: Is the fate of key NPCs and world state explicitly stated?

Key stakeholders:
- Protagonist (should be addressed; see arc closure above)
- Love interest / key relationship (what happens to this bond?)
- Mentor / antagonist (alive? dead? reconciled?)
- Supporting cast (at least mentioned, not completely abandoned)
- World state (changed by player choices or reset?)

**Validation**:
```
ENDING-PEACE:
  Prose: "The city is quiet. Marcus smiles from the balcony.
          You realize Sera went back to her family.
          The war council never meets again."
  ✅ All key NPCs addressed:
     • Protagonist: at peace, contemplative
     • Marcus (mentor): alive, content
     • Sera (love interest): departed but acknowledged
     • Antagonists: implicitly defeated (war council dissolved)
     • World: permanently changed

ENDING-BETRAYED:
  Prose: "You're alone in the basement.
         The door closes. You hear footsteps above,
         then silence."
  ⚠️  AMBIGUOUS:
     • Protagonist: trapped, possibly dead?
     • Marcus: fate unclear (was he the betrayer?)
     • Sera: fate unknown
     • Antagonists: not addressed
     Fix: Add 1-2 lines clarifying fates of key NPCs
```

**Report**:
```
ENDING-PEACE:
  Marcus (mentor): Addressed ✅
  Sera (love interest): Addressed ✅
  Antagonists: Addressed ✅
  World state: Addressed ✅
  Status: ✅ All stakeholders clear

ENDING-BETRAYED:
  Marcus: Unknown ⚠️
  Sera: Unknown ⚠️
  Antagonists: Unknown ⚠️
  Status: ⚠️ Multiple ambiguous fates
```

#### D. **Thematic Resonance Check**

**Question**: Does the ending echo the central theme and resolve or ironize it meaningfully?

**Theme examples** (from constitution.md §V Theme):
- "Trust must be earned" → Ending should show trust dynamics
- "Power corrupts" → Ending should show player power usage
- "Love transcends boundaries" → Ending should center on love

**Validation**:
```
Theme: "Trust must be earned"

ENDING-PARTNERSHIP:
  Prose: "Marcus extends his hand. 'I trust you now.' 
          Years of small choices led here."
  ✅ RESONATES — Centers on trust being earned through action
  
ENDING-BETRAYAL:
  Prose: "Marcus smiles as he stabs you.
          You gave him everything. He didn't earn your trust—he took it."
  ✅ RESONATES (ironically) — Subverts the theme darkly; trust was misplaced

ENDING-ESCAPE:
  Prose: "You flee the city. Nobody follows."
  ❌ IGNORES THEME — Doesn't address trust at all
  Fix: Add element showing trust dynamics (or reconsider if this is right ending for this theme)
```

**Report**:
```
ENDING-PARTNERSHIP:
  Central theme: "Trust must be earned"
  Resonance: ✅ Strong — explores earning trust
  Type: Direct resolution

ENDING-ESCAPE:
  Central theme: "Trust must be earned"
  Resonance: ❌ None — ending avoids theme
  Type: Thematic gap
  Fix: Rewrite to include trust element OR reconsider if ending fits this game
```

#### E. **Consequence Weight Check**

**Question**: Do player choices feel like they matter? Does the ending prove that stakes were real?

**Consequence weight exists when**:
- Different endings reachable based on different choice paths
- High-stakes choices lead to visibly different outcomes
- Player agency decisions are reflected in ending variation
- Sacrifices made in-game are acknowledged in ending

**Validation**:
```
Choice at NODE-010: "Save Marcus or Protect City"

Save Marcus path:
  → Marcus alive in ending prose
  → City falls, mentioned as lost
  → Variables: marcus_alive = true, city_standing = -5
  ✅ Consequence clear

Protect City path:
  → Marcus mentioned as fallen hero
  → City stands but wounded
  → Variables: marcus_alive = false, city_standing = 2
  ✅ Consequence clear

Both paths → ENDING-001 but with different variable snapshots
✅ Same ending ID, but meaningful state difference
```

**Report**:
```
ENDING-VICTORY:
  Consequence weight (choice → outcome):
    • "Save Marcus" path has marcus_alive = true ✅
    • "Protect City" path has marcus_alive = false ✅
    • Ending prose reflects both variants
  Status: ✅ Strong consequence weight
```

### 3. **Generate Ending Quality Report**

Create `specs/ending-audit.md`:

```markdown
## Ending Quality Audit

**Game**: [NAME]
**Central Question**: [from constitution]
**Theme**: [from constitution]
**Date**: [ISO]

| Ending ID | Name | Central Q | Arc | Clarity | Thematic | Consequence | Status |
|-----------|------|-----------|-----|---------|----------|-------------|--------|
| ENDING-001 | Victory | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ PASS |
| ENDING-002 | Escape | ✅ | ⚠️ | ✅ | ⚠️ | ✅ | ⚠️ REVIEW |
| ENDING-003 | Death | ✅ | ✅ | ⚠️ | ✅ | ✅ | ✅ PASS |
| ENDING-004 | Reset | ❌ | ❌ | ✅ | ❌ | ❌ | ❌ FAIL |

### Violations

**Fail (4 - Need fixes)**:
- ENDING-004 (Reset): Doesn't resolve central question, no character arc

**Review (2 - Consider fixes)**:
- ENDING-002 (Escape): Weak arc, ambiguous thematic payoff

**Pass (2)**:
- ENDING-001 (Victory): Fully resolving
- ENDING-003 (Death): Thematically resonant tragedy

### Recommendations

**Priority 1 (Fix before release)**:
1. ENDING-004: Either add character arc or cut this ending
2. ENDING-002: Strengthen emotional closure and thematic tie-in

**Priority 2 (Polish)**:
1. ENDING-001: Clarify one ambiguous NPC fate
2. ENDING-003: Consider adding epilogue variant for different variable states
```

### 4. **Ending Variants** (optional with --show-variants)

Some endings may have multiple variants based on variables:

```
ENDING-PEACE (base):
  Base prose: "The city is quiet."
  
  + if marcus_alive: "Marcus smiles from the balcony."
  + elif marcus_dead: "We honor Marcus's memory at the memorial."
  
  + if rebellion_won: "The new council meets in the square."
  + elif rebellion_lost: "The occupiers have left, but the wound remains."

Variants generated: 4 (2 × 2 combinations)
Status: ✅ Ending reflects major choice branches
```

**Report all variants** so writers can verify each feels satisfying.

### 5. **Reachability Check** (optional with --check-reachability)

Trace from root node → each ending:
- Is there at least one valid path to this ending?
- Are there choice combinations that make this ending unreachable?

**Report unreachable endings** — they may be dead code or blocked by agency violations.

### 5A. **RPG Campaign Ending Validation** (if [PLATFORM] detected)

**For Tabletop RPG**:
- Campaign epilogue: All sessions lead to coherent ending (ENDING-CAMPAIGN or ENDING-SESSION-N for final chapter)
- Companion fate resolution: Each companion (alive/dead/left party) has explicit outcome mentioned in ending
- Faction outcome clarity: Each faction's final reputation and alliance status stated in ending
- Ruleset-specific resolution: (D&D 5e) spell effects, conditions resolved; (Pathfinder 2e) critical outcomes honored; (Shadowrun 6e) Karma/Edge pool consequences shown
- Player introduction acknowledgment: Final ending should acknowledge character introduction hook from SESSION-1 briefing (closure of personal story)

**For Computer Game**:
- Route-specific endings: Each playstyle route (Stealth/Combat/Diplomacy) has distinct ending variants (different prose, outcomes, NPC reactions)
- Accessibility consistency: If accessibility mode set (colorblind/audio/motor), ending prose and cinematics support that mode (same emotional impact, no visual-only critical information)
- Route commitment acknowledgment: Ending acknowledges player's playstyle choice throughout campaign (reflected in ending dialogue, NPC reactions)
- Chapter-to-chapter continuity: Final ending addresses key decisions from CHAPTER-2-4 (routes chosen, accessibility modes used)
- Cross-route fairness: Each route's ending feels equally satisfying (not one route getting better rewards/epilogue than others)

### 6. **Report**

Output `ending-audit.md` with:
- Audit table (all 7 quality dimensions per ending)
- Violation list (fail, review, pass categories)
- Specific recommendations for each failing ending
- If RPG campaign: Add companion fate table, faction outcome table, route-specific ending variants
- If `--show-variants`: Variant table for each ending
- If `--check-reachability`: Reachability analysis

---

## Important Notes

**Satisfying ≠ Happy**: Tragic, bittersweet, and dark endings can be fully satisfying if they resolve the dramatic question and close character arcs. A sad ending where the character changed is more satisfying than a happy ending where nothing mattered.

**Ambiguity Rule**: Minor ambiguities are fine (reader interpretation space). Major ambiguities (protagonist fate, world state, key NPC survival) should be explicit.

**Theme Payoff**: If you chose a central theme, every ending should either resolve it directly, subvert it meaningfully, or explain why it doesn't apply. Ignoring your own theme is weak.

**Variable Snapshots**: Different paths can reach the same ending ID but with different variable states. This is GOOD — it shows player choices matter. Always include prose variants or metadata showing how the same ending plays differently based on player history.

---

## RPG Campaign Ending Notes

### Tabletop Campaign Ending Considerations

**Campaign Epilogue Structure**:
- Tabletop campaigns typically end with a final SESSION (SESSION-N) where the climactic choice/confrontation occurs
- Ending should provide closure for the entire campaign arc, not just the final session
- Example: Campaign spans SESSION-1 through SESSION-9. ENDING-VICTORY plays out in SESSION-9 but references events/relationships from all previous sessions
- Red flags:
  - Ending only addresses SESSION-9 events (feels episodic, not campaign-level)
  - Ending ignores major plot threads from SESSION-3-6 (feels incomplete)
  - No acknowledgment of how party's journey from SESSION-1 led to this outcome

**Companion Fate Resolution**:
- Each companion must have an explicit fate in the ending (alive, dead, left party, sacrificed, ascended, etc.)
- Companion fate should reflect their loyalty arc (loyal companion gets honored/survives; betrayed companion faces consequences)
- Example: Sir Theron joined in SESSION-2 with loyalty(theron) starting at 0. If loyalty reached +3, ending describes him as honored ally standing by party. If loyalty reached -3, ending describes him as estranged or fallen in service.
- Red flags:
  - Companion recruited in SESSION-2 never mentioned in final ending
  - Companion's fate contradicts their loyalty arc (loyal companion suddenly abandoned)
  - Party roster change not acknowledged ("the party of four" but only three companions with defined fates)

**Faction Outcome Clarity**:
- Each faction the party interacted with should have a stated outcome (won, lost, neutral, alliance, enmity)
- Faction outcome should reflect faction reputation trajectory (high reputation → favorable outcome; low reputation → unfavorable outcome)
- Example: If Temple of Light had faction_reputation = +3 (favorable), ending might state "The Temple leadership publicly acknowledges your service" or "Temple doors open to you forever"
- Red flags:
  - Faction mentioned in SESSION-3 quest never appears in ending
  - Faction reputation was -5 (hostile) but ending shows them as allies
  - Multiple factions with no clear winner/loser (feels inconsequential)

**Ruleset-Specific Ending Resolutions**:

**D&D 5e**:
- Spell effects (bless, curse, geas) should be resolved (removed or acknowledged as permanent)
- Conditions (charmed, frightened, stunned) should be cleared or acknowledged as permanent disability
- Ability score reductions should be addressed (if ability score was reduced by curse, is it restored?)
- Example: Party was cursed to -2 Charisma in SESSION-4. Ending should explicitly state curse is lifted (or accepted as permanent consequence)

**Pathfinder 2e**:
- Critical success outcomes should be honored in ending consequences (not ignored)
- Conditions (panicked, off-guard, etc.) should be cleared or acknowledged
- Persistent damage should cease or transition to permanent scarring
- Example: If party achieved 4 critical successes on final boss negotiation, ending reflects the exceptional outcome (not same as regular success ending)

**Shadowrun 6e**:
- Karma pool final value should be stated (shows resource usage throughout campaign)
- Edge pool exhaustion should be addressed (did player save Edge for final moment?)
- Matrix/Physical separation should have outcomes for both roles (hacker and physical team both get resolution)
- Unfinished contracts should be addressed ("The Johnson still owes you nuyen..." or "The contract is closed")
- Example: `$karma_remaining = 2` at final session. Ending might show party low on resources, making tough choice with limited magical support

**Player Introduction Acknowledgment**:
- Each player receives SESSION-1-BRIEFING.md with personal hook ("Your sister was kidnapped by the cult")
- Final ending should acknowledge and resolve this personal hook
- Example: If player hook was "Find sister", ending should explicitly state sister is found (or confirmed dead, or left behind), not just mention victory over cult
- Red flags:
  - Final ending makes no reference to personal introduction hook
  - Personal story left unresolved ("You never learned what happened to your sister")
  - Personal hooks vary by player but ending is generic (doesn't personalize closure)

### Computer Game Ending Considerations

**Route-Specific Ending Variants**:
- Each playstyle route (Stealth, Combat, Diplomacy) can have distinct ending variant with different prose, outcomes, and NPC reactions
- Ending should reflect the player's choice commitment (Stealth route ending shows stealth-based approach to final confrontation, not generic victory)
- Example:
  - STEALTH ROUTE: Ending shows silent infiltration success, enemies never saw player coming, quiet resolution
  - COMBAT ROUTE: Ending shows dramatic final battle, enemies fought honorably, victory hard-won
  - DIPLOMACY ROUTE: Ending shows negotiated peace, enemies become allies, non-violent resolution
- Red flags:
  - All three routes have identical ending prose (wastes route design)
  - One route's ending feels better-written or more rewarding than others (creates fairness problem)
  - Ending contradicts route commitment (Stealth route ending shows open combat)

**Accessibility Consistency in Endings**:
- If player selected colorblind mode, final ending cinematics/visual sequences must support colorblind vision
- If player selected audio mode, ending must provide audio cues for critical story moments (not rely on visual-only cutscenes)
- If player selected motor accessibility, ending button mashing or quick-time events should be optional or fully remappable
- Example:
  - COLORBLIND MODE: Final boss defeat cutscene doesn't use color-only visual effects; shapes/patterns are distinct
  - AUDIO MODE: Ending cinematic includes audio narration of text dialogue (not just subtitles with silent actors)
  - MOTOR ACCESSIBILITY: Ending doesn't require precise timing on controllers; story unfolds at player pace
- Red flags:
  - Accessibility mode set but ending cinematics ignore it
  - Colorblind mode disabled for "true experience" in ending
  - Audio mode players get silent ending cinematics

**Route Commitment Acknowledgment**:
- Ending should explicitly reference the player's route choice
- NPCs should react to the player's approach (Stealth NPC: "Your quiet approach saved lives"; Combat NPC: "Your strength won the day")
- Example: If player committed to Stealth in CHAPTER-2, final ending dialogue includes recognition of that choice
- Red flags:
  - NPC ending dialogue makes no reference to player's route choice
  - All routes get identical NPC reactions (defeats route customization)
  - Route commitment treated as irrelevant to ending narrative

**Chapter-to-Chapter Continuity in Ending**:
- Ending should reference major decisions from CHAPTER-2-4 (route commitment, accessibility mode usage, story-critical choices)
- Example: If player chose Accessibility Mode in CHAPTER-1 and used it throughout, ending should acknowledge adaptation (not pretend player was unassisted)
- Red flags:
  - CHAPTER-2 route choice never mentioned again in ending
  - CHAPTER-3-4 consequences ignored (ending acts as if those chapters didn't matter)
  - Accessibility mode treated as cheat/limitation rather than valid playstyle

**Cross-Route Fairness**:
- Each route's ending should feel equally satisfying and equally long
- No route should get materially better rewards, epilogues, or narrative closure than others
- Example:
  - STEALTH: 3-minute ending cinematic, positive outcome
  - COMBAT: 3-minute ending cinematic, positive outcome
  - DIPLOMACY: 3-minute ending cinematic, positive outcome
  - (Different outcomes, but equal weight and screen time)
- Red flags:
  - Stealth ending: 5 minutes, "perfect" victory
  - Combat ending: 2 minutes, "pyrrhic" victory with heavy losses
  - Diplomacy ending: 1 minute, "compromise" ending (treated as lesser)

### Ruleset-Specific Ending Considerations

**D&D 5e Campaign Endings**:
- Ability scores affected by curse/age should be addressed
- Long-term blessings/curses should be resolved or acknowledged
- Example: If campaign involved geas (magical compulsion), ending should show geas lifted or accepted as permanent condition
- Party level should feel earned (ending feels appropriately epic for party's level)

**Pathfinder 2e Campaign Endings**:
- Persistent conditions (doomed, drained, frightened) should be cleared or acknowledged
- Critical success/failure outcomes in final scenes should be honored
- Example: If final negotiation roll was critical success, outcome should reflect exceptional result

**Shadowrun 6e Campaign Endings**:
- Final karma/edge pool state should be shown or acknowledged
- Matrix/Physical teams should both get resolution (not just one or the other)
- Outstanding contracts/debts should be closed or acknowledged
- Example: Campaign involved 3 johnson contracts. Ending should address status of each (completed, failed, ongoing)

