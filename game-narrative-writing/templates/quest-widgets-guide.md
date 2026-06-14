# Quest Widgets for SugarCube — Implementation Guide

This guide explains how to implement quest tracking and display widgets in SugarCube/Twine for narrative-focused games.

## Overview

Quest widgets provide a simplified but complete quest tracking system for games using the speckit narrative design tool. They allow designers to:

- Track quest progress (stages: 1, 2, 3, etc.)
- Track quest status (active, completed, failed)
- Display quests organized by status to players
- Advance quests through story choices
- Mark quests complete or failed based on narrative outcomes

**Philosophy**: Quests are narrative structure, not game mechanics. They organize where and when scenes occur, helping players understand progress through multi-stage objectives.

---

## Core Widgets

### 1. `<<questList>>`

**Purpose**: Display all quests organized by status (Active, Completed, Failed)

**Output**: 
- List grouped by status
- Shows quest name and current stage for active quests
- Uses emoji indicators (📋 active, ✅ completed, ❌ failed)

**Usage**:
```twee
:: QuestUI
<h2>Quest Log</h2>
<<questList>>
<<link "Back" previous()>><</link>>
```

**Result**:
```
📋 Active Quests (1)
  SEEKING THE BLESSING — Stage 2

✅ Completed Quests (0)
  (none)

❌ Failed Quests (0)
  (none)
```

---

### 2. `<<questProgress "quest_id">>`

**Purpose**: Display current progress of a single quest inline in prose

**Parameters**:
- `quest_id` — Quest identifier (e.g., "quest_shrine_blessing")

**Output**: 
- Status indicator with stage (if active)
- One-line format: "📍 Stage 2 (In Progress)" or "✅ Completed" or "❌ Failed"

**Usage**:
```twee
You have made significant progress on your quest.

<<questProgress "quest_shrine_blessing">>

The priestess seems to recognize your advancement.
```

**Result**:
```
You have made significant progress on your quest.

📍 Stage 2 (In Progress)

The priestess seems to recognize your advancement.
```

---

### 3. `<<advanceQuestStage "quest_id">>`

**Purpose**: Increment quest to next stage

**Parameters**:
- `quest_id` — Quest identifier

**Effect**: 
- Increases `$quest_[id]_stage` by 1
- Silent (no message)

**Usage**:
```twee
The priestess guides you forward in your spiritual journey.

[MECHANIC:QUEST advance=quest_shrine_blessing]
<<advanceQuestStage "quest_shrine_blessing">>

You feel yourself progressing toward a deeper understanding.
```

---

### 4. `<<completeQuest "quest_id">>`

**Purpose**: Mark a quest as completed

**Parameters**:
- `quest_id` — Quest identifier

**Effect**: 
- Sets `$quest_[id]_status` to "completed"
- Displays completion message

**Usage**:
```twee
The priestess places her hand on your forehead.

[MECHANIC:QUEST complete=quest_shrine_blessing]
<<completeQuest "quest_shrine_blessing">>

Your quest for the blessing is complete.
```

**Result**:
```
✅ SEEKING THE BLESSING quest completed!

Your quest for the blessing is complete.
```

---

### 5. `<<failQuest "quest_id">>`

**Purpose**: Mark a quest as failed (only if `failed_quests: true` in constitution)

**Parameters**:
- `quest_id` — Quest identifier

**Effect**: 
- Sets `$quest_[id]_status` to "failed"
- Displays failure message

**Usage**:
```twee
The priestess shakes her head sadly.

[MECHANIC:QUEST fail=quest_shrine_blessing]
<<failQuest "quest_shrine_blessing">>

You have lost her trust. The blessing is beyond your reach.
```

**Result**:
```
❌ SEEKING THE BLESSING quest failed.

You have lost her trust. The blessing is beyond your reach.
```

---

## Data Structure

### Quest Tracking Variables

Each quest is tracked with **two variables**:

```javascript
$quest_[location]_[quest_id]_status  // "active" | "completed" | "failed" | "inactive"
$quest_[location]_[quest_id]_stage   // Integer (current stage number)
```

