---
description: Run comprehensive unit test suite on drafted nodes — structural tests, per-node quality gates, engine compiler validation, and self-correction loops. Now includes per-node checklist checks. Optional; speckit.compile includes basic validation automatically.
handoffs:
  - label: Re-draft failing node
    agent: speckit.implement
    prompt: Re-draft the node that failed validation
    send: true
  - label: Fix Checklist Failures
    agent: speckit.revise
    prompt: Fix the failures flagged by verification for this node
    send: true
scripts:
  py: scripts/python/verify.py --spec $SPECNAME --engine $ENGINE
---

# speckit.verify

Run comprehensive unit tests on drafted node files. Covers **structural validation, per-node quality gates (choice meaningfulness, hook declarations, dead-end detection, POV drift), engine compiler validation, and self-correction loops**. Now includes per-node checklist checks (formerly `speckit.checklist`).

**When to use**: After `speckit.compile` if you want thorough validation beyond basic checks. Not required for standard workflows.

## User Input

```text
$ARGUMENTS
```

Accepted input:
- `[NODE_ID]` — validate a single node (e.g. `NODE-003`)
- `[NODE_ID] [NODE_ID] ...` — validate a list of nodes
- `--all` — validate every file in `nodes/`
- `--unit-tests` — run the full cross-node unit test suite only (no compiler)
- `--structural-only` — run only structural unit tests (no compiler/linter)
- *(no argument)* — validate every DRAFT node that has no `verified: true` flag

## What this command does

`speckit.verify` runs three layers in sequence:

### Layer 1 — Structural Unit Tests (always runs)

| ID | Name | What it checks |
|----|------|---------------|
| T-01 | YAML-HEADER | YAML front-matter present and parseable |
| T-02 | YAML-FIELDS | Required header fields present (node_id, title, status, drafted) |
| T-03 | HOOK-SYNTAX | Every `[MECHANIC:...]` tag is properly closed |
| T-04 | CURRENCY | CURRENCY hooks have `variable=` declared |
| T-05 | RANDOM | RANDOM hooks have `min=` and `max=` |
| T-06 | DEAD-END | Non-terminal nodes have at least one outgoing choice |
| T-07 | DUPLICATE-ID | No two nodes share the same `node_id` |
| T-08 | VAR-DECLARED | All hook variables are registered in `specs/variables.md` |
| T-09 | CHOICE-TARGET | All choice link targets exist in `specs/plan.md` |

### Layer 2 — Per-Node Quality Checklist (formerly speckit.checklist)

For each node, run quality gates:

| Check | Description |
|-------|-------------|
| Choice meaningfulness | Each choice leads to measurably different outcome (different target node or variable change) |
| Hook declaration | All mechanic hooks used in prose are declared in node's YAML frontmatter or mechanics.md |
| Dead-end detection | Node has at least one outgoing choice link (unless marked as ending) |
| Variable read-before-set | No variable read in prose that hasn't been initialized on any path to this node |
| POV drift | Prose POV matches constitution.md player_perspective setting |
| Bible compliance | Referenced characters, locations, items exist in their respective spec documents |

Each check produces a PASS/FAIL/WAIVE verdict. A WAIVE means the check is not applicable (e.g., no choices in a terminal node).

Output per node:
```
CHECKLIST: NODE-010
  ✅ Choice meaningfulness: 3 choices, 3 distinct targets
  ✅ Hook declaration: 2 hooks used, both declared in frontmatter
  ✅ Dead-ends: node has 3 outgoing choices
  ✅ Variable read-before-set: $trust_marcus initialized on all paths
  ✅ POV drift: prose uses "you" (matches second-person constitution)
  ✅ Bible compliance: Marcus, Victor exist in characters.md
  
VERDICT: ✅ PASS (weighted score: 6/6)
```

### Layer 3 — Engine Compiler / Linter (skipped if `--structural-only`)

| Target | Toolchain |
|--------|-----------|
| `ink` | `inklecate -p` |
| `twine` / `sugarcube` | `tweego` |
| `renpy` | `renpy [project] lint` |
| `generic` | Structural tests only |

Toolchain warnings (binary not found) are reported but do not fail. Hard errors (syntax errors) fail and trigger self-correction.

### Self-Correction Loop

If hard errors found in any layer:

```
Attempt 1 of 3
  - Analyze error messages, identify specific lines/constructs
  - Apply minimal targeted fix to the node file
  - Re-run validate_engine.py
  → If clean: mark as verified and continue
  → If still failing: proceed to Attempt 2
```

After 3 failed attempts: output full error log, do NOT mark node as verified, prompt user with options (show failing section, retry with different strategy, skip).

### Execution Steps

1. **Resolve target list**: From $ARGUMENTS or scan `nodes/` for files without `verified: true`
2. **Load constitution**: Extract `export_target`
3. **For each target node file**:
   a. Run Layer 1 (structural tests)
   b. Run Layer 2 (quality checklist)
   c. Run Layer 3 (compiler/linter)
   d. If errors → Self-Correction Loop (max 3)
   e. If clean: add `verified: true` and `verified_at: [date]` to YAML header
4. **After all nodes**: Print summary table with status per node
5. If `--unit-tests`: Run full cross-node test suite

### Output

```
| Node     | Structural | Checklist | Compiler | Attempts | Status |
|----------|-----------|-----------|----------|----------|--------|
| NODE-001 | ✅ Pass    | ✅ 6/6    | ✅ Pass  | 1        | ✅     |
| NODE-002 | ✅ Pass    | ✅ 6/6    | ⚠️ Fixed | 2        | ✅     |
| NODE-003 | ❌ Fail    | ⚠️ 4/6    | ❌ Fail  | 3        | ❌     |
```

## Important Notes

**verify is optional**: `speckit.compile` includes basic structural validation automatically. Use this for deep audits.

**Self-correction modifies node files**: The loop applies targeted fixes to pass validation. Review changes afterward.

**Toolchain warnings don't fail**: Missing compilers are reported but structural + quality checks still run.

**Checklist verdict is weighted**: Each check contributes to a pass/fail score. Nodes with < 5/6 may still compile but need attention.
