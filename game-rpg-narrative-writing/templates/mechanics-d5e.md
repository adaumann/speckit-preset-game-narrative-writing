---
title: "[CAMPAIGN_NAME] Mechanic Hooks Configuration"
template: "mechanics-d5e"
game_system: "D&D 5e"
---

# [CAMPAIGN_NAME] — Mechanic Hooks Configuration

D&D-specific configuration for all 8 mechanic hooks used in the campaign. Referenced during `speckit.outline` for hook validation and `speckit.compile` for engine translation.

---

## How to Use This Template: Examples vs. Customization

**This template shows examples from a conspiracy investigation campaign.** You should customize every section for your campaign theme.

### Why Examples Are Included

Each section includes:
1. **SAMPLE concrete examples** (evidence_ledger, guard_captain, temple_key, etc.)
2. **ALTERNATIVE patterns** showing how AI creates similar mechanics for other campaigns
3. **YOUR CAMPAIGN section** where you fill in your own items, NPCs, factions

### How AI Creates Alternatives

When you ask Spec Kit AI to generate mechanics for a different campaign:

**For different campaign themes, AI creates:**
- **Monster Hunt:** Replaces "conspiracy" with "monster sighting", evidence with "monster signs", NPCs with "hunters/scholars"
- **Heist Campaign:** Replaces "investigation" with "planning phase", items with "blueprints/access cards", NPCs with "crew members"
- **Political Intrigue:** Replaces "conspiracy" with "scandal/betrayal", evidence with "letters/documents", NPCs with "nobility/spies"
- **Curse Breaking:** Replaces "evidence gathering" with "component collection", items with "ritual objects/ancient tomes", NPCs with "sages/priests"

**The pattern stays the same:**
- One primary investigation goal (conspiracy, monster threat, heist objective, curse)
- 3-5 quest items that progress the investigation
- 1-3 key ally NPCs that can be recruited
- 3-4 major factions with competing interests
- Multiple endings based on which factions you've aligned with

### How to Generate Your Own

In `speckit.constitution`, select your campaign template (if available):
1. **speckit.plan** → Uses constitution to create session structure
2. **speckit.outline** → Uses plan to generate node beats
3. When hooks needed, **AI creates YOUR theme's hooks** by:
   - Replacing conspiracy with YOUR investigation goal
   - Replacing factions with YOUR power structures
   - Creating quest items matching YOUR theme
   - Generating NPC allies for YOUR setting

---

## Overview: What Are Mechanic Hooks?

Mechanic hooks are narrative-to-game bridges—they connect story decisions to mechanical consequences. When a player makes a choice in dialogue (narrative layer), a hook triggers a mechanical effect (game layer).

**Spec Kit Hook Categories:**
1. **flag** — Binary story states (did conspiracy get discovered?)
2. **counter** — Numeric values that can increment/decrement (faction reputation)
3. **visited** — Track if player has been somewhere (which locations)
4. **inventory** — Items acquired and used (quest items)
5. **timer** — Countdown mechanics (session deadlines)
6. **trust** — NPC relationship tracking (companion approval)
7. **currency** — Gold and wealth management
8. **npc_state** — NPC status and conditions

---

## I. FLAG Hooks

Mechanics: Binary story states that enable/disable branches.

**SAMPLE CAMPAIGN PATTERN:** Examples below show a conspiracy investigation campaign. For your campaign, substitute placeholders with your own plot drivers:
- Conspiracy investigation → Monster hunt, Prophecy discovery, Artifact retrieval, Murder mystery, Political scandal, etc.
- Guard/Temple/Syndicate factions → Your three rival power structures
- Guard Captain NPC → Your key ally/informant character

### Investigation Progression Flags (SAMPLE: Conspiracy Investigation Theme)

**Example below uses conspiracy investigation. Create YOUR investigation goal flags following this pattern:**

