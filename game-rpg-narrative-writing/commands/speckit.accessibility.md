---
description: Accessibility validator — measure readability (Flesch-Kincaid, sentence length), flag content warnings needed, validate contrast for UI text, identify ableist language. For RPG campaigns (tabletop D&D/Pathfinder/Shadowrun and computer game), validates accessibility across sessions/chapters, playstyle routes, companion choice accessibility, and ruleset mechanic accessibility (DC readability, hero point clarity, attribute name clarity).
handoffs:
  - label: Revise Readability
    agent: speckit.revise
    prompt: Some passages have poor readability. Please simplify sentence structure and vocabulary.
    send: true
  - label: Polish
    agent: speckit.polish
    prompt: After accessibility review, refine prose for readability and clarity.
    send: true
---

# speckit.accessibility

Accessibility validator — measure **readability (Flesch-Kincaid grade level, sentence length), flag content warnings, validate contrast for UI text, identify ableist language**.

**🎮 RPG Campaign Support**: Validates accessibility across tabletop campaign sessions (companion choice clarity, mechanical ruleset terminology), computer game chapters and playstyle routes (route-specific accessibility consistency, colorblind/audio/motor variant coverage), and RPG-specific content warnings (mechanical failure states, companion death/abandonment moments, faction betrayal consequences).

## Accessibility Principle

**Accessible content** = Readable by broad audience (ages 8–80, various reading abilities), appropriate content warnings provided, UI legible, no unnecessary jargon or ableist language.

**Accessibility barriers include**:
- ❌ High reading level (grade 16+ for general audience)
- ❌ Run-on sentences (40+ words without punctuation)
- ❌ Missing content warnings (violence, gore, trauma, strobe effects)
- ❌ Poor contrast (UI text hard to read on backgrounds)
- ❌ Ableist language ("crazy," "lame," "psycho," "schizo")
- ❌ Inaccessible description (no alt text for images/emojis in parser IF)

**Valid accessibility includes**:
- ✅ Grade 8–10 reading level (general audience)
- ✅ Mix of sentence lengths (avg 15–20 words)
- ✅ Content warnings at game start
- ✅ High contrast (WCAG AA minimum)
- ✅ Respectful language (no slurs, no ableist phrasing)
- ✅ Content descriptions (self-explanatory without prerequisite knowledge)

## User Input

```text
$ARGUMENTS
```

Accepted input:
- Nothing — full accessibility audit across all nodes
- `--readability-only` — check only reading level (skip warnings, contrast, language)
- `--warnings-only` — extract content warnings needed (skip reading level)
- `--contrast-only` — check UI contrast only
- `--language-only` — check for ableist/inaccessible language

- `--target-grade [N]` — custom target reading level (default: 8–10)
- `--strict` — flag any sentence >30 words
- `--show-violations` — display problematic text passages with suggestions
- `--content-warnings-template` — generate starter content warning block

## Pre-Execution Checks

**Extract Platform & Ruleset** (auto-detect RPG context):
- Read `.specify/memory/constitution.md` YAML frontmatter and extract `[PLATFORM]` and `[RULESET]`
- If `[PLATFORM]` = "Tabletop": Set `SESSION.is_rpg = "tabletop"` and load Tabletop accessibility validation
- If `[PLATFORM]` = "Computer Game": Set `SESSION.is_rpg = "computer"` and load Computer Game accessibility validation
- If neither detected: Set `SESSION.is_rpg = false` (generic accessibility model)
- Store `SESSION.platform` and `SESSION.ruleset` for RPG-specific accessibility checks

**Load RPG-Specific Documents** (if platform detected):
- **Tabletop**: Load `specs/companions.md` (for companion choice accessibility), `specs/mechanics-[ruleset].md` (for mechanical terminology clarity), `specs/factions.md` (for faction-specific content warnings)
- **Computer**: Load `specs/variables.md` (for route-specific accessibility), `specs/accessibility.md` (for existing accessibility variants)

