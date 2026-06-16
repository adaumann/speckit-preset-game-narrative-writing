---
description: "D&D 5e Node Outline Template for SugarCube/Twine Engine. Shows Twee 3 syntax with SugarCube 2.x macros for skill checks (with actual d20 rolling), companion approval, faction reputation, and combat aftermath. Use this for all dialogue nodes in a D&D campaign compiled to SugarCube."
engine_target: "sugarcube"
game_system: "d&d-5e"
---

# D&D 5e Node Outline (SugarCube/Twine Format)

This template shows how to structure D&D 5e campaign nodes in SugarCube 2.x syntax. All nodes follow this pattern.

---

## Node Structure (SugarCube Format)

```twee
:: NODE_015_GUARD_INTERROGATION [scene]
<h1>Guard Interrogation (NODE-015)</h1>

You've discovered Guard Captain Aldric is connected to the conspiracy. 
He's in the interrogation room, hands bound, guards outside.

Current Status:
Party Level: $partyLevel
Guard Captain HP: $guardCaptainHP
Thorne Recruited: $thorneRecruited
Sister Mercy Recruited: $sisterMercyRecruited

---

Captain Aldric sits across from you, defiant despite his bonds.

<p><strong>Guard Captain:</strong> "You can't prove anything. My unit is loyal."</p>

[[Insight Check - "Someone's forcing you. I can see it in your eyes."|NODE_015_INSIGHT_CHECK]]
[[Deception Check - "Your lieutenant already confessed."|NODE_015_DECEPTION_CHECK]]
[[Intimidation Check - "Talk or your family suffers too."|NODE_015_INTIMIDATION_CHECK]]
[[Mercy - "I know you're trapped. Help me and I'll protect your family."|NODE_015_MERCY_PATH]]

---

:: NODE_015_INSIGHT_CHECK
<<set $insightDC to 14>>
<<set $insightRoll to random(1, 20)>>
<<set $insightMod to $playerInsightMod>>
<<set $insightTotal to $insightRoll + $insightMod>>

<p><em>You roll the dice...</em></p>

<p>Insight Check: <strong>d20 + $insightMod = $insightRoll + $insightMod = $insightTotal</strong> (DC $insightDC)</p>

<<if $insightTotal gte $insightDC>>

  <h3>✓ SUCCESS</h3>
  
  <p><strong>Guard Captain (quietly):</strong> "You're right. They have my family. I was going to confess anyway."</p>
  
  <<set $conspiracyDiscovered to true>>
  <<set $conspiratorsIdentified to true>>
  <<set $guardCaptainConfesses to true>>
  <<set $guardRep += 10>>
  <<set $thorneApproval -= 5>>
  <<set $sisterMercyApproval += 10>>
  
  <p>You've learned the conspiracy extends beyond the barracks. The Guard Captain becomes a potential ally.</p>
  
  <<if $thorneRecruited and $thorneApproval lt 0>>
    <p><strong>Thorne (scoffing):</strong> "Compassion. How... charitable."</p>
  <</if>>
  
  <<if $sisterMercyRecruited and $sisterMercyApproval gte 15>>
    <p><strong>Sister Mercy (nodding):</strong> "You read him well. Mercy opens doors."</p>
  <</if>>
  
  [[Continue to Report to Commander|NODE_020_REPORT_TO_COMMANDER]]

<<else>>

  <h3>✗ FAILURE</h3>
  
  <p>Guard Captain remains silent, staring at you with defiance.</p>
  
  <<set $guardRep -= 5>>
  <<set $insightFailed to true>>
  
  <p>You'll need another approach to break him.</p>
  
  <<if $sisterMercyRecruited>>
    <p><strong>Sister Mercy (gently):</strong> "Perhaps try a different path, friend."</p>
  <</if>>
  
  [[Try a Different Skill Check|NODE_015_GUARD_INTERROGATION]]

<</if>>

---

:: NODE_015_DECEPTION_CHECK
<<set $deceptionDC to 12>>
<<set $deceptionRoll to random(1, 20)>>
<<set $deceptionMod to $playerCharismaMod>>
<<set $deceptionTotal to $deceptionRoll + $deceptionMod>>

<p><em>You lean in, speaking with calculated certainty...</em></p>

<p>Deception Check: <strong>d20 + $deceptionMod = $deceptionRoll + $deceptionMod = $deceptionTotal</strong> (DC $deceptionDC)</p>

<<if $deceptionTotal gte $deceptionDC>>

  <h3>✓ SUCCESS - He Believes You</h3>
  
  <p><strong>Guard Captain (eyes widening):</strong> "No... Marcus wouldn't... He promised..."</p>
  
  <p>He breaks, spilling everything about the conspiracy structure.</p>
  
  <<set $conspiracyDiscovered to true>>
  <<set $conspiratorsIdentifiedCount to 5>>
  <<set $guardRep -= 10>>
  <<set $thorneApproval += 15>>
  <<set $sisterMercyApproval -= 10>>
  
  <p>You gain detailed intelligence, though the Guard views this as underhanded.</p>
  
  <<if $thorneRecruited and $thorneApproval gte 15>>
    <p><strong>Thorne (grinning):</strong> "Now THAT'S how you interrogate. I like your style."</p>
  <</if>>
  
  [[Continue to Report to Commander|NODE_020_REPORT_TO_COMMANDER]]

<<else>>

  <h3>✗ FAILURE - He Sees Through It</h3>
  
  <p><strong>Guard Captain (laughing bitterly):</strong> "Nice try. But Marcus is dead. You're bluffing."</p>
  
  <<set $guardRep -= 15>>
  <<set $deceptionFailed to true>>
  
  <p>He clams up entirely, refusing to say another word.</p>
  
  [[Try a Different Approach|NODE_015_GUARD_INTERROGATION]]

<</if>>

---

:: NODE_015_INTIMIDATION_CHECK
<<set $intimidationDC to 16>>
<<set $intimidationRoll to random(1, 20)>>
<<set $intimidationMod to $playerCharismaMod>>
<<set $intimidationTotal to $intimidationRoll + $intimidationMod>>

<p><em>You slam your fist on the table.</em></p>

<p>Intimidation Check: <strong>d20 + $intimidationMod = $intimidationRoll + $intimidationMod = $intimidationTotal</strong> (DC $intimidationDC)</p>

<<if $intimidationTotal gte $intimidationDC>>

  <h3>✓ SUCCESS - Terror Breaks Him</h3>
  
  <p><strong>Guard Captain (terrified):</strong> "Okay! Okay! I'll tell you everything! Please, just... don't hurt me!"</p>
  
  <p>His confession reveals a conspiracy extending into the highest levels of government.</p>
  
  <<set $conspiracyDiscovered to true>>
  <<set $conspiratorsIdentified to true>>
  <<set $guardRep -= 20>>
  <<set $thorneApproval += 10>>
  <<set $sisterMercyApproval -= 15>>
  
  <<if $sisterMercyRecruited and $sisterMercyApproval lt -10>>
    <p><strong>Sister Mercy (dismayed):</strong> "Fear-based confession? That troubles my conscience."</p>
  <</if>>
  
  [[Continue to Report to Commander|NODE_020_REPORT_TO_COMMANDER]]

<<else>>

  <h3>✗ FAILURE - He Refuses</h3>
  
  <p><strong>Guard Captain (spitting blood):</strong> "I'd rather die than live in fear of you!"</p>
  
  <<set $guardRep -= 25>>
  <<set $sisterMercyApproval += 5>>
  <<set $combatWithCaptainTriggered to true>>
  
  <p>His defiance is admirable, but now you have no choice. Combat erupts.</p>
  
  [[Combat Begins|NODE_016_COMBAT_WITH_CAPTAIN]]

<</if>>

---

:: NODE_015_MERCY_PATH
<p><strong>You (calmly):</strong> "I know you're trapped. Help me and I'll protect your family."</p>

<p>Guard Captain (slowly): "How do I know you're trustworthy?"</p>

<p>You describe your plan to protect his family, shield them from retaliation.</p>

<<set $guardRep += 25>>
<<set $sisterMercyApproval += 20>>
<<set $thorneApproval -= 10>>
<<set $guardCaptainConfesses to true>>
<<set $conspiracyDiscovered to true>>
<<set $guardCaptainBecomesAlly to true>>

<p><strong>Guard Captain (with relief):</strong> "Thank you. I'll tell you everything. And... if you truly keep my family safe, I'll owe you a debt."</p>

<<if $thorneRecruited and $thorneApproval lt 0>>
  <p><strong>Thorne (muttering):</strong> "Soft. But effective, I suppose."</p>
<</if>>

<<if $sisterMercyRecruited and $sisterMercyApproval gte 20>>
  <p><strong>Sister Mercy (warmly):</strong> "Mercy opens hearts. Well done."</p>
<</if>>

You gain a powerful ally in the Guard hierarchy.

[[Continue to Report to Commander|NODE_020_REPORT_TO_COMMANDER]]

---

:: NODE_016_COMBAT_WITH_CAPTAIN [combat]

<h1>Combat Begins</h1>

<<if $lastCombatOutcome eq "player_won">>
  
  <p>Guard Captain Aldric falls, blood dripping from his wounds.</p>
  
  <<set $guardCaptainDefeated to true>>
  <<set $guardCaptainHP to 0>>
  
  <p><strong>Guard Captain (gasping):</strong> "Mercy... or finish me..."</p>
  
  [[Show mercy to the wounded enemy|NODE_017_WOUNDED_CAPTAIN_MERCY]]
  [[Execute him|NODE_017_CAPTAIN_EXECUTED]]
  [[Interrogate him while vulnerable|NODE_017_INTERROGATE_WOUNDED]]

<<elseif $lastCombatOutcome eq "player_lost">>
  
  <p>Darkness closes in as you fall...</p>
  
  <<set $partyDefeated to true>>
  
  [[Game Over|GAME_OVER]]

<<elseif $lastCombatOutcome eq "player_retreated">>
  
  <p>You manage to escape the interrogation room, but enemies are in pursuit.</p>
  
  <<set $enemiesHunting to true>>
  
  [[Continue on the run|NODE_018_PURSUIT]]

<</if>>

---

:: NODE_017_WOUNDED_CAPTAIN_MERCY

<p>You lower your weapon and help the Guard Captain to his feet.</p>

<p><strong>Guard Captain (grateful, weakly):</strong> "Thank you... I was going to confess anyway. They forced me into this."</p>

<<set $guardCaptainConfesses to true>>
<<set $conspiracyDiscovered to true>>
<<set $guardCaptainBecomesAlly to true>>
<<set $guardCaptainWounded to true>>
<<set $guardRep += 15>>
<<set $sisterMercyApproval += 15>>

<p>He tells you everything about the conspiracy, including names and locations.</p>

[[Continue to Report to Commander|NODE_020_REPORT_TO_COMMANDER]]

---

:: NODE_020_REPORT_TO_COMMANDER [scene]

<h1>Report to Commander</h1>

<<if $conspiracyDiscovered>>
  
  <p>You present your evidence to the Guard Commander.</p>
  
  <<if $conspiratorsIdentifiedCount gte 5>>
    <p><strong>Commander (gravely):</strong> "This goes deeper than I feared. We have a serious problem."</p>
    <<set $commanderBelievesYou to true>>
    <<set $nextSessionUnlocked to true>>
  <<else>>
    <p><strong>Commander (skeptical):</strong> "Interesting, but not conclusive. Bring me more evidence."</p>
    <<set $commanderSkeptical to true>>
  <</if>>
  
  <<if $guardCaptainBecomesAlly>>
    <p>Guard Captain Aldric stands beside you, vouching for your claims.</p>
    <<set $commanderFullyBelievesYou to true>>
  <</if>>

<<else>>

  <p><strong>Commander:</strong> "You've found nothing. Get out of my sight."</p>
  <<set $commanderRejectsYou to true>>

<</if>>

---

```

