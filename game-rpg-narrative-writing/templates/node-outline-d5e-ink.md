---
description: "D&D 5e Node Outline Template for Ink Engine. Shows proper Ink syntax for skill checks, companion approval, faction reputation, and combat aftermath dialogue. Use this for all dialogue nodes in a D&D campaign compiled to Ink."
engine_target: "ink"
game_system: "d&d-5e"
---

# D&D 5e Node Outline (Ink Format)

This template shows how to structure D&D 5e campaign nodes in Ink syntax. All nodes follow this pattern.

---

## Node Structure (Ink Format)

```ink
=== NODE_015_GUARD_INTERROGATION ===

# Guard Interrogation (NODE-015)

## Setup
You've discovered Guard Captain Aldric is connected to the conspiracy. 
He's in the interrogation room, hands bound, guards outside.

VAR success_dc = 0
VAR check_result = 0

## Scene Context
- Current party_level: {party_level}
- Guard Captain HP: {guard_captain_hp}
- Thorne recruited: {thorne_recruited}
- Sister Mercy recruited: {sister_mercy_recruited}

---

Captain Aldric sits across from you, defiant despite his bonds.

Guard Captain: "You can't prove anything. My unit is loyal."

### Choice A: Insight Check (DC 14)

* [Insight Check] "Someone's forcing you. I can see it in your eyes."
  ~ check_result = player_insight_mod  // Game engine passes this
  ~ success_dc = 14
  
  {check_result >= success_dc:
    // SUCCESS PATH
    Guard Captain (quietly): "You're right. They have my family."
    
    ~ conspiracy_discovered = true
    ~ conspirators_identified = true
    ~ guard_captain_confesses = true
    ~ guard_rep += 10
    ~ thorne_approval -= 5  // Cynical rogue dislikes compassion
    ~ sister_mercy_approval += 10  // Cleric appreciates insight
    
    You've learned the conspiracy extends beyond the barracks.
    -> NODE_020_REPORT_TO_COMMANDER
  
  - else:
    // FAILURE PATH
    Guard Captain remains silent, staring.
    
    ~ guard_rep -= 5
    ~ insight_failed = true
    
    You'll need another approach.
    -> NEXT_CHECK_OPTION
  }

### Choice B: Deception Check (DC 12)

* [Deception Check] "Your lieutenant already confessed. We're making deals."
  ~ check_result = player_charisma_mod
  ~ success_dc = 12
  
  {check_result >= success_dc:
    // SUCCESS PATH
    Guard Captain's eyes widen.
    
    Guard Captain: "No... Marcus wouldn't..."
    
    He breaks, spilling everything about the conspiracy structure.
    
    ~ conspiracy_discovered = true
    ~ conspirators_identified = true
    ~ conspirators_identified_count = 5  // More detailed intelligence
    ~ guard_rep -= 10  // Betrayed by trickery
    ~ thorne_approval += 15  // Respects ruthlessness
    ~ sister_mercy_approval -= 10  // Dislikes manipulation
    
    The path forward becomes clear.
    -> NODE_020_REPORT_TO_COMMANDER
  
  - else:
    // FAILURE PATH
    Guard Captain laughs.
    
    Guard Captain: "Nice try. Marcus is dead. You're bluffing."
    
    ~ guard_rep -= 15  // Failed manipulation offends him
    ~ deception_failed = true
    
    He clams up entirely.
    -> NEXT_CHECK_OPTION
  }

### Choice C: Intimidation Check (DC 16)

* [Intimidation Check] *Slam fist on table* "Talk or your family suffers too."
  ~ check_result = player_charisma_mod
  ~ success_dc = 16
  
  {check_result >= success_dc:
    // SUCCESS PATH (Risky but effective)
    Guard Captain (terrified): "Okay! Okay! I'll tell you everything!"
    
    ~ conspiracy_discovered = true
    ~ conspirators_identified = true
    ~ guard_rep -= 20  // Fear-based cooperation not respected
    ~ thorne_approval += 10  // Appreciates power
    ~ sister_mercy_approval -= 15  // Horrified by threat
    
    His confession reveals a deeper conspiracy layer.
    -> NODE_020_REPORT_TO_COMMANDER
  
  - else:
    // FAILURE PATH
    Guard Captain spits blood in defiance.
    
    Guard Captain: "I'd rather die than live in fear of you."
    
    ~ guard_rep -= 25  // Massive disrespect
    ~ sister_mercy_approval += 5  // Respects his courage
    ~ combat_with_captain_triggered = true
    
    The interrogation turns violent.
    -> NODE_016_COMBAT_WITH_CAPTAIN
  }

### Choice D: Mercy (No Check Required)

* [Mercy Path] "I know you're trapped. Help me and I'll protect your family."
  
  Guard Captain (slowly): "How do I know you're trustworthy?"
  
  ~ guard_rep += 25  // Loyalty rewarded with loyalty
  ~ sister_mercy_approval += 20  // Compassion resonates
  ~ thorne_approval -= 10  // Sees it as weakness
  ~ guard_captain_confesses = true
  ~ conspiracy_discovered = true
  ~ guard_captain_becomes_ally = true
  
  You gain a powerful ally in the Guard hierarchy.
  -> NODE_020_REPORT_TO_COMMANDER

---

## Variable Tracking (After Node Completion)

```ink
// Update state based on chosen path
{conspiracy_discovered:
  ~ progress_chapter_1 = true
  ~ available_nodes += NODE_020
  ~ available_nodes += NODE_030
}

