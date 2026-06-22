#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Compile Twee/Ink files using native compilers (tweego.exe, inklecate.exe).

This is a thin wrapper that:
1. Locates source files (.twee, .ink, .rpy)
2. Calls the appropriate compiler
3. Handles compilation errors with auto-fix and retry
4. Optionally receives error context from speckit.implement via --error

Usage:
    python compile.py --spec <specname> --engine <engine>
    python compile.py --spec <specname> --engine ink --error "NODE-001 not found"
"""

import argparse
import re
import subprocess
import sys
import uuid
from pathlib import Path
from typing import Optional
import yaml

from postprocess import run_postprocess

# Fix Unicode encoding for Windows console
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')


class CompileWrapper:
    """Thin wrapper for native compilers (tweego, inklecate)."""
    
    def __init__(self, spec_path: Path, engine: str, output_dir: Optional[Path] = None):
        self.spec_path = spec_path
        self.engine = engine.lower()
        self.output_dir = output_dir or spec_path / f"output/{engine}"
        self.draft_dir = spec_path / f"draft/{engine}"
        self.export_dir = spec_path / f"export/{engine}"
        self.source_dir = None
        self.source_label = "Draft"
        self.errors = []
        self.max_retries = 3
        self.retry_count = 0
        # Locate preset templates directory (handles both presets)
        self._template_dir = self._resolve_template_dir()
        
    def run(self, error_context: Optional[str] = None) -> bool:
        """Execute compilation with optional error context."""
        # Prefer export/ over draft/ when export exists
        if self.export_dir.exists():
            self.source_dir = self.export_dir
            self.source_label = "Export"
        elif self.draft_dir.exists():
            self.source_dir = self.draft_dir
            self.source_label = "Draft"
        
        print(f"🎮 Speckit Compiler")
        print(f"📦 Spec: {self.spec_path.name}")
        print(f"🔧 Engine: {self.engine}")
        if self.source_dir:
            print(f"📁 Source ({self.source_label}): {self.source_dir}")
        print(f"📤 Output: {self.output_dir}")
        
        if error_context:
            print(f"⚠️  Error context: {error_context}")
        
        # Check if engine is allowed by constitution
        allowed_engines = self._get_allowed_engines()
        if allowed_engines and self.engine not in allowed_engines:
            print(f"\n❌ Error: Engine '{self.engine}' not in constitution export_engines: {allowed_engines}")
            print(f"   Configure export_engines in constitution.md or spec.yml")
            return False
        
        # Validate setup
        if not self._validate_setup():
            return False
        
        # Find source file
        source_files = self._find_source_files()
        if not source_files:
            print(f"❌ Error: No {self.engine} source files found")
            return False
        
        print(f"\n📄 Source: {len(source_files)} file(s)")
        for f in source_files:
            print(f"   • {f.name}")
        
        # Prepare combined compile source with mechanic hook conversion
        print(f"\n📦 Preparing combined source...")
        compile_file = self._create_compile_twee(source_files)
        
        # Run postprocessing BEFORE compilation so scripts can
        # transform the combined file (convert tokens, add headers, etc.)
        run_postprocess(
            spec_path=self.spec_path,
            engine=self.engine,
            stage="compile",
            source_dir=self.output_dir,
            output_dir=self.output_dir,
        )
        
        # Attempt compilation with retries.
        # Auto-fix modifies compile_file directly, so don't re-create between retries.
        compile_files = [compile_file]
        print(f"\n🔄 Compilation attempts (max: {self.max_retries}):")
        while self.retry_count < self.max_retries:
            self.retry_count += 1
            print(f"\n▶️  Attempt {self.retry_count}/{self.max_retries}...")
            
            if self._compile(compile_files):
                print(f"\n✅ Compilation succeeded on attempt {self.retry_count}")
                # Run postprocessing after compilation for output file transforms
                run_postprocess(
                    spec_path=self.spec_path,
                    engine=self.engine,
                    stage="post-compile",
                    source_dir=self.output_dir,
                    output_dir=self.output_dir,
                )
                return True
            
            if self.retry_count >= self.max_retries:
                print(f"\n❌ Compilation failed after {self.max_retries} attempts")
                print(f"   Check the errors above and fix the source files")
                return False
            
            print(f"⏳ Will retry in next attempt...")
        
        return False
    
    def _resolve_template_dir(self) -> Path:
        """Find the preset templates directory.
        
        Uses the preset that compile.py is installed in first,
        then falls back to the other preset.
        """
        script_dir = Path(__file__).parent
        own_preset = script_dir.parent.parent  # e.g. game-narrative-writing/
        own_templates = own_preset / "templates"
        if own_templates.exists():
            return own_templates
        # Fallback: try sibling preset
        workspace_root = own_preset.parent
        sibling = "game-rpg-narrative-writing" if own_preset.name == "game-narrative-writing" else "game-narrative-writing"
        sibling_templates = workspace_root / sibling / "templates"
        if sibling_templates.exists():
            return sibling_templates
        return script_dir

    def _validate_setup(self) -> bool:
        """Check if spec and source directory (export or draft) exist."""
        if not self.spec_path.exists():
            print(f"❌ Error: Spec not found: {self.spec_path}")
            return False
        
        if not self.source_dir:
            print(f"❌ Error: No source files found. Checked:")
            print(f"   • Export: {self.export_dir}")
            print(f"   • Draft:  {self.draft_dir}")
            print(f"   Run speckit.implement (or speckit.export) first.")
            return False
        
        return True
    
    def _get_allowed_engines(self) -> Optional[list]:
        """Read export_engines from spec.yml or constitution.md."""
        # Try spec.yml first
        spec_yml = self.spec_path / "spec.yml"
        if spec_yml.exists():
            try:
                with open(spec_yml, 'r', encoding='utf-8') as f:
                    spec_data = yaml.safe_load(f) or {}
                if 'export_engines' in spec_data:
                    engines = spec_data['export_engines']
                    if isinstance(engines, list):
                        return engines
                    elif isinstance(engines, str):
                        return [engines]
            except Exception:
                pass
        
        # Try constitution.md (YAML front matter)
        constitution = self.spec_path / "constitution.md"
        if constitution.exists():
            try:
                with open(constitution, 'r', encoding='utf-8') as f:
                    content = f.read()
                    if content.startswith('---'):
                        parts = content.split('---', 2)
                        if len(parts) >= 2:
                            front_matter = yaml.safe_load(parts[1]) or {}
                            if 'export_engines' in front_matter:
                                engines = front_matter['export_engines']
                                if isinstance(engines, list):
                                    return engines
                                elif isinstance(engines, str):
                                    return [engines]
            except Exception:
                pass
        
        # No configuration found
        return None
    
    def _find_source_files(self) -> list:
        """Find all source files for the target engine.
        
        When using export/, collect all relevant engine files (includes
        boilerplate: init, widgets, ui). When using draft/, check for
        a pre-combined story file first, then collect NODE-* files.
        Falls back to .md files (generic drafts with [MECHANIC:...] tokens).
        """
        source_dir = self.source_dir
        is_export = self.source_label == "Export"
        
        if self.engine == 'sugarcube':
            if is_export:
                return sorted(source_dir.glob("*.twee"))
            story_file = source_dir / "story.twee"
            if story_file.exists():
                return [story_file]
            twee_files = sorted(source_dir.glob("NODE-*.twee"))
            if twee_files:
                return twee_files
            # Fallback: generic .md drafts with [MECHANIC:...] tokens
            return sorted(source_dir.glob("NODE-*.md"))
        
        elif self.engine == 'ink':
            if is_export:
                return sorted(source_dir.glob("*.ink"))
            story_file = source_dir / "story.ink"
            if story_file.exists():
                return [story_file]
            ink_files = sorted(source_dir.glob("NODE-*.ink"))
            if ink_files:
                return ink_files
            return sorted(source_dir.glob("NODE-*.md"))
        
        elif self.engine == 'renpy':
            if is_export:
                return sorted(source_dir.glob("*.rpy"))
            story_file = source_dir / "story.rpy"
            if story_file.exists():
                return [story_file]
            return sorted(source_dir.glob("NODE-*.rpy"))
        
        return []
    
    def _load_yaml_frontmatter(self, content: str) -> Optional[dict]:
        """Extract YAML front matter from file content."""
        if content.startswith('---'):
            parts = content.split('---', 2)
            if len(parts) >= 2:
                try:
                    return yaml.safe_load(parts[1]) or {}
                except Exception:
                    return None
        return None

    def _translate_mechanic_hooks(self, content: str) -> str:
        """Translate [MECHANIC:...] tokens to engine-native syntax."""
        if self.engine == 'sugarcube':
            return self._translate_to_sugarcube(content)
        elif self.engine == 'ink':
            return self._translate_to_ink(content)
        return content

    def _translate_to_sugarcube(self, content: str) -> str:
        lines = content.split('\n')
        result = []
        for line in lines:
            hook_match = re.match(r'^\s*\[MECHANIC:(\w+)\s+(.*?)\]\s*$', line)
            if hook_match:
                hook_type = hook_match.group(1)
                hook_args = hook_match.group(2)
                translated = self._sugarcube_hook(hook_type, hook_args)
                if translated:
                    result.append(translated)
                    continue
            close_match = re.match(r'^\s*\[/MECHANIC\]\s*$', line)
            if close_match:
                continue
            full_match = re.match(r'^\s*\[MECHANIC:(\w+)\s+(.*?)\]\[/MECHANIC\]\s*$', line)
            if full_match:
                translated = self._sugarcube_hook(full_match.group(1), full_match.group(2))
                if translated:
                    result.append(translated)
                    continue
            result.append(line)
        return '\n'.join(result)

    def _sugarcube_hook(self, hook_type: str, args: str) -> Optional[str]:
        hook_type = hook_type.upper()
        if hook_type == 'VISITED':
            m = re.search(r'(?:variable=)?\$?(\w+)', args)
            if m:
                return f"<<set ${m.group(1)} to true>>"
        elif hook_type == 'FLAG':
            m = re.search(r'(?:set|variable)=?\$?(\w+)', args)
            if m:
                return f"<<set ${m.group(1)} to true>>"
        elif hook_type == 'COUNTER':
            m = re.search(r'variable=\$?(\w+).*?delta=\+?(-?\d+)', args)
            if m:
                return f"<<set ${m.group(1)} += {m.group(2)}>>"
            m2 = re.search(r'variable=\$?(\w+).*?set=(-?\d+)', args)
            if m2:
                return f"<<set ${m2.group(1)} to {m2.group(2)}>>"
        elif hook_type == 'INVENTORY':
            m = re.search(r'(add|remove)=(\w+)', args)
            if m:
                action, item = m.group(1), m.group(2)
                if action == 'add':
                    return f"<<run $inv.push(\"{item}\")>>"
                elif action == 'remove':
                    return f"<<run $inv.delete(\"{item}\")>>"
        elif hook_type == 'TRUST':
            m = re.search(r'npc=(\w+).*?delta=([+-]?\d+)', args)
            if m:
                return f"<<set ${m.group(1)}Trust += {m.group(2)}>>"
        elif hook_type == 'CURRENCY':
            m = re.search(r'(?:variable=)?\$?(\w+).*?(add|remove|delta)=([+-]?\d+)', args)
            if m:
                var_name = m.group(1)
                delta = m.group(3)
                return f"<<set ${var_name} += {delta}>>"
        elif hook_type == 'NPC_STATE':
            m = re.search(r'npc=(\w+).*?set=(\w+)', args)
            if m:
                return f"<<set ${m.group(1)}_state to \"{m.group(2)}\">>"
        elif hook_type == 'ENDING_CONDITION':
            m = re.search(r'(?:variable=)?\$?(\w+).*?delta=([+-]?\d+)', args)
            if m:
                return f"<<set ${m.group(1)} += {m.group(2)}>>"
        elif hook_type == 'TIMER':
            m = re.search(r'(start|stop|tick)=(\w+).*?(?:duration=)?(\d+)?', args)
            if m:
                action, timer = m.group(1), m.group(2)
                if action == 'start' and m.group(3):
                    return f"<<set ${timer}Timer to {m.group(3)}>>"
                elif action == 'tick':
                    return f"<<set ${timer}Timer -= 1>>"
        elif hook_type == 'RANDOM':
            m = re.search(r'range=(\d+)-(\d+).*?target=(\w+)', args)
            if m:
                return f"<<set ${m.group(3)} to random({m.group(1)}, {m.group(2)})>>"
        elif hook_type == 'CLUE':
            m = re.search(r'set=(\w+)', args)
            if m:
                return f"<<set $clue_{m.group(1)} to true>>"
        elif hook_type == 'CHOICE_MEMORY':
            m = re.search(r'(?:variable=)?\$?(\w+).*?value=([\w\"]+)', args)
            if m:
                return f"<<set ${m.group(1)} to {m.group(2)}>>"
        elif hook_type == 'ATTRIBUTE':
            m = re.search(r'(?:modify|variable)=(\w+).*?delta=([+-]?\d+)', args)
            if m:
                return f"<<set $character.{m.group(1)} += {m.group(2)}>>"
        elif hook_type == 'QUEST':
            m = re.search(r'(advance|complete|fail)=(\w+)', args)
            if m:
                action, quest = m.group(1), m.group(2)
                if action == 'advance':
                    return f"<<advanceQuestStage \"{quest}\">>"
                elif action == 'complete':
                    return f"<<completeQuest \"{quest}\">>"
                elif action == 'fail':
                    return f"<<failQuest \"{quest}\">>"
        return None

    def _translate_to_ink(self, content: str) -> str:
        lines = content.split('\n')
        result = []
        for line in lines:
            hook_match = re.match(r'^\s*\[MECHANIC:(\w+)\s+(.*?)\]\s*$', line)
            if hook_match:
                hook_type = hook_match.group(1)
                hook_args = hook_match.group(2)
                translated = self._ink_hook(hook_type, hook_args)
                if translated:
                    result.append(translated)
                    continue
            close_match = re.match(r'^\s*\[/MECHANIC\]\s*$', line)
            if close_match:
                continue
            full_match = re.match(r'^\s*\[MECHANIC:(\w+)\s+(.*?)\]\[/MECHANIC\]\s*$', line)
            if full_match:
                translated = self._ink_hook(full_match.group(1), full_match.group(2))
                if translated:
                    result.append(translated)
                    continue
            result.append(line)
        return '\n'.join(result)

    def _ink_hook(self, hook_type: str, args: str) -> Optional[str]:
        hook_type = hook_type.upper()
        if hook_type == 'VISITED':
            m = re.search(r'(?:variable=)?\$?(\w+)', args)
            if m:
                return f"~ {m.group(1)} = true"
        elif hook_type == 'FLAG':
            m = re.search(r'(?:set|variable)=?\$?(\w+)', args)
            if m:
                return f"~ {m.group(1)} = true"
        elif hook_type == 'COUNTER':
            m = re.search(r'variable=\$?(\w+).*?delta=\+?(-?\d+)', args)
            if m:
                return f"~ {m.group(1)} += {m.group(2)}"
        elif hook_type == 'INVENTORY':
            m = re.search(r'(add|remove)=(\w+)', args)
            if m:
                action, item = m.group(1), m.group(2)
                if action == 'add':
                    return f"~ inv(\"{item}\")"
                elif action == 'remove':
                    return f"~ inv(\"{item}\", false)"
        elif hook_type == 'TRUST':
            m = re.search(r'npc=(\w+).*?delta=([+-]?\d+)', args)
            if m:
                return f"~ {m.group(1)}Trust += {m.group(2)}"
        elif hook_type == 'CURRENCY':
            m = re.search(r'(?:variable=)?\$?(\w+).*?(add|remove|delta)=([+-]?\d+)', args)
            if m:
                return f"~ {m.group(1)} += {m.group(3)}"
        elif hook_type == 'NPC_STATE':
            m = re.search(r'npc=(\w+).*?set=(\w+)', args)
            if m:
                return f"~ {m.group(1)}_state = \"{m.group(2)}\""
        elif hook_type == 'ENDING_CONDITION':
            m = re.search(r'(?:variable=)?\$?(\w+).*?delta=([+-]?\d+)', args)
            if m:
                return f"~ {m.group(1)} += {m.group(2)}"
        elif hook_type == 'TIMER':
            m = re.search(r'(start|stop|tick)=(\w+).*?(?:duration=)?(\d+)?', args)
            if m:
                action, timer = m.group(1), m.group(2)
                if action == 'start' and m.group(3):
                    return f"~ {timer}Timer = {m.group(3)}"
                elif action == 'tick':
                    return f"~ {timer}Timer -= 1"
        elif hook_type == 'RANDOM':
            m = re.search(r'range=(\d+)-(\d+).*?target=(\w+)', args)
            if m:
                return f"~ temp {m.group(3)} = RANDOM({m.group(1)}, {m.group(2)})"
        elif hook_type == 'CLUE':
            m = re.search(r'set=(\w+)', args)
            if m:
                return f"~ clue_{m.group(1)} = true"
        elif hook_type == 'CHOICE_MEMORY':
            m = re.search(r'(?:variable=)?\$?(\w+).*?value=([\w\"]+)', args)
            if m:
                return f"~ {m.group(1)} = {m.group(2)}"
        elif hook_type == 'ATTRIBUTE':
            m = re.search(r'(?:modify|variable)=(\w+).*?delta=([+-]?\d+)', args)
            if m:
                return f"~ character.{m.group(1)} += {m.group(2)}"
        elif hook_type == 'QUEST':
            m = re.search(r'(advance|complete|fail)=(\w+)', args)
            if m:
                action, quest = m.group(1), m.group(2)
                if action == 'advance':
                    return f"~ quest_{quest}_stage += 1"
                elif action == 'complete':
                    return f"~ quest_{quest}_complete = true"
                elif action == 'fail':
                    return f"~ quest_{quest}_failed = true"
        return None

    def _load_variables(self) -> list:
        """Parse variables.md for variable declarations."""
        path = self.spec_path / "variables.md"
        if not path.exists():
            return []
        content = path.read_text(encoding='utf-8')
        variables = []
        # Try YAML front matter first
        header = self._load_yaml_frontmatter(content)
        if header and 'variables' in header:
            for v in header['variables']:
                variables.append({
                    'name': v.get('name', ''),
                    'type': v.get('type', 'flag'),
                    'default': str(v.get('default', 'false')),
                })
            return variables
        # Fallback: parse markdown list format like `$var_name` — type — default
        var_pattern = re.compile(
            r'`\$([a-zA-Z_]\w*)`\s*(?:[:\-]\s*type:\s*(\w+))?\s*(?:[:\-]\s*default:\s*(\S+))?'
        )
        for m in var_pattern.finditer(content):
            variables.append({
                'name': m.group(1),
                'type': m.group(2) or 'flag',
                'default': m.group(3) or 'false',
            })
        return variables

    def _load_boilerplate_sugarcube(self, first_node: str) -> str:
        """Load sugarcube-boilerplate.twee template and fill placeholders."""
        template_path = self._template_dir / "sugarcube-boilerplate.twee"
        if not template_path.exists():
            # Fallback: generate minimal boilerplate
            return self._generate_minimal_story_data_sugarcube(first_node)

        content = template_path.read_text(encoding='utf-8')
        story_name = self._get_story_name()
        ifid = self._get_ifid()

        content = content.replace('{story_name}', story_name)
        content = content.replace('{ifid}', ifid)
        content = content.replace('{start_node}', first_node)

        # Inject variable initializations into StoryInit
        variables = self._load_variables()
        if variables:
            var_lines = ['']
            var_lines.append('  {- Variable initializations -}')
            for v in variables:
                default = v.get('default', 'false')
                vtype = v.get('type', 'flag')
                name = v['name']
                if vtype == 'flag':
                    val = 'true' if default in ('true', 'True', '1') else 'false'
                    var_lines.append(f'  <<set ${name} to {val}>>')
                elif vtype == 'string':
                    var_lines.append(f'  <<set ${name} to "{default}">>'  )
                elif vtype == 'inventory':
                    var_lines.append(f'  <<set ${name} to []>>')
                else:
                    var_lines.append(f'  <<set ${name} to {default}>>')
            var_block = '\n'.join(var_lines)
            # Insert after <<run setup()>>
            content = content.replace(
                '  <<run setup()>>\n',
                f'  <<run setup()>>{var_block}\n'
            )

        return content

    def _generate_minimal_story_data_sugarcube(self, first_node: str) -> str:
        """Fallback minimal boilerplate when template is missing."""
        story_name = self._get_story_name()
        ifid = self._get_ifid()
        return f''':: StoryData
{{
  "ifid": "{ifid}",
  "name": "{story_name}",
  "startnode": "{first_node}",
  "engine": "SugarCube",
  "engineversion": "2.30.0"
}}

:: StoryInit [header]
  <<run setup()>>
'''

    def _get_story_name(self) -> str:
        constitution = self._load_yaml_frontmatter_file("constitution.md")
        if constitution and 'story_name' in constitution:
            return constitution['story_name']
        return self.spec_path.name

    def _get_ifid(self) -> str:
        constitution = self._load_yaml_frontmatter_file("constitution.md")
        if constitution and 'ifid' in constitution:
            return str(constitution['ifid'])
        return str(uuid.uuid4()).upper()

    def _load_yaml_frontmatter_file(self, filename: str) -> Optional[dict]:
        """Load YAML front matter from a file in the spec directory."""
        path = self.spec_path / filename
        if not path.exists():
            return None
        try:
            content = path.read_text(encoding='utf-8')
            return self._load_yaml_frontmatter(content)
        except Exception:
            return None

    def _generate_var_decls_ink(self) -> str:
        """Generate VAR declarations for Ink."""
        lines = ['// Variable declarations']
        variables = self._load_variables()
        for v in variables:
            default = v.get('default', 'false')
            vtype = v.get('type', 'flag')
            name = v['name']
            if vtype == 'string':
                lines.append(f'VAR {name} = "{default}"')
            elif vtype == 'flag':
                val = 'true' if default in ('true', 'True', '1') else 'false'
                lines.append(f'VAR {name} = {val}')
            else:
                lines.append(f'VAR {name} = {default}')
        if len(lines) > 1:
            lines.append('')  # blank line after declarations
        return '\n'.join(lines)

    def _create_compile_twee(self, source_files: list) -> Path:
        """Create a combined compile source file from all source files.
        
        Converts [MECHANIC:...] tokens to engine-native syntax,
        strips YAML front matter, converts markdown choices to
        engine-appropriate links, and wraps bare prose in passage headers.
        Uses engine-appropriate extension (.twee for SugarCube, .ink for Ink).
        """
        ext = {'sugarcube': '.twee', 'ink': '.ink', 'renpy': '.rpy'}.get(self.engine, '.twee')
        self.output_dir.mkdir(parents=True, exist_ok=True)
        compile_file = self.output_dir / f"compile{ext}"

        passages = []
        has_story_data = False
        has_var_decls = False

        for src_path in source_files:
            content = src_path.read_text(encoding='utf-8')
            if ':: StoryData' in content:
                has_story_data = True
            if re.search(r'\bVAR\s+\w+\s*=', content):
                has_var_decls = True

            if src_path.suffix == '.md':
                # .md files need full conversion to engine format
                header = self._load_yaml_frontmatter(content)

                # Strip YAML front matter
                body = content
                if content.startswith('---'):
                    parts = content.split('---', 2)
                    if len(parts) >= 3:
                        body = parts[2].strip()

                # Convert [MECHANIC:...] tokens
                body = self._translate_mechanic_hooks(body)

                if self.engine == 'sugarcube':
                    node_id = src_path.stem
                    if header and 'node_id' in header:
                        node_id = header['node_id']
                    # Convert markdown choices to Twee wiki-links
                    body = re.sub(
                        r'-\s*\[([^\]]+)\]\(([^)]+)\)',
                        r'[[\1|\2]]',
                        body
                    )
                    # Build passage with header
                    lines = [f':: {node_id} [header]']
                    lines.append(f'  {{- Node ID: {node_id} -}}')
                    lines.append('')
                    for line in body.split('\n'):
                        lines.append(f'  {line}')
                    passages.append('\n'.join(lines))
                elif self.engine == 'ink':
                    node_id = src_path.stem.replace('-', '_').upper()
                    if header and 'node_id' in header:
                        node_id = header['node_id'].replace('-', '_').upper()
                    # Convert markdown choices to Ink diverts
                    body = re.sub(
                        r'-\s*\[([^\]]+)\]\(([^)]+)\)',
                        r'+ [\1] -> \2',
                        body
                    )
                    lines = [f'=== {node_id} ===']
                    lines.append(f'// Node ID: {src_path.stem}')
                    lines.append('')
                    for line in body.split('\n'):
                        lines.append(f'{line}')
                    passages.append('\n'.join(lines))
                else:
                    passages.append(body)
            else:
                # .twee / .ink files: keep as-is after hook conversion
                body = self._translate_mechanic_hooks(content)
                passages.append(body)

        # Prepend boilerplate if not already present in source files
        if self.engine == 'sugarcube' and not has_story_data:
            first_node = source_files[0].stem
            boilerplate = self._load_boilerplate_sugarcube(first_node)
            passages.insert(0, boilerplate)
            print(f"   StoryData + StoryInit from template (no boilerplate found)")
        elif self.engine == 'ink' and not has_var_decls:
            boilerplate = self._generate_var_decls_ink()
            passages.insert(0, boilerplate)
            print(f"   VAR declarations generated (no boilerplate found)")

        combined = '\n\n'.join(passages)
        compile_file.write_text(combined, encoding='utf-8')
        print(f"   {compile_file.name} — {len(passages)} passage(s) combined")
        return compile_file

    def _compile(self, source_files: list) -> bool:
        """Execute the compiler for the target engine."""
        if self.engine == 'sugarcube':
            return self._compile_tweego(source_files)
        elif self.engine == 'ink':
            return self._compile_ink(source_files)
        elif self.engine == 'renpy':
            print(f"⚠️  Ren'py compilation not yet implemented")
            return False
        else:
            print(f"❌ Unknown engine: {self.engine}")
            return False
    
    def _compile_tweego(self, source_files: list) -> bool:
        """Call tweego.exe to compile Twee to HTML."""
        self.output_dir.mkdir(parents=True, exist_ok=True)
        output_file = self.output_dir / "story.html"
        
        try:
            cmd = ['tweego.exe', '-o', str(output_file)]
            for src in source_files:
                cmd.append(str(src))
            
            # Include story.css if it exists (for SugarCube theming)
            css_file = (self.spec_path / "story.css") if (self.spec_path / "story.css").exists() else None
            if css_file is None:
                # Check output directory
                css_file = self.output_dir / "story.css" if (self.output_dir / "story.css").exists() else None
            
            if css_file and css_file.exists():
                cmd.append(str(css_file))
                print(f"   CSS theme: {css_file.name}")
            
            # Include story.js if it exists (for SugarCube JavaScript)
            js_file = self.spec_path / "story.js" if (self.spec_path / "story.js").exists() else None
            if js_file and js_file.exists():
                cmd.append(str(js_file))
                print(f"   JavaScript: {js_file.name}")
            
            print(f"\n🔨 Running: tweego.exe ...")
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=30
            )
            
            if result.returncode == 0:
                file_size = output_file.stat().st_size
                print(f"✅ Output: {output_file}")
                print(f"   Size: {file_size} bytes")
                return True
            else:
                print(f"❌ Compilation error:")
                error_output = (result.stderr + result.stdout).strip()
                if error_output:
                    for line in error_output.split('\n')[:10]:  # Show first 10 lines
                        print(f"   {line}")
                
                # Try to auto-fix common errors
                if self._try_fix_tweego_error(error_output, source_files):
                    return False  # Signal to retry
                
                return False
        
        except FileNotFoundError:
            print(f"❌ tweego.exe not found. Install Twine or add tweego to PATH")
            return False
        except subprocess.TimeoutExpired:
            print(f"❌ Compilation timeout (30s)")
            return False
        except Exception as e:
            print(f"❌ Compilation error: {e}")
            return False
    
    def _compile_ink(self, source_files: list) -> bool:
        """Compile Ink with inklecate.exe to generate both JSON and HTML."""
        self.output_dir.mkdir(parents=True, exist_ok=True)
        output_json = self.output_dir / "story.json"
        output_html = self.output_dir / "story.html"
        
        try:
            # Use first source file for compilation (or story.ink if available)
            compile_file = source_files[0]
            
            # First pass: Validate with -p flag
            print(f"\n🔨 Running: inklecate.exe (validation) ...")
            cmd_validate = ['inklecate.exe', '-p', str(compile_file)]
            
            result = subprocess.run(
                cmd_validate,
                capture_output=True,
                text=True,
                timeout=30
            )
            
            if result.returncode != 0:
                print(f"❌ Validation error:")
                error_output = (result.stderr + result.stdout).strip()
                if error_output:
                    for line in error_output.split('\n')[:10]:  # Show first 10 lines
                        print(f"   {line}")
                
                # Try to auto-fix common errors
                if self._try_fix_ink_error(error_output, source_files):
                    return False  # Signal to retry
                
                return False
            
            print(f"✅ Ink validation passed")
            
            # Second pass: Compile to JSON with -c flag
            print(f"🔨 Running: inklecate.exe (compilation) ...")
            cmd_compile = ['inklecate.exe', '-c', str(compile_file), '-o', str(output_json)]
            
            result = subprocess.run(
                cmd_compile,
                capture_output=True,
                text=True,
                timeout=30
            )
            
            if result.returncode == 0:
                print(f"✅ Ink compilation successful")
                file_size = output_json.stat().st_size
                print(f"   JSON: {output_json} ({file_size} bytes)")
                
                # Generate HTML wrapper for the compiled Ink story
                self._generate_ink_html(output_json, output_html)
                
                return True
            else:
                print(f"❌ Compilation error:")
                error_output = (result.stderr + result.stdout).strip()
                if error_output:
                    for line in error_output.split('\n')[:10]:  # Show first 10 lines
                        print(f"   {line}")
                
                return False
        
        except FileNotFoundError:
            print(f"❌ inklecate.exe not found. Install Ink from https://github.com/inkle/ink/releases")
            return False
        except subprocess.TimeoutExpired:
            print(f"❌ Compilation timeout (30s)")
            return False
        except Exception as e:
            print(f"❌ Compilation error: {e}")
            return False
    
    def _generate_ink_html(self, json_file: Path, html_file: Path) -> None:
        """Generate HTML wrapper for Ink compiled story with theme support."""
        try:
            import json
            
            # Read compiled story JSON
            with open(json_file, 'r', encoding='utf-8') as f:
                story_data = json.load(f)
            
            # Extract metadata
            title = story_data.get('name', 'Ink Story')
            
            # Check for themed HTML wrapper template
            themed_wrapper = self._load_ink_theme_wrapper()
            
            if themed_wrapper:
                # Use themed template
                html_content = themed_wrapper.format(
                    title=title,
                    story_json=json.dumps(story_data)
                )
            else:
                # Fallback to minimal default HTML wrapper with Ink player
                html_content = self._generate_ink_html_default(title, story_data)
            
            html_file.write_text(html_content, encoding='utf-8')
            file_size = html_file.stat().st_size
            print(f"   HTML: {html_file} ({file_size} bytes)")
        
        except Exception as e:
            print(f"⚠️  Could not generate HTML wrapper: {e}")
            print(f"   JSON output is still available at {json_file}")
    
    def _load_ink_theme_wrapper(self) -> Optional[str]:
        """Load a themed HTML wrapper template for Ink stories."""
        # Check for theme.txt in output dir or spec root
        theme_file = self.output_dir / "ink-theme.html"
        if not theme_file.exists():
            theme_file = self.spec_path / "ink-theme.html"
        
        if theme_file.exists():
            try:
                return theme_file.read_text(encoding='utf-8')
            except Exception:
                return None
        
        return None
    
    def _generate_ink_html_default(self, title: str, story_data: dict) -> str:
        """Generate default minimal HTML wrapper for Ink stories (no theme)."""
        import json
        
        return f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>{title}</title>
    <style>
        * {{
            box-sizing: border-box;
        }}
        body {{
            font-family: Arial, sans-serif;
            max-width: 800px;
            margin: 0 auto;
            padding: 20px;
            line-height: 1.6;
            color: #333;
            background: #f5f5f5;
        }}
        #story {{
            background: white;
            padding: 30px;
            border-radius: 8px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }}
        .passage {{
            margin-bottom: 20px;
            min-height: 100px;
        }}
        .choices {{
            margin-top: 20px;
        }}
        .choice {{
            display: block;
            margin: 10px 0;
            padding: 10px;
            background: #f0f0f0;
            border: 1px solid #ddd;
            border-radius: 4px;
            cursor: pointer;
            transition: all 0.2s;
        }}
        .choice:hover {{
            background: #e0e0e0;
            border-color: #999;
        }}
        h1 {{
            color: #333;
            border-bottom: 2px solid #333;
            padding-bottom: 10px;
        }}
    </style>
</head>
<body>
    <div id="story">
        <h1>{title}</h1>
        <div id="content">
            <p>Loading story...</p>
        </div>
    </div>
    <script>
        // Minimal Ink player wrapper
        const storyData = {json.dumps(story_data)};
        
        console.log('Ink story compiled successfully');
        console.log('Knots:', storyData.knots ? Object.keys(storyData.knots).length : 0);
        console.log('Total characters:', JSON.stringify(storyData).length);
        
        // Display story info
        document.getElementById('content').innerHTML = `
            <p><strong>Story compiled successfully!</strong></p>
            <p>Use an Ink runtime player to execute this story.</p>
            <ul>
                <li><a href="https://github.com/inkle/ink-web" target="_blank">Ink Web Player</a></li>
                <li><a href="https://github.com/inkle/inky" target="_blank">Inky IDE</a></li>
            </ul>
            <pre style="background: #f5f5f5; padding: 10px; border-radius: 4px; overflow-x: auto;">${{JSON.stringify(storyData, null, 2).substring(0, 500)}}...</pre>
        `;
    </script>
</body>
</html>"""
    
    def _try_fix_tweego_error(self, error_msg: str, source_files: list) -> bool:
        """Attempt to fix common Twee compilation errors. Returns True if fix attempted."""
        if not error_msg:
            return False

        print(f"\n🔧 Attempting auto-fix...")

        # Common issue: unmatched braces in macros
        if 'unmatched' in error_msg.lower() and '<<' in error_msg:
            print(f"   Detected: Unmatched macro braces")
            fixed_any = False
            for src_file in source_files:
                content = src_file.read_text(encoding='utf-8')
                fixed = content
                # Fix unclosed << >> pairs: count opens vs closes
                opens = fixed.count('<<')
                closes = fixed.count('>>')
                if opens > closes:
                    print(f"   Fixing {opens - closes} unclosed macro(s) in {src_file.name}")
                    lines = fixed.split('\n')
                    for i in range(len(lines) - 1, -1, -1):
                        if opens <= closes:
                            break
                        if lines[i].count('<<') > lines[i].count('>>'):
                            lines[i] += '>>'
                            opens -= 1
                    fixed = '\n'.join(lines)
                elif closes > opens:
                    print(f"   Fixing {closes - opens} extra closing tag(s) in {src_file.name}")
                    lines = fixed.split('\n')
                    for i in range(len(lines) - 1, -1, -1):
                        if closes <= opens:
                            break
                        extra_closes = lines[i].count('>>') - lines[i].count('<<')
                        if extra_closes > 0:
                            lines[i] = lines[i].rstrip('>')
                            closes -= extra_closes
                    fixed = '\n'.join(lines)

                # Fix unmatched curly braces
                open_braces = fixed.count('{')
                close_braces = fixed.count('}')
                if open_braces > close_braces:
                    fixed += '\n' + '}' * (open_braces - close_braces)
                    print(f"   Fixed {open_braces - close_braces} unclosed brace(s) in {src_file.name}")
                elif close_braces > open_braces:
                    lines = fixed.split('\n')
                    extra = close_braces - open_braces
                    for i in range(len(lines) - 1, -1, -1):
                        if extra <= 0:
                            break
                        if lines[i].strip().startswith('}'):
                            lines[i] = ''
                            extra -= 1
                    fixed = '\n'.join(lines)
                    print(f"   Fixed {close_braces - open_braces} extra closing brace(s) in {src_file.name}")

                if fixed != content:
                    src_file.write_text(fixed, encoding='utf-8')
                    fixed_any = True
            return fixed_any

        # Common issue: invalid node references
        if 'not found' in error_msg.lower() or 'undefined' in error_msg.lower():
            print(f"   Detected: Node/variable reference error")
            refs = re.findall(r"'([^']+)'", error_msg)
            if refs:
                for ref in refs[:3]:
                    print(f"   Reference: {ref}")
            print(f"   Cannot auto-fix: Requires manual correction")
            return False

        # Common issue: passage header problems
        if 'passage' in error_msg.lower() or 'header' in error_msg.lower():
            print(f"   Detected: Passage header error")
            fixed_any = False
            for src_file in source_files:
                content = src_file.read_text(encoding='utf-8')
                fixed = content
                # Check for :: passage without space
                fixed = re.sub(r'^::(\S)', r':: \1', fixed, flags=re.MULTILINE)
                # Remove duplicate :: headers
                lines = fixed.split('\n')
                seen_headers = set()
                clean_lines = []
                for line in lines:
                    if line.startswith(':: '):
                        header_name = line.strip()
                        if header_name in seen_headers:
                            continue
                        seen_headers.add(header_name)
                    clean_lines.append(line)
                fixed = '\n'.join(clean_lines)
                if fixed != content:
                    src_file.write_text(fixed, encoding='utf-8')
                    fixed_any = True
                    print(f"   Fixed passage header in {src_file.name}")
            return fixed_any

        print(f"   No auto-fix available for this error")
        return False
    
    def _try_fix_ink_error(self, error_msg: str, source_files: list) -> bool:
        """Attempt to fix common Ink compilation errors. Returns True if fix attempted."""
        if not error_msg:
            return False
        
        print(f"\n🔧 Attempting auto-fix...")
        
        # Common issue: unmatched diverts
        if '->>' in error_msg or ('unexpected' in error_msg.lower() and '->' in error_msg):
            print(f"   Detected: Divert syntax error")
            fixed_any = False
            for src_file in source_files:
                content = src_file.read_text(encoding='utf-8')
                # Try to fix double arrows
                fixed = content.replace('->>', '->')
                if fixed != content:
                    src_file.write_text(fixed, encoding='utf-8')
                    fixed_any = True
                    print(f"   Fixed: {src_file.name}")
            return fixed_any
        
        print(f"   No auto-fix available for this error")
        return False


