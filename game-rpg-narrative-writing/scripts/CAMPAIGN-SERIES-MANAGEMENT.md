# RPG Campaign Series Management

Guide for using `speckit.series` to manage tabletop and computer game RPG campaign progression across multiple entries.

## Overview

For RPG campaigns, `speckit.series` tracks:

| Tabletop RPG | Computer Game |
|---|---|
| Session allocation and pacing | Chapter/act structure |
| Companion NPC state continuity | Playstyle route progression |
| Faction reputation changes | Accessibility coverage across routes |
| Map distribution per session | Asset map inventory across levels |
| Campaign prep documents | Route-exclusive content isolation |
| Player briefing materials | Ending route reachability |

## Getting Started: Initialize Campaign Series

```bash
speckit.series init
```

**Tabletop RPG Questions** (when [PLATFORM] = tabletop detected):

```
1. Series title: "The Lost Dragon Campaign"
2. Total entry count: "3 modules" (Adventure 1, 2, 3)
3. Genre / tone: "High fantasy, exploration-focused"
4. Target audience: "D&D 5e players, 3-5 party size"
5. Overarching dramatic question: "Will the party discover who stole the dragon egg?"
6. Overarching theme: "Trust and betrayal in alliances"
7. Engine target: "Sugarcube (play-online)" or "Ink" or "Generic PDF"
8. Carry-over strategy: "questionnaire (players answer intro questions per module)"
9. Series ending contract: "Resolve dragon theft mystery; determine companion fates"

10. Campaign ruleset: "D&D 5e"
11. Recommended party size: "4-5 characters, levels 5-10"
12. Campaign structure: "12-16 sessions per module, 36-48 total sessions"
13. Companion system: "Yes (3 recruitable NPCs)"
14. Faction system: "Yes (4 factions, reputation tracker)"
15. Player introduction document: "Yes (campaign guide for players)"
16. Campaign pacing: "3-4 hours per session, 2 sessions per week"
```

**Computer Game Questions** (when [PLATFORM] = computer detected):

```
10. Game ruleset: "D&D 5e"
11. Playstyle routes: "Yes (Stealth, Combat, Diplomacy)"
12. Game structure: "3 acts per module, 9 acts total"
13. Accessibility requirements: "Yes (colorblind, audio descriptions, motor remapping)"
14. Route count: "3 (Stealth, Combat, Diplomacy)"
```

**Generated Files**:
- `series/series-bible.md` - Campaign bible with all series metadata
- `series/CAMPAIGN-PREP.md` - Player introduction template (tabletop only)
- `series/ROUTE-BALANCE.md` - Playstyle route tracking (computer only)

## Tabletop Campaign Workflow

### 1. Module Planning (`speckit.plan` → Entry 1)

In `speckit.plan`, declare session allocation:

```markdown
## Campaign Structure - Entry 1

### Session Pacing
- Sessions 1-4: Tavern introduction + caravan journey
- Sessions 5-8: Explore Lost Dragon Ruins
- Sessions 9-12: Final confrontation + companion resolution

### Companions Introduced
- Sir Theron (Knight, joins Session 3)
- Maia (Rogue, joins Session 5)
- Brother Aldric (Cleric, joins Session 8)

### Faction Involvement
- **Merchant's Guild**: Introduction, +1 reputation if deal with smugglers
- **Temple of Light**: Recruitment, +2 if heal corrupted souls
- **Shadow Thieves**: Warning encounter, -1 if refuse help

### Maps Used
- map-tavern-flosston.json (Sessions 1-2)
- map-caravan-route.json (Sessions 3-4, regional)
- map-dragon-ruins-level1.json (Sessions 5-7, battle)
- map-dragon-ruins-level2.json (Sessions 8-9, battle)
- map-final-throne.json (Session 12, boss arena)
```

### 2. After Module Release (`speckit.series update 1`)

```bash
speckit.series update 1
```

**Tabletop-specific prompts**:

```
✓ NPC State Registry sync
  Sir Theron (final level: 7, equipment: +1 greatsword, reputation: Knight Commander)
  Maia (final level: 7, equipment: Cloak of Elvenkind, reputation: Guild Spy)
  Brother Aldric (final level: 7, equipment: Holy symbol, reputation: Temple Acolyte)

✓ Faction reputation sync
  Merchant's Guild: +3 (helped with smuggling problem)
  Temple of Light: +4 (saved corrupted souls, healed priest)
  Shadow Thieves: 0 (ignored recruitment)

✓ Campaign prep doc update
  Regenerating campaign-guide.md for Module 2
  Generating SESSION-13-BRIEFING.md (module start recap)

✓ Map registry sync
  Registered 5 maps used in Module 1
  Added to series-level inventory

✓ Session count validation
  Module 1: 12 sessions (on track)
  Modules 1-3 total: 36/48 sessions planned
  ✓ Pacing validated

✓ Player briefing
  "What should players know before Module 2?"
  → "Companion fates depend on Module 1 endings"
  → Updated SESSION-13-BRIEFING.md
```

