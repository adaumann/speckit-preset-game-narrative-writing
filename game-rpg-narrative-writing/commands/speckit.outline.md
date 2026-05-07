---
description: Generate editable node outline files from plan.md. Authors review and approve each outline before AI drafting begins, or mark SKIP to write their own prose.
handoffs:
  - label: Start Drafting
    agent: speckit.implement
    prompt: Draft nodes from approved outlines
    send: true
  - label: Check Branch Structure First
    agent: speckit.plan
    prompt: Node targets or branch logic conflict with the flowmap. Please review and fix it.
    send: true
---

# speckit.outline

Generate a node outline (`outlines/NODE-NNN.md`) for one or more nodes. Outlines must be reviewed and approved before `speckit.implement` will draft the node.

## User Input

```text
$ARGUMENTS
```

You **MUST** consider the user input before proceeding (if not empty). Accepted arguments:
- `[NODE_ID]` � generate outline for a single node (e.g. `NODE-003`)
- `[NODE_ID] [NODE_ID] ...` � generate outlines for a list of nodes
- `--act [N]` � outline all nodes for a given act
- `--force` � regenerate an existing outline (overwrite)
- `--batch` / `--all` — generate outlines for ALL nodes listed in `plan.md` that do not yet have an outline- `--mode rpg` — include RPG-specific outline sections (skill checks, companion interactions, faction effects, ending gates)- *(no argument)* — outline the next unoutlined node from `plan.md`

## Pre-Execution Checks

**Check for extension hooks (before outline generation)**:
- Check if `.specify/extensions.yml` exists in the project root.
- If it exists, read it and look for entries under the `hooks.before_outline` key.
- Process as standard hook block (Optional/Mandatory). Skip silently if absent.

**Extract Platform & Ruleset** (auto-detect RPG context):
- Read `.specify/memory/constitution.md` YAML frontmatter and extract `[PLATFORM]` and `[RULESET]`
- If `[PLATFORM]` = "Tabletop": Enable Tabletop-specific outline sections
- If `[PLATFORM]` = "Computer Game": Enable Computer Game-specific outline sections
- If `[RULESET]` = "D&D 5e": Use D&D 5e skill DC ranges (5-20), approval ranges (-100 to +100)
- If `[RULESET]` = "Pathfinder 2e": Use PF2e skill DC ranges (10-50+), hero points, degree of success
- If `[RULESET]` = "Shadowrun 6e": Use SR6e karma/edge, matrix vs street vs astral routing
- Store platform/ruleset context for conditional section generation

Then:
1. Confirm `specs/[FEATURE_DIR]/plan.md` and `.specify/memory/constitution.md` exist.
2. For each requested node, verify it appears in `plan.md` – warn if not found.
3. **Skip any node that already has an outline file with `status: APPROVED` or `status: SKIP`** � never overwrite approved or skipped outlines unless `--force` is set.
4. Confirm `specs/[FEATURE_DIR]/variables.md` exists � hooks cannot be declared without it.

## Outline

**Goal**: Generate structured, decision-complete node outlines in `outlines/` that give the author all the information needed to approve the node before drafting begins.
**Language Rule**: All node outlines MUST be generated in English (`en`) by default, regardless of any `[LANGUAGE]` setting in the constitution. This stage remains in English to facilitate author review against project specifications.

### Player Character Configuration (RPG Tabletop Only)

**Activated when**: `[PLATFORM]` = "Tabletop" AND no `specs/player-classes.md` exists (first-time setup)

If running outline for the first time on a tabletop campaign, auto-generate `specs/player-classes.md` with:

#### Section 1: Character Classes & Progression

**D&D 5e** (if `[RULESET]` = "D&D 5e"):

| Class | Hit Dice | Primary Attribute | Proficiency | Skills | Special |
|-------|----------|-------------------|-------------|--------|---------|
| Barbarian | d12 | Strength | Medium armor, shields | Athletics, survival | Rage (damage resistance) |
| Bard | d8 | Charisma | Light armor | Insight, persuasion, deception | Spell slots, inspiration |
| Cleric | d8 | Wisdom | Light/medium armor, shields | Medicine, insight, religion | Channel divinity, healing |
| Druid | d8 | Wisdom | Light armor, shields | Medicine, nature, survival | Wild shape, spell slots |
| Fighter | d10 | Strength/Dexterity | All armor, shields | Athletics, perception | Second wind, multiple attacks |
| Monk | d8 | Dexterity | None (unarmored AC) | Acrobatics, insight, stealth | Ki points, unarmed strikes |
| Paladin | d10 | Strength + Charisma | All armor, shields | Athletics, insight, persuasion | Divine smite, lay on hands |
| Ranger | d10 | Dexterity + Wisdom | Light/medium armor, shields | Insight, nature, perception, stealth | Favored enemy, spellcasting |
| Rogue | d8 | Dexterity | Light armor | Acrobatics, deception, insight, perception, sleight of hand, stealth | Sneak attack, expertise |
| Sorcerer | d6 | Charisma | None | Arcana, insight, perception | Sorcery points, spell slots |
| Warlock | d8 | Charisma | Light armor | Arcana, deception, insight, perception | Pact magic, invocations |
| Wizard | d6 | Intelligence | None | Arcana, insight, investigation, medicine, perception, religion | Spellbook, cantrips, arcane recovery |

**Pathfinder 2e** (if `[RULESET]` = "Pathfinder 2e"):

| Class | Hit Points | Proficiencies | Special | Class Features |
|-------|------------|---------------|---------|--------------------|
| Alchemist | 8 + CON | Crafting, alchemy | Infusions, quick alchemy | Alchemy specialties |
| Barbarian | 12 + CON | Athletics, survival | Rage actions | Instinct choice |
| Bard | 8 + CON | Occultism, performance | Inspiration, spellcasting | Muse selection |
| Champion | 10 + CON | All armor | Deity/cause choice | Reaction-based actions |
| Cleric | 8 + CON | Deity choice | Healing/harm spells | Domain selections |
| Druid | 8 + CON | Primal magic | Wild shape | Primal order choice |
| Fighter | 10 + CON | All armor & weapons | Bonus actions | Weapon specialization |
| Monk | 10 + CON | Martial arts unarmed | Flurry of blows | Monastic tradition |
| Paladin | 10 + CON | Deity/oath choice | Divine ally | Tenets enforcement |
| Ranger | 10 + CON | Survival specialty | Monster hunting | Ranger specialization |
| Rogue | 8 + CON | Light armor, stealth | Sneak attack | Racket choice |
| Sorcerer | 6 + CON | Bloodline spellcasting | Spontaneous spells | Bloodline selection |
| Wizard | 6 + CON | Intelligence focus | Prepared spells | Arcane school |

