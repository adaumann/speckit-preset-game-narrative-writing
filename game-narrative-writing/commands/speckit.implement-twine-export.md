# SugarCube/Twine Export Guidance for speckit.implement

When drafting narrative prose from approved outlines for SugarCube/Twine, the implementation process generates engine-agnostic markdown that gets exported to Twee (SugarCube format) during `speckit.export`.

## Workflow: Outline → Implement → Export

```
OUTLINE (structured metadata)
    ↓ [speckit.implement]
MARKDOWN NODE (prose + [MECHANIC:*] markup)
    ↓ [speckit.export --engine sugarcube]
TWEE FILE (.twee - SugarCube format)
    ↓ [speckit.compile]
PLAYABLE GAME (witchhunter.html)
```

---

## Prose Generation for SugarCube Export

When `speckit.implement` generates prose for a node, it produces markdown like this:

```markdown
---
node_id: NODE-002
title: Shrine Greeting
status: DRAFT
pov: second-person
variables_read: [$visited_shrine, $character.wisdom, $inventory.amulet]
variables_set: [$flags.priestess_spoken_to, $character.wisdom]
export_engines: [sugarcube, generic]
---

You push open the heavy wooden door of the shrine. Incense smoke curls through the shadows. At the altar, a priestess in gray robes looks up from her prayers, her eyes calm and knowing.

[MECHANIC:FLAG check=priestess_spoken_to]

<<if not $flags.priestess_spoken_to>>
  "Welcome, traveler," she says softly. "Few seek sanctuary these days."
  [MECHANIC:FLAG set=priestess_spoken_to value=true]
<<else>>
  "You return," she says, nodding in recognition. "I trust the outside world has not claimed you."
<</if>>

[MECHANIC:INVENTORY check=amulet]

<<if $inventory.amulet>>
  Her eyes linger briefly on the amulet at your chest, as if recognizing something in its weathered metal.
<</if>>

## Dialogue Options

[MECHANIC:ATTRIBUTE check=wisdom op=gte value=6]

**"I've noticed the amulet you wear. It's unusual."** 
<!-- requires: wisdom >= 6 | Effect: Priestess respects your insight; opens secret dialogue -->
```

When `speckit.export` processes this, it converts to Twee:

```twee
:: NODE-002 [act-I dialogue-heavy]
You push open the heavy wooden door of the shrine. Incense smoke curls through the shadows. At the altar, a priestess in gray robes looks up from her prayers, her eyes calm and knowing.

<<if not $flags.priestess_spoken_to>>
  "Welcome, traveler," she says softly. "Few seek sanctuary these days."
  <<set $flags.priestess_spoken_to to true>>
<<else>>
  "You return," she says, nodding in recognition. "I trust the outside world has not claimed you."
<</if>>

<<if $inventory.amulet>>
  Her eyes linger briefly on the amulet at your chest, as if recognizing something in its weathered metal.
<</if>>

## Dialogue Options

<<if $character.wisdom gte 6>>
  [[I've noticed the amulet you wear. It's unusual.|NODE-003]]
<</if>>
[[Can I find sanctuary here?|NODE-004]]
[[I'll be on my way|NODE-005]]
```

---

## Key Guidance for Implementation

### 1. **Use MECHANIC Blocks for Dynamic Logic**

Don't write SugarCube macros directly in your prose. Use markup:

✅ **DO:**
```markdown
[MECHANIC:FLAG check=priestess_likes_you]

<<if $flags.priestess_likes_you>>
  She smiles warmly at you.
<<else>>
  Her expression remains neutral.
<</if>>
```

❌ **DON'T:** (SugarCube syntax in the prose file)
```markdown
<<if $flags.priestess_likes_you>>
  She smiles warmly at you.
<<else>>
  Her expression remains neutral.
<</if>>
```

The markdown approach lets you maintain engine-agnostic prose. `speckit.export` converts the `[MECHANIC:*]` blocks to engine-specific syntax.

### 2. **Dialogue Choices as Prose Bullet Points**

Structure dialogue options clearly:

```markdown
## Dialogue Options

**"Ask about the amulet"**
<!-- requires: wisdom >= 6 | Effect: +wisdom, priestess_likes_you flag -->

**"Offer sanctuary in exchange for information"**
<!-- requires: gold >= 20 | Effect: -20 gold, opens secret dialogue -->

**"Politely excuse yourself"**
<!-- Effect: priestess_disappointed flag; colder future interactions -->
```