```
flag:[INVESTIGATION_GOAL]_discovered
  Name: "[INVESTIGATION_GOAL] Discovered"
  Default: false
  Trigger: At NODE-040 (major evidence accumulation)
  Effect: Unlocks all investigation-related dialogue options
  Narrative Consequence: All NPCs react differently based on knowledge
  Revert Possible: No (one-way state change)
  Validation: Must trigger between Session 3-4
  
  YOUR CAMPAIGN ALTERNATIVES:
  - flag:dragon_sighting_confirmed (Monster hunt: Dragon discovered)
  - flag:prophecy_translated (Mystical: Prophecy understood)
  - flag:artifact_unearthed (Heist: Artifact location found)
  - flag:murderer_identified (Mystery: Killer identified)
  
flag:[INVESTIGATION_GOAL]_resolved
  Name: "[INVESTIGATION_GOAL] Resolved"
  Default: false
  Trigger: After defeating final obstacle or collecting all evidence
  Effect: Locks discovery nodes, unlocks resolution nodes
  Narrative Consequence: World visibly changes (threat/mystery diminished)
  Revert Possible: No
  Validation: Must trigger before Session 15 for any ending
  
  YOUR ALTERNATIVES:
  - flag:dragon_slain (Monster defeated)
  - flag:prophecy_fulfilled (Prophecy completed)
  - flag:artifact_secured (Artifact acquired)
  - flag:murderer_brought_to_justice (Killer caught)
  
flag:[INVESTIGATION_GOAL]_exposed_publicly
  Name: "[INVESTIGATION_GOAL] Public Knowledge"
  Default: false
  Trigger: At NODE-200 (party chooses to reveal publicly vs. secretly)
  Effect: Dialogue tone shifts to public scandal/crisis instead of secret
  Narrative Consequence: Faction alignments shift (public pressure)
  Revert Possible: No
  Validation: Choose reveal vs. secret routes at Act 2 climax
```

### Key Ally/Informant Recruitment (SAMPLE: Guard Captain Pattern)

**Example: Guard Captain as informant/ally. Your campaign alternatives:**
- Merchant guild leader, Rebel commander, Cursed noble, Ancient spirit, Ex-convict, Street urchin, etc.

```
flag:key_ally_converts
  Name: "[KEY_ALLY] Confesses/Cooperates"
  Default: false
  Trigger: At NODE-015 (successful persuasion check DC 14)
  Effect: Direct evidence, major reputation boost with aligned faction
  Narrative Consequence: [KEY_ALLY] becomes available for recruitment
  Revert Possible: No
  Validation: Failing check allows retry but with harder DC
  
  YOUR ALTERNATIVES:
  - flag:merchant_guild_master_betrays_guild (Insider trading)
  - flag:rebel_commander_joins_cause (Political defection)
  - flag:cursed_noble_reveals_curse_origin (Mystical revelation)
  - flag:street_informant_trusts_party (Trust building)
  
flag:key_ally_recruited
  Name: "[KEY_ALLY] Joins Party"
  Default: false
  Trigger: At NODE-020 (if cooperated, offer recruitment)
  Effect: [KEY_ALLY] becomes active ally NPC
  Narrative Consequence: Brings faction perspective to all future dialogue
  Revert Possible: No (once recruited, permanent unless dies or betrays)
  Validation: Only available if converted; blocks other ally recruitment
  
  IMPLEMENTATION: AI can create multiple ally patterns—see values for how many are available per campaign tier
```

### Companion Recruitment Flags

