# Variable Registry: [GAME_TITLE]

<!-- All state variables used in this project.
     Every variable referenced in a node [MECHANIC:*] hook MUST be declared here.
     speckit.checklist and speckit.continuity validate against this registry. -->

---

## Registry Format

Each entry:
- **Variable name**: exact name used in hook blocks and export output
- **Type**: hook type category
- **Scope**: `global` (persists across saves) | `session` (resets on load) | `branch` (reset when branch rejoins)
- **Default**: initial value at game start
- **Export name**: name used in engine output (Sugarcube: `$name`, Ink: `~ name`)
- **Set in**: node IDs where this variable is first/primarily set
- **Read in**: node IDs where this variable gates content or choices

---

## Character Sheet

<!-- Core player character stats consumed by sugarcube-d5e-combat.js and MECHANIC:CHARSHEET.
     CRITICAL: these variable names are hardcoded in the combat engine — do not rename them.
     Set defaults from class/race/starting equipment during campaign constitution phase.
     Ability modifier formula: floor((score - 10) / 2)
     Proficiency bonus formula: ceil(partyLevel / 4) + 1  -->

### Identity

| Variable | Type | Scope | Default | Description | Export (SC) |
|---|---|---|---|---|---|
| playerName | string | global | "[CHARACTER_NAME]" | Player character name | `$playerName` |
| playerClass | string | global | "[CLASS]" | Character class (Fighter, Wizard, Rogue…) | `$playerClass` |
| playerRace | string | global | "[RACE]" | Character race | `$playerRace` |
| playerBackground | string | global | "[BACKGROUND]" | Character background | `$playerBackground` |
| playerAlignment | string | global | "[ALIGNMENT]" | Alignment (optional — omit if not used) | `$playerAlignment` |

### Level & Experience

| Variable | Type | Scope | Default | Range | Description | Export (SC) |
|---|---|---|---|---|---|---|
| partyLevel | counter | global | 1 | 1–20 | Current character level — read by combat engine | `$partyLevel` |
| playerXP | counter | global | 0 | 0–355000 | Total XP accumulated | `$playerXP` |
| xpThreshold | counter | global | 300 | — | XP needed for next level (set on levelup) | `$xpThreshold` |
| playerProfBonus | counter | global | 2 | 2–6 | Proficiency bonus — auto-computed from partyLevel | `$playerProfBonus` |

### Hit Points

| Variable | Type | Scope | Default | Range | Description | Export (SC) |
|---|---|---|---|---|---|---|
| partyCurrentHP | counter | global | [MAX] | 0–partyMaxHP | Current HP — read and written by combat engine | `$partyCurrentHP` |
| partyMaxHP | counter | global | [MAX] | 1–∞ | Maximum HP | `$partyMaxHP` |
| playerHitDie | string | global | "d8" | d6/d8/d10/d12 | Hit die type for short rest recovery | `$playerHitDie` |
| playerHitDiceRemaining | counter | global | [partyLevel] | 0–partyLevel | Hit dice remaining for short rests | `$playerHitDiceRemaining` |

### Ability Scores & Modifiers

<!-- Modifier variables must be kept in sync with score variables.
     The combat engine reads modifiers (playerStrMod etc.), not raw scores.
     <<setAbility>> widget recalculates modifiers automatically.
     Default values below are for a Fighter at level 1; adjust per constitution.md. -->

| Score Variable | Mod Variable | Default Score | Default Mod | Description | Export (SC — score) | Export (SC — mod) |
|---|---|---|---|---|---|---|
| playerSTR | playerStrMod | 16 | +3 | Strength | `$playerSTR` | `$playerStrMod` |
| playerDEX | playerDexMod | 13 | +1 | Dexterity | `$playerDEX` | `$playerDexMod` |
| playerCON | playerConMod | 14 | +2 | Constitution | `$playerCON` | `$playerConMod` |
| playerINT | playerIntMod | 10 | 0 | Intelligence | `$playerINT` | `$playerIntMod` |
| playerWIS | playerWisMod | 12 | +1 | Wisdom | `$playerWIS` | `$playerWisMod` |
| playerCHA | playerChaMod | 10 | 0 | Charisma | `$playerCHA` | `$playerChaMod` |

