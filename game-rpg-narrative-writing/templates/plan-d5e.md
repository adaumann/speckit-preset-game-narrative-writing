---
title: "[CAMPAIGN_NAME] Campaign Plan"
template: "plan-d5e"
game_system: "D&D 5e"
---

# [CAMPAIGN_NAME] — Campaign Plan

This document structures the campaign into acts, sessions, and encounter beats. **This plan PREPARES all variables, encounters, and gates needed for outline/implement steps.**

---

## I. Campaign Structure Overview

**Total Sessions:** [SESSION_COUNT] (e.g., 15)  
**Sessions per Act:** [ACT_1_SESSIONS] / [ACT_2_SESSIONS] / [ACT_3_SESSIONS]  
**Party Level Progression:** [START_LEVEL] → [END_LEVEL] (e.g., 5 → 8)  
**Estimated Total Playtime:** [HOURS] hours  

**Node Count Target:** ~[TOTAL_NODES] nodes (e.g., 140)  
- Session 1-5 (Act 1): ~[NODES] nodes
- Session 6-10 (Act 2): ~[NODES] nodes
- Session 11-15 (Act 3): ~[NODES] nodes

---

## II. ACT 1: [ACT_1_NAME] — Sessions 1-5

**Act Goal:** [OBJECTIVE]

**Dramatic Question This Act:** [QUESTION]

**Starting State:** 
- Party Level: [LEVEL]
- Party Gold: [GOLD] gp
- Known Factions: [LIST]
- Known Companions: [LIST]

**Faction Reputation (Start of Act 1):**
- [FACTION_1]: [START_REP] (neutral/allied/hostile)
- [FACTION_2]: [START_REP]
- [FACTION_3]: [START_REP]

---

### Session 1: [SESSION_1_NAME]
**Goal:** [SESSION_GOAL]  
**Level:** 5  
**Encounters:** [NUM] (mix of combat/social/exploration)  
**Node Range:** NODE_001 to NODE_010 (~10 nodes)  
**Key Events:**
- [EVENT_1]
- [EVENT_2]
- [EVENT_3]

**NPCs Met:**
- [NPC_1]: [ROLE]
- [NPC_2]: [ROLE]

**Faction Changes:**
- [FACTION]: [+/- REP CHANGE]

**Skills Checks Planned:**
- [SKILL] DC 12 (Social encounter)
- [SKILL] DC 14 (Investigation)

**Loot Awarded:**
- [GOLD] gp
- [ITEM_1] (if quest item, mark here)

**Clues Revealed:**
- [CLUE_1] (hints at conspiracy)
- [CLUE_2] (establishes faction conflict)

---

### Session 2: [SESSION_2_NAME]
**Goal:** [SESSION_GOAL]  
**Level:** 5  
**Encounters:** [NUM]  
**Node Range:** NODE_011 to NODE_025 (~15 nodes)  
**Key Events:**
- [EVENT_1]
- [EVENT_2]
- [EVENT_3]

**Companion Milestone:**
- [COMPANION_1] First Meeting (Approval starts at -10)

**Faction Changes:**
- [FACTION_1]: [+5] (party helps faction member)
- [FACTION_2]: [-5] (party ignores faction request)

**Skills Checks Planned:**
- [SKILL] DC 13 (Companion recruitment)
- [SKILL] DC 15 (High-stakes negotiation)

**Variable Initialization (For outline/implement):**
- `conspiracy_first_hint`: false → true
- `[COMPANION_1]_recruited`: false
- `[COMPANION_1]_approval`: -10

---

### Session 3: [SESSION_3_NAME]
**Goal:** [SESSION_GOAL]  
**Level:** 5  
**Encounters:** [NUM]  
**Node Range:** NODE_026 to NODE_045 (~20 nodes)  
**Key Events:**
- [EVENT_1]
- [EVENT_2]
- [EVENT_3]

**Major Combat Encounter:**
- Enemy Type: [TYPE]
- CR: [CR] (should be Medium or Hard for party level 5)
- Loot: [GOLD] gp, [ITEM]

**Faction Changes:**
- [FACTION]: [+/- REP]

**Skills Checks Planned:**
- [SKILL] DC 12 (x3)
- [SKILL] DC 14 (x2)

---

### Session 4: [SESSION_4_NAME]
**Goal:** [SESSION_GOAL]  
**Level:** 5  
**Encounters:** [NUM]  
**Node Range:** NODE_046 to NODE_065 (~20 nodes)  

**Companion Milestone:**
- [COMPANION_2] Introduced (Recruitment option appears)

**Faction Changes:**
- Multiple factions react to party's choices in Session 3

