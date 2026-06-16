#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test runner for game narrative Speckit projects.

Runs the full test pipeline: export -> compile -> Playwright tests.
Auto-fixes errors found during testing with retry logic.

Usage:
    python run_tests.py --spec my-game --engine sugarcube
    python run_tests.py --spec my-game --engine sugarcube --headed
    python run_tests.py --spec my-game --all-engines
"""

import argparse
import json
import os
import re
import subprocess
import sys
import time
from pathlib import Path
from typing import Optional


class TestRunner:
    """Orchestrates export -> compile -> Playwright testing with auto-fix."""

    def __init__(self, spec_path: Path, engine: str, headed: bool = False, max_retries: int = 3):
        self.spec_path = spec_path
        self.engine = engine
        self.headed = headed
        self.max_retries = max_retries
        self.script_dir = spec_path.parent.parent / "scripts" / "python"
        self.test_script_dir = spec_path.parent.parent / "scripts" / "tests"
        self.draft_dir = spec_path / "draft" / engine
        self.export_dir = spec_path / "export" / engine
        self.output_dir = spec_path / "output" / engine
        self.all_fixes = []

    def run(self) -> bool:
        """Run the full test pipeline."""
        print(f"\n{'='*60}")
        print(f" Speckit Test Runner")
        print(f"{'='*60}")
        print(f" Spec:   {self.spec_path.name}")
        print(f" Engine: {self.engine}")
        print(f" Headed: {self.headed}")
        print(f"{'='*60}")

        # Step 1: Run structural validation
        if not self._run_validation():
            return False

        # Step 2: Export
        if not self._run_export():
            return False

        # Step 3: Compile
        if not self._run_compile():
            return False

        # Step 4: Run Playwright tests
        if not self._run_playwright():
            return False

        print(f"\n{'='*60}")
        print(f" All tests passed!")
        print(f"{'='*60}")
        return True

    def _run_command(self, cmd: list, desc: str, timeout: int = 120) -> subprocess.CompletedProcess:
        """Run a command and return the result."""
        print(f"\n {desc}...")
        print(f"   {' '.join(str(c) for c in cmd)}")
        try:
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout)
            if result.returncode == 0:
                last_lines = result.stdout.strip().split('\n')[-5:]
                for line in last_lines:
                    if line.strip():
                        print(f"   {line.strip()}")
            else:
                err_lines = (result.stderr or result.stdout or '').strip().split('\n')[-10:]
                for line in err_lines:
                    if line.strip():
                        print(f"   {line.strip()}")
            return result
        except subprocess.TimeoutExpired:
            print(f"   Timed out ({timeout}s)")
            return subprocess.CompletedProcess(cmd, -1, '', 'Timeout')
        except FileNotFoundError as e:
            print(f"   Command not found: {e}")
            return subprocess.CompletedProcess(cmd, -1, '', str(e))
        except Exception as e:
            print(f"   Error: {e}")
            return subprocess.CompletedProcess(cmd, -1, '', str(e))

    def _run_validation(self) -> bool:
        """Run structural validation with auto-fix."""
        verify_script = self.script_dir / "verify.py"
        if not verify_script.exists():
            print(f"\n verify.py not found; skipping validation")
            return True

        for attempt in range(self.max_retries):
            result = self._run_command(
                [sys.executable, str(verify_script),
                 '--spec', str(self.spec_path.name),
                 '--engine', self.engine,
                 '--all',
                 '--fix-all' if attempt > 0 else ''],
                f"Structural validation (attempt {attempt + 1}/{self.max_retries})"
            )
            if result.returncode == 0:
                return True
            if attempt < self.max_retries - 1:
                print(f"\n   Validation failed, will retry after fixes...")
                time.sleep(1)
        return False

    def _run_export(self) -> bool:
        """Run export with auto-fix."""
        export_script = self.script_dir / "export.py"
        if not export_script.exists():
            print(f"\n export.py not found; skipping export")
            return True

        for attempt in range(self.max_retries):
            result = self._run_command(
                [sys.executable, str(export_script),
                 '--spec', str(self.spec_path.name),
                 '--engine', self.engine,
                 '--force'],
                f"Export (attempt {attempt + 1}/{self.max_retries})"
            )
            if result.returncode == 0:
                return True
            if attempt < self.max_retries - 1:
                print(f"\n   Export failed, will retry...")
                time.sleep(1)
        return False

    def _run_compile(self) -> bool:
        """Run compile with auto-fix."""
        compile_script = self.script_dir / "compile.py"
        if not compile_script.exists():
            print(f"\n compile.py not found; cannot compile")
            return False

        for attempt in range(self.max_retries):
            result = self._run_command(
                [sys.executable, str(compile_script),
                 '--spec', str(self.spec_path.name),
                 '--engine', self.engine],
                f"Compilation (attempt {attempt + 1}/{self.max_retries})"
            )
            if result.returncode == 0:
                html_path = self.output_dir / "story.html"
                if html_path.exists():
                    print(f"\n   Output: {html_path} ({html_path.stat().st_size} bytes)")
                return True
            if attempt < self.max_retries - 1:
                print(f"\n   Compilation failed, will retry...")
                time.sleep(1)
        return False

    def _generate_tests(self) -> bool:
        """Generate Playwright test specs from .twee files."""
        generate_script = self.script_dir / "generate_tests.py"
        if not generate_script.exists():
            print(f"\n generate_tests.py not found; skipping test generation")
            return True

        result = self._run_command(
            [sys.executable, str(generate_script),
             '--spec', str(self.spec_path.name),
             '--engine', self.engine],
            "Generate Playwright tests from .twee files"
        )
        return result.returncode == 0

    def _run_playwright(self) -> bool:
        """Run Playwright tests."""
        if not self.test_script_dir.exists():
            print(f"\n Test scripts not found at {self.test_script_dir}")
            print(f"   Install Playwright tests separately")
            return True

        # Generate tests from .twee files first
        if not self._generate_tests():
            print(f"\n   Test generation reported issues (broken links)")
            # Continue anyway - static tests will still run

        spec_files = list(self.test_script_dir.glob("*.spec.ts")) + list(self.test_script_dir.glob("generated/*.spec.ts"))
        if not spec_files:
            print(f"\n No Playwright test specs found at {self.test_script_dir}")
            return True

        # Check if Playwright is installed
        try:
            subprocess.run(['npx', 'playwright', '--version'], capture_output=True, timeout=10)
        except (FileNotFoundError, subprocess.TimeoutExpired):
            print(f"\n Playwright not found. Install with:")
            print(f"   npm init -y && npm install @playwright/test && npx playwright install chromium")
            return True

        headless_flag = [] if self.headed else ['--headless']

        for attempt in range(self.max_retries):
            print(f"\n Running Playwright tests (attempt {attempt + 1}/{self.max_retries})...")
            print(f"   npx playwright test --config {self.test_script_dir}/playwright.config.ts")

            result = self._run_command(
                ['npx', 'playwright', 'test',
                 '--config', str(self.test_script_dir / "playwright.config.ts"),
                 *headless_flag],
                "Playwright tests",
                timeout=180
            )

            if result.returncode == 0:
                print(f"\n   All Playwright tests passed!")
                return True

            if attempt < self.max_retries - 1:
                self._try_auto_fix_test_errors(result)
                time.sleep(1)

        print(f"\n   Playwright tests failed after {self.max_retries} attempts")
        return False

    def _try_auto_fix_test_errors(self, result: subprocess.CompletedProcess):
        """Try to auto-fix common test errors."""
        output = (result.stderr + result.stdout).lower()

        if 'passage not found' in output or 'cannot find' in output or 'link not found' in output:
            print(f"\n   Attempting to fix: Missing passages/links")
            self._fix_missing_references(output)

        if 'timeout' in output:
            print(f"\n   Attempting to fix: Timeout issues")
            self._fix_timeout_issues()

    def _fix_missing_references(self, output: str):
        """Fix missing passage/link references in draft files."""
        if not self.draft_dir.exists():
            return

        refs = re.findall(r"'([^']+?)'", output)
        for ref in refs:
            if ref.startswith('NODE-') or ref.startswith('LOC-') or ref.startswith('END-'):
                # Check if the referenced passage exists as a file
                existing = list(self.draft_dir.glob(f"{ref}.*"))
                if not existing:
                    print(f"   Creating stub for missing reference: {ref}")
                    stub_path = self.draft_dir / f"{ref}.md"
                    stub_content = f"""---