```
flag:companion_1_recruited
  Name: "[COMPANION_1_NAME] Recruited"
  Default: false
  Trigger: At NODE-025 (recruitment climax for [COMPANION_1_NAME])
  Effect: `thorne_recruited = true`, `thorne_in_party = true`
  Narrative Consequence: [COMPANION_1_NAME] appears in all subsequent dialogue options
  Revert Possible: No (can die, but not un-recruit)
  Validation: Prerequisite: Must have met [COMPANION_1_NAME] and approval > -20
  
flag:companion_2_recruited
  Name: "[COMPANION_2_NAME] Recruited"
  Default: false
  Trigger: At NODE-045 (recruitment climax for [COMPANION_2_NAME])
  Effect: `sister_mercy_recruited = true`, `sister_mercy_in_party = true`
  Narrative Consequence: [COMPANION_2_NAME] provides faction perspective
  Revert Possible: No
  Validation: Prerequisite: Faction alignment required
  Validation: Prerequisite: temple_rep > 0
  
flag:companion_3_recruited
  Name: "[COMPANION_3_NAME] Recruited"
  Default: false
  Trigger: At NODE-070 (recruitment climax for [COMPANION_3_NAME])
  Effect: `kael_recruited = true`, `kael_in_party = true`
  Narrative Consequence: [COMPANION_3_NAME] offers unique perspective
  Revert Possible: No
  Validation: No strict prerequisite, recruits last
```

### Companion Death Flags

```
flag:companion_1_alive
  Name: "[COMPANION_1_NAME] Still Alive"
  Default: true
  Trigger: At NODE-150 (if major combat goes badly) or NODE-280 (final choice)
  Effect: If false, disables all [COMPANION_1_NAME] dialogue
  Narrative Consequence: Alternate companion perspectives replace [COMPANION_1_NAME]
  Revert Possible: No
  Validation: Can die in combat, can choose sacrifice, can be executed
  
flag:companion_2_alive
  Name: "[COMPANION_2_NAME] Still Alive"
  Default: true
  Trigger: Similar to [COMPANION_1_NAME]
  Effect: If false, disables key companion questline possibility
  Narrative Consequence: Faction loses main advocate
  Revert Possible: No
  Validation: Death can block specific ending path
  
flag:companion_3_alive
  Name: "[COMPANION_3_NAME] Still Alive"
  Default: true
  Trigger: Similar to other companions
  Effect: If false, affects companion availability
  Narrative Consequence: Limits economic leverage in final acts
  Revert Possible: No
  Validation: Can survive with any ending
```

### Faction Status Flags

```
flag:guard_weakened
  Name: "Guard Weakened or Dismantled"
  Default: false
  Trigger: After major Guard setback (NODE-180 or later)
  Effect: Guard soldiers appear less frequently, authority questioned
  Narrative Consequence: Other factions become more visible
  Revert Possible: No
  Validation: Blocks Just Ruler ending if true
  
flag:temple_corrupted
  Name: "Temple Leadership Compromised"
  Default: false
  Trigger: If conspirators infiltrate Temple (NODE-190)
  Effect: Temple NPCs act suspiciously or hostilely
  Narrative Consequence: Players can't fully trust Temple priests
  Revert Possible: Only if corruption is actively purged
  Validation: Blocks Redemption ending if true by Session 13
  
flag:syndicate_exposed
  Name: "Syndicate Identity Publicly Revealed"
  Default: false
  Trigger: If party broadcasts Syndicate involvement (NODE-210)
  Effect: Syndicate becomes openly hostile, reputation drops
  Narrative Consequence: Shadow Broker ending becomes impossible
  Revert Possible: No
  Validation: Choose to expose or protect Syndicate at Act 2 climax
```

---

## II. COUNTER Hooks

Mechanics: Numeric values that can increment/decrement based on choices.

### Reputation Counters

