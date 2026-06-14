#!/usr/bin/env python3
"""
SpecKit Map Export Utility
Converts JSON map files to PNG/SVG images for player handouts and documentation.

Usage:
    python map-export.py --input maps/goblin-hideout.json --output handouts/goblin.png
    python map-export.py --input maps/regional.json --output reference/regional.svg --format svg
    python map-export.py --dir specs/maps/ --output-dir handouts/ --format png
"""

import json
import os
import sys
import argparse
from pathlib import Path

# Terrain color definitions (RGB)
TERRAIN_COLORS = {
    'grass': (58, 140, 66),
    'water': (37, 99, 235),
    'stone': (139, 139, 139),
    'tree': (45, 80, 22),
    'wall': (90, 90, 90),
    'door': (196, 167, 71),
    'trap': (255, 107, 107),
    'treasure': (255, 215, 0),
    'floor': (100, 100, 120),
    'default': (68, 68, 68)
}

TOKEN_COLOR = (231, 76, 60)
TOKEN_BORDER = (255, 255, 255)

def load_map_json(filepath):
    """Load JSON map file."""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            return json.load(f)
    except (json.JSONDecodeError, IOError) as e:
        print(f"Error loading {filepath}: {e}")
        return None

def export_png(map_data, output_path, cell_size=10, show_grid=True):
    """Export map to PNG using PIL/Pillow."""
    try:
        from PIL import Image, ImageDraw
    except ImportError:
        print("ERROR: Pillow not installed. Install with: pip install Pillow")
        return False

    width = map_data.get('width', 20)
    height = map_data.get('height', 20)
    
    # Create image with padding
    img_width = width * cell_size + 20
    img_height = height * cell_size + 20
    img = Image.new('RGB', (img_width, img_height), color=(26, 26, 46))
    draw = ImageDraw.Draw(img)

    # Draw grid if enabled
    if show_grid:
        grid_color = (80, 80, 100)
        for x in range(width + 1):
            x_pos = x * cell_size + 10
            draw.line([(x_pos, 10), (x_pos, height * cell_size + 10)], fill=grid_color, width=1)
        for y in range(height + 1):
            y_pos = y * cell_size + 10
            draw.line([(10, y_pos), (width * cell_size + 10, y_pos)], fill=grid_color, width=1)

    # Draw tiles
    if 'tiles' in map_data:
        for tile in map_data['tiles']:
            x = tile['x'] * cell_size + 10
            y = tile['y'] * cell_size + 10
            color = TERRAIN_COLORS.get(tile.get('type', 'default'), TERRAIN_COLORS['default'])
            draw.rectangle([x, y, x + cell_size - 1, y + cell_size - 1], fill=color, outline=(0, 0, 0))

    # Draw tokens
    if 'tokens' in map_data:
        for token in map_data['tokens']:
            x = token['x'] * cell_size + 10 + cell_size // 2
            y = token['y'] * cell_size + 10 + cell_size // 2
            radius = cell_size // 3
            draw.ellipse([x - radius, y - radius, x + radius, y + radius], fill=TOKEN_COLOR, outline=TOKEN_BORDER, width=2)

    # Save
    try:
        os.makedirs(os.path.dirname(output_path) or '.', exist_ok=True)
        img.save(output_path, 'PNG')
        print(f"✓ PNG exported: {output_path}")
        return True
    except Exception as e:
        print(f"Error saving PNG: {e}")
        return False

