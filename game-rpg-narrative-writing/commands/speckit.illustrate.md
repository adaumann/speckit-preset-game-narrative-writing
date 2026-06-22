---
description: Generate detailed illustration briefs and AI image-generation prompts for game narrative scenes. Creates scene illustrations and full-page interior art. Focuses on game-appropriate visual styles. Reads existing spec.md, constitution.md, outlines, and character/world-building files to produce game-ready visual direction. Outputs illustration-brief.md with character descriptions, setting details, mood, and ready-to-paste prompts for Midjourney, DALL-E 3, Adobe Firefly, or Stable Diffusion.
handoffs:
  - label: Compile to Playable Output
    agent: speckit.compile
    prompt: Compile the game with the new illustration briefs available for reference
    send: false
  - label: Revise Character Descriptions
    agent: speckit.revise
    prompt: Update character prose descriptions to better match the visual references established in the illustration briefs
    send: false
  - label: Review Visual Consistency
    agent: speckit.polish
    prompt: Check that prose descriptions across all nodes are consistent with the visual references in illustration briefs
    send: false
---

# speckit.illustrate

Generate illustration briefs and AI image-generation prompts for game narrative scenes. This command does not generate images — it produces everything needed to commission or generate scene illustrations:

1. **Illustration Brief** (`FEATURE_DIR/illustrations/<NODE_ID>-brief.md`) — a full creative specification for the scene illustration
2. **Image Generation Prompt** — a ready-to-paste prompt calibrated to the chosen style, color range, and aspect ratio
3. **Character Reference** — visual cues for characters present in the scene
4. **Setting Details** — key visual elements from locations and world-building

## User Input

```text
$ARGUMENTS
```

You **MUST** consider the user input before proceeding (if not empty).

Accepted arguments:
- `--node <node-id>` — target a specific node (e.g., `A1.101`, `JO3.201`)
- `--scene all` — generate illustrations for all drafted nodes
- `--scene description` — generate illustration for a scene description (interactive mode)
- `--style [name]` — visual style preset (see Style Catalogue below)
- `--color [range]` — color range: `2color` (default), `full`, `greyscale`
- `--aspect [ratio]` — output aspect ratio: `portrait` (default), `landscape`, `square`
- `prompt-only` — output only the image generation prompt, no brief document
- `brief-only` — generate the illustration brief document without writing an image prompt

---

## What speckit.illustrate reads from existing files

| Source field | Where it reads |
|---|---|
| Node title | `outlines/<NODE_ID>-outline.md` or `specs/[FEATURE_DIR]/draft/<NODE_ID>*.md` |
| Scene beats | `outlines/<NODE_ID>-outline.md` |
| POV character | `outlines/<NODE_ID>-outline.md` |
| Setting | `outlines/<NODE_ID>-outline.md` and `locations.md` |
| Characters present | `outlines/<NODE_ID>-outline.md` and `characters/*.md` |
| Mood/Atmosphere | `constitution.md` tone section and scene sensory anchors |
| Key imagery | `world-building.md` and `themes.md` |
| Default visual style | `constitution.md` genre/tone/audience |

---

## Style Catalogue

Each style preset defines a default approach optimized for game narrative illustrations.

| Key | Style Name | Best for | Typical color range |
|---|---|---|---|---|
| `penandink` | Pen and Ink | Literary fiction, visual novels, MG | Greyscale with line weight variation |
| `2color` | Two-Color | Node openers, section dividers | Duotone (black + 1 accent colour) |
| `greyscale` | Greyscale | Interior illustrations, budget printing | Full greyscale range |
| `woodcut` | Woodcut | Historical, horror, dark fantasy | High contrast black/white |
| `lineart` | Line Art | MG, node headers, decorative | Single color line work |
| `engraving` | Copperplate Engraving | Period pieces, literary | Cross-hatching, greyscale |
| `artnouveau` | Art Nouveau | Fantasy, historical romance | 2-color with flowing lines |
| `artdeco` | Art Deco | 1920s-1930s settings, noir | 2-color geometric style |
| `vintage` | Vintage Game Style | Period pieces, nostalgia | Sepia or 2-color vintage |
| `minimalist` | Minimalist | Contemporary, literary | Limited palette, clean lines |
| `conceptart` | Concept Art | Fantasy, sci-fi, RPGs | Full color, rendered |
| `pixelart` | Pixel Art | Retro games, indie | Limited palette, pixel grid |
| `cel` | Cel-Shaded | Anime games, visual novels, JRPGs | Flat colors, bold outlines |
| `anime` | Anime | Japanese-style games, visual novels | Full color, gradient shading |
| `manga` | Manga | Manga-style games, cutscene panels | Greyscale, screentones |
| `comic` | Comic Book | Superhero, action, adventure games | Halftones, bold inks, full color |
| `retrocomic` | Retro Comic | Period superhero, pulp adventure | Dot screen, primary colors |
| `graphicnovel` | Graphic Novel | Mature narrative games, noir | Painted panels, rich color |
| `westerncartoon` | Western Cartoon | Kids games, comedy, platformers | Exaggerated, bold colors |
| `rpgmaker` | RPG Maker | 16-bit JRPG, indie retro | Full color, tiled sprites |
| `handpainted` | Hand-Painted | MMO, ARPG (WoW, Torchlight style) | Full color, textured |
| `rendered` | 3D Rendered | AAA games, cinematic cutscenes | Full color, photorealistic |
| `stylized3d` | Stylized 3D | Fortnite, Overwatch, Zelda: BotW | Full color, stylized shading |
| `dither` | Dither | Retro indie, pointilistic shading | Limited palette, dither pattern |
| `silhouette` | Silhouette | Cinematic reveals, transitions | High contrast black/color |

