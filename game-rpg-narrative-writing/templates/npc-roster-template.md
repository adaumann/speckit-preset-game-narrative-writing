# NPC Roster Template

## Quick-Reference NPC Index

This document provides a quick-lookup table for all NPCs in your campaign or game. For detailed character profiles, refer to individual character files in `characters/`.

---

## How to Use This Template

**For Tabletop RPG:**
- Use the table to track combat stats, faction affiliations, and quest hooks at a glance
- Print/reference during session prep for quick NPC lookup
- Track companion approval ranges for recruitment and ending gates
- Use "Reputation Impact" column to see faction consequences of NPC interactions

**For Computer Game:**
- Use the table to track dialogue node counts, quest integration, and recruitment paths
- Identify which NPCs appear in which quests
- Reference voice actor and dialogue type for implementation notes
- Track approval ranges for relationship/romance gating

---

## Tabletop NPC Roster

| NPC Name | Role/Title | Primary Location | Faction Affiliation | Quest Hooks | Combat Stats | Recruitable Companion? | Reputation Impact | Special Notes |
|----------|-----------|------------------|-------------------|------------|-------------|----------------------|------------------|----------------|
| [Name] | [Position] | [Location node] | [Faction name] | [Quest 1, Quest 2] | [AC / HP / Attack] | [Yes/No, Approval range] | [Faction: ±X if hired/killed/helped] | [Key personality trait or plot role] |
| [Name] | [Position] | [Location node] | [Faction name] | [Quest 1, Quest 2] | [AC / HP / Attack] | [Yes/No, Approval range] | [Faction: ±X if hired/killed/helped] | [Key personality trait or plot role] |
| [Name] | [Position] | [Location node] | [Faction name] | [Quest 1, Quest 2] | [AC / HP / Attack] | [Yes/No, Approval range] | [Faction: ±X if hired/killed/helped] | [Key personality trait or plot role] |

---

## Example (Tabletop)

| NPC Name | Role/Title | Primary Location | Faction Affiliation | Quest Hooks | Combat Stats | Recruitable Companion? | Reputation Impact | Special Notes |
|----------|-----------|------------------|-------------------|------------|-------------|----------------------|------------------|----------------|
| Thorn | Bartender / Information Broker | Drunken Griffin | Thieves Guild (neutral contact) | "Local Jobs," "The Favor" | AC 12, HP 18, Dagger +3 | No | TG: +5 if helped, -10 if betrayed | Knowledgeable about underworld; deaf in left ear (uses sign language backup) |
| Marta Vex | Thieves Guild Master / Rogue Companion | Drunken Griffin / Hidden Market | Thieves Guild | "The Thief's Debt," "The Vault Job" | AC 14, HP 27, Rapier +4, Stealth +6 | Yes, Rogue (-100 to +100) | TG: +15 to +25 per quest outcome | Can be recruited after Quest 1; romance subplot if ≥75 approval |
| Captain Harren | City Guard Captain | Guard House / Patrols | Guard House | "Missing Shipment," "Corruption Exposed" | AC 18, HP 45, Longsword +6, Command | No | GH: +10 if helped, -30 if opposed | By-the-book lawman; conflicted about corrupt superiors; redeemable |
| Lyssa Nightshadow | Ranger Scout / Ranger Companion | Wilderness / Ranger Camp | Ranger Order | "Monster Hunt" (chain), "Wilderness Pact" | AC 16, HP 35, Longbow +5, Survival +7 | Yes, Ranger (-100 to +100) | RO: +5 to +40 per hunt success | Quiet, prefers action; strong tracker; protective of wilds |
| Kess the Sage | Retired Wizard / Lore NPC | Sage's Tower | Mage College | "Ancient Texts," "Spell Research" | AC 13, HP 22, Staff +2 (spell), Arcana +8 | No (disabled, uses staff as mobility aid) | MC: +15 if helped, -20 if grimoire stolen | Extensive knowledge; accessibility note: uses ASL interpreter when visiting cities |

---

## Computer Game NPC Roster

