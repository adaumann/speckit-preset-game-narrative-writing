---
description: Compile node files to playable output format (HTML for Twine/SugarCube, compiled JSON for Ink with HTML wrapper, etc.). Prefers export/ over draft/ when export exists. Includes built-in structural validation and a self-correcting fix loop that runs until compilation succeeds or no further progress can be made.
handoffs:
  - label: Run full test suite
    agent: speckit.verify
    prompt: Run optional full unit tests if you want comprehensive validation beyond compilation checks
    send: false
  - label: Re-draft failing nodes
    agent: speckit.implement
    prompt: Some nodes failed validation. Show which ones and suggest fixes, then re-draft them
    send: true
  - label: View node drafts
    agent: speckit.implement
    prompt: Show me the current drafted nodes
    send: false
scripts:
  py: scripts/python/compile.py --spec $SPECNAME --engine $ENGINE
---

# speckit.compile

Compile node files to a playable output file in `spec/<specname>/output/<ENGINE>/`.

**Source priority**: prefers `spec/<specname>/export/<ENGINE>/` (if `speckit.export` has been run), falls back to `spec/<specname>/draft/<ENGINE>/`.

Uses native compilers (tweego for SugarCube, inklecate for Ink) with a self-correcting fix loop: each compilation error is parsed, a targeted fix is applied to the specific file, and the compiler re-runs until the story compiles clean or no further automatic progress can be made.

**Output formats**:
- **Twine/SugarCube** (twee) → HTML file with StoryData JSON header (via tweego.exe)
- **Ink** (.ink) → Compiled JSON + HTML wrapper (via inklecate.exe)
- **Renpy** (.rpy) → Python script for Ren'py engine
- **Generic** (markdown) → Linked HTML pages

## User Input

```text
$ARGUMENTS
```

Accepted arguments:
- `[ENGINE]` - compile for a specific engine (e.g., `sugarcube`, `ink`, `renpy`, `generic`)
- `--all-engines` - compile all engines in export_engines configuration simultaneously
- `--force-rebuild` - force full rebuild even if output exists
- `--dry-run` - validate without writing output files
- *(no argument)* - compile to the engine specified in `constitution.md`

## Pre-Execution Checks

**Extract Platform & Ruleset** (auto-detect RPG context):
- Read `.specify/memory/constitution.md` YAML frontmatter and extract `[PLATFORM]` and `[RULESET]`
- If `[PLATFORM]` = "Tabletop": Set `SESSION.is_rpg = "tabletop"` and enable Tabletop compilation checks
- If `[PLATFORM]` = "Computer Game": Set `SESSION.is_rpg = "computer"` and enable Computer Game compilation checks
- If neither detected: Set `SESSION.is_rpg = false` (generic compilation model)
- Store `SESSION.platform` and `SESSION.ruleset` for RPG-specific validation

**Load RPG-Specific Documents** (if platform detected):
- **Tabletop**: Load `specs/companions.md`, `specs/factions.md`, `specs/mechanics-[ruleset].md`, `campaign-guide.md`, `SESSION-N-BRIEFING.md`
- **Computer**: Load `specs/variables.md` (route-specific variables), `specs/accessibility.md` (accessibility variants), `playthrough_route` variable usage

**Verify source files exist** (checks in order):
- Scan `spec/<specname>/export/<ENGINE>/` for all engine files (boilerplate + nodes from `speckit.export`)
- If no export dir, scan `spec/<specname>/draft/<ENGINE>/` for `story.twee` or `NODE-*.twee` files
- If no files found - halt: "No source files found for engine `$ENGINE`. Run `speckit.implement` (or `speckit.export`) first."

**Verify engine configuration**:
- Check `constitution.md` for `export_engines`
- Check `variables.md` for export names for the target engine
- Check `mechanics.md` for Tier 1 hook compatibility with target engine

**RPG Campaign Compilation Checks** (if platform detected):