```
counter:guard_rep (Range: -100 to +100)
  Name: "Guard Faction Reputation"
  Default: 20
  Increment Events (by Session):
    Session 2: +5 (help Guard patrol)
    Session 3: +10 (capture conspirator)
    Session 5: +15 (prevent Guard assassination)
    Session 8: +5 (provide evidence)
  Decrement Events:
    Session 2: -5 (ignore Guard request)
    Session 4: -10 (help Syndicate instead)
    Session 6: -15 (expose Guard corruption)
  Gates:
    < -20: Revolution ending available
    > 50: Just Ruler ending available
    > 70: Can recruit Guard NPCs
  Validation: Never exceeds +100 or -100
  
counter:temple_rep (Range: -100 to +100)
  Name: "Temple Faction Reputation"
  Default: 10
  Increment Events:
    Session 1: +5 (help temple priest)
    Session 4: +10 (cleanse corrupted temple site)
    Session 6: +15 (defend against desecration)
    Session 10: +20 (become temple protector)
  Decrement Events:
    Session 2: -5 (desecrate temple)
    Session 5: -10 (side with syndicate against temple)
    Session 8: -15 (expose temple corruption)
  Gates:
    > 60: Redemption ending available
    > 70: Can access temple resources
  Validation: Must cross 0 during early acts
  
counter:syndicate_rep (Range: -100 to +100)
  Name: "Syndicate Faction Reputation"
  Default: 0
  Increment Events:
    Session 2: +10 (help with crime)
    Session 4: +15 (steal for syndicate)
    Session 6: +20 (eliminate syndicate rival)
    Session 8: +25 (join syndicate operations)
  Decrement Events:
    Session 3: -10 (report syndicate to guard)
    Session 5: -15 (steal from syndicate)
    Session 7: -20 (disrupt syndicate operation)
  Gates:
    > 70: Shadow Broker ending available
    < 0: Shadow Broker ending blocked
  Validation: Most volatile counter, most choice-dependent
```

### Investigation Counters

```
counter:conspirators_identified (Range: 0 to 10)
  Name: "Number of Conspirators Identified"
  Default: 0
  Increment Events:
    NODE-015: +1 (interrogate Guard Captain)
    NODE-030: +1 (find evidence ledger)
    NODE-040: +2 (locate meeting place)
    NODE-060: +1 (each additional conspirator identified)
  Gates:
    >= 3: Conspiracy investigation becomes critical path
    >= 5: Ending gates start to apply
    >= 8: Conspiracy can be fully dismantled
  Validation: Cannot exceed 10, represents known conspirators
  
counter:conspirators_caught (Range: 0 to 10)
  Name: "Number of Conspirators Defeated/Arrested"
  Default: 0
  Increment Events:
    NODE-050: +1 (defeat conspirator in combat)
    NODE-070: +1 (capture conspirator non-lethally)
    NODE-100: +2 (major arrest action)
  Decrement Events: (Conspirator escapes)
    NODE-110: -1 (if player lets conspir escape)
  Gates:
    >= 4: Tragic Defeat ending blocked
    >= 5: Justice-focused endings become viable
  Validation: Cannot exceed conspirators_identified
  
counter:conspirators_dead (Range: 0 to 10)
  Name: "Number of Conspirators Killed"
  Default: 0
  Increment Events:
    NODE-080: +1 (kill conspirator in combat)
    NODE-150: +1 (during major battle)
    NODE-200: +1 (final confrontation)
  Gates:
    >= 3: Pyrrhic Victory blocks some endings
    >= 5: Redemption ending becomes impossible
    >= 7: Revolution ending becomes impossible
  Validation: Cannot exceed conspirators_caught
```

### Combat & Resource Counters

```
counter:party_xp (Range: 0 to 50000+)
  Name: "Party Experience Points"
  Default: 0
  Increment Events:
    Combat: +100-300 per encounter (based on CR)
    Investigation: +50 per significant clue discovered
    Social: +50 per major NPC convinced
  Gates:
    6500: Level up to 6
    13500: Level up to 7
    23000: Level up to 8
  Validation: Controls party_level, used for encounter scaling
  
counter:party_gold (Range: 0 to 20000+)
  Name: "Party Accumulated Gold"
  Default: 0
  Increment Events:
    Combat loot: +50-200 per encounter
    Quest rewards: +100-500 per quest
    Theft: +50-300 (if stealing)
  Decrement Events:
    Equipment purchase: -10-200
    Bribes: -50-300
    Lodging: -10-30 per session
  Validation: No hard cap, affects ending flavor text
  
counter:party_total_damage_taken (Range: 0 to 1000+)
  Name: "Cumulative Party Damage"
  Default: 0
  Increment Events:
    Each combat: +damage_taken
  Gates:
    >= 100: Party showing strain (dialogue flavor)
    >= 300: Pyrrhic Victory ending becomes likely
  Validation: Represents party exhaustion level
```

