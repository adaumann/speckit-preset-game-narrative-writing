#!/usr/bin/env python3
"""
Postprocessing plugin system for Speckit.

Discovers and executes Python scripts from:
    specs/<specname>/postprocessing/*.py   (primary)
    specs/<specname>/postprocess/*.py      (legacy fallback)

Each script should expose a `postprocess(ctx)` function that receives:
    ctx = {
        "spec_path": Path        - spec directory
        "engine": str            - "sugarcube" | "ink"
        "stage": str             - STAGE_COMPILE | STAGE_POST_COMPILE | "export"
        "source_dir": Path       - directory with .twee/.ink source files
        "output_dir": Path       - compilation output directory (None during export)
    }

Scripts can modify source files in-place before compilation, or
output files after compilation.

Helpers provided:
    TweeParser(path)           - Parse a .twee file into structured passages
    STAGE_COMPILE              - "compile" (pre-compile)
    STAGE_POST_COMPILE         - "post-compile" (post-compile)
    STAGE_EXPORT               - "export"

Usage:
    from postprocess import run_postprocess, TweeParser, STAGE_COMPILE
    run_postprocess(spec_path, engine, stage, source_dir, output_dir=None)
"""

import importlib.util
import re
import sys
from pathlib import Path
from typing import Optional

# Stage constants for script convenience
STAGE_COMPILE = "compile"
STAGE_POST_COMPILE = "post-compile"
STAGE_EXPORT = "export"


class Passage:
    """Represents a single Twee passage."""

    def __init__(self, name: str, tags: list, body: str, raw_header: str):
        self.name = name
        self.tags = tags
        self.body = body
        self.raw_header = raw_header

    def __repr__(self):
        return f"Passage({self.name!r}, tags={self.tags})"

    def has_tag(self, tag: str) -> bool:
        return tag in self.tags


class TweeParser:
    """Parse and modify a Twee source file.

    Usage:
        parser = TweeParser(Path("compile.twee"))
        for passage in parser.passages:
            print(passage.name)

        story = parser.find("StoryStylesheet")
        if story:
            story.body += "\\n  .passage { animation: fadeIn 0.4s; }\\n"
            parser.write()
    """

    PASSAGE_RE = re.compile(r"^::\s+(.+?)\s*(?:\[(.*?)\])?\s*$", re.MULTILINE)

    def __init__(self, path: Path):
        self.path = path
        self.raw = path.read_text(encoding="utf-8") if path.exists() else ""
        self.passages: list[Passage] = []
        self._parse()

    def _parse(self):
        """Split raw text into passages."""
        self.passages = []
        matches = list(self.PASSAGE_RE.finditer(self.raw))
        if not matches:
            return

        for i, m in enumerate(matches):
            header_line = m.group(0)
            name_and_tags = m.group(1).strip()
            tags_str = m.group(2) or ""

            # Name may have trailing tags separated by spaces before [tags]
            # e.g. "StoryStylesheet [stylesheet]" -> name="StoryStylesheet", tags=["stylesheet"]
            # e.g. "NODE-001 [header]" -> name="NODE-001", tags=["header"]
            name = name_and_tags
            tags = [t.strip() for t in tags_str.split() if t.strip()]

            start = m.end()
            end = matches[i + 1].start() if i + 1 < len(matches) else len(self.raw)
            body = self.raw[start:end].strip("\n")

            self.passages.append(Passage(name, tags, body, header_line))

    def find(self, name: str) -> Optional[Passage]:
        """Find a passage by exact name."""
        for p in self.passages:
            if p.name == name:
                return p
        return None

    def find_by_tag(self, tag: str) -> list[Passage]:
        """Find all passages with a given tag."""
        return [p for p in self.passages if p.has_tag(tag)]

    def find_by_pattern(self, pattern: str) -> list[Passage]:
        """Find passages whose name matches a regex pattern."""
        rx = re.compile(pattern)
        return [p for p in self.passages if rx.search(p.name)]

    def inject_css(self, css_block: str) -> bool:
        """Inject CSS into the StoryStylesheet passage. Idempotent."""
        stylesheet = self.find("StoryStylesheet")
        if not stylesheet:
            return False
        if css_block.strip() in stylesheet.body:
            return True  # Already present
        stylesheet.body += "\n" + css_block + "\n"
        return True

    def inject_widget(self, widget_name: str, widget_body: str) -> bool:
        """Inject or replace a widget passage. Idempotent for body content."""
        existing = self.find(widget_name)
        if existing:
            if widget_body.strip() in existing.body:
                return True  # Already present
            existing.body += "\n" + widget_body + "\n"
            return True
        # Create new widget passage at end
        self.passages.append(
            Passage(widget_name, ["widget"], widget_body, f":: {widget_name} [widget]")
        )
        return True

    def add_passage_header_footer(self, header: str = "", footer: str = "") -> int:
        """Add header/footer to every non-boilerplate passage.
        Returns number of passages modified.
        """
        skip = {"StoryData", "StoryInit", "StoryStylesheet", "StoryMenu",
                "StoryCaption", "StoryContinue"}
        count = 0
        for p in self.passages:
            if p.name in skip or p.has_tag("widget") or p.has_tag("script") or p.has_tag("stylesheet"):
                continue
            if header and header not in p.body:
                p.body = header + "\n" + p.body
            if footer and footer not in p.body:
                p.body = p.body + "\n" + footer
            count += 1
        return count

    def write(self):
        """Re-serialize passages and write back to disk."""
        parts = []
        for p in self.passages:
            if p.tags:
                parts.append(f":: {p.name} [{' '.join(p.tags)}]")
            else:
                parts.append(f":: {p.name}")
            parts.append(p.body)
            parts.append("")  # blank line between passages
        self.path.write_text("\n".join(parts).strip() + "\n", encoding="utf-8")