During export, these become linked choices. The `<!-- comment -->` provides metadata for branching.

### 3. **Attribute Changes Within Prose**

When a dialogue choice modifies attributes, mark it clearly:

```markdown
You think carefully about her words. The weight of insight settles on you.

[MECHANIC:ATTRIBUTE modify=wisdom delta=+1]
```

This auto-converts to:
```twee
<<set $character.wisdom += 1>>
<<run $ui.displayCharacterUpdate("wisdom", "+1")>>
```

### 4. **Inventory Checks and Updates**

```markdown
[MECHANIC:INVENTORY check=rusty_key]

<<if $inventory.rusty_key>>
  "That key," she whispers. "Where did you find it?"
<</if>>

[MECHANIC:INVENTORY add=amulet_of_protection]

She removes the amulet from around her neck and hands it to you.

<<set $inventory.amulet_of_protection to true>>
```

### 5. **Multiple NPCs in One Node**

When multiple NPCs are present, structure dialogue with character names:

```markdown
## Multi-NPC Dialogue

**Priestess:**
"You speak as one who understands the old ways."

**Henne (Guard):**
"Enough mysticism, priestess. We have a practical problem."

**Priestess:**
"Practical and spiritual are not opposites, guard. They are one."

**You can respond to:**
[[Side with the priestess|NODE-006]]
[[Support Henne's pragmatism|NODE-007]]
[[Suggest compromise|NODE-008]]
```

---

## Template: Node Implementation for SugarCube

```markdown
---
node_id: NODE-00X
title: [NODE_TITLE]
status: DRAFT
pov: second-person
act: I
variables_read: [$variable_1, $variable_2]
variables_set: [$variable_3, $variable_4]
export_engines: [sugarcube, generic]
---

# [NODE_TITLE]

[2-3 sentences of prose setting the scene]

[MECHANIC:FLAG check=any_conditional_flags]

<<if conditional_flag>>
  [Prose for conditional path]
  [MECHANIC:FLAG set=new_flag value=true]
<<else>>
  [Prose for default path]
<</if>>

[MECHANIC:INVENTORY check=key_item]

<<if $inventory.key_item>>
  [Prose acknowledging the item]
<</if>>

[Main prose paragraph or dialogue]

[MECHANIC:ATTRIBUTE check=relevant_attribute op=gte value=threshold]

## Dialogue Choices

[If dialogue-heavy: structure choices with character responses]

**"Choice A: [Player phrase]"**
<!-- requires: condition | Effect: consequence -->

**"Choice B: [Player phrase]"**
<!-- Effect: consequence -->

**"Choice C: [Player phrase]"**
<!-- Effect: consequence -->
```

---

## Compile & Test Cycle

After implementing nodes:

1. **Run export:**
   ```bash
   speckit export --engine sugarcube
   ```
   This generates `.twee` files in `export/sugarcube/`

2. **Compile to HTML:**
   ```bash
   speckit compile --engine sugarcube
   ```
   This produces `witchhunter.html` with all nodes linked together

3. **Test in browser:**
   - Open `witchhunter.html`
   - Verify prose renders correctly
   - Click dialogue choices; verify branching works
   - Check that attribute changes display in UI
   - Verify inventory changes persist

4. **Iterate:**
   - If dialogue needs adjusting, edit the markdown node file
   - Re-run `speckit export` + `speckit compile`
   - Refresh browser to test changes

---

## Common Pitfalls & Fixes

| Issue | Cause | Fix |
|---|---|---|
| Dialogue choice doesn't appear | Condition evaluates to false; gate not met | Check attribute value in game UI; verify condition syntax |
| Attribute doesn't change | Missing `[MECHANIC:ATTRIBUTE modify=...]` block | Add markup before export; re-export |
| Inventory item missing | Forgot to add via `[MECHANIC:INVENTORY add=...]` | Add block to prose; re-export; re-compile |
| NPC dialogue wrong tone | Prose_profile not matching character voice | Review `character-profile-template.md`; adjust prose tone; re-export |
| Choice leads to wrong node | Node ID typo in outline or prose comment | Verify `outlines/NODE-XXX.md` targets; check comment metadata |

---

## Next: Export & Compile

Once all nodes are implemented and tested:

```bash
speckit export --engine sugarcube --all    # Generate all .twee files
speckit compile --engine sugarcube         # Compile to playable HTML
speckit verify --engine sugarcube          # Run validation checks
```

Then share `witchhunter.html` with testers or stakeholders.