**Output**:
```
???????????????????????????????????????????????????????
  SERIES BIBLE UPDATED – Entry 1: The Lost Dragon Ruins
???????????????????????????????????????????????????????
  NPC state rows updated  : 3 companions synced
  New world rules (SWR)   : 2 (dragon lore, temple prophecy)
  New series threads (ST) : 1 (mystery: who stole the egg?)
  Resolved threads        : 0
  Entry status            : released

  RPG Campaign Updates:
    Companion state synced : 3/3 companions
    Maps registered        : 5 maps
    Campaign prep docs     : Updated for Module 2
    Session allocation     : 12/12 completed

  Next: speckit.series audit or speckit.specify (Module 2)
???????????????????????????????????????????????????????
```

### 3. Series Audit (`speckit.series audit 1-3`)

Check all three modules for continuity:

```bash
speckit.series audit 1-3
```

**RPG Campaign Audit Checks**:

```
???????????????????????????????????????????????????????
  SERIES AUDIT REPORT
  Series  : The Lost Dragon Campaign
  Scope   : Entries 1-3 (Modules 1-3)
  Date    : 2026-05-07
???????????????????????????????????????????????????????

### Companion State Continuity
✓ Sir Theron: Level 7 (Module 1 end) → Level 8 starting stats (Module 2 ok)
✓ Maia: Level 7 (Module 1 end) → Level 8 starting stats (Module 2 ok)
✓ Brother Aldric: Level 7 (Module 1 end) → Level 8 starting stats (Module 2 ok)

### Faction Reputation
✓ Merchant's Guild: +3 (Module 1) → +5 (Module 2 check in)
✓ Temple of Light: +4 (Module 1) → +6 (Module 2, quest)
✓ Shadow Thieves: 0 (Module 1) → -2 (Module 2, revenge subplot)

### Map Continuity
✓ All 5 Module 1 maps have valid JSON files
✓ Module 2 maps registered: 6
✓ Module 3 maps registered: 4
⚠ WARNING: Map "dragon-egg-chamber" referenced in Module 3 but JSON missing

### Session Allocation
✓ Module 1: 12 sessions (complete)
✓ Module 2: 18 sessions planned (on track)
✓ Module 3: 18 sessions planned (on track)

### Campaign Prep Documents
✓ campaign-guide.md exists
✓ SESSION-1-BRIEFING.md through SESSION-13-BRIEFING.md exist
✓ SESSION-31-BRIEFING.md (Module 3 start) pending

### Player Briefing Materials
✓ Module 1 companion selection documented
⚠ WARNING: Module 2 companion fates not documented in SESSION-13-BRIEFING.md
✓ Module 3 final reveal documented

### Summary
CRITICAL: 0 | WARNINGS: 2 | PASS: 10
Recommended action: Create missing dragon-egg-chamber.json, update SESSION-13-BRIEFING.md
???????????????????????????????????????????????????????
```

## Computer Game Campaign Workflow

### 1. Route-Based Planning (`speckit.specify` → Entry 1)

In `speckit.specify`, track playstyle routes:

```markdown
## Playstyle Routes - Entry 1

### Stealth Route (Scout)
- Chapter 1: Enter Castle (sneak past guards)
- Chapter 2: Infiltrate Tower (pickpocket key)
- Chapter 3: Escape with Scroll (avoid patrols)

### Combat Route (Fighter)
- Chapter 1: Enter Castle (fight guard captain)
- Chapter 2: Breach Tower (defeat sentries)
- Chapter 3: Battle Mage (final confrontation)

### Diplomacy Route (Negotiator)
- Chapter 1: Enter Castle (negotiate passage)
- Chapter 2: Convince Tower Guard (bluff/persuade)
- Chapter 3: Negotiate Peace (resolve peacefully)

### Content Balance
| Route | Chapters | Encounters | Secrets | Playstyle Score |
|-------|----------|-----------|---------|-----------------|
| Stealth | 3 | 2 (avoidable) | 5 | 85% |
| Combat | 3 | 4 (required) | 2 | 78% |
| Diplomacy | 3 | 3 (optional) | 4 | 81% |

✓ Balance ratio: 85/78 = 1.09× (within 3:1 threshold)

### Accessibility Variants
- Colorblind: Stealth guards marked with different patterns
- Audio: Diplomacy includes character voice descriptions
- Motor: Combat can be automated via difficulty settings
- Cognitive: All routes available regardless of puzzle difficulty
```