---

## Key SugarCube Patterns

### 1. **Dice Roll with Modifiers (SugarCube Does Math)**

```twee
<<set $insightRoll to random(1, 20)>>
<<set $insightMod to $playerInsightMod>>
<<set $insightTotal to $insightRoll + $insightMod>>

Success Check: <strong>d20 + $insightMod = $insightRoll + $insightMod = $insightTotal</strong>

<<if $insightTotal gte $insightDC>>
  ✓ SUCCESS
<<else>>
  ✗ FAILURE
<</if>>
```

**Key difference from Ink:** SugarCube can roll dice DIRECTLY. You don't need an external game engine to pass the roll result.

### 2. **Conditional Display (Companion Reactions)**

```twee
<<if $thorneRecruited and $thorneApproval gte 15>>
  <p><strong>Thorne (grinning):</strong> "Nice work. I respect that."</p>
<<elseif $thorneRecruited and $thorneApproval lt 0>>
  <p><strong>Thorne (scoffing):</strong> "Soft. Typical."</p>
<</if>>
```

### 3. **Reputation Gates (Ending Selection)**

```twee
<<if $guardRep gte 50 and $templeRep gte 60 and $syndicateRep lt 20>>
  <<set $endingType to "Just_Ruler">>
<<elseif $syndicateRep gt 70 and $guardRep lt 0>>
  <<set $endingType to "Shadow_Broker">>
<<else>>
  <<set $endingType to "Tragedy">>
<</if>>

You reach the ending: <<print $endingType>>.
```

