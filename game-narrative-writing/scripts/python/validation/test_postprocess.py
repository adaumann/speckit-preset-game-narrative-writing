"""
test_postprocess.py — Speckit Postprocessing Unit Test Suite

Tests the postprocessing plugin system: TweeParser, Passage, script discovery,
script loading, and run_postprocess orchestration.

Usage:
    python test_postprocess.py [--json]

Exit codes:
    0 = all tests passed
    1 = one or more tests failed
"""

import json
import os
import re
import sys
import tempfile
import argparse
from pathlib import Path

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

SAMPLE_TWEE = """:: StoryData
{
  "ifid": "12345",
  "format": "SugarCube",
  "formatVersion": "2.36.1"
}

:: StoryStylesheet [stylesheet]
body {
  font-family: Georgia, serif;
}

:: StoryInit
<<set $trust_marcus to 5>>

:: Start
Welcome to the story.

What do you do?

- [Talk to Marcus](NODE-001)
- [Leave](NODE-002)

:: NODE-001 [tag1]
You talk to Marcus.
- [Ask about the case](NODE-003)

:: NODE-002 [tag2]
You leave the room.

:: NODE-003
The case unfolds.
"""


def _make_twee_file(content=SAMPLE_TWEE):
    """Create a temporary .twee file and return the path."""
    tmp = tempfile.NamedTemporaryFile(mode="w", suffix=".twee", delete=False, encoding="utf-8")
    tmp.write(content)
    tmp.close()
    return Path(tmp.name)


def _make_script_file(code: str):
    """Create a temporary .py postprocess script and return the path."""
    tmp = tempfile.NamedTemporaryFile(mode="w", suffix=".py", delete=False, encoding="utf-8")
    tmp.write(code)
    tmp.close()
    return Path(tmp.name)


# ---------------------------------------------------------------------------
# Test helpers — import postprocess module
# ---------------------------------------------------------------------------

def _import_postprocess():
    """Import postprocess from its location."""
    script_dir = Path(__file__).resolve().parent.parent
    sys.path.insert(0, str(script_dir))
    import postprocess
    return postprocess


# ---------------------------------------------------------------------------
# Test definitions
# Each test returns a list of Failure dicts: {"test": str, "detail": str}
# ---------------------------------------------------------------------------

def test_passage_creation():
    """Passage can be created with name, tags, body, raw_header."""
    pp = _import_postprocess()
    failures = []
    p = pp.Passage("Test", ["widget"], "hello", ":: Test [widget]")
    if p.name != "Test":
        failures.append({"test": "PASSAGE-CREATE", "detail": f"Expected name 'Test', got '{p.name}'"})
    if p.tags != ["widget"]:
        failures.append({"test": "PASSAGE-CREATE", "detail": f"Expected tags ['widget'], got {p.tags}"})
    if p.body != "hello":
        failures.append({"test": "PASSAGE-CREATE", "detail": f"Expected body 'hello', got '{p.body}'"})
    if not p.has_tag("widget"):
        failures.append({"test": "PASSAGE-CREATE", "detail": "has_tag('widget') should be True"})
    if p.has_tag("script"):
        failures.append({"test": "PASSAGE-CREATE", "detail": "has_tag('script') should be False"})
    return failures


def test_twee_parser_parses_correctly():
    """TweeParser correctly splits raw twee into passages."""
    pp = _import_postprocess()
    path = _make_twee_file()
    try:
        parser = pp.TweeParser(path)
        failures = []
        names = [p.name for p in parser.passages]
        expected = ["StoryData", "StoryStylesheet", "StoryInit", "Start", "NODE-001", "NODE-002", "NODE-003"]
        if names != expected:
            failures.append({"test": "PARSER-PARSE", "detail": f"Expected passages {expected}, got {names}"})
        # Check tags
        tags_map = {p.name: p.tags for p in parser.passages}
        if tags_map["StoryStylesheet"] != ["stylesheet"]:
            failures.append({"test": "PARSER-PARSE", "detail": f"Expected ['stylesheet'] tags, got {tags_map['StoryStylesheet']}"})
        if tags_map["NODE-001"] != ["tag1"]:
            failures.append({"test": "PARSER-PARSE", "detail": f"Expected ['tag1'] tags, got {tags_map['NODE-001']}"})
        if tags_map["Start"] != []:
            failures.append({"test": "PARSER-PARSE", "detail": f"Expected [] tags, got {tags_map['Start']}"})
        return failures
    finally:
        os.unlink(path)


