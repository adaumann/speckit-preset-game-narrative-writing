---
description: Generate background image briefs and AI image-generation prompts for game narrative scenes. Focuses on environments, locations, and atmospheric settings without character emphasis. Can target a single node or compose a background from multiple nodes sharing a location. Reads outlines, locations.md, and world-building files to produce ready-to-paste prompts for Midjourney, DALL-E 3, Adobe Firefly, or Stable Diffusion.
handoffs:
  - label: Generate Illustration
    agent: speckit.illustrate
    prompt: Now generate a full character-focused illustration brief for this node using the same visual style
    send: false
  - label: Compile to Playable Output
    agent: speckit.compile
    prompt: Compile the game — background references are ready for embedding
    send: false
  - label: Review World-Building
    agent: speckit.revise
    prompt: Update location descriptions in world-building to match the visual references established in the background briefs
    send: false
---

# speckit.background

Generate background image briefs and AI image-generation prompts for game narrative environments. This command does not generate images — it produces everything needed to commission or generate background art:

1. **Background Brief** (`FEATURE_DIR/backgrounds/<NODE_ID>-bg.md`) — a full creative specification for the environment
2. **Image Generation Prompt** — a ready-to-paste prompt calibrated to the chosen style, color range, and aspect ratio
3. **Setting Details** — key visual elements from locations and world-building
4. **Atmospheric Notes** — lighting, weather, time of day, mood

## User Input

```text
$ARGUMENTS
```

You **MUST** consider the user input before proceeding (if not empty).

Accepted arguments:
- `--node <node-id>` — target a specific node (e.g., `A1.101`, `JO3.201`)
- `--scene all` — generate backgrounds for all drafted nodes
- `--scene <node-id> <node-id> ...` — compose a single background brief from multiple nodes sharing a location
- `--scene description` — generate background for a described environment (interactive mode)
- `--style [name]` — visual style preset (see Style Catalogue below)
- `--color [range]` — color range: `full` (default), `2color`, `greyscale`
- `--aspect [ratio]` — output aspect ratio: `landscape` (default), `portrait`, `square`
- `--type [variant]` — background type: `environment` (default), `interior`, `exterior`, `abstract`
- `--composite` — generate a single composite background brief merging multiple node contexts
- `prompt-only` — output only the image generation prompt, no brief document
- `brief-only` — generate the background brief document without writing an image prompt

---

## What speckit.background reads from existing files

| Source field | Where it reads |
|---|---|
| Location name | `outlines/<NODE_ID>-outline.md` and `locations.md` |
| Scene beats | `outlines/<NODE_ID>-outline.md` |
| Setting description | `locations.md` |
| Sensory anchors | `outlines/<NODE_ID>-outline.md` |
| World rules/visual motifs | `world-building.md` and `themes.md` |
| Mood/Atmosphere | `constitution.md` tone section |
| Lighting/palette defaults | `constitution.md` genre/tone/audience |

When `--composite` or multiple `--scene <id>` values are given:
- Group nodes by shared location (from `locations.md`)
- Merge sensory anchors, time-of-day ranges, and key visual elements
- Emit a single composite background brief covering the location across the specified nodes

---

## Style Catalogue

Each style preset defines a default approach optimized for background environments.

| Key | Style Name | Best for | Typical color range |
|---|---|---|---|---|
| `environment` | Environment Art | Fantasy, sci-fi, RPG worlds | Full color |
| `interior` | Interior Design | Indoor scenes, buildings, rooms | Full color |
| `landscape` | Landscape Painting | Open worlds, vistas, wilderness | Full color |
| `map` | Map/Diagram | Top-down views, region maps | 2-color or full |
| `tiled` | Tiled Background | 2D games, pixel art scenes | Full color |
| `watercolor` | Watercolor | Visual novels, literary games | Full color, soft |
| `inkwash` | Ink Wash | Dark/moody environments | Greyscale or 2-color |
| `silhouette` | Silhouette | Cinematic reveals, transitions | High contrast |
| `penandink` | Pen and Ink | Literary fiction, classics | Greyscale |
| `greyscale` | Greyscale | Interior art, budget | Full greyscale range |
| `2color` | Two-Color | Section dividers, cost-effective | Duotone |
| `minimalist` | Minimalist | Clean UI, modern | Limited palette |
| `cel` | Cel-Shaded Background | Anime games, visual novels | Flat colors, bold outlines |
| `anime` | Anime Background | Japanese-style games, VN backgrounds | Full color, gradient shading |
| `manga` | Manga Background | Manga-style games | Greyscale, screentones |
| `comic` | Comic Book Background | Superhero, pulp adventure | Halftones, bold inks |
| `painted` | Painted Environment | Concept art, fantasy RPGs | Full color, painterly |
| `pixelart` | Pixel Art Background | Retro games, 2D indie | Limited palette, pixel grid |
| `rpgmaker` | RPG Maker | 16-bit JRPG environments | Full color, tiled |
| `handpainted` | Hand-Painted | MMO, ARPG environments | Full color, textured |
| `rendered` | 3D Rendered | AAA games, realistic environments | Full color, photorealistic |
| `stylized3d` | Stylized 3D | Fortnite, Zelda: BotW environments | Full color, stylized |
| `dither` | Dither | Retro indie, pointilistic | Limited palette, dither |
| `vaporwave` | Vaporwave | Synthwave, cyberpunk, retro-futurism | Neon, gradients |
| `lowpoly` | Low Poly | Indie 3D, mobile games | Full color, faceted |
| `gothic` | Gothic | Dark fantasy, horror environments | Dark palette, dramatic |