### Saving Throw Proficiencies

     Proficient saves: class-specific; set from constitution.md. -->

| Variable | Type | Default | Description | Export (SC) |
|---|---|---|---|---|
| playerProfSaveStr | flag | false | Proficient in STR saves | `$playerProfSaveStr` |
| playerProfSaveDex | flag | false | Proficient in DEX saves | `$playerProfSaveDex` |
| playerProfSaveCon | flag | false | Proficient in CON saves | `$playerProfSaveCon` |
| playerProfSaveInt | flag | false | Proficient in INT saves | `$playerProfSaveInt` |
| playerProfSaveWis | flag | false | Proficient in WIS saves | `$playerProfSaveWis` |
| playerProfSaveCha | flag | false | Proficient in CHA saves | `$playerProfSaveCha` |

### Combat Stats (Derived)

<!-- Computed from ability scores + equipment. Updated by <<setAbility>>, <<equipWeapon>>, <<equipArmor>>.
     The combat engine reads partyAC, partyWeaponDmg — keep these in sync. -->

| Variable | Type | Default | Description | Export (SC) |
|---|---|---|---|---|
| partyAC | counter | global | 13 | Total AC (base + armor + shield + DEX cap) — read by combat engine | `$partyAC` |
| partyWeaponDmg | string | global | "1d8+3" | Damage expression for primary weapon — read by combat engine | `$partyWeaponDmg` |
| playerInitiativeMod | counter | global | 1 | Initiative modifier (usually DEX mod) | `$playerInitiativeMod` |
| playerPassivePerception | counter | global | 11 | 10 + WIS mod + perception proficiency | `$playerPassivePerception` |

### XP Thresholds by Level (D&D 5e)

<!-- Reference table — do not declare as variables. Used by <<levelUp>> widget to set $xpThreshold. -->

| Level | XP to reach | Proficiency Bonus |
|---|---|---|
| 1 | 0 | +2 |
| 2 | 300 | +2 |
| 3 | 900 | +2 |
| 4 | 2700 | +2 |
| 5 | 6500 | +3 |
| 6 | 14000 | +3 |
| 7 | 23000 | +3 |
| 8 | 34000 | +3 |
| 9 | 48000 | +4 |
| 10 | 64000 | +4 |

<!-- Continue per PHB for levels 11–20. Thresholds are hardcoded in <<levelUp>> widget. -->

---


<!-- Auto-set when a node is entered. Used to prevent repeated intro text,
     unlock lore options, or track exploration. -->

| Variable | Type | Scope | Default | Export (SC) | Export (Ink) | Set in | Read in |
|---|---|---|---|---|---|---|---|
| visited_NODE-001 | visited | global | false | `$visited_NODE_001` | `~ visited_node_001` | NODE-001 | [NODE_IDs] |
| visited_NODE-[N] | visited | global | false | | | | |

---


<!-- Simple true/false state. Use for events that happen once. -->

| Variable | Type | Scope | Default | Description | Export (SC) | Export (Ink) | Set in | Read in |
|---|---|---|---|---|---|---|---|---|
| flag_[name] | flag | global | false | [DESCRIPTION] | `$flag_[name]` | `~ flag_[name]` | NODE-[N] | NODE-[N] |

---

## Counters

<!-- Integer values. Use for progress tracking, aggregate choice scoring, turn counts. -->

| Variable | Type | Scope | Default | Range | Description | Export (SC) | Export (Ink) | Set in | Read in |
|---|---|---|---|---|---|---|---|---|---|
| counter_[name] | counter | global | 0 | 0–[MAX] | [DESCRIPTION] | `$counter_[name]` | `~ counter_[name]` | NODE-[N] | NODE-[N] |

---

## Inventory

<!-- Item tracking. type=array: unlimited list. type=slots: fixed capacity from constitution.md. -->

| Item Variable | Type | Scope | Default | Description | Export (SC) | Export (Ink) |
|---|---|---|---|---|---|---|
| inv_[item_name] | inventory | global | false | [ITEM_DESCRIPTION] | `$inv_[item_name]` (boolean flag) | `~ inv_[item_name]` |

     Sugarcube array alternative (manual): `<<set $inv.push("item")>>` / `<<if $inv.includes("item")>>`
     Use the array alternative only if you need to iterate or count items; write it as raw prose markup. -->

