---
title: "[CAMPAIGN_NAME] Ending Conditions"
template: "endings-d5e"
game_system: "D&D 5e"
---

# [CAMPAIGN_NAME] — Ending Conditions

Complete definition of all possible campaign endings, requirements, and consequences. Used by `speckit.consequences` for validation and `speckit.endings` for documentation.

---

## Ending Architecture

**Total Endings:** 7  
**Ending Lock Timing:**
- After Session 3: 0 endings locked (all 7 viable)
- After Session 8: 4-5 endings locked (2-3 viable)
- After Session 13: 5-6 endings locked (1-2 viable)
- After Session 15: 1 ending active

---

## ENDING 1: The Just Ruler

### Summary
The party has restored order through law, justice, and cooperation with legitimate authority. The conspiracy is dismantled, the Guard maintains power, and the world stabilizes under established rule.

### Requirements

**Primary Gate (ALL must be true):**
- `guard_rep >= 50` (favored the Guard faction)
- `temple_rep >= 60` (maintained good relations with Temple)
- `syndicate_rep < 20` (kept Syndicate influence minimal)

**Secondary Gates (AT LEAST 2 must be true):**
- `conspirators_caught >= 4` (caught most conspirators)
- `conspiracy_dismantled = true` (destroyed conspiracy infrastructure)
- `guard_captain_confesses = true` (obtained confession)

**Companion Requirements (Optional):**
- Any companion configuration valid
- If `thorne_alive = true`: Adds "hard-won alliance" flavor text
- If `sister_mercy_alive = true`: Adds "spiritual blessing" flavor text

### Lock Timing
**Locked after Session 8 if:**
- `syndicate_rep > 30` (player sided with criminals too much)
- `temple_rep < 40` (player ignored spiritual authority)
- `guard_rep < 30` (player rejected law enforcement)

### Consequences

**World Changes:**
- Guard expands authority (increased checkpoints and patrols)
- Temple begins reformation (purging corruption)
- Syndicate pushed underground (less visible crime)
- Economy stabilizes with Guard oversight

**Companion Outcomes:**
- If recruited, all companions remain active in new power structure
- [COMPANION_1_NAME] gains Guard commission (if recruited and `thorne_alive`)
- [COMPANION_2_NAME] becomes Temple advisor (if recruited and `sister_mercy_alive`)
- [COMPANION_3_NAME] establishes merchant network under Guard protection (if recruited)

**Character Endings (Nodes 281-285):**
- Party receives official commendation
- Promoted to Guard advisory council or regional administrators
- Annual salary from Guard (`party_gold += 500`)
- Access to Guard resources (trained soldiers, equipment)

**Narrative Consequences:**
- Crime rates decline 60% over next year
- Innocent nobles imprisoned by overzealous Guard begin releasing
- Remaining syndicate members flee city or go dormant
- Temple influence grows significantly

**Hidden Cost:**
- Freedom of information restricted (Guard monitors all communication)
- Dissidents face harsh penalties (even if innocent)
- Merchant trade routes controlled by Guard taxation
- Some sympathetic criminals go unpunished

---

## ENDING 2: The Shadow Broker

### Summary
The party has seized power through criminal influence, establishing a hidden regime. The Syndicate controls the city from shadows, and order is maintained through fear and bribery rather than law.

### Requirements

**Primary Gate (ALL must be true):**
- `syndicate_rep >= 70` (deeply aligned with Syndicate)
- `guard_rep < 0` (opposed/destroyed Guard faction)
- `conspiracy_dismantled = true` (destroyed original conspiracy to seize power)

**Secondary Gates (AT LEAST 2 must be true):**
- `choice_faction_first_alliance = "syndicate"` (chose Syndicate first)
- `party_gold >= 5000` (accumulated significant wealth through crime)
- `npc_syndicate_master_opinion = "favorable"` (Syndicate leader trusts party)

**Companion Requirements:**
- `thorne_alive = true` (REQUIRED — [COMPANION_1_NAME] runs the criminal operation)
- `thorne_approval >= 70` ([COMPANION_1_NAME] must be deeply loyal)
- Optional: `sister_mercy_alive = true` (adds moral conflict flavor)