def main():
    """CLI entry point."""
    parser = argparse.ArgumentParser(
        description="Compile Twee/Ink files using native compilers"
    )
    parser.add_argument(
        '--spec',
        required=True,
        help='Spec name or path (e.g., "test-tier-mechanics" or "specs/test-tier-mechanics")'
    )
    parser.add_argument(
        '--engine',
        choices=['sugarcube', 'ink', 'renpy', 'generic'],
        help='Target engine (required unless --all-engines is used)'
    )
    parser.add_argument(
        '--all-engines',
        action='store_true',
        help='Compile all engines in export_engines configuration'
    )
    parser.add_argument(
        '--output',
        help='Output directory (default: specs/<spec>/output/<engine>)'
    )
    parser.add_argument(
        '--error',
        help='Error context from speckit.implement (e.g., "NODEx not found")'
    )
    parser.add_argument(
        '--export-first', action='store_true',
        help='Run speckit.export before compiling'
    )
    parser.add_argument(
        '--no-test', action='store_true',
        help='Skip runtime testing after compilation'
    )

    args = parser.parse_args()
    
    # Validate arguments
    if not args.engine and not args.all_engines:
        parser.error('Either --engine or --all-engines must be specified')
    
    if args.engine and args.all_engines:
        parser.error('Cannot specify both --engine and --all-engines')
    
    # Find spec directory - handle both "test-tier-mechanics" and "specs/test-tier-mechanics"
    spec_path = args.spec.strip()
    
    # If user included "specs/" prefix, remove it
    if spec_path.startswith('specs/') or spec_path.startswith('specs\\'):
        spec_path = spec_path[6:]  # Remove "specs/" or "specs\"
    
    spec_dir = Path('specs') / spec_path
    if not spec_dir.exists():
        print(f"❌ Spec not found: {spec_dir}")
        sys.exit(1)
    
    # If --all-engines, get the list from export_engines
    engines_to_compile = []
    if args.all_engines:
        compiler = CompileWrapper(spec_dir, 'sugarcube')  # temp instance to get allowed engines
        allowed_engines = compiler._get_allowed_engines()
        if not allowed_engines:
            print(f"❌ No export_engines configured in spec.yml or constitution.md")
            sys.exit(1)
        engines_to_compile = allowed_engines
    else:
        engines_to_compile = [args.engine]
    
    # Auto-run export if --export-first is set
    if args.export_first:
        print(f"\n📤 Running export before compile...")
        export_script = Path(__file__).parent / "export.py"
        if export_script.exists():
            for engine in engines_to_compile:
                export_cmd = [sys.executable, str(export_script), '--spec', args.spec, '--engine', engine, '--force']
                try:
                    export_result = subprocess.run(export_cmd, capture_output=True, text=True, timeout=30)
                    if export_result.returncode != 0:
                        print(f"⚠️  Export for {engine} had issues:")
                        print(export_result.stdout[-300:] if export_result.stdout else export_result.stderr[-300:])
                    else:
                        print(f"✅ Export for {engine} completed")
                except Exception as e:
                    print(f"⚠️  Export failed: {e}")
        else:
            print(f"⚠️  export.py not found at {export_script}")

    # Compile each engine
    print(f"🎮 Speckit Compiler - Multi-Engine")
    print(f"📦 Spec: {args.spec}")
    print(f"🔧 Engines: {', '.join(engines_to_compile)}")
    print()
    
    all_success = True
    for engine in engines_to_compile:
        if engine not in ['sugarcube', 'ink', 'renpy', 'generic']:
            print(f"⚠️  Skipping unsupported engine: {engine}")
            continue
        
        print(f"\n{'='*60}")
        print(f"Compiling engine: {engine}")
        print(f"{'='*60}")
        
        output_dir = Path(args.output) if args.output else None
        compiler = CompileWrapper(spec_dir, engine, output_dir)
        
        success = compiler.run(args.error if engine == engines_to_compile[0] else None)
        
        if not success:
            all_success = False
            print(f"❌ {engine} compilation failed")
        else:
            print(f"✅ {engine} compilation succeeded")
            
            # Run Playwright tests unless --no-test
            if not args.no_test:
                _run_playwright_tests(args.spec, engine)
    
    print(f"\n{'='*60}")
    if all_success:
        print(f"✅ All engines compiled successfully!")
    else:
        print(f"❌ Some engines failed to compile")
    print(f"{'='*60}")
    
    sys.exit(0 if all_success else 1)


