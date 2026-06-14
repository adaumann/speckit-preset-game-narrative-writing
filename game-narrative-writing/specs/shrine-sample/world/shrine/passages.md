# Passages at The Shrine — Shrine Sample

This document lists all available passages (scenes/encounters) at The Shrine location.

## Passage Registry

| Passage ID | Title | Quest | Stage | Opening Condition | Type |
|---|---|---|---|---|---|
| PASS-shrine-001 | Shrine Entrance | — | — | Always available | Intro |
| PASS-shrine-002 | Priestess Dialogue | Seeking the Blessing | 1 | First visit | Encounter |
| PASS-shrine-003 | Search the Shrine | — | — | After meeting Priestess | Optional |
| PASS-shrine-004 | Priestess Blessing | Seeking the Blessing | 2 | After completing dialogue | Conclusion |

---

## Passage Descriptions

### PASS-shrine-001: Shrine Entrance

**Location**: Outside The Shrine
**Act**: 1
**Quest**: None (optional entry point)
**Opening Condition**: Always available on first visit
**Closing Condition**: Player chooses to enter shrine (required for main narrative)

**Description**:
You stand before an ancient shrine, its stone walls weathered by centuries. The sight fills you with awe and unease.

**Leads to**:
- PASS-shrine-002 (Enter shrine → meet priestess)
- PASS-shrine-005 (Leave shrine → end encounter)

---

### PASS-shrine-002: Priestess Dialogue

**Location**: Inside The Shrine (main chamber)
**Act**: 1–2
**Quest**: Seeking the Blessing (Stage 1 → Stage 2)
**Opening Condition**: 
- Must have entered shrine from PASS-shrine-001
- NOT available: `$quest_shrine_blessing_complete == true`

**Closing Condition**: 
- Complete one of three dialogue paths (Ask History / Donate / Search)
- Sets `$quest_shrine_blessing_stage = 2`

**Description**:
A priestess emerges from the shadows within. She studies you with keen eyes.

**NPC Present**: Priestess

**Key Decisions**:
- Ask about shrine history (INT ≥ 6 for special path)
- Offer a donation (GOLD ≥ 5 for generous path)
- Search the shrine (find Old Book item)

**Leads to**:
- PASS-shrine-004 (Priestess Blessing) — after dialogue completes

---

### PASS-shrine-003: Search the Shrine

**Location**: Hidden chamber within shrine
**Act**: 1–2
**Quest**: None (optional side passage)
**Opening Condition**: 
- Must have talked to priestess in PASS-shrine-002
- Priestess permits search: `$spoke_priestess == true`

**Closing Condition**: 
- Find Old Book item
- Sets `$found_old_book == true`

**Description**:
You search the shrine's hidden alcoves. Dust and shadows conceal ancient secrets.

**Key Actions**:
- `[MECHANIC:INVENTORY add=old_book]` — Discover Old Book

**Leads to**:
- PASS-shrine-004 (Return to priestess)

---

### PASS-shrine-004: Priestess Blessing

**Location**: Inside The Shrine (main chamber, revisit)
**Act**: 2
**Quest**: Seeking the Blessing (Stage 2 → Stage 3)
**Opening Condition**: 
- Must have completed PASS-shrine-002 (dialogue)
- `$quest_shrine_blessing_stage == 2`

**Closing Condition**: 
- Receive blessing or depart
- Sets `$quest_shrine_blessing_complete = true`

**Description**:
The priestess regards you with understanding. She raises her hand in blessing.

**NPC Present**: Priestess

**Leads to**:
- PASS-shrine-005 (Depart shrine — end)
- END-A_Blessed (if wisdom > 6) — special ending
- END-B_Departed (if wisdom ≤ 6) — standard ending

---

### PASS-shrine-005: Depart

**Location**: Outside The Shrine (or anywhere)
**Act**: 2
**Quest**: None (exit passage)
**Opening Condition**: Always available after shrine encounter

**Closing Condition**: End of sample

**Description**:
You leave the shrine behind. The encounter remains etched in your memory.

**Leads to**:
- END-A_Blessed / END-B_Departed / END-C_Unknown (based on choices)

---

## Revisit Rules

If `revisit_allowed: true` in constitution:
- Player may return to The Shrine after completing main quest
- Priestess has different dialogue on revisit (optional variant)
- Can attempt to earn additional blessing (if wisdom improved)

## Quest Stage Map

```
PASS-shrine-001 (Entrance)
    ↓
PASS-shrine-002 (Dialogue) — $quest_shrine_blessing_stage = 1 → 2
    ├→ Ask History (INT ≥ 6) → Wisdom +1
    ├→ Donate (GOLD ≥ 5) → Wisdom +2
    └→ Search → Find Old Book
    ↓
PASS-shrine-004 (Blessing) — $quest_shrine_blessing_stage = 2 → 3
    ├→ Receive Blessing (Wisdom ≥ 6) → END-A
    └→ Depart (Wisdom < 6) → END-B
    ↓
PASS-shrine-005 (Depart)
    ↓
[ENDING]
```