### 4. **Inventory Gating (Quest Items)**

```twee
<<if $inventory.has("evidence_ledger") and $inventory.has("signet_ring")>>
  You have irrefutable proof. The evidence is undeniable.
  <<set $proofComplete to true>>
<<elseif $inventory.has("evidence_ledger")>>
  You have partial evidence, but it's not enough.
  <<set $proofPartial to true>>
<<else>>
  You have nothing. Without evidence, the Commander won't listen.
<</if>>
```

### 5. **Combat Outcome Branching**

```twee
<<if $lastCombatOutcome eq "player_won">>
  Enemy falls! You've won.
  <<set $combatVictory to true>>
<<elseif $lastCombatOutcome eq "player_lost">>
  Darkness closes in...
  [[Game Over|GAME_OVER]]
<<elseif $lastCombatOutcome eq "player_retreated">>
  You escape, but enemies pursue.
  <<set $enemiesPursuing to true>>
<</if>>
```

---

## Variable Declaration (Story Data Section)

```twee
:: StoryData
{
  "ifid": "D669B589-6C13-4F5A-8000-7E5E47DA8ADA",
  "format": "SugarCube",
  "format-version": "2.36.0",
  "start": "START"
}

---

:: START
<<set $partyLevel to 5>>
<<set $partyGold to 0>>
<<set $partyXP to 0>>

:: INIT [script]
<<set $playerInsightMod to 4>>
<<set $playerCharismaMod to 1>>
<<set $playerDeceptionMod to 2>>
<<set $playerIntimidationMod to 1>>

<<set $guardRep to 20>>
<<set $templeRep to 10>>
<<set $syndicateRep to 0>>

<<set $thorneRecruited to false>>
<<set $thorneApproval to -10>>
<<set $sisterMercyRecruited to false>>
<<set $sisterMercyApproval to 20>>

<<set $conspiracyDiscovered to false>>
<<set $conspiratorsIdentified to false>>
<<set $conspiratorsIdentifiedCount to 0>>

<<set $inventory to new Set()>>
```

