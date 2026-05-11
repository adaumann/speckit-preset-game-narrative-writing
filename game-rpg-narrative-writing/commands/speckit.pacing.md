---
description: Story pacing analyzer — measure word count, beat spacing, emotional tempo, and reading time per branch. Detects pacing problems (info dumps, draggy sections, rushed climax).
handoffs:
  - label: Check Tone
    agent: speckit.tone
    prompt: After analyzing pacing, validate emotional beats align with pace.
    send: true
  - label: Revise Pacing
    agent: speckit.revise
    prompt: Some sections have pacing problems. Please adjust prose length and beat spacing.
    send: true
---

# speckit.pacing

Story pacing analyzer — measure **word count, beat spacing, emotional tempo, and reading time** per branch. Detects problems: info dumps, draggy middle, rushed climax, dead zones.

## Pacing Principle

**Good pacing** = Emotional beats, prose length, and scene changes maintain consistent reading rhythm; player never feels bored or overwhelmed.

**Bad pacing includes**:
- ❌ Info dump (1,000+ word exposition block with no dialogue/action)
- ❌ Draggy middle (sequences where nothing changes; minimal prose but feels slow)
- ❌ Rushed climax (2,000 words leading to 500 word payoff)
- ❌ Dead zones (nodes with low word count AND no emotional/mechanical change)
- ❌ Inconsistent node size (NODE-010 is 300 words, NODE-011 is 4,000 words for same scene weight)

**Valid pacing includes**:
- ✅ Varied node length (300–3,000 words) reflecting emotional weight
- ✅ Short nodes for decisions/transitions
- ✅ Long nodes for climactic moments
- ✅ Beat spacing matches emotional progression (clusters during tension, space after climax)
- ✅ Reading time roughly equal across same-weight story phases

## User Input

```text
$ARGUMENTS
```

Accepted input:
- Nothing — analyze entire game pacing across all branches
- Branch ID (e.g., `BRANCH-A`) — analyze pacing in one branch only
- `--act [N]` — analyze pacing of a single act only
- `--node [NODE-ID]` — analyze one node in detail

Optional flags:
- `--strict` — flag any node >2,500 words or <100 words
- `--target-wc [NUMBER]` — custom target word count per node (default: 800)
- `--show-stats` — display full statistics table
- `--show-graph` — ASCII graph of word count per node

## Pre-Execution Checks

**Extract Platform & Ruleset** (auto-detect RPG context):
- Read `.specify/memory/constitution.md` YAML frontmatter and extract `[PLATFORM]` and `[RULESET]`
- If `[PLATFORM]` = "Tabletop": Set `SESSION.is_rpg = "tabletop"` and activate Tabletop RPG pacing analysis (session-based, encounter-based)
- If `[PLATFORM]` = "Computer Game": Set `SESSION.is_rpg = "computer"` and activate Computer Game RPG pacing analysis (route-based, difficulty-scaled)
- If neither detected: Set `SESSION.is_rpg = false` (generic game pacing)
- Store `SESSION.platform` and `SESSION.ruleset` for conditional pacing strategy selection

1. Load `specs/plan.md`: Branch structure, act boundaries, **session groupings (if Tabletop)**
2. Load all `draft/[ENGINE]/NODE-*.md` files
3. Parse node prose (exclude YAML frontmatter, metadata)
4. Identify emotional beat markers (dialogue, action, revelation)
5. Load `specs/constitution.md` target reading time if specified

**RPG-Specific Context** (if `SESSION.is_rpg = true`):
- `specs/mechanics-[ruleset].md` – encounter scaling, skill check mechanics
- `specs/bestiary.md` (if Tabletop) – enemy CR/difficulty profiles
- `draft/campaign-guide.md` (if Tabletop) – session duration targets, pacing goals
- `specs/locations.md` (if Computer) – difficulty scaling notes

## Execution Steps

### 1. **Measure Word Count Per Node**

For each node, count prose words (exclude code/syntax):

```
NODE-010: (drama scene, relationship intro)
  Prose: "The cafe was crowded, but Marcus stood out.
          His dark suit looked expensive, dangerous. 
          He waited at the corner table, watching the door.
          When I entered, his expression didn't change,
          but his hand tightened on the coffee cup."
          
  Word count: 47 words
  Status: ✅ SHORT (appropriate for intro)

NODE-015: (exposition + dialogue)
  Prose: [1,800 words of dialogue explaining backstory]
  Status: ⚠️ LONG (but contains dialogue, so justified)

NODE-020: (climactic confrontation)
  Prose: [2,400 words of action, dialogue, emotional beats]
  Status: ✅ LONG (appropriate for climax weight)

NODE-025: (quiet aftermath)
  Prose: [250 words of reflection]
  Status: ✅ SHORT (appropriate for post-climax space)
```

### 2. **Categorize Nodes by Weight**

Assign emotional/mechanical weight to each node:

```
Weight categories:
  🔴 MAJOR (climax, major choice, major revelation)
     Expected: 1,500–3,000 words
     Example: NODE-020 (confrontation), NODE-015 (plot twist)
  
  🟡 MODERATE (development, dialogue, moderate stakes)
     Expected: 800–1,500 words
     Example: NODE-010 (relationship intro), NODE-017 (subplot progress)
  
  🟢 MINOR (transition, decision point, brief scene)
     Expected: 300–800 words
     Example: NODE-005 (setup), NODE-025 (quiet moment)
  
  ⚪ MICRO (navigation, brief exchange, mechanical)
     Expected: 50–300 words
     Example: NODE-003 (intro), NODE-012 (door passage)
```

**Node categorization example**:
```
NODE-005: Setting introduction       → MINOR (300–800 wc)
NODE-010: Character intro           → MODERATE (800–1,500 wc)
NODE-015: Major revelation          → MAJOR (1,500–3,000 wc)
NODE-020: Choice moment             → MODERATE (800–1,500 wc)
NODE-025: Aftermath reflection      → MINOR (300–800 wc)
ENDING:   Narrative resolution      → MODERATE/MAJOR (600–2,000 wc)
```

### 3. **Analyze Pacing Per Branch**

Create a pacing timeline:

```
BRANCH A: Redemption Path
═════════════════════════════════════

NODE-005 (MINOR):  50 wc  | Setup intro          | ✅ Appropriate
NODE-010 (MOD):    950 wc | Relationship intro   | ✅ Appropriate
NODE-012 (MOD):    1,200 wc | Dialogue reveal    | ⚠️ LONG but justified (dialogue)
NODE-015 (MAJOR):  2,300 wc | Choice climax      | ✅ Appropriate for weight
NODE-020 (MOD):    800 wc  | Victor escape scene | ✅ Appropriate
NODE-025 (MINOR):  400 wc  | Quiet moment       | ✅ Appropriate
ENDING (MOD):      900 wc  | Resolution         | ✅ Appropriate

Reading time: ~15 minutes
Total words: 6,600 wc
Average node: 943 wc
Pace stability: ✅ GOOD (varied but consistent)

Pacing analysis:
  • Climax (NODE-015) is longest: ✅ Good
  • Post-climax (NODE-020, NODE-025): Short & medium ✅ Good spacing
  • Overall rhythm: Builds to NODE-015, then releases ✅ Satisfying
```

### 4. **Detect Pacing Problems**

#### 🔴 **PROBLEM: Info Dump**
Single node has 2,000+ words of exposition with minimal dialogue/action.

```
NODE-012 (backstory reveal):
  Prose: [2,100 words of character monologue explaining family history]
  
Analysis:
  • Word count: 2,100 wc (HIGH)
  • Dialogue: 5% (minimal)
  • Action: 0% (static)
  • Beat changes: None (single scene, same location, no mechanical change)
  
Problem: Reader must absorb 2,100 words of exposition without break
Status: 🔴 INFO DUMP

Flag: Feels like encyclopedia dump
Fix options:
  1. Break into 2-3 nodes with intervening action
  2. Add dialogue interaction (character responds, interrupts)
  3. Reduce to 1,200 words max with key details only
  4. Move to multiple scenes with dialogue/action interspersed
```

#### 🟡 **PROBLEM: Draggy Middle**
Sequence where nothing mechanically/emotionally changes; minimal prose but feels slow.

```
NODE-013 → NODE-014 → NODE-015:
  
NODE-013 (travel to city):  150 wc
  Prose: "We rode for three days. The landscape changed."
  No decision. No emotional beat. No new information.
  
NODE-014 (arrive at city):  200 wc
  Prose: "The city gates loomed. Guards checked papers."
  No decision. No emotional beat. No new information.
  
NODE-015 (enter tavern):    180 wc
  Prose: "Inside smelled of ale and smoke."
  No decision. No emotional beat. No new information.

Combined: 530 wc across 3 nodes with NO mechanical/emotional change
Reading time: ~3 minutes
Impact: Player feels like progress stalls despite prose

Problem: Transitional beats stretched thin
Status: 🟡 DRAGGY MIDDLE

Flag: These nodes could be combined or cut entirely
Fix options:
  1. Combine into single 300-word transition
  2. Add decision point in NODE-014 (different routes to tavern?)
  3. Add emotional beat (nervous about city? Excited?)
  4. Add NPC interaction (helpful guide? Suspicious merchant?)
```

#### 🟠 **PROBLEM: Rushed Climax**
Climactic moment receives disproportionately short prose compared to build-up.

```
Build-up:
  NODE-010: 1,200 wc (tension rises)
  NODE-012: 1,400 wc (stakes revealed)
  NODE-015: 1,600 wc (choice point)
  Subtotal: 4,200 wc of build-up

Climax:
  NODE-020: 500 wc (confrontation resolved)
  
Analysis:
  Build-up:Climax ratio = 4,200:500 = 8.4:1
  Standard ratio should be ~3:1 to 5:1
  
Problem: 4,200 words of build-up paid off in 500 words
         Feels anticlimactic, rushed, unearned
         
Status: 🟠 RUSHED CLIMAX

Flag: Climax underwritten relative to investment
Fix: Expand NODE-020 to 1,500–2,000 words minimum
```

#### 💨 **PROBLEM: Dead Zone**
Node with low word count AND no emotional/mechanical change; feels pointless.

