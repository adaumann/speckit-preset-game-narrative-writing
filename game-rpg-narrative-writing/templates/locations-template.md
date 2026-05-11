# Location Registry Template

## Location Structure

Use this template for each distinct location in your world.

---

# [Location Name]

**Location ID:** LOC-[ShortName]  
**Location Type:** [Urban / Rural / Dungeon / Wilderness / Interior / Exterior / Hybrid]  
**Parent Region:** [REGION-xxx — the Region this Location belongs to]  
**Parent Area:** [AREA-xxx — the Area within the Region]  
**Accessibility:** [Easy to reach / Hidden / Restricted / Remote]  
**Hub Passage:** [LOC-xxx passage that acts as the navigation hub for this Location]  
**First Appearance Node:** [NODE reference where players first visit]  
**Scene IDs:** [NODE-NNN, NODE-NNN, ... — all scenes that take place in this Location]

---

## Setting & Atmosphere

**Atmosphere Description:**  
[1-2 sentences about the mood/feel of the location]

**Sensory Anchors:**
- **Sound:** [What do players hear? Ambient or disturbing?]
- **Smell:** [What odors characterize this place?]
- **Visual:** [Color palette, distinctive landmarks, visual mood]
- **Tactile:** [Texture of ground, air temperature, humidity]
- **Taste:** [If relevant - air quality, foodstuffs, etc.]

**Thematic Elements:**
[What narrative themes does this location represent? What story role does it play?]

---

## Location Details

**Scale/Dimensions:**
[For tactical locations: "40 ft. × 25 ft." or "3 levels, 60×80 per level"]  
[For narrative locations: "Small town" or "sprawling dungeon complex"]

**Notable Features/Points of Interest:**
- [Feature 1]: [What is it? Why is it important?]
- [Feature 2]: [Description and mechanical significance]
- [Feature 3]: [Description and mechanical significance]

**NPCs Present:**
- [NPC Name]: [Role/purpose, when present, dialogue hooks]
- [NPC Name]: [Role/purpose, when present, dialogue hooks]
- [Occasional NPCs]: [Who else might be here? Under what conditions?]

---

## Faction & Political Control

**Controlling Faction(s):**
[Which factions have power/influence here?]

**Faction Reputation Effects:**
- [Faction name] ≥ [threshold]: [What access/treatment does high rep grant?]
- [Faction name] ≤ [threshold]: [What happens with low/negative rep?]

**Neutral Ground?**
[Is this a safe location for all factions, or are some unwelcome?]

**Law Enforcement Presence:**
[Are guards/authorities present? How actively patrolled?]

---

## Connections & Navigation

**Connected Locations:**
- [Location A] via [path/door/direction]: [How far? Obstacles?]
- [Location B] via [path/door/direction]: [How far? Obstacles?]
- [Location C] via [path/door/direction]: [How far? Obstacles?]

**Escape Routes:**
[Can players flee from combat? Where do exits lead?]

**Fast Travel:**
[Can players skip to this location after discovering it? Any restrictions?]

---

## Hazards & Environmental Features

**Environmental Hazards:**
- [Hazard type]: [Description, save DC if applicable, damage]
- [Hazard type]: [Description, save DC if applicable, damage]

**Traps (if applicable):**
- [Trap location]: [Trigger condition, DC to detect/disable, effect]
- [Trap location]: [Trigger condition, DC to detect/disable, effect]

**Weather/Time Effects:**
[Do weather or time of day affect this location? How?]

**Restrictions:**
[Can parties camp here? Rest safely? Or are there dangers during downtime?]

---

## Encounters & Quests

**Scenes occurring here:**
<!-- These must match the Scene IDs listed in the Location header above. -->
- [NODE-NNN]: [Scene name], type: [scene_type], [brief description]
- [NODE-NNN]: [Scene name], type: [scene_type], [brief description]