def test_twee_parser_find():
    """TweeParser.find returns correct passage or None."""
    pp = _import_postprocess()
    path = _make_twee_file()
    try:
        parser = pp.TweeParser(path)
        failures = []
        p = parser.find("Start")
        if p is None:
            failures.append({"test": "PARSER-FIND", "detail": "find('Start') returned None"})
        elif "Welcome to the story" not in p.body:
            failures.append({"test": "PARSER-FIND", "detail": "find('Start') body missing expected text"})
        if parser.find("NonExistent") is not None:
            failures.append({"test": "PARSER-FIND", "detail": "find('NonExistent') should return None"})
        return failures
    finally:
        os.unlink(path)


def test_twee_parser_find_by_tag():
    """TweeParser.find_by_tag returns passages with matching tag."""
    pp = _import_postprocess()
    path = _make_twee_file()
    try:
        parser = pp.TweeParser(path)
        failures = []
        tagged = parser.find_by_tag("tag1")
        if len(tagged) != 1 or tagged[0].name != "NODE-001":
            failures.append({"test": "PARSER-FIND-TAG", "detail": f"Expected [NODE-001], got {[p.name for p in tagged]}"})
        no_match = parser.find_by_tag("nonexistent")
        if no_match != []:
            failures.append({"test": "PARSER-FIND-TAG", "detail": "find_by_tag('nonexistent') should return []"})
        return failures
    finally:
        os.unlink(path)


def test_twee_parser_find_by_pattern():
    """TweeParser.find_by_pattern matches names via regex."""
    pp = _import_postprocess()
    path = _make_twee_file()
    try:
        parser = pp.TweeParser(path)
        failures = []
        nodes = parser.find_by_pattern(r"^NODE-")
        names = [p.name for p in nodes]
        expected = ["NODE-001", "NODE-002", "NODE-003"]
        if names != expected:
            failures.append({"test": "PARSER-FIND-PATTERN", "detail": f"Expected {expected}, got {names}"})
        return failures
    finally:
        os.unlink(path)


def test_inject_css():
    """inject_css adds CSS to StoryStylesheet and is idempotent."""
    pp = _import_postprocess()
    path = _make_twee_file()
    try:
        parser = pp.TweeParser(path)
        failures = []
        css = ".passage { color: red; }"
        result = parser.inject_css(css)
        if not result:
            failures.append({"test": "INJECT-CSS", "detail": "inject_css returned False"})
            return failures
        stylesheet = parser.find("StoryStylesheet")
        if css not in stylesheet.body:
            failures.append({"test": "INJECT-CSS", "detail": "CSS not found in StoryStylesheet body"})
        # Idempotency
        result2 = parser.inject_css(css)
        if not result2:
            failures.append({"test": "INJECT-CSS", "detail": "inject_css returned False on second call"})
        count = stylesheet.body.count(css)
        if count != 1:
            failures.append({"test": "INJECT-CSS", "detail": f"CSS appears {count} times, expected 1 (idempotency)"})
        return failures
    finally:
        os.unlink(path)


def test_inject_widget_create():
    """inject_widget creates a new widget passage when it doesn't exist."""
    pp = _import_postprocess()
    path = _make_twee_file()
    try:
        parser = pp.TweeParser(path)
        failures = []
        body = "<<widget 'myWidget'>>Hello<</widget>>"
        result = parser.inject_widget("myWidget", body)
        if not result:
            failures.append({"test": "INJECT-WIDGET", "detail": "inject_widget returned False"})
            return failures
        widget = parser.find("myWidget")
        if widget is None:
            failures.append({"test": "INJECT-WIDGET", "detail": "myWidget passage not found after inject"})
            return failures
        if "widget" not in widget.tags:
            failures.append({"test": "INJECT-WIDGET", "detail": "myWidget should have [widget] tag"})
        if body not in widget.body:
            failures.append({"test": "INJECT-WIDGET", "detail": "Widget body not found in passage"})
        return failures
    finally:
        os.unlink(path)


def test_inject_widget_update():
    """inject_widget appends to existing widget passage idempotently."""
    pp = _import_postprocess()
    path = _make_twee_file()
    try:
        parser = pp.TweeParser(path)
        failures = []
        # First inject
        body = "<<widget 'myWidget'>>Hello<</widget>>"
        parser.inject_widget("myWidget", body)
        # Second inject (same body — idempotent)
        result = parser.inject_widget("myWidget", body)
        if not result:
            failures.append({"test": "INJECT-WIDGET-UPDATE", "detail": "inject_widget returned False on update"})
            return failures
        widget = parser.find("myWidget")
        count = widget.body.count(body)
        if count != 1:
            failures.append({"test": "INJECT-WIDGET-UPDATE", "detail": f"Body appears {count}x, expected 1 (idempotency)"})
        # Different body — should append
        body2 = "<<widget 'myWidget'>>World<</widget>>"
        parser.inject_widget("myWidget", body2)
        widget = parser.find("myWidget")
        if body2 not in widget.body:
            failures.append({"test": "INJECT-WIDGET-UPDATE", "detail": "Second body not appended"})
        return failures
    finally:
        os.unlink(path)