{guard_captain_becomes_ally:
  ~ npc_guard_captain_status = "ally"
  ~ npc_guard_captain_combat_support = true
}

{thorne_recruited:
  {thorne_approval > 50:
    ~ thorne_dialogue_tone = "warm"
  - thorne_approval > 0:
    ~ thorne_dialogue_tone = "neutral"
  - else:
    ~ thorne_dialogue_tone = "cold"
  }
}
```

---

## Outcomes (Next Nodes)

=== NODE_020_REPORT_TO_COMMANDER ===

## Report to Guard Commander

You leave the interrogation room and head to the Commander's office...

[Story continues based on what you learned]

-> END

---

=== NODE_016_COMBAT_WITH_CAPTAIN ===

## Combat Begins

[Combat resolved by game engine]

[After combat, link back to aftermath dialogue]

~ guard_captain_defeated = true
~ guard_captain_hp = 0

// Narrator describes combat result
The Guard Captain falls, wounded but alive.

Guard Captain (gasping): "Finish me... or let me confess..."

* [Show mercy to wounded enemy]
  ~ guard_captain_confesses = true
  -> NODE_017_WOUNDED_CAPTAIN_CONFESSION

* [Execute him]
  ~ guard_captain_dead = true
  ~ guard_rep -= 30  // Guard dishonored
  ~ sister_mercy_approval -= 25  // Horrified
  -> NODE_020_REPORT_TO_COMMANDER

---

=== NODE_017_WOUNDED_CAPTAIN_CONFESSION ===

Guard Captain (weakly, with relief): "Thank you... I was going to confess anyway..."

[Confession dialogue and information reveal]

~ conspiracy_discovered = true
~ guard_captain_becomes_ally = true
~ guard_captain_wounded = true  // Affects later combat availability

-> NODE_020_REPORT_TO_COMMANDER

---
```

---

## Pattern Explanations

### 1. Skill Check Structure

```ink
* [Skill Name] "Dialogue option"
  ~ check_result = player_ability_mod  // Set by game engine
  ~ success_dc = 12
  
  {check_result >= success_dc:
    // SUCCESS OUTCOME
    ~ consequence_variable = true
    -> NEXT_NODE
  - else:
    // FAILURE OUTCOME
    ~ consequence_variable = false
    -> ALTERNATE_NODE
  }
```

**How game engine integrates:**
```csharp
// Unity: Before continuing Ink story, set the check result
story.VariableState["player_insight_mod"] = PlayerStats.insight_modifier;
story.VariableState["check_result"] = diceRoll + modifier;

// Then let Ink evaluate the condition
story.Continue();
```

---

### 2. Companion Approval Tracking

```ink
~ thorne_approval += 15  // Rogue respects the cunning approach
~ sister_mercy_approval -= 10  // Cleric disapproves of manipulation

// Later, use approval to unlock reactions
{thorne_approval > 75:
  Thorne: "I'm starting to like your style."
}
```

**Companion tone based on approval:**
```ink
{thorne_recruited:
  {thorne_approval > 50:
    ~ thorne_tone = "warm"
  - thorne_approval > 0:
    ~ thorne_tone = "neutral"
  - else:
    ~ thorne_tone = "cold"
  }
  
  Thorne ({thorne_tone}): "[dialogue that reflects tone]"
}
```

---

### 3. Faction Reputation Gates

```ink
~ guard_rep += 10  // Player action increases Guard reputation

// Later, check if ending is unlocked
{guard_rep > 50 && temple_rep > 60 && syndicate_rep < 20:
  ~ ending_type = "Just Ruler"
  -> ENDING_JUST_RULER
- else:
  ~ ending_type = "Fallen"
  -> ENDING_FALLEN
}
```

---

### 4. Combat Aftermath (Ink Narrates Result, Game Engine Does Mechanics)

```ink
// Combat handled by game engine
// Ink waits for result

{combat_party_won:
  Guard Captain (wounded, falling to one knee): "Mercy..."
  
  * [Interrogate while vulnerable]
    ~ guard_rep -= 10  // Fear-based cooperation
    ~ information_gained = true
    -> INTERROGATION_SUCCESS
  
  * [Show mercy]
    ~ guard_rep += 20  // Honorable victory
    ~ guard_captain_becomes_ally = true
    -> CAPTAIN_BECOMES_ALLY

- combat_party_lost:
  Darkness closes in...
  -> GAME_OVER

- combat_party_retreated:
  You escape, but enemies remain alive...
  ~ enemies_still_hunting = true
  -> PURSUIT_NODE
}
```