If no `--style` is given, infer from genre + tone + target audience read from the spec.

---

## Color Range Options

| Option | Description | Best for |
|---|---|---|
| `full` (default) | Full color (CMYK/RGB) | Primary backgrounds, splash screens |
| `2color` | Two-color (black + 1 spot color) | Section dividers, budget printing |
| `greyscale` | Greyscale only | Atmospheric, noir, budget |

---

## Execution Steps

### Step 1 — Load Node Context

Load the following files if they exist in `FEATURE_DIR/`:
- `outlines/<NODE_ID>-outline.md` — extract: setting, beat sequence, sensory anchors
- `specs/[FEATURE_DIR]/draft/<NODE_ID>*.md` — if outline missing, extract from draft
- `locations.md` — extract: visual details for the scene's setting, architecture, geography
- `world-building.md` — extract: key visual symbols, colours, motifs, world rules
- `constitution.md` — extract: Tone, genre, target audience for mood guidance, plus YAML frontmatter fields `default_illustration_style`, `default_illustration_color_range`, `default_illustration_aspect`, `default_background_type` for visual defaults

If `--composite` or multiple scene IDs are given:
- Load each node's context
- Group by shared location name
- Merge sensory anchors, time ranges, and key elements

If no node files found for any specified ID, emit:
```
⚠️ No outline or draft found for [NODE_ID]. Skipping.
```

Build an internal **Background Seed** object:
```
Location:      [Location name]
Nodes:         [NODE_ID, NODE_ID, ...]
Type:          [interior / exterior / abstract]
Key Elements:  [3–7 architectural/geographic/atmospheric features]
Mood:          [3–5 adjectives from tone/sensory anchors]
Lighting:      [time of day, light sources, weather]
Palette:       [dominant colours, accent colours]
```

### Step 2 — Resolve Arguments

Parse `$ARGUMENTS` to set:
- `node` — required unless `--scene all`, `--scene description`, or multiple scene IDs
- `style` — infer from constitution.md `default_illustration_style` if set, else from genre/tone/target audience
- `color` — use constitution.md `default_illustration_color_range` if set, else `full`
- `aspect` — use constitution.md `default_illustration_aspect` if set, else `landscape`
- `type` — use constitution.md `default_background_type` if set, else `environment`

**Load defaults from constitution.md:**
- Read `constitution.md` YAML frontmatter for illustration config fields
- If `illustrations_enabled` is `no` or absent, emit a warning:
  ```
  ⚠️ Illustrations not enabled in constitution.md. Set illustrations_enabled: yes to persist these defaults.
  ```
  But still proceed with this run.

If `--scene all` is passed:
- Scan `outlines/` directory for all outline files
- Group by location where possible
- Generate background briefs for each location group
- Output summary at the end

If multiple `--scene <node-id>` values or `--composite`:
- Group nodes by location
- Generate one composite background brief per location

If `--scene description` is passed:
- Enter interactive mode to describe an environment
- Ask the user about all options
- Generate a single background brief

If no arguments are provided:
- Ask interactively for the node/location/environment to background
- Ask about style, color, aspect, type
- Use defaults for any missing options

### Step 3 — Setting Visual Details

Extract and consolidate setting information:
- Primary location from outline(s)
- Key visual elements from `locations.md`
- Architectural style, geography, vegetation
- Atmospheric details from sensory anchors
- Time of day and weather if specified
- Lighting conditions and dominant colours

If composite mode:
- Merge time-of-day ranges (e.g., "dusk to night")
- Combine seasonal/weather variations
- List elements unique to each node and shared across all

Output as:
```
### Setting Visual Details
**Location**: [Location name]
- Type: [interior / exterior / abstract]
- Key elements: [3–7 visual elements that must appear]
- Atmosphere: [lighting, weather, mood]
- Time of day: [range if composite, specific if single]
- Colours: [dominant palette]
```

### Step 4 — Background Image Prompt Construction

Build three prompt variants with color range consideration:

**Variant A — Wide Environment**: The full setting
Template:
```
[STYLE_MODIFIER], [COLOR_RANGE] background, [LOCATION_DESCRIPTION], [KEY_ELEMENTS], [LIGHTING], [MOOD_WORDS], environment, game background, [ASPECT_RATIO], no characters, no text, no letters, no watermark
```