```
NODE-018 (transition scene):
  Word count: 85 wc
  Prose: "I left the apartment and walked to the street.
          A taxi was waiting."
  
Analysis:
  • Word count: 85 wc (VERY SHORT)
  • Emotional beat: None
  • Mechanical change: None (no choice, no new information)
  • Purpose: Scene transition only
  
Problem: Too short to matter, too long to ignore
         Reads like a vestigial scene that could be cut

Status: 💨 DEAD ZONE

Flag: Cut this node entirely OR combine with adjacent node
Fix: Either delete NODE-018, or merge with NODE-017 or NODE-019
```

#### 📊 **PROBLEM: Inconsistent Node Size**
Similar-weight scenes vary wildly in length.

```
Same act, same scene weight:

NODE-010 (dialogue scene):   300 wc
NODE-015 (dialogue scene):   2,800 wc
NODE-020 (dialogue scene):   500 wc

Analysis:
  All three are dialogue-driven relationship development
  All three occur at similar story points
  Word counts vary 300x → 2,800x → 500x
  
Problem: Why does NODE-015 get 9x the space as NODE-010?
         If both are "dialogue scenes," they should be closer
         
Status: 📊 INCONSISTENT NODE SIZE

Possible reasons (verify):
  ✅ VALID: NODE-015 is climactic dialogue; others are exposition
  ✅ VALID: NODE-010 is quick intro; NODE-020 is complex negotiation
  ❌ PROBLEM: Inconsistency is accidental; editor missed one scene

Fix: Either justify the difference in weight, or normalize to 800–1,200 wc
```

### 5. **Calculate Reading Time**

Estimate total reading time per branch:

```
Standard reading speed: 200–250 words per minute
Conservative: 200 wpm (slower, more thoughtful reading)
Aggressive: 250 wpm (faster, skimming)

BRANCH A word count: 6,600 words

Estimated reading time:
  • At 200 wpm (conservative): 33 minutes
  • At 225 wpm (average): 29 minutes
  • At 250 wpm (fast): 26 minutes

Report: "BRANCH A estimated reading time: 26–33 minutes"

Target check:
  If constitution specifies "30-minute gameplay":
    BRANCH A (26–33 min) ✅ WITHIN RANGE
  
  If constitution specifies "15-minute gameplay":
    BRANCH A (26–33 min) ⚠️  TOO LONG
    Fix: Cut 3,300+ words (50% reduction needed)
```

### 6. **Generate Pacing Audit Report**

Create `specs/pacing-audit.md`:

```markdown
## Pacing Audit

**Game**: [NAME]
**Target Reading Time**: 30 minutes (from constitution)
**Date**: [ISO]

### Branch Pacing Summary

| Branch | Total WC | Avg Node | Reading Time | Status |
|--------|----------|----------|--------------|--------|
| Branch A | 6,600 | 943 | 26–33 min | ✅ On target |
| Branch B | 5,200 | 867 | 21–26 min | ✅ On target |
| Branch C | 7,800 | 1,040 | 31–39 min | ⚠️ 6 min over |

### Node Length Analysis

| Node | Weight | WC | Target | Status |
|------|--------|----|---------| -------|
| NODE-005 | MINOR | 50 | 300–800 | ✅ Short but OK |
| NODE-010 | MOD | 950 | 800–1,500 | ✅ Good |
| NODE-012 | MOD | 2,100 | 800–1,500 | 🔴 INFO DUMP |
| NODE-015 | MAJOR | 2,300 | 1,500–3,000 | ✅ Good |
| NODE-020 | MOD | 500 | 800–1,500 | 🟠 SHORT FOR WEIGHT |

### Pacing Problems

**🔴 Info Dump** (1):
- NODE-012: 2,100 wc backstory monologue (fix: break into 2 scenes)

**🟡 Draggy Middle** (1):
- NODE-013→014→015: 530 wc across 3 nodes, no change (fix: combine or add decision)

**🟠 Rushed Climax** (1):
- NODE-020: 500 wc payoff vs 4,200 wc build-up (fix: expand to 1,500+ wc)

**💨 Dead Zone** (1):
- NODE-018: 85 wc transition-only (fix: delete or merge)

**📊 Inconsistent Size** (1):
- NODE-010/015/020: Similar weight, 300–2,800 wc variance (fix: normalize)

### Recommendations

**Priority 1 (Major impact)**:
1. NODE-012: Break info dump into 2–3 scenes with dialogue/action
2. NODE-020: Expand rushed climax to match build-up investment
3. Branch C: Cut 1,500+ words to match 30-minute target

**Priority 2 (Polish)**:
1. NODE-013→014→015: Consolidate dead transitions
2. NODE-010/015/020: Normalize similar scenes to 800–1,200 wc

**Overall Assessment**: Pacing generally good; 5 specific problem areas identified.
```

### 7. **Show Stats** (optional with --show-stats)

Full statistics table:

```
PACING STATISTICS

Nodes:          37 total
Total WC:       18,600 words
Average WC:     502 words/node

Word count distribution:
  • Under 100 wc:    5 nodes (13%)    [MICRO]
  • 100–300 wc:      8 nodes (22%)    [MINOR]
  • 300–800 wc:      12 nodes (32%)   [MINOR+]
  • 800–1,500 wc:    8 nodes (22%)    [MODERATE]
  • 1,500–2,500 wc:  3 nodes (8%)     [MAJOR]
  • 2,500+ wc:       1 node  (3%)     [MAJOR+]

Longest node:   NODE-012 (2,100 wc)
Shortest node:  NODE-018 (85 wc)
Median node:    618 wc
Standard dev:   487 wc

Reading time (estimated):
  • Total: 18,600 wc ÷ 225 wpm = 82.7 minutes (all branches combined)
  • Branch A: 29–33 minutes
  • Branch B: 21–26 minutes
  • Branch C: 31–39 minutes
```

### 8. **Show Graph** (optional with --show-graph)

ASCII visualization of word count per node:

```
WORD COUNT PER NODE (Branch A)

NODE-005: ████ (50)
NODE-010: ████████████████████████ (950)
NODE-012: ████████████████████████████████████████████ (2,100)
NODE-015: ███████████████████████████████████████████ (2,300)
NODE-020: ██████████████████ (800)
NODE-025: ███████████ (400)
ENDING:   ███████████████████ (900)

[Each █ = ~50 words]

Shape analysis: Rises to NODE-015 (climax), then descends ✅ Good arc
```

### 9. **Report**

Output `pacing-audit.md` with:
- Branch pacing summary (total words, reading time, status)
- Node length analysis (weight vs actual word count)
- Problem list (info dump, draggy middle, rushed climax, dead zones, inconsistency)
- Reading time comparison vs constitution target
- If `--show-stats`: Full statistics distribution
- If `--show-graph`: ASCII word count visualization per branch

---

## Key Principles for RPG Pacing

**Auto-Detection**: No flags required. Pacing analyzer automatically detects platform/ruleset from `constitution.md`. RPG-specific analysis activates based on detected context.

**Tabletop Session Pacing Model**:
- Sessions target 2.5–3.5 hours for most rulesets (configurable per game)
- Nodes per session: 15–22 average (~12–15 min per node)
- Encounter placement: Combat climax typically in later nodes of session (provides arc)
- Skill check distribution: Spread across session (not clustered); 3–5 per session optimal
- Rest scenes: Provided after major encounters (narrative breathing room)
- Player agency: Multiple decision points per session (3–5 choices with consequences)

**Computer Game Route Pacing Model**:
- All playstyle routes should converge within 2–3 nodes of each other
- Time imbalance should not exceed 3× (e.g., Combat 8 min, Dialogue 24 min is unbalanced)
- Difficulty scaling should not double playtime (Hard mode +20% typical, not +100%)
- Chapter/act structure consistent across all playstyles
- Accessibility variants should add <30 seconds per puzzle

**Ruleset-Specific Pacing**:
- **D&D 5e**: ~15 min per combat CR level, 3–5 skill checks/session, 1–2 combats/session
- **Pathfinder 2e**: ~20 min per encounter level, 6–8 skill checks/session, 1–3 combats/session
- **Shadowrun 6e**: 90–120 min per run, 5–7 skill checks/run, 30–60 min intrigue/combat

**Tabletop Campaign Introduction** (Auto-Generated):
- `draft/campaign-pacing-guide.md` created for player distribution before campaign starts
- Shows session structure, encounter pacing, companion timeline, faction reputation arc, ending preparation
- Player-facing tone (welcoming, clear expectations, no spoilers)
- GM-facing optional section for preparation notes

**Companion Arc Pacing** (Tabletop-specific):
- Companions join throughout campaign (not all at once)
- Approval progression tracked per session
- Companion milestones (recruitment, romance peak, betrayal, death) telegraphed by pacing
- Companion arcs conclude in final 3 sessions

**Faction Reputation Pacing** (Tabletop-specific):
- Rep changes announced in NPC dialogue (not silent)
- Cumulative progression toward ending gates
- No faction rep change >±25 per node (except exceptional circumstances)
- Faction milestones align with campaign arcs (sessions 4–7 establish factions, sessions 8–12 escalate stakes, sessions 13–15 lock endings)

**Word Count Is Not Sacred**: A 300-word emotional climax can work if prose is dense and impactful. A 2,000-word comedy scene can work if it's entertaining. Judge pacing by *reading experience*, not just numbers.

**Emotional Beats Matter More Than Words**: A 500-word scene with 3 major emotional shifts reads faster than a 2,000-word static scene. Word count is a proxy for complexity, not absolute measure.

**Reading Speed Varies**: Non-native readers, accessibility needs (dyslexia, screen readers), and engagement level all affect perceived pacing. 200–250 wpm is average; adjust for target audience.

**Branch Pacing Consistency**: Different branches can have different total word counts (different story paths), but similar-weight scenes should have similar node lengths. Inconsistency signals either intentional weight difference or editor oversight.

**Silent Scenes Count**: Even if a node has minimal prose, if it contains emotional beats, decision points, or mechanical changes, it's not a dead zone. Dead zones are purely transitional with nothing else.

---

## RPG-Specific Pacing Analysis

**Activated based on `SESSION.is_rpg` and `SESSION.ruleset` values.**

