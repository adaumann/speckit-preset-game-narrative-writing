---
title: "Campaign Instantiation Example"
description: "How concrete campaign values fill abstract template placeholders"
---

# Campaign Instantiation: From Template to Reality

This document shows **how a concrete campaign instantiates the abstract D&D 5e templates**.

---

## Example: The Syndicate Conspiracy Campaign

### Step 1: Campaign Pitch (spec-d5e.md → Concrete)

**Template asks for:**
```yaml
- [CAMPAIGN_NAME]: [USER_INPUT]
- [INVESTIGATION_GOAL]: [USER_INPUT]
- [COMPANION_1_NAME]: [USER_INPUT]
- [FACTION_1_NAME]: [USER_INPUT]
```

**Concrete campaign fills in:**
```yaml
CAMPAIGN_NAME: "The Syndicate Conspiracy"
INVESTIGATION_GOAL: "Uncover hidden Syndicate leadership controlling the city"
COMPANION_1_NAME: "Thorne" (street orphan turned rogue)
COMPANION_2_NAME: "Sister Mercy" (temple priestess doubting her faith)
COMPANION_3_NAME: "Kael" (merchant prince with guild connections)
FACTION_1_NAME: "City Guard" (lawful authority, currently corrupt)
FACTION_2_NAME: "Temple of Light" (spiritual authority, infiltrated)
FACTION_3_NAME: "Syndicate" (hidden criminal empire, secretly running city)
```

### Step 2: Constitution Applied (constitution-template.md → Concrete)

**Template variable:**
```
VAR thorne_approval = -10
VAR sister_mercy_approval = 20
VAR kael_approval = 0
```

**Campaign fills in ratios:**
```
thorne_approval = -10  # Orphan distrusts wealthy party
sister_mercy_approval = 20  # Priestess wants to help but has doubts
kael_approval = 0  # Merchant neutral—wants profit
```

### Step 3: Plan Applied (plan-d5e.md → Concrete)

**Template asks:**
```
Session 1: [SESSION_1_NAME]
Session 2: [SESSION_2_NAME]
Companion 1 recruited in: [SESSION]
```

**Campaign fills in:**
```
Session 1: "Dead Informant" (murder leads to Syndicate question)
Session 2: "First Lead" (party meets Thorne, street urchin witness)
Session 3: "Guard Confrontation" (party meets Sister Mercy in temple)
Session 4: "Merchant Connection" (party meets Kael through guild)
Session 5: "Act 1 Climax - Guard Captain Revelation"

Thorne recruited: Session 2-3 (proves trustworthiness)
Sister Mercy recruited: Session 5-6 (leaves temple to help)
Kael recruited: Session 7-8 (merchant resources committed)
```

### Step 4: Variables Applied (variables-d5e.md → Concrete)

**Template variable:**
```
counter:guard_rep (Range: -100 to +100)
counter:temple_rep (Range: -100 to +100)
counter:syndicate_rep (Range: -100 to +100)
```

**Campaign fills in SESSION-BY-SESSION flow:**
```
Session 1:
  guard_rep: +20 → +25 (help guard solve murder, +5)
  temple_rep: +10 → +10 (neutral)
  syndicate_rep: 0 → -5 (guard suspects Syndicate)

Session 2:
  guard_rep: +25 → +30 (provide info, +5)
  temple_rep: +10 → +15 (Sister Mercy appreciates investigation, +5)
  syndicate_rep: -5 → -15 (Syndicate notices party, -10)

Session 3:
  guard_rep: +30 → +20 (party sides with temple over guard, -10)
  temple_rep: +15 → +30 (defend temple, +15)
  syndicate_rep: -15 → -20 (Syndicate warns party, -5)

[... continues through all 15 sessions ...]

Session 15 - Ending Selection:
IF guard_rep > 50 AND temple_rep > 60 AND syndicate_rep < 20:
  → Just Ruler ending
ELSE IF syndicate_rep > 70 AND guard_rep < 0:
  → Shadow Broker ending
ELSE IF temple_rep > 60 AND sister_mercy_alive AND sister_mercy_approval > 50:
  → Redemption ending
[... etc ...]
```

### Step 5: Mechanics Applied (mechanics-d5e.md → Concrete)

**Template asks:**
```
flag:[INVESTIGATION_GOAL]_discovered
  Trigger: At NODE-040
  
inventory:[QUEST_ITEM_1]
  Acquired: NODE-030
  Required To: NODE-040
```

**Campaign fills in:**
```
flag:syndicate_leadership_discovered
  Trigger: At NODE-040 (Guard Captain confesses about Syndicate boss)
  Effect: Unlocks dialogue revealing Syndicate leadership location

inventory:evidence_ledger
  Acquired: NODE-030 (found in Guard Captain's office)
  Required To: NODE-040 (show to Sister Mercy for validation)
  Consequences: Sister Mercy joins party

inventory:signet_ring
  Acquired: NODE-015 (lifted from conspirator at murder scene)
  Required To: NODE-050 (show to Kael—recognizes Syndicate mark)
  Consequences: Kael admits Syndicate connection, joins investigation

inventory:temple_key
  Acquired: NODE-080 (Sister Mercy gives access to temple vault)
  Required To: NODE-090 (access vault containing Syndicate documents)
  Consequences: Discovers Syndicate has infiltrated temple
```

