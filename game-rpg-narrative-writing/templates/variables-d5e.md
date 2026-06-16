---
title: "[CAMPAIGN_NAME] Variables Registry"
template: "variables-d5e"
game_system: "D&D 5e"
---

# [CAMPAIGN_NAME] — Variables Registry

Complete list of all variables used in the campaign. This enables `speckit.outline` and `speckit.implement` to reference consistent state.

---

## I. Ability Scores & Modifiers (Immutable — Set at Campaign Start)

These are set once and never change.

```
Strength Modifier:              player_strength_mod = [N]  // e.g., +3
Dexterity Modifier:            player_dexterity_mod = [N]  // e.g., +0
Constitution Modifier:         player_constitution_mod = [N]
Intelligence Modifier:         player_intelligence_mod = [N]
Wisdom Modifier:               player_wisdom_mod = [N]
Charisma Modifier:             player_charisma_mod = [N]  // e.g., +1
```

---

## II. Skill Modifiers (Calculated from Ability Scores)

Derived from ability scores + proficiency (if trained):

```
player_acrobatics = player_dexterity_mod + [prof if trained]
player_animal_handling = player_wisdom_mod + [prof if trained]
player_arcana = player_intelligence_mod + [prof if trained]
player_athletics = player_strength_mod + [prof if trained]
player_deception = player_charisma_mod + [prof if trained]
player_history = player_intelligence_mod + [prof if trained]
player_insight = player_wisdom_mod + [prof if trained]
player_intimidation = player_charisma_mod + [prof if trained]
player_investigation = player_intelligence_mod + [prof if trained]
player_medicine = player_wisdom_mod + [prof if trained]
player_nature = player_intelligence_mod + [prof if trained]
player_perception = player_wisdom_mod + [prof if trained]
player_performance = player_charisma_mod + [prof if trained]
player_persuasion = player_charisma_mod + [prof if trained]
player_sleight_of_hand = player_dexterity_mod + [prof if trained]
player_stealth = player_dexterity_mod + [prof if trained]
player_survival = player_wisdom_mod + [prof if trained]
```

---

## III. Companion Approval Tracking (Mutable — Change Per Session)

Range: -100 to +100

### Companion 1: [NAME]

```
thorne_recruited: false → true (when party recruits)
thorne_approval: -10 (starts here, changes with choices)
thorne_alive: true
thorne_romance_gate: 76 (approval needed for romance dialogue)
thorne_in_party: false → true (actively adventuring with party)
thorne_wounded: false (during combat)
thorne_betrayed: false (if companion feels wronged)
thorne_ending_locked: "Revolution" (this ending requires this companion)
```

### Companion 2: [NAME]

```
sister_mercy_recruited: false → true
sister_mercy_approval: 20
sister_mercy_alive: true
sister_mercy_romance_gate: 81
sister_mercy_in_party: false → true
sister_mercy_wounded: false
sister_mercy_betrayed: false
sister_mercy_ending_locked: "Redemption"
```

### Companion 3: [NAME]

```
kael_recruited: false → true
kael_approval: 0
kael_alive: true
kael_romance_gate: 81
kael_in_party: false → true
kael_wounded: false
kael_betrayed: false
kael_ending_locked: "Power_Broker"
```

---

## IV. Faction Reputation Tracking (Mutable — Change Per Session)

Range: -100 to +100

```
guard_rep: 20 (start) → [final] (ending gate: >50)
temple_rep: 10 (start) → [final] (ending gate: >60)
syndicate_rep: 0 (start) → [final] (ending gate: >70)
merchant_rep: 5 (start) → [final] (flavor faction)

guard_weakened: false (if guard loses power)
temple_corrupted: false (if temple leadership compromised)
syndicate_exposed: false (if conspiracy revealed)
```

---


```
// Discovery phase
conspiracy_discovered: false → true (session 3-4)
conspiracy_depth: 0 → 5 (number of layers revealed)
conspirators_identified: 0 → 5 (count of identified conspirators)
conspirators_identified_list: [] (names of conspirators known)

// Investigation phase
guard_captain_confesses: false → true (NODE-015 outcome)
evidence_ledger_acquired: false → true (quest item)
conspiracy_location_found: false → true (hideout discovered)

// Confrontation phase
conspirators_caught: 0 → [count] (arrested/defeated)
conspirators_dead: 0 → [count] (killed in combat)
conspiracy_dismantled: false → true (final victory)

// Ending determination
ending_type: null → "Just_Ruler" | "Shadow_Broker" | etc.
ending_reached: false → true (final node)
```

