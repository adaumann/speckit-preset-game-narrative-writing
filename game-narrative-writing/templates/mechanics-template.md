# Mechanic Hook Schemas: [GAME_TITLE]

<!-- Reference document for all mechanic hooks used in this project.
     Cross-referenced by speckit.implement, speckit.outline, speckit.checklist, and export.py.
     Only hooks declared as enabled in constitution.md Section II are active.
     
     NARRATIVE DESIGN FOCUS: These mechanics enable dialogue branching, state tracking,
     and outcome validation. All export to SugarCube for rapid prototyping and testing.
-->

---

## Core Mechanics — Exported to SugarCube

### flag — Boolean State

`
[MECHANIC:FLAG set=[variable_name] value=true|false]
[MECHANIC:FLAG check=[variable_name]]
[conditional prose]
[/MECHANIC]
`

| Parameter | SugarCube Export |
|---|---|
| set=true | <<set $[var] to true>> |
| set=false | <<set $[var] to false>> |
| check (true) | <<if $[var]>>...<</if>> |
| check (false) | <<if not $[var]>>...<</if>> |

**Use case:** Quest completed, dialogue seen, puzzle solved, area unlocked

---

### counter — Integer Increment/Decrement

`
[MECHANIC:COUNTER set=[variable_name] delta=+1|-1|N]
[MECHANIC:COUNTER check=[variable_name] op=gte|lte|eq value=N]
[conditional prose]
[/MECHANIC]
`

| Parameter | SugarCube Export |
|---|---|
| delta=+1 | <<set $[var] += 1>> |
| delta=-1 | <<set $[var] -= 1>> |
| delta=N | <<set $[var] += N>> |
| check gte N | <<if $[var] gte N>>...<</if>> |
| check lte N | <<if $[var] lte N>>...<</if>> |
| check eq N | <<if $[var] is N>>...<</if>> |

**Use case:** Loyalty points, days elapsed, encounter count, player reputation with faction

---

### visited — Node Seen Tracking

`
[MECHANIC:VISITED set=[variable_name]]
[MECHANIC:VISITED check=[variable_name]]
[prose shown only on first visit]
[/MECHANIC]
`

| Parameter | SugarCube Export |
|---|---|
| set | <<set $[var] to true>> |
| check (first visit) | <<if not $[var]>>...<</if>> |
| check (revisit) | <<if $[var]>>...<</if>> |

**Use case:** Tutorial text on first playthrough, NPC intro dialogue, location description variations

---

### inventory — Item Management (Widget)

`
[MECHANIC:INVENTORY add=[item_variable]]
[prose describing item acquisition]
[/MECHANIC]

[MECHANIC:INVENTORY remove=[item_variable]]

[MECHANIC:INVENTORY check=[item_variable]]
[prose shown when item is present]
[/MECHANIC]
`

| Parameter | SugarCube Export |
|---|---|
| add | <<set $inventory.[item] to true>> |
| remove | <<set $inventory.[item] to false>> |
| check present | <<if $inventory.[item]>>...<</if>> |
| check absent | <<if not $inventory.[item]>>...<</if>> |

**Use case:** Key items gating dialogue, tools enabling puzzle solutions, collectibles for endings

**Widget:** Inventory display widget shows all items with descriptions (defined in character profile)

---

## Tier 3 Hooks — Point-and-Click / High-Fidelity

### move — Actor Navigation

| Engine | Syntax |
|---|---|
| Escoria | :walk [actor] [target] |
| AGS | c[Actor].Walk([x], [y]); |
| Unity | character.MoveTo(\"[target]\"); |

---

### udio — Sound Triggers

| Engine | Syntax |
|---|---|
| Escoria | snd_play [file] |
| Ren'Py | play sound \"[file]\" |
| Sugarcube | <<audio \"[file]\" play>> |

---

### attribute — Player Stats / Character Traits

`
[MECHANIC:ATTRIBUTE modify=[attribute] delta=+1|-1|N]
[MECHANIC:ATTRIBUTE check=[attribute] op=gte|lte|eq value=N]
[conditional prose]
[/MECHANIC]
`

| Parameter | SugarCube Export |
|---|---|
| modify +N | <<set $character.[attr] += N>> |
| modify -N | <<set $character.[attr] -= N>> |
| check gte N | <<if $character.[attr] gte N>>...<</if>> |
| check lte N | <<if $character.[attr] lte N>>...<</if>> |
| check eq N | <<if $character.[attr] eq N>>...<</if>> |

**Predefined attributes:**
- `intelligence` — Affects logical/puzzle dialogue choices
- `wisdom` — Affects moral/spiritual dialogue choices
- `power` — Affects combat/intimidation outcomes
- `gold` — Currency; gating purchases or bribes
- `custom: [user-defined]` — Define in character profile

**Use case:** Gate dialogue choices by minimum stat, modify outcome probability, track character growth

**Widget:** Character Profile widget displays current attributes and changes per dialogue choice

---

## Generic/Markdown Annotations

When using generic export or documentation, all hooks are written as:
```
[MECHANIC:TYPE parameter=value]
conditional prose
[/MECHANIC]
```
or inline:
```
[MECHANIC:TYPE parameter=value] (inline)
```