**Investigation Milestone:**
- Conspiracy becomes clearer (player has identified [N] conspirators)

---

### Session 5: [SESSION_5_NAME] — ACT 1 CLIMAX
**Goal:** [SESSION_GOAL]  
**Level:** 5  
**Encounters:** [NUM] (should include significant combat or social confrontation)  
**Node Range:** NODE_066 to NODE_085 (~20 nodes)  

**Act 1 Climax Event:**
- [CLIMAX_DESCRIPTION]

**Major Combat Encounter:**
- Boss-type enemy (CR 4-5)
- High-stakes skill checks (multiple DC 14-16 options)

**Variable State After Act 1:**
- `conspiracy_discovered`: true or false (depends on player choices)
- `[COMPANION_1]_recruited`: true or false
- `[COMPANION_2]_met`: true
- Major faction alignments established

**Ending Gates After Act 1:**
- At least 3 of 7 endings should be impossible (locked by party choices)
- At least 3 of 7 endings should be possible

**XP After Act 1:**
- Total XP gained: ~[XP_TOTAL]
- Party Level: Still 5 (or 6 if ahead of schedule)

---

## III. ACT 2: [ACT_2_NAME] — Sessions 6-10

**Act Goal:** [OBJECTIVE]

**Starting State (Act 2):**
- Party Level: 6 (or 5 if behind)
- Companions: [COMPANIONS_RECRUITED_SO_FAR]
- Factions: [CURRENT_REP_STATE]

---

### Session 6: [SESSION_6_NAME]
**Goal:** [SESSION_GOAL]  
**Level:** 6  
**Encounters:** [NUM]  
**Node Range:** NODE_086 to NODE_105 (~20 nodes)  

**Key Events:**
- [EVENT_1]
- [EVENT_2]
- [EVENT_3]

**Faction Pressure:**
- Multiple factions demand party commitment
- Reputation gates start to lock out endings

**Companion Milestone:**
- [COMPANION_2] Recruitment window (approval -10 to +20)
- Or [COMPANION_3] First meeting

---

### Session 7: [SESSION_7_NAME]
**Goal:** [SESSION_GOAL]  
**Level:** 6  
**Encounters:** [NUM]  
**Node Range:** NODE_106 to NODE_130 (~25 nodes)  

**Major Encounter Type:** [COMBAT/SOCIAL/EXPLORATION]

**Variable Tracking Needed:**
- Which faction is party aligned with?
- How many companions recruited? (expect 1-2 by now)
- Conspiracy revelation level (identified [N] conspirators)

---

### Session 8: [SESSION_8_NAME]
**Goal:** [SESSION_GOAL]  
**Level:** 6  
**Encounters:** [NUM]  
**Node Range:** NODE_131 to NODE_150 (~20 nodes)  

**Companion Milestone:**
- [COMPANION_3] Recruitment opportunity
- Or existing companion approval tests (faction vs. companion loyalty)

---

### Session 9: [SESSION_9_NAME]
**Goal:** [SESSION_GOAL]  
**Level:** 7  
**Encounters:** [NUM]  
**Node Range:** NODE_151 to NODE_170 (~20 nodes)  

**Major Combat Encounter:**
- Boss-type enemy (CR 6)
- Significantly higher stakes than Act 1

---

### Session 10: [SESSION_10_NAME] — ACT 2 CLIMAX
**Goal:** [SESSION_GOAL]  
**Level:** 7  
**Encounters:** [NUM] (climactic)  
**Node Range:** NODE_171 to NODE_190 (~20 nodes)  

**Act 2 Climax Event:**
- [CLIMAX_DESCRIPTION]
- Major revelation or choice point

**Variable State After Act 2:**
- All companions should be recruited or locked out
- Faction alignments mostly decided
- Only 2-3 endings still viable

**Ending Gates After Act 2:**
- At least 5 of 7 endings locked out
- Only 2-3 ending paths remain open

**XP After Act 2:**
- Total cumulative XP: ~[XP_TOTAL]
- Party Level: 7

---

## IV. ACT 3: [ACT_3_NAME] — Sessions 11-15

**Act Goal:** [OBJECTIVE]

**Starting State (Act 3):**
- Party Level: 7
- All companions recruited or permanently unavailable
- Factions: Clear alignments established
- Endings: Only 2-3 viable paths

---

### Session 11: [SESSION_11_NAME]
**Goal:** [SESSION_GOAL]  
**Level:** 7  
**Encounters:** [NUM]  
**Node Range:** NODE_191 to NODE_210 (~20 nodes)  