**Shadowrun 6e** (if `[RULESET]` = "Shadowrun 6e"):

| Archetype | Role | Special Abilities | Core Attributes | Essence Cost |
|-----------|------|-------------------|------------------|--------------|
| Street Samurai | Melee specialist | Weapon specialization, armor | STR + AGI | Varies by cybernetics |
| Rigger | Vehicle operator | Drone control, vehicle mods | RXN + LOG | Vehicle-dependent |
| Decker | Hacker | Matrix actions, device control | LOG + INT | Cyberdeck required |
| Shaman | Spirit summoner | Spell casting, spirit allies | WIL + CHA | Bound spirits |
| Sorcerer | Combat mage | Spell casting, drain resistance | LOG + WIL | Mana pool-based |
| Face | Social specialist | Persuasion, infiltration | CHA + INT | Charisma-focused |
| Physad | Adept martial artist | Physical enhancement, abilities | STR + AGI + WIL | Initiative boost |

#### Section 2: Ability Scores & Racial Modifiers

**D&D 5e** (if `[RULESET]` = "D&D 5e"):

Ability Score Generation Method: [Standard Array (8, 10, 12, 13, 14, 15) / Point Buy / Roll 4d6]

**Races & Bonuses**:

| Race | STR | DEX | CON | INT | WIS | CHA | Special |
|------|-----|-----|-----|-----|-----|-----|---------|
| Human | +1 | +1 | +1 | +1 | +1 | +1 | Extra feat at level 1 |
| Dwarf | +2 CON | +2 WIS | — | — | — | — | Medium size, 25 ft speed |
| Elf | — | +2 DEX | — | — | — | — | Darkvision 60 ft, trances instead of sleep |
| Halfling | — | +2 DEX | — | — | — | — | Small size, lucky trait |
| Dragonborn | +2 STR | — | — | — | — | +2 CHA | Dragon ancestry, breath weapon |
| Gnome | — | — | — | +2 INT | — | — | Small size, gnome cunning |
| Half-Elf | — | — | — | — | — | +2 CHA | +1 to 3 other abilities |
| Half-Orc | +2 STR | — | +1 CON | — | — | — | Darkvision 60 ft |
| Tiefling | — | — | — | — | — | +2 CHA | Infernal heritage, innate spells |

**Pathfinder 2e** (if `[RULESET]` = "Pathfinder 2e"):

All abilities start at 10. Select 4 ability boosts during creation (raise 2 abilities +2, or 1 ability +2 and increase HP).

**Ancestries & Bonuses**:

| Ancestry | Ability Boosts | Special | Heritage Options |
|----------|---------------|---------|--------------------|
| Human | +2 free choice | Extra feat at 1st | Diverse backgrounds |
| Dwarf | +2 CON, +2 WIS, -2 CHA | Darkvision 60 ft | Stone-blooded, hardy |
| Elf | +2 DEX, +2 INT, -2 CON | Darkvision 60 ft | Keen-eyed, low-light vision |
| Gnome | +2 CON, +2 CHA, -2 STR | Small size, darkvision 60 ft | Fey-touched, fey wings |
| Goblin | +2 DEX, +2 CHA, -2 WIS | Small size, darkvision 60 ft | Burn bright, oversized teeth |
| Halfling | +2 DEX, +2 WIS, -2 STR | Small size | Halfling luck, keen eyes |
| Orc | +2 STR, +2 CON, -2 INT | Darkvision 60 ft | Intimidating strike, powerful build |

**Shadowrun 6e** (if `[RULESET]` = "Shadowrun 6e"):

**Attributes** (Rating 1-6, start 2-4):

| Metatype | STR | AGI | RXN | STR | WIL | LOG | INT | CHA | Edge | Essence |
|----------|-----|-----|-----|-----|-----|-----|-----|-----|------|---------|
| Human | — | — | — | — | — | — | — | — | +1 | Standard |
| Elf | — | +1 | — | — | — | — | — | +1 | — | Standard |
| Dwarf | +1 | — | — | +1 | — | — | — | — | — | Standard |
| Orc | +2 | — | — | +2 | — | -1 | — | -1 | — | 0.5 less |
| Troll | +2 | -1 | — | +2 | — | -1 | — | -2 | — | 0.5 less |

#### Section 3: Skill Recommendations by Class

**D&D 5e**: List suggested skills per class (e.g., Rogues → Stealth, Sleight of Hand, Acrobatics; Clerics → Medicine, Insight, Religion)

**Pathfinder 2e**: Each class has trained skills at 1st level (pick from available trained skills) + 4 additional trained skills

**Shadowrun 6e**: Skill ratings (1-12), skill specializations, knowledge skills specific to archetype

#### Section 4: Feats, Abilities & Starting Equipment