If no `--style` is given, infer from genre + tone + target audience read from the spec.

---

## Color Range Options

| Option | Description | Best for |
|---|---|---|
| `full` | Full color (CMYK/RGB) | Premium editions, children's games, splash screens |
| `2color` | Two-color printing (black + 1 spot color) | Node openers, section dividers, most adult games |
| `greyscale` | Greyscale only | Interior illustrations, mass market, budget |

The color range affects the prompt construction and palette recommendations.

---

## Execution Steps

### Step 1 — Load Node Context

Load the following files if they exist in `FEATURE_DIR/`:
- `outlines/<NODE_ID>-outline.md` — extract: node title, POV character, setting, beat sequence, sensory anchors
- `specs/[FEATURE_DIR]/draft/<NODE_ID>*.md` — if outline missing, extract from draft
- `characters/<pov_character>.md` — extract: appearance, clothing style, distinguishing features
- `locations.md` — extract: visual details for the scene's setting
- `world-building.md` — extract: key visual symbols, colours, motifs
- `constitution.md` — extract: Tone, genre, target audience for mood guidance, plus YAML frontmatter fields `default_illustration_style`, `default_illustration_color_range`, `default_illustration_aspect` for visual defaults

If the node file is missing, emit:
```
⚠️ No outline or draft found for [NODE_ID]. Cannot generate illustration brief.
```

Build an internal **Illustration Seed** object:
```
Node:       [NODE_ID] — [Node Title]
POV Character: [Character name]
Setting:       [Location name]
Key Beats:     [3–5 key visual moments from beat sequence]
Mood:          [3–5 adjectives from tone/sensory anchors]
Characters:    [List of characters present with brief appearance notes]
Key Objects:   [Important items from the scene]
```

### Step 2 — Resolve Arguments

Parse `$ARGUMENTS` to set:
- `node` — required unless `--scene all` or `--scene description`
- `style` — infer from constitution.md `default_illustration_style` if set, else from genre/tone/target audience
- `color` — use constitution.md `default_illustration_color_range` if set, else `2color`
- `aspect` — use constitution.md `default_illustration_aspect` if set, else `portrait`

**Load defaults from constitution.md:**
- Read `constitution.md` YAML frontmatter for illustration config fields
- If `illustrations_enabled` is `no` or absent, emit a warning:
  ```
  ⚠️ Illustrations not enabled in constitution.md. Set illustrations_enabled: yes to persist these defaults.
  ```
  But still proceed with this run.
- Use `default_illustration_style`, `default_illustration_color_range`, `default_illustration_aspect` as fallback defaults before inferring

If `--scene all` is passed:
- Scan `outlines/` directory for all outline files
- Generate illustration briefs for each in sequence
- Output summary at the end

If `--scene description` is passed:
- Enter interactive mode to describe a scene
- Ask the user interactively about all options (style, color, aspect, output mode)
- Generate a single illustration brief from the description

If no arguments are provided:
- Ask the user interactively for the node/scene to illustrate
- Ask about style, color, aspect, output mode
- Use defaults for any missing options

### Step 3 — Character Visual Reference

For each character present in the scene:
- Extract appearance details from `characters/<name>.md`
- Note distinguishing features, clothing style, typical expressions
- Record any visual motifs or symbolic elements associated with them

Output as:
```
### Character Visual References
**[Character Name]** (POV):
- Appearance: [age, build, hair, eyes, distinguishing features]
- Clothing: [typical attire, colours, style]
- Expression: [usual expression, emotional state in this scene]
- Visual cues: [symbols, accessories, posture notes]
```

### Step 4 — Setting Visual Details

Extract setting information:
- Primary location from outline
- Key visual elements from `locations.md`
- Atmospheric details from sensory anchors
- Time of day and weather if specified

Output as:
```
### Setting Visual Details
**Location**: [Location name]
- Key elements: [3–5 visual elements that must appear]
- Atmosphere: [lighting, weather, mood]
- Time of day: [if specified]
```

### Step 5 — Image Generation Prompt Construction

Build three prompt variants with color range consideration:

**Color Range Modifiers**:
- `full` — full color illustration
- `2color` — two-color printing (black + 1 accent colour)
- `greyscale` — greyscale only

**Variant A — Hero Moment**: The pivotal visual moment of the scene
Template:
```
[STYLE_MODIFIER], [COLOR_RANGE] illustration, [CHARACTER_DESCRIPTION], [SETTING_DESCRIPTION], [KEY_ACTION_OR_EMOTION], [LIGHTING], [MOOD_WORDS], book illustration, [ASPECT_RATIO], no text, no letters, no watermark
```