| NPC Name | NPC Type | Quest Count | Primary Dialogue Nodes | AI Behavior | Recruitment | Voice Actor | Approval Range | Special Integration |
|----------|----------|------------|----------------------|------------|------------|------------|----------------|----------------------|
| [Name] | [Companion / Ally / Antagonist / Quest-Giver / Vendor / Other] | [# quests] | [NODE-#### refs] | [Combat / Stealth / Support / Evasive / Tactical] | [Recruitble / Locked ally / Hostile / Optional] | [Actor name or TBD] | [-100 to +100, or N/A] | [Romance? Can betray? Multiple recruitment paths?] |
| [Name] | [Companion / Ally / Antagonist / Quest-Giver / Vendor / Other] | [# quests] | [NODE-#### refs] | [Combat / Stealth / Support / Evasive / Tactical] | [Recruitble / Locked ally / Hostile / Optional] | [Actor name or TBD] | [-100 to +100, or N/A] | [Romance? Can betray? Multiple recruitment paths?] |
| [Name] | [Companion / Ally / Antagonist / Quest-Giver / Vendor / Other] | [# quests] | [NODE-#### refs] | [Combat / Stealth / Support / Evasive / Tactical] | [Recruitble / Locked ally / Hostile / Optional] | [Actor name or TBD] | [-100 to +100, or N/A] | [Romance? Can betray? Multiple recruitment paths?] |

---

## Example (Computer Game)

| NPC Name | NPC Type | Quest Count | Primary Dialogue Nodes | AI Behavior | Recruitment | Voice Actor | Approval Range | Special Integration |
|----------|----------|------------|----------------------|------------|------------|------------|----------------|----------------------|
| Kael (Warrior) | Companion | 4 | NODE-1002 (recruitment), 1045, 2030, 3100 | Combat-focused aggressor, charges enemies | Recruitable at NODE-1015 (tavern encounter) | James Chen | -100 to +100 | Can betray party in Act 2 if approval < -50; strong ending if ≥75 |
| Riana (Rogue) | Companion | 5 | NODE-1005 (recruitment), 1050, 2015 (personal quest), 3020, 4080 (final scene) | Stealth-first, quips during dialogue | Recruitable at NODE-1008 (night heist) | Maria Lopez | -100 to +100 | Romance option if ≥75 approval; "Lost Amulet" personal quest unlocks at approval ≥10 |
| Thora (Scholar) | Companion | 3 | NODE-1010 (recruitment), 2050, 3150 | Support caster, suggests alternate solutions | Recruitable at NODE-1020 (library) | Sarah Khan | -100 to +100 | Can provide lore hints; betrays if approval < -75; best ending if research completed |
| Elder Grimm | NPC (Mentor/Quest-Giver) | 7 | NODE-1100 through NODE-7100 (one per act) | Cryptic, offers wisdom not direct answers | Not recruitable (permanent NPC guide) | David Liu | N/A (NPC-only) | Appears at major story beats; dialogue changes based on player choices; alternate ending if befriended |
| Shadowmaster | Antagonist | 0 | NODE-3500 (confrontation 1), NODE-4500 (confrontation 2), NODE-5500 (final) | Ruthless, tactical, uses minions | Locked hostile (secret recruitment path if approval ≥80 via hidden dialogue, NODE-5500-SECRET) | Unknown (hidden identity) | -100 (locked hostile) | Secret recruitment transforms ending; can become ally for post-game content |
| Merchant Iris | Vendor / Quest-Giver | 2 | NODE-2100 (shop), NODE-2105 (fetch quest) | Neutral, business-focused, witty | Vendor (always available after first encounter) | Amanda Wong | N/A (reputation-based, not approval) | Merchant rank increases: Standard → Premium stock → Unique items at quest completion |

---

## NPC Categories

### Recruitable Companions (Tabletop)

**Definition:** NPCs who can join the party in combat/adventures and have personal arcs.

**Tracking Elements:**
- **Approval Range:** -100 to +100 typically
- **Recruitment Condition:** What must happen for party to recruit this companion?
- **Breakup Points:** At what approval do they leave permanently?
- **Romance Gate:** If applicable, at what approval does romance unlock?
- **Ending Influence:** Can this companion's ending be affected by quest completion / approval?
- **Betrayal Path:** Can they betray the party? Under what conditions?

### Quest-Giver NPCs (Both)

**Definition:** NPCs who initiate quests or provide major story direction.

**Tracking Elements:**
- **Quest Chain:** What quests does this NPC offer? In what order?
- **Gating:** What reputation or conditions unlock their quests?
- **Dialogue Variations:** Do their quest offers change based on player choices?
- **Reward Control:** Do they control reward amounts or faction rep changes?

### Antagonists/Opposition (Both)

**Definition:** NPCs who oppose the party or represent opposing forces.

**Tracking Elements:**
- **Hostility Level:** Permanently hostile? Can be befriended? Secret alliance?
- **Minion Command:** Do they control other enemies? How many?
- **Redemption Path:** Is there a quest chain to redeem them?
- **Defeat Consequences:** Does defeating them affect faction relations?

### Faction Leaders (Tabletop focus)

**Definition:** NPCs who represent major factions and control faction mechanics.

**Tracking Elements:**
- **Reputation Gates:** What approval thresholds unlock faction benefits?
- **Quest Authority:** Do they command faction-specific quests?
- **Ending Impact:** Can faction leader choices affect ending states?
- **Betrayal Consequences:** What happens if party betrays their faction?

### Ally NPCs (Non-Recruitable)

**Definition:** NPCs who support the party but don't join actively.

**Tracking Elements:**
- **Support Type:** Do they provide resources / information / shelter / magic?
- **Availability:** When/where can party contact them?
- **Cost:** Is their help free or does it have faction/approval consequences?
- **Limitations:** Can they assist in certain situations only?

---

## Design Notes

**NPC Distribution:**
[How many total NPCs are in your campaign? How are they distributed across factions/locations?]

**Naming Conventions:**
[Do NPCs follow a naming pattern by culture/faction? Accessibility note: are names pronounceable?]

**Accessibility:**
[Any NPCs with disabilities or non-standard representations? How are they portrayed?]

**Voice Acting:**
[If applicable, which NPCs need professional voice acting vs. text-only?]

**Relationship Web:**
[Do NPCs have relationships with each other? Conflicts? Alliances?]