---

## III. INVENTORY Hooks

Mechanics: Items acquired and used as story gates.

**SAMPLE CAMPAIGN PATTERN:** Examples show an investigation campaign (evidence ledger, temple key, etc.). Your campaign might feature:
- **Monster Hunt:** Monster heart, prophecy scroll, hunter's map, monster weaknesses
- **Heist:** Stolen artifact, access key, blueprints, buyer's contract
- **Political Intrigue:** Royal decree, secret letter, witness testimony, sealed envelope
- **Curse Breaking:** Curse object, mystical component, ritual ingredients, ancient tome

### Quest Items (SAMPLE: Investigation → Proof → Consequence Pattern)

```
inventory:evidence_ledger
  Name: "Conspiracy Evidence Ledger"
  Acquired: NODE-030 (investigate evidence room)
  Required To: NODE-040 (show evidence to Guard Captain)
  Consequences: +10 guard_rep, guard_captain_confesses = true
  Reusable: No (consumed/submitted at NODE-040)
  Alternative: Can be destroyed (blocks Justice ending)
  Validation: Must be acquirable; blocks certain ending paths if lost
  
  SAMPLE ALTERNATIVES (How AI Creates Options):
  - Monster heart: Acquired from dead monster → Show to alchemist → Recipe for monster antidote
  - Secret letter: Acquired from lover's room → Show to faction leader → Proof of affair/betrayal
  - Blueprint: Acquired from caravan → Study → Can bypass security DC 16 instead of 20
  - Curse object: Acquired from haunted location → Study with sage → Path to curse breaking
  
inventory:signet_ring
  Name: "Conspirator's Signet Ring"
  Acquired: NODE-015 (successful interrogation)
  Required To: NODE-050 (identify another conspirator)
  Consequences: Helps identify conspirator network
  Reusable: Yes (can show to multiple NPCs)
  Alternative: Can be destroyed (conspiracy remains hidden)
  Validation: First inventory item, teaches system
  
inventory:temple_key
  Name: "Temple Inner Sanctum Key"
  Acquired: NODE-080 (from [COMPANION_2_NAME] or theft)
  Required To: NODE-090 (access hidden temple chamber)
  Consequences: Discovers major faction evidence or trap
  Reusable: Yes (keeps key for future access)
  Alternative: Can pick lock instead (harder check)
  Validation: Enables mid-campaign faction questline
  
inventory:conspiracy_letter
  Name: "Conspiracy Leadership Letter"
  Acquired: NODE-140 (found in leadership hideout)
  Required To: NODE-180 (use letter to unite factions against conspiracy)
  Consequences: +15 guard_rep, +10 temple_rep, -5 syndicate_rep
  Reusable: No (letter destroyed when used)
  Alternative: Can keep secret (don't reveal)
  Validation: Acts as major turning point document
```

### Equipment with Narrative Effects

```
inventory:priestess_robes
  Name: "Priestess Robes (Disguise)"
  Acquired: NODE-085 (optional, borrow from [COMPANION_2_NAME])
  Effect: Allows dialogue branch impersonating faction priestess
  Consequences: Skill checks treated as if you're faction-aligned
  Reusable: Yes (return to [COMPANION_2_NAME])
  Alternative: Forgo disguise (face faction members openly)
  Validation: Optional for stealth-focused play
  
inventory:guard_insignia
  Name: "Guard Insignia (Uniform Component)"
  Acquired: NODE-050 (optional, reward from Guard)
  Effect: Allows dialogue branch impersonating guard
  Consequences: Faction guards are less hostile
  Reusable: Yes (can switch costumes)
  Alternative: No disguise (face all challenges openly)
  Validation: Optional for social stealth
  
inventory:syndicate_ring
  Name: "Syndicate Rank Ring"
  Acquired: NODE-110 (optional, join Syndicate or steal)
  Effect: Allows access to Syndicate facilities
  Consequences: Open Syndicate hideout doors, alternative dialogue
  Reusable: Yes
  Alternative: Force entry (combat required)
  Validation: Optional, but enables Shadow Broker ending path
```

