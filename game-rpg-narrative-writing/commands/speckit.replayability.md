---
description: Replayability metrics — measure unique content per playthrough, branch coverage, variation in dialogue/prose, and content reuse across paths. For RPG campaigns (tabletop D&D/Pathfinder/Shadowrun and computer game), measures companion loyalty paths, faction outcomes, session variants, playstyle route distinctness, and ruleset-specific mechanical variation.
handoffs:
  - label: Check Agency
    agent: speckit.agency
    prompt: After measuring replayability, verify choices provide meaningful variations.
    send: true
  - label: Analyze Complexity
    agent: speckit.complexity
    prompt: Review branch structure to optimize replayability coverage.
    send: true
---

# speckit.replayability

**RPG Campaign Support**: Adapts replayability metrics for tabletop (companion loyalty paths, faction outcomes, session variants, ruleset-specific mechanics) and computer game (playstyle routes, route-exclusive content, accessibility variants, chapter progression).

Replayability metrics — measure **unique content per playthrough, branch coverage, dialogue variation, and content reuse**. Helps optimize for "want to play again" factor.

## Replayability Principle

**High replayability** = Each playthrough reveals different content, choices lead to distinct experiences, player has reason to see other branches.

**For RPG campaigns** (tabletop): Different campaigns, companion rosters, faction standings, session structures
**For RPG campaigns** (computer): Different playstyle routes, route-exclusive encounters, accessibility variant experiences

