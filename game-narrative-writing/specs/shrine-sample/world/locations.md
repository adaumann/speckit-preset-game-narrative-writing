# World Locations — Shrine Sample

This document indexes all locations available in the Shrine sample narrative.

## Location Registry

| Location ID | Name | Description | Acts | Passages | Quests |
|---|---|---|---|---|---|
| LOC-shrine | The Shrine | Ancient stone structure, weathered by centuries. Site of spiritual power and mystery. | 1–2 | 3 | Seeking the Blessing (optional) |

---

## Location Profiles

### The Shrine (LOC-shrine)

**Sensory Anchors**:
- Visual: Cracked stone walls covered in moss and lichen, ancient carvings worn smooth by time, iron doors heavy with rust
- Audio: Whisper of wind through gaps, occasional creaking of aged wood
- Smell: Stone dust, incense (faint), earth
- Touch: Cold, rough stone; dampness in the air

**Internal Rules**:
- Time of day does not affect availability
- Player can revisit between passages (if revisit enabled in constitution)
- NPCs present: Priestess (always), possibly others based on quest progression

**Passages at This Location**:
1. Shrine Entrance — Initial arrival, setting establishment
2. Priestess Dialogue — Main encounter, dialogue choices, attribute gating
3. Search/Loot — Optional inventory pickup, treasure discovery

**Quests Available**:
- Seeking the Blessing (optional, 3 stages)
  - Stage 1: Arrive and meet priestess
  - Stage 2: Dialogue and choices
  - Stage 3: Conclusion (blessing granted, knowledge shared, or departure)

---

## Spatial Layout (Optional)

If implementing spatial navigation (not required for Shrine sample):

```
Shrine Entrance
    │
    ├─→ [Priestess] (dialogue passage)
    │
    ├─→ [Hidden Chamber] (search passage)
    │
    └─→ [Altar] (ritual/blessing passage)
```

For this sample, passages are linear and location-based, not spatially navigable.
