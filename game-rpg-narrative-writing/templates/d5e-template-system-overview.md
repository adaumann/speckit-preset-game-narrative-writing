---
title: "D&D 5e Template System Overview"
description: "Complete guide to all D&D 5e templates, their purposes, and how they connect"
---

# D&D 5e Template System Overview

Complete reference for the D&D 5e template system: what files exist, what they do, and how they flow into the Spec Kit commands.

---

## Directory Structure

```
templates/
├── Core D&D 5e Templates (Campaign-Specific)
│   ├── spec-d5e.md                          # Campaign pitch & initialization
│   ├── constitution-template.md             # Game bible & system rules (unified, all rulesets)
│   ├── plan-d5e.md                          # Campaign structure (15 sessions, 290 nodes)
│   ├── variables-d5e.md                     # State registry (~150 variables)
│   ├── mechanics-d5e.md                     # Mechanic hooks (8 types, 40+ hooks)
│   ├── endings-d5e.md                       # 7 possible endings & gates
│   │
│   ├── Outline Templates (Node-Level)
│   ├── node-outline-d5e-ink.md              # Sample Ink syntax with D&D mechanics
│   └── node-outline-d5e-sugarcube.md        # Sample SugarCube syntax with dice rolling
│
├── Reference & Customization Guides
│   ├── mechanics-customization-guide.md     # How to create mechanics for other themes
│   ├── campaign-instantiation-example.md    # How templates fill with concrete values
│   └── [THIS FILE]                          # You are here
│
└── Pending/Lower Priority Templates
    ├── characters-d5e.md                    # NPC stat blocks (not yet created)
    ├── encounters-d5e.md                    # Monster & loot definitions
    ├── skills-d5e.md                        # DC progression & mapping
    └── factions-d5e.md                      # Faction definitions & rep tracking
```

---

## Template Dependency Flow

```
spec-d5e.md (Campaign Pitch)
    ↓ (User approves & clarifies)
constitution-template.md (Game Bible)
    ↓ (Defines system rules & mechanics)
plan-d5e.md (Campaign Structure)
    ↓ (15 sessions × ~19 nodes = 290 nodes)
variables-d5e.md (State Registry)
    ↓ (References available variables)
mechanics-d5e.md (Hooks Configuration)
    ↓ (How variables change with choices)
endings-d5e.md (Ending Gates)
    ↓ (Final state evaluation at Node 280)
node-outline-d5e-ink.md / .sugarcube.md (Engine-Specific Outlines)
    ↓ (Beat sheets for each node)
speckit.outline → speckit.implement → speckit.validate → speckit.compile
```

---

## Each Template's Purpose

### 1. spec-d5e.md — Campaign Initialization

**What it is:** High-level campaign pitch and planning document

**Contains:**
- Core concept (logline, dramatic question)
- Setting & world
- Party & characters (class suggestions, party size)
- Core conflict & antagonists
- Companion NPCs (3 recruitment points, romance gates)
- Possible endings (5-7 branching outcomes)
- Tone & style
- Campaign arc (Acts 1-3 breakdown)
- **7 unresolved questions (OQ-001 through OQ-007) for speckit.clarify**
- Success criteria checklist

**When used:**
- Start of campaign design
- `speckit.clarify` input (resolves OQ-NNN items)
- Communication tool (share pitch with players)

**Example template placeholder:**
```yaml
logline: "[ONE_SENTENCE_HOOK_ABOUT_CAMPAIGN]"
dramatic_question: "[WHAT_MUST_PARTY_RESOLVE]"
party_size: "[4-6]"
party_level_range: "[5-8]"
```

---

### 2. constitution-template.md — Game Bible

**What it is:** Complete D&D 5e system rules & campaign-specific mechanics for THIS campaign

**Contains:**
- Party composition (HP, abilities, proficiencies)
- D&D ability/skill system (d20 formula, DC scale 5-20)
- Encounter CR scale & XP awards
- Monster templates & stat blocks
- Loot & treasure tables
- Companion system (3 NPCs, approval scale)
- Faction system (3-4 factions, reputation scale)
- Ending conditions (7 endings, their gates)
- Campaign variables (immutable ability scores, mutable state)
- Dialogue tone & craft rules
- Unmodified throughout campaign