**Key Events:**
- Consequences of Act 2 climax become clear
- Final confrontation begins to take shape

---

### Session 12: [SESSION_12_NAME]
**Goal:** [SESSION_GOAL]  
**Level:** 7  
**Encounters:** [NUM]  
**Node Range:** NODE_211 to NODE_230 (~20 nodes)  

---

### Session 13: [SESSION_13_NAME]
**Goal:** [SESSION_GOAL]  
**Level:** 8  
**Encounters:** [NUM]  
**Node Range:** NODE_231 to NODE_250 (~20 nodes)  

**Major Combat Encounter:**
- Penultimate boss (CR 7-8)

---

### Session 14: [SESSION_14_NAME]
**Goal:** [SESSION_GOAL]  
**Level:** 8  
**Encounters:** [NUM]  
**Node Range:** NODE_251 to NODE_270 (~20 nodes)  

**Final Preparations:**
- Last chance for companion bonding
- Final faction choices
- Setup for ending sequence

---

### Session 15: [SESSION_15_NAME] — FINAL SESSION & ENDING
**Goal:** Resolve campaign  
**Level:** 8  
**Encounters:** [NUM] (should include final boss)  
**Node Range:** NODE_271 to NODE_290 (~20 nodes)  

**Final Boss Encounter:**
- Primary antagonist (CR 8-9)
- Multiple difficulty options (can be bypassed with diplomacy)

**Ending Sequence:**
- Node 280-290: Epilogue branching based on:
  - `ending_type` (one of 7)
  - `companions_alive`: which companions survived
  - `faction_alignment`: which factions favor the party
  - `world_state`: major consequences

**Final Variable State (For Epilogue):**
```
- ending_type: "Just_Ruler" | "Shadow_Broker" | "Redemption" | etc.
- thorne_alive: true/false
- sister_mercy_alive: true/false
- kael_alive: true/false
- guard_rep: final value
- syndicate_rep: final value
- temple_rep: final value
- party_gold: total accumulated
- conspirators_caught: count
- world_state_changed: true (irreversible changes made)
```

---

## V. Node Distribution Summary

| Act | Sessions | Nodes | Avg/Session | Encounters | Major Skill Checks |
|-----|----------|-------|-------------|------------|-------------------|
| 1 | 1-5 | 001-085 | 17 | 5-7 | 15-20 |
| 2 | 6-10 | 086-190 | 21 | 6-8 | 20-25 |
| 3 | 11-15 | 191-290 | 20 | 7-9 | 25-30 |
| **TOTAL** | **15** | **001-290** | **~19** | **18-24** | **60-75** |

---

## VI. Skill Check Distribution (Prepared for Outline/Implement)

**Expected Skill Checks Per Session:** 4-6

**DC Progression by Level:**
| Party Level | Common DC | Hard DC | Impossible DC |
|---|---|---|---|
| 5 | 12 | 14-15 | 18+ |
| 6 | 12-13 | 15-16 | 19+ |
| 7 | 13-14 | 16-17 | 20+ |
| 8 | 14-15 | 17-18 | 20+ |

**Skill Frequency:**
- Charisma (Persuasion/Deception): ~30%
- Wisdom (Insight/Perception): ~25%
- Intelligence (Investigation/Arcana): ~20%
- Strength (Athletics/Intimidation): ~15%
- Dexterity (Stealth/Acrobatics): ~10%

---

## VII. Companion Approval Timeline

| Companion | Session Met | Session Recruited | Approval Start | Act 1 Goal | Act 2 Goal | Act 3 Goal |
|---|---|---|---|---|---|---|
| [COMPANION_1] | 2 | 2-3 | -10 | 0+ (neutral) | 30+ (warm) | 60+ (romance option) |
| [COMPANION_2] | 4 | 5-6 | 0 | 10+ (positive) | 40+ (friendly) | 70+ (romance option) |
| [COMPANION_3] | 6 | 7-8 | -5 | 5+ (neutral) | 35+ (friendly) | 65+ (romance option) |

**Approval Events Per Session:** 2-4 (based on choices)

---

## VIII. Faction Reputation Arc

| Faction | Start | End of Act 1 | End of Act 2 | End of Act 3 | Ending Gate |
|---|---|---|---|---|---|
| [FACTION_1] | +20 | +25 to -10 (depends on choices) | +30 to -30 | Final alignment | >50 = ending A |
| [FACTION_2] | 0 | +10 to -5 | +20 to -20 | Final alignment | >70 = ending B |
| [FACTION_3] | +10 | +15 to 0 | +25 to -10 | Final alignment | >60 = ending C |

**Reputation Change Events:** 4-6 per session (based on player choices/skill checks)

