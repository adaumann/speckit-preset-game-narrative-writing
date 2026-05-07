# SpecKit RPG Map Visualization Tools

Tools for visualizing, editing, and exporting JSON maps for tabletop and computer game RPG campaigns.

## Quick Start

### 1. Interactive Map Viewer (Browser)

Open the interactive map viewer in your browser:

```bash
# Windows
start scripts/map-viewer.html

# macOS
open scripts/map-viewer.html

# Linux
xdg-open scripts/map-viewer.html
```

**Features**:
- Load JSON map files (drag & drop or file picker)
- Pan map (click & drag)
- Zoom in/out (scroll or slider)
- Toggle grid and token display
- View map metadata and terrain legend
- Export map to PNG with one click
- Multiple maps in one session

### 2. Command-Line Export (Python)

Export maps to PNG, SVG, or markdown inventory:

```bash
# Single map to PNG
python scripts/python/map-export.py --input specs/maps/goblin-hideout.json --output handouts/goblin.png

# Single map to SVG
python scripts/python/map-export.py --input specs/maps/regional.json --output reference/regional.svg --format svg

# Batch export: all maps in directory to PNG
python scripts/python/map-export.py --dir specs/maps/ --output-dir output/handouts/ --format png

# Batch export: all maps in directory to SVG
python scripts/python/map-export.py --dir specs/maps/ --output-dir output/reference/ --format svg

# Custom cell size (pixels)
python scripts/python/map-export.py --input specs/maps/battle.json --output battle.png --cell-size 20

# Disable grid lines
python scripts/python/map-export.py --input specs/maps/battle.json --output battle.png --no-grid
```

**Options**:
```
--input FILE              Input JSON map file
--output FILE             Output image file
--format {png,svg}        Export format (default: png)
--dir DIRECTORY           Input directory for batch export
--output-dir DIRECTORY    Output directory for batch export
--cell-size PIXELS        Grid cell size (default: 10)
--no-grid                 Disable grid lines in export
```

### 3. Automatic Export During Compilation

When you run `speckit.compile` with maps enabled:

```bash
speckit.compile
```

**Automatically generates**:
- `output/handouts/*.png` - High-resolution player handouts
- `output/reference/*.svg` - Editable GM reference maps
- `output/maps/map-viewer.html` - Interactive viewer (copy of map-viewer.html)
- `output/MAP-INVENTORY.md` - Index of all maps

## JSON Map File Format

Maps are stored as JSON files in `specs/maps/` directory.

**Minimal map**:
```json
{
  "name": "Goblin Hideout",
  "type": "battle",
  "session": 3,
  "scale": "5ft",
  "width": 20,
  "height": 20,
  "tiles": [],
  "tokens": [],
  "encounters": ["ENC-015"],
  "notes": "Battle map for Session 3"
}
```

**Full example with terrain and tokens**:
```json
{
  "name": "Goblin Hideout - Battle",
  "type": "battle",
  "session": 3,
  "scale": "5ft",
  "width": 20,
  "height": 20,
  "tiles": [
    {"x": 0, "y": 0, "type": "stone", "difficulty": 0},
    {"x": 5, "y": 5, "type": "tree", "difficulty": 2, "occupies": "2x2"},
    {"x": 10, "y": 10, "type": "wall", "difficulty": 0},
    {"x": 2, "y": 8, "type": "trap", "difficulty": 0}
  ],
  "tokens": [
    {"id": "goblin-1", "name": "Goblin Scout", "x": 5, "y": 5, "cr": "1/8"},
    {"id": "goblin-chief", "name": "Chief Grok", "x": 15, "y": 10, "cr": "1/2"}
  ],
  "encounters": ["ENC-015"],
  "lighting": "daylight",
  "music_track": "combat-tense.ogg",
  "notes": "Secret door at (8, 12), requires DC 15 Perception check to discover"
}
```

**Field Reference**:

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `name` | string | Yes | Display name for the map |
| `type` | string | Yes | Map type: `battle`, `regional`, `location`, or `asset` |
| `session` | number | For tabletop | Session number when map is used |
| `scale` | string | For battle maps | Grid scale: `5ft` (D&D), `10ft`, or custom |
| `width` | number | Yes | Map width in grid squares |
| `height` | number | Yes | Map height in grid squares |
| `tiles` | array | No | Array of terrain tile objects |
| `tokens` | array | No | Array of token/creature objects |
| `encounters` | array | No | Associated encounter IDs (e.g., `["ENC-015"]`) |
| `lighting` | string | No | Lighting state: `daylight`, `torchlight`, `magical-darkness`, `variable` |
| `music_track` | string | No | Background music filename |
| `notes` | string | No | GM notes, secrets, or special rules |