### Tabletop RPG Pacing (if `SESSION.is_rpg = "tabletop"`)

**Key Metric**: Session pacing (nodes per session, estimated session duration 2-4 hours)

**Session Structure Analysis**:

For each session in `plan.md`:
1. Count nodes assigned to `session: [N]` field
2. Sum total word count for session nodes
3. Estimate session duration:
   - GM narration time: ~1 word per 2 seconds (average) = 900 wc = 30 min narration
   - Skill checks: ~3 min per check (average) × check count
   - Combat encounters: ~5-10 min per combat (average) × encounter count
   - Player decision/roleplay: ~2 min per choice average
   - Total estimate: narration + skill checks + combat + decisions

**Example Session Pacing**:
```
SESSION 2: "Syndicate Recruitment"
─────────────────────────────────

Nodes assigned: NODE-015 through NODE-022 (8 nodes)
Total prose: 6,200 words

Narration breakdown:
  • NODE-015: 750 wc = 25 min narration
  • NODE-017: 850 wc = 28 min narration
  • NODE-020: 1,200 wc (+ 2 skill checks) = 40 min + 6 min checks
  • NODE-022: 600 wc (+ 1 combat CR3) = 20 min + 8 min combat
  • [Other nodes...] = 45 min

Total estimated session time: 172 minutes (2 hours 52 minutes)
Target session time: 2-4 hours (per constitution)
Status: ✅ WITHIN RANGE

Session pacing quality:
  • Nodes per session: 8 (good variety, ~20 min per node)
  • Encounter pacing: Combat in NODE-022 (acts as climax for session)
  • Skill check distribution: 3 checks spread across session ✅
  • Decision points: 4 major choices ✅ (player agency throughout)
  • Narrative arc: Builds to encounter, then resolution ✅
```

**Pacing Problems for Tabletop**:

🔴 **SESSION TOO LONG**: Session nodes total >240 min (exceeds typical 4-hour session)
- Fix: Split session into 2 sessions, move nodes to next session

🟡 **SESSION TOO SHORT**: Session nodes total <60 min (less than 1 hour gameplay)
- Fix: Add nodes (exploration, character interaction, skill challenges)

🔴 **ENCOUNTER CLUSTERING**: Multiple combats back-to-back without rest scenes
- Example: NODE-015 (combat), NODE-016 (combat), NODE-017 (combat) consecutively
- Problem: Players exhausted; party resources depleted; no narrative breathing room
- Fix: Add rest/roleplay scenes between encounters; spread combats across sessions

🟡 **SKILL CHECK DROUGHT**: Session has <2 skill checks or >8 skill checks
- <2: Players feel on-rails; insufficient opportunity for ability-based solutions
- >8: Session feels like a gauntlet; exhausting number of checks
- Fix: Aim for 3-5 skill checks per session (distributed across nodes)

⚠️ **COMBAT-HEAVY SESSION**: >50% of session time devoted to combat encounters
- Problem: Neglects exploration, dialogue, character development
- Fix: Balance combats with roleplay/skill check nodes

⚠️ **COMBAT-LIGHT SESSION**: <10% of session time devoted to combat
- Problem: If game system emphasizes combat, feels tame
- Fix: Add encounter or ensure skill checks are mechanically challenging

**Tabletop Pacing Report** (if `SESSION.is_rpg = "tabletop"`):

```
TABLETOP CAMPAIGN PACING REPORT

Campaign: [CAMPAIGN_NAME] | System: [D&D 5e / PF2e / SR6e]
Total Sessions: 15 | Total Nodes: 290 | Average: 19.3 nodes/session

SESSION PACING SUMMARY
─────────────────────
| Ses | Nodes | Total WC | Est. Time | Pacing | Issues |
|-----|-------|----------|-----------|--------|--------|
| 1   | 18    | 5,400    | 180 min   | ✅ Good | None |
| 2   | 20    | 6,200    | 207 min   | ✅ Good | — |
| 3   | 21    | 6,800    | 227 min   | ✅ Good | — |
| ... | ...   | ...      | ...       | ... | ... |
| 15  | 17    | 5,100    | 170 min   | ✅ Good | None |

Overall: Consistent 2.5–4 hour sessions ✅

ENCOUNTER PACING
────────────────
Combats per session: 2.1 average (good balance)
Combats distributed: Spread across sessions ✅
Combat-heavy sessions: 2 (Sessions 6, 12) — manageable
Combat-light sessions: 1 (Session 10) — roleplay-focused ✅

SKILL CHECK DISTRIBUTION
─────────────────────────
Skill checks per session: 3.8 average ✅
Ability balance: Charisma 28%, Wisdom 24%, Dexterity 22%, Int 20%, Str 6% — good variance ✅
Hotspot skills: Persuasion used in 12/15 sessions (expected for intrigue campaign)

SESSION ARCS
─────────────
S1–3: Low pressure, character introductions (avg 190 min/session)
S4–7: Tension ramps up, faction intrigue (avg 215 min/session)
S8–12: High stakes, major encounters (avg 225 min/session)
S13–15: Denouement, ending branches (avg 175 min/session)

Assessment: ✅ WELL-PACED Campaign arc builds pressure, then releases into endings

PROBLEMS DETECTED
──────────────────
None (pacing is well-balanced)
```