**D&D 5e**:
- Feat selection at 1st level (if variant rules)
- Class-specific features (Barbarian's Unarmored Defense, etc.)
- Starting equipment packages

**Pathfinder 2e**:
- Ancestry feat at 1st level (heritages)
- Background grant, class feats, archetype options

**Shadowrun 6e**:
- Spells / Adept powers / Drone configuration
- Starting gear & Priority allocation (Metatype, Attributes, Magic/Resonance, Skills, Resources)

#### Section 5: Character Creation Briefing (Player Introduction)

Include in `SESSION-0-BRIEFING.md`:

```markdown
# Character Creation for [CAMPAIGN_NAME]

## Ruleset: [D&D 5e / Pathfinder 2e / Shadowrun 6e]

### Step 1: Choose Race
Available races: [list from above table]
Recommended for this campaign: [top 2-3 races that fit world/campaign]

### Step 2: Choose Class
Available classes: [list from above table]
Recommended for this campaign: [top 3-4 classes, briefly why]

### Step 3: Assign Ability Scores
Use: [Standard Array / Point Buy / Roll 4d6]

Recommended ability score priority for [CLASS]:
1. [Primary attribute] (highest)
2. [Secondary attribute]
3. [Tertiary attribute]

### Step 4: Choose Skills & Feats
[Follow class progression from player-classes.md]

### Step 5: Equipment & Starting Resources
[Generate starting equipment checklist per class]
```

---

### Companion & NPC Stat Block Builder (RPG Tabletop Priority 1)

**Activated when**: `[PLATFORM]` = "Tabletop" AND no `specs/npc-roster.md` exists (first-time setup)

If running outline for the first time on a tabletop campaign, auto-generate `specs/npc-roster.md` with stat blocks for all companions and major NPCs.

#### NPC Stat Block Template (All Rulesets)

For each companion/significant NPC, create a standardized entry in `specs/npc-roster.md`:

```markdown
## [NPC_NAME]

**NPC ID**: NPC-[N]  
**Role**: [Companion / Quest-giver / Enemy / Faction Leader / Merchant / other]  
**Faction**: [Faction affiliation, if any]  
**Introduction Session**: [SESSION-N]  
**Recruitment Gate**: [if companion: skill check DC, companion loyalty trigger, or faction requirement]  

### I. Character Details

| Attribute | Value |
|-----------|-------|
| **Age/Appearance** | [Brief description for DM reference] |
| **Personality** | [Core traits: brave, cunning, loyal, etc.] |
| **Motivation** | [Why does this NPC act? What do they want?] |
| **Flaw/Weakness** | [What can undermine their cooperation?] |

### II. Mechanical Stats (per Ruleset)

#### [RULESET Selected]

**[Stat Block Details - see ruleset-specific subsections below]**

### III. Combat Role (if applicable)

| Element | Value |
|---------|-------|
| **Combatant Type** | [Melee / Ranged / Caster / Support / Non-combatant] |
| **Armor Class** | [N] |
| **Hit Points** | [N] |
| **Damage Output** | [Average damage per round] |
| **Special Abilities** | [If any: spellcasting, abilities, item effects] |

### IV. Companion Approval States

| Approval Range | State | Behavior | Recruitment | Ending Availability |
|---|---|---|---|---|
| >= 50 | **Ally** | Aids party actively, shares secrets, opens companion quest | Recruited | Available in all endings except tragic |
| 0 to 49 | **Friendly** | Cooperates, provides normal quest assistance | Recruitable with effort | Available in most endings |
| -50 to -1 | **Wary** | Helpful but cautious, withholds secrets, may refuse quest assistance | Hard to recruit, requires major approval boost | Limited ending availability |
| -100 | **Betrayed** | Actively opposes party, betrays trust, becomes enemy | Impossible to recruit | Not available, may fight party |

**Starting Approval**: [Default value, typically 0-10]  
**Max Approval**: [Typically 100, unless NPC is antagonist]  
**Min Approval**: [-100, indicates complete betrayal/enmity]  

### V. Dialogue Trees (if major NPC)

Key dialogue options by approval state:

| Approval | Key Dialogue | Approval Change Options |
|----------|---|---|
| **High** | [Companion shares personal quest or secret] | [±0: neutral path], [+2: support their goal], [-5: refuse to help] |
| **Mid** | [Companion proposes quest cooperation] | [+2: accept], [-1: refuse], [+1: negotiate terms] |
| **Low** | [Companion questions party trust] | [+5: convince them], [-10: betrayal becomes real], [±0: defensive] |

### VI. Ending Fates (Narrative Closure)

| Ending | Fate | Approval Gate | Notes |
|--------|------|---|---|
| [ENDING-A] | [What happens to this NPC] | [Approval >= N] | [Impact on story/world] |
| [ENDING-B] | [Alternative outcome] | [if approval < M] | [Alternative impact] |

**Example**: If approval >= 50 at campaign end: NPC becomes faction leader. If approval < 0: NPC leaves party/joins enemies.

### VII. Notes for DM

- **Roleplay Tips**: [Suggested voice, mannerisms, common phrases]
- **Tactical Advice**: [How should DM play this NPC in combat?]
- **Story Triggers**: [Which events should cause approval changes?]
- **Red Flags**: [Common mistakes in running this NPC]
```

#### D&D 5e NPC Stat Block

**Template** (use for any combatant NPC):

```markdown
### II. Mechanical Stats (D&D 5e)

**Class/Level**: [Class] [N]  
**Armor Class**: [AC]  
**Hit Points**: [HP] ([N d(X) + (N)]  
**Speed**: [30 ft., or special movement]  

| STR | DEX | CON | INT | WIS | CHA |
|-----|-----|-----|-----|-----|-----|
| +N  | +N  | +N  | +N  | +N  | +N  |

**Saving Throws**: [If higher than ability mod, e.g., WIS +3]  
**Skills**: [Acrobatics +3, Perception +4, etc.]  
**Damage Resistances**: [If applicable]  
**Senses**: [Passive Perception N, Darkvision 60 ft., etc.]  
**Languages**: [Common, Thieves' Cant, etc.]  
**Challenge**: [CR N (XP value)] 

**Class Features**:
- [Feature 1]: [Brief description]
- [Feature 2]: [Brief description]

**Spellcasting** (if applicable):
- **Spellcaster Level**: [N]
- **Spell Save DC**: [N]
- **Spell Attack Bonus**: [+N]
- **Cantrips** (at will): [list]
- **Spell Slots**: [1st: N, 2nd: N, etc.]
- **Spells Known/Prepared**: [List major spells by level]

**Actions**:
- **Multiattack**: [N attacks per turn, or special action economy]
- **[Weapon/Spell Name]**: [+N to hit; Reach N ft.; Hit: N (NdN+N) damage]
- **[Special Ability]**: [Description and effect]

**Bonus Actions**:
- **[Ability Name]**: [Description]

**Reactions**:
- **[Reaction Name]**: [Trigger and effect]

**Resources** (if tracked):
- **Action Surge**: [Usages remaining]
- **Spellcasting Focus**: [Item or component]
```

**Example D&D 5e NPC**:
```markdown
### II. Mechanical Stats (D&D 5e)

**Mira Voss (Companion Rogue)**
**Class/Level**: Rogue 4  
**Armor Class**: 15 (Leather Armor + DEX)  
**Hit Points**: 27 (4d8 + 8)  
**Speed**: 30 ft.  

| STR | DEX | CON | INT | WIS | CHA |
|-----|-----|-----|-----|-----|-----|
| +0  | +3  | +2  | +1  | +1  | +2  |

**Skills**: Acrobatics +5, Perception +3, Sleight of Hand +5, Stealth +7  
**Senses**: Passive Perception 13  
**Languages**: Common, Thieves' Cant  

**Expertise**:
- Sleight of Hand: Advantage on checks; can always take 10 on checks
- Stealth: Same as above

**Actions**:
- **Multiattack**: Two attacks per turn (shortsword or hand crossbow)
- **Shortsword**: +5 to hit; 1d6 + 3 damage. If offhand weapon available: bonus action shortsword +5 for 1d4 + 3.
- **Hand Crossbow**: +5 to hit; 1d6 + 3 damage.

**Reactions**:
- **Uncanny Dodge**: When hit by attack, use reaction to halve damage (1/turn)

**Resources**:
- **Sneak Attack Dice**: 4d6 (2d6 when hidden, 4d6 when ally within 5 ft. of target)
```

#### Pathfinder 2e NPC Stat Block

**Template**:

```markdown
### II. Mechanical Stats (Pathfinder 2e)

**Class/Level**: [Class] [N]  
**Ancestry**: [Heritage, if important]  
**Armor Class**: [AC from armor]  
**Hit Points**: [HP] ([N d(X) + (N)]  
**Speeds**: [Movement type: N ft.]  

| STR | DEX | CON | INT | WIS | CHA |
|-----|-----|-----|-----|-----|-----|
| +N  | +N  | +N  | +N  | +N  | +N  |

**Saving Throws**:
- **Fortitude**: [+N]
- **Reflex**: [+N]
- **Will**: [+N]

**Skills**: [Acrobatics +N, Medicine +N, etc.]  
**Immunities/Resistances**: [If applicable]  
**Senses**: [Perception +N, special senses]  
**Languages**: [Common, etc.]  

**Hero Points**: [N per encounter/day]  

**Abilities**:
- **[Class Ability Name]**: [Effect and usage]
- **[Ancestry Ability]**: [Effect]

**Spellcasting** (if applicable):
- **Spell Save DC**: [N]
- **Spell Attack Bonus**: [+N]
- **Cantrips**: [List]
- **Spell Slots**: [1st: N, 2nd: N, etc.]

**Actions**:
- **Multiattack**: [Actions available per turn]
- **[Weapon/Spell]**: [+N to hit or save DC; effects on hit/success]

**Reactions**:
- **[Reaction]**: [Trigger and effect]
```

#### Shadowrun 6e NPC Stat Block

**Template**:

```markdown
### II. Mechanical Stats (Shadowrun 6e)

**Archetype**: [Street Samurai / Rigger / Decker / Shaman / Mage / Face / etc.]  
**Rating**: [1-10, overall power level]  
**Essence**: [Current / Max (e.g., 2.5 / 6)]  

| STR | AGI | RXN | STR | WIL | LOG | INT | CHA |
|-----|-----|-----|-----|-----|-----|-----|-----|
| +N  | +N  | +N  | +N  | +N  | +N  | +N  | +N  |

**Condition Monitor**:
- **Physical**: [N boxes] (8 + CON/2)
- **Stun**: [N boxes] (8 + WIL/2)

**Skills** (Rating 1-N):
- [Combat Skills]: [Automatics +N, Pistols +N, etc.]
- [Technical Skills]: [Hacking +N, Electronics +N, etc.]
- [Social Skills]: [Con +N, Persuasion +N, etc.]

**Specializations**: [Special training in one skill, +2 dice]

**Resources**:
- **Karma**: [Current / Max]
- **Edge**: [Current / Max]
- **Nuyen**: [Carrying cash]

**Gear**:
- **Weapons**: [List with damage codes, e.g., "Katana: 4P"]
- **Armor**: [Rating N, e.g., "Lined Armor Jacket: 6/4"]
- **Cybernetics**: [List with essence cost, e.g., "Smartlink: 0.1 essence"]
- **Magic/Resonance**: [If applicable: "Spells: Fireball (Force 6), Invisibility (Force 4)"]
- **Vehicles/Drones**: [If applicable]

**Spells/Powers** (if mage/shaman/adept):
- **Fireball**: Force [N], Damage Code [NP]
- **Invisibility**: Force [N], Duration [T turns]
- **Adept Power**: [Name and effect]

**Special Abilities**:
- **[Name]**: [Effect and triggering condition]
```

#### NPC Roster Registry Template

**Create `specs/npc-roster.md` Index**:

```markdown
# NPC Roster

| NPC ID | Name | Role | Faction | Intro Session | Recruitment | Starting Approval | Max Ending Fate |
|--------|------|------|---------|---|---|---|---|
| NPC-001 | Mira Voss | Companion (Rogue) | Thieves Guild | SESSION-2 | Loyalty >= 50 at SESSION-2 | 10 | Leader/Dead/Betrayer |
| NPC-002 | Brother Theron | Companion (Cleric) | Temple | SESSION-1 | Loyalty >= 0 at SESSION-1 | 20 | Faction Leader/Sacrifice |
| NPC-003 | Lord Cassian | Quest-giver | City Guard | SESSION-1 | N/A (NPC, not companion) | 0 | Ally/Enemy |
| NPC-004 | Duchess Alyssa | Faction Leader | Kingdom | SESSION-3 | N/A (enemy first, optional ally late) | -25 | Ally/Dead/Betrayer |

**Totals**: 4 companions possible, 2 factions (Thieves / Temple), 3-4 major quest-givers, 15 sessions
```

---

### Execution Steps

1. **Setup**: Run `{SCRIPT}` from repo root and parse JSON for spec file paths.
   - **Detect platform/ruleset**: Extract `[PLATFORM]` and `[RULESET]` from constitution.md (performed during Pre-Execution Checks)
   - Outline generation automatically adapts to detected platform/ruleset context for each node

2. **Load source documents**:
   - **Required**: `specs/plan.md` (node graph, branch dependencies, act breakdown), `specs/spec.md` (NPC profiles, variable registry, research gaps)
   - **Required**: `.specify/memory/constitution.md` (enabled mechanics list, world rules, tone, target platform, `prose_profile`)
   - **Required**: `specs/mechanics.md` (hook schemas, tier levels, translations, parameter definitions for all declared hooks including newly added ones)
   - **Required**: `specs/endings.md` (ending IDs, variable gates, thematic statements) -- needed to validate all choice targets
   - **Required**: `specs/characters.md` index + `specs/characters/` profiles (NPC trust thresholds, state behaviors, bark lines, dialogue consistency)
   - **Required if style_mode is humanized-ai**: `.specify/memory/craft-rules.md` (to tune beat language and dialogue register per active prose profile)
   - **Optional**: `specs/variables.md` (declared variables with types and value ranges) -- validate Variables Read and Variables Set sections
   - **Optional**: `specs/glossary.md` (terminology registry) -- load if present; check outline for any terminology that should be flagged for consistency checking during drafting
   - **Optional**: `specs/locations.md` (sensory anchors, location rules) -- load if present; populate location context in outline if this node takes place in a key location
   - **Optional**: `specs/themes.md` -- load if present; use to populate the Thematic work field in the outline Beat Summary: match the node's act to the Thematic Arc by Act table, and check whether any registered motif (MO-NNN) or symbol has a planned occurrence in this node
   - **Optional**: `specs/world-building.md` (location sensory anchors, world rules)
   - **RPG-Tabletop Optional** (if platform detected): `specs/player-classes.md` (available classes, races, attributes), `specs/items.md`, `specs/bestiary.md`, `specs/quests.md`, `specs/npc-roster.md`, `specs/puzzles.md`
   - **RPG-Computer Optional** (if platform detected): `specs/player-classes.md` (playstyle archetypes, accessibility variants), `specs/npc-roster.md`, `specs/locations.md`   - Note any missing required documents -- abort with clear error if `specs/endings.md` or `specs/characters.md` missing
   - Note any missing optional documents � affected outline sections are marked `[TBD � populate <document>]`

3. **Determine target nodes**:
   - If `$ARGUMENTS` is `--batch` or `--all`: find ALL nodes in `plan.md` that do not yet have an outline file and process them in order.
   - If `$ARGUMENTS` is empty: find the first node in `plan.md` that has no outline file yet.
   - If `$ARGUMENTS` is a node ID or list: use those nodes.
   - If `$ARGUMENTS` is `--act N`: use all nodes in that act without an existing outline file.
   - Skip any node already outlined with `status: APPROVED` or `status: SKIP` (unless `--force`).

4. **For each target node, generate an outline file**:

   **Output path**: `outlines/[NODE_ID].md`

   Use `templates/node-outline-template.md` as the base structure. Populate each section from the source documents:

   **Frontmatter** — pull from `plan.md` node entry:
   - `node_id`, `title`, `act`, `status: DRAFT`, `pov` (from constitution.md default or node override)

   **Beat Summary** � derive from the flowmap node entry:
   - 2�4 sentences: what happens in this node, what the player is doing or deciding
   - Narrative purpose: `decision / consequence / revelation / setup / hub / transition / climax / ending`
   - Tension level: 1�10 with brief rationale

   **Variables Read** � derive from flowmap branch conditions into this node:
   - Each variable used as a gate or prose condition, with expected value and source node
   - Flag any variable not yet declared in `variables.md` with `[UNDECLARED]`

   **Variables Set** � derive from flowmap annotations and constitution.md hook schemas:
   - Each variable changed by this node, with hook type, new value/delta, and trigger condition
   - Flag any variable not yet declared in `variables.md` with `[UNDECLARED]`

   **Choices** — derive all outgoing edges from `plan.md`:
   - Minimum 2 choices for non-terminal nodes; 0 for ending nodes
   - Each choice: label, condition (if conditional), target node ID, narrative consequence
   - Default path if no conditional choices are met

   **Dialogue Tree** — *only if node is flagged `(dialogue-centric)` or `(mixed)` in plan.md*:
   - Structure player dialogue options and NPC responses within the node
   - Each dialogue choice includes: player phrase, NPC responses by character, gating/variable effects
   - Include all NPCs present in this node; each NPC uses their correct dialogue register from `specs/characters/[NPC_ID].md` Section VIII
   - Multi-party reactions: both/all NPCs respond to the player's dialogue choice (shown in sequence)
   - Dialogue sub-branches: indicate if a dialogue choice continues in-node or branches to a different node
   - If no structured dialogue tree is needed, mark as `None`

   **Mechanic Hooks Summary & Checklist** — Identify all mechanics relevant to this node:
   
   1. **First, derive explicit hooks** from `specs/mechanics.md` and flowmap annotations:
      - All hooks already triggered: type, tier (1 or 2), variable, action, timing
      - Include any custom hooks added via `speckit.mechanics declare`

   2. **Then, use the Mechanic Hooks Checklist** (in template) to identify forgotten mechanics:
      
      For each node type, prompt the author through these common patterns:
      - **Dialogue-centric** (dialogue-heavy prose_profile or dialogue-centric flag):
        - ✓ CHOICE_MEMORY (record which dialogue option player chose)
        - ✓ TRUST (dialogue choice should affect NPC trust by ±N)
        - ✓ NPC_STATE (dialogue can change NPC mood or relationship tier)
        - ✓ FLAG (dialogue might reveal secrets or flag new knowledge)
        
      - **Quest/Task hub** (setup or hub narrative purpose):
        - ✓ COUNTER (track active quests, attempts, or rounds)
        - ✓ INVENTORY (check prerequisites, award completion items)
        - ✓ VISITED (mark location explored)
        
      - **Investigative/Mystery** (contains clue discovery or evidence gathering):
        - ✓ CLUE (discover evidence piece)
        - ✓ INVENTORY (collect physical evidence)
        - ✓ COUNTER (track evidence collected, theories tested)
        
      - **Timed challenge** (tension level 7+, obstacle or puzzle):
        - ✓ TIMER (start countdown or ticking timer)
        - ✓ COUNTER (track attempts or rounds remaining)
        - ✓ ENDING_CONDITION (major success/failure consequence)
        
      - **Choice consequence** (decision node with multiple paths):
        - ✓ TRUST (choice affects NPC relationships)
        - ✓ FLAG (choice unlocks/locks paths)
        - ✓ NPC_STATE (NPC reacts to choice)
        - ✓ ENDING_CONDITION (choice pushes toward specific ending)
        
      - **Any node with player resources (items, money, health)**:
        - ✓ INVENTORY (track items acquired/lost)
        - ✓ CURRENCY (track resources spent/gained)

   3. **Populate the template's Mechanic Hooks Checklist**: 
      - Check the boxes for all mechanics that should apply to this node
      - Fill in the summary table at the top with the concrete hooks
      - Reference "Common Hook Combinations" section if uncertain

   **Branch Logic Notes** � pull from flowmap annotations:
   - Any complex gate logic, reachability conditions, or POV overrides
   - If this node is only reachable via specific upstream variable states, document them here

   **Game Bible Compliance Notes** � scan `constitution.md` for:
   - Any mechanic or hook constraints relevant to this node
   - Platform/engine limits on choice count or variable types
   - POV rules or tone requirements that apply

   **Deviations from plan.md** — default to `None`. Only populate if the outline generation process identified an inconsistency (e.g. a variable read in this node that no upstream node sets).

   **Ending Gate Validation** — derive from `specs/endings.md`:
   - For each choice in the Choices table:
     - If the target node ID is a terminal node: verify it maps to a valid `END-NNN` entry in `specs/endings.md`
     - Flag any choice target that is not in `plan.md` as `[MISSING NODE]`
     - Flag any ending node reference that has no corresponding `END-NNN` in `specs/endings.md` as `[UNREGISTERED ENDING]`

   **Location & Sensory Context** — load from `specs/locations.md` if present:
   - If this node's title or POV mentions a location, find that location in `specs/locations.md`
   - Populate a new **Setting Anchors** field in the outline with sensory and rule details from the location profile
     - E.g., "Sanctuary Station: sterile white walls, hum of life support, restricted entry"
   - If location is absent from locations.md, mark as `[LOCATION PROFILE NEEDED]`

   **Terminology Cross-Check** — load from `specs/glossary.md` if present:
   - Scan beat summary and choice labels for any specialized terminology
   - If any term appears in both the outline and `specs/glossary.md`, cross-reference the definition in the Glossary section of the outline
   - Flag any term used that is not in the glossary (for writer awareness during drafting) as `[GLOSSARY NOTE]`

5. **Outline quality rules**:
   - Every beat must be one sentence � no prose
   - If a `[NEEDS CLARIFICATION]` marker is present in the flowmap entry, propagate it into the outline � do not invent a resolution
   - A variable listed in Variables Read must be set by at least one upstream node in `plan.md` — flag otherwise
   - No choice may target a node ID not present in `plan.md`
   - The outline is a brief, not a draft � no narrative prose, no dialogue text

6. **Report**: List all outline files created with their output paths and `status: DRAFT`. Include a per-node summary: `[NODE_ID] [title] — [N] beats, [N] choices, [N] variables set, [ending gates], act [N]`. Flag any:
   - `[UNDECLARED]` variables
   - `[MISSING NODE]` choice targets
   - `[UNREGISTERED ENDING]` terminal nodes
   - `[LOCATION PROFILE NEEDED]` locations not in locations.md
   - `[GLOSSARY NOTE]` terminology not in glossary.md
   - Propagated `[NEEDS CLARIFICATION]` markers
   - **RPG-specific flags** (if platform/ruleset detected):
     - `[UNBALANCED SKILL CHECKS]`, `[COMPANION TIMELINE CONFLICT]`, `[ENDING GATE UNREACHABLE]`, `[REPUTATION SPIKE]`, `[SKILL CHECK DISCONNECT]`
     - `[DIFFICULTY LOCK]`, `[PLAYSTYLE ROUTING UNBALANCED]`, `[MISSING ACCESSIBILITY]`
   
   Remind the author to:
   - Review each outline file and edit beats, choices, and variable tables as needed
   - **Complete the Mechanic Hooks Checklist** for each node — check all applicable hook types (dialogue-centric nodes should include CHOICE_MEMORY + TRUST + NPC_STATE; quest hubs should include COUNTER + INVENTORY; timed challenges should include TIMER; etc.)
   - **Review platform/ruleset-specific sections** (if RPG outline): Verify skill checks, companion interactions, faction effects, difficulty scaling are appropriate
   - Verify ending gates are still viable and tracked correctly
   - Check accessibility features for puzzles/timed challenges (if Computer Game platform)

---

## Platform & Ruleset-Specific Outline Sections

**Auto-detection**: Platform (`[PLATFORM]`) and ruleset (`[RULESET]`) are automatically detected from constitution.md during Pre-Execution Checks. Appropriate sections are generated for each node based on detected values. No `--mode rpg` flag needed—all RPG contexts are handled automatically.

---

## I. Tabletop RPG Outline Extensions

**Activated when**: `[PLATFORM]` = "Tabletop" in constitution.md

Add these sections to the standard outline (in addition to standard Beat Summary, Variables, Choices, Dialogue Tree, Mechanic Hooks):

### A. Session Context

| Field | Value |
|-------|-------|
| **Session Number** | [1-15, or applicable session count] |
| **Story Arc** | [Act 1 / Act 2 / Act 3 / Climax / Epilogue] |
| **Expected Party Level** | [Level range where this node appears] |

### B. NPCs Present

List all NPCs who appear or are referenced in this node:

| NPC Name | Role | Faction | Approval Impact | Notes |
|----------|------|---------|-----------------|-------|
| [NAME] | [Role: Leader / Quest-giver / Ally / Enemy] | [Faction] | [±N approval if recruited companion] | [Brief context: only appears if condition met?] |

### C. Encounter Summary (if applicable)

| Element | Details |
|---------|---------|
| **Encounter Type** | [Combat / Social / Stealth / Puzzle / Exploration / Hybrid] |
| **CR (if combat)** | [CR, or "N/A"] |
| **Expected Difficulty** | [Easy / Medium / Hard / Deadly] |
| **Combat Participants** | [Number of enemies and their types, e.g., "2 Thugs (CR 1/8 each), 1 Guard (CR 1/4)"] |
| **Alternative Bypass** | [Skill check or social option that bypasses combat? Or "No bypass—mandatory combat"] |

### D. Skill Check Opportunities

| Skill | DC | Ability | Success Outcome | Failure Outcome | Mandatory? |
|-------|----|---------|-----------------|-----------------|-|
| [SKILL] | [N] | [Ability] | [Consequence] | [Consequence] | [Yes/No] |

**Validation**:
- Every DC must be 5-20 (D&D 5e scale) or system-appropriate
- Each check should genuinely affect story progression
- At least one skill check path per scene (unless pure combat/roleplay)

### E. Session Pacing Notes

- **Combat %**: [Estimated percentage of time in combat]
- **Social %**: [Estimated percentage of roleplay/dialogue]
- **Exploration %**: [Estimated percentage of travel/discovery]
- **Investigation %**: [Estimated percentage of puzzle-solving/clue gathering]
- **Total Time Estimate**: [X hours typical session time for this node]

---

## II. Computer Game RPG Outline Extensions

**Activated when**: `[PLATFORM]` = "Computer Game" in constitution.md

Add these sections to the standard outline (in addition to standard Beat Summary, Variables, Choices, Dialogue Tree, Mechanic Hooks):

### A. Playthrough Context

| Field | Value |
|-------|-------|
| **Chapter** | [1-X, or act-based chapter numbering] |
| **Expected Playtime** | [Minutes from node entry to exit] |
| **Quest Type** | [Main / Side / Optional / Companion] |
| **Player Level** | [Recommended level range] |

### B. Playstyle Routing

For each major path through this node, indicate which playstyles lead there:

| Playstyle | Node Paths | % of Players Routing This Way | Notes |
|-----------|-----------|-------------------------------|-------|
| **Combat** | [NODE IDs or location names] | [~X%] | [Difficulty scaling: Easy/Normal/Hard] |
| **Dialogue** | [NODE IDs or location names] | [~X%] | [Skill checks or persuasion gates?] |
| **Exploration** | [NODE IDs or location names] | [~X%] | [Hidden paths or discovery-based?] |

**Validation**:
- All three playstyles should reach the same story beat (no locking players out of major plot)
- Rewards should be roughly equivalent across playstyles (same XP, similar items)
- Travel times should be comparable (combat route shouldn't be 5× faster than dialogue)

### C. Difficulty Scaling Variants

If this node includes combat encounters or puzzles, document Easy/Normal/Hard adjustments:

| Difficulty | Encounter Changes | Loot Changes | XP Changes |
|------------|-------------------|--------------|------------|
| **Easy** | [Lower enemy count, -2 AC, more healing items] | [Standard loot] | [80% XP] |
| **Normal** | [Standard encounter] | [Standard loot] | [100% XP] |
| **Hard** | [Additional enemies, +2 AC, minion reinforcements] | [+1 rare item] | [120% XP] |

### D. Dialogue Tree Structure (if dialogue-heavy)

For nodes with significant branching dialogue:

| Dialogue Choice | Leads To | NPCs Affected | Approval/Rep Changes | Notes |
|-----------------|----------|---------------|---------------------|-------|
| [Player phrase] | [NODE or location] | [Which companions react?] | [±N with whom?] | [Locks other paths?] |

### E. Accessibility & UI Notes

- **Puzzle Accessibility**: [Colorblind mode?] [Audio alternatives?] [Adjustable timers?]
- **Dialogue Accessibility**: [Subtitles?] [Audio description?] [Text size adjustable?]
- **Motor Accessibility**: [Timed sequences?] [Button alternatives?] [Remappable controls?]
- **Cognitive Accessibility**: [Text clarity?] [Objective markers?] [Hint system?]

---

## III. D&D 5e-Specific Outline Sections

**Activated when**: `[RULESET]` = "D&D 5e" in constitution.md

### A. Skill Checks (D&D 5e)

| Skill | DC | Ability | Success Outcome | Failure Outcome | Party Alternative |
|-------|----|---------|-----------------|-----------------|-|
| [SKILL_NAME] | [5-20] | [Ability] | [Consequence] | [Consequence] | [Can party find alternate solution?] |

**D&D 5e Validation**:
- DC 5-9 = Very Easy
- DC 10-12 = Easy
- DC 13-15 = Medium
- DC 16-18 = Hard
- DC 19-20 = Very Hard
- DC 21+ = Nearly Impossible (should be rare and justified)

### B. Companion Interactions (D&D 5e)

| Companion | Approval Threshold | Reaction | Approval Change | Recruitable? |
|-----------|-------------------|----------|-----------------|--------------|
| [NAME] | if_approval >= [N] | [What does companion say/do?] | [±N per outcome] | [Yes/No/Already recruited] |

**D&D 5e Validation**:
- Approval ranges from -100 to +100
- Recruitment typically requires approval >= -50 or >= 0 (based on companion personality)
- Romance gates typically at approval >= 75
- Betrayal/leaving at approval <= -100

### C. Faction Reputation Effects (D&D 5e)

| Faction | Session Start Rep | Rep Change Trigger | Rep Delta | Effect at New Rep | Notes |
|---------|-------------------|--------------------|-----------|-------------------|-------|
| [FACTION] | [Base rep] | if_[choice] | [±N] | [Story consequence at new total] | [Any ending gate implications?] |

**D&D 5e Validation**:
- Factions typically range -100 to +100
- Cumulative changes across 15 sessions should total ±50 to ±100 (not hitting extremes until mid/late campaign)
- No single node should exceed ±25 rep per faction

### D. Ending Gate Tracking (D&D 5e)

| Ending | Required Gate | Current Status After This Node | Viable? | Session Locked? |
|--------|---------------|--------------------------------|---------|-----------------|
| [NAME] | [guard_rep >= 50, temple_rep >= 60, etc.] | [On track / At risk / Locked out] | [Yes/No] | [Session # when locked] |

---

## IV. Pathfinder 2e-Specific Outline Sections

**Activated when**: `[RULESET]` = "Pathfinder 2e" in constitution.md

### A. Skill Checks (Pathfinder 2e - Degree of Success)

| Skill | DC | Ability | Critical Success | Success | Failure | Critical Failure | Party Alternative |
|-------|----|---------|----|--|--|---|---|
| [SKILL] | [10-50+] | [Ability] | [Best outcome] | [Good outcome] | [Bad outcome] | [Worst outcome] | [Alternate solution?] |

**Pathfinder 2e Validation**:
- DC 10-11 = Easy
- DC 12-15 = Medium
- DC 16-20 = Hard
- DC 21-30 = Very Hard
- DC 31+ = Extremely Difficult
- Degree of success system means failure/critical failure often have milder consequences than D&D 5e

### B. Hero Points & Heroic Actions (Pathfinder 2e)

For nodes where hero points might be spent:

| Point Available? | Available For | Cost | Effect |
|------------------|---------------|------|--------|
| [Yes/No] | [Combat / Skill Check / Reroll / Other] | [# hero points] | [Benefit] |

### C. Ancestry & Background Implications (Pathfinder 2e)

If this node's outcome varies by ancestry/background:

| Ancestry/Background | Special Option? | Description | Approval/Rep Impact |
|---------------------|---|---|---|
| [Ancestry] | [Yes/No] | [What can they do differently?] | [±N rep if faction-relevant] |

### D. Resonance & Treasure Distribution (Pathfinder 2e)

- **Resonance Tracking**: [Does resonance matter in this node? Track sources]
- **Treasure Placement**: [Items allocated to party members per PF2e loot tables for party level]
- **Consumables**: [Potions, scrolls, other consumables distributed]

---

## V. Shadowrun 6e-Specific Outline Sections

**Activated when**: `[RULESET]` = "Shadowrun 6e" in constitution.md

### A. Dice Pool Checks (Shadowrun 6e)

For key tests in this node:

| Check Type | Pool | Threshold | Glitch Risk | Success Outcome | Glitch/Failure Outcome |
|-----------|------|-----------|-------------|-----------------|----------------------|
| [SKILL+ATTRIBUTE] | [# dice] | [Hits needed] | [Yes/No] | [Consequence] | [Consequence] |

**Shadowrun 6e Validation**:
- Pool = Skill rating + Attribute rating + modifiers
- Glitch on 2+ 1s rolled (regardless of successes)
- Always-on threats in Shadowrun (Matrix, Astral, Corporate security)

### B. Routing: Street vs Matrix vs Astral (Shadowrun 6e)

| Approach | Available? | Specialization Needed? | Team Role | Karma Cost | Success Outcome |
|----------|-----------|---|---|---|---|
| **Street (Physical)** | [Yes/No] | [Combat / Stealth / Social] | [Decker / Rigger / Face / Street Samurai / Mage] | [Karma spent] | [Consequence] |
| **Matrix (Hacking)** | [Yes/No] | [Hacking / Data Theft / System Control] | [Decker only] | [Karma spent] | [Consequence] |
| **Astral (Magic)** | [Yes/No] | [Spellcasting / Summoning / Spirit Work] | [Mage / Shaman] | [Karma spent] | [Consequence] |

**Shadowrun 6e Validation**:
- All three routes should be viable (no forced specialization)
- Rewards should be equivalent across routes (karma, nuyen, info)
- Matrix/Astral routes should offer unique intel or advantages

### C. Karma & Edge Tracking (Shadowrun 6e)

| Karma Source | Karma Earned | Edge Use? | Edge Regain? | Total Session Karma |
|---|---|---|---|---|
| [Objective completion / Roleplaying / Mission success] | [# karma] | [Yes/No, used for?] | [When restored?] | [Running total] |

### D. Contacts & Street Cred (Shadowrun 6e)

| Contact | Street Cred Impact | Networking Opportunity | Rep Tier | Notes |
|---------|---|---|---|---|
| [Contact Name] | [±X Street Cred] | [Can recruit for follow-up?] | [1-10] | [Professional rivalry / alliance?] |

---

## VI. RPG Quality Checklist (Auto-Generated Per Platform & Ruleset)

When outline is generated for an RPG preset, automatically validate:

**All RPG Contexts**:
- ✓ All referenced variables exist in system-specific variables file (variables-d5e.md, variables-pf2e.md, etc.)
- ✓ All NPCs mentioned have profiles in specs/characters/
- ✓ All ending gates are reachable (no impossible combinations)
- ✓ Ending gate viability is tracked (at least 2-3 endings remain viable until Session 13+)

**Tabletop-Specific**:
- ✓ Encounter CRs are appropriate to party level (±2 CR)
- ✓ Skill checks have documented alternatives or progression paths
- ✓ Companion arcs have no soft-locks (recruitment → progression → fate is clear)
- ✓ Session pacing adds up to realistic session length (2-4 hours typical)
- ✓ NPC presence is documented (no surprise NPCs appearing without context)

**Computer Game-Specific**:
- ✓ Playstyle routing is balanced (combat/dialogue/exploration all viable)
- ✓ Difficulty scaling is consistent (no difficulty locks story progression)
- ✓ Accessibility features are documented (colorblind, audio, motor, cognitive)
- ✓ Dialogue trees have reasonable branching (not >10 immediate choices)

**D&D 5e-Specific**:
- ✓ Skill check DCs fall within 5-20 range (5-9 Easy, 10-12 Easy, 13-15 Med, 16-18 Hard, 19-20 V.Hard)
- ✓ Approval gates fall within -100 to +100 range
- ✓ Faction reps are cumulative and realistic for campaign length
- ✓ Magic item rarity aligns with party level

**Pathfinder 2e-Specific**:
- ✓ Skill DCs follow PF2e scale (10-11 Easy, 12-15 Med, 16-20 Hard, 21-30 V.Hard, 31+ Extreme)
- ✓ Degree of success system acknowledged (critical success vs. success vs. failure outcomes documented)
- ✓ Hero points availability and costs are documented
- ✓ Treasure allocated per PF2e loot tables

**Shadowrun 6e-Specific**:
- ✓ All three routing options (Street / Matrix / Astral) are genuinely available
- ✓ Dice pools are documented with realistic thresholds
- ✓ Karma economy is tracked (no excessive karma dumping in single node)
- ✓ Street Cred and Contact networking opportunities are clear

## VII. RPG-Mode Warning Flags

Flag these issues for author review (auto-generated based on context):

- ⚠️ `[UNBALANCED SKILL CHECKS]` – Only one ability being tested (should diversify Str/Dex/Con/Int/Wis/Cha checks)
- ⚠️ `[COMPANION TIMELINE CONFLICT]` – Companion appears before recruitment or after death
- ⚠️ `[ENDING GATE UNREACHABLE]` – This ending can no longer be reached after this node's changes
- ⚠️ `[REPUTATION SPIKE]` – Single node changes faction rep by >±25 (should be distributed)
- ⚠️ `[SKILL CHECK DISCONNECT]` – Skill check result doesn't actually affect story progression
- ⚠️ `[DIFFICULTY LOCK]` – Difficulty setting locks player out of story on Hard (all content should be completable)
- ⚠️ `[PLAYSTYLE ROUTING UNBALANCED]` – One playstyle takes significantly longer (>2× as much time as others)
- ⚠️ `[MISSING ACCESSIBILITY]` – Puzzle or timed challenge lacks accessibility features (colorblind, motor, audio alternatives)

---

---
   - Verify ending gates are correct (choice targets are valid ending IDs or intermediate nodes)
   - Check sensory anchors for location-based nodes
   - Change `status: DRAFT` ? `status: APPROVED` when satisfied, or `status: SKIP` to write the node themselves
   - Run `speckit.implement` once outlines are approved

7. **Check for extension hooks** (after generation): check `hooks.after_outline`.