**Tile object**:
```json
{
  "x": 0,                  // Column (0-indexed)
  "y": 0,                  // Row (0-indexed)
  "type": "grass",         // Terrain type
  "difficulty": 0,         // 0=normal, 1=difficult, 2=very difficult
  "occupies": "1x1"        // Size for multi-tile features (e.g., "2x2" tree)
}
```

**Token object**:
```json
{
  "id": "goblin-1",        // Unique token ID
  "name": "Goblin Scout",  // Display name (short 1-3 words recommended)
  "x": 5,                  // Column position
  "y": 5,                  // Row position
  "cr": "1/8"              // Challenge rating (D&D) or difficulty level
}
```

**Terrain Types** (with default colors):

| Type | Color | Use |
|------|-------|-----|
| `grass` | Green | Natural terrain |
| `water` | Blue | Rivers, lakes, difficult terrain |
| `stone` | Gray | Paved floors, dungeon stone |
| `tree` | Dark green | Obstacles, line-of-sight blockers |
| `wall` | Dark gray | Walls, barriers |
| `door` | Gold | Doors, gates, transitions |
| `trap` | Red | Hazards, traps (not visible to players) |
| `treasure` | Yellow | Treasure, items |
| `floor` | Light gray | Interior floors, varied terrain |
| `default` | Gray | Unknown terrain type |

## Terrain Difficulty

Terrain difficulty affects movement and line-of-sight:

- **0 (Normal)**: Standard movement, no penalties
- **1 (Difficult)**: Half speed, `-5 ft movement` in D&D
- **2 (Very Difficult)**: Quarter speed or impassable

Example difficult terrain:
```json
{"x": 10, "y": 10, "type": "water", "difficulty": 1}
```

## Player Handouts

Generate simplified player-facing map handouts:

```bash
# Export battle maps only (tokens shown)
python scripts/python/map-export.py --dir specs/maps/ --output-dir output/handouts/ --format png

# Print PNG maps at 150 dpi for tabletop
# - 20×20 grid = 2×2 inches at 10 pixel/cell = 150 dpi handout
```

**What to do with PNG handouts**:
1. Print or display on projector during play
2. Save copies for player reference after session
3. Redact secret information (use transparent PNG layer or Photoshop)
4. Add player annotations (physical paper or digital markup)

## GM Reference Maps

Generate editable reference maps for prep:

```bash
python scripts/python/map-export.py --dir specs/maps/ --output-dir output/reference/ --format svg
```

**Then annotate in Inkscape**:
1. Open SVG in Inkscape
2. Add notes, measurements, or GM-only information
3. Create encounters or patrol routes as layers
4. Export to PDF for printing

## Integration with SpecKit Workflow

### In speckit.specify

Maps are catalogued:
```markdown
## Map Inventory

| Map ID | Name | Type | Session(s) | Size | Encounters | Handout? |
|--------|------|------|-----------|------|------------|----------|
| MAP-001 | Goblin Warren | Battle | S3 | 20×20 | ENC-015 | Yes |
| MAP-002 | Kingdom Overview | Regional | S1–S10 | 120×80 | — | Yes |
```

### In speckit.plan

Maps.md document is generated:
- Lists all maps and their properties
- Links to JSON files
- Tracks handout versions
- Documents session assignments

### In speckit.compile

Maps are automatically exported **and integrated into story output**:

```bash
# During compile, these run automatically:
python scripts/python/map-export.py --dir specs/maps/ --output-dir output/handouts/ --format png
python scripts/python/map-export.py --dir specs/maps/ --output-dir output/reference/ --format svg

# Then maps are integrated into:
# - Twine/SugarCube: Embedded passages + "Maps" menu
# - Ink: HTML wrapper with sidebar gallery
# - Generic: Linked map pages in story navigation
```

**See [MAP-ENGINE-INTEGRATION.md](MAP-ENGINE-INTEGRATION.md) for detailed instructions on how maps appear in each story output format.**

## Troubleshooting

### "Pillow not installed" error

Install PIL/Pillow for PNG export:
```bash
pip install Pillow
```

### PNG export produces blank image

Check that tiles and tokens have valid coordinates within map bounds:
```json
{
  "width": 20,
  "height": 20,
  "tiles": [
    {"x": 0, "y": 0, "type": "grass"}  // ✓ Valid (0 ≤ x,y < 20)
    {"x": 25, "y": 0, "type": "water"}  // ✗ Out of bounds (x > 20)
  ]
}
```