### Step 6: Endings Applied (endings-d5e.md → Concrete)

**Template matrix:**
```
| Ending | Gate 1 | Gate 2 | Gate 3 |
| Just Ruler | guard_rep ≥ 50 | temple_rep ≥ 60 | syndicate_rep < 20 |
| Shadow Broker | syndicate_rep ≥ 70 | guard_rep < 0 | thorne_recruited |
| Redemption | temple_rep ≥ 60 | sister_mercy_recruited | sister_mercy_approval ≥ 50 |
```

**Campaign determines ending paths:**
```
Party choices Session 1-5:
- Helped Guard early → guard_rep +25
- Defended Temple → temple_rep +30
- Avoided Syndicate → syndicate_rep -15
Result: On track for "Just Ruler" ending

Party choices Session 6-10:
- Recruited Thorne and Kael → thorne_recruited = true, kael_recruited = true
- Sister Mercy's approval rose to +60 → sister_mercy_approval ≥ 50
- Final session reputation: guard_rep +65, temple_rep +70, syndicate_rep -25
Result: Multiple endings viable (Just Ruler, Redemption, Pyrrhic if any die)

Session 15 Calculation:
- Just Ruler gates: guard_rep (65 ≥ 50 ✓), temple_rep (70 ≥ 60 ✓), syndicate_rep (-25 < 20 ✓)
- Redemption gates: temple_rep (70 ≥ 60 ✓), sister_mercy_recruited (✓), approval (60 ≥ 50 ✓)
Result: Two endings possible; party makes final choice in Node 280
```

---

## How Different Campaign Types Instantiate Differently

### Comparison: Same Template, Different Themes

| Element | Syndicate (Concrete) | Monster Hunt (Concrete) | Heist (Concrete) |
|---------|---|---|---|
| **Investigation Goal** | Syndicate leadership | Dragon lair location | Royal vault contents |
| **Quest Item 1** | Evidence ledger | Dragon scales | Building blueprint |
| **Companion 1** | Thorne (rogue) | Master Hunter | Heist coordinator |
| **Faction 1** | City Guard | Hunters Guild | Noble house |
| **Faction 2** | Temple | Royal court | City watch |
| **Faction 3** | Syndicate | Scholars | Thieves guild |
| **Rep Counter 1** | guard_rep | hunter_rep | noble_house_rep |
| **Rep Counter 2** | temple_rep | royal_court_rep | city_watch_rep |
| **Rep Counter 3** | syndicate_rep | scholar_rep | thieves_rep |

**Template structure identical; content changes based on theme**

---

## How AI Generates These Concrete Instances

### Process: Template → Customization → Instantiation

**Step 1: User provides constitution**
```
Game system: D&D 5e
Campaign name: "The Syndicate Conspiracy"
Main goal: Uncover hidden Syndicate leadership
Companions: Thorne (rogue), Sister Mercy (priestess), Kael (merchant)
Factions: Guard, Temple, Syndicate
```

**Step 2: AI instantiates all templates**
- `plan-d5e.md` → Creates session structure, node ranges, encounter list
- `variables-d5e.md` → Creates faction rep counters, companion approval scales
- `endings-d5e.md` → Creates ending gates using faction reputation
- `mechanics-d5e.md` → Creates quest items matching investigation goal

**Step 3: Validation occurs**
- Check: Each ending has 2-3 unique gates? ✓
- Check: Companion timelines align with plan? ✓
- Check: All quest items acquirable? ✓
- Check: Reputation changes cumulative? ✓

---

## Template Reusability

The **same D&D 5e template system** can instantiate 100+ different concrete campaigns:

**Conspiracy theme variations:**
- Political scandal, Corporate espionage, Noble betrayal, Cult infiltration, Dragon cult plot

**Monster theme variations:**
- Single monster hunt, Horde invasion, Necromancer plague, Curse spreading

**Faction theme variations:**
- Any 3-faction power structure: Noble houses, Merchant guilds, Religious orders, Criminal syndicates, Academic factions, Political parties

**All use identical mechanical structure—only concrete values differ**

---

## When Users Modify Templates

Users commonly:

1. **Add custom factions** (add 4th faction)
2. **Extend companions** (add 4th companion)
3. **Adjust approval scales** (lower romance gate from 76 to 60)
4. **Modify session count** (20 sessions instead of 15)
5. **Add custom quest items** (beyond 4 core items)

**Each modification regenerates connected templates:**
- Add companion → variables-d5e updates, endings-d5e adds companion gate, mechanics updates approval counter

---

**Next Step:** Use these filled-in templates in `speckit.outline` to generate node beat sheets!