**For Tabletop RPG**:
1. Verify campaign prep documents exist and are up-to-date:
   - ✓ `campaign-guide.md` (updated with latest party composition, companion status, faction relations)
   - ✓ `SESSION-N-BRIEFING.md` for all sessions (contains session-specific setup and NPC intro)
   - ✓ `campaign-pacing-guide.md` (session time estimates, encounter pacing)
2. Validate companion state consistency:
   - All companions in `companions.md` have initial loyalty values defined
   - Loyalty gates (recruitment at ≥70, betrayal at ≤-50) match story nodes
3. Validate faction reputation tracking:
   - All factions in `factions.md` have initial reputation values (baseline 0)
   - Faction rep gates (quest availability at ≥100/-100) match story branches
4. Check ruleset-specific mechanics:
   - D&D 5e: All DCs fall within 5-20 range for campaign level (with exceptions noted)
   - Pathfinder 2e: All DCs follow 10-50+ success scale; hero points tracked
   - Shadowrun 6e: All karma costs specified; attribute rolls within 1-6 rating

**For Computer Game**:
1. Verify route variable isolation:
   - All route-exclusive variables use prefixes ($stealth_*, $combat_*, $diplomacy_*)
   - No cross-route variable leakage (route A can't read route B's variables)
   - Route commitment lock: `playthrough_route` set once in CHAPTER-2, immutable after
2. Validate accessibility variants:
   - Colorblind mode: Implemented in all routes (not color-dependent indicators)
   - Audio mode: Implemented in all routes (if audio-based cues exist)
   - Motor mode: No timed inputs after CHAPTER-2 commit, or timer ≥10 seconds
   - Cognitive mode: Route summary available before final commit
3. Check chapter structure:
   - All chapters have pacing guidelines (target: 45-120 min per chapter)
   - All chapters have accessibility exit points (no dead-ends requiring specific ability)

## Execution Steps

### 1. Structural Validation (automatic)
- Parse all node YAML headers
- Validate required fields (node_id, title, status)
- Check mechanic hook syntax ([MECHANIC:...] blocks)
- Check choice block syntax ([CHOICE:...] blocks)
- Report all validation errors with line context

### 2. Load Node Files
- Read validated node files into memory
- Parse YAML headers and body content
- Handle both individual NODE files and combined story files

### 3. Engine-Specific Compilation

#### Twine/SugarCube (twee → HTML via tweego)

**Compiler**: `tweego.exe` (from Twine installation)

**Process**:
1. Create `spec/<specname>/output/sugarcube/` directory
2. Read `spec.md`, `constitution.md`, and `variables.md` to build StoryData JSON
3. Concatenate all node .twee files in order
4. Convert mechanic hooks to SugarCube syntax
5. Run tweego.exe with all .twee files as input
6. Generate `spec/<specname>/output/sugarcube/story.html`

**Output**: Playable HTML file - open in browser to play

**Fix loop** (runs until compiled or no further progress):
1. Run tweego. If success → done.
2. Parse tweego error output: extract file name, line number, error type.
3. For each error, apply a targeted fix to the specific `.twee` file:
   - `Unmatched '<<'` → find unclosed macro block in that file, close it
   - `Undefined variable: $var` → add `<<set $var to 0>>` to StoryInit block
   - `Passage not found: NAME` → check if the passage exists in another file; if not, create a stub `:: NAME` passage with a placeholder link back
   - `Unexpected token` / `Unknown macro` → flag to user; cannot auto-fix — report line with suggestion
4. Re-run tweego after each fix batch.
5. If the same errors repeat unchanged after a fix attempt (no progress), stop the loop and report: `Stuck — auto-fix made no progress. Manual edit required.` with exact file/line/error.
6. No hard retry limit — loop continues as long as errors are being resolved.

#### Ink (ink → JSON + HTML via inklecate)

**Compiler**: `inklecate.exe` (from Ink installation)