---

## Equipment Slots

<!-- Tracks what is currently equipped per slot.
     Slot variables hold the item name (string) or "none" when empty.
     Each slot variable must be paired with inv_[item] in the Inventory section above.
     Slots: weapon | armor | shield | off_hand
     Stat variables (stat_ac_bonus, stat_damage_bonus) reflect the combined effect of all equipped items. -->

| Variable | Slot | Type | Scope | Default | Valid Values | Export (SC) | Export (Ink) |
|---|---|---|---|---|---|---|---|
| equipped_weapon | weapon | string | global | "none" | "none" / inv item names | `$equipped_weapon` | `~ equipped_weapon` |
| equipped_armor | armor | string | global | "none" | "none" / inv item names | `$equipped_armor` | `~ equipped_armor` |
| equipped_shield | shield | string | global | "none" | "none" / inv item names | `$equipped_shield` | `~ equipped_shield` |
| equipped_off_hand | off_hand | string | global | "none" | "none" / inv item names | `$equipped_off_hand` | `~ equipped_off_hand` |

## Equipment Stats (Derived)

<!-- Derived counters updated by MECHANIC:EQUIP. Do not set these directly in prose.
     stat_ac_bonus: sum of AC bonuses from equipped armor + shield.
     stat_damage_bonus: bonus from equipped weapon (flat modifier, not dice).
     Declare additional stat variables here if the project uses other derived values (e.g. stat_initiative_bonus). -->

| Variable | Type | Scope | Default | Range | Description | Export (SC) | Export (Ink) |
|---|---|---|---|---|---|---|---|
| stat_ac_bonus | counter | global | 0 | 0–[MAX] | Combined AC bonus from equipped armor and shield | `$stat_ac_bonus` | `~ stat_ac_bonus` |
| stat_damage_bonus | counter | global | 0 | 0–[MAX] | Flat damage bonus from equipped weapon | `$stat_damage_bonus` | `~ stat_damage_bonus` |

<!-- For tabletop output: these variables are printed as GM reference callouts, not rendered in engine.
     Declare real armor/weapon items as inv_[item] entries in the Inventory section,
     then reference them in MECHANIC:EQUIP hooks. -->

---

## Accessory Slots

<!-- Tracks what is currently equipped in each magical/clothing accessory slot.
     Slot variables hold the item name (string) or "none" when empty.
     Available slots: ring_left | ring_right | neck | cloak | boots | gloves | belt | head
     Add only the slots your project uses — delete unused rows. -->

| Variable | Slot | Type | Scope | Default | Valid Values | Export (SC) | Export (Ink) |
|---|---|---|---|---|---|---|---|
| equipped_ring_left | ring_left | string | global | "none" | "none" / inv item names | `$equipped_ring_left` | `~ equipped_ring_left` |
| equipped_ring_right | ring_right | string | global | "none" | "none" / inv item names | `$equipped_ring_right` | `~ equipped_ring_right` |
| equipped_neck | neck | string | global | "none" | "none" / inv item names | `$equipped_neck` | `~ equipped_neck` |
| equipped_cloak | cloak | string | global | "none" | "none" / inv item names | `$equipped_cloak` | `~ equipped_cloak` |
| equipped_boots | boots | string | global | "none" | "none" / inv item names | `$equipped_boots` | `~ equipped_boots` |
| equipped_gloves | gloves | string | global | "none" | "none" / inv item names | `$equipped_gloves` | `~ equipped_gloves` |
| equipped_belt | belt | string | global | "none" | "none" / inv item names | `$equipped_belt` | `~ equipped_belt` |
| equipped_head | head | string | global | "none" | "none" / inv item names | `$equipped_head` | `~ equipped_head` |

## Accessory Stats (Derived)

<!-- Cumulative stat bonuses contributed by all equipped accessories.
     Updated by MECHANIC:ACCESSORY — do not set directly in prose.
     Add rows for any additional stats your project needs (e.g. stat_stealth_bonus). -->

