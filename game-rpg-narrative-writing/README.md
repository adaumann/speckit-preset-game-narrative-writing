# RPG Narrative Writing Preset

A Spec Kit preset for designing and implementing tabletop RPG campaigns with mechanics-driven narrative structure.

## Overview

This preset provides comprehensive templates and validation tools for creating RPG campaigns with:
- **Campaign structure** across multiple sessions with pacing and progression
- **Companion system** with recruitment, approval tracking, and conditional outcomes
- **Faction system** with reputation mechanics and ending gates
- **Skill check system** with difficulty scaling and consequence tracking
- **Encounter system** with CR scaling and XP awards
- **Seven endings** with multiple path requirements and lock timing

## Supported Systems

- **D&D 5e** (primary) — Complete templates for 15-session campaigns
- **PBTA** (Powered by the Apocalypse) — Mechanics patterns documented
- **FATE** — Aspect-based mechanics patterns documented
- **Blades in the Dark** — Faction and crew mechanics patterns documented

See [campaign-themes-by-system.md](templates/campaign-themes-by-system.md) for system-specific mechanics.

## Quick Start

### 1. Create Campaign Spec
```bash
speckit spec --preset game-rpg-narrative-writing --system d5e
```
This generates a campaign pitch with 13 sections to define your core concept, setting, party, conflict, factions, companions, and ending conditions.

### 2. Define Campaign Rules (Constitution)
The constitution template defines:
- Ability scores and skill modifiers
- Encounter CR scaling and XP awards
- Companion system (3 NPCs, -100 to +100 approval)
- Faction system (3-4 factions, -100 to +100 reputation)
- Seven ending conditions with lock timing
- Campaign themes (Dungeon Delving, Monster Hunt, Political Intrigue, Heist, etc.)

### 3. Plan Campaign Structure (Plan)
Structure your 15-session campaign with:
- Session-by-session goals and encounters
- NPC appearance timelines
- Companion recruitment schedule
- Faction reputation progression
- Ending gate viability tracking

### 4. Define Campaign Variables
Declare 150+ variables including:
- Ability scores (immutable)
- Skill modifiers (derived)
- Companion approval tracking
- Faction reputation tracking
- Plot flags and inventory items
- NPC state and combat tracking

### 5. Configure Mechanic Hooks
Choose from 8 hook types:
- **FLAG** — Binary story states (conspiracy_discovered)
- **COUNTER** — Numeric values with ranges (guard_rep: -100 to 100)
- **VISITED** — Location tracking (guard_headquarters)
- **INVENTORY** — Quest items (evidence_ledger)
- **TIMER** — Countdown mechanics (investigation_deadline)
- **TRUST** — NPC approval tracking (companion_1_approval)
- **CURRENCY** — Gold accumulation (party_gold)
- **NPC_STATE** — NPC status (alive/dead/wounded)

### 6. Generate Node Outlines
```bash
speckit outline --mode rpg --session 3
```

Generates outlines with:
- RPG beat summary and pacing breakdown
- Skill checks with DC, ability, success/failure outcomes
- Companion interactions with approval gates
- Faction effects with reputation changes
- Ending gate status showing viable paths

### 7. Implement Dialogue and Mechanics
```bash
speckit implement --mode rpg --outline node-session-3-01.md
```

Draft dialogue with:
- Skill check narration showing what characters learn
- Companion reactions announcing approval changes
- Faction announcements for reputation shifts
- Choice consequences documenting ending impact

### 8. Validate Campaign Structure
```bash
speckit verify --mode rpg --campaign
```

Validates:
- Skill check DCs within 5-20 range
- Companion approval within -100 to +100
- Faction reputation within -100 to +100
- 2-3 endings viable at Session 8, exactly 1 by Session 15
- All 3 companions recruited in logical sequence
- Skill checks balanced across abilities

## Campaign Structure

### Default: 15 Sessions, 290 Nodes, Party Levels 5→8

```
Session Range │ Nodes │ Level │ Encounters │ Notes
──────────────┼───────┼───────┼────────────┼──────────────────────
  1-5 (Act 1) │  ~85  │  5-6  │    4-5     │ Introduction, recruitment
  6-10 (Act 2) │ ~105  │  6-7  │    5-6     │ Main conflict, factions
11-15 (Act 3) │ ~100  │  7-8  │    6-7     │ Climax, endings
```

### Ending Gates

Endings lock at strategic points:
- **Session 3:** Initial lock (2-3 endings viable)
- **Session 8:** Mid-campaign lock (ending path clarifies)
- **Session 13:** Final lock (exactly 1 ending viable)

### Companion System

Three recruitable NPCs with:
- **Recruitment points** (Session 2, 5, 7-8)
- **Approval gates** (-10, 0, -5 thresholds for recruitment)
- **Conditional outcomes** (if alive, approval ≥ 76 for romance, < -N for leaving)
- **Ending-specific fates** (each ending defines companion outcomes)

### Faction System

Three to four factions with:
- **Starting reputation** (typically -20 to 20)
- **Session-by-session changes** (realistic arcs, -100 to 100 total range)
- **Ending requirements** (e.g., Just Ruler: guard_rep ≥ 50, temple_rep ≥ 60)
- **Cross-faction conflicts** (some endings require balancing factions)

## Campaign Themes

### 8 D&D 5e Themes

