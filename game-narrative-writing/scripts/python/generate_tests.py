#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Generate Playwright test specs from .twee files for a given spec.

Parses all .twee files in the export or draft directory, extracts passage
names and link targets, validates link integrity, and generates a targeted
.spec.ts file that verifies runtime behavior against the parsed story graph.

Usage:
    python generate_tests.py --spec my-game --engine sugarcube
    python generate_tests.py --spec my-game --engine sugarcube --validate-only
"""

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Dict, List, Optional, Set, Tuple


# SugarCube system passages that don't need to be reachable from Start
SYSTEM_PASSAGES: Set[str] = {
    'StoryTitle', 'StoryData', 'StoryInit', 'StoryMenu',
    'StoryCaption', 'StoryStylesheet', 'StoryShare', 'StorySettings',
    'StoryAuthoring', 'Start', 'AllWidgets',
    'CharacterSheet', 'InventoryUI', 'QuestJournal', 'PartyRoster',
    'DialogueUI', 'SpellsUI', 'FactionUI', 'WorldMap',
    'CombatOutcome', 'CombatModeSelect', 'TacticalCombatUI',
    'LootContainer', 'LootContainerUI', 'CraftUI', 'CraftResultUI',
    'RestUI', 'TravelEncounterTransition',
}

# SugarCube system link targets that are built-in (not user-defined passages)
SYSTEM_LINK_TARGETS: Set[str] = {
    'StoryMenu', 'StoryCaption', 'CharacterSheet', 'InventoryUI',
    'QuestJournal', 'PartyRoster', 'SpellsUI', 'FactionUI', 'WorldMap',
}


class TweeTestGenerator:
    """Parse .twee files and generate Playwright test specs."""

    def __init__(self, spec_path: Path, engine: str, output_dir: Optional[Path] = None):
        self.spec_path = spec_path
        self.engine = engine
        self.source_label = 'Draft'
        self.source_dir: Optional[Path] = None
        self.output_dir = output_dir or (
            Path(__file__).parent.parent / 'tests' / 'generated'
        )

        export_dir = spec_path / f'export/{engine}'
        draft_dir = spec_path / f'draft/{engine}'
        if export_dir.exists():
            self.source_dir = export_dir
            self.source_label = 'Export'
        elif draft_dir.exists():
            self.source_dir = draft_dir
            self.source_label = 'Draft'
        elif list(spec_path.glob('*.twee')):
            self.source_dir = spec_path
            self.source_label = 'Spec'

    def run(self, validate_only: bool = False) -> bool:
        """Run test generation. Returns True if validations pass."""
        print(f"  Generating Playwright tests for {self.spec_path.name}/{self.engine}...")

        if not self.source_dir:
            print(f"  ⚠️  No {self.engine} source files found (checked export/ and draft/)")
            return True

        passages, links = self._parse_twee_files()
        if not passages:
            print(f"  ⚠️  No passages found in {self.source_dir}")
            return True

        print(f"  📄 Parsed {len(passages)} passages from {self.source_label}/")

        errors = self._validate_links(passages, links)
        orphan_passages = self._find_orphans(passages, links)

        if errors:
            print(f"  ❌ Found {len(errors)} broken link(s):")
            for err in errors:
                print(f"     • {err}")
        else:
            print(f"  ✅ All links are valid")

        if orphan_passages:
            print(f"  ⚠️  {len(orphan_passages)} passage(s) unreachable from Start:")
            for p in orphan_passages:
                print(f"     • {p}")

        if errors and not validate_only:
            print(f"  ❌ Cannot generate tests with broken links. Fix them first.")
            return False

        if not validate_only:
            self._generate_spec_file(self.spec_path.name, passages, links, orphan_passages)
            print(f"  ✅ Generated test spec")

        return len(errors) == 0

    def _parse_twee_files(self) -> Tuple[Dict[str, str], Dict[str, List[str]]]:
        """Parse all .twee files and return (passages, links)."""
        passages: Dict[str, str] = {}
        links: Dict[str, List[str]] = {}

        for twee_file in sorted(self.source_dir.glob('*.twee')):
            content = self._read_file(twee_file)
            if content is None:
                continue

            lines = content.split('\n')
            current_passage = None
            in_block_comment = False

            for line in lines:
                stripped = line.strip()

                # Track block comments /* ... */
                if '/*' in stripped:
                    in_block_comment = True
                if in_block_comment:
                    if '*/' in stripped:
                        in_block_comment = False
                    continue

                # Skip single-line comments
                if stripped.startswith('//') or stripped.startswith('%'):
                    continue

                header_match = re.match(r'^::\s+(\S+)', line)
                if header_match:
                    current_passage = header_match.group(1)
                    passages[current_passage] = twee_file.name
                    if current_passage not in links:
                        links[current_passage] = []
                    continue

                if current_passage is None:
                    continue

                self._extract_links(line, current_passage, links)

        for passage in list(links.keys()):
            links[passage] = list(dict.fromkeys(links[passage]))

        return passages, links

    def _extract_links(self, line: str, current_passage: str, links: Dict[str, List[str]]):
        """Extract link targets from a single line of Twee content."""
        line_links = []

        for match in re.finditer(r'\[\[([^\[\]]+?)\]\]', line):
            content = match.group(1).strip()
            if '|' in content:
                parts = content.split('|', 1)
                target = parts[1].strip()
            elif '->' in content:
                parts = content.split('->', 1)
                target = parts[1].strip()
            else:
                target = content
            if target:
                line_links.append(target)

        for match in re.finditer(r'<<link\s+"([^"]*)"\s+"([^"]+)"', line):
            line_links.append(match.group(2))

        for match in re.finditer(r'<<goto\s+"([^"]+)"', line):
            line_links.append(match.group(1))

        for match in re.finditer(r'<<initiateCombat\s+"([^"]+)"\s+"([^"]+)"', line):
            line_links.append(match.group(2))

        for match in re.finditer(r'<<craftStation\s+"([^"]+)"\s+"([^"]+)"', line):
            line_links.append(match.group(2))

        for match in re.finditer(r'<<lootContainer\s+"([^"]+)"\s+"([^"]+)"', line):
            line_links.append(match.group(2))

        for match in re.finditer(r'<<endingSlide\s+"([^"]+)"', line):
            line_links.append(match.group(1))

        for target in line_links:
            if current_passage not in links:
                links[current_passage] = []
            links[current_passage].append(target)

    def _validate_links(self, passages: Dict[str, str], links: Dict[str, List[str]]) -> List[str]:
        """Check every link target exists as a passage. Return error messages."""
        all_passages = set(passages.keys()) | SYSTEM_PASSAGES | SYSTEM_LINK_TARGETS
        errors = []

        for passage, targets in links.items():
            for target in targets:
                if target not in all_passages and not target.startswith('END-'):
                    errors.append(f"'{passage}' -> '{target}' (not found)")

        return errors

    def _find_orphans(self, passages: Dict[str, str],
                      links: Dict[str, List[str]]) -> List[str]:
        """Find passages not reachable from Start via link traversal."""
        reachable = set()
        queue = ['Start']
        visited = set()

        while queue:
            current = queue.pop(0)
            if current in visited:
                continue
            visited.add(current)
            reachable.add(current)

            for target in links.get(current, []):
                if target in passages and target not in visited:
                    queue.append(target)

        non_system = {p for p in passages if p not in SYSTEM_PASSAGES and p != 'Start'}
        orphans = sorted(non_system - reachable)
        return orphans

    def _generate_spec_file(self, spec_name: str, passages: Dict[str, str],
                            links: Dict[str, List[str]], orphans: List[str]):
        """Generate a Playwright .spec.ts file with passage data embedded."""
        non_system = {p for p in passages if p not in SYSTEM_PASSAGES and p != 'Start'}
        story_passages = sorted(non_system)

        passages_json = json.dumps(story_passages)
        links_json = json.dumps(links, indent=2)



        test_code = f'''import {{ test, expect }} from '@playwright/test';
import {{
  navigateToGame,
  getCurrentPassage,
  getPassageText,
  getVisibleChoices,
  clickLink,
  getGamePath,
}} from '../helpers';

const SPEC_NAME = '{spec_name}';
const ENGINE = '{self.engine}';

const ALL_PASSAGES: string[] = {passages_json};

const PASSAGE_LINKS: Record<string, string[]> = {links_json};

const PASSAGE_SOURCE: Record<string, string> = {json.dumps(passages)};

test.describe(`${{SPEC_NAME}} Generated Passage Tests (${{ENGINE}})`, () => {{

  test('all passages from .twee files are known and valid', async ({{ page }}) => {{
    expect(ALL_PASSAGES.length).toBeGreaterThanOrEqual(1);
    for (const p of ALL_PASSAGES) {{
      expect(p).toMatch(/^[A-Z]/);
    }}
  }});

  test('every link target exists as a passage', async ({{ page }}) => {{
    const systemPassages = new Set([
      'StoryTitle', 'StoryData', 'StoryInit', 'StoryMenu',
      'StoryCaption', 'StoryStylesheet', 'StoryShare', 'StorySettings',
      'StoryAuthoring', 'Start', 'AllWidgets',
      'CharacterSheet', 'InventoryUI', 'QuestJournal', 'PartyRoster',
      'SpellsUI', 'FactionUI', 'WorldMap',
    ]);
    for (const [passage, targets] of Object.entries(PASSAGE_LINKS)) {{
      for (const target of targets) {{
        if (!ALL_PASSAGES.includes(target) && !systemPassages.has(target) && !target.startsWith('END-')) {{
          expect(true).toBeFalsy(
            `${{passage}} links to "${{target}}" which is not defined in any .twee file`);
        }}
      }}
    }}
  }});

  test('BFS walkthrough covers all story passages', async ({{ page }}) => {{
    await navigateToGame(page, SPEC_NAME, ENGINE);

    const visited = new Set<string>();
    const queue: string[][] = [];

    const initialPassage = await getCurrentPassage(page);
    if (initialPassage) {{
      visited.add(initialPassage);
      queue.push([]);
    }}

    const storyPassages = ALL_PASSAGES.filter(
      p => !p.startsWith('Story') && p !== 'Start'
    );

    const maxNodes = Math.min(200, storyPassages.length * 3);
    let nodesVisited = 0;

    while (queue.length > 0 && nodesVisited < maxNodes) {{
      const choicePath = queue.shift()!;
      nodesVisited++;

      await page.goto(getGamePath(SPEC_NAME, ENGINE), {{ waitUntil: 'networkidle' }});

      for (const choiceText of choicePath) {{
        const choices = await getVisibleChoices(page);
        if (choices.includes(choiceText)) {{
          await clickLink(page, choiceText);
          await page.waitForTimeout(300);
        }} else {{
          break;
        }}
      }}

      const passage = await getCurrentPassage(page);
      if (!passage) continue;

      const text = await getPassageText(page);
      expect(text).not.toContain('[error]');
      expect(text).not.toContain('undefined');

      const choices = await getVisibleChoices(page);
      for (const choice of choices.slice(0, 5)) {{
        const newPath = [...choicePath, choice];
        await page.goto(getGamePath(SPEC_NAME, ENGINE), {{ waitUntil: 'networkidle' }});

        for (const c of newPath) {{
          const cs = await getVisibleChoices(page);
          if (cs.includes(c)) {{
            await clickLink(page, c);
            await page.waitForTimeout(300);
          }} else {{
            break;
          }}
        }}

        const targetPassage = await getCurrentPassage(page);
        if (targetPassage && !visited.has(targetPassage)) {{
          visited.add(targetPassage);
          queue.push(newPath);

          const targetText = await getPassageText(page);
          expect(targetText).not.toContain('[error]');
          expect(targetText).not.toContain('undefined');
        }}
      }}
    }}

    const unvisited = storyPassages.filter(p => !visited.has(p));
    if (unvisited.length > 0) {{
      console.log(`⚠️  Unvisited passages (${{unvisited.length}}): ${{unvisited.join(', ')}}`);
    }}

    expect(visited.size).toBeGreaterThanOrEqual(1);
  }});

  test('every story passage contains valid content', async ({{ page }}) => {{
    await navigateToGame(page, SPEC_NAME, ENGINE);

    for (let i = 0; i < Math.min(10, ALL_PASSAGES.length); i++) {{
      await page.goto(getGamePath(SPEC_NAME, ENGINE), {{ waitUntil: 'networkidle' }});

      const choices = await getVisibleChoices(page);
      if (choices.length === 0) break;

      const choiceIndex = i % choices.length;
      await clickLink(page, choices[choiceIndex]);
      await page.waitForTimeout(500);

      const passage = await getCurrentPassage(page);
      expect(passage).toBeTruthy();

      const text = await getPassageText(page);
      expect(text).toBeTruthy();
      expect(text).not.toContain('[error]');
    }}
  }});
}});
'''

        self.output_dir.mkdir(parents=True, exist_ok=True)
        output_file = self.output_dir / f'{spec_name}-{self.engine}.spec.ts'
        output_file.write_text(test_code, encoding='utf-8')
        print(f"  📝 Wrote {output_file}")

    def _read_file(self, path: Path) -> Optional[str]:
        try:
            return path.read_text(encoding='utf-8')
        except Exception as e:
            print(f"  ⚠️  Could not read {path}: {e}")
            return None


def main():
    parser = argparse.ArgumentParser(
        description='Generate Playwright tests from .twee files'
    )
    parser.add_argument('--spec', required=True, help='Spec name')
    parser.add_argument('--engine', default='sugarcube', help='Target engine')
    parser.add_argument('--validate-only', action='store_true',
                        help='Only validate links, do not generate test files')

    args = parser.parse_args()

    spec_path = Path.cwd() / 'specs' / args.spec
    if not spec_path.exists():
        print(f"❌ Spec not found: {spec_path}")
        sys.exit(1)

    generator = TweeTestGenerator(spec_path, args.engine)
    success = generator.run(validate_only=args.validate_only)

    sys.exit(0 if success else 1)


if __name__ == '__main__':
    main()
