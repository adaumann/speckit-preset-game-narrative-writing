---
quest_id: quest-shrine-blessing
quest_title: Seeking the Blessing
location: shrine
status: DRAFT
---

# Seeking the Blessing — Shrine Sample Quest

A three-stage optional quest where the player seeks guidance from the Priestess.

---

## Quest Overview

| Field | Value |
|---|---|
| Quest ID | `quest-shrine-blessing` |
| Location | The Shrine |
| Stage Count | 3 |
| Completion Variable | `$quest_shrine_blessing_complete` |
| Completable | Yes (always solvable) |
| Consequence | Attribute changes (Wisdom ±1 to ±2), possible item acquisition (Old Book) |

---

## Stage 1: Arrival

**Variable**: `$quest_shrine_blessing_stage = 1`

**Objective**: Meet the Priestess and choose a dialogue path

**Passage**: PASS-shrine-002 (Priestess Dialogue)

**Opening Condition**: 
- Player has entered shrine from entrance

**Available Choices**:
1. Ask about shrine history
2. Offer a donation
3. Search the shrine

**Consequences by Choice**:
- **Ask History** (INT ≥ 6): Wisdom +1, unlock intelligence-specific ending
- **Donate** (GOLD ≥ 5): Wisdom +2, show generosity
- **Search**: Find Old Book item, demonstrates curiosity

**Closing Condition**:
- Player makes one choice and completes passage
- `$quest_shrine_blessing_stage = 2`

---

## Stage 2: Resolution

**Variable**: `$quest_shrine_blessing_stage = 2`

**Objective**: Receive priestess's blessing or insight

**Passage**: PASS-shrine-004 (Priestess Blessing)

**Opening Condition**:
- Must have completed Stage 1
- `$quest_shrine_blessing_stage == 2`

**Available Choices**:
1. Accept the blessing
2. Politely depart

**Consequences**:
- **Accept** (Wisdom ≥ 6): Receive special ending, priestess's respect
- **Depart** (Wisdom < 6): Leave with priestess's thanks, standard ending

**Closing Condition**:
- Player makes final choice
- `$quest_shrine_blessing_complete = true`

---

## Stage 3: Conclusion / Ending

**Variable**: `$quest_shrine_blessing_complete = true`

**Objective**: Quest concluded

**Passage**: PASS-shrine-005 (Depart) → Ending passage

**Endings Available**:
- `END-A_Blessed` (if Wisdom ≥ 6) — Priestess grants blessing; wisdom is your strength
- `END-B_Departed` (if Wisdom < 6) — You leave respectfully; humility is your virtue
- `END-C_Unknown` (if Old Book acquired) — Priestess hints at deeper mysteries

---

## Quest Variables

| Variable | Type | Initial | Final | Used In |
|---|---|---|---|---|
| `$quest_shrine_blessing_stage` | int | 1 | 3 | Stage tracking |
| `$quest_shrine_blessing_complete` | bool | false | true | Completion flag |
| `$visited_shrine` | bool | false | true | Location tracking |
| `$spoke_priestess` | bool | false | true | NPC interaction |

---

## Attribute Impact

| Choice | Attribute | Change | Gate |
|---|---|---|---|
| Ask History | Wisdom | +1 | Requires INT ≥ 6 |
| Donate (generous) | Wisdom | +2 | Requires GOLD ≥ 5 |
| Accept Blessing | Wisdom | +1 (potential) | Wisdom must already be ≥ 6 |

**Total possible Wisdom gain**: +4 (ask history + donate + accept blessing)

---

## Optional Paths

### Alternative: Search for Old Book

If player chooses to search instead of dialogue:
- `$found_old_book = true`
- Priestess recognizes grimoire
- Unlocks secret ending: priestess hints at deeper mysteries in the world
- Does not prevent other quest paths (can continue after searching)

### Alternative: No Donation (Low Gold)

If player has `$character.gold < 5`:
- Donation choice is disabled
- Can still ask history or search
- Priestess respects honesty: "You have little, yet you came seeking"

---

## Replay Consideration

If `revisit_allowed: true` in constitution:
- Player can return to shrine after completing quest
- Priestess has shortened greeting: "Ah, you've returned. What brings you back?"
- Can attempt to earn additional wisdom (new dialogue option)
- Original choices not repeatable

---

## Design Notes

This quest demonstrates:
- **Optional multi-stage quest** with conditional dialogue
- **Attribute gating** (INT, GOLD, Wisdom checks)
- **Inventory interaction** (optional Old Book pickup)
- **Location-based passages** (all occur at shrine)
- **Multiple endings** based on quest performance

It serves as a template for slightly larger quest structures while remaining beginner-friendly for designers learning narrative design patterns.
