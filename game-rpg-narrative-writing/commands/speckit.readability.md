---
description: Narrative flow analyzer — measure pacing, reading time, emotional beat trajectory, and tonal consistency across branches. Detects info dumps, tonal whiplash, draggy sections, rushed climax, and manipulative tone. Combines former speckit.pacing + speckit.tone.
handoffs:
  - label: Revise Flow
    agent: speckit.revise
    prompt: Some sections have pacing or tone issues flagged in the readability audit. Please adjust.
    send: true
  - label: Check Branching
    agent: speckit.branching
    prompt: After readability analysis, verify choice consequences across branches.
    send: false
---

# speckit.readability

Narrative flow analyzer — measures **word count, beat spacing, emotional tempo, reading time, and tone trajectory** across all branches. Formerly two separate commands (`speckit.pacing` + `speckit.tone`).

## Principles

**Good pacing** = Emotional beats, prose length, and scene changes maintain consistent reading rhythm; player never feels bored or overwhelmed.  
**Earned tone** = Emotional moment feels deserved based on prior build-up and character development.  
**Tonal whiplash** = Abrupt shift in emotional temperature without transition.  
**Hollow emotion** = Moment claims emotional weight but hasn't been set up.

### Problems detected

- Info dump (1,000+ word exposition block with no dialogue/action)
- Draggy middle (sequences where nothing changes)
- Rushed climax (disproportionately short payoff vs build-up)
- Dead zones (low word count AND no emotional/mechanical change)
- Tonal whiplash (abrupt emotional shift without transition)
- Hollow emotion (emotional beat without groundwork)
- Manipulative tone (guilt-tripping without story justification)

## User Input

```text
$ARGUMENTS
```

Accepted input:
- Nothing — analyze full game pacing and tone
- Branch ID (e.g., `BRANCH-A`) — scope to one branch
- `--act [N]` — scope to a single act
- `--node [NODE-ID]` — analyze one node in detail

- `--strict` — flag any node >2,500 wc or <100 wc; flag any tonal shift as requiring explanation
- `--target-wc [NUMBER]` — custom target word count per node (default: 800)
- `--emotional-only` — focus only on high-emotion moments
- `--show-stats` — display full statistics table
- `--show-graph` — ASCII graph of word count per node
- `--show-arcs` — display emotional arc visualization per branch

## Pre-Execution Checks

1. Load `specs/constitution.md`: Tone (§VII), Target Audience, Tense
2. Load `specs/plan.md`: Act structure, node sequence per branch, target reading time
3. Load all `specs/[FEATURE_DIR]/draft/[ENGINE]/NODE-*.md` files
4. Parse node prose (exclude YAML frontmatter)
5. Identify emotional beat markers (dialogue, action, revelation)
6. Load `specs/themes.md` if present: Thematic resonance expectations

## Execution Steps

### 1. Define Expected Tone Baseline

From `constitution.md` §VII Tone, identify baseline emotional temperature:

```
Constitution Tone: "Dark fantasy with dark humor"
Baseline temperature: DARK
Allowed movements: Dark → Darker, Dark → Darkly Comic, Dark → Quiet
Forbidden: Dark → Heartwarming without prior setup
```

### 2. Measure Word Count & Categorize

```asciidoc
Weight categories:
  MAJOR (climax, major choice, major revelation):   1,500–3,000 wc
  MODERATE (development, dialogue, moderate stakes):   800–1,500 wc
  MINOR (transition, decision point, brief scene):     300–800 wc
  MICRO (navigation, brief exchange, mechanical):       50–300 wc
```

### 3. Identify Emotional Beats

Tag each node's emotional moments:

```
NODE-010: "You find Marcus bleeding on the steps."
  → EMOTIONAL BEAT: Betrayal + Loss
  → Temperature: SHARP COLD (trust broken)
  → Build-up: Node-005 (Marcus vouched for you), Node-007 (gave you intel)
  → Earned? YES (3 nodes of relationship building)
```

### 4. Map Emotional Arc Per Branch

Create beat-by-beat emotional trajectory with temperature scale:

```
BRANCH A: Help Victor
NODE-005:  Baseline (neutral)           ≈ 0°
NODE-010:  Relationship deepens         ↑ +2° (warm)
NODE-012:  Danger escalates             ↓ -2° (tense)
NODE-015:  Critical choice point        ↓ -3° (climactic tension)
           → Choose to help (compassion)
NODE-020:  Victor escapes safely        ↑ +2° (relief + triumph)
NODE-025:  Meeting Victor's daughter    ↑ +1° (warmth, earned)
ENDING:    "You find peace together"    ↑ +1° (bittersweet closure)
Trajectory: Trough-and-rise (tension → relief → earned warmth)
```

### 5. Detect Problems

#### 🔴 Info Dump
`NODE-012`: 2,100 wc backstory monologue with 5% dialogue, 0% action. Break into 2–3 scenes.

#### 🔴 Tonal Whiplash
`NODE-020` (grief -4°) → `NODE-021` (comedy +3°): 7° swing with no transition. Add grief acknowledgment before comedy.

#### 🟡 Draggy Middle
`NODE-013→014→015`: 530 wc across 3 nodes with no emotional/mechanical change. Combine or add decision point.

#### 🟡 Hollow Emotion
`NODE-025`: "I love you" with no prior romantic build-up. Add vulnerable moment before declaration.

#### 🟠 Rushed Climax
Build-up: 4,200 wc → Climax: 500 wc (8.4:1 ratio, should be 3–5:1). Expand to 1,500+ wc.

#### 🟠 Manipulative Tone
Narrator shames player for reasonable choice without foreshadowing. Either add foreshadowing or remove shame language.

#### 💨 Dead Zone
`NODE-018`: 85 wc transition with no emotional/mechanical change. Delete or merge.

#### 📊 Inconsistent Node Size
Similar-weight scenes vary 300–2,800 wc. Justify or normalize to 800–1,200 wc.

### 6. Calculate Reading Time

```
Standard: 200–250 wpm
BRANCH A: 6,600 wc = 26–33 min
Target (from constitution): 30 min → ✅ ON TARGET
```

### 7. Generate Audit Report

Output `readability-audit.md` with:
- Branch pacing summary (total words, avg node, reading time per branch)
- Node length analysis (weight vs actual word count)
- Emotional arc per branch (temperature chart, beat table)
- Problem list grouped by severity (🔴/🟡/🟠/💨/📊)
- Tonal violation list (whiplash, hollow, manipulative)
- Thematic alignment analysis
- Recommendations prioritized by impact
- If `--show-stats`: full statistics distribution
- If `--show-graph`: ASCII word count visualization per branch
- If `--show-arcs`: visual temperature charts per branch

## Important Notes

**Word count ≠ quality**: A 300-word emotional climax can work if prose is dense. Judge by reading experience, not numbers.

**Tone shifts aren't inherently bad**: Tonal variation (dark humor, bittersweet) is legitimate. The issue is abruptness and lack of justification.

**Branch variance is OK**: Different branches can have different word counts and emotional arcs (one optimistic, one tragic). Each branch must be internally coherent.

**Reading speed varies**: Non-native readers and accessibility needs affect perceived pacing. Adjust for target audience.