def _discover_scripts(spec_path: Path) -> list:
    # Primary: postprocessing/ (with "ing")
    pp_dir = spec_path / "postprocessing"
    if not pp_dir.exists():
        # Legacy fallback: postprocess/ (without "ing")
        pp_dir = spec_path / "postprocess"
    if not pp_dir.exists():
        return []
    scripts = sorted(pp_dir.glob("*.py"))
    return [s for s in scripts if s.is_file()]


def _load_script(script_path: Path):
    module_name = f"_speckit_pp_{script_path.stem}"
    spec = importlib.util.spec_from_file_location(module_name, script_path)
    if spec is None or spec.loader is None:
        print(f"   ⚠️  Could not load postprocess script: {script_path.name}")
        return None
    module = importlib.util.module_from_spec(spec)
    try:
        spec.loader.exec_module(module)
    except Exception as e:
        print(f"   ⚠️  Error loading {script_path.name}: {e}")
        return None
    return module


def run_postprocess(
    spec_path: Path,
    engine: str,
    stage: str,
    source_dir: Path,
    output_dir: Optional[Path] = None,
):
    scripts = _discover_scripts(spec_path)
    if not scripts:
        return

    print(f"\n🔧 Postprocessing ({stage})")
    ctx = {
        "spec_path": spec_path,
        "engine": engine,
        "stage": stage,
        "source_dir": source_dir,
        "output_dir": output_dir,
    }

    for script_path in scripts:
        module = _load_script(script_path)
        if module is None:
            continue
        if not hasattr(module, "postprocess"):
            print(f"   ⚠️  {script_path.name} has no postprocess() function")
            continue
        try:
            module.postprocess(ctx)
            print(f"   ✅ {script_path.name}")
        except Exception as e:
            print(f"   ❌ {script_path.name} failed: {e}")


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Run postprocessing scripts for a spec")
    parser.add_argument("--spec", required=True, help="Spec name or path")
    parser.add_argument("--engine", required=True, help="Target engine")
    parser.add_argument("--stage", required=True, choices=["export", "compile", "post-compile"])
    parser.add_argument("--source-dir", required=True, help="Source directory")
    parser.add_argument("--output-dir", help="Output directory (compile stage)")
    args = parser.parse_args()

    spec_name = args.spec.strip()
    if spec_name.startswith("specs/") or spec_name.startswith("specs\\"):
        spec_name = spec_name[6:]
    spec_path = Path("specs") / spec_name
    source_dir = Path(args.source_dir)
    output_dir = Path(args.output_dir) if args.output_dir else None

    run_postprocess(spec_path, args.engine, args.stage, source_dir, output_dir)