**Standard Pre-Execution**:
1. Load all `draft/[ENGINE]/NODE-*.md` files
2. Load `specs/constitution.md` target audience
3. Load `specs/themes.md` if present (for content warning tracking)
4. Extract prose text (separate from code/syntax)
5. Check for UI/theme files (story.css, ink-theme.html) for contrast validation

## Execution Steps

### 1. **Measure Reading Level**

Flesch-Kincaid Grade Level per node:

```
Formula: 0.39 × (words/sentences) + 11.8 × (syllables/words) - 15.59

NODE-010 prose:
  "Marcus sits across from you, hands folded.
   His expression is unreadable. Something shifts in his eyes—
   a flicker of doubt? Understanding? You can't tell."
   
Analysis:
  Words: 43
  Sentences: 3
  Syllables: ~68
  Grade level: (0.39 × 14.3) + (11.8 × 1.58) - 15.59 = 6.2 (Grade 6)
  
Interpretation:
  • Grade 6 = ~12-year-old reading level
  • Accessible to most audiences ✅

NODE-015 prose:
  "The epistemological lacunae inherent in phenomenological discourse 
   regarding intersubjective intentionality necessitate a reconsideration 
   of the hermeneutic apparatus undergirding contemporary metaphysical 
   frameworks."
   
Analysis:
  Words: 32
  Sentences: 1
  Syllables: ~82
  Grade level: (0.39 × 32) + (11.8 × 2.56) - 15.59 = 16.8 (Grade 16+)
  
Interpretation:
  • Grade 16+ = College/academic reading level
  • Only accessible to highly educated readers ❌
  • Need to simplify for general audience
```

### 2. **Analyze Sentence Structure**

Check for run-on sentences and variety:

```
NODE-020 sentences:

1. "You push through the crowd." (6 words)
2. "Bodies press against you from all sides, shoulders colliding, 
   voices rising in cacophony, and you can barely breathe as 
   you fight forward through the sea of humanity." (40 words)
3. "The door is ahead." (4 words)

Analysis:
  • Sentence 1: Very short (6 words) ✅
  • Sentence 2: Run-on (40 words) ⚠️
  • Sentence 3: Very short (4 words) ✅
  
  Average: 17 words
  Variance: Good (4 → 40 → 4 creates rhythm)
  
Problem with Sentence 2:
  • 40 words without primary break is difficult to parse
  • Could be split: "Bodies press against you from all sides. Shoulders collide. 
    Voices rise in cacophony. You can barely breathe as you fight forward 
    through the sea of humanity."
    
Fix: Break at logical points (punctuation or clause boundaries)
```

### 3. **Detect Content Warnings Needed**

Flag sensitive content requiring disclosure:

```
Content warning categories:

VIOLENCE:
  • Gore/graphic description → Label: "Graphic Violence"
  • Combat/action → Label: "Violence"
  • Death of named character → Label: "Character Death"

PSYCHOLOGICAL:
  • Torture, abuse → Label: "Torture, Abuse"
  • Existential dread, body horror → Label: "Psychological Content"
  • Suicide/self-harm → Label: "Suicide, Self-Harm"
  • Trauma revisiting → Label: "Trauma Content"

SENSORY:
  • Flashing lights, strobe effects → Label: "Flashing Lights (Seizure Risk)"
  • Loud sudden noises → Label: "Loud Sound Effects"

CONTENT:
  • Sexual content → Label: "Sexual Content"
  • Drug/alcohol use → Label: "Drug Use, Alcohol"
  • Discrimination, slurs → Label: "Discrimination [specify]"
  • Animal harm/death → Label: "Animal Harm, Death"

Example NODE scan:

NODE-025: "Marcus bleeds out. His body jerks once, then stills. 
          You watch the light leave his eyes."
          
Warnings needed: "Character Death, Graphic Violence"

NODE-030: "Red lights pulse. Red lights pulse. Red lights pulse. 
          [This continues for 10 seconds in-game]"
          
Warnings needed: "Flashing Lights (Seizure Risk)" + explanation of duration
```

### 4. **Validate UI Contrast**

Check readability of on-screen text:

```
Contrast Check (WCAG standard):
  • AA (minimum): 4.5:1 for normal text, 3:1 for large text
  • AAA (enhanced): 7:1 for normal text, 4.5:1 for large text

Example (SugarCube CSS):

--color-text: #1a1a1a (near black)
--color-bg: #faf8f3 (off-white)

Contrast ratio: 14.2:1 ✅ EXCELLENT (AAA compliant)

---

Problematic example:

--color-text: #888888 (medium gray)
--color-bg: #999999 (slightly darker gray)

Contrast ratio: 1.1:1 ❌ FAIL (too low)
Issue: Text will be unreadable for colorblind and low-vision players
Fix: Either darken text or lighten background
```

### 5. **Scan for Ableist Language**

Identify harmful or exclusionary phrasing:

```
Ableist language examples to flag:

FLAGGED:
  ❌ "He's crazy" → Use: "He's unstable" or specific behavior
  ❌ "That's lame" → Use: "That's disappointing" or "ineffective"
  ❌ "Blind to the truth" → Use: "Unaware of" or "Missing"
  ❌ "Psycho killer" → Use: "Unstable person" or "Murderer"
  ❌ "Crippled economy" → Use: "Struggling economy" or "Weakened"
  ❌ "Deaf to reason" → Use: "Unwilling to listen" or "Stubborn"
  ❌ "Schizo behavior" → Use: "Fractured" or specific behavior description
  ❌ "Spaz out" → Use: "Lose control" or "Panic"
  ❌ "That's retarded" → Use: "That's slow" or "That's ineffective"
  ❌ "Leper" (slur) → Use: "Exile" or "Outcast" depending on context

ACCEPTABLE:
  ✅ "Blind rage" (metaphorical, common usage)
  ✅ "Crippling doubt" (metaphorical, accepted)
  ✅ Character describing their own disability: "I'm deaf. I read lips."
  ✅ Historical context slurs in dialogue (with content warning)

CONTEXT MATTERS:
  • When? Historical period, modern day, fantasy world?
  • Who? Character slur vs. narrator slur vs. game itself?
  • Why? Authentic to character or gratuitous?

Example NODE scan:

NODE-015: "The militia troops were deaf to reason and blind to mercy.
          Their leader was clearly insane."
          
  • "deaf to reason" → Metaphorical, acceptable ✅
  • "blind to mercy" → Metaphorical, acceptable ✅
  • "clearly insane" → Ableist, imprecise ⚠️
  
Fix: "Their leader was clearly unhinged" or "unstable"
```

### 6. **Generate Accessibility Audit Report**

Create `specs/accessibility-audit.md`:

```markdown
## Accessibility Audit

**Game**: [NAME]
**Target Audience**: [from constitution.md]
**Date**: [ISO]

### Reading Level Analysis

| Node | Grade Level | Target | Status |
|------|-------------|--------|--------|
| NODE-010 | 6.2 | 8–10 | ✅ Pass |
| NODE-015 | 16.8 | 8–10 | ❌ Too High |
| NODE-020 | 8.9 | 8–10 | ✅ Pass |
| NODE-025 | 9.1 | 8–10 | ✅ Pass |

Average game grade level: 10.2 (slightly high)
Recommended target: 8–10
Status: ⚠️ Review NODE-015

### Sentence Structure

| Node | Avg Length | Max Length | Variety | Status |
|------|-----------|-----------|---------|--------|
| NODE-010 | 14 | 22 | Good | ✅ Pass |
| NODE-015 | 28 | 45 | Poor | ⚠️ Review |
| NODE-020 | 16 | 40 | Fair | ⚠️ Review |
| NODE-025 | 12 | 18 | Good | ✅ Pass |

Guideline: Avg 12–18 words, max 30 words
Status: ⚠️ Some nodes need shortening

### Content Warnings Required

**Primary**:
- Character Death (Marcus: NODE-025)
- Graphic Violence (NODE-025, NODE-030)
- Psychological Content (NODE-032: existential crisis)

**Secondary**:
- Drug Use (NODE-018: militia drugs)
- Discrimination (NODE-020: slurs toward outsiders)

**Sensory**:
- None identified

Recommended opening warning:
"⚠️ Content Warning: This game contains character death, 
graphic violence, and psychological content."

### UI Contrast

| Element | Foreground | Background | Ratio | Standard | Status |
|---------|-----------|-----------|-------|----------|--------|
| Main text | #1a1a1a | #faf8f3 | 14.2:1 | AA (4.5:1) | ✅ AAA |
| Link text | #2563eb | #faf8f3 | 8.1:1 | AA | ✅ AAA |
| Button | #faf8f3 | #8b5cf6 | 5.3:1 | AA | ✅ AAA |

All contrast ratios meet WCAG AAA standard ✅

### Ableist Language

**Flagged** (2 instances):
1. NODE-015: "clearly insane" → suggest "unstable" or "unhinged"
2. NODE-020: "lame excuse" → suggest "weak excuse" or "pathetic"

**Acceptable** (3 instances):
1. NODE-010: "blind rage" (metaphorical) ✅
2. NODE-025: "deaf to pleas" (metaphorical) ✅
3. NODE-032: Character says "I'm crazy" (self-identification) ✅

### Recommendations

**Priority 1 (Readability)**:
1. NODE-015: Reduce grade level from 16.8 → 8–10
   - Simplify vocabulary (epistemological → concerning)
   - Break long sentences (40+ words → 25 max)

2. NODE-020: Reduce max sentence from 40 → 25 words
   - Break compound sentences with periods or semicolons

**Priority 2 (Language)**:
1. Replace "insane" with character-appropriate alternative
2. Replace "lame" with "weak" or "pathetic"

**Priority 3 (Polish)**:
1. Add explicit content warning block to opening
2. Consider audio description for key visual scenes
3. Test with colorblind simulation tools

### Accessibility Score: 7/10

Strong: Contrast ratios, content warnings identified
Weak: Reading level, sentence length, some ableist language
Improvements needed before release
```

### 7. **Show Violations** (optional with --show-violations)

Display problematic passages with fixes:

```
READABILITY VIOLATION: High Grade Level

NODE-015 (Grade 16.8):
  Passage:
    "The epistemological lacunae inherent in phenomenological discourse..."
  
  Problem:
    • "epistemological" (college-level: 5 syllables)
    • "lacunae" (rare plural: 3 syllables)
    • "phenomenological" (academic jargon: 6 syllables)
    • Grade 16.8 vs target 8–10
  
  Suggested rewrite:
    "The gaps in how we think about consciousness are becoming clear..."
  
  New grade level: 7.2 ✅

---

RUN-ON SENTENCE VIOLATION

NODE-020:
  Passage:
    "Bodies press against you from all sides, shoulders colliding, voices 
     rising in cacophony, and you can barely breathe as you fight forward 
     through the sea of humanity."
  
  Problem:
    • 40 words in single sentence
    • Multiple clauses linked by commas (hard to parse)
    • Reader loses breath before meaning is clear
  
  Suggested rewrite:
    "Bodies press against you from all sides. Shoulders collide. 
     Voices rise in cacophony. You can barely breathe as you fight 
     forward through the sea of humanity."
  
  Analysis:
    • Split into 4 sentences
    • Avg length: 10 words each
    • Now easier to read while maintaining rhythm

---

ABLEIST LANGUAGE VIOLATION

NODE-015:
  Passage:
    "The general was clearly insane, ordering troops to burn villages."
  
  Problem:
    • "insane" is ableist; conflates mental illness with evil
    • Imprecise (what specific behavior is insane?)
  
  Suggested rewrite:
    "The general was clearly unstable, ordering troops to burn villages."
  
  OR (more specific):
    "The general was clearly ruthless, ordering troops to burn villages."
```

### 8. **Content Warnings Template** (optional with --content-warnings-template)

Generate starter warning block:

