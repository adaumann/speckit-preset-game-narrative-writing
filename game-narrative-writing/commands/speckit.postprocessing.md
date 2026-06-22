---
description: Interactive postprocessing script generator. Guides the user through selecting visual/structural effects (animations, headers, act openings, HUD, backgrounds, etc.), asks clarifying questions about each choice, and builds a deterministic Python script in specs/[FEATURE_DIR]/postprocessing/. The script runs automatically on every speckit.export and speckit.compile.
handoffs:
  - label: Compile to see results
    agent: speckit.compile
    prompt: Compile the game to apply the postprocessing script and see the visual changes
    send: true
  - label: Export then compile
    agent: speckit.export
    prompt: Run export to regenerate boilerplate, then compile to apply postprocessing
    send: false
  - label: Refine postprocessing
    agent: speckit.postprocessing
    prompt: I want to change or extend the postprocessing script — add another visual effect
    send: false
---

# speckit.postprocessing

Run an **interactive session** that builds a deterministic Python postprocessing script. The script is saved to `specs/[FEATURE_DIR]/postprocessing/` and runs automatically on every subsequent `speckit.export` and `speckit.compile`, transforming `.twee` files in-place before Tweego compiles them.

**Key principle**: The generated script is **deterministic** — no AI, no LLM calls at runtime. The AI writes the script once during this interactive session; the script runs as plain Python on every subsequent compile.

## User Input

```text
$ARGUMENTS
```

If **input is provided** (e.g. `"add a typewriter animation to all text"`, `"gold bar header with quest hud"`, `"fade in and parallax background"`): skip the interactive menu and go straight to **Step 2 — Category Selection**, mapping the description to one or more categories below. Then proceed with follow-up questions for each identified category.

If **empty**: start the interactive session from Step 1.

## Pre-Execution Checks

1. **Verify the spec exists**: Confirm `specs/[FEATURE_DIR]/` has a valid project (constitution.md at minimum).
2. **Read constitution.md**: Extract engine target (sugarcube/ink), theme (dark/light/minimal), story_name.
3. **List existing scripts**: Check `specs/[FEATURE_DIR]/postprocessing/*.py`. Show them to the user at session start. If a script with the same name as the intended output already exists, warn and ask before overwriting.
4. **Check engine**: SugarCube vs. Ink determines the technical approach. SugarCube uses `StoryStylesheet [stylesheet]` passages; Ink uses `<style>` in the HTML wrapper. Note the engine and adjust all generated code accordingly.
5. **Read variables.md**: Scan for available `$character.*`, `$inventory`, `$quest*` variables so HUD generation can reference real variable names.
6. **Scan assets**: Check `assets/illustrations/` and `assets/backgrounds/` for available images.

---

## Interactive Session

### Step 1 — Welcome & Effect Menu

If no arguments were given, display:

```
═══════════════════════════════════════════
   POSTPROCESSING — Effect Builder
═══════════════════════════════════════════

  Choose one or more effects to add to your
  postprocessing script. You can combine
  multiple effects — they'll be merged into
  a single .py file.

  1  header — Passage headers, footers, breadcrumbs
  2  animation — CSS animations & transitions
  3  act-opening — Title cards & scene transitions
  4  hud — Custom HUD, stats, quest tracker
  5  background — Background images, gradients, effects
  6  other — Fonts, sound, accessibility, custom JS
  q  quit — Cancel and do nothing

  Type a number, a name, or comma-separated list.
  Examples: "2" | "animation, header" | "1,3,4"
```

- Accept numbers, names, or comma-separated combinations.
- For each selected effect, enter the **follow-up dialogue** for that category (Steps 2a–2f below).
- After each effect is configured, ask: *"Add another effect? (y/n)"* — if yes, show the menu again. If no, proceed to Step 3.

If the user typed `q` at any prompt, exit with: `Postprocessing cancelled. No files were changed.`

### Step 2 — Effect Configuration

For each selected category, conduct the follow-up dialogue:

---

### 2a. Header Effect

Ask these questions in order:

```
  ── Header setup ──

  1  What type of header?
     a) passageHeader / passageFooter widgets (injected into every passage)
     b) Breadcrumb trail (e.g. "Act I > Chapter 2 > The Forest")
     c) Visual bar (coloured bar with chapter/passage name)
     d) Custom (describe what you want)

  2  What visual style? (for options b/c/d)
     - Background colour / gradient?
     - Text colour?
     - Font?
     - Border style?
     - Height / padding?

  3  Should headers appear on every passage, or only specific ones?
     a) Every passage
     b) Only passages tagged [header] or [act-opening]
     c) Only passages matching a pattern (e.g. NODE-*)

  4  Footer behaviour:
     a) No footer (just header)
     b) Footer with "Continue" button
     c) Footer with page counter (e.g. "Page 3 of 12")
     d) Footer with breadcrumb
```

