# Strategic Shift: Narrative Design Focus (v0.2)

## What Changed

The `game-narrative-writing` preset has been refocused from **"RPG/Point-and-Click Game Creation"** to **"Narrative Design Validation Tool"**.

### Previous Direction (v0.1)
- RPG mechanics (D&D 5e, combat, quests)
- Point-and-click support (Escoria, animations, etc.)
- Game engine integration (Godot, Baldur's Gate)
- Problem: Too broad, too complex, requires game dev expertise

### New Direction (v0.2)
- **Narrative design validation** (story structure, branching, dialogue)
- **SugarCube/Twine export** (rapid prototyping, browser testing)
- **Designer-friendly** (focuses on story, not engine details)

---

## What Was Removed

| Component | Reason | Affected Files |
|---|---|---|
| **Point-and-click references** | Not core narrative design | `mechanics-template.md` |
| **Escoria/AGS/Unity exports** | Engine-specific, not narrative | `mechanics-template.md` |
| **Ink/Ren'Py exports** | Too many platforms; SugarCube is the proof-of-concept | `constitution-template.md` |
| **RPG Tier 3 hooks** | Move/Audio/Hotspot are engine concerns, not narrative | `mechanics-template.md` |
| **Game implementation scope** | Focus on design, not runtime | README + product scope |

---

## What Was Added

### 1. **Player Attributes Mechanic**
New first-class mechanic for character stats that gate dialogue choices:
- Predefined: `intelligence`, `wisdom`, `power`, `gold`
- Custom: User-defined attributes per game
- Use case: Dialogue choices require minimum stat values
- Export: Full SugarCube/Twine support

**File:** `templates/mechanics-template.md` (Attribute section)

### 2. **Character Profile Template**
Complete template for defining player character:
- Identity (name, background, appearance)
- Starting attributes (values, ranges, defaults)
- Personality & alignment
- Relationships & faction standings
- Inventory starting state
- Character arc & development notes

**File:** `templates/character-profile-template.md` (NEW)

### 3. **Simplified Constitution (Mechanics Selection)**
Designers now **opt-in** to mechanics:
- Checkbox list: Which mechanics does your narrative use?
- Attribute configuration: Define custom attributes
- Inventory configuration: Setup starting items
- Removed RPG/Point-and-Click specific configs

**File:** `templates/constitution-template.md` (Section II revised)

### 4. **Twine/SugarCube Export Guidance**
Two new comprehensive guides:
- `speckit.outline-twine-export.md` — How outlines translate to Twee
- `speckit.implement-twine-export.md` — How prose becomes SugarCube macros

**Files:** `commands/speckit.outline-twine-export.md` (NEW), `commands/speckit.implement-twine-export.md` (NEW)

### 5. **Shrine Sample (Minimal Narrative)**
A **much simpler** reference implementation:
- 3 scenes, 1 NPC, 3 attributes, ~30 min playthrough
- Focuses on dialogue branching + attribute gating + inventory checks
- Good for learning narrative design patterns
- Complements (not replaces) Witchhunter

**File:** `specs/shrine-sample/README.md` (NEW)

---

## Architecture: The New Workflow

```
NARRATIVE DESIGN (speckit)
    ├─ Define player character (attributes, starting inventory)
    ├─ Plan scene structure (nodes, branches, dialogue options)
    ├─ Outline each node (mechanics, gates, consequences)
    ├─ Implement prose (dialogue, descriptions, branching)
    └─ Export to SugarCube
        │
        └─ PLAYABLE PROTOTYPE (browser-based testing)
            ├─ Verify dialogue gates work
            ├─ Test attribute changes
            ├─ Validate branching logic
            └─ Share with stakeholders/testers

THEN: External Engines (Optional)
    ├─ Extract narrative specs (JSON/YAML)
    ├─ Port to game engine (Unity, Godot, etc.)
    └─ Build full game (art, audio, mechanics)
```

**Key principle:** Speckit is the **narrative design tool**, not the game engine. SugarCube is the **test bed**, not the deployment platform.

---

## Core Mechanics (Simplified)

### What's In
✅ **Flag** — Boolean state (quest done, NPC met, puzzle solved)
✅ **Counter** — Integer tracking (reputation, day count)
✅ **Visited** — First-visit detection (intro dialogue)
✅ **Inventory** — Item management (keys, tools, collectibles)
✅ **Attribute** — Player stats (intelligence, wisdom, power, gold, custom)

### What's Out
❌ Combat system (D&D mechanics, armor class, etc.)
❌ Movement/navigation (Escoria walks, hotspots)
❌ Audio/animation scripting (SFX triggers, sprite animation)
❌ Procedural generation (encounter tables, weighted loot)
❌ Session persistence (save/load systems)

---

## Sample Projects

### Shrine Sample (NEW) — "Hello World for Narrative Design"
**Use when:**
- Learning the tool
- Understanding dialogue gating
- Testing simple branching

**Scope:** 3 nodes, ~1 NPC, attribute-gated dialogue, 2-3 hrs to design

### Witchhunter Sample (KEPT) — "Complex Reference Implementation"
**Use when:**
- Need a comprehensive example
- Understanding multi-system integration
- Seeing how dialogue + quest + companion + faction systems work

**Scope:** 7+ nodes, 4+ NPCs, quest system, faction reputation, ~40 hrs to design

**Note:** Witchhunter is still useful as a reference, but it's NOT the recommended starting point. Start with Shrine, then graduate to Witchhunter patterns if needed.

---

## For Users

### If you were using the old preset (v0.1):

**Old focus:** "I want to design an RPG campaign"
→ **New approach:** Use the **RPG preset** (`game-rpg-narrative-writing`) instead, with caveats about scope

→ **New approach:** Use **narrative preset** with SugarCube export; then port to Escoria/Godot if needed

**Old focus:** "I want a tool to write branching stories"
→ **New approach:** ✅ **This is perfect for the new narrative preset!**

### If you're starting fresh:

1. **Start with Shrine sample** — Understand the workflow (2-3 hrs)
2. **Create your own narrative** — Plan → Outline → Implement → Export
3. **Test in browser** — Verify dialogue, choices, attributes work
4. **Optional:** Export specs to external engine or convert to Ink/Ren'Py

---

## Technical Details: What Exports to SugarCube

During `speckit export --engine sugarcube`, these become Twee (SugarCube) code:

| Mechanic | Twee Output |
|---|---|
| `[MECHANIC:ATTRIBUTE modify=wisdom delta=+1]` | `<<set $character.wisdom += 1>>` |
| `[MECHANIC:INVENTORY check=amulet]` | `<<if $inventory.amulet>>...{{</if>>` |
| Dialogue choice with gate | `[[Choice|NODE-X]] <!-- requires: wisdom >= 6 -->` |
| Character widget | Auto-generated from `character-profile-template.md` |

All exports go through `speckit.export`, preserving narrative specs while translating to engine syntax.

---

## Migration Path: From Old to New

If you have an existing narrative game using the old preset:

1. **Evaluate:** Do you actually need RPG mechanics?
   - Yes → Use `game-rpg-narrative-writing` preset
   - No → Migrate to new `game-narrative-writing` preset

2. **If migrating:**
   - Copy your narrative nodes to new preset
   - Update `constitution.md` with new mechanics selection
   - Create `character-profile.md` for player character
   - Simplify if you were using combat/loot/quest systems
   - Re-export to SugarCube

3. **Test:** Ensure dialogue branching, attributes, inventory all work in browser

---

## Summary: The Vision

**Spec Kit's Narrative Preset is now:**
- ✅ A tool for **story design validation** (structure, branching, consequences)
- ✅ A tool for **rapid prototyping** (test in browser in minutes)
- ✅ A tool for **narrative architecture** (machine-readable specs)
- ✅ NOT a game engine (that's what external tools like Godot/Unity are for)
- ✅ NOT game-specific (can export to Ink, Ren'Py, Yarn, custom engines)

**Core mechanics are narrative-only:**
- Character progression (attribute changes from choices)
- State validation (no narrative logical errors)

**This positions Spec Kit as:**
- The **design layer** (where stories are authored and validated)
- The **prototyping layer** (where stories are tested in SugarCube)
- NOT the implementation layer (that's external engines)

This separation of concerns makes Spec Kit more valuable: it's a **narrative design tool that outputs specs**, not a competing game engine.

---

## Questions?

See the README in `game-narrative-writing/` for:
- Quick start guide
- Shrine sample walkthrough
- How to create your own narrative
- Export and testing workflow
