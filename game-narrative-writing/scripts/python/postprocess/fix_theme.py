"""
Example postprocess script: Replace or inject CSS theme into StoryStylesheet.

Copy this file into specs/<specname>/postprocessing/fix_theme.py and customize.

Runs during: export (modifies ui.twee) or compile (modifies compile.twee)
"""

import sys
from pathlib import Path

# Add the script directory to path so we can import postprocess helpers
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "scripts" / "python"))
from postprocess import TweeParser, STAGE_COMPILE


def postprocess(ctx):
    if ctx["stage"] != STAGE_COMPILE:
        return  # Only modify source, not compiled HTML

    source_dir = ctx["source_dir"]
    for twee_file in source_dir.glob("*.twee"):
        parser = TweeParser(twee_file)
        stylesheet = parser.find("StoryStylesheet")
        if not stylesheet:
            continue

        new_theme = """
  #passages {
    max-width: 42em;
    margin: 0 auto;
    font-family: Georgia, serif;
    font-size: 18px;
    line-height: 1.8;
    color: #2d2d2d;
  }
  body {
    background: #faf8f5;
  }
  .passage {
    margin-bottom: 1.5em;
    opacity: 0;
    animation: fadeIn 0.5s ease-in forwards;
  }
  @keyframes fadeIn {
    to { opacity: 1; }
  }
  a.internal-link, a.link-internal {
    color: #8b4513;
    text-decoration: none;
    border-bottom: 1px dotted #8b4513;
  }
  a.internal-link:hover {
    color: #a0522d;
    border-bottom: 1px solid #a0522d;
  }
"""
        # Replace existing stylesheet content (everything after header)
        stylesheet.body = new_theme.strip()
        parser.write()
