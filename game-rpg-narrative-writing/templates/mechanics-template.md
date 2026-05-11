# Mechanic Hook Schemas: [GAME_TITLE]

<!-- Reference document for all mechanic hooks used in this project.
     Cross-referenced by speckit.implement, speckit.checklist, speckit.continuity, and export.py.
     Only hooks declared as enabled in constitution.md Section II are active. -->

---

## Tier 1 Hooks — Fully Exported (v1.0)

### lag — Boolean State

`
[MECHANIC:FLAG set=[variable_name] value=true|false]
[MECHANIC:FLAG check=[variable_name]]
[conditional prose]
[/MECHANIC]
`

| Parameter | Sugarcube Export | Ink Export | Ren'Py |
|---|---|---|---|
| set=true | <<set $[var] to true>> | ~ [var] = true | $ [var] = True |
| set=false | <<set $[var] to false>> | ~ [var] = false | $ [var] = False |
| check (true) | <<if $[var]>>...<</if>> | {[var]: ...} | if [var]: |
| check (false) | <<if not $[var]>>...<</if>> | {not [var]: ...} | if not [var]: |

---

### counter — Integer Increment/Decrement

`
[MECHANIC:COUNTER set=[variable_name] delta=+1|-1|N]
[MECHANIC:COUNTER check=[variable_name] op=gte|lte|eq value=N]
[conditional prose]
[/MECHANIC]
`

| Parameter | Sugarcube Export | Ink Export | Ren'Py |
|---|---|---|---|
| delta=+1 | <<set $[var] += 1>> | ~ [var]++ | $ [var] += 1 |
| delta=-1 | <<set $[var] -= 1>> | ~ [var]-- | $ [var] -= 1 |
| delta=N | <<set $[var] += N>> | ~ [var] += N | $ [var] += N |
| check gte N | <<if $[var] gte N>>...<</if>> | {[var] >= N: ...} | if [var] >= N: |
| check lte N | <<if $[var] lte N>>...<</if>> | {[var] <= N: ...} | if [var] <= N: |
| check eq N | <<if $[var] is N>>...<</if>> | {[var] == N: ...} | if [var] == N: |

---

### isited — Node Seen Tracking

`
[MECHANIC:VISITED set=[variable_name]]
[MECHANIC:VISITED check=[variable_name]]
[prose shown only on first visit]
[/MECHANIC]
`