**Process**:
1. Create `spec/<specname>/output/ink/` directory
2. Validate with inklecate (-p flag):
   - Checks for syntax errors
   - Validates knot/stitch references
   - Reports validation errors
3. If validation passes, compile with inklecate (-c flag):
   - Generates `story.json` (compiled story format)
   - Generates `story.html` (HTML wrapper for story.json)
4. HTML wrapper includes:
   - Story metadata and info
   - Links to Ink web player and Inky IDE
   - Embedded story JSON for reference

**Output files**:
- `spec/<specname>/output/ink/story.json` - Compiled story (use with Ink runtime)
- `spec/<specname>/output/ink/story.html` - HTML display wrapper

**Fix loop** (same pattern as SugarCube above):
1. Run inklecate `-p` (validate). If clean → compile with `-c` → done.
2. Parse inklecate error output: extract knot name, line, error type.
3. For each error, apply a targeted fix:
   - `Unknown knot: NAME` → create stub `=== NAME ===\n-> END` in the appropriate file
   - `INCLUDE file not found` → flag; cannot auto-fix — report with path suggestion
   - Divert syntax errors (`->` missing) → add missing divert
4. Re-run inklecate `-p` after each fix batch.
5. Stop loop if same errors repeat (no progress); report stuck state with file/line/error.

#### Multi-Engine Compilation

When using `--all-engines`:
1. Reads export_engines from constitution.md or spec.yml
2. Iterates through each configured engine
3. Compiles each with its appropriate compiler
4. Reports success/failure for each engine
5. Exit code is 0 only if ALL engines succeed

Example:
```bash
speckit.compile --all-engines
# Compiles: sugarcube → tweego, ink → inklecate, etc.
# Outputs results for each engine
```

### 4. Map Integration (NEW for RPG campaigns)

**When**: Only runs if `constitution.md` has `map_format` set (not "none")

**Maps in Output**: Maps are always available to players in sidebar/menu, with battle maps embedded in story passages when relevant.

#### Map Export (All Engines)

1. Scan `specs/maps.md` registry for map files
2. Export JSON maps to images:
   - PNG: `output/<ENGINE>/handouts/<map-name>.png` (high-res for printing)
   - SVG: `output/<ENGINE>/reference/<map-name>.svg` (editable vector)
3. Generate markdown inventory: `output/<ENGINE>/MAP-INVENTORY.md`

**Commands**:
```bash
python scripts/python/map-export.py --dir specs/maps/ --output-dir output/sugarcube/handouts/ --format png
python scripts/python/map-export.py --dir specs/maps/ --output-dir output/sugarcube/reference/ --format svg
```

#### Map Integration by Engine

##### **Twine/SugarCube Integration**

Maps embedded in HTML story with interactive controls:

1. **Create Maps Passage** with gallery menu:
   ```twee
   :: Maps [menu]
   <div class="map-gallery">
     <<for _map range $maps>>
       <<link _map.name "Map: " + _map.name>>
         <<set $currentMap = _map>>
       <</link>>
     <</for>>
   </div>
   ```

2. **Create Map Display Passage** for each map:
   ```twee
   :: Map: Goblin Hideout
   [img[handouts/goblin-hideout.png]]
   
   <<if hasVisited("Encounter: Goblin Battle")>>
     **Visited**: Yes (Session 3)
     **Encounters**: Goblin Scout (CR 1/8), Chief Grok (CR 1/2)
   <</if>>
   
   <<link "Back to Maps" "Maps">><</link>>
   ```

3. **Embed Battle Maps in Story Passages**:
   - When player enters battle location, display map inline
   - Example:
   ```twee
   :: Encounter: Goblin Battle
   You turn the corner and spot a goblin camp!
   
   [img[handouts/goblin-hideout.png]]
   
   **Enemies spotted**: 3 goblins, 1 chief
   ```