```
# Content Warnings

This game contains the following content. 
If any of these are triggers for you, please proceed with caution.

**Violence**:
- Graphic violence (blood, injuries)
- Character death (multiple NPCs)
- Combat/action sequences

**Psychological**:
- Existential dread (NODE-032)
- Betrayal themes

**Other**:
- Drug use (mention, NODE-018)
- Discrimination and slurs (historical setting)

**Sensory**:
- None

**Not included**:
- Sexual content
- Animal harm
- Strobe lights
- Loud sudden noises

---

If you need to skip a section containing any of these elements, 
please let us know and we can suggest an alternate path.
```

### 9. **Report**

Output `accessibility-audit.md` with:
- Reading level analysis (grade level per node, average, target)
- Sentence structure analysis (length, variety, run-on detection)
- Content warnings needed (categorized, specific nodes)
- UI contrast validation (all UI elements checked)
- Ableist language scan (flagged terms, context analysis)
- If `--show-violations`: Problem passages with suggested rewrites
- If `--content-warnings-template`: Generated warning block ready to use

---

## RPG Campaign Accessibility Validation

### Tabletop Campaign Accessibility

#### 1. Companion Choice Clarity

**Validate accessibility of companion loyalty choice presentation**:
- Is it clear what each choice does to the relationship?
- Will players understand the loyalty consequence?
- Is the choice language free of ambiguity?

**Example check**:
```
SESSION-3, NODE-012 (Companion Loyalty Choice):
  
Choice A: "I trust Mira with this secret"
  Accessibility: ✅ Clear what trust means, clear consequence
  
Choice B: "I need to keep this between us"
  Accessibility: ⚠️ Ambiguous - does this mean you DON'T trust Mira?
                     Or means it's not about Mira at all?
  
Fix: "I can't tell Mira about this" (clearer that it's about secrecy, not trust)
```

**Content warnings for companion choices**:
- If a companion can die/abandon player → Warn at session start
- If a companion is betrayed → Warn if content is emotionally difficult
- If companion loyalty can become hostile → Warn about potential consequences

#### 2. Ruleset Mechanics Accessibility

**Validate clarity of ruleset-specific terminology**:
- Are D&D 5e ability scores (STR/DEX/CON/INT/WIS/CHA) explained clearly?
- Are Pathfinder 2e proficiency levels accessible to non-experts?
- Are Shadowrun 6e attribute names and karma mechanics understandable?

**Example check**:
```
D&D 5e Mechanics Text:
  "Make a DC 15 DEX save or take half damage"
  
Accessibility:
  • "DC 15" might not be clear to new D&D players
  • "DEX save" assumes knowledge of Dexterity = speed
  • "half damage" is clear
  
Fix: "Make a Dexterity save (DC 15 - like dodging a trap). 
      If you fail, you take damage; if you succeed, you take half."
```

**Content warnings for mechanical failures**:
- If a failed check causes a companion to be harmed → Warn
- If mechanical failure leads to "game over" state → Warn
- If ruleset mechanics could cause frustration (hard DCs, luck-based outcomes) → Note pacing

#### 3. Session Accessibility Tracking

**Ensure accessibility variants available across all sessions**:
- Colorblind mode available in Session 1-N (not just Session 1)
- Audio descriptions available in all sessions
- Motor accessibility (no time pressure in critical sessions)

**Example check**:
```
Session 1: ✅ Colorblind mode implemented (patterns visible)
Session 2: ✅ Colorblind mode working (NPC states shown with icons)
Session 3: ❌ Colorblind mode missing!
           NPC affiliation shown with colors only
           
Issue: Accessibility drops in Session 3
Fix: Apply colorblind patterns to Session 3 nodes
```

#### 4. Content Warnings for Campaign Structure

**Warn about campaign-level emotional beats**:
- "A companion may die at end of Module 2"
- "A faction you allied with may betray you"
- "Session 5 contains extended combat (90+ minutes)"

### Computer Game Accessibility

#### 1. Route-Specific Accessibility Consistency

**Ensure accessibility variants available in ALL playstyle routes**:

```
CHAPTER-2 Route Commit:

Stealth Route: ✅ Colorblind UI (patterns on guards)
               ✅ Audio mode (beep patterns for alert levels)
               ✅ Motor mode (no time pressure)

Combat Route:  ✅ Colorblind UI (patterns on enemies)
               ✅ Audio mode (beep patterns for health)
               ✅ Motor mode (auto-target option available)

Diplomacy Route: ❌ Colorblind UI (color-coded only)
                 ❌ Audio mode (no audio cues)
                 ✅ Motor mode (turn-based, no time pressure)
                 
Issue: Diplomacy route missing colorblind and audio variants
Fix: Implement colorblind patterns and audio cues for diplomacy route
```

**Content warnings per route**:
- "Stealth route: You must avoid violence" (content warning if violence is triggered)
- "Combat route: Contains frequent violence and enemy death"
- "Diplomacy route: Contains betrayal and potential loss of faction reputation"

#### 2. Chapter Pacing for Accessibility

**Validate chapter length doesn't exceed accessibility constraints**:

```
Chapter 3 Pacing:
  
Motor accessibility: Chapter 3 has 12 nodes with timed choices
                     ⚠️ Concern: Some motor disabilities need >3 sec per choice
                     
Audio accessibility: Chapter 3 dialogue is 20 minutes
                     ✅ OK: Average for chapter
                     
Cognitive accessibility: Chapter 3 has 4 major route choices
                        ⚠️ Concern: Decision fatigue in one chapter
                        
Fix: Extend Chapter 3 timing windows to 10 seconds (from 3)
     Add "summary" option before major route choices
```

#### 3. Accessibility Variant Content Warnings

**Warn about sensory accessibility features**:
- "Colorblind mode changes visual appearance (blue/red become patterns)"
- "Audio mode uses sound cues instead of visual indicators"
- "Motor accessibility uses text-based inputs instead of timed clicks"

#### 4. Route Balance for Accessibility

**Ensure no route is inherently more accessible than others**:

```
Stealth Route:  Grade level 8.2, colorblind OK, audio OK, motor OK
Combat Route:   Grade level 8.5, colorblind OK, audio OK, motor OK
Diplomacy Route: Grade level 9.1, ⚠️ colorblind missing, audio missing

Status: Diplomacy route less accessible
Fix: Implement colorblind and audio for diplomacy route
```

### Best Practices for RPG Accessibility

**Campaign-Level Considerations**:
- Content warnings should appear before SESSION-1 AND at major escalation points
- Companion death/abandonment should be foreshadowed if possible
- Mechanical difficulty (DCs, enemy stats) should scale with player progression

**Choice Accessibility**:
- Loyalty/reputation choices must have clear consequences stated
- Playstyle route commits should have summary options
- Time-limited choices should include accessibility alternatives (no time pressure option)

**Ruleset Clarity**:
- Define any ruleset-specific terms in SESSION-0-BRIEFING.md
- Explain failure consequences (what happens if you fail this check?)
- Provide character sheet templates with clear explanations

**Consistency Across Sessions/Chapters**:
- Accessibility features available in SESSION 1 must stay in SESSION 2-N
- Accessibility features in CHAPTER 1 must stay in CHAPTER 2-5
- Playstyle routes must have equal accessibility across all chapters

**Content Warning Specificity**:
- Instead of "Violence": "Combat encounters with enemy death descriptions"
- Instead of "Psychological content": "A companion may be betrayed or abandon you"
- Instead of "Difficult choices": "A faction choice with irreversible consequences"

---

## Important Notes

**Grade Level Is Approximate**: Flesch-Kincaid is useful but not perfect. Manual review is important.

**Context Matters for Language**: A character using an ableist slur in dialogue (especially period piece) might be intentional and acceptable. Narrator using it is different.

**Self-Identification Is Valid**: A character saying "I'm crazy" or "I'm deaf" is different from labeling them that way. Respect character voice.

**Test With Real Readers**: Best accessibility testing involves people from target audiences (various ages, abilities, backgrounds). Automated checks are baseline, not comprehensive.

**Warnings Are Spoiler-Free**: Content warnings shouldn't spoil plot. E.g., "Character death" is OK; "Marcus dies at NODE-25" is not.

**Contrast Extends to All Text**: Menu text, button text, link text—all need to meet contrast standards. Don't rely on white text on light backgrounds.