### 2. Route Balance Check (`speckit.series update 1`)

```bash
speckit.series update 1
```

**Computer-specific prompts**:

```
✓ Route balance check
  Stealth route: 85 points, 5 encounters
  Combat route: 78 points, 8 encounters
  Diplomacy route: 81 points, 6 encounters
  Ratio: 85/78 = 1.09× ✓ (balanced)

✓ Accessibility variant sync
  Colorblind: ✓ Enabled (Stealth, Diplomacy)
  Audio: ✓ Enabled (Diplomacy, Combat narrator)
  Motor: ✓ Enabled (all routes, autopilot option)
  Cognitive: ✓ Enabled (no cognitive barriers)

✓ Asset map sync
  Stealth: 3 level maps
  Combat: 2 arena maps
  Diplomacy: 1 throne room map
  Total: 6 maps registered

✓ Playstyle branching
  Stealth-exclusive variable: $stealth_discovery = true
  Combat-exclusive variable: $combat_victory = true
  Diplomacy-exclusive variable: $peace_agreement = true
  ✓ All isolated (no cross-route pollution)

✓ Ending route coverage
  Ending: "Scroll Acquired" - Reachable from: Stealth, Combat, Diplomacy ✓
  Ending: "Mage Defeated" - Reachable from: Combat ✓
  Ending: "Peace Treaty" - Reachable from: Diplomacy ✓
```

### 3. Route Audit (`speckit.series audit 1-3`)

```bash
speckit.series audit 1-3
```

**Computer Campaign Audit Output**:

```
???????????????????????????????????????????????????????
  SERIES AUDIT REPORT
  Series  : Lost Dragon Game
  Scope   : Entries 1-3 (Acts 1-3)
  Date    : 2026-05-07
???????????????????????????????????????????????????????

### Playstyle Route Balance
✓ Entry 1: Stealth 85, Combat 78, Diplomacy 81 (1.09× balanced)
✓ Entry 2: Stealth 92, Combat 88, Diplomacy 90 (1.05× balanced)
✓ Entry 3: Stealth 100, Combat 95, Diplomacy 98 (1.05× balanced)

### Accessibility Coverage
✓ Entry 1: Colorblind ✓, Audio ✓, Motor ✓, Cognitive ✓
✓ Entry 2: Colorblind ✓, Audio ✓, Motor ✓, Cognitive ✓
✓ Entry 3: Colorblind ✓, Audio ✓, Motor ✓, Cognitive ✓

### Variable Isolation
✓ Stealth route variables: 12 unique, 0 cross-route pollution
✓ Combat route variables: 10 unique, 0 cross-route pollution
✓ Diplomacy route variables: 11 unique, 0 cross-route pollution

### Ending Reachability
✓ "Scroll Acquired": All 3 routes ✓
✓ "Dragon Awakened": Stealth, Combat ✓
✓ "Peace Treaty": Diplomacy ✓
✓ "Hidden Ending": All 3 routes (secret) ✓

### Summary
CRITICAL: 0 | WARNINGS: 0 | PASS: 12
Recommended action: Proceed to next phase
???????????????????????????????????????????????????????
```

## Status Dashboard

### Tabletop Campaign Status

```bash
speckit.series status
```

**Output**:

```
???????????????????????????????????????????????????????
  SERIES STATUS: The Lost Dragon Campaign
  3 modules planned (Tabletop RPG – D&D 5e)
  Dramatic question: Will the party discover who stole the dragon egg?
???????????????????????????????????????????????????????

### Modules
| # | Title | Status | Sessions | Companions | Factions |
|---|---|---|---|---|---|
| 1 | Lost Dragon Ruins | released | 12/12 | 3 | 3 |
| 2 | Fey Enclave | in-progress | 8/18 | 2 added | 2 new |
| 3 | Dragon's Lair | planned | 0/18 | 1 final | 0 |

### Companions
| Name | Module Joined | Current Level | Loyalty |
|---|---|---|---|
| Sir Theron | 1 | 9 | Loyal |
| Maia | 1 | 9 | Neutral (faction choice?) |
| Brother Aldric | 1 | 9 | Devoted |
| New Companion 1 | 2 | 8 | Unknown |
| New Companion 2 | 2 | 7 | Unknown |

### Campaign Prep Status
✓ campaign-guide.md (players read before Module 1)
✓ SESSION-1-BRIEFING.md through SESSION-20-BRIEFING.md (all released)
⏳ SESSION-31-BRIEFING.md (Module 3 start, not yet written)

### RPG Campaign Status
| Metric | Value | Target |
|--------|-------|--------|
| Total sessions completed | 20 | 48 |
| Companions active | 5 | ~5 |
| Factions tracked | 5 | ~5 |
| Maps created | 14 | ~20 |
| Campaign guide ready | ✓ | Entry 1 |

⚠  Action recommended: Generate SESSION-31-BRIEFING.md for Module 3 before Module 2 release.

???????????????????????????????????????????????????????
```