### Computer Game RPG Pacing (if `SESSION.is_rpg = "computer"`)

**Key Metric**: Route pacing (playstyle routes should take similar time; no >3× imbalance)

**Route Pacing Analysis**:

For each playstyle route (Combat/Dialogue/Exploration):
1. Identify all nodes reachable via that route
2. Sum prose word count for route
3. Estimate playthrough time per route
4. Check balance (no route >3× longer than others)

**Example Route Pacing**:
```
CHAPTER 3: "The Vault Heist"
──────────────────────────────

Combat Route: NODE-031 → NODE-033 → NODE-035 → NODE-040
  Prose: 2,100 wc (combat-focused narration)
  Gameplay time: ~11 minutes
  Status: ✅ Combat focus

Dialogue Route: NODE-031 → NODE-034 → NODE-036 → NODE-040
  Prose: 2,050 wc (dialogue-heavy negotiation)
  Gameplay time: ~10 minutes
  Status: ✅ Dialogue focus

Exploration Route: NODE-031 → NODE-032 → NODE-037 → NODE-040
  Prose: 2,200 wc (discovery-focused, puzzle solving)
  Gameplay time: ~11 minutes
  Status: ✅ Exploration focus

Time imbalance: 11 min vs 10 min vs 11 min = 1.1× ratio ✅ BALANCED
All routes reach NODE-040 (convergence point) ✅ Story progression equal
```

**Pacing Problems for Computer Game**:

🔴 **ROUTE IMBALANCE**: One playstyle route >3× longer than others
- Example: Combat 8 min | Dialogue 24 min | Exploration 9 min
- Problem: Dialogue players spend excessive time; might skip dialogue
- Fix: Trim dialogue route, add dialogue branching to combat/exploration routes

🟠 **ROUTE DIVERGENCE**: Routes don't reconverge for >3 nodes
- Example: Combat and Dialogue split at NODE-050, don't rejoin until NODE-057
- Problem: Story feels fractured; ending branches unclear
- Fix: Add convergence points every 2-3 nodes; ensure major beats meet all routes

⚠️ **DIFFICULTY SCALING IMPACT**: Hard mode adds so many enemies that route time doubles
- Example: Normal difficulty Dialogue route 8 min | Hard difficulty 16 min
- Problem: Hard mode feels like padding, not challenge
- Fix: Scale difficulty via mechanical changes (more powerful enemies, not more enemies); limit time increase to <1.5×

🟡 **ACCESSIBILITY VARIANT TIME**: Colorblind/audio/motor variants add <30 sec per puzzle
- Generally acceptable (variants should not meaningfully extend playtime)
- Flag if variants extend playtime by >1 minute per puzzle

**Computer Game Pacing Report** (if `SESSION.is_rpg = "computer"`):

```
COMPUTER GAME PACING REPORT

Game: [GAME_NAME] | System: [D&D 5e / PF2e / SR6e]
Total Playstyles: 3 (Combat/Dialogue/Exploration)
Total Chapters: 8 | Total Nodes: 156

ROUTE PACING SUMMARY
────────────────────
| Chapter | Combat | Dialogue | Exploration | Imbalance | Status |
|---------|--------|----------|-------------|-----------|--------|
| 1       | 8 min  | 9 min    | 8 min       | 1.1×      | ✅     |
| 2       | 11 min | 10 min   | 12 min      | 1.2×      | ✅     |
| 3       | 9 min  | 11 min   | 10 min      | 1.2×      | ✅     |
| ... | ... | ... | ... | ... | ... |
| 8       | 7 min  | 8 min    | 7 min       | 1.1×      | ✅     |

Overall Campaign Time:
  • Combat route: 82 minutes (all chapters)
  • Dialogue route: 78 minutes (all chapters)
  • Exploration route: 85 minutes (all chapters)
  • Maximum imbalance: 1.09× ratio ✅ BALANCED

CONVERGENCE POINTS
────────────────────
Chapter 1–2: Routes meet at ch2-node-8 ✅ (converge every 2 nodes)
Chapter 3–4: Routes meet at ch4-node-5 ✅
Chapter 5–7: Routes meet at ch7-node-12 ✅
Chapter 8: All routes meet at ending ✅
Assessment: ✅ Good convergence frequency

DIFFICULTY SCALING
────────────────────
Normal difficulty campaign: 82 min average
Easy difficulty: 75 min (8.5% shorter) — scaling appropriate ✅
Hard difficulty: 88 min (7.3% longer) — scaling appropriate ✅
Expert difficulty: Not offered for this game ✅

ACCESSIBILITY VARIANTS
────────────────────────
Timed puzzles: 12 total
  • Colorblind mode: +15 sec avg per puzzle = 3 min added
  • Audio cues: +10 sec avg per puzzle = 2 min added
  • Motor simplification: +20 sec avg per puzzle = 4 min added
  • Cognitive variant: +25 sec avg per puzzle = 5 min added
Assessment: ✅ Variants acceptable (<1 min per puzzle)

OVERALL PACING
────────────────
Campaign duration: 78–85 minutes ✅ Within target
Route balance: All within 1.1× of each other ✅ BALANCED
Story convergence: Every 2 nodes on average ✅
Difficulty scaling: Non-disruptive ✅
Accessibility: Minimal time impact ✅
Assessment: ✅ WELL-PACED Game feels balanced across all playstyles
```