---

## IX. Ending Gates Matrix (Prepared for Consequences Check)

| Ending | Requirements | Locked After | Factions Required | Companions |
|---|---|---|---|---|
| Just Ruler | guard_rep > 50 && temple_rep > 60 && syndicate_rep < 20 | Session 8 | Guard +, Temple + | Any except [COMPANION_1] |
| Shadow Broker | syndicate_rep > 70 && guard_rep < 0 | Session 9 | Syndicate + | [COMPANION_1] alive |
| Redemption | temple_rep > 60 && sister_mercy_alive && charisma > 12 | Session 10 | Temple + | [COMPANION_2] |
| Revolution | thorne_recruited && thorne_approval > 80 && guard_rep < -20 | Session 8 | Guard - | [COMPANION_1] + |
| Power Void | syndicate_dead && guard_weakened | Session 12 | Custom | Any |
| Tragedy | [failing_condition] | Always possible | Any | Any (but tragic) |
| Pyrrhic Victory | [achieved_but_costly] | Session 11 | Custom | Any alive |

---

## X. Variables to Initialize (For speckit.outline)

### Ability Scores (Set once at campaign start)
```
player_strength_mod: [N]
player_dexterity_mod: [N]
player_constitution_mod: [N]
player_intelligence_mod: [N]
player_wisdom_mod: [N]
player_charisma_mod: [N]
```

### Companion State
```
thorne_recruited: false
thorne_approval: -10
thorne_alive: true

sister_mercy_recruited: false
sister_mercy_approval: 20
sister_mercy_alive: true

kael_recruited: false
kael_approval: 0
kael_alive: true
```

### Faction State
```
guard_rep: 20
temple_rep: 10
syndicate_rep: 0
merchant_rep: 5
```

### Plot Flags
```
conspiracy_discovered: false
conspiracy_depth: 0
conspirators_identified: 0
conspirators_caught: 0
conspirators_dead: 0
```

### Session Tracking
```
current_session: 1
current_level: 5
party_gold: 0
party_xp: 0
```

---

## XI. Encounter Master List (Prepared for Mechanics Check)

**Session 1 Encounters:**
- [ENCOUNTER_1]: [TYPE], CR [N], [LOOT]
- [ENCOUNTER_2]: [TYPE], CR [N], [LOOT]

**Session 2 Encounters:**
- [ENCOUNTER_1]: [TYPE], CR [N], [LOOT]

[... Complete list for all 15 sessions ...]

**Boss Encounters:**
- Act 1 Climax Boss: [NAME], CR 4, unique loot
- Act 2 Climax Boss: [NAME], CR 6, unique loot
- Act 3 Final Boss: [NAME], CR 8-9, legendary loot

---

## XII. Critical Checkpoints (For speckit.continuity Validator)

**After Each Act, Verify:**
- [ ] Companion approval states are consistent across all branches
- [ ] Faction reputation changes are cumulative and consistent
- [ ] No dead-end quest items (all quest items reachable)
- [ ] At least one ending path remains viable
- [ ] NPC knowledge states are accurate ("who knows what by when?")
- [ ] Skill check DCs scale appropriately with party level

---

## XIII. Play-Testing Checkpoints

**Session 3 Check:**
- Is conspiracy hint clear enough?
- Are skill checks feeling fair?
- Do companions feel distinct?

**Session 8 Check:**
- Are faction conflicts compelling?
- Have at least 2 companions been recruited?
- Are multiple endings still viable?

**Session 13 Check:**
- Is final confrontation building tension?
- Are player choices creating meaningful consequences?
- Do endings feel earned?

---

## XIV. Next Steps (What This Plan Enables)

**Once plan is approved:**

1. **speckit.outline --all**
   - Uses node range (NODE_001-NODE_290) from this plan
   - Uses encounter list from Section XI
   - Uses session breakdown from Sections II-IV
   - Creates beat sheet for each node

2. **speckit.implement --all**
   - Uses companion approval arc from Section VII
   - Uses faction reputation timeline from Section VIII
   - Uses skill check distribution from Section VI
   - Drafts NPC dialogue with proper tone/flavor

3. **speckit.consequences**
   - Validates ending gates from Section IX
   - Checks reputation changes cascade correctly
   - Verifies multiple endings remain viable

4. **speckit.compile --engine ink**
   - Ready to export to Ink for Unity

---

**Plan Status:** [DRAFT / APPROVED / READY FOR OUTLINE]

**Total Nodes Planned:** ~290  
**Total Sessions:** 15  
**Estimated Playtime:** ~45 hours  

**Last Updated:** [DATE]
