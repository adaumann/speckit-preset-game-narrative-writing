"""
Example postprocess script: Inject CSS animations into the StoryStylesheet.

Copy this file into specs/<specname>/postprocessing/add_animations.py and customize.

Runs during: export or compile (modifies compile.twee)
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent / "scripts" / "python"))
from postprocess import TweeParser, STAGE_COMPILE


def postprocess(ctx):
    if ctx["stage"] != STAGE_COMPILE:
        return

    source_dir = ctx["source_dir"]
    for twee_file in source_dir.glob("*.twee"):
        parser = TweeParser(twee_file)

        animations = """
  @keyframes slideIn {
    from { transform: translateY(20px); opacity: 0; }
    to   { transform: translateY(0);    opacity: 1; }
  }
  @keyframes fadeIn {
    from { opacity: 0; }
    to   { opacity: 1; }
  }
  .passage {
    animation: slideIn 0.4s ease-out;
  }
  .choice {
    animation: fadeIn 0.3s ease-in;
  }
  a.internal-link {
    transition: all 0.2s ease;
  }
  a.internal-link:hover {
    transform: scale(1.02);
  }
"""
        if parser.inject_css(animations):
            parser.write()