4. **Add Map Sidebar** (if using SugarCube UI bar):
   ```twee
   :: StoryData
   {
     "ifid": "...",
     "sidebar": true,
     "maps": [
       {"id": "map-1", "name": "Goblin Hideout", "type": "battle"},
       {"id": "map-2", "name": "Kingdom Overview", "type": "regional"}
     ]
   }
   ```

**Output files**:
- `output/sugarcube/story.html` - Main story with embedded maps
- `output/sugarcube/handouts/*.png` - Battle map images (embedded in passages)
- `output/sugarcube/reference/*.svg` - Reference maps (linked in Maps menu)

##### **Ink Integration**

Maps added to compiled JSON and HTML wrapper with interactive viewer:

1. **Add Map Metadata to Compiled JSON**:
   ```json
   {
     "maps": [
       {
         "id": "map-1",
         "name": "Goblin Hideout",
         "type": "battle",
         "session": 3,
         "image": "handouts/goblin-hideout.png"
       }
     ],
     "story": { ... }
   }
   ```

2. **Create Map Display in HTML Wrapper** with:
   - Map gallery menu in sidebar
   - Click map name → display PNG image
   - Show metadata (type, session, encounters)
   - Link to SVG for editing

3. **Embed Battle Maps in Story Text**:
   - When Ink story reaches battle knot, inject map reference:
   ```ink
   === goblin_encounter ===
   You turn the corner and spot a goblin camp!
   
   ~displayMap("goblin-hideout")  // Display inline
   
   - [Fight] -> battle_start
   - [Flee] -> run_away
   ```

4. **HTML Wrapper Features**:
   - Map gallery in left sidebar (always visible)
   - Main story area in center
   - Map viewer toggles when map selected
   - All maps available as PNG + SVG

**Output files**:
- `output/ink/story.json` - Compiled story with map metadata
- `output/ink/story.html` - HTML wrapper with map viewer sidebar
- `output/ink/handouts/*.png` - Battle map images (referenced in wrapper)
- `output/ink/reference/*.svg` - Reference maps (available in viewer)

##### **Generic (Markdown → HTML) Integration**

Maps as linked pages with full reference documentation:

1. **Create Maps Index** (`output/generic/maps.html`):
   - Gallery of all maps with thumbnails
   - Links to individual map pages
   - Search by type (battle, regional, location, asset)

2. **Create Individual Map Pages** (`output/generic/maps/map-NAME.html`):
   ```html
   <h1>Goblin Hideout</h1>
   <img src="handouts/goblin-hideout.png" alt="Goblin Hideout Battle Map">
   
   <h2>Details</h2>
   <p><strong>Type</strong>: Battle</p>
   <p><strong>Session</strong>: 3</p>
   <p><strong>Grid Size</strong>: 20×20 squares</p>
   <p><strong>Encounters</strong>: Goblin Scout, Chief Grok</p>
   
   <h2>Reference</h2>
   <p><strong>Secret Door</strong> at (8, 12) - DC 15 Perception</p>
   <p><strong>Trap</strong> at (10, 10) - DC 14 save for half damage</p>
   
   <a href="reference/goblin-hideout.svg">Download SVG (editable)</a>
   ```

3. **Link Maps from Story Pages**:
   - Story page mentions location → link to map page
   - Example:
   ```html
   <p>You enter the <a href="maps/map-goblin-hideout.html">Goblin Hideout</a>...</p>
   ```

4. **Navigation** in story pages:
   - "View Map" button/link prominent
   - "Maps Index" in footer/sidebar
   - Breadcrumb navigation (Story → Maps Index → Individual Map)

**Output files**:
- `output/generic/maps.html` - Map gallery and index
- `output/generic/maps/map-*.html` - Individual map pages
- `output/generic/handouts/*.png` - Battle map images
- `output/generic/reference/*.svg` - Reference maps (downloadable)

#### Summary: Maps in All Engines