**Example**:
```javascript
$quest_shrine_blessing_status = "active"
$quest_shrine_blessing_stage = 1

$quest_guild_contract_status = "completed"
$quest_guild_contract_stage = 3

$quest_tavern_revenge_status = "failed"
```

### Status Values

| Status | Meaning | Widget Display |
|---|---|---|
| `"active"` | Quest in progress | 📍 Stage N (In Progress) |
| `"completed"` | Quest finished successfully | ✅ Completed |
| `"failed"` | Quest failed (optional) | ❌ Failed |
| `"inactive"` | Quest not started | ◯ Not started |

### Naming Convention

```
$quest_[location]_[quest_id]_status
        └─ shrine        └─ blessing  └─ status
```

**Examples**:
- `$quest_shrine_blessing_status` — Shrine location, blessing quest
- `$quest_guild_contract_status` — Guild location, contract quest
- `$quest_tavern_revenge_status` — Tavern location, revenge quest

---

## Common Patterns

### Initialize Quest at Story Start

```twee
:: StoryInit

/* Quest initialization */
<<set $quest_shrine_blessing_status to "active">>
<<set $quest_shrine_blessing_stage to 1>>

<<set $quest_guild_contract_status to "inactive">>
<<set $quest_guild_contract_stage to 0>>
```

### Display Quest in UI Menu

```twee
:: StoryMenu
<<link "📋 Character" "CharacterSheet">><</link>>
<<link "🎒 Inventory" "InventoryUI">><</link>>
<<link "📜 Quests" "QuestUI">><</link>>
<<link "🏠 Home" "Start">><</link>>

:: QuestUI
<h2>Quest Log</h2>
<<questList>>
<<link "Back" previous()>><</link>>
```

### Gate Dialogue on Quest Stage

```twee
:: MeetPriestess
The priestess regards you with interest.

<<if $quest_shrine_blessing_stage === 1>>
  "You are new to seeking the blessing. Let me guide you."
<<elseif $quest_shrine_blessing_stage === 2>>
  "Your progress is notable. You grow in understanding."
<<elseif $quest_shrine_blessing_stage === 3>>
  "You are ready for the final revelation."
<</if>>

[[Continue|Next]]
```

### Multi-Stage Quest with Consequences

```twee
:: QuestChoice1
"Will you seek knowledge or demonstrate charity?" asks the priestess.

[[Ask about her history|KnowledgePath]]
[[Make a generous donation|CharityPath]]

:: KnowledgePath
You learn much from the priestess about the shrine's ancient origins.
<<set $character.intelligence += 1>>

[MECHANIC:QUEST advance=quest_shrine_blessing]
<<advanceQuestStage "quest_shrine_blessing">>

[[Continue|QuestChoice2]]

:: CharityPath
Your donation deeply moves the priestess.
<<set $character.wisdom += 2>>

[MECHANIC:QUEST advance=quest_shrine_blessing]
<<advanceQuestStage "quest_shrine_blessing">>

[[Continue|QuestChoice2]]

:: QuestChoice2
Both paths have revealed your character to the priestess.

<<questProgress "quest_shrine_blessing">>

[[Accept her blessing|BlessingEnding]]
[[Leave without the blessing|DepartEnding]]

:: BlessingEnding
[MECHANIC:QUEST complete=quest_shrine_blessing]
<<completeQuest "quest_shrine_blessing">>

The priestess grants you her blessing. Your wisdom is honored.

[[End|End]]

:: DepartEnding
[MECHANIC:QUEST complete=quest_shrine_blessing]
<<completeQuest "quest_shrine_blessing">>

You leave respectfully. The priestess nods in acknowledgment.

[[End|End]]
```

### Quest with Optional Failure Path