def export_svg(map_data, output_path, cell_size=10, show_grid=True):
    """Export map to SVG."""
    width = map_data.get('width', 20)
    height = map_data.get('height', 20)
    
    svg_width = width * cell_size + 20
    svg_height = height * cell_size + 20

    svg_lines = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{svg_width}" height="{svg_height}" viewBox="0 0 {svg_width} {svg_height}">',
        '<defs>',
        '<style>',
        '.grid-line { stroke: #505064; stroke-width: 1; }',
        '.tile { stroke: #000000; stroke-width: 0.5; }',
        '.token { fill: #e74c3c; stroke: #ffffff; stroke-width: 2; }',
        '.token-label { fill: #ffffff; font-size: 8px; text-anchor: middle; dominant-baseline: central; }',
        '</style>',
        '</defs>',
        f'<rect width="{svg_width}" height="{svg_height}" fill="#1a1a2e"/>',
    ]

    # Draw grid if enabled
    if show_grid:
        for x in range(width + 1):
            x_pos = x * cell_size + 10
            svg_lines.append(f'<line x1="{x_pos}" y1="10" x2="{x_pos}" y2="{height * cell_size + 10}" class="grid-line"/>')
        for y in range(height + 1):
            y_pos = y * cell_size + 10
            svg_lines.append(f'<line x1="10" y1="{y_pos}" x2="{width * cell_size + 10}" y2="{y_pos}" class="grid-line"/>')

    # Draw tiles
    if 'tiles' in map_data:
        for tile in map_data['tiles']:
            x = tile['x'] * cell_size + 10
            y = tile['y'] * cell_size + 10
            color = TERRAIN_COLORS.get(tile.get('type', 'default'), TERRAIN_COLORS['default'])
            color_hex = f'#{color[0]:02x}{color[1]:02x}{color[2]:02x}'
            svg_lines.append(f'<rect x="{x}" y="{y}" width="{cell_size}" height="{cell_size}" fill="{color_hex}" class="tile"/>')

    # Draw tokens
    if 'tokens' in map_data:
        for token in map_data['tokens']:
            x = token['x'] * cell_size + 10 + cell_size // 2
            y = token['y'] * cell_size + 10 + cell_size // 2
            radius = cell_size // 3
            token_name = token.get('name', 'T')[:3]
            svg_lines.append(f'<circle cx="{x}" cy="{y}" r="{radius}" class="token"/>')
            svg_lines.append(f'<text x="{x}" y="{y}" class="token-label">{token_name}</text>')

    # Add metadata comment
    map_name = map_data.get('name', 'Map')
    map_type = map_data.get('type', 'unknown')
    svg_lines.append(f'<!-- Map: {map_name} (Type: {map_type}) -->')
    svg_lines.append('</svg>')

    # Save
    try:
        os.makedirs(os.path.dirname(output_path) or '.', exist_ok=True)
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write('\n'.join(svg_lines))
        print(f"✓ SVG exported: {output_path}")
        return True
    except Exception as e:
        print(f"Error saving SVG: {e}")
        return False

def export_markdown_inventory(map_data_list, output_path):
    """Generate a markdown inventory of all maps."""
    md_lines = [
        "# Map Inventory",
        "",
        "| Map ID | Name | Type | Size | Encounters | Status |",
        "|--------|------|------|------|------------|--------|",
    ]

    for i, map_data in enumerate(map_data_list, 1):
        name = map_data.get('name', 'Unnamed')
        map_type = map_data.get('type', 'unknown')
        size = f"{map_data.get('width', '?')}×{map_data.get('height', '?')}"
        encounters = ', '.join(map_data.get('encounters', []))
        map_id = f"MAP-{i:03d}"
        
        md_lines.append(f"| {map_id} | {name} | {map_type} | {size} | {encounters or 'N/A'} | ✓ Exported |")

    md_lines.append("")

    try:
        os.makedirs(os.path.dirname(output_path) or '.', exist_ok=True)
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write('\n'.join(md_lines))
        print(f"✓ Markdown inventory: {output_path}")
        return True
    except Exception as e:
        print(f"Error saving inventory: {e}")
        return False

def main():
    parser = argparse.ArgumentParser(
        description='Export JSON maps to PNG/SVG images for SpecKit RPG campaigns'
    )
    parser.add_argument('--input', help='Input JSON map file')
    parser.add_argument('--output', help='Output image file')
    parser.add_argument('--format', choices=['png', 'svg'], default='png', help='Export format')
    parser.add_argument('--dir', help='Input directory (batch mode)')
    parser.add_argument('--output-dir', help='Output directory for batch export')
    parser.add_argument('--no-grid', action='store_true', help='Disable grid lines')
    parser.add_argument('--cell-size', type=int, default=10, help='Grid cell size in pixels')

    args = parser.parse_args()

    if args.dir and args.output_dir:
        # Batch mode: export all JSON files from directory
        map_dir = Path(args.dir)
        output_dir = Path(args.output_dir)
        output_dir.mkdir(parents=True, exist_ok=True)

        map_files = list(map_dir.glob('*.json'))
        if not map_files:
            print(f"No JSON files found in {map_dir}")
            return 1

        all_maps = []
        for json_file in map_files:
            map_data = load_map_json(json_file)
            if not map_data:
                continue

            all_maps.append(map_data)
            basename = json_file.stem

            if args.format == 'svg':
                output_file = output_dir / f"{basename}.svg"
                export_svg(map_data, str(output_file), args.cell_size, not args.no_grid)
            else:
                output_file = output_dir / f"{basename}.png"
                export_png(map_data, str(output_file), args.cell_size, not args.no_grid)

        # Generate inventory
        inventory_path = output_dir / 'INVENTORY.md'
        export_markdown_inventory(all_maps, str(inventory_path))

        print(f"\n✓ Batch export complete: {len(map_files)} maps")
        return 0

    elif args.input and args.output:
        # Single file mode
        map_data = load_map_json(args.input)
        if not map_data:
            return 1

        if args.format == 'svg':
            success = export_svg(map_data, args.output, args.cell_size, not args.no_grid)
        else:
            success = export_png(map_data, args.output, args.cell_size, not args.no_grid)

        return 0 if success else 1

    else:
        parser.print_help()
        return 1

if __name__ == '__main__':
    sys.exit(main())