### Map viewer doesn't load JSON

Ensure JSON is valid:
```bash
# Validate JSON syntax
python -m json.tool specs/maps/your-map.json
```

### Exported images are too small/large

Adjust cell size in pixels:
```bash
# Larger cells = larger image
python scripts/python/map-export.py --input specs/maps/map.json --output map.png --cell-size 20

# Smaller cells = smaller image
python scripts/python/map-export.py --input specs/maps/map.json --output map.png --cell-size 5
```

## Examples

### Battle Map (D&D 5e)

```json
{
  "name": "Dwarven Mine - Level 3",
  "type": "battle",
  "session": 5,
  "scale": "5ft",
  "width": 24,
  "height": 20,
  "tiles": [
    {"x": 0, "y": 0, "type": "stone", "difficulty": 0},
    {"x": 5, "y": 5, "type": "wall", "difficulty": 0},
    {"x": 10, "y": 10, "type": "trap", "difficulty": 0},
    {"x": 15, "y": 15, "type": "water", "difficulty": 1}
  ],
  "tokens": [
    {"id": "dwarf-warrior", "name": "Thorin", "x": 2, "y": 2, "cr": "3"},
    {"id": "dwarf-mage", "name": "Elara", "x": 20, "y": 18, "cr": "2"},
    {"id": "orc-1", "name": "Orc Raider", "x": 12, "y": 10, "cr": "1/2"}
  ],
  "encounters": ["ENC-047"],
  "lighting": "torchlight",
  "notes": "Party enters from west. Secret passage at (22, 3) DC 18 Perception. Trap at (10, 10) - DC 14 save for half 2d6 damage."
}
```

### Regional Campaign Map

```json
{
  "name": "Kingdom of Valdren",
  "type": "regional",
  "session": 1,
  "scale": "10mi",
  "width": 120,
  "height": 100,
  "tiles": [
    {"x": 0, "y": 0, "type": "grass", "difficulty": 0},
    {"x": 50, "y": 50, "type": "water", "difficulty": 1},
    {"x": 80, "y": 30, "type": "tree", "difficulty": 2}
  ],
  "tokens": [
    {"id": "city-1", "name": "Capital", "x": 60, "y": 50, "cr": "Major"},
    {"id": "city-2", "name": "Port", "x": 80, "y": 40, "cr": "Medium"}
  ],
  "notes": "Party starts at Capital. Forest provides cover but slows movement. River ford at (50, 50)."
}
```

## Advanced Usage

### Batch Process with Script

Create a shell script to export all maps with consistent settings:

```bash
#!/bin/bash
# export-all-maps.sh

MAPS_DIR="specs/maps"
OUTPUT_DIR="output/exports"

mkdir -p "$OUTPUT_DIR/handouts"
mkdir -p "$OUTPUT_DIR/reference"

python scripts/python/map-export.py \
  --dir "$MAPS_DIR" \
  --output-dir "$OUTPUT_DIR/handouts" \
  --format png \
  --cell-size 15

python scripts/python/map-export.py \
  --dir "$MAPS_DIR" \
  --output-dir "$OUTPUT_DIR/reference" \
  --format svg

echo "✓ All maps exported to $OUTPUT_DIR"
```

Run with:
```bash
bash export-all-maps.sh
```

### Custom Terrain Colors

To add or modify terrain colors, edit `scripts/python/map-export.py`:

```python
TERRAIN_COLORS = {
    'grass': (58, 140, 66),
    'lava': (255, 100, 0),          # Add custom terrain
    'mystical': (128, 0, 255),
    # ... rest of colors
}
```

## API Reference

### map-viewer.html

Browser-based map viewer. Features:
- Load JSON via file input
- Pan (drag), zoom (scroll), grid toggle
- Display terrain legend and token info
- Export to PNG
- Browse multiple loaded maps

### map-export.py

Python script for batch export.

```bash
python map-export.py --help
```

Usage:
- Single file export: `--input` + `--output`
- Batch export: `--dir` + `--output-dir`
- Format control: `--format` (png|svg)
- Styling: `--cell-size`, `--no-grid`

## Next Steps

1. **Create maps**: Add JSON files to `specs/maps/`
2. **Visualize**: Open `scripts/map-viewer.html` in browser
3. **Export**: Run `map-export.py` to create handouts
4. **Integrate**: Reference maps in node files and encounters
5. **Distribute**: Provide handouts to players before sessions

---

**Questions or bugs?** Report in the SpecKit issue tracker.