**Variant B — Atmospheric Detail**: Close-up on a defining element
Template:
```
[STYLE_MODIFIER], [COLOR_RANGE] background, detail of [SPECIFIC_ELEMENT], [TEXTURE_OR_MATERIAL], [LIGHTING], [MOOD_WORDS], game art, [ASPECT_RATIO], no characters, no text
```

**Variant C — Mood/Ambient**: Atmospheric bleed, no distinct focal point
Template:
```
[STYLE_MODIFIER], [COLOR_RANGE] ambient background, [ATMOSPHERE], [LIGHTING], [COLOUR_PALETTE], [MOOD_WORDS], environmental concept, [ASPECT_RATIO], no figures, no text, soft focus
```

For each variant, also output:
- **Negative prompt**: `text, watermark, letters, signature, character, person, people, blurry, deformed, oversaturated, clipart`
- **Midjourney parameters**: `--ar [ratio] --style raw --stylize [value]`

### Step 5 — Write Background Brief

Write `FEATURE_DIR/backgrounds/<NODE_ID>-bg.md` (or `<LOCATION>-bg.md` for composites) with the following structure:
```markdown
# Background Brief: [NODE_ID / LOCATION]
<!-- Generated: [DATE] | speckit.background | Style: [STYLE] | Color: [COLOR] | Aspect: [RATIO] | Type: [TYPE] -->

---

## 1. Context

| Field | Value |
|---|---|
| Location | [NAME] |
| Nodes | [NODE_ID, ...] |
| Type | [interior / exterior / abstract] |
| Mood | [3–5 adjectives] |

---

## 2. Setting Visual Details

**Location**: [Location name]
- Key elements: [visual elements]
- Atmosphere: [lighting, weather, mood]
- Time of day: [if specified]
- Colours: [dominant palette]

---

## 3. Visual Style

**Style**: [STYLE_NAME]
[1–2 sentence rationale]

**Color Range**: [COLOR_RANGE]
[Rationale]

**Mood words**: [3–5 adjectives]

---

## 4. Image Generation Prompts

### Variant A — Wide Environment
```
[PROMPT A]
```
Negative: `[NEGATIVE PROMPT]`
MJ params: `[PARAMS]`

### Variant B — Atmospheric Detail
```
[PROMPT B]
```
Negative: `[NEGATIVE PROMPT]`
MJ params: `[PARAMS]`

### Variant C — Mood/Ambient
```
[PROMPT C]
```
Negative: `[NEGATIVE PROMPT]`
MJ params: `[PARAMS]`

---

## 5. Revision History
| Date | Change | By |
|---|---|---|
| [DATE] | Initial brief generated | speckit.background |
```

### Step 6 — Output Summary to Chat

After writing the file, output a condensed summary:
```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  BACKGROUND BRIEF — [NODE_ID / LOCATION]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  Location : [NAME]
  Nodes    : [NODE_ID, ...]
  Type     : [TYPE]
  Style    : [STYLE_NAME]
  Color    : [COLOR_RANGE]
  Aspect   : [RATIO]
  MOOD     : [mood words]
  IMAGE PROMPT — Variant A (recommended first pass):
  ──────────────────────────────────────────────────
  [FULL PROMPT A]
  Negative: [NEGATIVE PROMPT]
  Full brief with all 3 variants saved → FEATURE_DIR/backgrounds/[NODE_ID]-bg.md
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

If `prompt-only` was passed, output only the prompt block and stop.
If `brief-only` was passed, skip chat output and write only the file.

### Step 7 — Handle Placeholder Reference

After writing the background brief, create a placeholder reference comment for the draft file(s):
- For each node, add: `<!-- background: <NODE_ID>-bg.md -->`
  - Insert at the beginning of the node content (after any node header)
  - If the draft file doesn't exist, note: "⚠️ Draft file not found — add `<!-- background: <NODE_ID>-bg.md -->` manually when draft is created."

---

## File Naming for Export Integration

**Background Brief Files**:
| File Location | Naming Pattern |
|---|---|
| `backgrounds/` | `<NODE_ID>-bg.md` or `<LOCATION_NAME>-bg.md` (e.g., `A1.101-bg.md`, `Throne_Room-bg.md`) |

When you compile the game:
- If `illustrations_enabled: yes` in constitution.md, the compiler automatically scans `assets/illustrations/` for `<NODE_ID>.png` files and embeds them at the start of each matching node
- Background briefs guide the image creation process; generated PNG files should be placed in `assets/illustrations/`

---

## Constraints
- **Read-only for source files** — spec.md, constitution.md, outlines, and location files are never modified
- **No character emphasis** — backgrounds should not feature characters prominently; use `speckit.illustrate` for character-focused scenes
- **No image generation** — this command produces briefs and prompts; actual image generation requires an external tool
- **Style consistency** — use the same style across all backgrounds for visual coherence
- **Location consistency** — maintain consistent architectural/geographic details across all backgrounds featuring the same location
