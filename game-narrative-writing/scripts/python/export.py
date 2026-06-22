#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Export drafted nodes to engine-specific boilerplate structure.

Generates scaffolding (init, widgets, UI, styling) and integrates drafted
nodes into a ready-to-compile project. Bridges the gap between narrative
design and playable output.

Usage:
    python export.py --spec <specname> --engine <engine>
    python export.py --spec <specname> --engine sugarcube --force
    python export.py --spec <specname> --all-engines
"""

import argparse
import json
import os
import re
import shutil
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional
import yaml

from postprocess import run_postprocess


# Fix Unicode encoding for Windows console
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')


class ExportEngine:
    """Engine-specific boilerplate generator."""

    def __init__(self, spec_path: Path, engine: str, output_dir: Optional[Path] = None):
        self.spec_path = spec_path
        self.engine = engine.lower()
        self.output_dir = output_dir or spec_path / f"export/{engine}"
        self.draft_dir = spec_path / f"draft/{engine}"
        self.constitution = self._load_yaml_frontmatter("constitution.md")
        self.variables = self._load_yaml_frontmatter("variables.md") or {}
        self.variables_list = self._load_variables_list()
        self.mechanics = self._load_yaml_frontmatter("mechanics.md") or {}
        self.preset_dir = Path(__file__).parent.parent.parent
        self.template_dir = self.preset_dir / "templates"
        self.errors = []

    def _load_yaml_frontmatter(self, filename: str) -> Optional[dict]:
        path = self.spec_path / filename
        if not path.exists():
            return None
        try:
            content = path.read_text(encoding='utf-8')
            if content.startswith('---'):
                parts = content.split('---', 2)
                if len(parts) >= 2:
                    return yaml.safe_load(parts[1]) or {}
            return {}
        except Exception:
            return {}

    def _load_variables_list(self) -> list:
        path = self.spec_path / "variables.md"
        if not path.exists():
            return []
        content = path.read_text(encoding='utf-8')
        vars_list = []
        var_pattern = re.compile(r'`\$([a-zA-Z_]\w*)`\s*(?:-\s*type:\s*(\w+))?\s*(?:-\s*default:\s*(\S+))?')
        for m in var_pattern.finditer(content):
            vars_list.append({
                'name': m.group(1),
                'type': m.group(2) or 'flag',
                'default': m.group(3) or 'false',
            })
        yaml_header = self._load_yaml_frontmatter("variables.md")
        if yaml_header and 'variables' in yaml_header:
            for v in yaml_header['variables']:
                existing = [x for x in vars_list if x['name'] == v.get('name')]
                if not existing:
                    vars_list.append({
                        'name': v.get('name', ''),
                        'type': v.get('type', 'flag'),
                        'default': str(v.get('default', 'false')),
                    })
        return vars_list

    def _get_story_name(self) -> str:
        if self.constitution:
            return self.constitution.get('story_name', self.spec_path.name)
        return self.spec_path.name

    def _get_ifid(self) -> str:
        import uuid
        if self.constitution and 'ifid' in self.constitution:
            return str(self.constitution['ifid'])
        return str(uuid.uuid4()).upper()

    def _get_start_node(self) -> str:
        plan = self._load_yaml_frontmatter("plan.md")
        if plan and 'first_node' in plan:
            return plan['first_node']
        drafts = sorted(self.draft_dir.glob("NODE-*.twee")) if self.draft_dir.exists() else []
        if not drafts:
            drafts = sorted(self.draft_dir.glob("NODE-*.ink")) if self.draft_dir.exists() else []
        if drafts:
            return drafts[0].stem
        return "Start"

    def _get_engine_syntax(self, engine: str) -> str:
        """Get the engine syntax for mechanic hook translation."""
        if engine == 'sugarcube':
            return 'macro'
        elif engine == 'ink':
            return 'ink'
        return 'generic'

    def export(self) -> bool:
        """Run the full export pipeline."""
        print(f" Speckit Export")
        print(f" Spec: {self.spec_path.name}")
        print(f" Engine: {self.engine}")
        print(f" Output: {self.output_dir}")

        if not self._validate_prerequisites():
            return False

        self.output_dir.mkdir(parents=True, exist_ok=True)

        if self.engine == 'sugarcube':
            success = self._export_sugarcube()
        elif self.engine == 'ink':
            success = self._export_ink()
        else:
            print(f" Unknown engine: {self.engine}")
            return False

        if success:
            self._generate_compile_script()
            self._generate_manifest()
            self._print_summary()
            run_postprocess(
                spec_path=self.spec_path,
                engine=self.engine,
                stage="export",
                source_dir=self.output_dir,
            )
        return success

    def _validate_prerequisites(self) -> bool:
        if not self.draft_dir.exists():
            print(f" Draft directory not found: {self.draft_dir}")
            print(f" Run speckit.implement first to draft nodes.")
            return False
        if not self.constitution:
            print(f" constitution.md not found or empty at {self.spec_path}")
            return False
        return True

    def _get_drafted_nodes(self, ext: str) -> list:
        return sorted(self.draft_dir.glob(f"*{ext}"))

    def _copy_nodes(self, ext: str) -> list:
        """Copy drafted node files to export directory."""
        nodes = self._get_drafted_nodes(ext)
        copied = []
        for src in nodes:
            dst = self.output_dir / src.name
            content = src.read_text(encoding='utf-8')
            dst.write_text(content, encoding='utf-8')
            copied.append(src.name)
        return copied

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
            # Open/close on same line [MECHANIC:...][/MECHANIC]
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

    def _parse_choices(self, content: str) -> list:
        choices = []
        md_choice = re.compile(r'^\s*-\s*\[([^\]]+)\]\(([^)]+)\)')
        twee_link = re.compile(r'\[\[([^\]]+)\]\(([^)]+)\)\]')
        # Generic markdown choices
        for m in md_choice.finditer(content, re.MULTILINE):
            choices.append({
                'label': m.group(1).strip(),
                'target': m.group(2).strip(),
            })
        # Twee [[links]]
        twee_choice = re.compile(r'\[\[([^|]+?)\|([^\]]+)\]\]')
        for m in twee_choice.finditer(content):
            choices.append({
                'label': m.group(1).strip(),
                'target': m.group(2).strip(),
            })
        twee_arrow = re.compile(r'\[\[([^\]]+?)\]\]')
        for m in twee_arrow.finditer(content):
            target = m.group(1).strip()
            if not target.startswith('NODE-') and not target.startswith('END-') and not target.startswith('LOC-'):
                continue
            choices.append({
                'label': target,
                'target': target,
            })
        return choices

    def _generate_init_sugarcube(self) -> str:
        story_name = self._get_story_name()
        ifid = self._get_ifid()
        start_node = self._get_start_node()

        lines = []
        lines.append(f':: StoryData')
        lines.append('{')
        lines.append(f'  "ifid": "{ifid}",')
        lines.append(f'  "name": "{story_name}",')
        lines.append(f'  "startnode": "{start_node}",')
        lines.append(f'  "engine": "SugarCube",')
        lines.append(f'  "engineversion": "2.30.0"')
        lines.append('}')
        lines.append('')
        lines.append(':: StoryInit [header]')
        lines.append('  <<run setup()>>')
        lines.append('')

        for v in self.variables_list:
            default = v['default']
            vtype = v['type']
            if vtype == 'flag':
                val = 'true' if default in ('true', 'True', '1') else 'false'
                lines.append(f'  <<set ${v["name"]} to {val}>>')
            elif vtype == 'counter':
                lines.append(f'  <<set ${v["name"]} to {default}>>')
            elif vtype == 'string':
                lines.append(f'  <<set ${v["name"]} to "{default}" >>')
            elif vtype == 'inventory':
                lines.append(f'  <<run setupInventory()>>')
            elif vtype == 'trust':
                lines.append(f'  <<set ${v["name"]} to {default}>>')
            elif vtype == 'currency':
                lines.append(f'  <<set ${v["name"]} to {default}>>')
            else:
                lines.append(f'  <<set ${v["name"]} to {default}>>')

        return '\n'.join(lines)

    def _generate_widgets_sugarcube(self) -> str:
        lines = []
        lines.append(':: SugarCubeWidgets [widget]')

        hook_types = set()
        draft_dir = self.draft_dir
        if draft_dir.exists():
            for f in sorted(draft_dir.glob("*")):
                try:
                    content = f.read_text(encoding='utf-8')
                    for m in re.finditer(r'\[MECHANIC:(\w+)', content):
                        hook_types.add(m.group(1).upper())
                    for m in re.finditer(r'<<(\w+)>>', content):
                        if m.group(1) in ('advanceQuestStage', 'completeQuest', 'failQuest', 'questList', 'questProgress'):
                            hook_types.add('QUEST')
                except Exception:
                    pass

        if 'QUEST' in hook_types:
            lines.append('')
            lines.append('  {- QUEST MANAGEMENT -}')
            lines.append('  <<widget "questList">>')
            lines.append('    <<silently>>')
            lines.append('      <<set _quests to $activeQuests || []>>')
            lines.append('    <</silently>>')
            lines.append('    <<if _quests.length == 0>>')
            lines.append('      <p>No active quests.</p>')
            lines.append('    <<else>>')
            lines.append('      <<for _i = 0; _i < _quests.length; _i++>>')
            lines.append('        <p><<=_quests[_i].name>> — Stage <<=_quests[_i].stage>></p>')
            lines.append('      <</for>>')
            lines.append('    <</if>>')
            lines.append('  <</widget>>')
            lines.append('')
            lines.append('  <<widget "advanceQuestStage" "questId">>')
            lines.append('    <<silently>>')
            lines.append('      <<set _quests to $activeQuests || []>>')
            lines.append('      <<for _i = 0; _i < _quests.length; _i++>>')
            lines.append('        <<if _quests[_i].id == $args[0]>>')
            lines.append('          <<set _quests[_i].stage to _quests[_i].stage + 1>>')
            lines.append('        <</if>>')
            lines.append('      <</for>>')
            lines.append('    <</silently>>')
            lines.append('  <</widget>>')
            lines.append('')
            lines.append('  <<widget "completeQuest" "questId">>')
            lines.append('    <<silently>>')
            lines.append('      <<set _quests to $activeQuests || []>>')
            lines.append('      <<for _i = 0; _i < _quests.length; _i++>>')
            lines.append('        <<if _quests[_i].id == $args[0]>>')
            lines.append('          <<set _quests[_i].status to "completed">>')
            lines.append('        <</if>>')
            lines.append('      <</for>>')
            lines.append('    <</silently>>')
            lines.append('  <</widget>>')

        if 'INVENTORY' in hook_types:
            lines.append('')
            lines.append('  {- INVENTORY SYSTEM -}')
            lines.append('  <<widget "pickupItem" "itemName">>')
            lines.append('    <<silently>>')
            lines.append('      <<set _inv to $inventory || []>>')
            lines.append('      <<set _inv.push($args[0])>>')
            lines.append('      <<set $inventory to _inv>>')
            lines.append('    <</silently>>')
            lines.append('  <</widget>>')
            lines.append('')
            lines.append('  <<widget "hasItem" "itemName">>')
            lines.append('    <<silently>>')
            lines.append('      <<set _inv to $inventory || []>>')
            lines.append('      <<set _found to false>>')
            lines.append('      <<for _i = 0; _i < _inv.length; _i++>>')
            lines.append('        <<if _inv[_i] == $args[0]>>')
            lines.append('          <<set _found to true>>')
            lines.append('        <</if>>')
            lines.append('      <</for>>')
            lines.append('    <</silently>>')
            lines.append('    <<return _found>>')
            lines.append('  <</widget>>')

        if not lines:
            lines.append('  {- No mechanics used — placeholder widget section -}')

        return '\n'.join(lines)

    def _generate_ui_sugarcube(self) -> str:
        lines = []
        lines.append(':: StoryCaption')
        lines.append('  <div id="caption">')
        lines.append('    <span id="game-title"><<=$storyTitle>></span>')
        lines.append('  </div>')
        lines.append('')
        lines.append(':: StoryMenu')
        lines.append('  <<link "Continue" "StoryContinue">><</link>>')
        lines.append('')
        lines.append(':: StoryContinue')
        lines.append('  <<back "Return to story">>')
        lines.append('')
        lines.append(':: StoryStylesheet [stylesheet]')
        lines.append('  {- Default theme -}')
        lines.append('  #passages {')
        lines.append('    max-width: 40em;')
        lines.append('    margin: 0 auto;')
        lines.append('    font-family: Georgia, serif;')
        lines.append('    font-size: 18px;')
        lines.append('    line-height: 1.6;')
        lines.append('  }')
        lines.append('  .passage {')
        lines.append('    margin-bottom: 1.5em;')
        lines.append('  }')
        return '\n'.join(lines)

    def _node_to_twee(self, file_path: Path) -> str:
        """Convert a node file to Twee passage format for SugarCube export."""
        content = file_path.read_text(encoding='utf-8')
        header = self._load_yaml_frontmatter(str(file_path.name))
        content = self._translate_mechanic_hooks(content)

        node_id = file_path.stem
        if header:
            node_id = header.get('node_id', node_id)
            title = header.get('title', node_id)
        else:
            title = node_id

        # Extract body (content after YAML header)
        body = content
        if content.startswith('---'):
            parts = content.split('---', 2)
            if len(parts) >= 3:
                body = parts[2].strip()

        # Convert markdown choices to Twee links
        body = re.sub(
            r'-\s*\[([^\]]+)\]\(([^)]+)\)',
            r'[[\1|\2]]',
            body
        )

        lines = []
        lines.append(f':: {node_id} [header]')
        lines.append(f'  {{- Node ID: {node_id} -}}')
        if header:
            if 'variables_read' in header:
                lines.append(f'  {{- Variables Read: {header["variables_read"]} -}}')
            if 'variables_set' in header:
                lines.append(f'  {{- Variables Set: {header["variables_set"]} -}}')
        lines.append('')
        for line in body.split('\n'):
            lines.append(f'  {line}')

        return '\n'.join(lines)

    def _collect_twee_nodes(self) -> str:
        """Collect all drafted nodes and convert to Twee passages."""
        parts = []
        for src in sorted(self.draft_dir.glob("*.twee")):
            if src.name in ('init.twee', 'widgets.twee', 'ui.twee'):
                continue
            parts.append(self._node_to_twee(src))
        for src in sorted(self.draft_dir.glob("*.md")):
            if src.name.startswith('_'):
                continue
            parts.append(self._node_to_twee(src))
        return '\n\n'.join(parts)

    def _export_sugarcube(self) -> bool:
        """Export for SugarCube engine."""
        print(f"\n Generating SugarCube boilerplate...")

        init_content = self._generate_init_sugarcube()
        widgets_content = self._generate_widgets_sugarcube()
        ui_content = self._generate_ui_sugarcube()

        (self.output_dir / "init.twee").write_text(init_content, encoding='utf-8')
        print(f"   init.twee — StoryData + StoryInit")

        (self.output_dir / "widgets.twee").write_text(widgets_content, encoding='utf-8')
        print(f"   widgets.twee — {widgets_content.count('<<widget')} widget(s)")

        (self.output_dir / "ui.twee").write_text(ui_content, encoding='utf-8')
        print(f"   ui.twee — UI chrome")

        # Copy CSS theme if available
        theme = (self.constitution or {}).get('theme', 'light')
        css_map = {'dark': 'sugarcube-theme-dark.css', 'light': 'sugarcube-theme-light.css', 'minimal': 'sugarcube-theme-minimal.css'}
        css_file = css_map.get(theme, 'sugarcube-theme-light.css')
        css_path = self.template_dir / css_file
        if css_path.exists():
            shutil.copy2(str(css_path), str(self.output_dir / "story.css"))
            print(f"   story.css — theme: {theme}")

        # Copy and convert node files
        node_files = list(self.draft_dir.glob("*.twee"))
        if node_files:
            twee_content = self._collect_twee_nodes()
            (self.output_dir / "nodes.twee").write_text(twee_content, encoding='utf-8')
            print(f"   nodes.twee — {len(node_files)} node(s) converted")
        elif list(self.draft_dir.glob("*.md")):
            twee_content = self._collect_twee_nodes()
            (self.output_dir / "nodes.twee").write_text(twee_content, encoding='utf-8')
            print(f"   nodes.twee — nodes converted from markdown")

        return True

    def _export_ink(self) -> bool:
        """Export for Ink engine."""
        print(f"\n Generating Ink boilerplate...")

        # Generate init.ink
        var_inits = []
        for v in self.variables_list:
            default = v['default']
            if v['type'] == 'string':
                var_inits.append(f'// VAR {v["name"]} = "{default}"')
            elif v['type'] == 'flag':
                val = 'true' if default in ('true', 'True', '1') else 'false'
                var_inits.append(f'// VAR {v["name"]} = {val}')
            else:
                var_inits.append(f'// VAR {v["name"]} = {default}')

        init_content = '// Story constants and variable initialization\n'
        init_content += '\n'.join(var_inits)
        init_content += '\n\n=== setup ===\n  // Initialization logic\n'
        (self.output_dir / "init.ink").write_text(init_content, encoding='utf-8')
        print(f"   init.ink — {len(var_inits)} variable(s)")

        # Generate widgets.ink (function stubs)
        widgets_lines = ['// Reusable functions']
        for f in sorted(self.draft_dir.glob("*")):
            try:
                content = f.read_text(encoding='utf-8')
                for m in re.finditer(r'\[MECHANIC:(\w+)', content):
                    ht = m.group(1).upper()
                    if ht == 'QUEST':
                        widgets_lines.append('\n=== function quest_list ===')
                        widgets_lines.append('  // Stub: developer fills in implementation')
                        widgets_lines.append('  ~ temp result = "No active quests"')
                        widgets_lines.append('  return result')
                        break
            except Exception:
                pass
        (self.output_dir / "widgets.ink").write_text('\n'.join(widgets_lines), encoding='utf-8')
        print(f"   widgets.ink — function stubs")

        # Convert and copy node files to Ink format
        node_count = 0
        for src in sorted(self.draft_dir.glob("*")):
            if src.suffix not in ('.ink', '.md', '.twee'):
                continue
            content = src.read_text(encoding='utf-8')
            content = self._translate_mechanic_hooks(content)

            # Extract body after YAML header
            body = content
            if content.startswith('---'):
                parts = content.split('---', 2)
                if len(parts) >= 3:
                    body = parts[2].strip()

            # Convert choices to Ink syntax
            body = re.sub(
                r'-\s*\[([^\]]+)\]\(([^)]+)\)',
                r'+ [\1] -> \2',
                body
            )

            # Convert Twee links to Ink
            body = re.sub(
                r'\[\[([^|]+?)\|([^\]]+)\]\]',
                r'+ [\1] -> \2',
                body
            )

            # Convert Markdown headings to Ink knots
            body = re.sub(r'^##+\s+(.+)$', r'// \1', body, flags=re.MULTILINE)

            # Convert Markdown bold/italic to Ink emphasis
            body = re.sub(r'\*\*(.+?)\*\*', r'<b>\1</b>', body)
            body = re.sub(r'\*(.+?)\*', r'<i>\1</i>', body)

            node_id = src.stem.replace('-', '_').upper()
            header = self._load_yaml_frontmatter(src.name)
            if header and 'node_id' in header:
                node_id = header['node_id'].replace('-', '_').upper()

            ink_content = f'=== {node_id} ===\n'
            ink_content += f'// Node ID: {src.stem}\n'
            if header:
                if 'variables_read' in header:
                    ink_content += f'// Variables Read: {header["variables_read"]}\n'
                if 'variables_set' in header:
                    ink_content += f'// Variables Set: {header["variables_set"]}\n'
            ink_content += '\n'
            for line in body.split('\n'):
                ink_content += f'{line}\n'

            dst = self.output_dir / f'{src.stem}.ink'
            dst.write_text(ink_content, encoding='utf-8')
            node_count += 1

        if node_count > 0:
            print(f"   {node_count} node file(s) converted to Ink")

        return True

    def _generate_compile_script(self):
        """Generate a compile shell script for the exported project."""
        script_path = self.output_dir / "compile.sh"

        if self.engine == 'sugarcube':
            twee_files = sorted(self.output_dir.glob("*.twee"))
            if twee_files:
                file_list = ' \\\n  '.join(str(f.name) for f in twee_files)
                css_file = self.output_dir / "story.css"
                css_arg = f' \\\n  {css_file.name}' if css_file.exists() else ''
                script_content = '#!/bin/bash\n'
                script_content += f'# Compile SugarCube story\n'
                script_content += f'tweego \\\n  {file_list}{css_arg} \\\n  -o story.html\n'
                script_content += f'echo "Compiled to story.html"\n'
        elif self.engine == 'ink':
            ink_files = sorted(self.output_dir.glob("*.ink"))
            if ink_files:
                main_file = None
                for f in ink_files:
                    if f.stem == 'story' or f.stem == 'main':
                        main_file = f
                        break
                if not main_file and ink_files:
                    main_file = ink_files[0]
                if main_file:
                    script_content = '#!/bin/bash\n'
                    script_content += f'# Compile Ink story\n'
                    script_content += f'inklecate -c {main_file.name} -o story.json\n'
                    script_content += f'echo "Compiled to story.json"\n'
                else:
                    script_content = '#!/bin/bash\necho "No Ink source files found"\n'
            else:
                script_content = '#!/bin/bash\necho "No Ink source files found"\n'
        else:
            return

        script_path.write_text(script_content, encoding='utf-8')
        script_path.chmod(0o755)
        print(f"   compile.sh — compilation script")

    def _generate_manifest(self):
        """Generate export-manifest.json with metadata."""
        node_count = len(list(self.output_dir.glob("*.twee"))) if self.engine == 'sugarcube' else len(list(self.output_dir.glob("*.ink")))
        # Exclude boilerplate from count for sugar
        if self.engine == 'sugarcube':
            boilerplate = {'init.twee', 'widgets.twee', 'ui.twee', 'nodes.twee'}
            node_count = len([f for f in self.output_dir.glob("*.twee") if f.name not in boilerplate])
            if not node_count:
                node_count = len(list(self.output_dir.glob("*.twee")))

        manifest = {
            "export_timestamp": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
            "engine": self.engine,
            "spec": self.spec_path.name,
            "node_count": node_count,
            "variable_count": len(self.variables_list),
            "status": "ready_for_compilation",
            "compile_command": f"speckit compile --spec {self.spec_path.name} --engine {self.engine}",
            "next_step": "speckit.compile",
        }
        manifest_path = self.output_dir / "export-manifest.json"
        manifest_path.write_text(json.dumps(manifest, indent=2), encoding='utf-8')
        print(f"   export-manifest.json — {node_count} node(s), {len(self.variables_list)} variable(s)")

    def _get_export_engines(self) -> Optional[list]:
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
        if self.constitution and 'export_engines' in self.constitution:
            engines = self.constitution['export_engines']
            if isinstance(engines, list):
                return engines
            elif isinstance(engines, str):
                return [engines]
        return None

    def _print_summary(self):
        print(f"\n Export complete for {self.engine}")
        node_count = len(list(self.output_dir.glob("*.twee"))) if self.engine == 'sugarcube' else len(list(self.output_dir.glob("*.ink")))
        print(f" {node_count} file(s) exported to {self.output_dir}")
        print(f" Run: speckit compile --engine {self.engine}")


def main():
    parser = argparse.ArgumentParser(
        description="Export drafted nodes to engine-specific boilerplate"
    )
    parser.add_argument(
        '--spec', required=True,
        help='Spec name or path'
    )
    parser.add_argument(
        '--engine',
        choices=['sugarcube', 'ink', 'renpy', 'generic'],
        help='Target engine'
    )
    parser.add_argument(
        '--all-engines', action='store_true',
        help='Export for all configured engines'
    )
    parser.add_argument(
        '--output',
        help='Output directory (default: specs/<spec>/export/<engine>)'
    )
    parser.add_argument(
        '--force', action='store_true',
        help='Regenerate existing export (overwrite)'
    )

    args = parser.parse_args()

    if not args.engine and not args.all_engines:
        parser.error('Either --engine or --all-engines must be specified')
    if args.engine and args.all_engines:
        parser.error('Cannot specify both --engine and --all-engines')

    spec_path = args.spec.strip()
    if spec_path.startswith('specs/') or spec_path.startswith('specs\\'):
        spec_path = spec_path[6:]

    spec_dir = Path('specs') / spec_path
    if not spec_dir.exists():
        print(f" Spec not found: {spec_dir}")
        sys.exit(1)

    engines_to_export = []
    if args.all_engines:
        exporter = ExportEngine(spec_dir, 'sugarcube')
        allowed = exporter._get_export_engines()
        if not allowed:
            print(f" No export_engines configured in constitution.md or spec.yml")
            sys.exit(1)
        engines_to_export = allowed
    else:
        engines_to_export = [args.engine]

    all_success = True
    for engine in engines_to_export:
        if engine not in ['sugarcube', 'ink']:
            print(f" Skipping unsupported engine: {engine}")
            continue

        print(f"\n{'='*60}")
        print(f"Exporting for engine: {engine}")
        print(f"{'='*60}")

        output_dir = Path(args.output) if args.output else None
        exporter = ExportEngine(spec_dir, engine, output_dir)

        if not args.force and exporter.output_dir.exists():
            print(f" Export directory already exists: {exporter.output_dir}")
            print(f" Use --force to overwrite")
            all_success = False
            continue

        if exporter.output_dir.exists():
            shutil.rmtree(str(exporter.output_dir))

        success = exporter.export()
        if not success:
            all_success = False
            print(f" Export for {engine} failed")
        else:
            print(f" Export for {engine} succeeded")

    sys.exit(0 if all_success else 1)


if __name__ == '__main__':
    main()