### Area Exploration Density (if `specs/world-map.md` present)

**Key Metric**: Scene-type balance per Area. No Area should be all-combat or all-exposition.

**Area Density Analysis** *(skip if `world-map.md` absent)*:

For each Area in `world-map.md`:
1. Collect all nodes whose `parent_location` is a Location belonging to this Area.
2. Group by `scene_type` (travel / exploration / dialogue / combat / rest / shop / quest_event / cutscene).
3. Check baseline requirements and flag violations:

| Flag | Condition | Severity |
|---|---|---|
| No entry scene | Area has no `scene_type: travel` node as first node | CRITICAL |
| No rest scene | Area has zero `scene_type: rest` nodes in any of its Locations | CRITICAL |
| Combat saturation | >50% of scenes are `combat` | WARNING |
| Exposition overload | >60% of scenes are `dialogue` + `cutscene` | WARNING |
| Optional content ratio | <20% of scenes are `exploration` or `quest_event` | NOTE (low discovery incentive) |
| Critical path isolation | Critical path visits <30% of the Area's scenes | NOTE (Computer Game only) |

4. Compute **area-level pacing curve**: For each Area, map scene types in story-order to show the combat/dialogue/rest rhythm. A healthy rhythm alternates: travel → exploration/dialogue → combat → rest → exploration/quest_event.

**Area Density Report format**:
```
AREA EXPLORATION DENSITY REPORT

AREA-KingsVault (dungeon)
  Scenes: 9 total (1 travel, 2 exploration, 1 dialogue, 4 combat, 1 rest)
  Combat ratio: 44% — ✅ OK
  Rest scenes: 1 — ✅ OK
  Entry scene: NODE-1010_VaultEntry (travel) — ✅ OK
  Scene rhythm: travel → exploration → combat → combat → dialogue → combat → exploration → combat → rest
  Pacing: ⚠️ Three consecutive combats (NODE-1013–1015) — suggest adding exploration or short rest between them

AREA-TownSquare (urban)
  Scenes: 6 total (1 travel, 0 exploration, 5 dialogue, 0 combat, 0 rest)
  Combat ratio: 0% — OK for urban hub
  Rest scenes: 0 — ⚠️ WARNING: No rest location in area (inn or safe house needed)
  Entry scene: NODE-1001_CityGate (travel) — ✅ OK
  Action: Add LOC-Inn with rest scene to AREA-TownSquare
```

**Pacing Problems — Area Density**:

🔴 **CRITICAL: No entry scene** — Area has no travel-typed entry node
- Fix: Add a `scene_type: travel` node as the first scene in one of this Area's Locations

🔴 **CRITICAL: No rest location** — Area has zero rest scenes; players cannot recover between combats
- Fix: Designate one Location in the Area as a rest point; add a `scene_type: rest` node

🟡 **WARNING: Combat saturation** — >50% of scenes are combat; player fatigue risk
- Fix: Replace 1–2 combat scenes with exploration or social scenes; or move some combat to adjacent Areas

---

### Ruleset-Specific Pacing (if `SESSION.ruleset = "D&D 5e" / "Pathfinder 2e" / "Shadowrun 6e"`)

**D&D 5e Session Pacing**:
- Expected session duration: 2.5–3.5 hours
- Typical encounter: 15 min per encounter CR (CR 1 = 15 min, CR 5 = 75 min)
- Skill check average: 3–5 per session
- Combat encounters per session: 1–2 recommended (one major, one minor)
- Roleplay/exploration time: ~60–90 min per session

**Pathfinder 2e Session Pacing**:
- Expected session duration: 2.5–4 hours (slightly longer due to three-action economy)
- Typical encounter: 20 min per encounter level
- Degree of success rolls: 6–8 skill checks per session (higher frequency than D&D 5e)
- Combat encounters: 1–3 per session (simpler mechanics allow more encounters)
- Roleplay/exploration: ~40–70 min per session

**Shadowrun 6e Session Pacing**:
- Expected session duration: 3–4 hours (matrix/astral actions add complexity)
- Typical run: 90–120 min for medium difficulty
- Routing decision point: 15–30 min per major choice (Street/Matrix/Astral branching)
- Skill checks: 5–7 per run (many simultaneous checks in team actions)
- Combat/Intrigue: 30–60 min per major conflict

---

## Tabletop Campaign Introduction Model

**Purpose**: Generate player-facing campaign pacing guide and session structure overview (published as `draft/campaign-pacing-guide.md` for players before campaign starts).

**When Generated**: Automatically generated during first SESSION-1 node pacing analysis (if `SESSION.is_rpg = "tabletop"`).

**Player Introduction Contents** (`draft/campaign-pacing-guide.md`):