### Consumable Counters

```
inventory:healing_potions
  Name: "Healing Potions (count)"
  Acquired: Purchased (50 gp each) or found in loot
  Default: 2 (starting)
  Restoration: +2 after each session (party finds/buys)
  Used In: Combat encounters (restores 20 HP)
  Validation: Infinite supply available for purchase
  
inventory:spell_scrolls
  Name: "Spell Scrolls (count)"
  Acquired: Found in loot or purchased (100 gp each)
  Default: 0
  Used In: Combat encounters (single use per scroll)
  Restoration: +1 per major loot acquisition
  Validation: Optional for specific combat strategies
```

---

## IV. COUNTER Hooks: Approval/Trust

Mechanics: NPC relationship tracking (-100 to +100 scale).

```
counter:companion_1_approval (Range: -100 to +100)
  Name: "[COMPANION_1_NAME] Approval"
  Default: -10 (initially distrustful)
  Increment Events:
    NODE-025: +15 (prove party's trustworthiness)
    NODE-050: +10 (help with companion's mission)
    NODE-100: +20 (major faction support)
    NODE-150: +10 (each session adventuring together)
  Decrement Events:
    NODE-030: -20 (betray companion's confidence)
    NODE-060: -15 (side with rival faction)
    NODE-120: -10 (ignore companion's advice)
  Romance Gate: >= 76 (enables romantic dialogue)
  Leaving Gate: <= -50 (companion leaves party)
  Ending Gate: >= 80 (enables specific ending path)
  Validation: Cannot exceed +100, can exceed -100 (causes abandonment)
  
counter:companion_2_approval (Range: -100 to +100)
  Name: "[COMPANION_2_NAME] Approval"
  Default: 20 (initially trusting)
  Increment Events:
    NODE-045: +15 (recruit for party)
    NODE-080: +20 (defend companion's faction)
    NODE-160: +15 (choose mercy over violence)
  Decrement Events:
    NODE-070: -15 (commit violence in front of companion)
    NODE-110: -20 (act against companion's values)
    NODE-140: -10 (ignore companion's moral advice)
  Romance Gate: >= 81 (enables romantic dialogue)
  Ending Gate: >= 50 (enables specific ending path)
  Validation: Reflects companion's core values
  
counter:companion_3_approval (Range: -100 to +100)
  Name: "[COMPANION_3_NAME] Approval"
  Default: 0 (neutral)
  Increment Events:
    NODE-070: +10 (recruit for party)
    NODE-090: +15 (support companion's interests)
    NODE-170: +20 (create opportunity for companion)
  Decrement Events:
    NODE-085: -15 (act against companion's interests)
    NODE-105: -10 (ignore companion's advice)
    NODE-180: -20 (sabotage companion's plans)
  Romance Gate: >= 81
  Validation: Reflects companion's core motivation
```

---

## V. VISITED Hooks

Mechanics: Track which locations party has visited (for consequence continuity).