**When used:**
- `speckit.plan` reads to understand party progression
- `speckit.implement` reads for NPC stat blocks
- `speckit.validate` reads for encounter checking

**Immutability:** These values DON'T change (unlike plan which has per-session breakdown)

---

### 3. plan-d5e.md — Campaign Structure

**What it is:** Session-by-session breakdown of 15-session campaign

**Contains:**
- Acts 1-3 structure (5 sessions each)
- Session goals, encounters, node ranges
- Companion recruitment timeline (which session, approval gates)
- Faction reputation arc (starting values, session-by-session changes)
- Skill check distribution (DCs by level, frequency)
- Ending gates matrix (which endings still viable after each session)
- Encounter list (boss battles, mob encounters, social)
- XP progression (level-up thresholds, 5→8 progression)
- **Total: 290 nodes (NODE_001 through NODE_290)**

**When used:**
- `speckit.outline --all` reads node ranges (001-085 Act 1, 086-190 Act 2, 191-290 Act 3)
- `speckit.implement --all` reads session goals & companion timelines
- `speckit.validate` checks progression against plan

**Key insight:** Plan is the SKELETON; nodes are the flesh

---

### 4. variables-d5e.md — State Registry

**What it is:** Complete list of all ~150 campaign variables and their ranges

**Contains:**
- Ability scores (immutable: STR, DEX, CON, INT, WIS, CHA mods)
- Skill modifiers (derived from ability + proficiency)
- Companion approval (-100 to +100 scale, 3 companions)
- Faction reputation (-100 to +100 scale, 3-4 factions)
- Quest items (evidence_ledger, temple_key, etc.)
- Combat state (HP tracking, spell slots, damage taken)
- Currency (party_gold, spending tracked)
- Skill check history (success/failure rates by skill)
- NPC state (location, status, opinion)
- Choice memory (major decisions logged)
- **Ink/SugarCube initialization block** (paste into first node)

**When used:**
- `speckit.outline` validates all hook references exist in variables
- `speckit.implement` uses variables for dialogue conditions
- `speckit.compile` exports variables to Ink/SugarCube

**Critical:** This is THE source of truth for what variables exist

---

### 5. mechanics-d5e.md — Mechanic Hooks Configuration

**What it is:** Configuration for all 8 mechanic hook types with concrete campaign examples

**Contains:**
- 8 Hook Types defined:
  1. **FLAG** — Binary states (conspiracy_discovered, ending_reached)
  2. **COUNTER** — Numeric values (faction_rep, companions_recruited)
  3. **VISITED** — Location tracking (guard_hq, temple_sanctuary)
  4. **INVENTORY** — Quest items (evidence_ledger, temple_key)
  5. **TIMER** — Countdown mechanics (investigation_deadline)
  6. **TRUST** — NPC approval (companion_approval)
  7. **CURRENCY** — Wealth tracking (party_gold)
  8. **NPC_STATE** — NPC conditions (npc_location, npc_status)
- Each hook type has 5-15 examples
- **SAMPLE CAMPAIGN PATTERN** section showing these are examples
- **YOUR CAMPAIGN ALTERNATIVES** sections showing how to customize

**When used:**
- `speckit.outline` validates nodes only use defined hooks
- `speckit.compile` translates hooks to engine-specific syntax (Ink vs. SugarCube)
- `speckit.checklist` validates no undefined hooks used

**Key insight:** These are samples! Other campaigns have different hooks following same pattern.

---

### 6. endings-d5e.md — Ending Conditions (7 Endings)

**What it is:** Complete definition of all 7 possible campaign endings

**Contains (per ending):**
- **Requirements:** Primary gates (ALL must be true), Secondary gates (AT LEAST N must be true)
- **Lock timing:** When ending becomes impossible
- **Companion outcomes:** Who dies, who survives, who gets what role
- **World changes:** Consequential shifts in setting
- **Character endings:** What party does in epilogue
- **Narrative consequences:** Society-wide impacts
- **Hidden costs/benefits:** Moral dimensions

**Seven Endings:**
1. **Just Ruler** — Law & order through Guard cooperation
2. **Shadow Broker** — Criminal empire maintained secretly
3. **Redemption** — Moral awakening, peace through reform
4. **Revolution** — Violent upheaval, new power structure
5. **Power Vacuum** — Chaos from lack of central authority
6. **Tragic Defeat** — Conspiracy succeeds (always available)
7. **Pyrrhic Victory** — Victory at terrible cost

