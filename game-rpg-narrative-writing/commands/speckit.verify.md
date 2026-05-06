---
description: Run comprehensive unit test suite on drafted nodes. Includes structural tests, engine compiler validation, and self-correction loops. Optional; speckit.compile includes basic validation automatically.
handoffs:
  - label: Re-draft failing node
    agent: speckit.implement
    prompt: Re-draft the node that failed validation
    send: true
  - label: View implementation instructions
    agent: speckit.implement
    prompt: Show implement instructions
    send: false
scripts:
  py: scripts/python/verify.py --spec $SPECNAME --engine $ENGINE
---

# speckit.verify

Run comprehensive unit tests on drafted node files. 

**When to use**: After `speckit.compile` if you want thorough validation. Not required for standard workflows.

## User Input

```text
$ARGUMENTS
```

Accepted arguments:
- `[NODE_ID]` — validate a single node (e.g. `NODE-003`)
- `[NODE_ID] [NODE_ID] ...` — validate a list of nodes
- `--all` — validate every file in `nodes/`
- `--unit-tests` — run the full cross-node unit test suite only (no compiler)
- `--structural-only` — run only structural unit tests (no compiler/linter invocation)
- `--mode rpg` — include RPG-specific validation checks
- *(no argument)* — validate every DRAFT node that has no `verified: true` flag in its header

## What this command does

`speckit.verify` runs two layers of validation in sequence:

### Layer 1 — Structural Unit Tests (always runs)

Executes `scripts/python/validation/test_nodes.py` against the target node(s).

Tests included:
| ID | Name | What it checks |
|---|---|---|
| T-01 | YAML-HEADER | YAML front-matter present and parseable |
| T-02 | YAML-FIELDS | All required header fields present (node_id, title, status, drafted) |
| T-03 | HOOK-SYNTAX | Every `[MECHANIC:...]` tag is properly closed |
| T-04 | CURRENCY | CURRENCY hooks have `variable=` declared |
| T-05 | RANDOM | RANDOM hooks have `min=` and `max=` |
| T-06 | DEAD-END | Non-terminal nodes have at least one outgoing choice |
| T-07 | DUPLICATE-ID | No two nodes share the same `node_id` |
| T-08 | VAR-DECLARED | All hook variables are registered in `specs/variables.md` |
| T-09 | CHOICE-TARGET | All choice link targets exist in `specs/plan.md` |

### Layer 2 — Engine Compiler / Linter (skipped if `--structural-only`)

Executes `scripts/python/validation/validate_engine.py [FILE] --target [EXPORT_TARGET]` where
`EXPORT_TARGET` is read from `.specify/memory/constitution.md`.

| Target | Toolchain | Install |
|---|---|---|
| `ink` | `inklecate -p` | https://github.com/inkle/ink/releases |
| `twine` / `sugarcube` | `tweego` | https://www.motoslave.net/tweego/ |
| `renpy` | `renpy [project] lint` | Ren'Py SDK on PATH |
| `unity` (`.yarn`) | `ysc compile` | https://github.com/YarnSpinnerTool/YarnSpinner-Console |
| `unity` (`.cs`) | `dotnet build` | .NET SDK |
| `escoria` | `godot --check-only` | Godot on PATH |
| `ags` | *(static analysis only)* | No CLI compiler available |
| `generic` | *(structural tests only)* | — |

Toolchain `[TOOLCHAIN]` warnings (binary not found) are reported but **do not fail** the build.
Hard errors (syntax errors returned by the compiler) **do fail** the build and trigger the loop.

## Self-Correction Loop

If any hard errors are found in Layer 1 or Layer 2:

```
Attempt 1 of 3
  - Analyze the error messages
  - Identify the specific lines / constructs causing the failure
  - Apply the minimal targeted fix to the node file
  - Re-run validate_engine.py
  → If clean: mark as verified and continue
  → If still failing: proceed to Attempt 2
```

The loop runs up to **3 attempts**. After 3 failed attempts:
- Output the full error log
- Do **NOT** mark the node as verified
- Prompt the user:
  ```
  ⚠ VERIFY FAILED after 3 attempts: nodes/[NODE_ID].[EXT]
  
  Remaining errors:
  [error list]
  
  Options:
    1. Show me the failing section so I can fix it manually.
    2. Retry with a different drafting strategy (delegates to speckit.implement --force).
    3. Skip this node for now and continue with others.
  ```

## Execution Steps

1. **Resolve target list**: From `$ARGUMENTS` or scan `nodes/` for files without `verified: true`.

2. **Load constitution**: Read `.specify/memory/constitution.md` → extract `export_target`.

3. **For each target node file**:

   a. Run Layer 1 (structural tests):
      ```
      python scripts/python/validation/test_nodes.py --nodes-dir nodes --specs-dir specs --json
      ```
      Filter results to the current node only.

   b. Run Layer 2 (compiler):
      ```
      python scripts/python/validation/validate_engine.py nodes/[NODE_ID].[EXT] --target [EXPORT_TARGET]
      ```

   c. If errors found → enter **Self-Correction Loop** (max 3 attempts).

   d. If clean after loop:
      - Add `verified: true` and `verified_at: [YYYY-MM-DD]` to the node's YAML header.
      - Report: `✓ VERIFIED: [NODE_ID] — [n] attempt(s)`