---

### 5. Multiple Endings Based on Variables

```ink
=== FINAL_CHOICE ===

## The Final Confrontation

The conspiracy leader stands before you.

* [Try diplomatic resolution]
  {guard_rep > 50 && temple_rep > 50 && thorne_approved < 50:
    ~ ending = "REDEMPTION"
    -> ENDING_REDEMPTION
  - guard_rep > 70 && thorne_approval > 80:
    ~ ending = "REVOLUTION"
    -> ENDING_REVOLUTION
  - syndicate_rep > 70:
    ~ ending = "SHADOW_BROKER"
    -> ENDING_SHADOW_BROKER
  - else:
    ~ ending = "TRAGEDY"
    -> ENDING_TRAGEDY
  }

* [Fight to the end]
  {thorne_alive && thorne_approval > 50:
    Thorne charges forward beside you.
    ~ ending = "PYRRHIC_VICTORY"
    -> ENDING_PYRRHIC_VICTORY
  - else:
    You stand alone.
    ~ ending = "SACRIFICE"
    -> ENDING_SACRIFICE
  }
```

---

### 6. Quest Item Gates (Inventory)

```ink
[Examine the evidence]
{inventory_evidence_ledger && inventory_signet_ring:
  You have both pieces. This is irrefutable proof.
  ~ conspiracy_proof_complete = true
  -> COMMANDER_BELIEVES_YOU

- inventory_evidence_ledger:
  You have partial evidence, but it's not conclusive...
  ~ conspiracy_proof_partial = true
  -> COMMANDER_SKEPTICAL

- else:
  You have nothing to show. Without evidence...
  ~ conspiracy_proof_none = true
  -> COMMANDER_DENIES_YOU
}
```

---

### 7. Dynamic NPC Reactions Based on Player State

```ink
{player_charisma > 15 && player_alignment == "good":
  Captain: "You have the bearing of a true hero."
  ~ captain_respect += 20

- player_charisma > 15:
  Captain: "You have presence, at least."
  ~ captain_respect += 10

- else:
  Captain: *Dismisses you with a wave*
  ~ captain_respect -= 5
}
```

---

## File Naming Convention

Save this template as:

```
templates/node-outline-d5e-ink.md
```

Then reference in commands:

```bash
speckit.outline --node-template d5e-ink
speckit.outline --node-template d5e-ink --node-id NODE_015
```

---

## Key Principles for D&D in Ink

1. **Dice rolls happen OUTSIDE Ink** — Game engine rolls d20+mod, passes result to Ink
2. **Combat resolves OUTSIDE Ink** — Game engine handles initiative, HP, damage; Ink narrates aftermath
4. **Dialogue branches WITHIN Ink** — All choice logic, NPC reactions, ending gates
5. **Variables bridge the gap** — Game engine sets ability scores, roll results; Ink reads them for narrative flow
6. **No mechanics math in Ink** — Ink doesn't calculate "1d6+2"; it receives the result and branches

---

## Example: Complete Campaign Node Flow (D&D 5e → Ink)

```
Session 1, Node 015 (Interrogation)
  ↓
Game Engine: Roll Insight check (d20 + player_insight_mod)
Game Engine: Pass result to Ink as `check_result = 18`
  ↓
Ink: Evaluate `[if check_result >= 14]` → TRUE
Ink: Execute success path (Captain confesses)
Ink: Update variables (conspiracy_discovered, guard_rep, thorne_approval)
  ↓
Ink: Branch to Node 020 (Report to Commander)
  ↓
Node 020 evaluates faction gates and companion reactions
  ↓
[Repeat for 140+ nodes across 15 sessions]
  ↓
Final Node: Evaluate ending conditions based on cumulative reputation/companion approval
  ↓
One of 7 endings reached based on variable state
```

---

## Testing This Template

```bash
# Compile to Ink
speckit.compile --engine ink

# Import story.ink into Unity
# Verify:
# 1. Skill checks receive results from game engine
# 2. Companion approval visible in dialogue
# 3. Faction reputation gates work
# 4. Multiple endings reachable
```

---

## Integration Checklist

- [ ] All nodes follow `=== NODE_NAME ===` header format
- [ ] Skill checks use `{check_result >= success_dc:` pattern
- [ ] Companion approval tracked with `~ companion_approval +/- N`
- [ ] Faction reputation gates check `{faction_rep > N:}`
- [ ] Combat aftermath uses `{combat_party_won:` outcomes
- [ ] Endings evaluate final conditions at `=== FINAL_CHOICE ===`
- [ ] No math calculations in Ink (game engine provides numbers)
- [ ] All variables declared before use
- [ ] Node links use `-> NODE_NAME` format
- [ ] Each non-terminal node has 2+ choices (except combat aftermath)