| Aspect | SugarCube | Ink | Generic |
|--------|-----------|-----|---------|
| Battle maps | Embedded in passages | In HTML viewer sidebar | Linked map pages |
| Regional maps | In Maps menu | In HTML viewer sidebar | Maps index page |
| Always visible? | Yes (menu) | Yes (sidebar) | Yes (navigation) |
| Player can explore? | Yes (menu navigation) | Yes (sidebar gallery) | Yes (map pages) |
| Export format | PNG in HTML | PNG + SVG in wrapper | Separate map pages |
| Interactive viewer? | Basic (image) | Full viewer in wrapper | PNG preview + SVG download |

## RPG Campaign Exports

### Tabletop Campaign Exports

When compiling a tabletop RPG campaign (`[PLATFORM]` = "Tabletop"), auto-generate campaign prep exports:

**Auto-Generated Campaign Prep Documents** (in `output/<ENGINE>/`):

1. **campaign-guide.md** (complete campaign bible):
   - Party composition and starting equipment
   - Companion roster with initial loyalty states
   - Faction list with initial reputation (0)
   - Map registry (all session maps)
   - Ruleset house rules (if any)
   - Session pacing summary

2. **SESSION-N-BRIEFING.md** (per session):
   - Session objective and location
   - NPC status at session start (companion loyalty, faction reps)
   - Encounter summary (enemies, DCs, treasure)
   - Map list for session
   - Expected duration and pacing notes

3. **character-builder-guide.md** (for Session 0 character creation):
   - Class/race/attribute selection tables (per ruleset)
   - Ability score generation method
   - Skill recommendations per class
   - Starting equipment and gold
   - Character sheet template

4. **MAP-INVENTORY.md** (map registry):
   - List of all maps per session
   - Map type (battle, regional, location, asset)
   - Encounter list per map
   - File locations (PNG handout, SVG reference)

**Exports by Compiler**:

| Document | SugarCube | Ink | Generic |
|----------|-----------|-----|---------|
| campaign-guide.md | In output/ | In output/ | In output/ |
| SESSION-N-BRIEFING.md | In output/ | In output/ | In output/ |
| character-builder-guide.md | In output/ | In output/ | In output/ |
| MAP-INVENTORY.md | In output/ | In output/ | In output/ |

### Computer Game Route Exports

When compiling a computer game (`[PLATFORM]` = "Computer Game"), validate and export route-specific content:

**Route Validation During Compilation**:

1. **Route Variable Isolation Check**:
   - Verify $stealth_*, $combat_*, $diplomacy_* prefixes used correctly
   - Detect cross-route variable reads (error if route A reads route B's variables)
   - Verify playthrough_route immutable after CHAPTER-2

2. **Route Balance Metrics**:
   - Calculate node count per route (within 20% parity recommended)
   - Calculate dialogue/choice count per route
   - Estimate playtime per route (using node weights)
   - Report: "Stealth: 45 nodes (87 min), Combat: 48 nodes (92 min), Diplomacy: 42 nodes (78 min)"

3. **Accessibility Variant Coverage**:
   - Check: Colorblind variant available in all routes? YES/NO
   - Check: Audio variant available in all routes? YES/NO
   - Check: Motor variant available in all routes? YES/NO
   - Check: Cognitive variant available in all routes? YES/NO
   - Report coverage % per variant

**Auto-Generated Route Exports** (in `output/<ENGINE>/`):

1. **playthrough-guide.md** (player-facing route descriptions):
   - Route descriptions (Stealth, Combat, Diplomacy)
   - Route-specific mechanics and abilities
   - Playstyle examples and tips
   - Estimated playtime per route
   - Accessibility notes per route

2. **ROUTE-BALANCE-REPORT.md** (dev reference):
   - Node count per route
   - Dialogue/choice count per route
   - Estimated playtime per route (with breakdown by chapter)
   - Content parity analysis
   - Rebalancing recommendations if routes unequal

3. **accessibility-variants.md** (documentation):
   - Colorblind: How variants are displayed per route
   - Audio: What audio cues represent per route
   - Motor: What alternatives available per route
   - Cognitive: What summaries provided per route

---

## Compiler Installation

### SugarCube/Tweego
1. Install Twine: https://twinery.org/
2. Tweego is included in Twine installation
3. Add Twine directory to PATH, or place tweego.exe in scripts/bin/

### Ink/Inklecate
1. Download from: https://github.com/inkle/ink/releases
2. Extract inklecate.exe
3. Add to PATH, or place inklecate.exe in scripts/bin/

## Error Handling

**If compilation fails**:
- Shows specific error from compiler (file, line, error text)
- Applies targeted auto-fix per error type (see Fix loop above)
- Re-runs compiler after each fix batch — no fixed limit on attempts
- Stops when: compilation succeeds, or no progress in a fix round (stuck)
- On stuck: reports exact errors that could not be auto-fixed with remediation suggestions
- Offers next steps (re-draft nodes, check configuration, manual edit)

**Example error output**:
```
❌ Compilation error:
   NODE-001.twee:15: Error: Unmatched '<<'
   NODE-003.twee:8: Error: Undefined variable: $player_name

🔧 Fix round 1:
   NODE-001.twee:15 — Unmatched '<<' → closed macro block ✓
   NODE-003.twee:8  — Undefined variable $player_name → added <<set $player_name to "">> in StoryInit ✓

▶️  Re-running tweego...
✅ Compilation succeeded after 1 fix round

--- (example: stuck case) ---
🔧 Fix round 1:
   NODE-007.twee:22 — Unknown macro <<customWidget>> → cannot auto-fix
   ⚠ Stuck: error unchanged after fix attempt
   Manual fix required: NODE-007.twee:22 — unknown macro <<customWidget>>
   Suggestion: Define <<widget "customWidget">> in your WidgetPassage, or replace with a supported macro
```

## Compilation Success Output

When compilation completes successfully:

```
✅ Compilation succeeded (no fixes needed)
✅ Output: spec/<specname>/output/sugarcube/story.html
   Size: 125000 bytes

Next steps:
- Open story.html in browser to playtest
- Gather feedback with speckit.feedback
- Document issues in tasks.md
```

## Script Support

The scripts support multiple invocation methods:

**Python**:
```bash
python scripts/python/compile.py --spec my-game --engine sugarcube
python scripts/python/compile.py --spec my-game --all-engines
```

**Python**:
```bash
python scripts/python/compile.py --spec my-game --engine sugarcube
python scripts/python/compile.py --spec my-game --all-engines
```

---

## About speckit.verify

`speckit.verify` is now **optional**. The `speckit.compile` command includes all basic structural validation automatically. 

Use `speckit.verify` if you want:
- Full unit test suite (beyond what compile checks)
- Deep branch coverage analysis
- Self-correction loops for complex fixes
   ```

**Compile steps**:
1. Read all source files in `spec/<specname>/draft/sugarcube/`:
   - `WorldMap.twee` — if present, include first after StoryInit/StoryMenu
   - `LOC-*.twee` — hub passage files; include in Area order (as listed in `world-map.md`, or alphabetically if world-map absent)
   - `NODE-*.twee` — scene files; include in node ID order after all LOC-* files
   - `END-*.twee` — ending files; include last
   **Assembly order**: `StoryInit → StoryMenu → WorldMap.twee → [LOC-*.twee in area order] → [NODE-*.twee in node ID order] → [END-*.twee]`
2. Strip YAML header (front matter) from each file
3. Convert `[MECHANIC:...]` blocks to SugarCube macro syntax:
   - `[MECHANIC:FLAG set=var value=true]` → `<<run $store.variables.var = true>>`
   - `[MECHANIC:VISITED set=visited_NODE_001]` → `<<run $store.visited.NODE_001 = true>>`
   - `[MECHANIC:INVENTORY add=key]` → `<<run $store.inventory.push('key')>>`
   - Other hooks converted per `mechanics.md` specifications
4. Convert `[CHOICE: N options]` blocks to SugarCube `<<link>>` macros
5. Concatenate all processed node files into a single `.twee` file
6. Wrap in Twee 3 StoryData structure with proper header
7. Generate HTML using tweego compiler (if available) or template-based HTML generation

**Output file**: `spec/<specname>/output/sugarcube/[specname].html` (playable)

**Error handling**:
- If `tweego.exe` not found, generate HTML directly from Twee template
- If macro conversion fails, report line number and hook type; offer re-draft option

### Ink (ink → single file)

**Status**: Placeholder (coming soon)

**Compile order** (when implemented):
- Include `LOC-*.ink` hub passage files before scene knots so diverts resolve correctly
- Hub passage labels use `=== LOC_{ShortName} ===` format (underscores — Ink identifier constraint); scene knots use `=== NODE_{seq}_{Name} ===`
- Assembly order: `START → [LOC_*.ink hub labels] → [NODE_*.ink scene knots] → [END_*.ink ending knots]`

### Renpy (rpy file)

**Status**: Placeholder (coming soon)

### Generic/Markdown (markdown → linked HTML)

**Status**: Placeholder (coming soon)

## Validation Error Report

If validation fails before compilation:

```
🔍 Validating node files...
  ✓ NODE-001.md
  ✓ NODE-002.md
  ❌ NODE-003.md
     • YAML validation failed: Missing required fields: node_id
     • Unclosed MECHANIC hooks: 3 open, 2 closed

❌ Validation failed: 2 error(s) found

⚠️  Compilation halted due to validation errors.
Fix the errors above and try again.
```

## Compilation Success Output

When compilation completes successfully:

```
COMPILATION SUCCESSFUL

Engine: [ENGINE]
Source nodes: spec/<specname>/draft/<ENGINE>/NODE-001.md ... NODE-NNN.md
Output file: spec/<specname>/output/<ENGINE>/[specname].[ext]

Playable: [Y/N]
- For SugarCube: Open [output file] in browser
- For Ink: Compile with Ink compiler: inklecate.exe [output file]
- For Ren'py: Run `renpy [output_directory]`

Node count: [N] nodes compiled
Variable count: [N] variables exported
Total hooks: [N] mechanic hooks converted

Next steps:
- playtest and gather feedback with speckit.feedback
- run speckit.analyze --report for full audit
- document issues in tasks.md
```

## Python Script Support

The `scripts/python/compile.py` script handles:
- Structural validation (YAML, hooks, variables)
- Parsing node YAML headers
- Converting mechanic hooks to engine syntax
- Generating proper StoryData/metadata headers
- Running iterative compilation with error capture
- Generating compilation report with statistics
- Supporting user-defined compilation plugins

**Usage**: `python scripts/python/compile.py --spec [specname] --engine [engine] [--output path] [--skip-validation]`

---

## About speckit.verify

`speckit.verify` is now **optional**. The `speckit.compile` command includes all basic structural validation automatically. 

Use `speckit.verify` if you want:
- Full unit test suite (beyond what compile checks)
- Deep branch coverage analysis
- Self-correction loops for complex fixes
- Detailed test reports

Most workflows: `speckit.compile` alone is sufficient.

---

## Troubleshooting

| Symptom | Cause | Fix |
|---|---|---|
| "No drafted nodes found" | No files in `draft/<ENGINE>/` | Run `speckit.implement` first |
| "YAML validation failed" | Malformed front matter | Check node header syntax |
| "Unknown hook type" | Invalid [MECHANIC:...] block | Check hook type against mechanics.md |
| "Variable undefined" | Export name missing in `variables.md` | Add export name for target engine |
| "tweego.exe not found" | Twine toolchain not installed | Use template-based HTML generation or install tweego |

---

