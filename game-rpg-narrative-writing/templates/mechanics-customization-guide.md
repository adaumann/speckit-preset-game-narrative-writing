---
title: "Mechanic Hooks Customization Guide"
description: "How to customize and generate mechanic hooks for different campaign themes"
---

# Mechanic Hooks Customization Guide

This guide explains how to customize the D&D 5e mechanic hooks template for different campaign types, and shows how AI generates alternatives.

---

## Part 1: Understanding the Sample Pattern

The **mechanics-d5e.md** template includes concrete examples from a **conspiracy investigation campaign**:

| Element | Investigation Campaign | Your Campaign |
|---------|---|---|
| **Investigation Goal** | Conspiracy discovered → dismantled | [YOUR_GOAL] discovered → resolved |
| **Primary Quest Item** | Evidence ledger → proves guilt | [YOUR_ITEM] → proves [YOUR_GOAL] |
| **Key Ally NPC** | Guard Captain confesses → recruits | [YOUR_ALLY] confesses → recruits |
| **Factions (3)** | Guard, Temple, Syndicate | [YOUR_FACTION_1], [YOUR_FACTION_2], [YOUR_FACTION_3] |
| **Ending Gates** | Reputation with each faction | Same structure, different thresholds |

---

## Part 2: How AI Creates Alternative Themes

When generating mechanics for different campaigns, AI follows this **substitution pattern:**

### Theme 1: Monster Hunt Campaign

**Substitutions:**
- Investigation goal: "Conspiracy" → "Monster sighting"
- Primary quest item: "Evidence ledger" → "Monster heart" or "Monster corpse"
- Key ally: "Guard Captain" → "Master Hunter" or "Monster Researcher"
- Factions: "Guard/Temple/Syndicate" → "Hunters/Royals/Scholars"
- Reputation gates: "Guard rep > 50" → "Hunter reputation > 50"

**Generated hooks would look like:**

```
flag:monster_confirmed
  Name: "Monster Confirmed"
  Default: false
  Trigger: NODE-040 (collected enough evidence)
  Effect: Unlocks all monster-hunting dialogue options
  Validation: Must trigger between Session 3-4

inventory:monster_heart
  Name: "Monster Heart"
  Acquired: NODE-030 (defeat weak monster to get organ)
  Required To: NODE-040 (give to Alchemist for identification)
  Consequences: Alchemist reveals monster type and weaknesses
  
counter:hunter_rep (Range: -100 to +100)
  Name: "Hunter Guild Reputation"
  Default: 20
  Increment Events: Slay monsters, report findings
```

### Theme 2: Heist Campaign

**Substitutions:**
- Investigation goal: "Conspiracy" → "Heist target location"
- Primary quest item: "Evidence ledger" → "Building blueprint"
- Key ally: "Guard Captain" → "Heist coordinator" or "Inside agent"
- Factions: "Guard/Temple/Syndicate" → "Nobles/City watch/Thieves guild"
- Ending gates: Reputation → "Trust level" with heist crew

**Generated hooks would look like:**

```
flag:target_surveyed
  Name: "Target Location Surveyed"
  Default: false
  Trigger: NODE-040 (completed scouting)
  Effect: Unlocks heist planning dialogue
  
inventory:building_blueprint
  Name: "Building Blueprint"
  Acquired: NODE-030 (steal from surveyor)
  Required To: NODE-040 (study with architect)
  Consequences: Security DC reduced by 5
  
counter:crew_trust (Range: -100 to +100)
  Name: "Heist Crew Trust Level"
  Default: 0
  Increment Events: Successful prep, share resources
```

### Theme 3: Political Intrigue Campaign

**Substitutions:**
- Investigation goal: "Conspiracy" → "Scandal" or "Betrayal"
- Primary quest item: "Evidence ledger" → "Secret letter" or "Love letter"
- Key ally: "Guard Captain" → "Rival noble" or "Inside spy"
- Factions: "Guard/Temple/Syndicate" → "House A/House B/House C"
- Ending gates: Reputation → "Political standing" with noble houses

**Generated hooks would look like:**

```
flag:scandal_discovered
  Name: "Political Scandal Discovered"
  Default: false
  Trigger: NODE-040 (found proof)
  Effect: Unlocks blackmail/alliance options
  
inventory:love_letter
  Name: "Compromising Love Letter"
  Acquired: NODE-030 (recover from lover's chamber)
  Required To: NODE-040 (use as blackmail or evidence)
  Consequences: Target noble owes party favor or faces exposure
  
counter:house_a_standing (Range: -100 to +100)
  Name: "House A Political Standing"
  Default: 20
```

### Theme 4: Curse Breaking Campaign

**Substitutions:**
- Investigation goal: "Conspiracy" → "Curse origin"
- Primary quest item: "Evidence ledger" → "Curse description" or "Ritual components"
- Key ally: "Guard Captain" → "Sage" or "Cursed victim"
- Factions: "Guard/Temple/Syndicate" → "Mages/Priests/Ancients"
- Ending gates: Reputation → "Mystical knowledge"

**Generated hooks would look like:**

```
flag:curse_source_found
  Name: "Curse Source Located"
  Default: false
  Trigger: NODE-040 (traced curse to origin)
  Effect: Unlocks curse-breaking ritual nodes
  
inventory:curse_object
  Name: "Cursed Object"
  Acquired: NODE-030 (find source of curse)
  Required To: NODE-040 (take to sage for analysis)
  Consequences: Sage reveals curse strength and breaking method
  
counter:mystical_knowledge (Range: 0 to 100)
  Name: "Mystical Knowledge Accumulation"
  Default: 0
  Increment Events: Study curse, collect components
```