### Computer Game Series Status

```bash
speckit.series status
```

**Output**:

```
???????????????????????????????????????????????????????
  SERIES STATUS: Lost Dragon Game
  3 acts planned (Computer RPG – D&D 5e)
  Dramatic question: Can the player choose their own destiny through different playstyles?
???????????????????????????????????????????????????????

### Acts (Chapters)
| # | Title | Status | Stealth | Combat | Diplomacy |
|---|---|---|---|---|---|
| 1 | Castle Infiltration | released | 85 | 78 | 81 |
| 2 | Tower Breach | in-progress | 92 | 88 | 90 |
| 3 | Final Confrontation | planned | — | — | — |

### Playstyle Route Balance
| Metric | Value | Target |
|--------|-------|--------|
| Stealth score | 85+92 = 177 | ~180 |
| Combat score | 78+88 = 166 | ~180 |
| Diplomacy score | 81+90 = 171 | ~180 |
| Max ratio | 177/166 = 1.07× | <3:1 ✓ |

### Accessibility Coverage
| Feature | Acts 1-3 | Coverage |
|---------|---------|----------|
| Colorblind modes | ✓✓✓ | 100% |
| Audio descriptions | ✓✓✓ | 100% |
| Motor alternatives | ✓✓✓ | 100% |
| Cognitive accessibility | ✓✓✓ | 100% |

### Ending Reachability
| Ending | All Routes? | Status |
|--------|-----------|--------|
| "Scroll Acquired" | ✓ All 3 | Released |
| "Dragon Awakened" | Stealth, Combat | Released |
| "Peace Treaty" | Diplomacy | In Act 2 |
| "Hidden Ending" | All 3 (secret) | In Act 3 |

### RPG Campaign Status
| Metric | Value | Target |
|--------|-------|--------|
| Playstyle routes | 3 | 3 ✓ |
| Acts completed | 2 | 3 |
| Accessibility variants | 4 | 4 ✓ |
| Asset maps | 9 | ~12 |
| Variable isolation | 33 unique | No pollution ✓ |

⚠  Action recommended: Balance Stealth content in Act 3 to close 177/166 gap.

???????????????????????????????????????????????????????
```

## Best Practices

### Tabletop Campaigns

1. **Session allocation**: Plan 2-4 hour sessions; validate total doesn't exceed realistic campaign length
2. **Companion state**: Record level, equipment, relationships, quest status after each module
3. **Faction tracking**: Document reputation changes per faction per module for continuity
4. **Player briefing**: Always generate SESSION-N-BRIEFING.md before module release so players know what happened
5. **Map distribution**: Spread maps evenly across sessions; track which maps used per session
6. **Campaign guide**: Generate once at series start; update only if ruleset/mechanics change

### Computer Games

1. **Route balance**: Audit route content ratio before each release; target <1.3:1 ratio
2. **Accessibility-first**: Include colorblind/audio/motor variants in Act 1; don't add retroactively
3. **Variable isolation**: Verify route-exclusive variables don't leak into other routes
4. **Ending coverage**: Ensure each ending reachable from at least 2 routes to prevent dead-ends
5. **Performance pacing**: Log loading times per chapter; alert if any chapter >20% slower than others
6. **Secret content**: Plan hidden endings/routes in series-bible.md before Act 1 so they don't feel tacked-on

## Integration with speckit Commands

| Command | Tabletop Use | Computer Use |
|---------|---|---|
| `speckit.specify` | Map inventory, companion intro | Route breakdown, accessibility matrix |
| `speckit.plan` | Session allocation, faction roles | Chapter structure, route gates |
| `speckit.research` | Companion mechanics, faction rules | Playstyle mechanics, route rebalancing |
| `speckit.series` | Continuity audit, prep doc sync | Route balance check, variable isolation |
| `speckit.compile` | Export with player briefing | Export with route selector |

---

Ready to manage your RPG campaign series! Start with `speckit.series init`.
