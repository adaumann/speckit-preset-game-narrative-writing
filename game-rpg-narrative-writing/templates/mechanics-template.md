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