def _run_playwright_tests(spec_name: str, engine: str):
    """Run Playwright tests on the compiled output."""
    test_dir = Path(__file__).parent.parent / "tests"
    if not test_dir.exists():
        print(f"\n⚠️  Playwright tests not found at {test_dir}")
        print(f"   Run tests manually: cd scripts/tests && npx playwright test")
        return
    
    # Check if compiled output exists
    html_file = Path('specs') / spec_name / 'output' / engine / 'story.html'
    if not html_file.exists():
        print(f"\n⚠️  Compiled HTML not found at {html_file}")
        return
    
    # Generate Playwright test specs from .twee files
    generate_script = Path(__file__).parent / "generate_tests.py"
    if generate_script.exists():
        print(f"\n🔧 Generating Playwright tests from .twee files...")
        gen_result = subprocess.run(
            [sys.executable, str(generate_script), '--spec', spec_name, '--engine', engine],
            capture_output=True, text=True, timeout=30
        )
        for line in gen_result.stdout.split('\n'):
            if line.strip():
                print(f"   {line.strip()}")
        if gen_result.returncode != 0:
            for line in gen_result.stderr.split('\n'):
                if line.strip():
                    print(f"   {line.strip()}")
            print(f"   ⚠️  Test generation reported issues (broken links)")
    else:
        print(f"\n⚠️  generate_tests.py not found at {generate_script}")
    
    print(f"\n🎭 Running Playwright tests for {engine}...")
    try:
        result = subprocess.run(
            ['npx', 'playwright', 'test', '--config', str(test_dir / 'playwright.config.ts')],
            capture_output=True,
            text=True,
            timeout=120,
            cwd=str(test_dir)
        )
        if result.returncode == 0:
            print(f"✅ Playwright tests passed")
        else:
            print(f"❌ Playwright tests failed")
            print(result.stdout[-500:] if result.stdout else result.stderr[-500:])
    except FileNotFoundError:
        print(f"⚠️  npx/playwright not found. Install: npm install @playwright/test")
    except subprocess.TimeoutExpired:
        print(f"⚠️  Playwright tests timed out (120s)")
    except Exception as e:
        print(f"⚠️  Playwright test error: {e}")


if __name__ == '__main__':
    main()