Based on answers, generate a script that:
- Injects `<<passageHeader>>` / `<<passageFooter>>` widget calls after each matching `:: PassageName` line
- Generates the corresponding `<<widget "passageHeader">>` and `<<widget "passageFooter">>` definitions in `widgets.twee`
- Injects CSS into `StoryStylesheet` for visual styling
- For breadcrumbs: inject a `<<breadcrumbs>>` widget that reads `$currentAct`, `$currentChapter`, and renders a styled trail

---

### 2b. Animation Effect

First determine the **implementation strategy**:

```
  ── Animation setup ──

  Implementation:
    1  Pure CSS (@keyframes + animation properties) — simplest, most reliable
    2  SugarCube widget-driven (<<typewriter>>, <<timed>>, custom widgets) — more control

  Which elements to animate?
    a) Passage entrance (when a new passage loads)
    b) Choice buttons (hover, appear)
    c) Links (hover effects)
    d) Background (parallax, ambient motion)
    e) Text content (typewriter, staggered reveal)
    f) Special elements (screen shake, glitch, dream sequences)
    g) Page transitions (between passages)
```

#### If Pure CSS (option 1):

Show the animation catalogue:

```
  ── CSS Animation Catalogue ──

  Code     Animation        Speed    Best for
  ─────────────────────────────────────────────────────
  fade     Fade in          0.4s     Default, works everywhere
  slideUp  Slide up         0.4s     Default, feels natural
  slideDn  Slide down       0.4s     Dramatic entrance
  slideL   Slide from left  0.4s     Side-panel feel
  slideR   Slide from right 0.4s     Side-panel feel
  scale    Scale in         0.4s     Cinematic zoom
  blur     Blur in          0.5s     Dream / memory scenes
  rot      Fade + rotate    0.5s     Whimsical / magical
  stagger  Staggered choices 0.3s ea Professional feel
  hoverS   Hover scale      0.2s     Link feedback
  hoverG   Hover glow       0.2s     Magical links
  hoverU   Underline slide  0.3s     Elegant links
  pulse    Pulse/Heartbeat  2.0s     Key items, warnings
  shake    Screen shake     0.3s     Explosions, impacts
  parallax Parallax bg      —        Immersive depth
  zoomBg   Slow zoom bg     20s      Cinematic background
  ambient  Gradient shift   10s      Dynamic atmosphere
  rain     Rain/snow        3s       Weather overlay
  glitch   Glitch effect    0.3s     Corruption, horror
  dream    Dreamy reveal    1.0s     Flashback, trance
  typeCss  Typewriter (CSS) 0.5s     Retro terminal (approx)

  Enter codes separated by commas (e.g. "fade, stagger, hoverS")
```

Then ask:

```
  Speed override? (defaults as shown above — type "fast", "slow", or Enter for default)
  Easing? (default: ease-out — type "ease", "ease-in", "linear", or Enter)
  Should animations play once or loop? (once / loop / enter for once)
```

For each selected animation, inject:
- The `@keyframes` definition into `StoryStylesheet`
- The animation class or selector rule
- Idempotency guard: check if `@keyframes <name>` already exists before injecting

#### If SugarCube widget-driven (option 2):

Show the widget animation catalogue:

```
  ── Widget Animation Catalogue ──

  Code     Animation              What it does
  ─────────────────────────────────────────────────────────
  type     Real typewriter        <<typewriter 40>> per passage
  reveal   Staggered paragraphs   <<timed>> wrappers
  toast    Notification toast     <<notify "message">> widget
  stat     Animated stat counter  <<animateStat var val>>
  scroll   Auto-scroll            Smooth scroll to choices
  xition   Scene transition       <<transition "fade">> postdisplay
  fadeOn   Reveal on scroll       IntersectionObserver widget
  slideOut Slide-out choices      CSS slide-out on navigate
  imgZoom  Image zoom on hover    Lightbox widget
  autoAdv  Auto-advance dialogue  Kinetic novel style
```

For selected widget animations, the generated script must:
1. Inject the `<<widget "name">>` definition into `widgets.twee` (skip if already defined)
2. Inject widget calls into each matching passage
3. Inject any required CSS into `StoryStylesheet`
4. For `stat`: scan passages for `<<set $var +/-= N>>` and replace with widget calls
5. For `autoAdv`: detect consecutive dialogue lines and wrap in `<<timed>>` chains

---

### 2c. Act Opening Effect