---

## SugarCube Macros Reference for D&D

| Macro | Purpose | Example |
|---|---|---|
| `<<if>>` | Conditional logic | `<<if $skillRoll gte $DC>>` |
| `<<elseif>>` | Else-if branch | `<<elseif $skillRoll gte $DC - 5>>` |
| `<<else>>` | Else branch | `<<else>>` |
| `<</if>>` | End conditional | `<</if>>` |
| `<<set>>` | Assign variable | `<<set $approval += 10>>` |
| `<<random>>` | Generate random number | `<<set $roll to random(1, 20)>>` |
| `<<print>>` | Display variable | `You rolled: <<print $roll>>` |
| `<<link>>` | Create clickable link | `<<link "Check Guard">>` |
| `[[Link]]` | Shorthand link | `[[Next Node\|NODE_020]]` |
| `<<if>>...<<for>>` | Loop with condition | Loop through companions |

---

## 6. D&D 5e Combat Engine (`sugarcube-d5e-combat.js`)

The preset ships a full JavaScript combat engine that runs D&D 5e rules inside SugarCube — no game engine required.

**File**: `scripts/sugarcube-d5e-combat.js`  
**Install**: paste the file's contents into a Twee passage tagged `[script]`:

```twee
:: D5eCombatEngine [script]
/* paste entire sugarcube-d5e-combat.js here */
```

### What the engine calculates

| Rule | Implementation |
|---|---|
| Initiative | `d20 + DEX mod` for party and enemy; party wins ties |
| Attack roll | `d20 + toHitBonus` vs target AC; natural 20 = crit, natural 1 = fumble |
| Critical hit | Damage dice doubled (bonus unchanged) |
| Damage | Parses expressions like `"2d8+3"`; applies resistance/immunity |
| Multiattack | Configurable per enemy (`multiattack: 2`) |
| Saving throws | `d20 + save mod` vs DC; on-hit effects (e.g. prone) |
| Enemy features | Triggered by HP threshold (`"hp_below_half"`) or turn start; e.g. Second Wind |
| Morale check | Wisdom save when enemy HP ≤ 25%; failure → surrender |
| XP & loot | Written to `$partyXP`, `$lastCombatLoot` on victory |
| Level-up | `D5e.checkLevelUp()` compares `$partyXP` to official thresholds |