```
visited:guard_headquarters
  Name: "Guard Headquarters"
  First Visit: NODE-008 (investigation begins)
  Consequence: Adds Guard investigation perspective
  Revisit Options: 5+ times (each visit potentially changes layout)
  Final State: Base of operations or ruined
  Validation: Core location, visited every 2-3 sessions
  
visited:temple_sanctuary
  Name: "Temple Inner Sanctum"
  First Visit: NODE-030 (first temple exploration)
  Consequence: Adds temple corruption knowledge
  Revisit Options: 3+ times
  Final State: Purified or still corrupted
  Validation: Optional for first visit (need key or lock pick)
  
visited:syndicate_hideout
  Name: "Syndicate Underground Hideout"
  First Visit: NODE-060 (if joining Syndicate path)
  Consequence: Commits player to Shadow Broker ending path
  Revisit Options: 5+ times
  Final State: Liberated or still active
  Validation: Optional, but gating Shadow Broker ending
  
visited:conspiracy_leadership_chamber
  Name: "Conspiracy Leadership Meeting Chamber"
  First Visit: NODE-140 (late discovery)
  Consequence: Reveals conspiracy structure
  Revisit Options: 2+ times (final battle)
  Final State: Destroyed or cleared
  Validation: Critical location for investigation climax
```

---

## VI. TIMER Hooks

Mechanics: Countdown events that create urgency.

```
timer:guard_investigation_deadline
  Name: "Guard's Investigation Deadline"
  Starts: Session 2 (NODE-012)
  Duration: 6 in-game days (approximately Session 5)
  Consequence: If conspiracy not exposed by deadline, Guard moves independently
  Effect: Reduces player agency (automatic Guard investigation begins)
  Restart Possible: No (one-way deadline)
  Validation: Creates mid-campaign pressure
  
timer:temple_ceremony_date
  Name: "Temple Ceremony Date"
  Starts: Session 4 (NODE-050)
  Duration: 4 in-game days (approximately Session 6)
  Consequence: If temple ceremony proceeds, templars take action
  Effect: Unlocks temple-specific quest line
  Restart Possible: No (ceremony happens once)
  Validation: Optional timer based on choices
  
timer:syndicate_operational_deadline
  Name: "Syndicate Operation Deadline"
  Starts: Session 6 (NODE-110)
  Duration: 3 in-game days (approximately Session 7)
  Consequence: If Syndicate plan not stopped/supported, it executes
  Effect: Major world state change (crime wave or new power structure)
  Restart Possible: No (deadline passes)
  Validation: Most consequential timer
```

---

## VII. CURRENCY Hooks

Mechanics: Gold accumulation and spending.

```
currency:party_gold
  Name: "Party Gold Pool"
  Default: 0
  Spending Categories:
    Equipment: 50-200 gp per item
    Bribes: 50-500 gp per NPC
    Lodging: 10-30 gp per session
    Carousing: 10-100 gp per leisure activity
  Acquisition:
    Combat Loot: 50-300 gp per encounter
    Quest Rewards: 100-500 gp per major quest
    Theft: 50-300 gp (risky)
    Faction Payments: 500-1000 gp (ending reward)
  Validation: Tracking wealth affects ending flavor text
  
currency:syndicate_protection_tax
  Name: "Syndicate Monthly Protection Tax"
  Paid To: Syndicate faction (if Shadow Broker ending path)
  Amount: 100 gp per in-game month
  Consequence: If not paid, Syndicate becomes hostile
  Effect: Ongoing cost of maintaining criminal empire
  Validation: Optional cost for Shadow Broker ending
```

---

## VIII. NPC_STATE Hooks

Mechanics: Track individual NPC conditions and relationships.

```
npc_state:guard_captain_status
  Name: "Guard Captain Status"
  Default: "enemy" (initially)
  States: "enemy" → "neutral" → "allied" → "recruited"
  Transitions:
    "neutral": If confessional dialogue (NODE-015)
    "allied": If party helps with faction quest
    "recruited": If party makes recruitment offer
  Consequences by State:
    "enemy": Guards attack on sight
    "neutral": Guards ignore party
    "allied": Guards provide assistance
    "recruited": Guard Captain available for dialogue/combat
  Validation: Required for Guard faction ending
  
npc_state:companion_2_wounded
  Name: "[COMPANION_2_NAME] Wounds (Post-Battle)"
  Default: "healthy"
  States: "healthy" → "wounded" → "recovering" → "healthy"
  Transitions:
    "wounded": After combat if damaged
    "recovering": If rested/healed
    "healthy": After 2-3 sessions
  Consequences:
    "wounded": Companion sits out dialogue options
    "recovering": Companion still travels but weak
  Validation: Affects companion availability
  
npc_state:conspiracy_leader_location
  Name: "Conspiracy Leader Location"
  Default: "unknown"
  States: "unknown" → "suspected" → "confirmed" → "confronted"
  Transitions:
    "suspected": After evidence accumulation (>= 3 conspirators)
    "confirmed": After NODE-140 (found leadership chamber)
    "confronted": At NODE-280 (final boss battle)
  Consequences:
    "unknown": Cannot initiate final confrontation
    "confirmed": Enables direct assault option
  Validation: Critical for campaign pacing
```