**Low replayability includes**:
- ❌ Same prose in all branches (only variables change)
- ❌ High content reuse (>70% of prose is shared across branches / routes)
- ❌ Limited branching (all paths converge quickly)
- ❌ Predictable outcomes (choices don't produce surprising variations)
- ❌ [Tabletop] Same companion roster appears in all campaigns (loyalty choices don't matter)
- ❌ [Tabletop] All factions have identical outcomes regardless of player choices
- ❌ [Computer] All routes have identical encounters (route choice cosmetic)
- ❌ [Computer] Accessibility modes treated as difficulty levels, not accessibility

**Valid replayability includes**:
- ✅ Distinct prose per branch (each path has unique dialogue/scenes)
- ✅ Moderate content reuse (40–60% shared, rest branch-specific)
- ✅ Multiple endings with meaningful differences
- ✅ Hidden content (only revealed in certain branches)
- ✅ Variant NPCs (different characters appear per path)
- ✅ [Tabletop] Multiple campaigns with different session structures, companion rosters vary by loyalty path
- ✅ [Tabletop] Faction outcomes differ noticeably (Temple victory ≠ Thieves Guild victory)
- ✅ [Tabletop] Ruleset-specific mechanics create mechanical variety (D&D 5e conditions affect encounters differently than Shadowrun 6e karma)
- ✅ [Computer] Each playstyle route (Stealth/Combat/Diplomacy) has unique encounters and NPCs
- ✅ [Computer] Route-exclusive choices lock out other route content (commit to one path)
- ✅ [Computer] Accessibility variants create distinct presentations without breaking playability

## User Input

```text
$ARGUMENTS
```

Accepted input:
- Nothing — analyze overall replayability metrics
- `--branch [BRANCH_ID]` — analyze replayability within one branch only
- `--content` — focus on unique prose content per branch

Optional flags:
- `--strict` — flag >50% content reuse as excessive
- `--show-coverage` — ASCII grid of which branches see which content
- `--show-variance` — display variant prose per branch
- `--unique-only` — show only branch-specific content (hide shared prose)

## Pre-Execution Checks

**Auto-detect platform and ruleset** (for RPG campaigns):
- Load `constitution.md`
- Extract `[PLATFORM]` (tabletop/computer) and `[RULESET]` (D&D 5e/Pathfinder 2e/Shadowrun 6e)
- Set SESSION object {platform, ruleset, mechanics}
- If RPG: Load `companions.md`, `factions.md`, `mechanics-[RULESET].md`, `plan.md` (for session/chapter structure)

**Standard checks**:
1. Load `specs/plan.md`: Branch structure, node mapping
2. Load all `draft/[ENGINE]/NODE-*.md` files (or SESSION-N files for tabletop)
3. Parse prose content (separate from code/mechanics)
4. Identify shared vs. branch-specific nodes
5. Calculate word count per branch type
6. Trace which nodes are reachable per branch
7. If RPG: Identify companion-dependent paths, faction-dependent outcomes, route-exclusive content

## Execution Steps

### 1. **Measure Unique Content Per Branch**

For each branch, measure original prose:

```
Content accounting:

Shared nodes (all branches visit):
  NODE-001 through NODE-010: 10 nodes
  Total prose: 5,500 words
  Reachability: 100% (every playthrough includes)

Branch A (Help Victor):
  NODE-015, NODE-020, NODE-025 (6 variants): 3,200 words
  Reachability: A path only
  Exclusivity: 0% shared with B/C (100% unique to A)

Branch B (Betray Victor):
  NODE-016, NODE-021, NODE-026: 2,800 words
  Reachability: B path only
  Exclusivity: 0% shared with A/C (100% unique to B)

Branch C (Flee):
  NODE-017, NODE-022, NODE-027: 2,100 words
  Reachability: C path only
  Exclusivity: 0% shared with A/B (100% unique to C)

Totals:
  • Shared: 5,500 words (45%)
  • Branch-specific: 8,100 words (55%)
  • Total: 13,600 words

Per-playthrough content:
  • Branch A playthrough: 5,500 (shared) + 3,200 (A) = 8,700 words
  • Branch B playthrough: 5,500 (shared) + 2,800 (B) = 8,300 words
  • Branch C playthrough: 5,500 (shared) + 2,100 (C) = 7,600 words
  
Content overlap between playthroughs:
  • A vs B overlap: 5,500 / 8,700 = 63% (large shared content)
  • A vs C overlap: 5,500 / 8,700 = 63%
  • B vs C overlap: 5,500 / 8,300 = 66%

Unique content per fresh playthrough:
  • Playthrough 1: 100% unique
  • Playthrough 2: 37% unique (65% shared with playthrough 1)
  • Playthrough 3: 37% unique (65% shared with previous plays)
```

### 2. **Calculate Content Reuse Ratio**

Measure how much prose is recycled across branches:

```
Content reuse matrix:

         A      B      C
A        —     5,500  5,500
B      5,500   —     5,500
C      5,500  5,500   —

Reading: Row A, Column B = both A and B contain the shared 5,500-word intro

Reuse percentage:
  • A–B overlap: 5,500 / (3,200 + 2,800) = 5,500 / 6,000 = 92% (very high)
    Interpretation: 92% of branch-specific content is actually shared
  
  • A–C overlap: 5,500 / (3,200 + 2,100) = 5,500 / 5,300 = 104% ???
    Wait, that's >100%; recalculate using union instead
  
  Better formula (Jaccard similarity):
  overlap / (A_content + B_content - overlap)
  = 5,500 / (8,700 + 7,600 - 5,500)
  = 5,500 / 10,800
  = 51% (moderate)

Interpretation:
  • 51% of content is seen in both A and C paths
  • 49% of content is unique to each branch
  • This is GOOD (neither over-reused nor too sparse)

Reuse assessment by category:
  • <30% reuse: Too branch-specific (wasteful, no consistency)
  • 30–50% reuse: Good balance (consistent intro, unique development)
  • 50–70% reuse: Moderate (shared story with variations)
  • >70% reuse: Excessive (feels like only variables change)
  
This game: 51% reuse = ✅ GOOD BALANCE
```

### 3. **Analyze Content Variation Per Branch**

Examine how prose differs across similar scenes:

```
SCENE: "Confronting Marcus" (appears in all branches)

Branch A version:
  "Marcus sits across from you, hands folded.
   'You helped Victor escape,' he says quietly.
   'I know it was the right choice.'
   His expression has changed—there's respect there."
   
Prose quality: Warm, accepting tone
Word count: 45 words
Mechanical effect: relationship_marcus += 10

Branch B version:
  "Marcus stands when you enter, face dark with anger.
   'You let him go,' he hisses.
   'Victor will cause more death.'
   His jaw clenches. He won't even look at you."
   
Prose quality: Cold, disappointed tone
Word count: 42 words
Mechanical effect: relationship_marcus -= 15

Branch C version:
  "Marcus shows no reaction when you walk in.
   'You ran,' he observes.
   'Smart. I would have done the same.'
   He returns to his paperwork, dismissing you."
   
Prose quality: Detached, pragmatic tone
Word count: 38 words
Mechanical effect: relationship_marcus += 0

Variation analysis:
  • All three versions address same event (confrontation)
  • All three have same mechanical purpose (affect relationship)
  • Prose DIFFERS significantly (warm vs cold vs indifferent)
  • Tone REFLECTS branch outcomes (aligned with Victor choice)
  
Content variation quality: ✅ EXCELLENT
              (Same scene, different prose, supports narrative)
```

### 4. **Detect Replayability Problems**

#### 🔴 **PROBLEM: Same Prose Across Branches**
Multiple branches have identical dialogue despite different contexts.

```
Branch A (Help Victor):
  NODE-020: "The city gate opens. You slip through."

Branch B (Betray Victor):
  NODE-020: "The city gate opens. You slip through."

Branch C (Flee):
  NODE-020: "The city gate opens. You slip through."

Problem: All three branches have IDENTICAL prose
         Yet outcomes are completely different (help/betray/flee)
         This feels fake—prose should reflect choice
         
Status: 🔴 SAME PROSE, DIFFERENT CHOICES

Fix options:
  1. Rewrite prose for each branch (B1: grateful escape, B2: guilty escape, C: cowardly escape)
  2. Use variable prose (if help: "...grateful"; if betray: "...guilty")
  3. Move this shared prose earlier (before divergence)
  
Impact: Players who replay feel like they're reading same content
        Reduces replayability
```

#### 🟡 **PROBLEM: Excessive Content Reuse**
>70% of content is shared across branches; branches feel cosmetic.

```
Game structure:
  • Shared nodes: 40 nodes
  • Branch A: 2 unique nodes
  • Branch B: 2 unique nodes
  • Branch C: 2 unique nodes
  
Reuse calculation:
  Shared: 40 nodes
  Total unique content: 6 nodes
  Reuse ratio: 40 / (40 + 6) = 87%
  
Problem: 87% reuse is excessive
         Feels like only variables change, not actual story
         Branches lack distinct identity
         
Status: 🟡 EXCESSIVE REUSE

Example: If reuse is >70%, the question becomes:
         "Am I really playing a different game, or just the same game with different flags?"

Fix options:
  1. Expand branch-specific content (write more unique scenes)
  2. Consolidate branches (merge similar paths into one)
  3. Keep >70% reuse if intentional (e.g., "same story, different player stats")
```

#### 🟠 **PROBLEM: Limited Branching**
Branches converge so quickly that unique content per path is minimal.

```
Design:
  NODE-001 (shared, 10 nodes)
  NODE-010 [divergence]: 3 branches
  NODE-015 [reconvergence]: All branches meet
  NODE-020+ (shared)
  
Content per branch:
  A: NODE-011, NODE-012, NODE-013 (3 nodes, ~600 wc)
  B: NODE-011, NODE-012, NODE-013 (same nodes, different prose) ???
  
Problem: Branch A and B share THE SAME NODE IDs
         But with different prose variants
         This is variable-based branching, not node branching
         
Results in:
  • Branch A: 10 (shared) + 3 (variant) = 13 nodes total
  • Branch B: 10 (shared) + 3 (variant) = 13 nodes total
  • Unique content: 3 nodes × 2 variants = only 6 unique nodes of actual branching
  
Replayability: ⚠️ LIMITED
              With quick reconvergence, branches feel superficial
              
Assessment: Is this acceptable?
  ✅ YES if: variants are SIGNIFICANTLY different (large prose changes, different mechanics)
  ❌ NO if: variants are cosmetic (same story, different flavor text)
```

#### 💨 **PROBLEM: Hidden Content Never Revealed**
Content exists in some branches but is inaccessible to most players.

```
Game structure:
  3 main branches (Help / Betray / Flee)
  
Branch A only content (secret scene):
  NODE-020A: Special dialogue with Marcus (only if relationship > 80)
  Content: 1,200 words (10% of branch A content)
  
Reachability:
  • Requires: Help Victor + Violent approach + no prior betrayals
  • Reachable in: 1 of 3 main paths
  • Percentage of players seeing it: ~33% (if distribution is even)
  
Problem: If players don't explore all branches, they'll miss content
         Hidden content isn't replayability if it's required for "completion"
         But if it's optional bonus: it's GOOD for replayability
         
Status: ✅ IF INTENTIONAL BONUS, otherwise 💨 WASTED CONTENT

Question: Is this secret designed to be found?
         Or accidentally hidden?
         
If intentional: mark it clearly (Achievements, guides)
If accidental: either remove or move to more accessible branch
```

### 5. **Generate Replayability Report**

Create `specs/replayability-audit.md`:

```markdown
## Replayability Audit

**Game**: [NAME]
**Date**: [ISO]

### Content Metrics

| Metric | Value | Assessment |
|--------|-------|------------|
| Total prose | 13,600 wc | Good volume |
| Shared content | 5,500 wc (40%) | ✅ Balanced |
| Branch-unique | 8,100 wc (60%) | ✅ Good variation |
| Content reuse | 51% | ✅ Healthy |
| Avg playthrough | 8,200 wc | ~40 min reading |
| Fresh content per playthrough | 37% | Moderate |

### Branch Coverage

| Branch | Playthrough | Unique | Reuse | Content |
|--------|------------|--------|-------|---------|
| A | 8,700 wc | 3,200 wc | 63% | Redemption |
| B | 8,300 wc | 2,800 wc | 66% | Tragedy |
| C | 7,600 wc | 2,100 wc | 72% | Escape |

### Replayability Assessment

**Content variation**: ✅ GOOD
- Each branch has distinct prose and tone
- Choice consequences reflected in prose variations
- No identical scenes across branches

**Branch distinctness**: ✅ GOOD
- 3 main branches with clear thematic differences
- A: Redemption (relationship +10 with Marcus, Victor escaped)
- B: Betrayal (relationship -15, Victor captured)
- C: Escape (relationship neutral, Victor fate ambiguous)

**Hidden content**: ✅ INTENTIONAL BONUS
- Secret scene in Branch A (relationship > 80)
- Discoverable on 2nd playthrough
- Not required for completion

**Replayability score**: 7/10

### Issues

**🔴 None critical**

**🟡 Moderate**:
1. Branch C has lowest unique content (2,100 wc)
   Consider: Add one more Branch C unique scene (~1,000 wc)

**Opportunities**:
1. Add hidden dialogue variant in Branch B (if relationship > 50 despite betrayal)
2. Consider alternate ending in Branch A (romantic vs platonic reconciliation)

### Recommendations

**For higher replayability** (if desired):
1. Expand Branch C to match A/B in unique content
2. Add 1–2 more choice points to create sub-variants (currently A has 1 sub-choice)
3. Consider new game+ content (unlocks after completing 1 branch)
4. Mark secrets clearly so players know they missed content

**Current design**: ✅ Solid baseline replayability
                   Players will want to see all 3 branches
                   Each playthrough offers ~37% new content
                   Recommend for players who like branching narratives
```

### 6. **Show Coverage** (optional with --show-coverage)

ASCII grid of which nodes appear in which branches:

```
CONTENT COVERAGE MATRIX

Node        A  B  C  Shared  Unique
────────────────────────────────────
NODE-001    ✅ ✅ ✅  YES      —
NODE-005    ✅ ✅ ✅  YES      —
NODE-010    ✅ ✅ ✅  YES      —
NODE-015    ✅ ❌ ❌  NO       A only
NODE-020A   ✅ ❌ ❌  NO       A (secret)
NODE-016    ❌ ✅ ❌  NO       B only
NODE-021    ❌ ✅ ❌  NO       B only
NODE-017    ❌ ❌ ✅  NO       C only
NODE-022    ❌ ❌ ✅  NO       C only
NODE-025    ✅ ✅ ✅  YES      —
────────────────────────────────────

Shared content: 5 nodes (visible in all paths)
A-only: 2 nodes (NODE-015, NODE-020A)
B-only: 2 nodes (NODE-016, NODE-021)
C-only: 2 nodes (NODE-017, NODE-022)

Key insight:
  • Half of game is shared introduction
  • Each branch has ~2 unique scenes
  • Very little overlap between B and C content
  • A has extra secret scene (NODE-020A)
```

### 7. **Show Variance** (optional with --show-variance)

Display variant prose for identical scene points:

```
SCENE: "Confronting Marcus"

─ Branch A (Help Victor) ─
"Marcus sits across from you, hands folded.
 'You helped Victor escape,' he says quietly.
 'I know it was the right choice.'
 His expression has changed—there's respect there."
[+10 relationship]

─ Branch B (Betray Victor) ─
"Marcus stands when you enter, face dark with anger.
 'You let him go,' he hisses.
 'Victor will cause more death.'
 His jaw clenches. He won't even look at you."
[-15 relationship]

─ Branch C (Flee) ─
"Marcus shows no reaction when you walk in.
 'You ran,' he observes.
 'Smart. I would have done the same.'
 He returns to his paperwork, dismissing you."
[+0 relationship]

Prose variations:
  A: Warm, accepting (seated, makes eye contact, praises)
  B: Angry, disappointed (stands, won't look at you, hisses)
  C: Detached, pragmatic (ignores you, returns to work)
  
Quality: ✅ EXCELLENT variation
         (Same scene beats, completely different emotional tone)
```

### 8. **Report**

Output `replayability-audit.md` with:
- Content metrics (total prose, shared vs unique, reuse ratio)
- Branch coverage analysis (what % of content is per-branch-only)
- Replayability score (1–10)
- Assessment of variation quality
- If `--show-coverage`: Content coverage matrix
- If `--show-variance`: Variant prose for key scenes
- If `--unique-only`: Only branch-specific content (hide shared intro)

---

## Important Notes

**Content Reuse 40–60% Is Ideal**: Allows consistency (shared world-building) while maintaining branch distinctness. Anything >70% starts feeling repetitive; anything <30% wastes effort.

**Hidden Content Has Diminishing Returns**: Most players won't see all branches on first playthrough. Hidden content is a bonus for completionists. Don't hide critical story behind low-probability branches.

**"New Game+" Extends Replayability**: If you unlock content after completing a branch, players have reason to replay. Sequential content unlock is powerful.

**Prose Quality > Quantity**: A 5,000-word unique branch with identical prose feels worse than a 2,000-word branch with totally distinct voice. Variation matters more than volume.

**Player Motivation Matters**: Players replay because:
1. Multiple endings (want to see them all)
2. Different protagonist choices (want to play their way)
3. Unlockable content (want to complete collection)
4. Challenge/speedrun (want optimal path)

Design for at least 1–2 of these motivations to maximize replayability.

---

## RPG Campaign Replayability Notes

### Tabletop Campaign Replayability Considerations

**Companion Loyalty Path Replayability**:
- Each loyalty path should unlock different campaign structures across sessions
- Example: Loyal party (all companions at +3 loyalty) → ACCESS SESSION-5A (final ritual with full party)
           Mixed loyalty (some high, some low) → ACCESS SESSION-5B (fractured party, some companions absent)
           All low loyalty → ACCESS SESSION-5C (solo campaign, companions abandoned you)
- Red flags:
  - Loyalty changes don't affect which SESSION-N variants appear
  - Companion roster is identical regardless of loyalty scores
  - No prose differences reflecting loyalty relationships
- Best practice: 2-3 major campaign structures based on companion loyalty distribution; each structure has distinct finale
- Measurement: Calculate replayability score separately for each loyalty configuration (what content unique to loyal path vs mixed vs betrayal path)

**Faction Outcome Replayability**:
- Each faction victory should produce noticeably different SESSION-N content and finale
- Example: Temple victory → SESSION-3 onwards has Temple NPC support, FINALE has Temple blessing mechanic
           Thieves Guild victory → SESSION-3 has underground passages, FINALE has guild safehouse as base
           Neutral → SESSION-3 has freelancer quests, FINALE has no faction aid
- Red flags:
  - Faction victory mentioned but doesn't change gameplay or encounters
  - All three faction endings lead to same finale (faction choice cosmetic)
  - Faction-specific NPCs appear regardless of faction standing
- Best practice: 3 distinct campaign structures (one per faction); each with unique encounters, NPCs, session progression
- Measurement: Calculate % unique prose per faction path (should be 30-50% faction-specific content per campaign run)

**Session-Based Branching**:
- Earlier session choices should branch into multiple possible SESSION-N structures
- Example: SESSION-2 choice to ally with Militia → affects SESSION-3-5 encounters, NPC availability, final confrontation
           SESSION-2 choice to betray Militia → different SESSION-3-5 structure (militia becomes enemies)
- Red flags:
  - SESSION-2 choice never mentioned again after SESSION-2
  - All sessions follow same structure regardless of earlier choices
  - Session encounters are identical (only dialogue changes based on flags)
- Best practice: Each major SESSION-N choice point locks in distinct SESSION-(N+1) structure; verify 2-3 session lookahead consequences
- Measurement: For each session divergence point, calculate word count delta between branches (should be 10-20% different content per branch)

**Ruleset-Specific Mechanical Replayability**:
- Mechanical differences should create replay-worthy variations (not just flavor)
- D&D 5e: Condition effects in sessions (Frightened status affects combat encounters differently across sessions)
  - Example: SESSION-3 curse → SESSION-4-5 have curse-affected rolls, changing success rates, forcing tactical adjustments
  - Replayability: Playing curse vs no-curse path offers mechanically different SESSION-4 encounters
- Pathfinder 2e: Critical success/failure cascades (critical successes in SESSION-N unlock SESSION-(N+1) shortcuts)
  - Example: Critical success in SESSION-2 negotiation → gain faction ally in SESSION-3 who wasn't available otherwise
  - Replayability: Re-running SESSION-2 with different approach might unlock different SESSION-3
- Shadowrun 6e: Karma depletion across sessions (spending Karma SESSION-3 reduces options SESSION-4)
  - Example: Spend 10 karma SESSION-3 → less Karma available for final boss SESSION-5 → forces different tactics
  - Replayability: Players replay with different Karma spending strategy to unlock easier finale
- Measurement: Identify mechanical bottlenecks; verify they create meaningfully different session experiences

**Campaign Variant Generation**:
- Build 2-3 "exemplar campaigns" to show replayability (e.g., loyal-Temple campaign vs neutral-Militia campaign)
- Explicitly calculate that campaign_A and campaign_B share 45-55% content but have distinct structures
- Identify if players have sufficient reason to run different campaign variants (different factions, different companion rosters, different mechanical paths)

### Computer Game Route Replayability Considerations

**Playstyle Route Content Distinctness**:
- Each route (Stealth/Combat/Diplomacy) should have 30-50% unique content vs shared content
- Measure reuse ratio separately per route:
  - Shared content (all routes): 40% of game
  - Stealth-exclusive: 25% (lock-picking scenes, shadow detection encounters)
  - Combat-exclusive: 25% (martial encounters, weapon tactics scenes)
  - Diplomacy-exclusive: 25% (negotiation scenes, relationship-building encounters)
- Red flags:
  - One route has <15% unique content (feels same as others)
  - One route has >60% unique content (feels disconnected from main story)
  - Routes converge too early (all differences erased by CHAPTER-3)
- Best practice: Each route has distinct encounter types, NPCs, and solutions; convergence points acknowledge all routes differently
- Measurement: Build content audit table showing shared vs exclusive % for each route

**Route-Exclusive Content Measurement**:
- Hidden content in one route shouldn't penalize players in other routes
- Example: Stealth route hidden scene (blacksmith's backstory) should NOT be required for Diplomacy route finale
- Red flags:
  - Critical story information locked to one route
  - One route has significantly more hidden content than others
  - Route-exclusive content contradicts shared story
- Best practice: Hidden content is bonus (achievement unlocks, gallery additions), not critical story
- Measurement: Verify no critical content is route-exclusive; count optional content per route (should be balanced)

**Accessibility Variant Replayability**:
- Accessibility modes (colorblind/audio/motor) should provide distinct experiences without difficulty advantage
- Example: Colorblind mode uses pattern + color for puzzles; Audio mode uses spatial + visual for puzzles
           Neither should be "easier", just different presentation
- Red flags:
  - Colorblind mode solves puzzles faster than normal (unfair advantage)
  - Audio mode disables story content (accessibility as punishment)
  - Accessibility variants treated as difficulty levels
- Best practice: Each accessibility mode has same challenge, different presentation; replayability comes from "how did other players experience this?"
- Measurement: Measure puzzle difficulty (time-to-solve, hint usage) in each accessibility mode; verify no statistical difference

**Chapter-Based Branching**:
- CHAPTER-2 route commitment should lock in distinct CHAPTER-3-5 structures
- Example: Stealth route in CHAPTER-2 → CHAPTER-3-5 have shadow mechanics, infiltration encounters, stealth-only bosses
           Combat route → different boss encounters (direct confrontation vs evasion)
- Red flags:
  - Route choice never mechanically affects encounters after CHAPTER-2
  - All chapters have identical encounter structure with different prose
  - Route commitment feels cosmetic
- Best practice: Each route should have mechanically distinct encounters (not just themed NPCs)
- Measurement: For each encounter, verify Stealth/Combat/Diplomacy solutions are equally viable but mechanically different

**Route Convergence Balance**:
- If routes reconverge (common finale), verify each route has equivalent replayability motivation to reach convergence
- Example: All routes → same final boss, but:
  - Stealth route: infiltrate secretly, avoid confrontation if possible
  - Combat route: heroic final battle with reinforcements
  - Diplomacy route: negotiate surrender, convince enemies to stand down
  - All lead to same boss defeat but mechanically different
- Red flags:
  - Routes reconverge too early (lose route distinctness)
  - Routes never reconverge (three separate games, not variants)
  - Convergence creates plot holes (route-exclusive events ignored)
- Best practice: Reconverge in final chapter; ensure each route's perspective is acknowledged in conclusion
- Measurement: For convergence scenes, verify each route sees route-appropriate content (not generic dialogue)

---

## RPG Campaign Replayability Best Practices

**Tabletop Campaign Replayability**:
- Design campaigns with 2-3 branching points per session (loyalty choices, faction choices, mechanical decisions)
- Verify each major branch has 15-25% unique content compared to others
- Create "exemplar campaigns" document showing 3 distinct campaign paths (loyal-Temple, neutral-Militia, betrayal-Thieves Guild)
- Test that companion roster actually varies by loyalty distribution (verify not all companions appear in all campaigns)
- Ruleset-specific mechanics should create mechanical variance (not just prose variance)
- Measure cross-campaign replayability: Players should see 40-60% new content on second campaign

**Computer Game Route Replayability**:
- Each route should commit early (CHAPTER-2) and maintain mechanical distinctness through finale
- Design 30-50% unique content per route (25% shared infrastructure, 25% route-exclusive)
- Verify route-exclusive content is bonus/optional (no critical story locked to one route)
- Create route-specific endings that acknowledge route choice (not generic finale for all routes)
- Accessibility modes should not reduce content or difficulty (only change presentation)
- Measure cross-route replayability: Players should see 30-50% new content on second playthrough

**Shared Across Both Platforms**:
- Replayability score should be 6-8/10 (players motivated to see most branches)
- Hidden content should be bonus (20-30% of players find it), not required
- Prose variation between branches should be noticeable (not just variable substitution)
- Content reuse should be 40-60% (balances consistency with distinctness)
- Test by playing through each branch: Each playthrough should feel meaningfully different, not like replaying same content with different flags
- Calculate actual replayability: (unique_content_per_branch / total_content_per_branch) × 100 should be 30-50%