### Built-in enemies

`thug` · `guard` · `guard_captain` · `bandit_leader` · `cult_fanatic`

Register your own:

```javascript
D5e.registerEnemy("syndicate_enforcer", {
    name: "Syndicate Enforcer", cr: 4, xp: 1100,
    hp: 65, ac: 17,
    str: 18, dex: 14, con: 16, int: 11, wis: 12, cha: 10,
    profBonus: 2, multiattack: 2,
    attacks: [
        { name: "Shortsword", toHitBonus: 6, damage: "1d6+4", damageType: "piercing" },
        { name: "Hand Crossbow", toHitBonus: 6, damage: "1d6+4", damageType: "piercing" }
    ],
    saves: { str: 6, dex: 4, con: 5, int: 1, wis: 1, cha: 0 },
    resistances: [], immunities: [],
    features: [],
    morale: 13,
    loot: ["30 gp", "Syndicate Medallion"]
});
```

### `<<combat>>` macro

Replace the old manual `$lastCombatOutcome` setup with a single macro call:

```twee
:: NODE_016_COMBAT_TRIGGER [scene]
<p>Combat erupts. Guard Captain Aldric draws his longsword.</p>

<<combat "guard_captain" "NODE_016_COMBAT_OUTCOME">>
```

The macro runs the full combat loop and navigates to `NODE_016_COMBAT_OUTCOME`.

### `<<skillcheck>>` macro

Replaces the verbose inline dice roll block:

```twee
/* Before (manual) */
<<set $insightRoll to random(1, 20)>>
<<set $insightTotal to $insightRoll + $playerInsightMod>>
<<if $insightTotal gte 14>>...

/* After (engine) */
<<skillcheck "Insight" $playerInsightMod 14 true>>
<<if $lastSkillCheckSuccess>>
  <p>Insight Check: <<print $lastSkillCheckRoll>> + <<print $playerInsightMod>> = <<print $lastSkillCheckTotal>> ✓ (DC <<print $lastSkillCheckDC>>)</p>
  ...success prose...
<<else>>
  <p>Insight Check: <<print $lastSkillCheckTotal>> ✗ (DC <<print $lastSkillCheckDC>>)</p>
  ...failure prose...
<</if>>
```

### Outcome passage pattern

```twee
:: NODE_016_COMBAT_OUTCOME [scene]

<<combatlog>>

<<if $lastCombatOutcome eq "player_won">>
  <p><<print $lastEnemyName>> falls.</p>
  
  <<if $lastEnemySurrendered>>
    <p><strong>Guard Captain (gasping):</strong> "Mercy... I yield!"</p>
  <<else>>
    <p><strong>Guard Captain (gasping):</strong> "Finish it..."</p>
  <</if>>
  
  <<if $lastCombatXP gt 0>>
    <p>+<<print $lastCombatXP>> XP | Loot: <<print $lastCombatLoot.join(", ")>></p>
  <</if>>
  
  <<run D5e.checkLevelUp()>>
  <<if $partyLeveledUp>><p>🎉 Level up! You are now level <<print $partyNewLevel>>.</p><</if>>
  
  <<set $guardCaptainDefeated to true>>
  [[Show mercy|NODE_017_WOUNDED_CAPTAIN_MERCY]]
  [[Execute him|NODE_017_CAPTAIN_EXECUTED]]
  [[Interrogate while vulnerable|NODE_017_INTERROGATE_WOUNDED]]

<<elseif $lastCombatOutcome eq "player_lost">>
  <p>Darkness closes in...</p>
  <<set $partyDefeated to true>>
  [[Game Over|GAME_OVER]]

<<elseif $lastCombatOutcome eq "player_retreated">>
  <p>You escape, but enemies pursue.</p>
  <<set $enemiesHunting to true>>
  [[Continue on the run|NODE_018_PURSUIT]]

<</if>>
```

### Story variables consumed by the engine

| Variable | Type | Purpose |
|---|---|---|
| `$partyLevel` | number | Used to compute proficiency bonus |
| `$partyCurrentHP` | number | Current HP; read and written each combat |
| `$partyMaxHP` | number | Max HP ceiling |
| `$partyAC` | number | Party armour class |
| `$partyXP` | number | Cumulative XP; engine adds enemy XP on win |
| `$partyWeaponDmg` | string | Damage expression e.g. `"1d8+3"` |
| `$playerStrMod` / `$playerDexMod` | number | Attack modifier |
| `$playerProfBonus` | number | Override proficiency (auto-computed if absent) |
| `$playerInsightMod` etc. | number | Skill modifiers used by `<<skillcheck>>` |

