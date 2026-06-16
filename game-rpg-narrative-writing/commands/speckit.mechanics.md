---
description: Declare, update, or promote mechanic hooks in specs/mechanics.md. For RPG campaigns (tabletop D&D/Pathfinder/Shadowrun and computer game), manages companion loyalty hooks, faction reputation tracking, session-based mechanics, playstyle routes, accessibility variants, and ruleset-specific mechanics. Use to register new Tier 2 stubs, promote a stub to Tier 1, add a compatibility warning rule, or audit which hooks are declared vs. in use.
handoffs:
  - label: Update Variables
    agent: speckit.constitution
    prompt: Update constitution.md Section II to reflect the mechanic changes just made
    send: false
  - label: Mechanic Health Check
    agent: speckit.status
    prompt: Run a mechanic health summary
    send: false
---

# speckit.mechanics

**RPG Campaign Support**: Adapts mechanic hook management for tabletop (companion loyalty tracking, faction reputation hooks, session-based mechanics, ruleset-specific rules and conditions) and computer game (playstyle route state, accessibility variant hooks, chapter progression, route-specific mechanics).

Manage the `specs/mechanics.md` hook schema document: declare new hooks, promote stubs, and audit hook coverage.

## User Input

```text
$ARGUMENTS
```

Accepted arguments:
- `declare [HOOK_TYPE]` � register a new Tier 2 stub hook schema in `specs/mechanics.md`
- `promote [HOOK_TYPE]` � move a Tier 2 stub to Tier 1; requires translation tables for all declared engine targets
- `audit` � compare hooks declared in `specs/mechanics.md` against hooks used in `nodes/` and `outlines/`; report unused declared hooks and undeclared in-use hooks
- `list` � print all declared hooks with tier, description, and engine support status
- *(no argument)* � equivalent to `list`

## Pre-Execution Checks
**Auto-detect platform and ruleset** (for RPG campaigns):
- Load `constitution.md`
- Extract `[PLATFORM]` (tabletop/computer) and `[RULESET]` (D&D 5e/Pathfinder 2e/Shadowrun 6e)
- Set SESSION object {platform, ruleset, mechanics}
- If RPG: Load `companions.md`, `factions.md`, `mechanics-[RULESET].md`, `plan.md` (for session/chapter structure)

**Standard checks**:1. Confirm `specs/mechanics.md` exists. If absent: "No mechanics.md found � run `speckit.constitution` first to generate the game bible and mechanics document."
2. Load `.specify/memory/constitution.md` Section II (enabled mechanics list) � used to cross-check declarations.
3. If `declare` or `promote`: confirm the hook type name follows kebab-case convention (e.g. `custom_mood`, `faction`).

---

## Mode: `list`

Print a registry table from `specs/mechanics.md`:

```
Declared hooks in specs/mechanics.md:

Tier 1 (fully exported):
  flag             ? Sugarcube  ? Ink
  counter          ? Sugarcube  ? Ink
  visited          ? Sugarcube  ? Ink
  inventory        ? Sugarcube  ? Ink
  timer            ? Sugarcube  ?? Ink (turn-based only)
  trust            ? Sugarcube  ? Ink
  currency         ? Sugarcube  ? Ink
  npc_state        ? Sugarcube  ? Ink
  ending_condition ? Sugarcube  ? Ink
  random           ? Sugarcube  ? Ink
  choice_memory    ? Sugarcube  ?? Ink (CONST mapping)
  clue             ? Sugarcube  ? Ink

Tier 2 (stubs � export with warning):
  knowledge        [Sugarcube: stub] [Ink: stub]
  faction          [Sugarcube: stub] [Ink: stub]
  location_state   [Sugarcube: stub] [Ink: stub]
  object_state     [Sugarcube: stub] [Ink: stub]
  [custom hooks registered for this project...]
RPG Campaign Hooks (if [PLATFORM]=tabletop):
  companion_loyalty    [Sugarcube: stub] [Ink: stub]  – tracks loyalty shift (-5 to +5)
  faction_reputation   [Sugarcube: stub] [Ink: stub]  – tracks faction standing across sessions
  session_milestone    [Sugarcube: stub] [Ink: stub]  – marks session progression
  npc_recruitment      [Sugarcube: stub] [Ink: stub]  – companion join/leave decisions
  ruleset_condition    [Sugarcube: stub] [Ink: stub]  – (D&D 5e) condition tracking; (Pathfinder 2e) critical state; (Shadowrun 6e) karma/edge pools

RPG Campaign Hooks (if [PLATFORM]=computer):
  playthrough_route    [Sugarcube: stub] [Ink: stub]  – commits playstyle choice (stealth/combat/diplomacy)
  route_variable       [Sugarcube: stub] [Ink: stub]  – route-exclusive variable ($stealth_*, $combat_*, $diplomacy_*)
  accessibility_mode   [Sugarcube: stub] [Ink: stub]  – tracks active accessibility variant (colorblind/audio/motor)
  chapter_milestone    [Sugarcube: stub] [Ink: stub]  – marks chapter progression

Run `speckit.mechanics audit` to check coverage against node files.
```