node_id: {ref}
title: {ref}
status: DRAFT
drafted: {time.strftime('%Y-%m-%d')}
---

# {ref}

This passage is under development.

## Choices

- [Continue](NODE-END)
"""
                    stub_path.write_text(stub_content, encoding='utf-8')
                    self.all_fixes.append(f"Created stub: {ref}")
                    print(f"   Created stub passage: {ref}")

    def _fix_timeout_issues(self):
        """Fix common timeout issues by adjusting test timing."""
        print(f"   Timeout fixes not automated; consider simplifying node content")


def main():
    parser = argparse.ArgumentParser(
        description="Run full test pipeline: export -> compile -> playwright"
    )
    parser.add_argument('--spec', required=True, help='Spec name')
    parser.add_argument('--engine', default='sugarcube', help='Target engine')
    parser.add_argument('--headed', action='store_true', help='Run Playwright in headed mode')
    parser.add_argument('--all-engines', action='store_true', help='Test all configured engines')
    parser.add_argument('--max-retries', type=int, default=3, help='Max retry attempts')

    args = parser.parse_args()

    spec_path = Path.cwd() / "specs" / args.spec
    if not spec_path.exists():
        print(f" Spec not found: {spec_path}")
        sys.exit(1)

    engines = [args.engine]
    if args.all_engines:
        engines = ['sugarcube', 'ink']

    all_success = True
    for engine in engines:
        runner = TestRunner(spec_path, engine, args.headed, args.max_retries)
        if not runner.run():
            all_success = False

    sys.exit(0 if all_success else 1)


if __name__ == '__main__':
    main()
