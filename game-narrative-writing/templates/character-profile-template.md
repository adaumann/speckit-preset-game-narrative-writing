# Character Profile: [CHARACTER_NAME]

<!-- Widget template for SugarCube playable prototypes.
     Defines initial player character and displays as UI widget.
     Updated via MECHANIC:ATTRIBUTE hooks throughout narrative.
-->

---

## Identity

**Name:** [Player character name or customizable]

**Title/Role:** [e.g., "Wandering Scholar", "Knight Errant"]

**Background:** 
[2-3 sentences describing origin, motivation, or starting situation]

**Appearance:**
[Optional: Physical description, style notes for reference art]

---

## Starting Attributes

Define the player's core stats. These gate dialogue choices, affect outcomes, and track changes throughout the narrative.

| Attribute | Value | Range | Use Case |
|---|---|---|---|
| **Intelligence** | `[1-10]` | 1-10 | Affects logical/puzzle dialogue choices; gating cerebral puzzles |
| **Wisdom** | `[1-10]` | 1-10 | Affects moral/spiritual dialogue; perception & insight choices |
| **Power** | `[1-10]` | 1-10 | Affects combat/intimidation outcomes; martial skill gating |
| **Gold** | `[amount]` | 0-[max] | Currency for transactions, bribes, resource gating |
| **Custom: [name]** | `[value]` | [min-max] | User-defined stat (e.g., Charisma, Sanity, Reputation) |

### Predefined Attributes

```sugarcube
<<set $character to {
  name: "[CHARACTER_NAME]",
  intelligence: 5,
  wisdom: 5,
  power: 5,
  gold: 50,
  // custom attributes added here
}>>

// Define attribute ranges
<<set $character_ranges to {
  intelligence: { min: 1, max: 10 },
  wisdom: { min: 1, max: 10 },
  power: { min: 1, max: 10 },
  gold: { min: 0, max: 1000 }
}>>
```

---

## Personality & Alignment

**Archetype:** 
[e.g., Scholar, Warrior, Diplomat, Rogue — describes decision-making style]

**Alignment / Moral Stance:** 
[e.g., Good/Neutral/Evil, Chaotic/Lawful, or descriptive: "Pragmatic but honor-bound"]

**Voice & Tone:** 
[How does this character speak? Formal, casual, witty, grim? Affects dialogue options presented]

---

## Relationships & Factions

Track connections that affect dialogue gating and reputation mechanics.

| Type | Name | Initial Standing | Change Trigger |
|---|---|---|---|
| **NPC** | [Name] | [Value or "Unknown"] | [What changes this relationship] |
| **NPC** | [Name] | [Value or "Unknown"] | [What changes this relationship] |
| **Faction** | [Name] | [Tier: Hostile/Unfriendly/Neutral/Friendly/Allied/Exalted] | [Dialogue choice or quest] |

### Example:

| Type | Name | Initial Standing | Change Trigger |
|---|---|---|---|
| NPC | Henne (Guard) | Neutral | Dialogue choice in Act 1 |
| NPC | Priestess | Unknown | Interact in shrine |
| Faction | City Guard | Neutral | Complete quests for guard captain |
| Faction | Dark Syndicate | Hidden | Special dialogue unlock |

---

## Inventory Starting State

Define items the player begins with.

```sugarcube
<<set $inventory to {
  rusty_key: true,
  journal: true,
  travel_pack: true,
  gold_coins: true
}>>
```

| Item | Owned at Start | Description | Gating Use |
|---|---|---|---|
| [item_name] | Yes/No | [What is it?] | [What does it unlock?] |

---

## Character Arc & Development

**Starting Conflict:** 
[What drives the character's initial decisions?]

**Potential Growth:** 
[How might attributes change? What experiences reshape personality?]

**End States:** 
[Different endings based on final attribute values or relationship standings]

**Example:**
- High Wisdom + Allied with Temple Order → Spiritual ending
- High Power + Exalted with Dark Syndicate → Ambitious/dark ending
- Balanced attributes → Nuanced/diplomatic ending

---

## Notes for Narrative Designer

[Any context about this character's role, special mechanics, or branching logic that affects outline/dialogue tree planning]

**Example:**
- "This character can refuse key quests if Power < 3"
- "Dialogue with Priestess changes based on Intelligence score (puzzle solutions)"
- "Final choice locked behind Wisdom ≥ 7 OR faction standing"
