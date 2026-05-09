# RPG Narrative Writing Preset

A Spec Kit preset for designing and implementing RPG campaigns—both tabletop and computer games—with flexible ruleset support and mechanics-driven narrative structure.

## Overview

This preset provides comprehensive templates and validation tools for creating RPG campaigns across:
- **Multiple rulesets**: D&D 5e (full support), Pathfinder 2e, Shadowrun 6e, and generic system-agnostic templates
- **Multiple platforms**: Tabletop campaigns (GM-run) and computer game implementations
- **Multiple genres**: Fantasy, Sci-Fi, Horror, Cyberpunk, Urban Fantasy, Steampunk, and more
- **Multiple export engines**: Generic Markdown, Sugarcube (web), Ink (dialogue scripting), Yarn Spinner (Unity/Godot)

Core narrative features include:
- **Campaign/Quest structure** with branching narrative and player agency
- **NPC characterization** with dynamic relationships and dialogue trees
- **World-building** with faction systems, location mechanics, and lore consistency
- **Encounter design** with skill checks, combat pacing, and consequences
- **Endings system** with multiple paths and variable-based locking

## Supported Rulesets

- **D&D 5e** (primary) — Complete templates for campaign design and mechanics
- **Pathfinder 2e** (planned) — Templates ready; mechanics pending
- **Shadowrun 6e** (planned) — Templates ready; mechanics pending
- **Generic/System-Agnostic** — Templates with no system-specific assumptions

See [campaign-themes-by-system.md](templates/campaign-themes-by-system.md) for system-specific guidance (D&D 5e themes documented; others in development).

## Quick Start

### 1. Initialize Campaign Constitution
```bash
speckit constitution
```

You'll be prompted to select:
1. **Ruleset** — D&D 5e (complete), Pathfinder 2e, Shadowrun 6e, or Generic
2. **Genre** — Fantasy, Sci-Fi, Horror, Cyberpunk, Urban Fantasy, Steampunk, Post-Apocalyptic, Historical, or Mixed
3. **Platform** — Tabletop (GM-run) or Computer Game (video game implementation)
4. **Export Engine** — Generic Markdown, Sugarcube (web), Ink (dialogue), or Yarn Spinner (game engines)

**For Tabletop:** Platform auto-excludes Ink engine; exports to generic Markdown and Sugarcube.
**For Computer Game:** All export engines available.

This generates `.specify/memory/constitution.md` with your campaign's rules and configuration.

### 2. Define Campaign Spec
```bash
speckit spec
```
This generates `specs/spec.md` with your campaign pitch:
- Core concept and dramatic question
- Setting and world rules
- Party/Protagonist overview (for computer games) or Player guidance (tabletop)
- Key conflicts and central premise
- Ending conditions and narrative goals

### 3. Configure Campaign Mechanics and Variables

**Mechanics** — Create `specs/mechanics.md` with:
- If D&D 5e: Encounter CR scaling, skill check ranges, loot tables, companion approval ranges
- If other ruleset: Relevant system mechanics with ranges and thresholds
- Universal hooks: FLAG (binary states), COUNTER (numeric), VISITED (locations), INVENTORY (items), TIMER (deadlines), TRUST (NPC approval), CURRENCY (resources), NPC_STATE (conditions)

**Variables** — Create `specs/variables.md` with:
- All tracked state (NPC approval, faction reputation, plot flags, inventory)
- Type, scope, default value, and persistence rules per export engine

### 4. Create Campaign Plan
```bash
speckit plan
```

Generates `specs/plan.md` with your campaign structure:
- **For Tabletop**: Session-by-session breakdown, NPC encounter timeline, skill check pacing, faction rep changes
- **For Computer Game**: Node-based flowmap, branching outcomes, player agency gates, ending path tracking
- Ruleset-specific mechanics integration (D&D 5e uses encounter CR balance, Shadowrun uses action economy, etc.)

### 5. Create Node Outlines
```bash
speckit outline
```

Generates node outlines from the plan with:
- Beat summary and pacing
- Skill checks or ability-relevant challenges (ruleset-specific)
- NPC interactions with relationship states
- Mechanic hooks to trigger (flags, counters, state changes)
- Choice branching and consequence mapping

### 6. Draft Nodes
```bash
speckit implement
```

Draft node content with:
- Prose body (narration, dialogue, environmental description)
- Mechanic hook blocks embedded in narrative
- Choice list with branch targets and conditions
- Variables read/write for state management

### 7. Verify and Polish
```bash
speckit verify
```

Validates campaign structure:
- All variables registered and used correctly
- Endings reachable via at least one path
- Mechanic hooks compatible with target export engine
- Choices properly formatted for export

### 8. Export Campaign
```bash
speckit compile --engine [generic|sugarcube|ink|yarn-spinner]
```

Exports narrative and mechanics to your target platform:
- **Generic**: Annotated Markdown (universal, portable)
- **Sugarcube**: Twee 3 / Sugarcube 2 (web-based RPG tools)
- **Ink**: Inkle dialogue scripting (dialogue-heavy games)
- **Yarn Spinner**: Yarn Spinner format (Unity/Godot RPGs)

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
│   ├── constitution-template.md (unified game bible — all rulesets)
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
│   ├── map-export.py (RPG map data export)
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
4. Run `speckit constitution` — it generates a single constitution.md covering all ruleset configuration
5. Follow plan-d5e.md to structure your sessions
6. Generate outlines with `speckit outline --mode rpg`
7. Validate your campaign with `speckit verify --mode rpg --campaign`

Happy specifying!