**Variant B — Environmental**: Setting and atmosphere dominant
Template:
```
[STYLE_MODIFIER], [COLOR_RANGE] illustration, [SETTING_DESCRIPTION], [ATMOSPHERIC_DETAILS], [LIGHTING], [MOOD_WORDS], book illustration, [ASPECT_RATIO], no figures, no text
```

**Variant C — Character Study**: Close-up or medium shot of a character
Template:
```
[STYLE_MODIFIER], [COLOR_RANGE] illustration, portrait of [CHARACTER_DESCRIPTION], [EXPRESSION], [LIGHTING], [MOOD_WORDS], book illustration, [ASPECT_RATIO], no text
```

For each variant, also output:
- **Negative prompt**: `text, watermark, letters, signature, blurry, deformed, oversaturated, childish, clipart, color bleed`
- **Midjourney parameters**: `--ar [ratio] --style raw --stylize [value]`

### Step 6 — Write Illustration Brief

Write `FEATURE_DIR/illustrations/<NODE_ID>-brief.md` with the following structure:
```markdown
# Illustration Brief: [NODE_ID] — [Node Title]
<!-- Generated: [DATE] | speckit.illustrate | Style: [STYLE] | Color: [COLOR] | Aspect: [RATIO] -->

---

## 1. Scene Context

| Field | Value |
|---|---|
| Node ID | [NODE_ID] |
| Node Title | [TITLE] |
| POV Character | [CHARACTER] |
| Setting | [LOCATION] |
| Key Beats | [3–5 visual moments] |

---

## 2. Character Visual References

**[Character Name]** (POV):
- Appearance: [details]
- Clothing: [style, colours]
- Expression: [emotional state]
- Visual cues: [symbols, accessories]

---

## 3. Setting Visual Details

**Location**: [Location name]
- Key elements: [visual elements]
- Atmosphere: [lighting, weather, mood]
- Time of day: [if specified]

---

## 4. Visual Style

**Style**: [STYLE_NAME]
[1–2 sentence rationale]

**Color Range**: [COLOR_RANGE]
[Printing consideration note]

**Mood words**: [3–5 adjectives]

---

## 5. Image Generation Prompts

### Variant A — Hero Moment
```
[PROMPT A]
```
Negative: `[NEGATIVE PROMPT]`
MJ params: `[PARAMS]`

### Variant B — Environmental
```
[PROMPT B]
```
Negative: `[NEGATIVE PROMPT]`
MJ params: `[PARAMS]`

### Variant C — Character Study
```
[PROMPT C]
```
Negative: `[NEGATIVE PROMPT]`
MJ params: `[PARAMS]`

---

## 6. Revision History
| Date | Change | By |
|---|---|---|
| [DATE] | Initial brief generated | speckit.illustrate |
```

### Step 7 — Output Summary to Chat

After writing the file, output a condensed summary directly in the chat:
```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  ILLUSTRATION BRIEF — [NODE_ID]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  Node : [NODE_ID] — [Title]
  Style   : [STYLE_NAME]
  Color   : [COLOR_RANGE]
  Aspect  : [RATIO]
  MOOD    : [mood words]
  IMAGE PROMPT — Variant A (recommended first pass):
  ──────────────────────────────────────────────────
  [FULL PROMPT A — paste into Midjourney / DALL-E 3 / Firefly]
  Negative: [NEGATIVE PROMPT]
  Full brief with all 3 variants saved → FEATURE_DIR/illustrations/[NODE_ID]-brief.md
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

If `prompt-only` was passed, output only the prompt block and stop (do not write illustration-brief.md).
If `brief-only` was passed, skip Step 7 chat output and write only the file.

### Step 8 — Handle Placeholder Reference

After writing the illustration brief, create a placeholder reference comment for the draft file:
- Add an illustration comment to the draft file: `<!-- illustration: <NODE_ID>-brief.md -->`
  - Insert at the beginning of the node content (after any node header)
  - If the draft file doesn't exist yet, note in the output: "⚠️ Draft file not found — add `<!-- illustration: <NODE_ID>-brief.md -->` manually when draft is created."

---

## File Naming for Export Integration

Illustration files must follow specific naming conventions for proper export integration:

**Interior Illustration Files**:
| File Location | Naming Pattern |
|---|---|
| `illustrations/` | `<NODE_ID>-brief.md` (e.g., `A1.101-brief.md`, `A2.201-brief.md`) |

When you compile the game:
- If `illustrations_enabled: yes` in constitution.md, the compiler automatically scans `assets/illustrations/` for `<NODE_ID>.png` files and embeds them at the start of each matching node
- Illustration briefs guide the image creation process; generated PNG files should be placed in `assets/illustrations/`

---

## Constraints
- **Read-only for source files** — spec.md, constitution.md, outlines, and character files are never modified
- **No image generation** — this command produces briefs and prompts; actual image generation requires an external tool
- **Style consistency** — use the same style across all illustrations for visual coherence
- **Character consistency** — maintain consistent character appearance across all illustrations featuring them