```twee
:: CriticalChoice
The priestess awaits your answer. Choose carefully.

[[Lie to her|LiePath]]
[[Tell the truth|TruthPath]]

:: LiePath
The priestess sees through your deception. Her expression hardens.

[MECHANIC:QUEST fail=quest_shrine_blessing]
<<failQuest "quest_shrine_blessing">>

You have lost her trust forever. The blessing is now impossible.

[[Leave in shame|BadEnding]]

:: TruthPath
The priestess appreciates your honesty.

[MECHANIC:QUEST advance=quest_shrine_blessing]
<<advanceQuestStage "quest_shrine_blessing">>

[[Continue|GoodEnding]]
```

---

## Integration with Attributes

Quest advancement often tied to character attributes:

```twee
:: QuestChoice
The priestess tests your resolve.

<<if $character.wisdom gte 6>>
  [[Demonstrate spiritual wisdom|WisdomPath]]
<</if>>

<<if $character.intelligence gte 6>>
  [[Show intellectual understanding|IntelligencePath]]
<</if>>

[[Walk away unchanged|DefaultPath]]

:: WisdomPath
Your spiritual maturity impresses her.
<<set $character.wisdom += 1>>
<<advanceQuestStage "quest_shrine_blessing">>
[[Continue|Next]]

:: IntelligencePath
Your keen insight surprises her.
<<set $character.intelligence += 1>>
<<advanceQuestStage "quest_shrine_blessing">>
[[Continue|Next]]

:: DefaultPath
You leave without further interaction.
[[Continue|Next]]
```

---

## CSS Styling (Optional)

Add to your `StoryStylesheet` for visual quest indicators:

```css
.quest-progress {
  display: inline-block;
  padding: 0.4em 0.6em;
  background: #444;
  border-radius: 3px;
  font-size: 0.9em;
  color: #b8b8b8;
  margin: 0.5em 0;
}

.quest-progress.completed {
  color: #4a9d5f;
}

.quest-progress.failed {
  color: #d64545;
}

.quest-item.active {
  border-left: 3px solid #7fb854;
  padding-left: 0.7em;
}

.quest-item.completed {
  border-left: 3px solid #4a9d5f;
  text-decoration: line-through;
  opacity: 0.8;
}

.quest-item.failed {
  border-left: 3px solid #d64545;
  opacity: 0.7;
}
```

---

## Design Considerations

### Keep Quests Simple

- Limit to 3–5 stages per quest
- Avoid excessive branching within quests
- Use quests to organize location-based narrative, not replace story structure

### Use Quests for Narrative Clarity

- Show players where they stand in a multi-stage objective
- Help designers track what stage each passage belongs to
- Enable location revisits with conditional content

### Multiple Quests

If running multiple quests simultaneously:

```twee
:: QuestUI
<h2>Active Quests</h2>
<<questProgress "quest_shrine_blessing">>
<<questProgress "quest_guild_contract">>
<<questProgress "quest_tavern_revenge">>
```

All quests display independently, making it clear which stages are active.

---

## Troubleshooting

**Q: Quest displays as "inactive" but I set it to "active"?**

A: Ensure you initialized it in `StoryInit`:
```twee
<<set $quest_shrine_blessing_status to "active">>
```

**Q: Advanced quest but stage didn't increase?**

A: Check that the quest exists first:
```twee
<<if $quest_shrine_blessing_status !== undefined>>
  <<advanceQuestStage "quest_shrine_blessing">>
<</if>>
```

**Q: Multiple quests getting tangled?**

A: Use clear naming: `$quest_[LOCATION]_[QUEST_ID]_status`. This keeps quest variables organized by location.

**Q: Want to reset a quest?**

A: Just re-initialize it:
```twee
<<set $quest_shrine_blessing_status to "active">>
<<set $quest_shrine_blessing_stage to 1>>
```

---

## Next Steps

1. **Copy widgets** from `shrine-widgets.twee` into your project
2. **Initialize quests** in StoryInit with appropriate starting values
3. **Add QuestUI passage** to display quest list
4. **Use `<<advanceQuestStage>>`, `<<completeQuest>>`, etc.** in your narrative passages
5. **Test** with `<<questProgress>>` to verify stage advancement

For full working example, see the Shrine sample: `shrine-widgets.twee`, `shrine-init.twee`, `shrine-ui.twee`.
