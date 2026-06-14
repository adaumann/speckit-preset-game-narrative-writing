# Shrine Sample: Simplified Widget Pattern

This guide documents the **minimal widget pattern** for narrative-focused design in the Shrine sample.

## Design Philosophy

The Shrine sample uses a **read-only character profile** and **minimal inventory** system. No character stat modifications, no combat mechanics—only narrative choices that gate dialogue based on attributes.

## Widget Reference

### Character Profile (Display Only)

**`<<charProfile>>`**
- Displays character sheet with all attributes
- Read-only; attributes only change through dialogue choices
- Usage:
  ```twee
  <<charProfile>>
  ```

**`<<charAttr "attr_name">>`**
- Display single attribute value inline
- Usage:
  ```twee
  You sense <<charAttr "wisdom">> points of wisdom in her gaze.
  ```

### Inventory System

**`<<pickupItem "item_key" "Display Name">>`**
- Add item to inventory (or increment qty if exists)
- Shows pickup message
- Usage:
  ```twee
  <<pickupItem "old_book" "Old Book">>
  ```

**`<<hasItem "item_key">>`**
- Check if inventory contains item
- Sets `_hasItem` variable (true/false)
- Use in conditionals
- Usage:
  ```twee
  <<hasItem "old_book">>
  <<if _hasItem>>
    You remember the old book you found.
  <</if>>
  ```

**`<<inventory>>`**
- Display full inventory list
- Shows item count
- Typically shown on dedicated UI passage
- Usage:
  ```twee
  << link "🎒 Inventory" "InventoryUI">><</link>>
  
  :: InventoryUI
  <<inventory>>
  ```

**`<<hasItemCheck "item_key" "Link Text" "Target Passage">>`**
- Convenience widget: show optional link only if player has item
- Usage:
  ```twee
  <<hasItemCheck "old_book" "Read the grimoire" "ReadGrimoire">>
  ```

### Quest System (Optional)

**`<<questList>>`**
- Display all quests grouped by status: Active, Completed, Failed
- Shows quest name and current stage for active quests
- Typically shown on dedicated QuestUI passage
- Usage:
  ```twee
  :: QuestUI
  <h2>Quests</h2>
  <<questList>>
  ```

**`<<questProgress "quest_id">>`**
- Show current status and stage of a single quest
- Displays: "📍 Stage 2 (In Progress)" or "✅ Completed" or "❌ Failed"
- Usage in prose:
  ```twee
  Your progress: <<questProgress "quest_shrine_blessing">>
  ```

**`<<advanceQuestStage "quest_id">>`**
- Increment quest to next stage
- Use when completing a stage
- Usage:
  ```twee
  [MECHANIC:QUEST advance=quest_shrine_blessing]
  <<advanceQuestStage "quest_shrine_blessing">>
  The priestess guides you forward. Stage complete.
  ```

**`<<completeQuest "quest_id">>`**
- Mark quest as complete (status = "completed")
- Shows completion message
- Usage:
  ```twee
  [MECHANIC:QUEST complete=quest_shrine_blessing]
  <<completeQuest "quest_shrine_blessing">>
  ```

**`<<failQuest "quest_id">>`**
- Mark quest as failed (status = "failed")
- Shows failure message
- Usage:
  ```twee
  [MECHANIC:QUEST fail=quest_shrine_blessing]
  <<failQuest "quest_shrine_blessing">>
  ```

## Data Structures

### Character Object
```javascript
$character = {
  name: "The Wanderer",
  intelligence: 5,    // 1-10 scale
  wisdom: 6,          // 1-10 scale
  power: 4,           // 1-10 scale
  gold: 10            // currency
}
```

Only **narrative choices** modify these attributes—never widget calls. Example:

```twee
<<if $character.intelligence gte 6>>
  You recognize the architectural style.
  <<set $character.wisdom += 1>>
<</if>>
```