---

## VI. Inventory & Items (Mutable — Add/Remove Per Node)

### Quest Items (Unique, Plot-Critical)

```
inventory_evidence_ledger: false → true (found NODE-030)
inventory_signet_ring: false → true (found NODE-015 if successful interrogation)
inventory_conspiracy_letter: false → true (found NODE-040)
inventory_temple_key: false → true (found NODE-080)
```

### Equipment (Optional, Flavor)

```
equipment_priestess_robes: false → true (affects dialogue with temple NPCs)
equipment_guard_insignia: false → true (affects dialogue with guard NPCs)
equipment_syndicate_ring: false → true (affects dialogue with syndicate NPCs)
```

### Consumables (Counters)

```
inventory_healing_potions: 0 → [count] (restored per session)
inventory_spell_scrolls: 0 → [count] (consumed when used)
inventory_antitoxin: 0 → [count] (used in specific encounters)
```

---

## VII. Combat State (Mutable During Encounters)

### Party HP Tracking

```
barbarian_hp_current: [full] → [remaining] (during combat)
barbarian_hp_max: [max] (for this level)
barbarian_status: "healthy" | "wounded" | "unconscious"

rogue_hp_current: [full] → [remaining]
rogue_hp_max: [max]
rogue_status: "healthy" | "wounded" | "unconscious"

cleric_hp_current: [full] → [remaining]
cleric_hp_max: [max]
cleric_status: "healthy" | "wounded" | "unconscious"

wizard_hp_current: [full] → [remaining]
wizard_hp_max: [max]
wizard_status: "healthy" | "wounded" | "unconscious"

// After combat
party_total_damage_taken: 0 → [cumulative]
```

### Spell Resources

```
wizard_spell_slots_1st: 4 → [remaining]
wizard_spell_slots_2nd: 3 → [remaining]
wizard_spell_slots_3rd: 2 → [remaining]

cleric_spell_slots_1st: 4 → [remaining]
cleric_spell_slots_2nd: 3 → [remaining]
cleric_channel_divinity: 2 → [remaining]
```

### Combat Outcomes

```
last_combat_outcome: "player_won" | "player_lost" | "player_retreated"
last_combat_opponent: "[NPC_NAME]" (e.g., "Guard_Captain")
last_combat_xp_gained: [N]
last_combat_loot_gold: [N]
last_combat_loot_items: ["item_1", "item_2"]
```

---

## VIII. Currency & Wealth (Mutable — Changes Per Session)

```
party_gold: 0 → [cumulative] (shared pool)
party_copper: 0 → [cumulative] (minor transactions)
party_silver: 0 → [cumulative] (if using variant rules)

// Spending tracked
gold_spent_on_equipment: 0
gold_spent_on_lodging: 0
gold_spent_on_bribes: 0
gold_donated_to_faction: 0

// Total accumulated
total_gold_earned: 0 → [cumulative]
```

---

## IX. Campaign Progression (Mutable — Update Per Session)

```
current_session: 1 → 15
current_level: 5 → 8 (party levels up when XP threshold reached)
current_act: 1 → 3

party_total_xp: 0 → [cumulative]
party_xp_threshold_next_level: 6500 (for level 6)

// Session tracking
sessions_completed: 0 → 15
time_in_campaign_days: 0 → [approximate game world days]
```

---

## X. Skill Check History (Mutable — Log Per Node)

Logged for `speckit.consequences` validation:

```
// Each skill check creates an entry
skill_checks_attempted: 0 → [count]
skill_checks_succeeded: 0 → [count]
skill_checks_failed: 0 → [count]

// Success rate by skill
insight_successes: 0 → [count]
insight_failures: 0 → [count]

persuasion_successes: 0 → [count]
persuasion_failures: 0 → [count]

deception_successes: 0 → [count]
deception_failures: 0 → [count]

intimidation_successes: 0 → [count]
intimidation_failures: 0 → [count]

// DC tracking
skill_checks_by_dc_12: 0 → [count]
skill_checks_by_dc_14: 0 → [count]
skill_checks_by_dc_16: 0 → [count]
```

---

## XI. NPC State Tracking (Mutable — Update Per Node)

```
// Guard Captain
npc_guard_captain_alive: true → false (if killed)
npc_guard_captain_status: "enemy" | "neutral" | "ally" | "dead"
npc_guard_captain_confessed: false → true
npc_guard_captain_joins_party: false → true
npc_guard_captain_wounded: false → true

// Conspiracy Leader
npc_conspiracy_leader_alive: true → false
npc_conspiracy_leader_location_known: false → true

// Faction Leaders
npc_guard_commander_opinion: "hostile" | "neutral" | "favorable"
npc_syndicate_master_opinion: "hostile" | "neutral" | "favorable"
npc_high_priest_opinion: "hostile" | "neutral" | "favorable"
```