**When used:**
- `speckit.consequences --all` validates ending gates
- `speckit.endings` generates epilogue for reached ending
- `speckit.compile` includes all ending branches

**Validation checklist included**

---

### 7a. node-outline-d5e-ink.md — Ink Engine Template

**What it is:** Working example showing Ink 5e syntax with D&D mechanics

**Contains:**
- NODE structure (`=== NODE_NAME ===`)
- 4 worked examples showing:
  1. Skill check gate with success/failure branches
  2. Companion approval reaction
  3. Faction reputation gate
  4. Inventory-based branching
- Variable initialization block (copy-paste into story.ink)
- How game engine passes ability_mod and check_result
- 7 example endings with variable combinations
- Linking pattern (`-> NODE_020_DIALOGUE`)

**When used:**
- Copy structure for own Ink nodes
- Reference for speckit.implement when generating Ink dialogue
- Shows how to integrate D&D mechanics (dice rolls, ability mods)

**Key syntax:**
```ink
{player_insight >= difficulty_dc: SUCCESS_OUTCOME - else: FAILURE_OUTCOME}
{thorne_approval > 75: warm_reaction}
{inventory_has("evidence_ledger"): show_evidence}
```

---

### 7b. node-outline-d5e-sugarcube.md — SugarCube Engine Template

**What it is:** Working example showing SugarCube 2.x Twee 3 syntax with self-contained dice rolling

**Contains:**
- NODE structure (`:: NODE_NAME [scene]`)
- 4 worked examples showing:
  1. Self-contained d20 roll with `random(1, 20)`
  2. Companion approval branching
  3. Faction gate with multiple conditions
  4. Inventory check with link branches
- Variable initialization block (StoryData, set statements)
- Dice rolling directly in story layer (NOT game engine)
- Links syntax (`[[Label|NODE_NAME]]`)

**When used:**
- Copy structure for own SugarCube nodes
- Reference for self-contained web-based playtesting
- Shows simpler alternative to Ink (no external engine needed)

**Key syntax:**
```twee
<<set $insightRoll to random(1, 20)>>
<<set $insightTotal to $insightRoll + $insightMod>>
<<if $insightTotal gte $insightDC>> SUCCESS <<else>> FAILURE <</if>>
[[Option Label|NODE_020]]
```

---

## Reference/Guide Templates (Customization)

### mechanics-customization-guide.md

**What it is:** How to customize mechanics for different campaign themes

**Contains:**
- How investigation-theme maps to other themes (Monster Hunt, Heist, Political, Curse)
- Theme substitution patterns
- 8 Hook Customization Matrix (per hook type, show variations)
- How to request custom hooks from AI
- Common mistakes & testing checklist

**Example:**
```
Investigation theme:
  conspiracy_discovered → Monster Hunt theme: monster_confirmed
  evidence_ledger → Monster heart
  conspirators_caught → monsters_slain
```

---

### campaign-instantiation-example.md

**What it is:** How concrete campaign fills abstract template placeholders

**Contains:**
- "Syndicate Conspiracy" example showing each step:
  - spec-d5e placeholder → concrete value
  - constitution-template.md variables → campaign ratios
  - plan-d5e → session breakdown
  - variables-d5e → faction reputation progression
  - endings-d5e → ending gate calculation
- Comparison table showing how different themes instantiate identically
- AI generation process (Template → Customization → Instantiation)

---

## Pending Templates (Not Yet Created)

### characters-d5e.md (PENDING)
- NPC stat blocks for 3 companions
- NPC personalities & approval reactions
- Major antagonist stat block
- Boss enemy templates

### encounters-d5e.md (PENDING)
- Monster stat blocks (varied CRs)
- Encounter difficulty matrices
- Loot tables (by CR, treasure type)
- Trap descriptions

### skills-d5e.md (PENDING)
- DC progression by party level
- Skill check node mapping (which skills checked where)
- Proficiency bonus progression
- Skill check difficulty scaling

### factions-d5e.md (PENDING)
- Faction definitions (motivations, leadership, territory)
- Starting reputation values
- Reputation change triggers
- Faction conflict matrix (who opposes whom)

---

## How Templates Feed Into Spec Kit Commands