### SugarCube vs. Ink (Key Differences)

| Feature | SugarCube | Ink |
|---|---|---|
| **Dice Rolling** | Direct: `random(1, 20)` or `<<skillcheck>>` | Must be done in game engine |
| **Full combat** | `<<combat>>` macro runs D&D 5e loop in-browser | Game engine runs combat; Ink reads outcome |
| **Math** | Full JavaScript support | Limited to conditional checks |
| **Complexity** | Can handle intricate logic | Better for narrative focus |
| **Performance** | Browser-based, fast | Requires compilation |
| **Distribution** | Single HTML file | Requires game engine import |
| **Branching** | Unlimited depth | Better for large projects |
| **Play Testing** | Play directly in browser | Need game engine setup |

---

## File Naming Convention

Save this template as:

```
templates/node-outline-d5e-sugarcube.md
```

Or in Twee format:

```
templates/node-outline-d5e-sugarcube.twee
```

---

## Complete Campaign Node Structure (SugarCube)

```
Session 1, Node 015 (Interrogation)
  ↓
SugarCube evaluates skill check directly: <<set $roll to random(1, 20) + $mod>>
  ↓
<<if $roll gte $DC>> → SUCCESS or FAILURE branch
  ↓
Update variables: <<set $guardRep += 10>>
  ↓
Display companion reactions: <<if $thorneApproval > 50>>
  ↓
Link to Node 020: [[Continue to Report|NODE_020_REPORT_TO_COMMANDER]]
  ↓
[Repeat for 140+ nodes across 15 sessions]
  ↓
Final Node: Evaluate ending conditions
  ↓
One of 7 endings based on cumulative variable state
  ↓
Display ending epilogue
```

---

## SugarCube Advantages Over Ink

✅ **Dice rolls built-in** — No need for external game engine to roll d20
✅ **Full JavaScript** — Complex conditions, loops, object manipulation  
✅ **Playable as HTML** — Test directly in browser, no compilation needed
✅ **Faster testing** — Make changes, refresh browser
✅ **Better for solo creation** — Don't need separate game engine
✅ **Standalone distribution** — Single `.html` file plays anywhere

---

## SugarCube Disadvantages vs. Ink

❌ **Single platform** — Locked to web browsers (not optimized for mobile/console)
❌ **Harder to port** — Exporting to other engines requires more work
❌ **Larger file size** — Full JavaScript runtime included
❌ **Less narrative focus** — Tempts you to build mechanics in story layer
❌ **State management complexity** — JavaScript scope can be confusing

---

## When to Use Each

**Use SugarCube if:**
- Solo developer building complete game
- Prefer browser-based playable prototype
- Want dice rolls in story layer (not external game engine)
- Targeting web-only distribution
- Need rapid testing/iteration

**Use Ink if:**
- Planning multi-platform export (Unity, Godot, Unreal)
- Narrative is separated from mechanics
- Game engine handles all combat/rolls
- Want portable dialogue system
- Prefer clean narrative-focused syntax

---

## Testing This Template

```bash
# Compile to SugarCube (Twee)
speckit.compile --engine sugarcube

# Output: story.html
# Open in browser and play directly
# No external engine needed
```

---

## Integration Checklist (SugarCube)

- [ ] Skill checks use `<<random(1, 20)>>` for actual dice rolls
- [ ] Companion approval tracked with `<<set $approval += N>>`
- [ ] Faction reputation gates use `<<if $faction gte N>>`
- [ ] Combat outcome stored in `$lastCombatOutcome`
- [ ] Inventory uses `$inventory.has("item")` checks
- [ ] Endings evaluate in final decision node
- [ ] All variables initialized in `INIT` section
- [ ] Companion reactions use `<<if>>` conditions
- [ ] Links use `[[Label|NODE_NAME]]` format
- [ ] No external game engine needed (self-contained HTML)

---

## Example: Play Testing Workflow (SugarCube)

1. **Compile to HTML:**
   ```bash
   speckit.compile --engine sugarcube
   ```

2. **Open in Browser:**
   ```
   story.html
   ```

3. **Play through campaign:**
   - Make skill check choices
   - Watch variables change in real-time
   - See companion reactions
   - Reach endings
   - Refresh to play again

4. **No compilation needed** — Play test immediately, make edits, refresh browser

**Much faster iteration than Ink-based approach.**