---

## XII. Player Knowledge State (Mutable — Update Per Node)

Tracks what player character knows (for information asymmetry validation):

```
// Conspiracy knowledge
player_knows_conspiracy_exists: false → true
player_knows_conspiracy_scale: 0 → 5 (depth of understanding)
player_knows_identities: [] (list of known conspirators)
player_knows_motive: false → true (why conspiracy formed)
player_knows_location: false → true (where conspirators meet)
player_knows_deadline: false → true (when conspiracy executes plan)

// Faction knowledge
player_knows_guard_connection: false → true
player_knows_syndicate_involvement: false → true
player_knows_temple_corruption: false → true
```

---

## XIII. Choice Memory (Mutable — Log Important Choices)

```
// Track significant party decisions for later branching
choice_interrogation_approach: "insight" | "deception" | "intimidation" | "mercy"
choice_faction_first_alliance: "guard" | "syndicate" | "temple"
choice_conspiracy_report_method: "directly" | "subtly" | "secretly"
choice_companion_1_priority: true | false (did party help recruit?)
choice_final_confrontation_method: "combat" | "diplomacy" | "deception"
choice_ending_direction: "justice" | "chaos" | "redemption" | etc.
```

---

## XIV. Ending Gates (Read-Only Reference — Set in endings-d5e.md)

These determine which ending unlocks:

```
// Just Ruler ending
ending_just_ruler_gate: (guard_rep > 50 AND temple_rep > 60 AND syndicate_rep < 20)

// Shadow Broker ending
ending_shadow_broker_gate: (syndicate_rep > 70 AND guard_rep < 0)

// Redemption ending
ending_redemption_gate: (temple_rep > 60 AND sister_mercy_alive AND player_charisma_mod > 0)

[... all 7 ending gates ...]
```

---

## XV. Validator Checkpoints (For speckit.checklist)

These are read during validation:

```
// Player Agency Check
choices_with_distinct_consequences: 0 → [count]
illusory_choices: 0 → [count] (should remain 0)

// Continuity Check
npc_knowledge_state_consistent: true | false
companion_approval_consistent: true | false
faction_alignment_consistent: true | false

// Reachability Check
unreachable_nodes: [] (should be empty)
unreachable_endings: [] (should have only 4-5 locked, not all 7)

// Difficulty Scaling Check
dc_matches_level: true | false
skill_check_distribution_healthy: true | false
```

---

## XVI. Variable Initialization Block (For outline/implement)

Copy this into first node (`=== START ===`):

```ink
VAR player_strength_mod = [N]
VAR player_dexterity_mod = [N]
VAR player_constitution_mod = [N]
VAR player_intelligence_mod = [N]
VAR player_wisdom_mod = [N]
VAR player_charisma_mod = [N]

VAR thorne_recruited = false
VAR thorne_approval = -10
VAR thorne_alive = true

VAR sister_mercy_recruited = false
VAR sister_mercy_approval = 20
VAR sister_mercy_alive = true

VAR kael_recruited = false
VAR kael_approval = 0
VAR kael_alive = true

VAR guard_rep = 20
VAR temple_rep = 10
VAR syndicate_rep = 0

VAR conspiracy_discovered = false
VAR conspirators_identified = 0
VAR party_level = 5
VAR party_gold = 0
VAR party_xp = 0

VAR ending_type = null
VAR ending_reached = false
```

---

## XVII. Variable Reference Guide (For Node Authors)

When writing nodes, reference these variables:

| Use Case | Variable | Type | Range |
|----------|----------|------|-------|
| Check if companion recruited | `thorne_recruited` | bool | true/false |
| Check approval level | `thorne_approval` | int | -100 to +100 |
| Check faction status | `guard_rep` | int | -100 to +100 |
| Check plot discovery | `conspiracy_discovered` | bool | true/false |
| Check inventory | `inventory_evidence_ledger` | bool | true/false |
| Check party level | `party_level` | int | 5-8 |
| Check NPC alive | `npc_guard_captain_alive` | bool | true/false |

---

**Variables Registry Status:** [DRAFT / APPROVED / READY FOR OUTLINE]

**Total Variables:** ~150  
**Mutable Variables:** ~120  
**Immutable Variables:** ~30  

**Last Updated:** [DATE]