| Parameter | Sugarcube Export | Ink Export | Ren'Py |
|---|---|---|---|
| set | <<run memorize(\"[var]\", true)>> or <<set $[var] to true>> | ~ [var] = true | $ [var] = True |
| check (first visit) | <<if not $[var]>>...<</if>> | {not [var]: ...} | if not [var]: |
| check (revisit) | <<if $[var]>>...<</if>> | {[var]: ...} | if [var]: |

---

### inventory — Item Management

`
[MECHANIC:INVENTORY add=[item_variable]]
[prose describing item acquisition]
[/MECHANIC]

[MECHANIC:INVENTORY remove=[item_variable]]

[MECHANIC:INVENTORY check=[item_variable]]
[prose shown when item is present]
[/MECHANIC]
`

| Parameter | Sugarcube Export | Ink Export | Ren'Py |
|---|---|---|---|
| add | <<set \[item] to true>> | ~ inv_[item] = true | $ inv_[item] = True |
| remove | <<set \[item] to false>> | ~ inv_[item] = false | $ inv_[item] = False |
| check present | <<if \[item]>>...<</if>> | {inv_[item]: ...} | if inv_[item]: |
| check absent | <<if not \[item]>>...<</if>> | {not inv_[item]: ...} | if not inv_[item]: |

---

### equip — Weapon & Armor Equipment

<!-- Equips or unequips an item into a named slot.
     Slots: weapon | armor | shield | off_hand
     Equipping sets the slot variable to the item name and updates derived stat variables (ac_bonus, damage_bonus).
     Unequipping resets the slot variable to "none" and zeroes the associated stat.
     Item must exist in inventory (MECHANIC:INVENTORY) before it can be equipped.
     All stat variables (stat_ac_bonus, stat_damage_bonus) must be declared in variables.md. -->

`
[MECHANIC:EQUIP slot=weapon|armor|shield|off_hand item=[item_variable] damage_bonus=N]
[prose describing equipping a weapon]
[/MECHANIC]

[MECHANIC:EQUIP slot=armor|shield item=[item_variable] ac_bonus=N]
[prose describing equipping armor or a shield]
[/MECHANIC]

[MECHANIC:EQUIP unequip slot=weapon|armor|shield|off_hand]

[MECHANIC:EQUIP check slot=weapon|armor|shield|off_hand item=[item_variable]]
[prose shown only when that item is in that slot]
[/MECHANIC]

[MECHANIC:EQUIP check slot=armor ac_bonus op=gte|lte|eq value=N]
[prose shown only when armor AC bonus meets the condition]
[/MECHANIC]
`

| Parameter | Sugarcube Export | Ink Export | Ren'Py |
|---|---|---|---|
| equip weapon | <<set $equipped_weapon to "[item]">><<set $stat_damage_bonus to N>> | ~ equipped_weapon = "[item]"<br>~ stat_damage_bonus = N | $ equipped_weapon = "[item]"<br>$ stat_damage_bonus = N |
| equip armor | <<set $equipped_armor to "[item]">><<set $stat_ac_bonus to N>> | ~ equipped_armor = "[item]"<br>~ stat_ac_bonus = N | $ equipped_armor = "[item]"<br>$ stat_ac_bonus = N |
| equip shield | <<set $equipped_shield to "[item]">><<set $stat_ac_bonus += N>> | ~ equipped_shield = "[item]"<br>~ stat_ac_bonus += N | $ equipped_shield = "[item]"<br>$ stat_ac_bonus += N |
| unequip weapon | <<set $equipped_weapon to "none">><<set $stat_damage_bonus to 0>> | ~ equipped_weapon = "none"<br>~ stat_damage_bonus = 0 | $ equipped_weapon = "none"<br>$ stat_damage_bonus = 0 |
| unequip armor | <<set $equipped_armor to "none">><<set $stat_ac_bonus to 0>> | ~ equipped_armor = "none"<br>~ stat_ac_bonus = 0 | $ equipped_armor = "none"<br>$ stat_ac_bonus = 0 |
| check item in slot | <<if $equipped_[slot] is "[item]">>...<</if>> | {equipped_[slot] == "[item]": ...} | if equipped_[slot] == "[item]": |
| check ac_bonus gte N | <<if $stat_ac_bonus gte N>>...<</if>> | {stat_ac_bonus >= N: ...} | if stat_ac_bonus >= N: |
| check ac_bonus lte N | <<if $stat_ac_bonus lte N>>...<</if>> | {stat_ac_bonus <= N: ...} | if stat_ac_bonus <= N: |

<!-- Validation rules:
     - item= must match an inv_[item_variable] declared in variables.md
     - slot values are restricted to: weapon, armor, shield, off_hand
     - ac_bonus and damage_bonus must be declared as type: counter in variables.md
     - speckit.checklist will flag EQUIP hooks whose item= has no matching INVENTORY entry
     - For tabletop output: EQUIP hooks render as GM handout callouts (see implement prose model) -->

---

### accessory — Rings, Amulets, Cloaks & Magical Accessories

<!-- Equips or unequips an accessory into a named slot.
     Slots: ring_left | ring_right | neck | cloak | boots | gloves | belt | head
     Each slot can hold one item. Accessories may contribute stat bonuses
     (magic_bonus, resist_bonus, initiative_bonus) or narrative flags.
     Item must exist in inventory (MECHANIC:INVENTORY) before equipping.
     All stat variables must be declared in variables.md ## Accessory Stats. -->

`
[MECHANIC:ACCESSORY slot=ring_left|ring_right|neck|cloak|boots|gloves|belt|head item=[item_variable] magic_bonus=N resist_bonus=N]
[prose describing equipping the accessory]
[/MECHANIC]

[MECHANIC:ACCESSORY unequip slot=ring_left|ring_right|neck|cloak|boots|gloves|belt|head]

[MECHANIC:ACCESSORY check slot=ring_left|ring_right|neck|cloak|boots|gloves|belt|head item=[item_variable]]
[prose shown only when that item is in that slot]
[/MECHANIC]

[MECHANIC:ACCESSORY check stat=magic_bonus|resist_bonus op=gte|lte|eq value=N]
[prose shown only when the combined stat meets the condition]
[/MECHANIC]
`

| Parameter | Sugarcube Export | Ink Export | Ren'Py |
|---|---|---|---|
| equip (magic_bonus) | <<set $equipped_[slot] to "[item]">><<set $stat_magic_bonus += N>> | ~ equipped_[slot] = "[item]"<br>~ stat_magic_bonus += N | $ equipped_[slot] = "[item]"<br>$ stat_magic_bonus += N |
| equip (resist_bonus) | <<set $equipped_[slot] to "[item]">><<set $stat_resist_bonus += N>> | ~ equipped_[slot] = "[item]"<br>~ stat_resist_bonus += N | $ equipped_[slot] = "[item]"<br>$ stat_resist_bonus += N |
| unequip | <<set $equipped_[slot] to "none">><<set $stat_magic_bonus -= N>> | ~ equipped_[slot] = "none"<br>~ stat_magic_bonus -= N | $ equipped_[slot] = "none"<br>$ stat_magic_bonus -= N |
| check item in slot | <<if $equipped_[slot] is "[item]">>...<</if>> | {equipped_[slot] == "[item]": ...} | if equipped_[slot] == "[item]": |
| check stat gte N | <<if $stat_magic_bonus gte N>>...<</if>> | {stat_magic_bonus >= N: ...} | if stat_magic_bonus >= N: |

<!-- Validation rules:
     - item= must match an inv_[item_variable] declared in variables.md
     - slot values restricted to: ring_left, ring_right, neck, cloak, boots, gloves, belt, head
     - stat bonuses accumulate across all equipped accessories; track per-item base in ac_base_[item]
     - speckit.checklist will flag ACCESSORY hooks whose item= has no matching INVENTORY entry
     - For tabletop output: renders as GM callout listing active magical bonuses -->

---

### consume — Scrolls, Potions & Wands

<!-- Consumes a single-use item: removes it from inventory and triggers a defined effect.
     Consumable types:
       potion  — restores a counter (hp, mana) by N
       scroll  — casts a spell without spending a spell slot; item is destroyed
       wand    — decrements a charge counter (wand_[item]_charges); destroyed at 0
     Item must exist in inventory before consuming.
     effect= names a flag set true after use (optional — for plot-relevant items). -->

`
[MECHANIC:CONSUME item=[item_variable] type=potion|scroll|wand restore=[counter_variable] delta=+N]
[prose describing using the item and its effect]
[/MECHANIC]

[MECHANIC:CONSUME item=[item_variable] type=wand spell=[spell_name] charges=[wand_charges_variable]]
[prose describing the wand firing]
[/MECHANIC]

[MECHANIC:CONSUME item=[item_variable] type=scroll spell=[spell_name]]
[prose describing reading the scroll aloud; it crumbles to ash]
[/MECHANIC]

[MECHANIC:CONSUME check item=[item_variable]]
[prose shown only when this consumable is in inventory]
[/MECHANIC]
`

| Parameter | Sugarcube Export | Ink Export | Ren'Py |
|---|---|---|---|
| potion (restore) | <<set $[counter] += N>><<dropItem "[item]">> | ~ [counter] += N<br>~ inv_[item] = false | $ [counter] += N<br>$ inv_[item] = False |
| scroll (cast spell) | <<castSpell "[spell]" free=true>><<dropItem "[item]">> | ~ [spell]_active = true<br>~ inv_[item] = false | $ [spell]_active = True<br>$ inv_[item] = False |
| wand (charge) | <<set $wand_[item]_charges -= 1>><<if $wand_[item]_charges lte 0>><<dropItem "[item]">><</if>> | ~ wand_[item]_charges -= 1 | $ wand_[item]_charges -= 1 |
| check present | <<if $inv_[item]>>...<</if>> | {inv_[item]: ...} | if inv_[item]: |

<!-- Validation rules:
     - item= must match an inv_[item_variable] declared in variables.md
     - restore= counter must be declared in variables.md ## Counters
     - wand charge variables must be declared as type: counter in variables.md
     - scroll spells must be declared in variables.md ## Spell Registry
     - For tabletop output: renders as GM callout describing item effect and removal from character sheet -->

---

### spell — Spell Casting & Slot Management

<!-- Tracks known spells and spell slot expenditure.
     Casting a spell spends one slot of the spell's level.
     Slot recovery is handled by MECHANIC:COUNTER (e.g. on long rest nodes).
     Spell effect is narrative — modelled as a flag, counter delta, or NPC state change.
     Known spells are declared as flags in variables.md ## Spell Registry.
     Spell slots per level are counters in variables.md ## Spell Slots. -->

`
[MECHANIC:SPELL cast=[spell_name] level=N]
[prose describing casting the spell and its narrative effect]
[/MECHANIC]

[MECHANIC:SPELL check=[spell_name] known=true]
[prose shown only when the character knows this spell]
[/MECHANIC]

[MECHANIC:SPELL check slots level=N op=gte value=1]
[prose shown only when at least one slot of this level remains]
[/MECHANIC]

[MECHANIC:SPELL recover level=N slots=N]
[prose describing rest or recovery that restores spell slots]
[/MECHANIC]
`

| Parameter | Sugarcube Export | Ink Export | Ren'Py |
|---|---|---|---|
| cast (spend slot) | <<if $spell_slots_[N] gte 1>><<set $spell_slots_[N] -= 1>><<set $spell_[name]_active to true>><</if>> | {spell_slots_N >= 1: ~ spell_slots_N -= 1<br>~ spell_[name]_active = true} | if spell_slots_N >= 1:<br>$ spell_slots_N -= 1<br>$ spell_[name]_active = True |
| check known | <<if $spell_known_[name]>>...<</if>> | {spell_known_[name]: ...} | if spell_known_[name]: |
| check slots gte 1 | <<if $spell_slots_[N] gte 1>>...<</if>> | {spell_slots_N >= 1: ...} | if spell_slots_N >= 1: |
| recover slots | <<set $spell_slots_[N] to [MAX]>> | ~ spell_slots_N = MAX | $ spell_slots_N = MAX |

<!-- Validation rules:
     - spell= must match a spell_known_[name] flag declared in variables.md ## Spell Registry
     - level= must correspond to a spell_slots_[N] counter in variables.md ## Spell Slots
     - speckit.checklist flags casts where no slot counter is declared for that level
     - For tabletop output: renders as GM callout (spell name, slot spent, effect summary);
       slot tracking is advisory only — physical spell slot tracking stays on the character sheet -->

---

### quest — Quest State Management

<!-- Tracks the lifecycle of quests defined in quests-template.md.
     Quest state machine: inactive → active → stage_N → complete | failed
     Each quest has:
       quest_[name]_state   string: "inactive" | "active" | "stage_N" | "complete" | "failed"
       quest_[name]_stage   counter: current stage index (0 = not started)
     All quest variables must be declared in variables.md ## Quest State.
     Quest display names and stage descriptions are authored in quests-template.md;
     the journal UI reads them from the $quest_registry array set in StoryInit. -->

`
[MECHANIC:QUEST accept=[quest_name]]
[prose describing the player accepting the quest]
[/MECHANIC]

[MECHANIC:QUEST advance=[quest_name] stage=N]
[prose describing completing a quest stage]
[/MECHANIC]

[MECHANIC:QUEST complete=[quest_name]]
[prose describing the quest resolving successfully]
[/MECHANIC]

[MECHANIC:QUEST fail=[quest_name]]
[prose describing the quest failing]
[/MECHANIC]

[MECHANIC:QUEST check=[quest_name] state=inactive|active|complete|failed]
[prose shown only when the quest is in that state]
[/MECHANIC]

[MECHANIC:QUEST check=[quest_name] stage op=gte|eq value=N]
[prose shown only when quest stage meets the condition]
[/MECHANIC]
`

| Parameter | Sugarcube Export | Ink Export | Ren'Py |
|---|---|---|---|
| accept | <<questAccept "[name]">> | ~ quest_[name]_state = "active"<br>~ quest_[name]_stage = 1 | $ quest_[name]_state = "active"<br>$ quest_[name]_stage = 1 |
| advance stage N | <<questAdvance "[name]" N>> | ~ quest_[name]_stage = N | $ quest_[name]_stage = N |
| complete | <<questComplete "[name]">> | ~ quest_[name]_state = "complete" | $ quest_[name]_state = "complete" |
| fail | <<questFail "[name]">> | ~ quest_[name]_state = "failed" | $ quest_[name]_state = "failed" |
| check state | <<if $quest_[name]_state is "[state]">>...<</if>> | {quest_[name]_state == "[state]": ...} | if quest_[name]_state == "[state]": |
| check stage gte N | <<if $quest_[name]_stage gte N>>...<</if>> | {quest_[name]_stage >= N: ...} | if quest_[name]_stage >= N: |

<!-- Validation rules:
     - quest= must match a quest_[name]_state variable declared in variables.md ## Quest State
     - stage N must exist in quests-template.md for that quest
     - speckit.checklist flags QUEST hooks with no matching quest declaration
     - speckit.analyze detects quests accepted but never completable (no complete/fail hook reachable)
     - For tabletop output: renders as GM callout (quest name, stage reached, reward summary) -->

---

### charsheet — Character Sheet & Progression

<!-- Manages player character stats that feed into sugarcube-d5e-combat.js.
     The combat engine reads these variables directly — they MUST be initialised
     in StoryInit via sugarcube-character-sheet-template.twee.

     Operations:
       hp delta=N       — add/subtract HP (clamped 0–$partyMaxHP)
       xp delta=N       — add XP; auto-triggers level-up check
       levelup          — advance partyLevel, recalculate profBonus, recompute mods
       ability set=STR|DEX|CON|INT|WIS|CHA value=N — set an ability score; recalcs modifier
       rest type=short|long — recover HP (short: 1 hit die; long: full) and spell slots (long only)

     All variables must be declared in variables.md ## Character Sheet.
     Ability modifier formula: floor((score - 10) / 2) — matches D5e.abilityMod() in combat engine.
     Proficiency bonus formula: ceil(level / 4) + 1    — matches D5e.profBonus() in combat engine. -->

`
[MECHANIC:CHARSHEET hp delta=+N|-N]
[prose describing taking damage or healing]
[/MECHANIC]

[MECHANIC:CHARSHEET xp delta=+N]
[prose describing gaining experience]
[/MECHANIC]

[MECHANIC:CHARSHEET levelup]
[prose describing levelling up; shows new level and any new features]
[/MECHANIC]

[MECHANIC:CHARSHEET ability set=STR|DEX|CON|INT|WIS|CHA value=N]
[prose describing an ability score change (curse, blessing, drain)]
[/MECHANIC]

[MECHANIC:CHARSHEET rest type=short|long]
[prose describing a rest]
[/MECHANIC]

[MECHANIC:CHARSHEET check stat=hp|xp|level|STR|DEX|CON|INT|WIS|CHA op=gte|lte|eq value=N]
[prose shown only when the stat meets the condition]
[/MECHANIC]
`

| Parameter | Sugarcube Export | Notes |
|---|---|---|
| hp delta | <<hpChange N>> | Widget clamps to 0–$partyMaxHP; triggers death check |
| xp delta | <<xpGain N>> | Widget checks $xpThreshold; calls <<levelUp>> automatically |
| levelup | <<levelUp>> | Increments $partyLevel, recalcs $playerProfBonus + all modifiers |
| ability set | <<setAbility "STR" N>> | Sets score + recalcs modifier; updates combat engine vars |
| rest short | <<shortRest>> | Rolls hit die + CON mod; restores HP only |
| rest long | <<longRest>> | Full HP restore + all spell slot recovery |
| check stat gte | <<if $partyCurrentHP gte N>>...<</if>> | Direct variable check — no widget needed |

<!-- Validation rules:
     - hp delta must not be set directly in prose — always use <<hpChange>> widget
     - xp delta must not be set directly — always use <<xpGain>> widget (triggers levelup check)
     - ability score changes must recalculate the corresponding modifier variable
     - speckit.checklist flags nodes that write $partyCurrentHP or $partyLevel directly
     - For tabletop output: renders as GM callout (stat changed, new value); tracking stays on character sheet -->

---

### faction — Faction & Reputation

<!-- Tracks the player's standing with named factions.
     Each faction has a numeric reputation score (signed integer).
     Thresholds divide scores into named tiers; tiers gate dialogue, quests, prices, and endings.

     Operations:
       rep delta=[faction] by=+N|-N    — change reputation; clamps to faction min/max
       rep set=[faction] value=N       — force-set reputation (cutscenes, major story beats only)
       check=[faction] tier=hostile|unfriendly|neutral|friendly|allied|exalted
         — conditional block shown only when standing is at or above the named tier
       check=[faction] op=gte|lte|eq value=N
         — conditional block checked against raw numeric score
       rank=[faction]                  — inline render of current tier name for prose

     All factions must be declared in variables.md ## Faction & Reputation.
     Tier thresholds must match the $faction_registry entry for the faction.

     Reputation scale convention (adjust per constitution.md):
       <= -100  hostile      ("Kill on sight")
       -99 – -51 unfriendly  ("Distrusted")
       -50 –  49 neutral     ("Unknown / indifferent")
        50 –  74 friendly    ("Accepted")
        75 –  99 allied      ("Trusted")
       >= 100   exalted      ("Champion / Revered")

     For tabletop output: renders as GM callout (faction, standing before/after, new tier if changed). -->

`
[MECHANIC:FACTION rep=[faction_name] by=+N|-N]
[prose describing the consequence — the NPC's reaction, a letter, a rumour spreading]
[/MECHANIC]

[MECHANIC:FACTION rep=[faction_name] by=-N]
[prose for a negative reputation event — betrayal, theft, killing a member]
[/MECHANIC]

[MECHANIC:FACTION rep set=[faction_name] value=N]
[prose for a forced standing change — e.g. publicly named a traitor, pardoned by the king]
[/MECHANIC]

[MECHANIC:FACTION check=[faction_name] tier=friendly|allied|exalted]
[prose shown only when standing is at or above the named tier]
[/MECHANIC]

[MECHANIC:FACTION check=[faction_name] tier=hostile|unfriendly]
[prose shown only when standing is hostile or unfriendly — locked doors, refused service]
[/MECHANIC]

[MECHANIC:FACTION check=[faction_name] op=gte value=N]
[prose shown when raw score meets condition — fine-grained checks beyond tier names]
[/MECHANIC]

[MECHANIC:FACTION rank=[faction_name]]
[inline: "Your standing with the [faction] is currently [tier_name] ([score])."]
[/MECHANIC]
`

| Parameter | SugarCube Export | Ink Export | Notes |
|---|---|---|---|
| rep delta | <<factionRep "[faction]" N>> | `~ faction_[name]_rep += N` | Widget clamps to min/max; updates derived tier |
| rep set | <<factionRepSet "[faction]" N>> | `~ faction_[name]_rep = N` | Use only for scripted story beats |
| check tier | <<if _factionTier("[faction]") gte [tier_index]>>...<</if>> | `{faction_[name]_rep >= [threshold]}` | Tier indices: hostile=0 unfriendly=1 neutral=2 friendly=3 allied=4 exalted=5 |
| check op gte | <<if $faction_[name]_rep gte N>>...<</if>> | `{faction_[name]_rep >= N}` | Direct score check |
| rank inline | <<factionTierName "[faction]">> | `{_factionTierName(faction_[name]_rep)}` | Renders current tier label |

<!-- Validation rules:
     - faction_[name]_rep must not be written directly in prose — always use <<factionRep>> widget
     - speckit.checklist flags $faction_*_rep direct assignments
     - speckit.continuity checks tier transitions are narratively motivated (at least one prose line per change)
     - Each faction in this table must have a matching entry in $faction_registry (variables.md)
     - Ending nodes that require specific faction standing must declare the threshold in endings-template.md -->

---

### shop — Merchant & Economy

<!-- Opens a shop, or triggers a buy/sell transaction inline within node prose.
     Shops are catalog-driven: all items, base prices, and stock limits are declared
     in world-building-template.md ## Shops and reflected in $shop_registry.

     Two modes:
       open=[shop_id]             — opens the full ShopUI passage (SugarCube)
                                    or a GM-facing item table (tabletop)
       buy=[item] price=N        — inline one-item transaction in prose
       sell=[item] price=N       — inline sell-back within prose
       check=[shop_id] stock=[item] — conditional block shown only when item is in stock
       check=[shop_id] open      — conditional block shown only when shop is accessible

     Dynamic pricing: base price × price_mod, where price_mod is computed from:
       - CHA modifier (default: ±[CHA_MOD]×2% per point)
       - Faction standing with the merchant's faction (if any)
       Defined in constitution.md ## VI. Currency Configuration → price_modifier.

     Limited stock: tracked per-item as shop_[name]_stock_[item] (−1 = unlimited).
     Restock: configurable per shop (long rest / in-game day / never).
     Sell-back: items sold at sell_ratio × base price (default 50% — set per shop).

     All shops must be declared in world-building-template.md ## Shops.
     All currency variables must be type: currency in variables.md ## Currency.
     speckit.checklist flags shops that reference items not in $item_registry (inventory). -->

`
[MECHANIC:SHOP open=[shop_id]]
[prose describing entering the shop — sights, sounds, the merchant's greeting]
[/MECHANIC]

[MECHANIC:SHOP buy=[item_variable] price=N currency=[currency_variable]]
[prose describing the purchase — what the player receives, the exchange]
[/MECHANIC]

[MECHANIC:SHOP sell=[item_variable] price=N currency=[currency_variable]]
[prose describing the sale — what the merchant pays, their reaction]
[/MECHANIC]

[MECHANIC:SHOP check=[shop_id] stock=[item_variable]]
[prose shown only when item is in stock — "The smith still has a spare shield.."]
[/MECHANIC]

[MECHANIC:SHOP check=[shop_id] stock=[item_variable] op=lte value=2]
[prose shown when stock is low — "Only a few left.."]
[/MECHANIC]

[MECHANIC:SHOP check=[shop_id] open]
[prose shown only when the shop is accessible — reputation gate, hours, story flag]
[/MECHANIC]
`

| Parameter | SugarCube Export | Tabletop Output | Notes |
|---|---|---|---|
| open | <<shopOpen "[shop_id]">> | GM table: shop catalog with prices | Full ShopUI passage; applies price_mod automatically |
| buy item | <<shopBuy "[shop_id]" "[item]" N "[currency]">> | GM callout: item transferred, currency deducted | Debits currency, adds item to $inv_list, decrements stock |
| sell item | <<shopSell "[shop_id]" "[item]" "[currency]">> | GM callout: item sold, gold received | Credits sell_ratio×price, removes item from $inv_list |
| check stock | <<if $shop_[name]_stock_[item] neq 0>> | *(inline condition)* | −1 = unlimited stock |
| check open | <<if $shop_[name]_open>> | *(inline condition)* | Driven by shop_[name]_open flag |

<!-- Validation rules:
     - currency debits must not write the currency variable directly — always use <<shopBuy>> widget
     - speckit.checklist flags nodes that write $[currency_var] directly instead of via a shop or MECHANIC:CURRENCY
     - Every shop_id referenced in a MECHANIC:SHOP hook must have an entry in $shop_registry
     - Items listed in shop catalogs must be declared in $item_registry (inventory)
     - buy/sell transactions must have matching prose (cannot silently transfer items)
     - For tabletop output: renders as a GM-facing item table with prices and stock counts -->

---

### loot — Container & Drop Table

<!-- Declares loot tables for containers (chests, corpses, post-combat drops) and
     quest completion payouts. The loot model (fixed / weighted / d100_table) is set
     in constitution.md ## VI-B. Randomness & Economy Model.

     Three modes:
       container=[container_id]   — declares a browsable or one-shot drop container
       drop=[container_id]        — same schema; marks this table as a post-combat drop
                                    (enemy body, not a placed chest)
       quest=[quest_name]         — quest completion payout (XP + items; gold via currency=)

     container_id must match a $loot_opened_[container_id] StoryInit variable.
     All item_variable values must be declared in variables.md ## Inventory.
     gold_min / gold_max are scaled by constitution.md gold_scale at compile time.
     weight: 1–100 = % chance to include the item (weighted model only).
             weight: 100 always includes the item. weight: 0 never includes it.
     qty: how many copies of the item to grant (default 1).

     speckit.compile generates:
       - $loot_table_registry entry in StoryInit
       - $loot_opened_[container_id] = false in StoryInit
       - $quest_[quest_name]_state / _stage init lines (quest mode)
     speckit.checklist validates all item_variable and container_id references. -->

```
[MECHANIC:LOOT container=[container_id] label="[Display Name]" gold_min=N gold_max=N]
  [item_variable] weight=[W] qty=[Q]  [Display Name of this item]
  [item_variable] weight=[W] qty=[Q]  [Display Name of this item]
[/MECHANIC]
```

```
[MECHANIC:LOOT drop=[container_id] label="[Enemy/Corpse Name]" gold_min=N gold_max=N]
  [item_variable] weight=[W] qty=[Q]  [Display Name]
[/MECHANIC]
```

```
[MECHANIC:LOOT quest=[quest_name] xp=N gold=N]
  [item_variable]  [Key item awarded on quest completion]
[/MECHANIC]
```

| Parameter | SugarCube Export | Tabletop Output | Notes |
|---|---|---|-|
| container | `$loot_table_registry[id]` StoryInit entry + `$loot_opened_id = false` | GM callout: container contents list | Player browses; items taken individually |
| drop | Same as container + flagged as combat drop | GM callout: loot line under monster stat block | Auto-granted on `<<combatEnd "won">>` |
| quest | `<<questReward>>` call in node + StoryInit quest vars | GM callout: rewards block at quest completion | Gold issued via `<<lootGold>>`; items via `<<lootFixed>>` |
| weight | Drop probability 1–100 (weighted model) | Listed with % likelihood | Ignored when `loot_model: fixed` |
| qty | Number of copies granted | Quantity shown in list | Default 1 |
| gold_min / gold_max | `random(min, max)` gp (or flat if equal) | GP range shown | Scaled by `gold_scale` from constitution |

<!-- Validation rules (speckit.checklist LT checks):
     - Every container_id must have a matching $loot_opened_[id] variable
     - Every item_variable must be declared in variables.md ## Inventory
     - Nodes with scene_type: combat must have a MECHANIC:LOOT drop= or explicit no-loot comment
     - Quest payout blocks must match quests-template.md Rewards section for that quest -->

---

---

### rest — Short Rest, Long Rest & Time Advance

<!-- Declares a rest event in the node. Drives HP recovery, spell slot restoration,
     time tracking, and resets for containers / quests per constitution.md ## VI-B.

     Three rest types:
       type=short       — 1 hour; spend hit dice, no spell slot recovery
       type=long        — 8 hours; full HP + all spell slots + half hit dice returned
       type=milestone   — no mechanical recovery; narrative only (dream, revelation)

     location: flavour tag shown in RestUI header.
       Values: inn | camp | cave | safe_house | any string
     return: NODE-ID or passage name to navigate to after rest completes.
       Required for type=long. Omit for type=short (stays in scene).
     interruption: set to true if the rest can be cut short by a story trigger.
       When true, speckit.implement adds a branch for the interruption outcome.

     speckit.compile generates:
       - <<shortRestScene>> / <<longRestScene>> / prose-only block per type
       - <<restReset "long">> container and quest resets per constitution config
       - <<recoverSpellSlots N MAX>> lines inside longRestScene per variables.md
     speckit.checklist validates:
       - Every Area has ≥1 rest node (SP-005 already covers this)
       - Long rest nodes have a return= target (RT-002)
       - Milestone rest nodes have no widget calls (RT-003) -->

```
[MECHANIC:REST type=short location=camp]
[prose describing the party resting — sensation, atmosphere, NPC reactions]
[/MECHANIC]
```

```
[MECHANIC:REST type=long location=inn return=NODE-050_Morning]
[prose describing settling in for the night — what the party says, the environment]
[/MECHANIC]
```

```
[MECHANIC:REST type=milestone location=camp]
[prose — a dream, a vision, a revelation; no HP/slot recovery]
[/MECHANIC]
```

```
[MECHANIC:REST type=long location=camp return=NODE-060_Dawn interruption=true]
[prose describing the night — then interrupted by an event]
[prose describing the interruption trigger]
[/MECHANIC]
```

| Parameter | SugarCube Export | Tabletop Output | Notes |
|---|---|---|---|
| type=short | `<<shortRestScene>>` + HP recovery prose | GM callout: hit die roll, HP gained | No spell slot recovery; `$rest_type_last = "short"` |
| type=long | `<<longRestScene location return>>` | GM callout: full recovery summary | Advances `$day_counter`, calls `<<restReset "long">>` |
| type=milestone | Prose only + `/* milestone rest */` comment | Narrative block only | No mechanical effect |
| location | Stored as `$rest_type_last_location`; shown in RestUI header | Listed in GM callout | Default: "camp" |
| return | ReturnPassage arg to `<<longRestScene>>` | Next node reference | Required for type=long |
| interruption=true | Generates `$rest_interruption = true` branch | Adds interruption note in GM callout | Rest is cut short; HP/slot recovery partial (50%) |

<!-- Validation rules (speckit.checklist RT checks):
     - Every scene_type: rest node must declare a MECHANIC:REST block
     - type=long nodes must have return= set
     - type=milestone nodes must NOT call <<shortRestScene>> or <<longRestScene>>
     - Long rest recovery must not be manually coded — always use <<longRestScene>>
     - Container and quest resets must not be written manually when speckit.compile
       is responsible for generating them via <<restReset>> -->

---

### craft — Recipe-Based Item Crafting

<!-- Declares a crafting interaction in the node. Drives ingredient consumption,
     optional skill checks, result item grants, and station access.

     Two modes:
       station=[station_id]   — opens the CraftUI menu for the player to choose a recipe
                                (player-driven; station must be unlocked)
       recipe=[recipe_id]     — scripted craft attempt (author-controlled; inline)

     station_id: must match a $craft_station_[id]_unlocked variable in StoryInit.
                 Declare stations in world-building-template.md ## Crafting Stations.
     recipe_id:  must match an entry in $craft_registry.
                 Declare recipes in world-building-template.md ## Recipes.
     return:     NODE-ID to navigate to when CraftUI closes (station mode only).

     speckit.compile generates:
       - $craft_registry StoryInit block from world-building-template.md ## Recipes
       - $craft_station_[id]_unlocked = false StoryInit lines per station
     speckit.checklist validates:
       - station_id and recipe_id exist in $craft_registry / StoryInit
       - ingredient item vars are declared in variables.md ## Inventory
       - result_item is declared in variables.md ## Inventory -->

```
[MECHANIC:CRAFT station=alchemy_bench return=NODE-040_AfterCraft]
[prose describing the player approaching the station — sight, smell, NPC comment]
[/MECHANIC]
```

```
[MECHANIC:CRAFT recipe=bandage_kit]
[prose describing the scripted craft attempt — the action, the result]
[/MECHANIC]
```

```
[MECHANIC:CRAFT unlock_station=forge]
[prose describing when the player gains access — the smith nods, the gate opens]
[/MECHANIC]
```

| Parameter | SugarCube Export | Tabletop Output | Notes |
|---|---|---|---|
| station | `<<craftStation "id" "return">>` navigates to CraftUI | GM table: available recipes at this station | Player browses and selects; skill checks rolled on click |
| recipe | `<<craftAttempt "id">>` + success/fail prose | GM callout: ingredient check, roll if skill_check | Scripted; author branches on `$last_craft_success` |
| unlock_station | `<<craftUnlockStation "id">>` | GM note: station now available | Sets `$craft_station_[id]_unlocked = true` |

<!-- Validation rules (speckit.checklist CF checks):
     - station_id must have a matching $craft_station_[id]_unlocked variable
     - recipe_id must exist in $craft_registry
     - All ingredient item vars must be declared in variables.md ## Inventory
     - result_item must be declared in variables.md ## Inventory
     - Scripted craft nodes must branch on $last_craft_success in prose -->

---

### travel_encounter — Random Encounter on Region Travel

<!-- Marks a travel node as an encounter-eligible crossing.
     Only active when constitution.md travel_encounters: encounter_table.
     If disabled (travel_encounters: none or scripted_only), this hook is a no-op
     and speckit.compile strips it from output.

     region=[REGION-ID]   — which region’s encounter table to roll against
     return=[NODE-ID]     — passage to navigate to if no encounter triggers (safe passage)

     The hook MUST be the last mechanic in the node, immediately before or instead of
     the exit link. <<travelRoll>> handles navigation for both outcomes; do NOT add
     a [[link]] or <<goto>> after it.

     Encounter roll: d20 + $region_[ShortName]_danger vs. travel_encounter_dc (constitution.md)
     On trigger: navigates to TravelEncounterTransition → resolves by type (combat/event/
     discovery/hazard) → returns to ReturnPassage.
     On safe: navigates directly to ReturnPassage.

     speckit.compile generates:
       - <<travelRoll "REGION-ID" "ReturnPassage">> in the travel node passage
       - $travel_encounter_registry from world-map-template.md ## Travel Encounter Tables
       - $region_[ShortName]_danger initialisers in StoryInit
       - $travel_encounter_dc initialiser from constitution.md travel_encounter_dc
     speckit.checklist validates:
       - Every region referenced here has a table entry in world-map-template.md
       - No exit [[link]] or <<goto>> exists after this hook in the same node
       - combat-type encounters reference valid enemy keys (cross-check encounters-d5e.md) -->

```
[MECHANIC:TRAVEL_ENCOUNTER region=REGION-Thornwood return=NODE-050_ArriveVillage]
[prose describing the journey — terrain, mood, the passage of time]
[Do NOT add an exit link after this block — <<travelRoll>> navigates automatically]
[/MECHANIC]
```

| Parameter | SugarCube Export | Tabletop Output | Notes |
|---|---|---|---|
| region | `<<travelRoll "REGION-ID" "ReturnPassage">>` | GM note: roll d20+danger vs. DC; see table | Must be the last statement in the node |
| return | ReturnPassage arg to `<<travelRoll>>` | Next node if safe passage | Required |

<!-- Validation rules (speckit.checklist TE checks):
     - region= must be a valid REGION-ID registered in world-map-template.md
     - The region must have an entry in world-map-template.md ## Travel Encounter Tables
     - No [[link]] or <<goto>> may follow this hook in the same passage
     - combat-type encounter enemies must be cross-referenced with encounters-d5e.md
     - If travel_encounters: none in constitution, this hook should not appear in any node -->

---

### companion — Companion Approval, Recruitment, and Reactions

<!-- Controls a companion's approval rating and party membership.
     Companions are defined in constitution.md ## Companion System and
     characters-template.md (one companion per file or one section per companion).
     All companion IDs must match variables.md ## Companion Approval Tracking.

     Hook variants:

       MECHANIC:COMPANION id=[NAME] approval=[+/-N]
         — Adjusts approval at this narrative moment. Display to player via prose.
         — Sign is mandatory: +10 or -15, not just 10 or 15.

       MECHANIC:COMPANION id=[NAME] action=recruit
         — Companion formally joins the party here. Call exactly once per companion.
         — Usually placed immediately after the recruit dialogue exchange.

       MECHANIC:COMPANION id=[NAME] action=leave reason=[reason]
         — Companion leaves the active party (still recruited; may rejoin).
         — reason: betrayal | story_event | low_approval | death
         — If reason=death: companion is permanently removed.

       MECHANIC:COMPANION id=[NAME] react threshold=[N] approve="[prose]" reject="[prose]"
         — Outputs approval_prose if approval >= N, reject_prose otherwise.
         — Use for short inline reactions (1–2 sentences).
         — Use <<if $[id]_tier is "warm">> blocks in .twee for multi-line branching.

     speckit.compile generates:
       — <<companionApproval "id" delta>> for approval changes
       — <<companionRecruit "id">> for recruit
       — <<companionLeave "id" "reason">> for leave
       — <<companionReact "id" N "approve" "reject">> for react
     speckit.checklist validates:
       — All companion IDs exist in constitution.md ## Companion System
       — Approval delta is a signed integer
       — recruit is called before any approval adjustment for that companion
       — leave reason=death matches a death-scene node context (scene_type: combat or cutscene)
       — react threshold is within [-100, 100] -->

```
[MECHANIC:COMPANION id=thorne approval=+10]
Thorne glances sideways at you, and for the first time allows himself a thin smile.
[/MECHANIC]
```

```
[MECHANIC:COMPANION id=thorne action=recruit]
"Then we're agreed," Thorne says, shouldering his pack. "Lead on."
[/MECHANIC]
```

```
[MECHANIC:COMPANION id=mira action=leave reason=betrayal]
Mira slams the door behind her. You hear her footsteps on the stairs and then nothing.
[/MECHANIC]
```

```
[MECHANIC:COMPANION id=mira react threshold=50
  approve="Mira nods, impressed by your candour."
  reject="Mira's jaw tightens. She says nothing."]
[/MECHANIC]
```

| Variant | SugarCube Export | Tabletop Output | Notes |
|---|---|---|---|
| approval | `<<companionApproval "id" ±N>>` | GM note: +/-N approval for [Name] | Sign required |
| recruit | `<<companionRecruit "id">>` | GM note: [Name] joins party | Once per companion |
| leave | `<<companionLeave "id" "reason">>` | GM note: [Name] leaves; reason | death = permanent |
| react | `<<companionReact "id" N "…" "…">>` | Conditional flavour text | Short prose only |

<!-- Validation rules (speckit.checklist CM checks):
     - companion id must be registered in constitution.md ## Companion System
     - approval delta must be a signed integer (never bare number)
     - recruit must precede all approval deltas for that companion across the full outline
     - leave reason=death may only appear in combat or cutscene scene_type nodes
     - react threshold must be numeric, within -100 to 100 -->

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

## Generic/Markdown Annotations

When export_target: generic is set, all hooks are written as:
[MECHANIC:TYPE parameter=value] prose [/MECHANIC]
or
[MECHANIC:TYPE parameter=value] (inline)