### speckit.constitution
**Input:** spec-d5e.md (user pitch)
**Output:** constitution-template.md (generated or updated)
**Template selection:**
- d5e (D&D 5e) → Populates Section XIII (D&D 5e Campaign Configuration) in constitution-template.md
- Generic → Leaves Section XIII blank

---

### speckit.plan
**Input:** constitution-template.md
**Uses:**
- Party level range to scale encounters
- Campaign goal/setting for session breakdown
- Faction count to create reputation arcs

---

### speckit.clarify
**Input:** spec-d5e.md (OQ-NNN unresolved questions)
**Output:** Updated spec-d5e.md with answers
**Example:** OQ-001: "How do players meet first companion?" → Answer filled in → constitution-template.md updated

---

### speckit.outline
**Input:** plan-d5e.md, variables-d5e.md, mechanics-d5e.md
**Output:** Beat sheets for NODE_001 through NODE_290
**Process:**
1. Read node ranges from plan-d5e.md (e.g., Act 1: NODE_001-085)
2. Validate all referenced variables exist in variables-d5e.md
3. Check all hooks used in conditions defined in mechanics-d5e.md
4. Generate beat sheet template for each node

---

### speckit.implement
**Input:** Outline (beat sheets), variables-d5e.md, mechanics-d5e.md
**Output:** Dialogue draft for each node
**Uses:**
- Companion approval timeline from plan-d5e.md
- Faction reputation progression from mechanics-d5e.md
- Character tone from constitution-template.md

---

### speckit.consequences
**Input:** endings-d5e.md, mechanics-d5e.md
**Output:** Validation report of ending gates & hook consistency
**Checks:**
- All ending gates reference valid variables from variables-d5e.md
- No ending requires impossible combinations
- At least 2-3 endings viable after Session 8
- Reputation changes cumulative

---

### speckit.compile --engine ink
**Input:** endings-d5e.md + implemented nodes, variables-d5e.md
**Output:** story.html (Ink + JSON compiled to web)
**Uses:**
- Variables list for Ink binding requirements
- Endings for epilogue branching
- node-outline-d5e-ink.md as structure template

---

## Template Interconnection Matrix

| Template | Reads | Writes | Used By |
|---|---|---|---|
| spec-d5e.md | — | (user creates) | clarify, constitution |
| constitution-template.md | spec-d5e.md | (framework) | plan, outline, implement |
| plan-d5e.md | constitution-template.md | session structure | outline, implement, validate |
| variables-d5e.md | plan-d5e.md | state registry | outline, implement, compile |
| mechanics-d5e.md | variables-d5e.md | hook definitions | outline, consequences, compile |
| endings-d5e.md | mechanics-d5e.md | ending gates | consequences, compile |
| node-outline-d5e-ink.md | constitution-template.md | (reference) | implement (Ink target) |
| node-outline-d5e-sugarcube.md | constitution-template.md | (reference) | implement (SugarCube target) |

---

## Customization Pathways

### Option 1: Use As-Is (D&D 5e Conspiracy)
```
spec-d5e.md → fill placeholders → constitution-template.md
→ plan-d5e.md (auto-generated) → outline → implement
```

### Option 2: Modify for D&D 5e Different Theme
```
spec-d5e.md (Monster Hunt) → constitution-template.md (updated)
→ plan-d5e.md (regenerated) → mechanics-d5e.md (customized)
→ outline → implement
```

### Option 3: Use Different System (Future)
```
constitution-pbta.md (Powered by the Apocalypse)
→ plan-pbta.md → variables-pbta.md → mechanics-pbta.md
→ outline → implement
```

---

## Quality Checklist Before Using

- [ ] All 7 templates present in templates/ directory
- [ ] spec-d5e.md filled with campaign pitch
- [ ] constitution-template.md generated (via `speckit constitution`)
- [ ] plan-d5e.md contains 15 sessions with node ranges
- [ ] variables-d5e.md lists 130+ variables
- [ ] mechanics-d5e.md defines 40+ hooks
- [ ] endings-d5e.md has 7 endings with gates
- [ ] `speckit.outline` runs without errors
- [ ] `speckit.implement` produces node dialogue
- [ ] `speckit.consequences` validates ending gates

---

**Status:** D&D 5e core template system ready for outline generation  
**Next:** Generate node outlines with `speckit.outline --all`