### Inventory Array
```javascript
$inventory = [
  {item: "old_book", name: "Old Book", qty: 1},
  {item: "coin", name: "Bronze Coin", qty: 3}
]
```

### Quest Tracking Variables

If using the optional quest system:

```javascript
/* Quest status (per quest) */
$quest_shrine_blessing_status = "active" | "completed" | "failed"
$quest_shrine_blessing_stage = 1  /* Current stage (integer) */

/* Multiple quests tracking */
$quest_guild_contract_status = "active"
$quest_guild_contract_stage = 2

$quest_tavern_revenge_status = "completed"
```

**Quest Status Values**:
- `"active"` — Quest in progress, currently available
- `"completed"` — Quest finished successfully
- `"failed"` — Quest failed (if `failed_quests: true` in constitution)
- `"inactive"` — Quest not yet started

**Naming Convention**: `$quest_[location]_[quest_id]_[property]`

## Common Patterns

### Gating Dialogue by Attribute

```twee
<<if $character.intelligence gte 6>>
  [Smart response]
<<else>>
  [Less informed response]
<</if>>
```

### Conditional Inventory Checks

```twee
<<hasItem "old_book">>
<<if _hasItem>>
  <<link "Consult the grimoire" "GrimoireScene">>
<</if>>
```

### Attribute Changes Through Choice

```twee
[[Help the priestess|HelpPriestess]]

:: HelpPriestess
You assist her with the shrine's repairs.

<<set $character.wisdom = Math.min($character.wisdom + 1, 10)>>
<<set $character.power = Math.max($character.power - 1, 1)>>

You feel wiser but wearier.

[[Continue|Start]]
```

### Quest Tracking (Optional)

If using the quest system (optional feature):

```twee
/* Display all quests organized by status */
<<questList>>

/* Show status of a single quest */
<<questProgress "quest_shrine_blessing">>

/* Advance quest to next stage */
[MECHANIC:QUEST advance=quest_shrine_blessing]
<<advanceQuestStage "quest_shrine_blessing">>

/* Complete a quest */
[MECHANIC:QUEST complete=quest_shrine_blessing]
<<completeQuest "quest_shrine_blessing">>

/* Fail a quest (if failed_quests enabled) */
[MECHANIC:QUEST fail=quest_shrine_blessing]
<<failQuest "quest_shrine_blessing">>
```

## Export Checklist

When exporting this pattern to SugarCube:

- ✅ All `<<charProfile>>` calls render character stats
- ✅ All `<<pickupItem>>` calls add items to $inventory array
- ✅ All `<<hasItem>>` checks work in conditionals
- ✅ All `<<if $character.attr gte N>>` gates work correctly
- ✅ Attributes update only through `<<set>>`, not widget calls
- ✅ No widget modifies character stats directly
- ✅ (Optional) All `<<questList>>` calls show quest state correctly
- ✅ (Optional) All `<<completeQuest>>` and `<<failQuest>>` calls update quest status
- ✅ (Optional) Quest stages track via `$quest_[id]_stage` and `$quest_[id]_status`

## Comparison to Witchhunter Sample

| Feature | Shrine (Simple) | Witchhunter (RPG) |
|---------|-----------------|------------------|
| Character Stats | 4 (INT, WIS, PWR, GLD) | 6 (D&D 5e abilities) |
| Inventory | View/Pickup/Check | View/Pickup/Drop/Equip |
| Combat | None | Skill checks, saving throws |
| Quests | None | Full quest system |
| Companions | None | Full companion system |
| Factions | None | Reputation system |
| Complexity | ~2-3 hours design | 40+ hours design |

## Next Steps

To extend the Shrine pattern:

1. Add more dialogue passages with attribute checks
2. Expand inventory (add more item pickup points)
3. Add flags for dialogue branching (e.g., `$spoke_priestess`)
4. Implement simple consequences (attribute changes based on choices)
5. Create multiple NPCs with different dialogue trees

Keep widgets **read-only for character** and **minimal for inventory**. The narrative is in the passage text, not the mechanics.
