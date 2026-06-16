#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Verify and validate drafted node files.

Runs comprehensive unit tests on nodes (structural tests + engine compiler
validation + per-node quality checklist). Includes self-correction loop
for fixing errors.

Usage:
    python verify.py [NODE_ID] [NODE_ID] ... [options]
    python verify.py --all [options]
    python verify.py --unit-tests [options]
    python verify.py --spec my-game --all --fix-all

Options:
    --all               Validate all nodes in draft/
    --unit-tests        Run cross-node unit test suite only
    --structural-only   Skip engine compiler validation
    --fix-all           Auto-fix all fixable errors
    --max-attempts N    Set max self-correction attempts (default: 3)
    --engine ENGINE     Target engine (default: sugarcube)
    --spec SPEC         Spec name (required)
"""

import argparse
import json
import os
import re
import sys
import subprocess
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Tuple, Optional
import yaml


class NodeVerifier:
    """Orchestrates node validation with self-correction."""
    
    def __init__(self, spec_path: Path, engine: str, max_attempts: int = 3, fix_all: bool = False):
        self.spec_path = spec_path
        self.engine = engine
        self.max_attempts = max_attempts
        self.fix_all = fix_all
        self.script_dir = spec_path.parent.parent / "scripts" / "python" / "validation"
        self.draft_dir = spec_path / "draft" / engine
        self.export_dir = spec_path / "export" / engine
        self.results: Dict[str, Dict] = {}
        self.errors: List[str] = []
        self.fixes_applied: List[str] = []

    def find_nodes(self, pattern: Optional[List[str]] = None) -> List[Path]:
        """Find node files matching pattern."""
        if not self.draft_dir.exists():
            return []
        node_files = []
        for ext in ['*.md', '*.twee', '*.ink', '*.rpy']:
            node_files.extend(self.draft_dir.glob(f"NODE-{ext[1:]}"))
        if not node_files:
            for ext in ['*.md', '*.twee', '*.ink', '*.rpy']:
                node_files.extend(sorted(self.draft_dir.glob(ext)))
        if pattern:
            filtered = []
            for node_file in node_files:
                node_id = node_file.stem
                if node_id in pattern or node_id.upper() in pattern:
                    filtered.append(node_file)
            return filtered
        return [f for f in node_files if f.name != 'story.twee' and not f.name.startswith('_')]

    def run_structural_tests(self, node_files: List[Path]) -> Tuple[bool, List[str]]:
        """Run test_nodes.py structural validation."""
        test_script = self.script_dir / "test_nodes.py"
        if not test_script.exists():
            return self._run_builtin_tests(node_files)

        print(f"\n  Running structural tests ({len(node_files)} nodes)...")
        try:
            result = subprocess.run(
                [sys.executable, str(test_script),
                 "--nodes-dir", str(self.draft_dir),
                 "--specs-dir", str(self.spec_path),
                 "--json"],
                capture_output=True,
                text=True,
                timeout=30
            )
            if result.returncode == 0:
                return True, []
            try:
                output = json.loads(result.stdout) if result.stdout else {}
                if isinstance(output, dict) and 'failures' in output:
                    errors = [f"{f['file']}: {f['detail']}" for f in output['failures']]
                    return False, errors
            except:
                pass
            return False, [result.stdout[:300] if result.stdout else "Test failed"]
        except subprocess.TimeoutExpired:
            return False, ["Structural tests timed out"]
        except Exception as e:
            return False, [f"Error running tests: {e}"]

    def _run_builtin_tests(self, node_files: List[Path]) -> Tuple[bool, List[str]]:
        """Run built-in structural tests when test_nodes.py not found."""
        errors = []
        for nf in node_files:
            content = nf.read_text(encoding='utf-8')
            header = self._extract_yaml_header(content)
            fname = nf.name

            # T-01: YAML header
            if header is None:
                errors.append(f"{fname}: Missing or malformed YAML front-matter")
                continue

            # T-02: Required fields
            for field in ('node_id', 'title', 'status'):
                if field not in header:
                    errors.append(f"{fname}: Missing required field: {field}")

            # T-03: Hook syntax
            open_hooks = re.findall(r'\[MECHANIC:', content)
            close_hooks = re.findall(r'\[MECHANIC:[^\]]+\]', content)
            if len(open_hooks) != len(close_hooks):
                errors.append(f"{fname}: {len(open_hooks)} opening vs {len(close_hooks)} closing MECHANIC hooks")

            # T-06: Dead-end check
            if str(header.get('status', '')).upper() != 'TERMINAL':
                has_choices = bool(
                    re.search(r'^- \[', content, re.MULTILINE) or
                    re.search(r'\[\[', content) or
                    re.search(r'^\* \[', content, re.MULTILINE)
                )
                if not has_choices:
                    errors.append(f"{fname}: Dead-end node (no choices, not TERMINAL)")

        return len(errors) == 0, errors

    def _extract_yaml_header(self, content: str) -> Optional[dict]:
        if not content.startswith('---'):
            return None
        end = content.find('\n---', 3)
        if end == -1:
            return None
        try:
            return yaml.safe_load(content[3:end])
        except yaml.YAMLError:
            return None

    def run_quality_checklist(self, node_file: Path) -> Tuple[bool, List[str]]:
        """Run per-node quality checklist checks."""
        content = node_file.read_text(encoding='utf-8')
        header = self._extract_yaml_header(content)
        if header is None:
            return False, ["Cannot run checklist: no YAML header"]

        issues = []
        fname = node_file.name

        # Choice meaningfulness
        choices = re.findall(r'-\s*\[([^\]]+)\]\(([^)]+)\)', content)
        if not choices:
            # Try Twee format
            choices = re.findall(r'\[\[([^|]+?)\|([^\]]+)\]\]', content)
        targets = set(c[1] for c in choices)
        if len(choices) >= 2 and len(targets) < 2:
            issues.append(f"Choice meaningfulness: {len(choices)} choices but only {len(targets)} distinct target(s)")

        variables_read = header.get('variables_read', [])
        variables_set = header.get('variables_set', [])

        # Hook declaration
        used_hooks = re.findall(r'\[MECHANIC:(\w+)', content)
        if used_hooks:
            hook_types = set(h.upper() for h in used_hooks)
            issues.append(f"Hook declaration: {len(hook_types)} hook type(s) used: {', '.join(sorted(hook_types))}")
        else:
            issues.append("Hook declaration: No MECHANIC hooks found in prose")

        # Variable read-before-set check (basic)
        for var in variables_read:
            if var in variables_set:
                issues.append(f"Variable read-before-set: {var} appears in both read and set lists")

        # Bible compliance (basic - just check referenced files exist)
        for var in variables_read:
            if isinstance(var, str) and not var.startswith('$'):
                var_path = self.spec_path / f"{var.lower().replace('_', '-')}.md"
                if not var_path.exists():
                    issues.append(f"Variable '{var}' referenced but no matching spec doc found")

        return len(issues) == 0, issues

    def run_engine_validation(self, node_files: List[Path]) -> Tuple[bool, List[str]]:
        """Run validate_engine.py for each node."""
        validate_script = self.script_dir / "validate_engine.py"
        if not validate_script.exists():
            return True, []
        all_errors = []
        for nf in node_files:
            try:
                result = subprocess.run(
                    [sys.executable, str(validate_script),
                     str(nf), "--target", self.engine],
                    capture_output=True, text=True, timeout=15
                )
                if result.returncode != 0:
                    try:
                        output = json.loads(result.stdout) if result.stdout else {}
                        if isinstance(output, dict) and 'errors' in output:
                            for err in output['errors']:
                                all_errors.append(f"{nf.name}: {err}")
                    except:
                        all_errors.append(f"{nf.name}: {result.stdout[:200]}")
            except subprocess.TimeoutExpired:
                all_errors.append(f"{nf.name}: Validation timed out")
            except Exception as e:
                all_errors.append(f"{nf.name}: {e}")
        return len(all_errors) == 0, all_errors

    def _fix_node_file(self, node_file: Path, errors: List[str]) -> bool:
        """Apply auto-fixes to a node file based on errors."""
        if not self.fix_all:
            return False
        content = node_file.read_text(encoding='utf-8')
        fixed = content
        any_fix = False

        for err in errors:
            # Fix missing YAML end marker
            if 'malformed YAML' in err.lower() or 'Missing' in err.lower() and 'front-matter' in err.lower():
                if fixed.startswith('---') and '\n---' not in fixed[3:]:
                    end_idx = fixed.find('\n---', 3)
                    if end_idx == -1:
                        lines = fixed.split('\n')
                        insert_at = 1
                        for i in range(1, min(10, len(lines))):
                            if lines[i].strip() == '':
                                insert_at = i + 1
                                break
                        lines.insert(insert_at, '---')
                        fixed = '\n'.join(lines)
                        any_fix = True
                        self.fixes_applied.append(f"{node_file.name}: Added missing YAML closing")

            # Fix missing required fields
            m = re.search(r"Missing required field: (\w+)", err)
            if m:
                field = m.group(1)
                if field == 'node_id':
                    stem = node_file.stem
                    fixed = re.sub(r'^(---\s*\n)', r'\1node_id: "' + stem + '"\n', fixed, re.MULTILINE)
                    any_fix = True
                    self.fixes_applied.append(f"{node_file.name}: Added missing node_id: {stem}")
                elif field == 'title':
                    stem = node_file.stem
                    fixed = re.sub(r'^(---\s*\n)', r'\1title: "' + stem + '"\n', fixed, re.MULTILINE)
                    any_fix = True
                    self.fixes_applied.append(f"{node_file.name}: Added missing title: {stem}")
                elif field == 'status':
                    fixed = re.sub(r'^(---\s*\n)', r'\1status: DRAFT\n', fixed, re.MULTILINE)
                    any_fix = True
                    self.fixes_applied.append(f"{node_file.name}: Added missing status: DRAFT")
                elif field == 'drafted':
                    today = datetime.now().strftime("%Y-%m-%d")
                    fixed = re.sub(r'^(---\s*\n)', fr'\1drafted: {today}\n', fixed, re.MULTILINE)
                    any_fix = True
                    self.fixes_applied.append(f"{node_file.name}: Added missing drafted date")

            # Fix unclosed hooks
            if 'opening vs' in err.lower() and 'closing' in err.lower():
                open_count = fixed.count('[MECHANIC:')
                close_count = len(re.findall(r'\[MECHANIC:[^\]]+\]', fixed))
                if open_count > close_count:
                    missing = open_count - close_count
                    lines = fixed.split('\n')
                    for i in range(len(lines) - 1, -1, -1):
                        if missing <= 0:
                            break
                        if '[MECHANIC:' in lines[i] and ']' not in lines[i].split('[MECHANIC:')[-1]:
                            lines[i] = lines[i].strip() + ']'
                            missing -= 1
                    fixed = '\n'.join(lines)
                    any_fix = True
                    self.fixes_applied.append(f"{node_file.name}: Fixed unclosed MECHANIC hooks")

        if any_fix:
            node_file.write_text(fixed, encoding='utf-8')
        return any_fix

    def verify_nodes(self, node_files: List[Path], structural_only: bool = False) -> bool:
        """Verify individual nodes with self-correction loop."""
        if not node_files:
            print("  No nodes to verify")
            return False

        print(f"\n Verifying {len(node_files)} node(s)...")
        all_passed = True

        for node_file in node_files:
            node_id = node_file.stem
            attempts = 0
            passed = False

            while attempts < self.max_attempts and not passed:
                attempts += 1
                print(f"\n  {node_id} (Attempt {attempts}/{self.max_attempts})", end="")

                struct_passed, struct_errors = self.run_structural_tests([node_file])
                quality_passed, quality_issues = self.run_quality_checklist(node_file)

                if not struct_passed:
                    print(" [structural ] ", end="")
                    if self.fix_all and attempts < self.max_attempts:
                        self._fix_node_file(node_file, struct_errors + quality_issues)
                        print("fixing...", end="")
                    else:
                        for e in struct_errors[:3]:
                            print(f"\n     • {e}")
                    all_passed = False
                    continue

                if quality_issues:
                    print(f" [quality: {len(quality_issues)} issues] ", end="")
                    for qi in quality_issues[:2]:
                        print(f"\n     • {qi}")
                    if self.fix_all and attempts < self.max_attempts:
                        self._fix_node_file(node_file, quality_issues)
                    all_passed = False
                    continue

                if not structural_only:
                    eng_passed, eng_errors = self.run_engine_validation([node_file])
                    if not eng_passed:
                        print(f" [engine: {len(eng_errors)} errors] ", end="")
                        for e in eng_errors[:2]:
                            print(f"\n     • {e}")
                        all_passed = False
                        continue

                print("  \u2705")
                passed = True
                self._mark_verified(node_file)

            if not passed:
                print(f"    \u274c Failed after {self.max_attempts} attempts")
                self.results[node_id] = {'status': 'failed', 'attempts': attempts}
            else:
                self.results[node_id] = {'status': 'passed', 'attempts': attempts}

        return all_passed

    def _mark_verified(self, node_file: Path):
        """Add verified flag to node YAML header."""
        try:
            content = node_file.read_text(encoding='utf-8')
            if content.startswith('---'):
                parts = content.split('---', 2)
                header = yaml.safe_load(parts[1])
                header['verified'] = True
                header['verified_at'] = datetime.now().strftime("%Y-%m-%d")
                new_header = yaml.dump(header, default_flow_style=False, sort_keys=False)
                new_content = f"---\n{new_header}---{parts[2]}"
                node_file.write_text(new_content, encoding='utf-8')
        except Exception as e:
            print(f"    \u26a0 Could not update header: {e}")

    def run_unit_test_suite(self) -> bool:
        """Run full cross-node unit test suite."""
        print(f"\n Running cross-node unit test suite...")
        test_script = self.script_dir / "test_nodes.py"
        if test_script.exists():
            try:
                result = subprocess.run(
                    [sys.executable, str(test_script),
                     "--nodes-dir", str(self.draft_dir),
                     "--specs-dir", str(self.spec_path)],
                    capture_output=True, text=True, timeout=60
                )
                if result.returncode == 0:
                    print("  \u2705 Full unit test suite passed")
                    return True
                print(f"  \u274c Full unit test suite failed")
                print(result.stdout[:400] if result.stdout else result.stderr[:400])
                return False
            except Exception as e:
                print(f"  \u274c Error running unit test suite: {e}")
                return False
        else:
            print("  \u26a0 test_nodes.py not found; skipping full unit tests")
            return True


def main():
    parser = argparse.ArgumentParser(
        description="Verify drafted node files with comprehensive unit tests"
    )
    parser.add_argument('nodes', nargs='*', help='Node IDs to verify')
    parser.add_argument('--all', action='store_true', help='Verify all nodes')
    parser.add_argument('--unit-tests', action='store_true', help='Run full cross-node unit tests')
    parser.add_argument('--structural-only', action='store_true', help='Skip engine compiler validation')
    parser.add_argument('--fix-all', action='store_true', help='Auto-fix all fixable errors')
    parser.add_argument('--engine', default='sugarcube', help='Target engine')
    parser.add_argument('--spec', required=True, help='Spec name')
    parser.add_argument('--max-attempts', type=int, default=3, help='Max self-correction attempts')

    args = parser.parse_args()

    spec_path = Path.cwd() / "specs" / args.spec
    if not spec_path.exists():
        print(f" Spec directory not found: {spec_path}")
        sys.exit(1)

    print(f" Speckit Verifier")
    print(f" Spec: {args.spec}")
    print(f" Engine: {args.engine}")
    if args.fix_all:
        print(f" Auto-fix: enabled")

    verifier = NodeVerifier(spec_path, args.engine, args.max_attempts, args.fix_all)

    if args.all:
        node_files = verifier.find_nodes()
    elif args.nodes:
        node_files = verifier.find_nodes(args.nodes)
    else:
        node_files = verifier.find_nodes()

    if not node_files:
        print(f" No nodes found to verify")
        sys.exit(0)

    success = True
    if args.unit_tests:
        success = verifier.run_unit_test_suite()
    else:
        success = verifier.verify_nodes(node_files, structural_only=args.structural_only)
        if success and not args.structural_only:
            success = verifier.run_unit_test_suite()

    print(f"\n{'='*50}")
    if verifier.fixes_applied:
        print(f" Fixes applied:")
        for fix in verifier.fixes_applied:
            print(f"   {fix}")

    print(f"\n Summary:")
    for nid, result in verifier.results.items():
        icon = "\u2705" if result['status'] == 'passed' else "\u274c"
        print(f"   {icon} {nid} ({result['attempts']} attempt(s))")

    if success:
        print(f" \u2705 All verification passed")
        sys.exit(0)
    else:
        print(f" \u274c Verification failed")
        sys.exit(1)


if __name__ == '__main__':
    main()