| Variable | Type | Scope | Default | Range | Description | Export (SC) | Export (Ink) |
|---|---|---|---|---|---|---|---|
| stat_magic_bonus | counter | global | 0 | 0–[MAX] | Cumulative magic attack/save bonus from accessories | `$stat_magic_bonus` | `~ stat_magic_bonus` |
| stat_resist_bonus | counter | global | 0 | 0–[MAX] | Cumulative elemental/magic resistance bonus | `$stat_resist_bonus` | `~ stat_resist_bonus` |

---

## Consumables

<!-- Single-use items (potions, scrolls, wands).
     Boolean flag tracks possession; removed from $inv_list on use via MECHANIC:CONSUME.
     Wands additionally need a charge counter (one row per wand in ## Counters). -->

| Item Variable | Type | Scope | Default | Consumable Type | Effect | Export (SC) | Export (Ink) |
|---|---|---|---|---|---|---|---|
| inv_[consumable_name] | inventory | global | false | potion\|scroll\|wand | [EFFECT_DESCRIPTION] | `$inv_[consumable_name]` | `~ inv_[consumable_name]` |

<!-- Wand charge counters: declare one entry per wand in ## Counters above.
     Naming convention: wand_[item_name]_charges
     Example: | wand_fire_wand_charges | counter | global | 7 | 0–7 | Charges remaining on fire wand | ... | -->

---

## Spell Registry

<!-- One flag per learnable spell. Set to true when the character learns or memorises the spell.
     Naming convention: spell_known_[spell_name]
     spell_[spell_name]_active: optional transient flag set true for one node after casting;
       reset to false at the next node or on a long rest. -->

| Variable | Type | Scope | Default | Description | Export (SC) | Export (Ink) |
|---|---|---|---|---|---|---|
| spell_known_[spell_name] | flag | global | false | [SPELL_DESCRIPTION] — [SCHOOL] spell, level [N] | `$spell_known_[spell_name]` | `~ spell_known_[spell_name]` |
| spell_[spell_name]_active | flag | session | false | True for one node after casting; reset on rest | `$spell_[spell_name]_active` | `~ spell_[spell_name]_active` |

---

## Spell Slots

<!-- One counter per spell level. Max values come from class/level in mechanics.md.
     Naming convention: spell_slots_[N] where N is the spell level (1–9).
     Recovered by MECHANIC:SPELL recover or MECHANIC:COUNTER on long rest nodes.
     Add only levels your project uses — delete unused rows. -->

| Variable | Level | Type | Scope | Default | Max | Export (SC) | Export (Ink) |
|---|---|---|---|---|---|---|---|
| spell_slots_1 | 1 | counter | global | [MAX_L1] | [MAX_L1] | `$spell_slots_1` | `~ spell_slots_1` |
| spell_slots_2 | 2 | counter | global | [MAX_L2] | [MAX_L2] | `$spell_slots_2` | `~ spell_slots_2` |
| spell_slots_3 | 3 | counter | global | [MAX_L3] | [MAX_L3] | `$spell_slots_3` | `~ spell_slots_3` |
| spell_slots_[N] | [N] | counter | global | [MAX_LN] | [MAX_LN] | `$spell_slots_[N]` | `~ spell_slots_[N]` |

<!-- Max slot counts per level are defined in mechanics-[ruleset].md by class and party level.
     For tabletop output: slot tracking is advisory; physical tracking stays on the character sheet. -->

---

## Trust Scores (per NPC)

<!-- Integer. Thresholds defined in characters/NPC-NNN.md. -->

| Variable | NPC ID | Scope | Default | Range | Export (SC) | Export (Ink) |
|---|---|---|---|---|---|---|
| trust_[npc_name] | NPC-[N] | global | 50 | 0–100 | `$trust_[npc_name]` | `~ trust_[npc_name]` |

---

## Currency

<!-- Declared once per currency type. Multiple currencies allowed. -->

| Variable | Name | Scope | Default | Min | Export (SC) | Export (Ink) |
|---|---|---|---|---|---|---|
| [var_name] | [CURRENCY_NAME] | global | [N] | 0 | `$[var_name]` | `~ [var_name]` |

---

## Shop State

<!-- One open-flag and one set of per-item stock counters per shop declared in
     world-building-template.md ## Shops.

     $shop_registry is an array consumed by ShopUI. Each entry:
       { id, display, npc, faction_id, sell_ratio, restock_on, catalog: [
           { item, display, price, currency, stock, min_tier }
         ] }
     shop_[name]_open   — flag; false = shop inaccessible (story gate, reputation, hours)
     shop_[name]_stock_[item] — counter; -1 = unlimited; 0 = sold out

     speckit.compile populates $shop_registry from world-building-template.md ## Shops.
     When authoring manually, keep this table in sync with $shop_registry.

     Price modifier sources (all optional; defined in constitution.md):
       CHA modifier: ±[CHA_MOD] × 2% per point above/below 10
       Faction standing: see world-building-template.md ## Shops → price_discount_by_tier -->

| Variable | Shop ID | Type | Scope | Default | Notes | Export (SC) |
|---|---|---|---|---|---|---|
| shop_[name]_open | SHOP-[N] | flag | global | true | false = inaccessible | `$shop_[name]_open` |
| shop_[name]_stock_[item] | SHOP-[N] | counter | global | [N] | -1 = unlimited; 0 = sold out | `$shop_[name]_stock_[item]` |

<!-- [REPEAT — one open-flag + one stock counter per limited-stock item, per shop]

     Unlimited-stock items do NOT need a stock counter — the catalog entry stock: -1 is sufficient.
     Only declare stock counters for items with a finite quantity (rare items, unique pieces). -->

---

## NPC State

<!-- Enumerated states per NPC. Valid values defined in characters/NPC-NNN.md. -->

| Variable | NPC ID | Scope | Default | Valid States | Export (SC) | Export (Ink — integer enum) |
|---|---|---|---|---|---|---|
| npc_[name]_state | NPC-[N] | global | alive | alive / dead / hostile / absent | `$npc_[name]_state` | `~ npc_[name]_state` (0=alive,1=dead,2=hostile,3=absent) |

---

## Ending Conditions

<!-- Progress counters toward specific endings. Checked at climax nodes. -->

| Variable | Ending ID | Scope | Default | Threshold to Unlock | Export (SC) | Export (Ink) |
|---|---|---|---|---|---|---|
| end_[ending_id]_progress | END-[ID] | global | 0 | >= [N] | `$end_[id]_progress` | `~ end_[id]_progress` |

---

## Faction & Reputation

<!-- Numeric reputation score per faction declared in world-building-template.md ## Factions.
     Each faction also carries a derived tier string (computed by <<factionRep>> widget).
     $faction_registry is consumed by FactionUI passage and the StoryCaption stub.

     Naming convention:
       faction_[faction_name]_rep    counter  — signed integer; clamped to [min, max]
       faction_[faction_name]_tier   string   — derived from score; do NOT write directly

     Tier threshold convention (adjust per constitution.md ## Reputation Scale):
       <= -100  "hostile"
       -99 – -51 "unfriendly"
       -50 –  49 "neutral"
        50 –  74 "friendly"
        75 –  99 "allied"
       >= 100   "exalted"

     $faction_registry: array of objects consumed by FactionUI and StoryCaption.
     Each entry: { id, display, icon, minRep, maxRep, thresholds: {hostile, unfriendly, neutral, friendly, allied, exalted} }
     speckit.compile populates this from world-building-template.md ## Factions for SugarCube targets.

     MECHANIC:FACTION hooks in node files must reference faction IDs exactly as declared here.
     speckit.continuity checks that tier transitions are narratively motivated. -->

| Variable | Faction ID | Type | Scope | Default | Range | Export (SC) | Export (Ink) |
|---|---|---|---|---|---|---|---|
| faction_[name]_rep | FACTION-[N] | counter | global | 0 | [MIN]–[MAX] | `$faction_[name]_rep` | `~ faction_[name]_rep` |
| faction_[name]_tier | FACTION-[N] | string | global | "neutral" | hostile / unfriendly / neutral / friendly / allied / exalted | `$faction_[name]_tier` | *(derived — read-only)* |

<!-- [REPEAT — one row pair per faction in world-building-template.md ## Factions]

     Common starting defaults per constitution.md:
       - Major civic factions: 0 (neutral)
       - Enemy factions: -50 (unfriendly)
       - Allied factions: 50 (friendly)
       - Secret factions: 0 (neutral, unknown to player initially)

     Faction reputation changes that cross a tier boundary should trigger a UI notification.
     The <<factionRep>> widget updates both _rep and _tier atomically. -->

---

## Quest State

<!-- One state variable + one stage counter per quest defined in quests-template.md.
     State machine: "inactive" → "active" → "stage_N" → "complete" | "failed"
     SOURCE: quests-template.md — one row pair per quest entry.
     Naming convention:
       quest_[quest_name]_state   string  — current lifecycle state
       quest_[quest_name]_stage   counter — current stage index (0 = not started)

     $quest_registry is a special array consumed by the QuestJournal UI passage.
     Each entry: { id, display, tier, stages[] }
     speckit.compile populates this from quests-template.md automatically for SugarCube targets.
     When authoring manually, keep $quest_registry in sync with the rows below. -->

| Variable | Quest ID | Type | Scope | Default | Valid States | Export (SC) | Export (Ink) |
|---|---|---|---|---|---|---|---|
| quest_[quest_name]_state | [QUEST_ID] | string | global | "inactive" | inactive / active / complete / failed | `$quest_[quest_name]_state` | `~ quest_[quest_name]_state` |
| quest_[quest_name]_stage | [QUEST_ID] | counter | global | 0 | 0–[MAX_STAGES] | `$quest_[quest_name]_stage` | `~ quest_[quest_name]_stage` |

<!-- [REPEAT — one row pair per quest in quests-template.md]

     Tier values (from quests-template.md ## Quest Tier):
       main | side | optional | companion | faction
     Used by QuestJournal UI to group and filter quest display. -->

---

## Timer Variables

<!-- Only when Hook: timer is enabled in constitution.md. -->

| Variable | Type | Scope | Default | Failure Node | Export (SC) | Export (Ink) |
|---|---|---|---|---|---|---|
| timer_[name] | timer | session | [N] | NODE-[N] | `$timer_[name]` | `~ timer_[name]` |

---

## Random Result Variables

<!-- Variables used with MECHANIC:RANDOM. Declare as type: counter.
     Roll results are integers in the declared min–max range. -->

| Variable | Type | Scope | Default | Range | Description | Export (SC) | Export (Ink) |
|---|---|---|---|---|---|---|---|
| random_[name] | counter | session | 0 | [min]–[max] | [DESCRIPTION — e.g. "Luck roll result"] | `$random_[name]` | `~ random_[name]` |

> **Note**: Use `scope: session` unless the roll result needs to persist across saves. Random variables are re-rolled each time the hook executes.

---

## Choice Memory Variables

<!-- Variables used with MECHANIC:CHOICE_MEMORY. Declare as type: string.
     Follow the naming convention choice_[node_id_context].
     Ink targets: string values are mapped to integer CONST at export. -->

| Variable | Type | Scope | Default | Possible Values | Description | Export (SC) | Export (Ink — CONST int) |
|---|---|---|---|---|---|---|---|
| choice_[name] | string | global | "" | "[label_a]" / "[label_b]" / ... | [DESCRIPTION] | `$choice_[name]` | `~ choice_[name]` (CONST) |

---

## Clue Variables

<!-- Variables used with MECHANIC:CLUE. Declare as type: flag.
     Always use the clue_ prefix. One variable per distinct clue. -->

| Variable | Type | Scope | Default | Description | Export (SC) | Export (Ink) |
|---|---|---|---|---|---|---|
| clue_[name] | flag | global | false | [WHAT THIS CLUE REVEALS] | `$clue_[name]` | `~ clue_[name]` |

---

## POV Variable

<!-- Only when player_perspective: switching is set in constitution.md. -->

| Variable | Valid Values | Default | Export (SC) | Export (Ink) |
|---|---|---|---|---|
| pov | [character_names] | [DEFAULT_CHARACTER] | `$pov` | `~ pov` |

---

## Tier 2 Variables (stubs — no export translation in v1.0)

<!-- Variables used with Tier 2 hooks. Exported with // UNSUPPORTED HOOK warning. -->

| Variable | Hook Type | Description |
|---|---|---|
| knowledge_[name] | knowledge | [DESCRIPTION] |
| faction_[name] | faction | [DESCRIPTION] |
| location_[name]_state | location_state | [DESCRIPTION] |
| object_[name]_state | object_state | [DESCRIPTION] |
