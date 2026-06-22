"""
Example postprocess script: Inject passage header/footer widgets into every passage.

Copy this file into specs/<specname>/postprocessing/add_headers.py and customize.

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
        modified = parser.add_passage_header_footer(
            header="  <<passageHeader>>",
            footer="  <<passageFooter>>"
        )
        if modified > 0:
            # Also ensure the widget definitions exist
            parser.inject_widget(
                "passageHeader",
                '  <<widget "passageHeader">>\n    <div class="passage-header"></div>\n  <</widget>>'
            )
            parser.inject_widget(
                "passageFooter",
                '  <<widget "passageFooter">>\n    <div class="passage-footer"></div>\n  <</widget>>'
            )
            parser.write()