```markdown
# [CAMPAIGN_NAME] – Campaign Pacing Guide

## Welcome, Adventurers!

This guide explains how [CAMPAIGN_NAME] is structured, what to expect from session pacing, 
and how your choices affect the story's flow.

### Campaign Overview

**Total Length**: 15 sessions, 78 hours of gameplay (5 hours/session average)
**System**: D&D 5e (or appropriate ruleset)
**Tone**: [Genre/tone from constitution]
**Party Size**: 3–5 characters | **Starting Level**: 1 | **Ending Level**: 11

### Session Pacing Expectations

**What to Expect Each Session**:
- Duration: 2–4 hours (typically 2.5–3.5 hours)
- Structure: Roleplay/exploration → skill challenges → major decision → (often) combat encounter → resolution
- Encounters per session: 1–2 combat encounters (avg), 3–5 skill checks, 2–4 major roleplay scenes
- Decision points: 3–5 player choices with mechanical or story consequences

**Session Arc Examples**:

| Session | Type | Typical Structure | Duration |
|---------|------|-------------------|----------|
| 1–3 | Introduction | Explore city, meet NPCs, skill challenges, no major combat | 2.5 hrs |
| 4–7 | Intrigue | Investigation, faction meetings, skill checks, 1–2 combats/session | 3 hrs |
| 8–12 | Escalation | Major encounters, companion recruitment, high stakes | 3.5 hrs |
| 13–15 | Climax | Final choices, ending encounters, campaign conclusion | 3 hrs |

### Encounter Pacing

**Combat Balance**:
- Most sessions have 1–2 combat encounters (never more than 3)
- Combat difficulty scales with party level (CR matches party level, ±1)
- Each combat typically 45–90 minutes of session time
- Rest scenes provided after major combats (recovery roleplay)

**Skill Check Flow**:
- Distributed across session (not clustered)
- Mix of abilities (Charisma, Wisdom, Dexterity, Intelligence, Strength, Constitution)
- Success/failure branches handled quickly (15–30 min per major check)

### Choice Impact

**Your Decisions Matter**:
- Sessions 1–3: Choices set tone and NPC relationships (low mechanical impact)
- Sessions 4–7: Choices lock/unlock faction paths and companion recruitment
- Sessions 8–12: Major choices determine ending viability (which endings are still possible)
- Sessions 13–15: Final choices select which ending(s) are reachable

**Decision Points Per Session**: Average 3–4 choices that meaningfully affect story progression

### Companion Arc Timeline

**Companions join throughout the campaign**:
| Session | Companion | Recruitment | Approval Focus |
|---------|-----------|--------------|-----------------|
| 2–3 | [Companion A] | Session 2–3 | Build trust sessions 4–8 |
| 5–6 | [Companion B] | Session 5–6 | Build trust sessions 7–11 |
| 7–8 | [Companion C] | Session 7–8 | Build trust sessions 9–13 |

**Companion arcs conclude** in Sessions 13–15 (romance peak, betrayal reveal, or death possible depending on choices)

### Faction Reputation Pacing

**Factions tracked across campaign**:
| Faction | Rep Arc | Sessions | Key Milestones |
|---------|---------|----------|---|
| [Faction 1] | 0→+85 | 4–14 | +20 (S4), +15 (S7), +25 (S10), +25 (S14) |
| [Faction 2] | 0→+70 | 5–13 | +15 (S6), +20 (S8), +10 (S10), +25 (S12) |
| [Faction 3] | 0→-30 | 6–12 | -10 (S6), -15 (S9), -5 (S12) |

**Rep changes announced by NPC dialogue**, not silent mechanical shifts.

### Ending Preparation

**Multiple Endings Available**: 5 possible endings (depending on faction rep + companion approvals + choice history)

- **Ending A** (Justice): Reachable after Session 6, locked by Session 14
- **Ending B** (Redemption): Reachable after Session 7, locked by Session 14
- **Ending C** (Shadow): Reachable after Session 8, locked by Session 13
- **[...more endings...]**

Sessions 13–15 are designed so that your accumulated choices determine which endings remain viable.

### Session Preparation Tips (for Players)

- **Session prep**: Read your character's emotional arc from previous session; review recent NPC interactions
- **Session goals**: Aim for 1–2 major goals per session (talk to NPC, complete task, make faction choice)
- **Builds matter**: Prepare for varied challenges (bring spells/abilities for multiple situations)
- **Roleplay drive pacing**: More roleplay → more connection to NPCs/outcomes; better session satisfaction

### GM Pacing Notes (For Reference)

[Optional: Include brief GM-facing notes on session structure without spoiling story]
- Sessions typically run 2.5–3.5 hours
- 15–20 nodes per session
- 5,000–6,500 words of narration per session
- Pace naturally (GMs don't need to rush; 15-minute skill checks are normal)

---

This campaign is designed to provide a satisfying mix of roleplay, exploration, decision-making, 
and combat across 15 sessions. Enjoy the journey!
```

**Auto-Generated Contents**:
- Total campaign length (sum of all session durations)
- Session arc summaries (what to expect at each stage)
- Encounter pacing overview (combats per session, skill check frequency)
- Companion recruitment timeline (which sessions, which companions)
- Faction reputation pacing (when rep changes, how much)
- Ending preparation (which sessions lock endings)
- Decision point frequency (choices per session)
- Session prep tips for players (roleplay, builds, goals)