4. **After all nodes processed**, print summary table:
   ```
   | Node     | Status   | Attempts | Errors |
   |----------|----------|----------|--------|
   | NODE-001 | ✓ Clean  | 1        | 0      |
   | NODE-002 | ✓ Fixed  | 2        | 0      |
   | NODE-003 | ✗ Failed | 3        | 4      |
   ```

5. If `--unit-tests` flag was passed (or after all individual nodes are verified), run the full
   cross-node test suite:
   ```
   python scripts/python/validation/test_nodes.py --nodes-dir nodes --specs-dir specs
   ```
   Report failures and suggest corrections.

## Toolchain Setup (first-time)

If any `[TOOLCHAIN]` warning is emitted, print the following once per missing tool:

```
ℹ  TOOLCHAIN MISSING: [tool]
   Install: [install URL]
   Without it, only static/structural checks will run.
   Add [tool] to PATH and re-run speckit.verify to enable full compilation checks.
```

---

## RPG-Specific Validation Tests (--mode rpg)

**When activated**: If `--mode rpg` or `constitution.md` declares `game_system: "d5e"` (or other RPG system), run these additional unit tests:

### RPG Test Suite

| ID | Name | What it checks |
|---|---|---|
| RPG-01 | SKILL-CHECK-DC | All skill check DCs fall within system range (5-20 for D&D, 0-4 for PBTA) |
| RPG-02 | APPROVAL-RANGE | All companion approval changes fall within -100 to +100 |
| RPG-03 | REP-RANGE | All faction reputation changes fall within -100 to +100 |
| RPG-04 | APPROVAL-GATE-VALID | If approval gate used, companion has been recruited before this node |
| RPG-05 | ENDING-GATE-REACHABLE | Ending gates in this node don't make endings impossible |
| RPG-06 | REP-CUMULATIVE | Sum of reputation changes across session doesn't exceed realistic 15-session arc |
| RPG-07 | SKILL-CHECK-OUTCOME | Each skill check has explicit success and failure narration |
| RPG-08 | SKILL-DIVERSITY | Node doesn't use only one ability (e.g., all Charisma checks) |
| RPG-09 | NPC-VOICE-CONSISTENT | NPC dialogue matches voice/tone from characters-d5e.md profile |
| RPG-10 | COMPANION-TIMELINE | Companion can only be recruited once, only alive if alive flag set |

### Cross-Campaign Validation

If `--mode rpg` and `--unit-tests`:

After all nodes verified, run:

| Check | What it validates |
|---|---|
| **Ending Gate Viability** | At least 2-3 endings viable at Session 8, exactly 1 by Session 15 |
| **Reputation Arc** | Each faction reputation traces realistic arc from start to ending (e.g., guard +50 total by Session 15) |
| **Companion Recruitment** | All 3 companions recruited in logical sequence with approval progression |
| **Skill Check Distribution** | Campaign uses balanced mix of abilities (not 70% Charisma, 30% others) |
| **Campaign Duration** | 290 nodes map correctly to 15 sessions (~19 nodes per session) |
| **Encounter Scaling** | Combat encounters scale with party level (CR appropriate per session) |
| **Loot Progression** | Gold/treasure awards cumulative and realistic for party level arc |

### RPG Validation Report

Output special report for `--mode rpg`:

```
RPG Campaign Validation Report
───────────────────────────────

Campaign: [CAMPAIGN_NAME] (System: D&D 5e)
Sessions: 15 | Nodes: 290 | Companions: 3 | Factions: 3

✓ ENDING GATES
  - Just Ruler: reachable after Session 5 ✓, locked by Session 14 ✓
  - Shadow Broker: reachable after Session 6 ✓, locked by Session 14 ✓
  - Redemption: reachable after Session 5 ✓, locked by Session 13 ✓
  - (2 more endings...) ✓

✓ REPUTATION ARCS
  - Guard Rep: 0 → +85 (target +50 for Just Ruler) ✓
  - Temple Rep: 0 → +70 (target +60 for Redemption) ✓
  - Syndicate Rep: 0 → -30 (target <20 for Just Ruler) ✓

✓ COMPANION TIMELINES
  - Thorne: recruited Session 2, approval arc -10→+60 ✓
  - Sister Mercy: recruited Session 5, approval arc 20→+75 ✓
  - Kael: recruited Session 7, approval arc 0→+50 ✓

✓ SKILL CHECK BALANCE
  - Charisma: 45 checks (26%)
  - Wisdom: 42 checks (24%)
  - Dexterity: 38 checks (22%)
  - Intelligence: 35 checks (20%)
  - Strength: 18 checks (10%)
  - Constitution: 12 checks (7%)
  Overall: ✓ BALANCED

⚠ WARNINGS
  - [NODE-087] Skill check outcome missing for Persuasion DC 12
  - [NODE-145] Faction reputation change not announced in dialogue
  - [SESSION-10] Session has only 17 nodes (expected ~19)

✓ VERIFIED: 287 nodes clean, 3 nodes with warnings
```

---