---

## Part 3: The 8 Hooks Customization Matrix

Each of the 8 hook types customizes the same way:

| Hook Type | Investigation Example | Monster Hunt Example | Heist Example | How to Customize |
|---|---|---|---|---|
| **FLAG** | conspiracy_discovered | monster_confirmed | target_surveyed | Replace investigation goal with YOUR goal |
| **COUNTER** | conspirators_caught | monsters_slain | heist_prep_score | Replace progress metric with YOUR metric |
| **VISITED** | conspiracy_chamber | monster_lair | vault_location | Replace locations with YOUR locations |
| **INVENTORY** | evidence_ledger | monster_heart | building_blueprint | Replace plot items with YOUR items |
| **TIMER** | investigation_deadline | monsoon_season (deadline) | guard_shift (patrol schedule) | Replace time pressure with YOUR deadline |
| **TRUST** | thorne_approval (companion) | hunter_master_trust | crew_member_trust | Replace NPC with YOUR key allies |
| **CURRENCY** | party_gold | bounty_gold | heist_pay | Replace wealth tracking |
| **NPC_STATE** | conspiracy_leader_location | monster_location | guard_patrol_schedule | Replace NPC tracking with YOUR tracking |

---

## Part 4: How to Request Custom Hooks from AI

### For a New Campaign Theme

Ask Spec Kit AI:

```
"I'm building a campaign about [YOUR_THEME]. Create a mechanics-d5e.md template where:
- Investigation goal: [YOUR_GOAL]
- Primary quest items: [ITEM_1], [ITEM_2], [ITEM_3]
- Key allies: [NPC_1], [NPC_2]
- Factions: [FACTION_1], [FACTION_2], [FACTION_3]
- Main locations: [LOCATION_1], [LOCATION_2], [LOCATION_3]"
```

### Example Prompt

```
"Create mechanics-d5e.md for a curse-breaking campaign where:
- Goal: Lift curse from cursed tower
- Quest items: Curse object, ritual components, ancient tome
- Key allies: Mystical sage, cursed victim, temple priest
- Factions: Mages college, Temple order, Cursed bloodline
- Locations: Tower, Mage academy, Temple library"
```

---

## Part 5: Creating Variations (AI Generation Process)

### Step 1: Identify Core Pattern

**All campaigns follow this structure:**
1. **Investigation Phase (Sessions 1-5):** Discover what needs to be done
2. **Complication Phase (Sessions 6-10):** Multiple paths/factions compete
3. **Resolution Phase (Sessions 11-15):** Final choice and consequences

### Step 2: Map to Campaign Elements

**Campaign elements that map to hooks:**

| Campaign Element | Hook Equivalent |
|---|---|
| **Main goal** → | flag: [GOAL]_discovered, flag: [GOAL]_resolved |
| **Evidence** → | inventory: [QUEST_ITEM] |
| **Key person** → | counter: [NPC]_approval, flag: [NPC]_recruited |
| **Factions** → | counter: [FACTION]_rep (one per faction) |
| **Locations** → | visited: [LOCATION] |
| **Time pressure** → | timer: [DEADLINE] |
| **Success metric** → | counter: [PROGRESS_METRIC] |

### Step 3: Generate Alternatives

For each hook, AI asks:
- "What would this look like in [CAMPAIGN_TYPE]?"
- "What are 3-5 variations that keep the same narrative function?"
- "How would a player experience this differently?"

**Example: Reputation Counter Variations**

```
Investigation: conspirators_caught (count)
Monster Hunt: monsters_slain (count)
Heist: heist_prep_completed (percentage)
Political: alliances_formed (count)
Curse: curse_components_gathered (count)
```

All work identically mechanically, but feel different narratively.

---

## Part 6: Common Customization Mistakes to Avoid

❌ **Don't:** Create hooks for things that don't affect story branching
- Example: "arrow_count" is inventory-tracked but never gated by dialogue

✅ **Do:** Only create hooks for decisions that matter
- Example: "poison_acquired" gates dialogue about poisoning vs. combat

---

❌ **Don't:** Mix concrete names with placeholders
- Example: "conspiracy_discovered" but "[MAJOR_NPC] confesses"

✅ **Do:** Use consistent placeholder style OR all concrete
- Example: Either all "[GOAL]_discovered" OR all "conspiracy_discovered"

---

❌ **Don't:** Create too many hooks (>40 total)
- Example: Individual counter for every single NPC

✅ **Do:** Use counter ranges to track groups
- Example: "conspirators_caught" (0-10) instead of separate flag for each conspirator

---

## Part 7: Testing Your Customized Hooks

Before using in campaign:

1. **Check gate consistency:**
   - Does each ending use 2-3 distinct hooks?
   - Can at least 2 endings be reached at Session 10?

2. **Verify item reachability:**
   - Can every quest item be acquired via multiple paths?
   - No dead-end items?

3. **Validate reputation changes:**
   - Does reputation actually change (-10 to +20 per session)?
   - Do changes feel impactful (not just cosmetic)?

4. **Confirm NPC availability:**
   - Can players recruit 1-3 companions?
   - Do companion fates affect endings?

---

**Next:** Use `speckit.mechanics` command to generate your custom hooks based on your constitution!