---

## IX. ENDING_CONDITION Hooks

Mechanics: Final state evaluation for ending determination.

```
ending_condition:ending_type
  Name: "Campaign Ending Determination"
  Default: null
  Possible Values:
    "Just_Ruler" (gates defined in endings-d5e.md)
    "Shadow_Broker"
    "Redemption"
    "Revolution"
    "Power_Vacuum"
    "Tragedy"
    "Pyrrhic_Victory"
  Evaluated At: NODE-280 (final decision point)
  Criteria: Complex combination of reputation, companion state, plot flags
  Validation: Must result in exactly one ending selected
  
ending_condition:world_state_change
  Name: "World State Changed Permanently"
  Default: false
  Trigger: Any ending reached
  Effect: Marks world as irreversibly altered (for sequel context)
  Validation: Always true by end of campaign
```

---

## X. Hook Interaction Matrix (For speckit.outline)

When writing nodes, reference this matrix to understand hook interactions:

| Hook Type | Read Frequency | Write Frequency | Gates Endings | Example |
|-----------|---|---|---|---|
| **flag** | Constant (dialogue branches) | Per session (state changes) | High (gates multiple endings) | conspiracy_discovered gates all investigation nodes |
| **counter** | Constant (dialogue flavor) | Multiple per session (reputation changes) | High (gates endings) | guard_rep > 50 gates Just Ruler ending |
| **visited** | Occasional (flavor text) | Once per location | Low (flavor only) | visited:temple_sanctuary adds theology perspective |
| **inventory** | Occasional (quest gating) | Per major quest | Medium (gates quests) | evidence_ledger required to prove conspiracy |
| **timer** | Per session check | Once per timer | Medium (forces choices) | guard_investigation_deadline creates pressure |
| **trust** | Constant (companion reactions) | Multiple per session | High (gates Redemption/Revolution) | thorne_approval > 80 gates Revolution ending |
| **currency** | Occasional (flavor) | Per transaction | Low (flavor only) | party_gold affects ending flavor text |
| **npc_state** | Occasional (NPC availability) | Per major event | Medium (affects party composition) | guard_captain_status determines recruitment availability |

---

## XI. Validation Checklist (For speckit.implement)

Before finalizing mechanics:

- [ ] All 8 hook types used at least once in campaign
- [ ] Each ending depends on 2-3 distinct hook states
- [ ] No hook exceeds maximum range (flags stay binary, counters within range)
- [ ] Reputation counters change meaningfully (not just +1 or -1)
- [ ] Companion approval changes tied to major story beats
- [ ] Quest items all acquirable via at least one path
- [ ] No inventory item permanently unobtainable
- [ ] Timers create genuine pressure (consequences if deadline passes)
- [ ] NPC states match companion/faction status
- [ ] Ending gates refer to consistent hook names
- [ ] All gates resolvable to true/false by Node 280
- [ ] No contradictory ending gates (e.g., can't require both guard_rep > 50 AND guard_rep < -20)

---

**Mechanics Configuration Status:** [DRAFT / APPROVED / READY FOR IMPLEMENT]

**Total Hooks Configured:** 8  
**Flags Defined:** 18+  
**Counters Defined:** 12+  
**Quest Items:** 4+  
**NPC States:** 5+  

**Last Updated:** [DATE]