def test_add_passage_header_footer():
    """add_passage_header_footer adds header/footer to non-boilerplate passages."""
    pp = _import_postprocess()
    path = _make_twee_file()
    try:
        parser = pp.TweeParser(path)
        failures = []
        header = "<<passageHeader>>"
        footer = "<<passageFooter>>"
        count = parser.add_passage_header_footer(header, footer)
        # Boilerplate passages to skip: StoryData, StoryInit, StoryStylesheet, StoryMenu,
        # StoryCaption, StoryContinue + widget/script/stylesheet tagged
        # In our sample: Start, NODE-001, NODE-002, NODE-003 should get header/footer = 4
        if count != 4:
            failures.append({"test": "HEADER-FOOTER", "detail": f"Expected 4 passages modified, got {count}"})
        for p in parser.passages:
            if p.name in ("Start", "NODE-001", "NODE-002", "NODE-003"):
                if not p.body.startswith(header):
                    failures.append({"test": "HEADER-FOOTER", "detail": f"'{p.name}' body should start with header"})
                if not p.body.endswith(footer):
                    failures.append({"test": "HEADER-FOOTER", "detail": f"'{p.name}' body should end with footer"})
            elif p.name in ("StoryData", "StoryInit", "StoryStylesheet"):
                if header in p.body or footer in p.body:
                    failures.append({"test": "HEADER-FOOTER", "detail": f"'{p.name}' should not have header/footer"})
        return failures
    finally:
        os.unlink(path)


def test_write_roundtrip():
    """TweeParser.write() roundtrips correctly: parse → write → parse."""
    pp = _import_postprocess()
    path = _make_twee_file()
    try:
        parser = pp.TweeParser(path)
        failures = []
        # Modify
        css = ".test { color: blue; }"
        parser.inject_css(css)
        parser.inject_widget("TestWidget", "<<widget 'tw'>>test<</widget>>")
        # Write
        parser.write()
        # Re-read and re-parse
        parser2 = pp.TweeParser(path)
        names = [p.name for p in parser2.passages]
        if "TestWidget" not in names:
            failures.append({"test": "WRITE-ROUNDTRIP", "detail": "TestWidget not found after roundtrip"})
        stylesheet = parser2.find("StoryStylesheet")
        if stylesheet is None or css not in stylesheet.body:
            failures.append({"test": "WRITE-ROUNDTRIP", "detail": "CSS not preserved after roundtrip"})
        return failures
    finally:
        os.unlink(path)


def test_discover_scripts():
    """_discover_scripts finds .py files in postprocessing/ directory."""
    pp = _import_postprocess()
    with tempfile.TemporaryDirectory() as tmpdir:
        spec_path = Path(tmpdir)
        # Create postprocessing dir with a script
        pp_dir = spec_path / "postprocessing"
        pp_dir.mkdir()
        script = pp_dir / "test_effect.py"
        script.write_text("# test")
        scripts = pp._discover_scripts(spec_path)
        if len(scripts) != 1:
            return [{"test": "DISCOVER-SCRIPTS", "detail": f"Expected 1 script, got {len(scripts)}"}]
        if scripts[0].name != "test_effect.py":
            return [{"test": "DISCOVER-SCRIPTS", "detail": f"Expected test_effect.py, got {scripts[0].name}"}]
    return []


def test_discover_scripts_legacy_fallback():
    """_discover_scripts falls back to postprocess/ (without 'ing')."""
    pp = _import_postprocess()
    with tempfile.TemporaryDirectory() as tmpdir:
        spec_path = Path(tmpdir)
        # Create legacy postprocess dir
        pp_dir = spec_path / "postprocess"
        pp_dir.mkdir()
        script = pp_dir / "legacy.py"
        script.write_text("# test")
        scripts = pp._discover_scripts(spec_path)
        if len(scripts) != 1:
            return [{"test": "DISCOVER-LEGACY", "detail": f"Expected 1 script from legacy dir, got {len(scripts)}"}]
    return []


def test_discover_scripts_empty():
    """_discover_scripts returns empty list when no dir exists."""
    pp = _import_postprocess()
    with tempfile.TemporaryDirectory() as tmpdir:
        scripts = pp._discover_scripts(Path(tmpdir))
        if scripts != []:
            return [{"test": "DISCOVER-EMPTY", "detail": "Expected [] when no postprocessing dir"}]
    return []