| Theme | Combat | Exploration | Social | Ideal Ending |
|-------|--------|-------------|--------|------------|
| **Dungeon Delving** | 60% | 30% | 10% | Cleared & Riches |
| **Monster Hunt** | 50% | 30% | 20% | Vanquished |
| **Political Intrigue** | 30% | 20% | 50% | Power Secured |
| **Heist** | 40% | 20% | 40% | Objective Stolen |
| **Investigation** | 20% | 40% | 40% | Mystery Solved |
| **Curse Breaking** | 40% | 40% | 20% | Curse Lifted |
| **Defense** | 70% | 10% | 20% | Settlement Saved |
| **Mixed/Open** | 30% | 30% | 40% | Various |

Each theme has:
- Customized skill check distribution
- Encounter type recommendations
- NPC archetype preferences
- Faction types that work well

See [campaign-themes-by-system.md](templates/campaign-themes-by-system.md) for cross-system theme analysis.

## File Structure

```
game-rpg-narrative-writing/
├── README.md (this file)
├── preset.yml
├── commands/
│   ├── speckit.outline.md (RPG-enhanced)
│   ├── speckit.implement.md (RPG-enhanced)
│   ├── speckit.verify.md (RPG validation)
│   └── (other shared commands)
├── templates/
│   ├── spec-d5e.md (campaign pitch)
│   ├── constitution-d5e.md (game rules & mechanics)
│   ├── plan-d5e.md (15-session structure)
│   ├── variables-d5e.md (150+ campaign variables)
│   ├── mechanics-d5e.md (8 hook types with 40+ examples)
│   ├── endings-d5e.md (7 endings with lock timing)
│   ├── node-outline-d5e-ink.md (Ink syntax examples)
│   ├── node-outline-d5e-sugarcube.md (SugarCube syntax examples)
│   ├── campaign-themes-by-system.md (D&D 5e, PBTA, FATE, Blades)
│   ├── campaign-instantiation-example.md (Syndicate Conspiracy walkthrough)
│   ├── mechanics-customization-guide.md (how to customize hooks)
│   └── d5e-template-system-overview.md (system architecture)
├── scripts/python/
│   ├── compile.py (shared)
│   ├── verify.py (shared)
│   ├── validate_ending_gates.py (RPG-specific)
│   ├── validate_reputation_arcs.py (RPG-specific)
│   ├── validate_companion_timelines.py (RPG-specific)
│   └── validate_skill_distribution.py (RPG-specific)
└── specs/
    └── (user campaigns go here)
```

## Export Engines

### Ink (Recommended for Professional/Portable)

- Compiles to JSON, runs in web or game engines (Unity, Godot)
- Game engine handles dice rolls via API
- `node-outline-d5e-ink.md` shows syntax and mechanics integration

### SugarCube (Best for Immediate Browser Play)

- Self-contained browser engine (Twee 3 format)
- Story layer handles dice rolls via `random(1,20)`
- No external engine needed for playtesting
- `node-outline-d5e-sugarcube.md` shows syntax and dice integration

## Validation Tools

### RPG-Specific Validators

- **validate_ending_gates.py** — Ensures 2-3 endings at Session 8, exactly 1 by Session 15
- **validate_reputation_arcs.py** — Tracks faction reputation realistic progressions
- **validate_companion_timelines.py** — Confirms 3 companions recruited in sequence with proper gates
- **validate_skill_distribution.py** — Verifies skill checks balanced across abilities (not 70% one type)

### Command-Line Validation

```bash
speckit verify --mode rpg --campaign
```

Runs 10 validation tests:
1. DCs within 5-20
2. Approvals within -100 to +100
3. Reputations within -100 to +100
4. Approval gates valid
5. Ending gates reachable
6. Reputations cumulative and realistic
7. Skill check outcomes narrated
8. Skill diversity balanced
9. NPC voices consistent
10. Companion timeline respected

## Customization

### Create Campaign for Different Theme

1. Copy spec-d5e.md → spec-your-theme.md
2. Customize campaign concept and setting
3. Adjust encounter mix in constitution based on theme
4. Use mechanics-customization-guide.md to adapt hook examples

### Create Campaign for Different System

- **PBTA:** See PBTA patterns in campaign-themes-by-system.md; create constitution-pbta.md
- **FATE:** See FATE patterns; create constitution-fate.md
- **Blades:** See faction patterns; create constitution-blades.md

See campaign-instantiation-example.md for step-by-step walkthrough of how concrete campaigns fill abstract template placeholders.

## Resources

- **d5e-template-system-overview.md** — Architecture documentation and interconnection matrix
- **campaign-themes-by-system.md** — Cross-system mechanics comparison
- **mechanics-customization-guide.md** — How AI generates alternative hook configurations
- **campaign-instantiation-example.md** — Concrete example (Syndicate Conspiracy) with SESSION-by-SESSION tracking

## Next Steps

1. Choose your system (D&D 5e, PBTA, FATE, or Blades)
2. Read d5e-template-system-overview.md to understand architecture
3. Start with spec-d5e.md to pitch your campaign concept
4. Use constitution-d5e.md to define your rules and mechanics
5. Follow plan-d5e.md to structure your sessions
6. Generate outlines with `speckit outline --mode rpg`
7. Validate your campaign with `speckit verify --mode rpg --campaign`

Happy specifying!