**Associated Quests:**
- [Quest name]: [Stage(s) that occur here]
- [Quest name]: [Stage(s) that occur here]

**Puzzle Locations:**
- [Puzzle name]: [Where in location?]
- [Puzzle name]: [Where in location?]

---

## Platform-Specific Information

### Tabletop RPG

**Tactical Grid Map:**
- Dimensions: [X ft. × Y ft.]
- Grid squares: [Example: "8 × 5 squares (1 square = 5 ft.)"]
- Lighting: [Bright / Dim / Darkness, and sources]
- Difficult Terrain: [Where? Why? DC to cross if applicable]

**Furniture & Obstacles:**
- [Description of scene layout for tactical positioning]
- [Cover points and their effectiveness]
- [Height variations or vertical features]

**Terrain Features:**
- [Water, stairs, pillars, etc. with mechanical implications]

**Environmental Mechanics:**
- [Gravity effects, temperature, magical auras, etc.]

**Encounter Difficulty Adjustments:**
- If combat occurs: [How does environment affect action economy, cover, tactics?]
- [Do neutral NPCs flee / stay neutral / interfere?]
- [Does proprietor/authority figure stop combat if it escalates?]

**Map Reference:**
[Where is the tactical map file? Example: `maps/city/tavern-main-floor.jpg`]

---

### Computer Game

**Level Design:**
- Interior/Exterior: [If interior, how many rooms? Connections?]
- Player movement: [Open exploration / linear / gated areas?]
- Verticality: [Stairs, platforms, elevation changes?]

**Interaction Hotspots:**
- [Interaction point 1]: [Object, NPC, or mechanic]
- [Interaction point 2]: [Object, NPC, or mechanic]
- [Interaction point 3]: [Object, NPC, or mechanic]

**AI Patrolling:**
- [NPC type]: [Patrol path, behavior triggers, dialogue opportunities]
- [NPC type]: [Patrol path, behavior triggers, dialogue opportunities]

**Stealth Considerations:**
- [Cover points for hiding]
- [Guard sight lines]
- [Noise sources that alert enemies]

**Progression Gating:**
- [What progression level should player reach before first visit?]
- [Are there level-gated areas within location?]
- [Can player return for post-game content?]

**Asset Requirements:**
- [Building/terrain models needed]
- [Day/night variants required?]
- [Destruction/corruption states if location changes through story?]
- [Animation requirements (NPCs, environmental effects)]

**Fast Travel:**
- [Is this a fast travel destination after discovery?]
- [Any restrictions on fast traveling in/out?]

---

## Social & Narrative Context

**History:**
[What is the location's background? Why does it exist? What events shaped it?]

**Current Events:**
[What's happening here NOW? What tensions exist?]

**Rumors/Gossip:**
[What do people say about this place? Legends? Warnings?]

**Quests Involving This Location:**
[Which quests can be triggered or completed here?]

---

## Design Notes

**Intended Role:**
[Is this a major story location, minor landmark, or alternative path? What purpose does it serve?]

**Atmosphere Goals:**
[What feelings should players experience here? Tension? Wonder? Danger? Peace?]

**Reusability:**
[Can this location be revisited? Does it change over time? Can it be used in multiple quests?]

**Variation Options:**
[Can this location exist in multiple states? (Friendly/hostile / Day/night / Pristine/corrupted?)]

**Playtesting Notes:**
[What issues have players encountered here? Balance adjustments made?]

---

## Quick Reference

| Aspect | Details |
|--------|---------|
| **Location Type** | [Type] |
| **Scale** | [Dimensions or description] |
| **Controlling Faction** | [Faction] |
| **Recommended Level** | [Character level range] |
| **Travel Time From** | [Previous location]: [Duration] |
| **Safe to Rest?** | [Yes / No / Conditional] |
| **Major NPCs** | [List] |
| **Main Encounters** | [CR or Difficulty] |
| **Quest Hubs** | [Quests that start/occur here] |
