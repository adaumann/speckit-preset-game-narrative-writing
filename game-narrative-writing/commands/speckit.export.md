---
description: Export drafted nodes to engine-specific boilerplate structure. Generates scaffolding (init, widgets, UI, styling) and integrates drafted nodes into a ready-to-compile project.
handoffs:
  - label: Compile to playable output
    agent: speckit.compile
    prompt: Compile the exported engine project to playable HTML/JSON with integrated testing loop
    send: true
  - label: Review or edit nodes
    agent: speckit.implement
    prompt: Review or re-draft individual nodes if needed before compilation
    send: false
  - label: Generate outlines again
    agent: speckit.outline
    prompt: Regenerate outlines (e.g., to add more nodes or revise structure)
    send: false
scripts:
  py: scripts/python/export.py --spec $SPECNAME --engine $ENGINE
---

# speckit.export

Export drafted node files to engine-specific boilerplate structure. Creates a complete, ready-to-compile project scaffold from narrative design + drafted nodes.

**Purpose**: Bridge the gap between narrative design (variables, mechanics, characters) and playable output. Generates engine-native code structure (not markdown), eliminating round-trip translation errors.

## User Input

```text
$ARGUMENTS
```

Accepted arguments:
- `[ENGINE]` - export for a specific engine (e.g., `sugarcube`, `ink`, `renpy`)
- `--all-engines` - export for all configured engines
- `--force` - regenerate existing export (overwrite)
- *(no argument)* - export for engine specified in `constitution.md`

## Pre-Execution Checks

**Verify prerequisites**:
1. Confirm `specs/[FEATURE_DIR]/draft/` exists with `.twee` or `.ink` files from `speckit.implement`
2. Verify `constitution.md`, `variables.md`, `mechanics.md` exist
3. Verify node files have valid YAML headers (node_id, title, status required)

**Check engine availability**:
- For SugarCube: Confirm tweego.exe available in PATH
- For Ink: Confirm inklecate.exe available in PATH

## Execution Steps

### 1. Load Configuration & Dependencies

For each target engine, load:
- **Required**: `constitution.md` (engine_target, prose_profile, tone, default_pov)
- **Required**: `variables.md` (all declared variables with export names, defaults, scopes)
- **Required**: `mechanics.md` (all Tier 1 & Tier 2 hook definitions with engine syntax)
- **Optional**: Selected CSS theme from `templates/` (Sugarcube only)
- **Optional**: `characters.md` (for NPC reference in generated comments)

### 2. Create Output Directory Structure

```
specs/<SPECNAME>/export/<ENGINE>/
├── init.[EXT]          # Variable initialization
├── widgets.[EXT]       # Widget/macro stubs + utilities
├── ui.[EXT]            # UI chrome, StoryCaption, menus, styling
├── [NODE_ID].[EXT]     # Copied from draft/
├── [NODE_ID].[EXT]
└── [NODE_ID].[EXT]
```

### 3. Generate Engine-Specific Boilerplate

#### For SugarCube (Twee format)

**init.twee** — StoryData + StoryInit:

```twee
:: StoryData
{
  "ifid": "[GUID from constitution]",
  "name": "[story_name from constitution]",
  "startnode": "[first_node_id from plan]",
  "engine": "SugarCube",
  "engineversion": "2.30.0"
}

:: StoryInit [header]
  <<run setup()>>

  {- [INITIALIZE VARIABLES] -}
  <<set $[variable_name] = [default_value]>>
  <<set $[variable_name] = [default_value]>>
  [... for each variable in variables.md ...]
```

**widgets.twee** — Widget definitions:

For each [MECHANIC:...] hook found in drafted nodes:
```twee
:: SugarCubeWidgets [widget]
  {- QUEST MANAGEMENT -}
  <<widget "questList">>
    [widget stub - developer fills in implementation]
  <</widget>>

  <<widget "advanceQuestStage">>
    [widget stub]
  <</widget>>

  {- INVENTORY SYSTEM -}
  <<widget "pickupItem">>
    [widget stub]
  <</widget>>

  [... generate stubs for all declared mechanics ...]
```

**ui.twee** — UI Chrome and Styling:

```twee
:: StoryCaption
  [Status display: gold, items, etc. - from shrine-sample model]

:: StoryMenu
  [Navigation menu - from shrine-sample model]

:: CharacterSheet [menu]
  [Character profile display]

:: InventoryUI [menu]
  [Inventory display]

:: QuestUI [menu nobr]
  [Quest tracking display]

:: StoryStylesheet [stylesheet]
  {- CSS Theme -}
  [Theme CSS from templates/ or constitution.md style settings]
```