---

## Mode: `declare [HOOK_TYPE]`

Register a new Tier 2 stub hook in `specs/mechanics.md`.

1. Ask (=3 questions):
   - What does this hook track? (one sentence)
   - What parameters does it take? (e.g. `set=[variable] value=[x]`, `check=[variable] op=gte value=N`)
   - Is there an authoring analogy to an existing Tier 1 hook? (e.g. "like FLAG but for moods")

2. **If [PLATFORM]=tabletop**: Ask additional question:
   - Is this hook used in campaign-wide tracking (across sessions) or per-session? (affects persistence)
   - What ruleset-specific mechanics does this relate to? (D&D 5e conditions, Pathfinder 2e critical outcomes, Shadowrun 6e karma/edge)

3. **If [PLATFORM]=computer**: Ask additional question:
   - Is this hook route-exclusive (stealth/combat/diplomacy) or shared across all routes?
   - Should this hook reset between chapters or persist throughout playthrough?

4. Generate the stub block and append to the **Tier 2** section of `specs/mechanics.md`:

   ```markdown
   ### `[hook_type]` � [Short Description]

   ```
   [MECHANIC:[HOOK_TYPE] [param1]=[value] [param2]=[value]]
   [conditional prose]
   [/MECHANIC]
   ```

   > // TIER 2 STUB � [target] export not yet implemented. Emits: `// UNSUPPORTED HOOK � [hook_type]`
   > Analogy: [existing hook analogy if provided]
   > [If RPG]: Scope: [Campaign-wide / Per-session / Route-exclusive]; Rulesets: [D&D 5e / Pathfinder 2e / Shadowrun 6e]
   ```

5. Confirm: "`[HOOK_TYPE]` added to Tier 2 in `specs/mechanics.md`."
6. Remind: "Add `[hook_type]` to `.specify/memory/constitution.md` Section II enabled mechanics list if you want it active for this project."

---

## Mode: `promote [HOOK_TYPE]`

Promote a Tier 2 stub to Tier 1 by adding full translation tables.

1. Load the existing stub block for `[HOOK_TYPE]` from `specs/mechanics.md`.
2. Ask (=4 questions, only what isn't clear from the stub):
   - Sugarcube macro translation for each parameter
   - Ink `~` or conditional translation for each parameter
   - Any compatibility warning conditions (e.g. "Ink requires X")
   - Should `export.py` handle this automatically or emit a manual TODO comment?
   - **If RPG**: Verify this hook's behavior across campaign sessions / chapters / routes (identify edge cases requiring special handling)

3. Replace the Tier 2 stub with a full Tier 1 block (with translation table) in `specs/mechanics.md`.
4. Add a row to the Compatibility Warning Rules table if any edge case was identified.
5. **If RPG**: Add a note about persistence scope (campaign-wide, per-session, or route-exclusive) in the Tier 1 block.
6. Confirm: "`[HOOK_TYPE]` promoted to Tier 1 in `specs/mechanics.md`. Update `export.py` to implement the translation."
7. Note: "If using `export.py`, the actual translation logic must be added manually to `scripts/python/export.py`. This command only updates the schema document."

---

## Mode: `audit`

Compare declared hooks against in-use hooks across all node and outline files.

1. Scan all `nodes/NODE-*.md` and `outlines/*.md` for `[MECHANIC:` blocks.
2. Build a list of all in-use hook types (unique).
3. Compare against declared hooks in `specs/mechanics.md`.

Output:

```
Mechanic Audit � [GAME_TITLE]

Declared and in use:
  flag, counter, trust, ending_condition, [...]

Declared but never used:
  ??  currency     � declared in mechanics.md, no nodes use it
  ??  timer        � declared in mechanics.md, no nodes use it

Used but not declared in mechanics.md:
  ?  mood_state   � used in NODE-007, NODE-012; run `speckit.mechanics declare mood_state`

Tier 2 stubs in active use (will produce export warnings):
  ??  knowledge    � used in 3 nodes (NODE-004, NODE-009, NODE-014)
  ??  faction      � used in 1 node (NODE-022)
```

Suggest: "Run `speckit.mechanics promote [HOOK_TYPE]` for any Tier 2 hooks in active use before export."

---

## RPG Campaign Mechanics Management Notes

### Tabletop Campaign Mechanics Considerations

**Companion Loyalty Hook Scope**:
- companion_loyalty must persist across all SESSION-N files (not reset between sessions)
- Set loyalty shift when player makes faction/companion-affecting choice
- Example: SESSION-3 choice to help Thieves Guild → Theron loyalty(-2), Lyssa loyalty(+1)
  - Loyalty resets between sessions (player loses all progress)
  - Loyalty shift declared but never checked before critical NPC actions
  - Loyalty threshold decisions lack corresponding NPC behavior changes
- Best practice: Every SESSION-N that includes NPC interaction should check current loyalty before dialogue/action

**Faction Reputation Hook Scope**:
- faction_reputation must persist campaign-wide, not reset per session
- Major faction choice in SESSION-N should affect faction standing permanently
- Example: SESSION-2 choice helps Temple → faction_reputation(Temple, +2) persists through SESSION-3, SESSION-4, SESSION-5
  - faction_reputation set in SESSION-3 but never checked again
  - Faction standing expected to be high but contradicts earlier choices
  - Faction's reaction to player is inconsistent despite same standing
- Best practice: faction_reputation decisions should have ripple effects (quest availability, NPC hostility, final faction outcome)

**Session Milestone Tracking**:
- session_milestone marks completion of SESSION-N, prevents re-entry
- Example: session_milestone(SESSION-3) set when player reaches final scene of SESSION-3
- Used to branch into SESSION-4-specific content
  - Player can re-enter SESSION-3 after completing it (milestone not checked)
  - SESSION-4 references SESSION-3 events but doesn't verify SESSION-3 was completed
  - Milestone set too early (player can skip critical SESSION-3 content)
- Best practice: Set milestone at actual completion point, verify in SESSION-(N+1) opening

**NPC Recruitment/Dismissal Hooks**:
- npc_recruitment tracks companion join/leave, must persist across sessions
- Once Theron joins in SESSION-2, availability in SESSION-3/4 depends on loyalty + faction
  - Companion rejoins without explanation (should require rescue/reunion scene)
  - Companion dismissed but returns without narrative justification
  - Recruitment state doesn't affect available party size or NPC dialogue
- Best practice: recruitment_state should gate NPC availability in subsequent sessions (unavailable companions shouldn't appear in nodes)

**Ruleset-Specific Condition Hooks**:
- D&D 5e: Conditions (Frightened, Poisoned, Cursed) should be tracked as hooks, checked before combat/social scenes
  - Example: If player character is Cursed from SESSION-3 choice, curse should persist, affect rolls in SESSION-5
- Pathfinder 2e: Critical success/failure states should persist session-to-session
  - Example: Critical success on check in SESSION-2 reveals secret; failure leads to combat
- Shadowrun 6e: Karma/Edge pool depletion must carry across sessions
  - Example: Spending Karma in SESSION-3 means less Karma available in SESSION-4

### Computer Game Route Mechanics Considerations

**Playthrough Route Commitment Hook**:
- playthrough_route must be set exactly ONCE in CHAPTER-2 (Stealth / Combat / Diplomacy)
- Once set, playthrough_route never changes (binding commitment)
  - playthrough_route set in CHAPTER-3 or later (too late for narrative weight)
  - playthrough_route reset mid-playthrough (breaks route exclusivity)
  - Player can switch routes dynamically (confuses route-exclusive content)
- Best practice: CHAPTER-2 choice that sets playthrough_route should have narrative weight (player deciding on playstyle after initial exposure)
- Example: CHAPTER-1 shows all three approaches available; CHAPTER-2 forces choice between sneaking/fighting/talking past major obstacle

**Route-Exclusive Variables**:
- Must use naming convention: $stealth_[VAR], $combat_[VAR], $diplomacy_[VAR]
- Each variable only set/checked in route-specific nodes
  - Variable $stealth_infiltration_plan set, but $combat_infiltration_plan checks same plan (routes bleeding together)
  - Route variable checked in route-agnostic node (defeats isolation)
  - Variable name doesn't indicate route ($plan vs $stealth_plan)
- Best practice: Every route-exclusive decision, item, NPC relationship should have [route]_-prefixed variable
- Verification: If player switches route (reload save, debug), should see "undefined" errors for wrong-route variables, confirming isolation

**Accessibility Mode Hooks**:
- accessibility_mode tracks active accessibility variant (colorblind/audio/motor)
- Should persist across entire playthrough (don't reset between chapters)
- Should be orthogonal to routes (all three routes support all accessibility modes)
  - Accessibility mode only applies to one route (breaks access equity)
  - Accessibility mode resets between chapters (frustrating for players with access needs)
  - Accessibility mode changes game difficulty balance (should only change presentation)
- Best practice: accessibility_mode should only affect how information is presented (colorblind: color→pattern; audio: sound→visual; motor: complex→simplified), not gameplay difficulty

**Chapter Milestone Tracking**:
- chapter_milestone marks CHAPTER-N completion
- Example: chapter_milestone(CHAPTER-2) set when player reaches CHAPTER-3 opening
- Used to prevent backtracking
  - Player can re-enter CHAPTER-2 after completing playthrough
  - CHAPTER-3 references CHAPTER-2 events but doesn't verify chapter_milestone
  - Milestone set too early (player skips critical CHAPTER-2 content)
- Best practice: Set milestone at clear chapter ending, verify in next chapter opening

**Route Convergence Hooks**:
- route_convergence marks where all three routes reconverge after divergence
- Example: CHAPTER-3 opens with all routes in common hub area (convergence point)
- Used to sync story state across routes for final chapters
  - Routes never reconverge (three separate endings, no common story)
  - Convergence creates plot holes (route-exclusive events ignored in common scenes)
  - Convergence happens too late (routes isolated through most of game)
- Best practice: Convergence points should acknowledge all route choices (final dialogue reflects how player got there)

---

## RPG Campaign Mechanics Best Practices

**Tabletop Campaign Mechanics**:
- Companion loyalty and faction reputation should be visible to players (campaign-guide.md lists current standing)
- Each SESSION-N should begin with recap of current standings (what loyalty changed last session, which factions are allied/opposed)
- Ruleset-specific condition effects should be consistent with core mechanic rules (D&D 5e Frightened = disadvantage on attack, not custom penalty)
- Campaign should be testable: Run through each loyalty path, verify rewards/penalties consistent across sessions

**Computer Game Route Mechanics**:
- Every route should have similar challenge level (not Stealth easy, Combat hard, Diplomacy medium)
- Route commitment in CHAPTER-2 should feel weighty (player sees consequences of choice in CHAPTER-3+)
- Accessibility modes should not disadvantage players (colorblind mode should solve puzzles as quickly as normal mode)
- Route convergence scenes should acknowledge multiple routes exist (dialogue references how player got there, not assumes single path)
- Each route should have exclusive content (unique NPC, unique quest, unique ending variant) that justifies replay

**Shared Across Both Platforms**:
- Any hook tracking persistent player choice must survive save/load (don't reset on chapter/session boundary)
- Hooks declared in specs/mechanics.md should be used consistently throughout (unused declarations waste export effort)
- Tier 2 stub hooks should be promoted to Tier 1 before export (stubs cause "UNSUPPORTED HOOK" warnings in output)
- Campaign/route-wide mechanics (loyalty, route, accessibility) should be verified by speckit.audit before final release

---

## Encounter Design & Balance (Tabletop RPG Priority 1)

### Encounter Structure & CR Calculations

#### D&D 5e Encounter Design

**XP Thresholds by Party Level**:

| Level | Easy | Medium | Hard | Deadly |
|-------|------|--------|------|--------|
| 1 | 25 | 50 | 75 | 100 |
| 2 | 50 | 100 | 150 | 200 |
| 3 | 75 | 150 | 225 | 400 |
| 4 | 125 | 250 | 375 | 500 |
| 5 | 250 | 500 | 750 | 1100 |
| 6 | 300 | 600 | 900 | 1400 |
| 7 | 350 | 750 | 1100 | 1700 |
| 8 | 450 | 900 | 1400 | 2100 |
| 9 | 550 | 1100 | 1600 | 2400 |
| 10 | 600 | 1200 | 1900 | 2800 |

**Multipliers for Party Size**:
- Solo (1 PC): ×1 (don't use solo multiplier; rebalance as Medium instead)
- Pair (2 PCs): ×1.5
- Standard (3-5 PCs): ×1
- Large (6+ PCs): ×0.5 to ×0.75

**CR by Enemy Type** (sample encounters):
- CR 0: Commoner, Cultist, Thug
- CR 1/8: Bandit, Guard, Acolyte
- CR 1/4: Cultist, Priest, Skeleton
- CR 1/2: Ghoul, Bugbear, Zombie
- CR 1: Gnoll, Goblin Warlord, Scout
- CR 2: Ogre, Werewolf, Wight
- CR 3: Basilisk, Dryad, Knight
- CR 5: Demon (Dretch), Efreeti, Hill Giant
- CR 8: Bone Dragon, Mummy Lord
- CR 10+: Demon Lord, Lich, Ancient Dragon

**Encounter Design Template** (per session):
- Session Level: [LEVEL]
- Total Party XP Budget: [XP] (based on level & thresholds above)
- Difficulty Target: [Easy/Medium/Hard/Deadly]
- Recommended Encounters per Session: 3-4 Medium OR 6-8 Easy OR 1-2 Hard/Deadly

**Encounter Builder Example** (SESSION-3, Level 4, Party of 4):
```
Total XP Budget: 1000 (Medium, 4 PCs)
Multiplier: ×1

Encounter 1: Goblin Ambush (Medium)
  - 2× Goblin (CR 1/4 = 50 XP each) = 100 XP × 1 = 100 XP
  - 1× Bugbear Captain (CR 2 = 450 XP) × 1 = 450 XP
  - Adjusted Total: 550 XP

Encounter 2: Hidden Cult Meeting (Hard)
  - 4× Cultist (CR 1/8 = 25 XP each) = 100 XP
  - 1× Cult Priest (CR 2 = 450 XP)
  - Adjusted Total: 550 XP

Total: 1100 XP (slightly over budget but acceptable)
```

**Bonus XP Mechanics**:
- Encounter bypassed via skill check: Award half XP
- Encounter completed with no combat (Diplomacy/Stealth): Award full XP
- Boss encounter: Award full XP + special treasure (magic item or extra gold)

**AC/Damage Expectations**:
- Expected Player AC by Level: 10 + (2 × DEX mod) or armor. L1-5: AC 12-15 typical.
- Expected Enemy AC: 10 + Level/2, rounded. L4 enemies: AC 12.
- Expected Single-Hit Damage: (Level × 1d6 + 5) average. L4 = 4d6+5 (about 18 damage).
- Player HP by Level: (10 + CON) × Level. L4 Fighter with 16 CON = (10+3)×4 = 52 HP.

**DCs by Difficulty**:
- Easy: DC 10
- Medium: DC 15
- Hard: DC 20
- Deadly: DC 25

#### Pathfinder 2e Encounter Design

**Encounter Budget System**:
- Party XP is combined, encounters grant XP in share of total party pool
- Party Level = median of party members
- Budget per session: Party Level × 4 = total XP budget

**Threat Adjustments by Enemy Level**:
- Trivial: Enemy ≤ Party Level - 5 (grants no XP)
- Low: Enemy = Party Level - 3 to Party Level - 2 (grants 10% XP value)
- Moderate: Enemy = Party Level - 1 (grants 15% XP value)
- Severe: Enemy = Party Level (grants 20% XP value)
- Extreme: Enemy = Party Level + 1 (grants 40% XP value)
- Overwhelming: Enemy ≥ Party Level + 2 (grants 100% XP value per enemy, don't mix with others)

**Encounter XP Budget Examples** (Party Level 4):
- Budget: 4 × 4 = 16 XP worth of encounters per session
- Option 1: 1× Severe (8 XP) + 1× Low (1.5 XP) + miscellaneous = ~16 XP
- Option 2: 3-4× Moderate (3.75 XP each) = 15 XP
- Option 3: 2× Extreme (6.4 XP each) = 12.8 XP

**Degree of Success System** (affects difficulty perception):
- Critical Success: Encounter fails or retreats immediately
- Success: Encounter goes normally, player wins decisively
- Failure: Encounter goes normally, player wins narrowly
- Critical Failure: Player caught off-guard, surprise round enemy advantage

**Hero Points Allocation**:
- Each session grants 3-4 Hero Points per player
- Usage: Re-roll any d20, reduce damage by half, grant ally an action
- Refund Hero Points not spent by session end (don't carry over)

**AC/Damage Expectations**:
- Expected Player AC: 15-17 by L4
- Expected Enemy AC: 14-16 by L4
- Expected Single Hit Damage: 2d6+3 (about 10 damage)
- Player HP by Level: (8 + CON mod) × Level. L4 Champion with 16 CON = (8+3)×4 = 44 HP

**DCs by Difficulty**:
- Easy: DC 10 (Party Level - 1)
- Standard: DC 15 (Party Level + 3)
- Hard: DC 18 (Party Level + 6)
- Extreme: DC 25 (Party Level + 10)

#### Shadowrun 6e Encounter Design

**Opposition Force Scaling**:
- Party Ratings: Sum all player character Ratings (Special Attributes + Magic/Resonance/etc)
- Encounter Budget: Party Rating × 0.8 to 1.2 (0.8 = easier, 1.2 = deadly)

**Enemy Rating by Type**:
- Street Level (Gangers, Thugs): Rating 1-3
- Professional (Mercenaries, Specialists): Rating 3-6
- Corporate Security: Rating 5-8
- Military/Powerful Mages: Rating 7-10+

**Combat Pacing** (Initiative & Actions):
- Initiative: REF + Intuition + d6
- Actions per turn: 1 Major + 1 Minor
- Hacking: Matrix actions take same time slot as physical actions
- Magic: Spell casting uses 1 Major action
- Astral combat: Astral mages project and engage spirits/astral entities simultaneously with physical world

**Damage Expectations**:
- Weapon Damage: (DV + net hits on attack roll)
- Armor Reduction: (Armor Rating) - (Attack net hits), minimum 0
- Player Armor: Rating 8-12 typical
- Expected Incoming Damage: 6-10 per hit after armor reduction
- Player Condition Monitor: 8 + (Willpower × 2). Example: WIL 3 = 14 boxes before knockdown

**Karma Expenditure per Session**:
- Typical session: Players burn 3-5 Karma per character on re-rolls/actions
- Karma sources: Mission payout (5-10), in-game discover (+1-2)
- Karma pool restoration: Between missions (resets to racial max typically)

**DCs by Difficulty**:
- Easy: Target 12-14
- Medium: Target 15-17
- Hard: Target 18-20
- Deadly: Target 21+

---

### Encounter Registration & Tracking

**Create `specs/encounters.md` Registry**:
- One entry per major encounter in the campaign
- Fields per encounter:
  - Encounter ID (ENC-001, ENC-002, etc.)
  - Session/Chapter placement
  - Enemy roster (names, CR/level/rating)
  - Tactical setup (terrain, NPC positioning, victory condition)
  - Loot table (treasure, XP)
  - Difficulty rating (Easy/Medium/Hard/Deadly)
  - Alternative routes (bypass via Stealth/Diplomacy if applicable)

**Example Encounter Entry**:
```markdown
### ENC-003: Goblin Hideout Battle

**Session**: SESSION-3  
**Party Level**: 4  
**Difficulty**: Hard  
**CR Budget**: 750 XP

**Enemies**:
- Bugbear Warlord (CR 2, 450 XP)
- 2× Goblin Scout (CR 1/4, 50 XP each)
- 1× Goblin Shaman (CR 1/2, 100 XP)
- **Total Raw**: 700 XP → **Adjusted (Hard)**: 750 XP ✓

**Terrain**: Hideout interior, 40×30 ft chamber, 2 entrances, raised platform (10 ft, NPC leader)

**Tactical Notes**:
- Warlord leads from platform, coordinates archers
- Shaman casts Scorching Ray (3 targets max, 4d6 damage)
- Goblins use hit-and-run tactics (disengage as bonus action)

**Loot** (if defeated):
- Warlord's Greatsword (magic, +1 damage)
- Leather Armor × 3
- 250 gp
- Shaman's Spell Scroll (Summon Beast)

**Alternative Routes**:
- **Stealth**: DC 16 Stealth check to bypass via back entrance → no combat, no treasure (half XP 375)
- **Diplomacy**: DC 18 Persuasion to negotiate peace → Goblins leave peacefully → full XP but no treasure
- **Combat (default)**: Standard encounter above

**Victory Condition**: All enemies defeated or fleeing
```

---

### Encounter Design Best Practices

**Balance Testing Checklist**:
- [ ] CR calculated correctly per ruleset (use templates above)
- [ ] XP total within session budget (±10%)
- [ ] AC/Damage expectations match party level
- [ ] At least one alternative route exists (Stealth/Diplomacy bypass)
- [ ] Loot table includes at least one rewarding magic item per 2-3 encounters
- [ ] Encounters don't repeat enemy types excessively (variety per session)
- [ ] Deadly encounters have clear telegraphing (players see danger before commitment)

- ⚠️ Party defeats Deadly encounter in <10 minutes → too easy, increase CR by 2-3
- ⚠️ Party takes >60 minutes on Medium encounter → too complex, simplify tactics or enemy count
- ⚠️ Single player downed while others untouched → unbalanced target allocation (enemy AI should focus fire, but not one target exclusively)
- ⚠️ Treasures hoarded across 5+ sessions → loot distribution sparse, increase magic item frequency
- ⚠️ Same tactics work every encounter → enemy variety needed (mix melee/ranged, magic/mundane, brute/cunning)

---

## Computer Game Route Mechanics (Priority 1)

### Route-Exclusive Mechanics Design

**Activated when**: `[PLATFORM]` = "Computer Game" in constitution.md

Three playstyle routes (Stealth, Combat, Diplomacy) committed in CHAPTER-2 with mechanically distinct progression paths:

#### Stealth Route Mechanics

**Core Mechanic**: Hide/detection system with consequence scaling

| Mechanic | Implementation | Progression | Rewards |
|----------|---|---|---|
| **Detection Risk** | Numerical risk (0-100%), increases by NPC proximity, line-of-sight | Hide mechanic reduces risk by 50-90% per distance tier | Undetected = full XP + loot, detected = combat or challenge |
| **Visibility** | Line-of-sight based; shadows reduce detection, light increases | Unlock "Shadow Cloak" ability (Chapter 3) | Perma-invisibility 30 sec (cooldown) |
| **Sound** | Movement speed affects detection; crouch = silent, run = loud | Unlock "Silent Step" ability (Chapter 2) | Muted footsteps, can move at normal speed undetected |
| **AI Patrol Routes** | Scripted guards follow fixed paths; stealth player learns paths | Unlock "Predict Patrol" ability (Chapter 3) | Highlight guard positions for 10 seconds |
| **Non-Lethal Options** | Sleeping darts, disguises, lockpicking; no casualties | Unlock "Doppelganger" disguise (Chapter 4) | Impersonate guards, access restricted areas |
| **Consequence** | Avoid combat, no alerts, no reinforcements | Stealth fails: combat encounter spawns | All routes converge at same story beat |

**Stealth Skill Checks**:
- Stealth DC: 10 (Easy) / 15 (Normal) / 20 (Hard)
- Perception DC: NPC guard perception vs. player stealth roll
- Alternative: Social engineering (Deception DC) bypasses Stealth entirely

**Companion Abilities (Stealth Route)**:
- Shadow assassin companion: "Flank" ability (companion attacks undetected enemy simultaneously)
- Rogue companion: "Lock Mastery" (guaranteed successful lockpicking in timed scenarios)
- Ranger companion: "Scout Ahead" (reveals guard positions before entry)

**Ending Gate for Stealth Route**:
- If completed ≥80% stealth (undetected in 4+ encounters): "Shadow Victory" ending available
- Companion loyalty affects stealth success (loyal companion provides backup if detected)

#### Combat Route Mechanics

**Core Mechanic**: Action economy and tactical positioning

| Mechanic | Implementation | Progression | Rewards |
|----------|---|---|---|
| **Action Economy** | 1 Major + 1 Minor per turn (standard D&D 5e) | Unlock "Extra Attack" (Chapter 3) | 2 attacks per turn |
| **Tactical Positioning** | Cover/high ground grant ±2 AC bonus/penalty | Unlock "Flanking" (Chapter 2) | Ally + player attacking same enemy = +2 attack bonus |
| **Weapon Switching** | Swap weapons as bonus action; each weapon has unique property | Unlock "Arsenal" ability (Chapter 4) | Swap mid-combat with no penalty, 3 weapons equipped |
| **Ability Power** | Abilities consume action points; recharged per encounter or on long rest | Unlock "Power Surge" (Chapter 3) | Abilities cost -1 action point for next 5 rounds |
| **Reinforcements** | AI spawns additional enemies if player defeats initial wave too quickly | Unlock "Overwhelm" (Chapter 4) | Prevent enemy reinforcements, all enemies spawn at start |
| **Consequence** | Combat encounters scale with player damage output; harder enemies if steamrolling | Fail if player health < 10% | Can flee combat or surrender (story consequence) |

**Combat Skill Checks**:
- Attack rolls: d20 + STR/DEX modifier vs. enemy AC
- Initiative DC: Standard d20 + DEX for first-round advantage
- Alternative: Intimidation DC allows peaceful resolution (surrender/flee)

**Companion Abilities (Combat Route)**:
- Paladin companion: "Divine Shield" (protect another character, absorb next hit)
- Fighter companion: "Riposte" (counter-attack when hit)
- Barbarian companion: "Rage" (double damage for 3 rounds, take half damage)

**Ending Gate for Combat Route**:
- If completed ≥80% combat (defeated all encounters without fleeing): "Warrior Victory" ending available
- Companion loyalty affects combat effectiveness (loyal = better AI tactics, higher damage)

#### Diplomacy Route Mechanics

**Core Mechanic**: Persuasion/negotiation with NPC emotional states

| Mechanic | Implementation | Progression | Rewards |
|----------|---|---|---|
| **Persuasion** | Dialogue check (Persuasion vs. NPC resistance); each NPC has unique triggers | Unlock "Silver Tongue" (Chapter 3) | Persuasion checks reduce difficulty by 1 tier |
| **Emotional State** | NPCs have moods (Angry, Fearful, Hopeful, Uncertain); state affects dialogue outcome | Unlock "Read Emotions" (Chapter 2) | Display NPC emotional state before dialogue choice |
| **Companion Loyalty** | Companion approval unlocks companion-specific dialogue lines (better persuasion) | Unlock "Bond of Trust" (Chapter 3) | Companion dialogue option auto-succeeds once per chapter |
| **Negotiation Outcomes** | Successful persuasion grants peaceful passage, quest cooperation, or NPC recruitment | Unlock "Master Negotiator" (Chapter 4) | All remaining NPCs start at "friendly" disposition |
| **Information Gathering** | Insight checks reveal NPC motivations; use to craft persuasion strategy | Unlock "Mind Reader" (Chapter 4) | Know NPC mood and preferences without rolling |
| **Consequence** | Persuasion fails: combat unavoidable OR NPC becomes enemy | Failed multiple times: NPC permanently hostile | All routes converge at same story beat |

**Diplomacy Skill Checks**:
- Persuasion DC: 10 (Easy) / 15 (Normal) / 20 (Hard)
- Insight DC: Understand NPC motivation (reveals emotional weak point)
- Deception DC: Lie about party intent (risky, discovery means hostility)

**Companion Abilities (Diplomacy Route)**:
- Cleric companion: "Divine Favor" (NPC is charmed for 1 round, auto-agrees to reasonable request)
- Bard companion: "Performance" (restore NPC mood, gain +3 bonus to next Persuasion check)
- Wizard companion: "Mind Meld" (know what NPC wants without dialogue)

**Ending Gate for Diplomacy Route**:
- If completed ≥80% diplomacy (peacefully resolved 4+ encounters): "Peace Victory" ending available
- Companion loyalty affects dialogue options (loyal = unlock companion-specific persuasion lines)

---

### Route Mechanical Distinction Framework

**Create `specs/route-mechanics.md` Registry** (Computer Game campaigns only):

```markdown
# Route Mechanics Registry

## Route Comparison Table

| Mechanic | Stealth | Combat | Diplomacy |
|----------|---------|--------|-----------|
| **Primary Stat** | Dexterity | Strength/Constitution | Charisma |
| **Core Challenge** | Avoid detection | Survive combat | Convince NPCs |
| **Failure Mode** | Detected = forced combat | Overwhelmed = death | Refused = combat or mission fail |
| **Progression Speed** | Slow (sneak, careful) | Fast (fight) | Medium (talk) |
| **Reward for Excellence** | "Shadow Victory" ending | "Warrior Victory" ending | "Peace Victory" ending |
| **Playtime per Chapter** | 45-60 min | 60-90 min (more encounters) | 45-75 min (dialogue-heavy) |
| **Difficulty Scaling** | Easy: fewer guards | Easy: lower enemy AC/HP | Easy: lower Persuasion DCs |
| **Companion Synergy** | Rogue, Ranger, Assassin | Paladin, Fighter, Barbarian | Cleric, Bard, Wizard |

## Route-Exclusive Abilities

### Stealth Abilities (Progression)

| Chapter | Ability | Effect | Cost |
|---------|---------|--------|------|
| 2 | Silent Step | Move at full speed undetected | 1 action |
| 3 | Shadow Cloak | Invisibility 30 sec | 1 action (60 sec cooldown) |
| 3 | Predict Patrol | Reveal guard positions 10 sec | Passive (once per encounter) |
| 4 | Doppelganger | Impersonate any NPC | 1 action (5 min cooldown) |

### Combat Abilities (Progression)

| Chapter | Ability | Effect | Cost |
|---------|---------|--------|------|
| 2 | Flanking | +2 attack bonus if ally attacks same target | Passive (always active) |
| 3 | Extra Attack | Attack twice per turn | Passive (always active) |
| 3 | Power Surge | Next 5 rounds, abilities cost -1 action | 1 action (60 sec cooldown) |
| 4 | Arsenal | 3 weapons equipped, swap freely mid-combat | Passive (always active) |

### Diplomacy Abilities (Progression)

| Chapter | Ability | Effect | Cost |
|---------|---------|--------|------|
| 2 | Read Emotions | Display NPC emotional state before dialogue | Passive (always active) |
| 3 | Silver Tongue | Persuasion checks reduce difficulty by 1 tier | Passive (always active) |
| 3 | Bond of Trust | Companion dialogue auto-succeeds once per chapter | 1 action (once per chapter) |
| 4 | Master Negotiator | All remaining NPCs start "friendly" | Passive (always active) |

## Route-Specific NPCs & Quests

| NPC | Stealth Route | Combat Route | Diplomacy Route | Notes |
|-----|---|---|---|---|
| Rip (Fence) | Available, sells stolen goods | Unavailable (combat route kills) | Recruitable ally (diplomacy check) | Quest giver for route-specific missions |
| Captain Kane (Guard) | Enemy (if discovered) | Combat encounter | Negotiable ally | Faction leader affects ending |
| Sister Mara (Healer) | Quest: Steal herbs | Optional: protect her | Quest: convince her to join cause | Companion approval varies by route |

## Route Balance Metrics (Validation)

- **Node count parity**: Each route should have ±10% similar node counts (no route inherently longer)
- **Encounter distribution**: Each route should face ≥3 "challenge" encounters (varied by route type)
- **Playtime parity**: Each route ~60-90 min per chapter (varies ±15%)
- **Companion availability**: Each route should have access to ≥3 companion types
- **Loot balance**: Each route receives equivalent rewards (not combat-heavy, stealth-light)
- **Ending viability**: All three endings reachable; no route permanently locked out
```

---

### Route Mechanical Best Practices

**Balance Checklist**:
- [ ] Each route has mechanically distinct core challenge (Stealth ≠ Combat ≠ Diplomacy)
- [ ] Abilities progressively unlock (Chapter 2 → 3 → 4 → end game)
- [ ] Route-exclusive NPCs appear only in their respective routes (no bleeding)
- [ ] No route is faster than others (pacing equivalent)
- [ ] All three routes reach same story convergence point (no narrative lock-out)
- [ ] Difficulty scaling consistent across routes (easy/normal/hard applies all routes)
- [ ] Companion synergy matches route playstyle (combat companions in combat route, etc.)

- ⚠️ Combat route trivializes encounters, stealth route struggles → rebalance enemy HP/AC
- ⚠️ Diplomacy always succeeds where others fail → raise Persuasion DCs or add consequences
- ⚠️ One route completes 30% faster than others → add padding encounters to shorter route
- ⚠️ Stealth/Combat route gets unique items denied to Diplomacy → redistribute loot equally
- ⚠️ NPC reacts differently to same choice across routes (breaks immersion) → standardize dialogue outcomes
- ⚠️ Route commitment in Chapter 2 locks out critical story content → ensure all routes see main plot
- ⚠️ Companion companions never use route-specific abilities → revisit AI companion logic



