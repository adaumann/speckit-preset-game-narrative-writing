#!/usr/bin/env python
import sys
import re

filepath = r"c:\Users\Andreas.Daumann\OneDrive\Source\speckit-preset-game-narrative-writing\game-rpg-narrative-writing\commands\speckit.plan.md"

try:
    # Read with UTF-8, replacing bad chars
    with open(filepath, 'r', encoding='utf-8', errors='replace') as f:
        content = f.read()
    
    # Fix mojibake patterns
    replacements = [
        ('â€"', '-'),      # em-dash mojibake
        ('â€"', '-'),      # en-dash mojibake  
        ('â€œ', '"'),      # left quote
        ('â€\x9d', '"'),   # right quote
        ('ï¿½', ''),       # corruption
        ('4ï¿½6', '4-6'),  # specific case
        ('–', '-'),        # actual en-dash
        ('—', '-'),        # actual em-dash
    ]
    
    for old, new in replacements:
        content = content.replace(old, new)
    
    # Write back as proper UTF-8
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print("SUCCESS: File cleaned and saved as UTF-8")
    sys.exit(0)
    
except Exception as e:
    print(f"ERROR: {e}")
    sys.exit(1)