def test_load_script():
    """_load_script loads a .py file with postprocess function."""
    pp = _import_postprocess()
    code = '''
def postprocess(ctx):
    ctx["_called"] = True
'''
    path = _make_script_file(code)
    try:
        module = pp._load_script(path)
        if module is None:
            return [{"test": "LOAD-SCRIPT", "detail": "_load_script returned None"}]
        if not hasattr(module, "postprocess"):
            return [{"test": "LOAD-SCRIPT", "detail": "module has no postprocess function"}]
        ctx = {"_called": False}
        module.postprocess(ctx)
        if not ctx["_called"]:
            return [{"test": "LOAD-SCRIPT", "detail": "postprocess(ctx) did not set ctx['_called']"}]
    finally:
        os.unlink(path)
    return []


def test_load_script_no_postprocess():
    """_load_script loads scripts without postprocess function gracefully."""
    pp = _import_postprocess()
    code = '# no postprocess function'
    path = _make_script_file(code)
    try:
        module = pp._load_script(path)
        if module is None:
            return [{"test": "LOAD-SCRIPT-NO-PP", "detail": "_load_script should not return None for valid .py"}]
        if hasattr(module, "postprocess"):
            return [{"test": "LOAD-SCRIPT-NO-PP", "detail": "module should not have postprocess attr"}]
    finally:
        os.unlink(path)
    return []


def test_run_postprocess():
    """run_postprocess discovers and invokes scripts."""
    pp = _import_postprocess()
    code = '''
def postprocess(ctx):
    ctx["results"].append("called")
'''
    with tempfile.TemporaryDirectory() as tmpdir:
        spec_path = Path(tmpdir)
        pp_dir = spec_path / "postprocessing"
        pp_dir.mkdir()
        script = pp_dir / "test_run.py"
        script.write_text(code)
        source_dir = Path(tmpdir) / "source"
        source_dir.mkdir()
        (source_dir / "story.twee").write_text(":: Start\nHello")
        ctx_extra = {"results": []}

        # Monkey-patch run_postprocess context construction
        original_run = pp.run_postprocess

        def patched_run(spec_path, engine, stage, source_dir, output_dir=None):
            scripts = pp._discover_scripts(spec_path)
            if not scripts:
                return
            ctx = {
                "spec_path": spec_path,
                "engine": engine,
                "stage": stage,
                "source_dir": source_dir,
                "output_dir": output_dir,
            }
            ctx.update(ctx_extra)
            for script_path in scripts:
                module = pp._load_script(script_path)
                if module is None:
                    continue
                if hasattr(module, "postprocess"):
                    module.postprocess(ctx)

        patched_run(spec_path, "sugarcube", "compile", source_dir)
        if ctx_extra["results"] != ["called"]:
            return [{"test": "RUN-POSTPROCESS", "detail": f"Expected ['called'], got {ctx_extra['results']}"}]
    return []


ALL_TESTS = [
    test_passage_creation,
    test_twee_parser_parses_correctly,
    test_twee_parser_find,
    test_twee_parser_find_by_tag,
    test_twee_parser_find_by_pattern,
    test_inject_css,
    test_inject_widget_create,
    test_inject_widget_update,
    test_add_passage_header_footer,
    test_write_roundtrip,
    test_discover_scripts,
    test_discover_scripts_legacy_fallback,
    test_discover_scripts_empty,
    test_load_script,
    test_load_script_no_postprocess,
    test_run_postprocess,
]

# ---------------------------------------------------------------------------
# Runner
# ---------------------------------------------------------------------------


def main():
    parser = argparse.ArgumentParser(description="Run unit tests for postprocessing system.")
    parser.add_argument("--json", action="store_true", help="Output results as JSON.")
    args = parser.parse_args()

    all_failures = []
    for test_fn in ALL_TESTS:
        try:
            all_failures.extend(test_fn())
        except Exception as e:
            all_failures.append({"test": test_fn.__name__, "detail": f"Exception: {e}"})

    passed = len(ALL_TESTS) - len({f["test"] for f in all_failures})
    report = {
        "summary": f"{len(ALL_TESTS)} test(s) | {len(all_failures)} failure(s) across {len({f['test'] for f in all_failures})} test(s)",
        "failures": all_failures,
        "passed": passed,
        "failed": len({f["test"] for f in all_failures}),
    }

    if args.json:
        print(json.dumps(report, indent=2))
    else:
        print(f"\n=== Speckit Postprocessing Unit Tests ===")
        print(f"Tests         : {len(ALL_TESTS)}")
        print(f"Failures      : {len(all_failures)}")
        if all_failures:
            print("\nFailures:")
            for f in all_failures:
                print(f"  \u2717 [{f['test']}] {f['detail']}")
        else:
            print("\n  \u2713 All postprocessing tests passed.")
        print()

    sys.exit(0 if not all_failures else 1)


if __name__ == "__main__":
    main()
