# World-Building Reference: [GAME_TITLE]

<!-- Living reference document for locations, objects, world rules, and ambient states.
     Updated throughout drafting. speckit.continuity checks node prose against these entries. -->

---

## World Overview

[WORLD_OVERVIEW]
<!-- 100–200 words. The setting's essential nature, tone, and rules.
     What makes this world distinct? What constraints does it place on narrative? -->

---

## World Rules

<!-- Rules that govern the game world and constrain narrative logic.
     Violations are caught by speckit.analyze and speckit.continuity.
     Format: WR-NNN | Rule | Category | First enforced in
     Categories: world-physics / social / technical / magical / mechanical -->

| Rule ID | Rule | Category | First Enforced In | Consequence if violated |
|---|---|---|---|---|
| WR-001 | [NEEDS CLARIFICATION] | world-physics / social / technical / magical / mechanical | NODE-[N] | [what breaks narratively or mechanically] |
| WR-002 | [NEEDS CLARIFICATION] | | | |

### Narrative Boundaries

<!-- What the player cannot do, access, or know in this world. Defines the edge of agency.
     These are not mechanical gates — they are world-level constraints that make choices meaningful. -->

| Boundary | Reason | Nodes where this matters |
|---|---|---|
| [PLAYER_CANNOT_DO_X] | [world-rule rationale] | NODE-[N] |
| [INFORMATION_UNAVAILABLE] | [narrative rationale] | NODE-[N] |

---

## Locations

<!-- One entry per location that appears in nodes. -->

### [LOCATION_NAME] — [LOCATION_ID]

| Field | Value |
|---|---|
| Location ID | LOC-[N] |
| State variable | $location_[name]_state (Tier 2 — stub only) |
| First appears | NODE-[N] |
| Connected to | [LOCATION_IDs] |

**Description** (canonical, second/third person per constitution.md):
[LOCATION_DESCRIPTION]

**Sensory anchors**:
- Sight: [SIGHT] — *"[Direct prose example — one sentence, second/third person per constitution.md]"*
- Sound: [SOUND] — *"[Direct prose example]"*
- Smell: [SMELL] — *"[Direct prose example]"*
- Texture / touch: [TEXTURE] — *"[Direct prose example]"*

**Atmosphere by time/state**:
| State | Atmosphere | Sensory shift |
|---|---|---|
| default | [ATMOSPHERE] | [what changes from baseline] |
| [STATE] | [ATMOSPHERE] | |

**Narrative function**: [What this location does for the story — tension source / sanctuary / decision point / revelation site / environmental pressure]

**Forbidden/off-limits**: [What the player cannot do or access here — creates boundaries and raises stakes]

**Object inventory**:
| Object ID | Object | State | Variable | Interactable |
|---|---|---|---|---|
| OBJ-[N] | [OBJECT_NAME] | [intact/broken/taken] | $object_[name]_state | yes/no |

**Node references**: NODE-[N], NODE-[N]

---

## Objects

<!-- Objects that appear across multiple locations or have mechanical significance. -->

### [OBJECT_NAME] — [OBJECT_ID]

| Field | Value |
|---|---|
| Object ID | OBJ-[N] |
| Location | LOC-[N] |
| Portable | yes / no |
| Inventory item | $inv_[name] (if portable) |
| State variable | $object_[name]_state (Tier 2 — stub only) |

**States**: [intact / broken / repaired / taken / combined]
**Description**: [OBJECT_DESCRIPTION]
**Sensory detail**: *"[Direct prose example — how this object looks, feels, or sounds when interacted with]"*
**Narrative purpose**: [What this object does for the story — Chekhov item / gate / trust signal / world-rule demonstration]
**Story function**: [1–2 sentences on symbolic or thematic role, if any]
**Appears in nodes**: NODE-[N], NODE-[N]

---

## Factions

<!-- Groups with standing in the world. Trust/faction hooks may reference these.
     Each entry here must have a corresponding object in $faction_registry (variables.md ## Faction & Reputation). -->

| Faction ID | Name | Role | Variable | Default Standing |
|---|---|---|---|---|
| FAC-[N] | [FACTION_NAME] | [FACTION_ROLE] | $faction_[name] (Tier 2) | [neutral/hostile/ally] |

---

## Shops

<!-- One entry per merchant or shop location.
     Drives $shop_registry in variables.md ## Shop State and ShopUI in sugarcube-shop-template.twee.
     speckit.compile reads this section to populate $shop_registry automatically for SugarCube targets.

     Design guide:
       - SHOP_ID: short snake_case key, e.g. "blacksmith", "alchemist_row", "black_market"
       - npc_id: references characters-template.md NPC; drives greeting and portrait
       - faction_id: optional; reputation with this faction modifies prices (see price_discount_by_tier)
       - sell_ratio: fraction of base price paid when player sells back (0.0–1.0; default 0.5)
       - restock_on: "long_rest" | "in_game_day" | "never" | "story_beat:[node_id]"
       - catalog items:
           item — matches item variable name in variables.md ## Inventory (or accessory/consumable/spell)
           display — human-readable label shown in UI
           price — base price in the shop's currency
           currency — currency variable name (from variables.md ## Currency)
           stock — starting quantity; -1 = unlimited
           min_tier — minimum faction tier required to see/buy (omit if no gate)
           description — one sentence shown in shop UI item tooltip

     Price modifier (computed in <<shopBuy>> widget):
       effective_price = base_price × (1 + faction_discount) × (1 - cha_mod × 0.02)
       faction_discount per tier is defined in price_discount_by_tier below.
       CHA modifier: ±2% per point above/below 10 (configurable in constitution.md).

     Limited stock items must have a matching stock counter in variables.md ## Shop State. -->

### [SHOP_NAME] — SHOP-[N]

| Field | Value |
|---|---|
| Shop ID | [SHOP_ID] |
| Display Name | [SHOP_DISPLAY_NAME] |
| NPC | NPC-[N] ([NPC_NAME]) |
| Location | LOC-[N] |
| Faction | FAC-[N] (optional — omit if no faction tie) |
| Currency | [CURRENCY_VARIABLE] |
| Sell Ratio | 0.5 |
| Restock On | long_rest \| in_game_day \| never \| story_beat:[NODE_ID] |
| Open By Default | true |
| Notes | [e.g. "Closes after NODE-040; only sells magic items at allied+ standing"] |

**Price Discount by Tier** (if Faction is set — leave blank if no faction tie):

| Tier | Modifier |
|---|---|
| hostile | +20% (price surcharge) |
| unfriendly | +10% |
| neutral | ±0% |
| friendly | −5% |
| allied | −10% |
| exalted | −15% |

**Catalog:**

| Item Variable | Display | Base Price | Currency | Stock | Min Tier | Description |
|---|---|---|---|---|---|---|
| [item_variable] | [Item Name] | [N] | [currency_var] | -1 | — | [One sentence description shown in UI tooltip] |
| [item_variable] | [Item Name] | [N] | [currency_var] | [N] | friendly | [Description] |

<!-- [REPEAT shop entry — copy from ### [SHOP_NAME] down for each shop] -->

---

## Ambient States

<!-- World-level states that affect multiple locations or narrative conditions.
     Examples: time of day, weather, political state, alert level. -->

| State Variable | Type | Valid Values | Default | Affects |
|---|---|---|---|---|
| [var_name] | flag / counter / enum | [VALUES] | [DEFAULT] | [NODES / LOCATIONS] |

---

## Continuity Log

<!-- Populated by speckit.continuity. Do not edit manually. -->

| Date | Node ID | Issue | Status |
|---|---|---|---|
| | | | |
