# SugarCube/Twine Export Guidance for speckit.outline

When `export_engines` includes `sugarcube` in your constitution.md, the outline generation process includes special considerations for Twee (Twine) compilation.

## What Gets Exported to SugarCube

From your narrative outline, `speckit.implement` will generate `.twee` passage files for SugarCube that include:

### 1. **Passage Header**
```twee
:: NODE-001 [tags]
```
- Tags include: `act-I`, `dialogue-heavy`, `choice-point`, etc.
- Generated automatically from outline metadata

### 2. **Prose + Mechanics Inline**
```twee
:: NODE-001 [dialogue-heavy]
You enter the shrine. [MECHANIC:FLAG check=priestess_spoken_to]

<<if $visited_shrine>>
  The priestess nods in recognition.
<<else>>
  [MECHANIC:FLAG set=visited_shrine value=true]
  The priestess looks up from her prayers.
<</if>>

[MECHANIC:INVENTORY check=amulet]
<<if $inventory.amulet>>
  She eyes the amulet with interest.
<</if>>

[[Continue|NODE-002]]
```

Mechanics markup is embedded in your prose and auto-converted to SugarCube macros during `speckit.export`.

### 3. **Dialogue Choice Structure**
```twee
[[Option 1: Ask about the amulet|NODE-003]] <!-- requires: $character.wisdom gte 6 -->
[[Option 2: Leave politely|NODE-005]]
```

Conditional choices (with attribute gates) include comment hints that `speckit.export` parses.

### 4. **Character Profile Widget**
When `attribute` mechanics are enabled, the Character Profile widget displays:
- Current attribute values (intelligence, wisdom, power, gold)
- Changes from last choice ("Wisdom +2 (asked thoughtful question)")
- Inventory count

Auto-generated from character-profile-template.md.

---

## What Happens During Export

When you run `speckit.export --engine sugarcube`:

1. **Parse mechanics markup** → Convert `[MECHANIC:*]` blocks to `<<set>>`, `<<if>>` macros
2. **Resolve variable names** → Map to `$character.`, `$inventory.`, `$flags.` namespaces
3. **Generate Twee file** → One `.twee` file per node (or combined if configured)
4. **Compile with Tweego** → Produce playable `witchhunter.html` with UI widgets

---

## Outline Considerations for SugarCube Export

When outlining a narrative for Twine/SugarCube export, keep these in mind:

### ✅ DO

- **Use simple, linear dialogue** — SugarCube handles branching well; avoid deeply nested conditions
- **Keep choice gates to 1-2 attributes max** — e.g., `requires: wisdom >= 6` works; `requires: (wisdom >= 6 AND power <= 4 AND NOT flag_x)` gets hard to read
- **Use inventory checks sparingly** — Each check adds UI complexity in SugarCube
- **Group related choices together** — SugarCube renders best with 2-4 choices per node
- **Document attribute changes clearly** — Outline should show `+1 wisdom`, `-5 gold`, etc.

### ❌ DON'T

- **Use attribute ranges that change mid-conversation** — SugarCube doesn't support dynamic range recalculation
- **Create more than 1 level of dialogue nesting** — Twee doesn't handle complex nested dialogue trees well
- **Use variables with spaces or special characters** — Stick to `snake_case` (e.g., `priestess_spoken_to`)
- **Gate choices on more than 2 unrelated variables** — Player can't mentally track complex multi-variable gates

---

## Example Outline for Twine Export

```markdown
---
node_id: NODE-002
title: Shrine Greeting
status: DRAFT
pov: second-person
---

## Beat Summary
The priestess greets you. You can ask about the amulet (if wise enough), inquire about sanctuary, or leave. Your dialogue choice affects her disposition and unlocks later dialogue paths.

## Variables Read
| Variable | Expected Value | Source |
|---|---|---|
| `$visited_shrine` | true or false | NODE-001 |
| `$character.wisdom` | 1-10 | character profile |
| `$inventory.amulet` | true or false | NODE-001 or earlier |

## Variables Set
| Variable | Hook Type | Action | Trigger |
|---|---|---|---|
| `$flags.priestess_spoken_to` | flag | set to true | any dialogue choice |
| `$character.wisdom` | attribute | +1 if wisdom choice selected | wisdom dialogue choice |
| `$character.gold` | attribute | -10 if bribe offered | specific dialogue branch |

## Choices
| Label | Condition | Target Node | Narrative Consequence |
|---|---|---|---|
| "What is that amulet?" | `$character.wisdom >= 6` | NODE-003 | Priestess respects your insight; opens secret dialogue |
| "Can I find sanctuary here?" | None | NODE-004 | Safe haven; affects later faction standing |
| "I'll be on my way" | None | NODE-005 | Priestess disappointed; future dialogue colder |

## Dialogue Tree
**NPC: Priestess (dialogue-heavy)**

```
Priestess: "Welcome, traveler. The shrine is sanctuary for those who seek it."

> CHOICE A: "What is that amulet?" [requires: wisdom >= 6]
  Priestess: "Ah, you have a discerning eye. Few notice such things."
  [MECHANIC:ATTRIBUTE modify=wisdom delta=+1]
  [MECHANIC:FLAG set=priestess_likes_you value=true]
  → NODE-003

> CHOICE B: "Can I find sanctuary here?"
  Priestess: "Of course. You are safe within these walls."
  [MECHANIC:FLAG set=shrine_sanctuary_granted value=true]
  → NODE-004

> CHOICE C: "I'll be on my way"
  Priestess: "As you wish. Safe travels." (coldly)
  → NODE-005
```

## Mechanic Hooks Summary
- ✓ VISITED: Already set in NODE-001
- ✓ FLAG: Set `priestess_spoken_to` on any dialogue choice
- ✓ ATTRIBUTE: Wisdom +1 for thoughtful dialogue
- ✓ INVENTORY: Check for amulet (optional reaction)
- ✓ DIALOGUE_BRANCH: Three paths with different NPC responses

## Export Notes for SugarCube
- Dialogue choices should render as 3 clickable links
- Priestess portrait widget can display (if art asset provided)
- Wisdom +1 notification should appear in character profile widget
- No inventory UI needed (only a check, no change)
```

---

## Next Steps

1. **Author reviews & approves** this outline
2. **Set status to `APPROVED`**
3. **Run `speckit.implement NODE-002`** → Generates `nodes/NODE-002.md` with full prose
4. **Run `speckit.export --engine sugarcube`** → Converts to `.twee` and compiles to HTML
5. **Test in browser** → Open `witchhunter.html`, verify dialogue choices work, attributes update