### Lock Timing
**Locked after Session 8 if:**
- `guard_rep > 30` (player maintained good relations with law)
- `thorne_recruited = false` (can't rule without [COMPANION_1_NAME])
- `conspiracy_location_found = true` AND `conspirators_caught < 2` (betrayal of Syndicate)

### Consequences

**World Changes:**
- Crime becomes systematized and "predictable" (wealthy bribed safe, poor targeted)
- Guard faction weakens or is corrupted from within
- Temple loses influence without Guard protection
- Black market becomes legitimate economy

**Companion Outcomes:**
- [COMPANION_1_NAME] becomes the Syndicate's new master (replacing previous leader)
- [COMPANION_2_NAME] (if alive) struggles with moral compromise or leaves in secret
- [COMPANION_3_NAME] prospers significantly but becomes target for power-hungry rivals
- Other recruited companions become Syndicate operatives

**Character Endings (Nodes 286-290):**
- Party owns multiple criminal enterprises
- Annual income from illegal operations (`party_gold += 2000`)
- Must maintain constant paranoia (assassination threats)
- Secretly meets with Syndicate council

**Narrative Consequences:**
- Corruption spreads through Guard (bribery successful)
- Innocent citizens live in fear of Syndicate enforcers
- Wealth inequality maximizes dramatically
- Underground resistance movements form

**Hidden Cost:**
- Party must commit crimes to maintain power (no escape)
- Betrayals from rival Syndicate members constant
- Cannot form lasting alliances with outside factions
- Ending is morally compromised (no redemption possible)

---

## ENDING 3: Redemption

### Summary
The party has broken the cycle of corruption by converting a key conspirator or NPC to justice. Despite personal cost, the conspiracy is dismantled through spiritual or moral awakening rather than force.

### Requirements

**Primary Gate (ALL must be true):**
- `temple_rep >= 60` (earned Temple's trust)
- `sister_mercy_alive = true` ([COMPANION_2_NAME] was not killed)
- `sister_mercy_recruited = true` (party actively recruited/converted [COMPANION_2_NAME])
- `sister_mercy_approval >= 50` ([COMPANION_2_NAME] trusts party)

**Secondary Gates (AT LEAST 3 must be true):**
- `choice_interrogation_approach = "mercy"` (showed mercy in key moments)
- `npc_guard_captain_confesses = true` (Guard Captain confessed willingly)
- `conspirators_caught >= 2` (caught conspirators through non-lethal means)
- `player_charisma_mod >= 1` (high Charisma enabled persuasion)

**Companion Requirements:**
- `sister_mercy_alive = true` (REQUIRED)
- `thorne_alive = false` OR `thorne_betrayed = false` ([COMPANION_1_NAME] not turned against party)
- Optional: `kael_alive = true` (adds "all companions saved" flavor)

### Lock Timing
**Locked after Session 10 if:**
- `sister_mercy_alive = false` (key companion must be alive)
- `temple_rep < 40` (lost Temple's faith)
- `conspirators_dead >= 4` (too much bloodshed for redemption narrative)
- `choice_ending_direction != "redemption"` (player rejected redemption path)

### Consequences

**World Changes:**
- Conspiracy leadership converts to Temple (pursuing justice through spiritual means)
- Guard and Temple cooperate (no longer competing)
- Syndicate influence reduces (loses criminal sponsors)
- Cycle of violence breaks (fewer people seeking revenge)

**Companion Outcomes:**
- [COMPANION_2_NAME] becomes High Priestess or spiritual advisor
- Guard Captain (if recruited) becomes Guard reformer
- [COMPANION_1_NAME] (if alive) questions loyalties and may leave or reform
- [COMPANION_3_NAME] becomes merchant advocating for honest trade

**Character Endings (Nodes 281-283):**
- Party receives spiritual recognition from Temple
- Made honorary clergy or blessed protectors
- Annual support from Temple (`party_gold += 300`)
- Pilgrims seek party's wisdom and counsel

**Narrative Consequences:**
- Crime rates decline 40% (through reform, not force)
- Conspiracy members imprisoned or reformed (many become monks/priests)
- Next generation taught peace rather than revenge
- Former conspirators work to undo previous corruption

**Hidden Benefit:**
- Community respects party (not fears them)
- Can ally with multiple factions simultaneously
- Unique ending available in sequel campaigns
- Moral high ground in all negotiations

---

## ENDING 4: The Revolution

### Summary
The party has orchestrated a rebellion against established order, replacing the corrupt regime with a new power structure. Society is radically restructured through violence and upheaval.

### Requirements

**Primary Gate (ALL must be true):**
- `thorne_recruited = true` ([COMPANION_1_NAME] leads the revolution)
- `thorne_approval >= 80` ([COMPANION_1_NAME] trusts party completely)
- `guard_rep <= -20` (party has actively opposed or dismantled Guard)
- `conspiracy_dismantled = true` (removed original obstacle to new order)

**Secondary Gates (AT LEAST 2 must be true):**
- `choice_faction_first_alliance = "thorne"` (supported [COMPANION_1_NAME] from start)
- `conspirators_caught < 2` (let conspirators live to use their knowledge)
- `temple_rep < 20` (rejected traditional authority)

**Companion Requirements:**
- `thorne_alive = true` (REQUIRED — [COMPANION_1_NAME] leads revolution)
- `thorne_in_party = true` ([COMPANION_1_NAME] actively participates)
- Optional: `kael_alive = true` ([COMPANION_3_NAME] provides merchant/common perspective)

### Lock Timing
**Locked after Session 8 if:**
- `thorne_recruited = false` (no revolutionary leader)
- `guard_rep > 40` (too friendly with existing power)
- `thorne_approval < 50` ([COMPANION_1_NAME] doesn't trust party)

### Consequences

**World Changes:**
- Guard hierarchy dismantled and replaced
- [COMPANION_1_NAME] becomes new leader (similar to Syndicate master but legitimate)
- Temple influence diminishes significantly
- Wealth redistribution attempted (with mixed results)

**Companion Outcomes:**
- [COMPANION_1_NAME] becomes city leader or regional warlord
- [COMPANION_2_NAME] (if alive) either flees or works covertly for Temple resistance
- [COMPANION_3_NAME] becomes merchant-class representative in new government
- Other companions become revolutionary officers

**Character Endings (Nodes 284-288):**
- Party becomes revolutionary council members
- Annual stipend from new government (`party_gold += 600`)
- Expected to continue fighting counter-revolutions
- Must maintain authority through force

**Narrative Consequences:**
- Old power structures collapse (chaos for 6+ months)
- Innocent casualties from fighting (estimated 200-500 deaths)
- Wealthy flee or lose influence
- New government struggles with legitimacy
- Neighboring regions may invade during transition

**Hidden Cost:**
- Violence spreads to avoid counter-coup
- Revolution is unstable (requires constant vigilance)
- Many party members become targets for revenge
- New government may become as corrupt as the old

---

## ENDING 5: The Power Vacuum

### Summary
The party has eliminated all major power structures without establishing clear replacement. Chaos and opportunism fill the void, creating anarchy or multiple smaller factions competing for control.

### Requirements

**Primary Gate (ALL must be true):**
- `guard_rep < -10` (Guard weakened or destroyed)
- `syndicate_rep < -10` (Syndicate weakened or destroyed)
- `temple_rep < 20` (Temple has no influence)
- `conspirators_dead >= 3` (killed many conspirators)

**Secondary Gates (AT LEAST 2 must be true):**
- `choice_faction_first_alliance = null` (party never committed to faction)
- `conspiracy_dismantled = true` (removed original power source)
- `last_combat_outcome = "player_won"` (multiple combat victories)

**Companion Requirements:**
- Any companion configuration allowed
- No specific companion required for this ending

### Lock Timing
**Locked after Session 8 if:**
- `guard_rep > 30` OR `syndicate_rep > 30` (at least one faction still strong)
- `choice_ending_direction = "justice"` (player chose stability)

### Consequences

**World Changes:**
- No central authority (organized chaos)
- Smaller criminal and civic groups fight for control
- Economy collapses and barter systems emerge
- Warlords and cults rise to fill power vacuum

**Companion Outcomes:**
- Recruited companions establish their own territories
- [COMPANION_1_NAME] becomes warlord of criminal underworld
- [COMPANION_2_NAME] leads spiritual resistance/refugee network
- [COMPANION_3_NAME] becomes merchant prince of new order

**Character Endings (Nodes 289-290):**
- Party must choose new power structure or establish their own
- No guaranteed income (must protect own territory)
- Constantly dealing with new rival factions
- Chaos either becomes opportunity or threat

**Narrative Consequences:**
- Crime rates spike 300% (no organization)
- Innocent citizens suffer worst consequences
- Foreign powers might invade during weakness
- Potential for new civilization to emerge
- Cycle of conflict continues (possibly worse)

**Hidden Opportunity:**
- Party can reshape society according to their vision
- Unique ending for sequel exploring new order
- Moral questions about chaos vs. tyranny

---

## ENDING 6: Tragic Defeat

### Summary
Despite efforts, the conspiracy succeeds or the party fails catastrophically. Not all is lost, but hard-won progress turns to tragedy. This ending remains available throughout the campaign as a last resort.

### Requirements

**Primary Gate (AT LEAST 1 must be true):**
- `conspirators_caught = 0` AND `current_session >= 12` (conspiracy never stopped)
- `party_total_damage_taken > 500` (party severely damaged in final combat)
- `party_level < 5` (party significantly underleveled)

**Alternative Gates (ALWAYS AVAILABLE):**
- `ending_reached = true` AND `party_xp < 30000` (player chose defeat)
- Manual selection by player (always available as option)

**Companion Requirements:**
- `thorne_alive = false` OR `sister_mercy_alive = false` OR `kael_alive = false`
- At least one key companion dies

### Lock Timing
**Never locked** — this ending is always available as a choice.

### Consequences

**World Changes:**
- Conspiracy succeeds partially (gains significant power)
- Guard, Temple, or Syndicate uses conspiracy for their own ends
- City descends into visible corruption or hidden control
- Status quo continues with added layer of conspiracy

**Companion Outcomes:**
- At least one companion dies (in battle or as consequence)
- Surviving companions scattered or imprisoned
- Party barely escapes with lives
- Potential for redemption in future campaigns

**Character Endings (Nodes 291-293):**
- Party survives but is hunted or exiled
- Must leave city or go into hiding
- Lost influence over events
- Can only watch consequences unfold

**Narrative Consequences:**
- Conspiracy deepens its hold
- More innocents suffer
- Power structures shift unpredictably
- Setup for potential sequel focusing on resistance

**Story Potential:**
- Most dramatic ending for emotional impact
- Enables hero's journey continuation in sequel
- Tests character values and survival instincts
- Audience investment in redemption arc

---

## ENDING 7: Pyrrhic Victory

### Summary
The party succeeds in stopping the conspiracy, but at massive personal and social cost. Victory is achieved but feels hollow — too many casualties, too much damage, or unacceptable compromises made.

### Requirements

**Primary Gate (ALL must be true):**
- `conspiracy_dismantled = true` (conspiracy stopped)
- `conspirators_caught + conspirators_dead >= 5` (most conspirators dealt with)
- `ending_type != "Shadow_Broker"` AND `ending_type != "Just_Ruler"` (not a clean ending)

**Secondary Gates (AT LEAST 2 must be true):**
- `party_total_damage_taken >= 300` (significant cost in battle)
- `thorne_alive = false` OR `sister_mercy_alive = false` (key ally lost)
- `temple_corrupted = true` OR `guard_weakened = true` (infrastructure damaged)
- `party_gold < 100` (economic ruin)

**Companion Requirements:**
- At least one companion dead or permanently injured
- At least one faction severely damaged
- Multiple casualties among NPC allies

### Lock Timing
**Companion Requirements:**
- `thorne_alive = true` AND `sister_mercy_alive = true` AND `kael_alive = true` (all survived)
- `guard_weakened = false` AND `temple_corrupted = false` (institutions intact)

### Consequences

**World Changes:**
- Conspiracy dismantled but city infrastructure damaged
- Recovery will take years
- Survivors struggle with PTSD and grief
- Refugee crisis or population displacement

**Companion Outcomes:**
- At least one companion dies (permanently)
- Survivors are traumatized but grateful
- [COMPANION_1_NAME] (if alive) honors fallen allies
- [COMPANION_2_NAME] (if alive) conducts memorial services

**Character Endings (Nodes 294-296):**
- Party recognized as heroes (mixed feelings)
- Receive medals but see suffering around them
- Offered limited reward (`party_gold += 200`)
- Expected to help with reconstruction

**Narrative Consequences:**
- Death toll: 100-500 civilians
- Infrastructure damage: 6-12 months to repair
- Psychological cost: party and city traumatized
- Lessons learned through blood and sacrifice

**Emotional Arc:**
- Bittersweet victory
- Questions about cost of justice
- Memorial for fallen
- Hope for future despite pain
- Sense of earned exhaustion

---

## Ending Matrix (For speckit.consequences Validation)

| Ending | Gate 1 | Gate 2 | Lock Condition | Viable After Session |
|---|---|---|---|---|
| Just Ruler | guard_rep ≥ 50 | temple_rep ≥ 60 | syndicate_rep > 30 | 8-13 |
| Shadow Broker | syndicate_rep ≥ 70 | guard_rep < 0 | thorne_recruited = false | 8-13 |
| Redemption | temple_rep ≥ 60 | sister_mercy_recruited | sister_mercy_alive = false | 10-13 |
| Revolution | thorne_approval ≥ 80 | guard_rep ≤ -20 | thorne_recruited = false | 8-13 |
| Power Vacuum | Multiple weak | Multiple weak | Any faction strong | 8-15 |
| Tragedy | [varies] | [varies] | Never | 1-15 |
| Pyrrhic | conspiracy_dismantled | ≥2 costs | All companions alive | 13-15 |

---

## Ending Validation Checklist

Before finalizing campaign:

- [ ] All 7 endings remain viable after Session 5
- [ ] Only 2-3 endings viable after Session 13
- [ ] Each ending has at least 2-3 unique variable gates
- [ ] No ending accidentally locked by routine events
- [ ] Tragic ending always remains available
- [ ] Each ending has distinct emotional tone
- [ ] Companion fates differ by ending (agency check)
- [ ] Faction final states differ by ending
- [ ] Epilogue text differs meaningfully by ending
- [ ] No ending requires impossible variable combinations

---

**Endings Registry Status:** [DRAFT / APPROVED / READY FOR CONSEQUENCES VALIDATION]

**Total Endings:** 7  
**Always-Available Endings:** 1 (Tragedy)  
**Locked Endings at Start:** 0  
**Locked Endings Mid-Campaign:** 4-5  

**Last Updated:** [DATE]