```
  ── Act Opening setup ──

  1  How are your act passages named?
     a) Match by ID pattern (e.g. ACT-*, CHAPTER-*, act_*)
     b) Match by tag (e.g. passages tagged [act-opening])
     c) Specific passage IDs (comma-separated)

  2  Title card style:
     a) Minimal — dark screen, act number + title, fade out
     b) Cinematic — full-screen image + subtitle + fade
     c) Book-style — ornate border, chapter number, epigraph
     d) Custom — describe the look

  3  Auto-advance? (automatically proceed after N seconds, or manual click?)
  4  Show a "Previously..." summary? (read $previousActSummary variable?)
  5  Background music/ambient placeholder? (inject audio widget call?)
```

---

### 2d. HUD Effect

```
  ── HUD setup ──

  Which HUD elements to display?
    a) StoryCaption — game title, current chapter/act
    b) Character stats — HP, gold, attributes (reads $character.*)
    c) Quest tracker — active quests from $activeQuests
    d) Inventory summary — item count, key items
    e) Custom sidebar — collapsible panel
    f) StoryMenu — navigation buttons

  HUD position? (top / bottom / left sidebar / right sidebar)
  HUD style? (compact / detailed / minimal icons)
  Collapsible? (y/n — toggleable with a button)
```

Read `variables.md` to discover real variable names. Display available variables:
```
  Available variables from variables.md:
    $character.hp, $character.gold, $character.wisdom
    $activeQuests, $inventory, $currentAct
    $visited_shrine, $spoke_priestess
```
Then for each HUD element, confirm which variable to display and the label text.

---

### 2e. Background Effect

```
  ── Background setup ──

  Background type:
    1  Solid colour
    2  CSS gradient (linear / radial)
    3  Image (from assets/backgrounds/ or assets/illustrations/)
    4  Pattern (CSS repeating pattern)
    5  Ambient animation (gradient shift, slow zoom, parallax)

  If image:
    - List available files from assets/backgrounds/ and assets/illustrations/
    - Ask user to pick or type a path
    - Size: cover / contain / repeat

  Per-passage backgrounds?
    a) Same background everywhere
    b) Different background per act (e.g. ACT-001 = forest, ACT-002 = cave)
    c) Different background per passage ID (match by name pattern)

  Overlay? (darken/blur overlay on passage text for readability)
    - None / dark overlay at N% / blur at Npx
```

If per-passage backgrounds (b/c): generate a mapping dict in the script that associates passage IDs or patterns with CSS classes. Inject `.passage-bg-forest { background-image: url(...) }` etc.

---

### 2f. Other Effect

For requests not covered above:

```
  ── Custom effect ──

  Describe what you want in plain language.
  Examples: "custom font from Google Fonts", "save slot UI",
            "high-contrast accessibility mode", "sound effect triggers",
            "achievement popup widget", "toggle dark/light mode"
```

Analyse the description and determine the technical approach:
- **Custom fonts**: Inject `@font-face` + `@import` into `StoryStylesheet`, override `font-family`
- **Accessibility**: Inject high-contrast CSS, larger font sizes, reduce-motion queries
- **Sound/music**: Inject `<<widget "playSound">>`, scan passages for `[sound:...]` markers
- **Achievements**: Inject `<<widget "achievement">>`, scan for `[ACHIEVEMENT:...]` markers
- **Save/load**: Inject custom save slot UI using SugarCube's `<<save>>` / `<<load>>`
- **Toggle UI**: Inject CSS class toggle + `<<link>>` to switch themes
- **Custom JS**: Inject `:: StoryJavaScript [script]` passage with the JS code

If the request is too complex for a single deterministic script, explain the limitation and suggest breaking it into parts.

---

### Step 3 — Session Manifest

After all effects are configured, show the accumulated manifest:

```
═══════════════════════════════════════════
   SESSION MANIFEST
═══════════════════════════════════════════

  Effects to generate:
   1. Animation — fade in + staggered choices + hover glow
      → CSS @keyframes into StoryStylesheet
   2. Header — gold bar with chapter name
      → passageHeader widget + CSS

  Output file: specs/my-game/postprocessing/effects.py

  ─────────────────────────────────────────
  a) Accept and generate
  b) Add another effect
  c) Remove an effect (enter number)
  d) Change an effect settings (enter number)
  q) Cancel — delete nothing
```

- If `a`: proceed to Step 4.
- If `b`: return to Step 1 menu.
- If `c`: prompt: *"Which effect number to remove?"* — remove from manifest, show updated manifest.
- If `d`: prompt: *"Which effect number to change?"* — re-run the Step 2 dialogue for that effect.

---

### Step 4 — Name & Generate

```
  ── Script name ──

  Filename (without .py):
  [ effects ]
```

Suggest a default name based on the effects (e.g. `fade_header_hud`, `typewriter_act_titles`). Let the user accept or override.

Then generate the Python file at `specs/[FEATURE_DIR]/postprocessing/<name>.py`.

**Generated script structure**:

```python
"""
Postprocessing script: <effect summary>
Generated by speckit.postprocessing
Engine: sugarcube
Effects: fade, stagger, hoverS, header-gold
"""

import re


def postprocess(ctx):
    source_dir = ctx["source_dir"]
    engine = ctx["engine"]
    for twee_file in sorted(source_dir.glob("*.twee")):
        content = twee_file.read_text(encoding="utf-8")
        original = content

        if engine == "sugarcube":
            content = _apply_fade_animation(twee_file.name, content)
            content = _apply_staggered_choices(twee_file.name, content)
            content = _apply_hover_glow(twee_file.name, content)
            content = _apply_gold_header(twee_file.name, content)

        if content != original:
            twee_file.write_text(content, encoding="utf-8")


def _apply_fade_animation(filename: str, content: str) -> str:
    if "@keyframes fadeIn" in content:
        return content
    # inject keyframes + animation rule
    return content


# ... additional effect functions ...


def _inject_into_storystylesheet(content: str, css_block: str) -> str:
    """Inject CSS block into the StoryStylesheet passage."""
    marker = ":: StoryStylesheet [stylesheet]"
    if marker not in content:
        return content
    # Find the end of the passage content and inject before closing
    ...
    return content
```

**Code generation rules**:

1. **One file, multiple functions** — each effect gets its own `_apply_*` function. The main `postprocess()` calls all of them in order.
2. **Use only `re` and `pathlib.Path`** — no external dependencies.
3. **Deterministic** — no randomness. For "randomized" effects, use CSS animation-delay with staggered values or the same timing every compile.
4. **Idempotent** — check if an effect is already applied (e.g. check `@keyframes fadeIn` exists) before injecting. Never duplicate.
5. **Skip boilerplate correctly**:
   - Modifying passage structure → touch `nodes.twee` only, skip `init.twee`, `widgets.twee`, `ui.twee`
   - Injecting CSS → target `StoryStylesheet` in `ui.twee`
   - Injecting widgets → target `widgets.twee`
   - Injecting HUD → target `StoryCaption`/`StoryMenu` in `ui.twee`
6. **Inject CSS into StoryStylesheet**: Find `:: StoryStylesheet [stylesheet]`, then inject before the passage end (before the next `:: ` or EOF). Use a helper function `_inject_into_storystylesheet()`.
7. **Inject widgets**: Find or create `:: WidgetName [widget]`, add the `<<widget "name">>` definition.
8. **Preserve existing content** — append or insert within the correct section; never delete user content unless explicitly replacing.

### 5. Validate

After writing, verify:
1. The file is syntactically valid Python (balanced parens, correct indentation)
2. It exports a `postprocess(ctx)` function
3. All referenced CSS selectors match SugarCube/Ink conventions
4. No syntax errors in injected CSS (balanced braces, valid property names)
5. If the script references variables from `variables.md`, confirm the variables exist

### 6. Report

```
═══════════════════════════════════════════
   POSTPROCESSING — Complete
═══════════════════════════════════════════

  ✅ Script generated: specs/my-game/postprocessing/effects.py

  What it does:
    • Fade-in animation on passage load (0.4s ease-out)
    • Staggered choice appearance (0.1s delay per choice)
    • Hover glow effect on all links
    • Gold gradient header bar with chapter name

  When it runs: Automatically during speckit.export and speckit.compile
  How to test:  Run `speckit.compile` now to see the effects

  How to disable:  Delete or rename the .py file in postprocessing/
  How to customize: Edit the .py file directly — pure Python, no AI needed

  ── Next steps ──
  • Run speckit.compile to apply the changes
  • If you want more effects, run speckit.postprocessing again
```

## Output

- **Success**: One `.py` file in `specs/[FEATURE_DIR]/postprocessing/<name>.py`
- **Extended**: An existing script was updated with new effects
- **No change**: User cancelled at any prompt

## Notes

- Scripts run in sorted filename order at compile time. If you have multiple scripts, prefix with numbers: `01_headers.py`, `02_animations.py`.
- The script receives `source_dir` pointing to the export directory (if export was run) or the draft directory (fallback). It always transforms the files that Tweego will compile.
- If a script raises an exception during postprocessing, the error is printed but export/compile continues. Fix the script and re-run.
- Temporarily disable a script by changing its extension (e.g. `.py.bak`) or moving it out of `postprocessing/`.
- The `speckit.postprocessing` command itself is not run during compile — it only generates the script. The generated script is what runs during compile.

## See Also

- `speckit.theme` — Generate CSS themes for stories
- `speckit.compile` — Compile and apply postprocessing
- `speckit.export` — Export boilerplate then apply postprocessing
- `scripts/python/postprocess.py` — The runner that discovers and executes postprocessing scripts
- `scripts/python/postprocess/` — Example postprocessing scripts