**Node files** — Copy drafted nodes:

```twee
  {- Node ID: [NODE_ID] -}
  {- Variables Read: [list from outline] -}
  {- Variables Set: [list from outline] -}

  [Drafted prose body from implement]

  [[Choice 1|TARGET_NODE]]
  [[Choice 2|TARGET_NODE]]
```

#### For Ink (ink format)

**init.ink** — Story constants + variable initialization:

```
// Story metadata
// VAR variable_name = default_value
// VAR another_var = default_value
[... for each variable ...]

=== setup ===
  // Initialization logic
```

**widgets.ink** — Reusable functions:

```
=== function quest_list ===
  // Stub: developer fills in implementation

=== function advance_quest_stage(quest_id) ===
  // Stub
```

**[NODE_ID].ink** — Narrative nodes copied from draft:

```
=== [NodeTitle] ===
  // Node ID: [NODE_ID]
  // Variables Read: [list]
  // Variables Set: [list]

  [Drafted prose from implement]

  * [Choice 1]
    -> TARGET_NODE
  * [Choice 2]
    -> TARGET_NODE
```

### 4. Inject Shrine-Sample Model Components

If exporting to SugarCube and no UI widgets provided, use shrine-sample as reference:

1. Copy quest widget pattern from `shrine-sample/shrine-widgets.twee`
2. Copy UI structure from `shrine-sample/shrine-ui.twee` 
3. Apply theme CSS from `shrine-sample/shrine-ui.twee`
4. Generate compile command matching shrine-sample pattern

### 5. Generate Compile Command

Create a shell script or Makefile:

**compile.sh** (for SugarCube):
```bash
#!/bin/bash
tweego init.twee widgets.twee ui.twee \
  [NODE_ID].twee [NODE_ID].twee [...] \
  -o story.html
echo "✓ Compiled to story.html"
```

**Rationale**: Developer can run `./compile.sh` without remembering tweego syntax.

### 6. Generate Export Manifest

**export-manifest.json** — Metadata for tracking:

```json
{
  "export_timestamp": "2024-05-11T14:32:00Z",
  "engine": "sugarcube",
  "node_count": 12,
  "variable_count": 24,
  "widgets_generated": 7,
  "status": "ready_for_compilation",
  "compile_command": "tweego init.twee widgets.twee ui.twee [nodes...] -o story.html",
  "next_step": "speckit.compile"
}
```

## Output

- **Success**: All boilerplate files generated, nodes copied, ready for `speckit.compile`
  ```
  ✓ Export complete for sugarcube
  ✓ 12 nodes exported
  ✓ 24 variables initialized
  ✓ 7 widgets generated (from mechanics.md)
  ✓ UI chrome applied (from shrine-sample model)
  ✓ Compile command: tweego init.twee widgets.twee ui.twee ... -o story.html
  ```

- **Failure**: Missing required files or syntax errors
  ```
  ✗ Export failed: variables.md not found
  ✗ Export failed: Node NODE-005 missing required field: node_id
  ```

## Notes

- Export does NOT modify drafted nodes - only copies them
- Export generates widget stubs, not implementations - developers fill in logic during testing
- Export applies default theme if `constitution.md` specifies one; can be overridden
- Export is re-runnable - safe to run multiple times (--force to overwrite)
- Exported files are ready for `speckit.compile` → playable output

## Postprocessing

After export, any Python scripts in `specs/[FEATURE_DIR]/postprocessing/*.py` are automatically
discovered and executed. Each script receives a `postprocess(ctx)` call with the export
directory as `source_dir`, allowing you to modify the generated `.twee`/`.ink` files.

**Use cases**: inject custom CSS themes, add passage headers/footers, apply animations.

**Generate scripts with**: `speckit.postprocessing` — describe what you want in natural language.

**Example** — create `specs/my-game/postprocessing/fix_theme.py`:
```python
def postprocess(ctx):
    for f in ctx["source_dir"].glob("*.twee"):
        content = f.read_text()
        # modify content...
        f.write_text(content)
```

Reference examples in `scripts/python/postprocess/`.

You can also use `speckit.postprocessing` to generate scripts automatically.

## See Also

- `speckit.implement` - Generate draft nodes in Twee/Ink format
- `speckit.compile` - Compile exported boilerplate + testing loop
- `shrine-sample` - Reference implementation showing full structure
