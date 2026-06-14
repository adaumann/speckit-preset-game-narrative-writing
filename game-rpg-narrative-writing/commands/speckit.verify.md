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
- *(no argument)* — validate every DRAFT node that has no `verified: true` flag in its header

**RPG Presets** (auto-detected): Platform/ruleset extracted from `constitution.md`; RPG validation runs automatically. No `--mode rpg` flag needed.

## What this command does

`speckit.verify` runs validation in sequence:

**Pre-Execution** (RPG Auto-Detection):
- Read `.specify/memory/constitution.md` and extract `[PLATFORM]` and `[RULESET]`
- If `[PLATFORM]` = "Tabletop": Activate Tabletop RPG validation (TR tests below)
- If `[PLATFORM]` = "Computer Game": Activate Computer Game RPG validation (CR tests below)
- Store `SESSION.platform` and `SESSION.ruleset` for ruleset-specific test selection (D&D 5e/PF2e/SR6e)

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

   a. **Load context**:
      - `.specify/memory/constitution.md` (POV, platform, ruleset)
      - `specs/plan.md` (node graph, paths)
      - `specs/variables.md` (declared variables)
      - **RPG Context** (if `SESSION.is_rpg = true`):
        - `specs/mechanics-[ruleset].md` (DC ranges, approval thresholds, faction rep ranges)
        - `specs/npc-roster.md` (companion profiles, recruitment gates)
        - `specs/quests.md` (quest/session context, factions)
        - **Tabletop only**: `draft/campaign-guide.md` (campaign context), `draft/SESSION-[N]/` (session node groupings)
        - **Computer only**: `specs/locations.md` (difficulty scaling), `specs/accessibility-features.md`

   b. Run Layer 1 (structural tests):
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

## RPG-Specific Validation Tests

**When activated**: If `constitution.md` declares `[PLATFORM]` as "Tabletop" or "Computer Game", RPG validation runs automatically. Runs in addition to structural tests (T-01 through T-09 still run).

### TR – Tabletop RPG Tests (if `SESSION.is_rpg = "tabletop"`)

| ID | Name | What it checks |
|---|---|---|
| TR-01 | SESSION-CONTEXT | Node frontmatter has `session: [N]` and `encounter_type` (Combat/Social/Investigation/Puzzle/Hybrid) |
| TR-02 | GM-NOTES-PRESENT | Node has GM Notes section with session #, NPC list, encounter type, key mechanics |
| TR-03 | CR-BALANCE | If combat: CR appropriate to party level (±2 tolerance per outlined party level) |
| TR-04 | SKILL-CHECK-OUTCOME | Each skill check has explicit success/failure narration documented |
| TR-05 | COMPANION-APPROVAL-VALID | Companion approval changes within -100 to +100; recruitment timeline valid (recruited before use) |
| TR-06 | FACTION-REP-ANNOUNCED | Faction reputation changes announced in dialogue (not silent variable shift) |
| TR-07 | SESSION-PACING | Node should fit within 30-120 minutes (typical session 2-4 hours) |
| TR-08 | COMBAT-NARRATIVE-JUSTIFIED | Combat is foreshadowed or narratively justified (not arbitrary encounter placement) |
| TR-09 | NPC-ROSTER-CONSISTENCY | All NPC names/voices match `npc-roster.md` Tabletop section |
| TR-10 | QUEST-STRUCTURE-VALID | If node contains quest stage, matches stage progression in `quests.md` |

### CR – Computer Game RPG Tests (if `SESSION.is_rpg = "computer"`)

| ID | Name | What it checks |
|---|---|---|
| CR-01 | PLAYSTYLE-ROUTING | Node documents which playstyles (Combat/Dialogue/Exploration) reach this node |
| CR-02 | PLAYSTYLE-CONVERGENCE | All three playstyles eventually converge to same story beat within 2 nodes |
| CR-03 | DIFFICULTY-SCALING | Easy/Normal/Hard variants documented with distinct NPC counts/AC/loot |
| CR-04 | ACCESSIBILITY-DOCUMENTED | If timed challenge or puzzle: accessibility features documented (colorblind, audio, motor, cognitive) |
| CR-05 | SKILL-CHECK-BRANCHING | All skill checks have distinct success/failure outcomes (success→NODE-X, failure→NODE-Y) |
| CR-06 | APPROVAL-GATES-VALID | Companion approval gates are within ±100; prerequisite companions recruited before use |
| CR-07 | DIFFICULTY-NOT-LOCKING | Hard mode does NOT lock progression (story completable on all difficulties) |
| CR-08 | PLAYSTYLE-TIME-BALANCE | No single playstyle route takes 3× longer than others |
| CR-09 | NPC-CONSISTENCY | All NPC names match `npc-roster.md` Computer Game section |
| CR-10 | DIALOGUE-BRANCHING | If dialogue-heavy: immediate options <10; sub-branches lead to fewer options |

### DR – D&D 5e Tests (if `SESSION.ruleset = "D&D 5e"`)

| ID | Name | What it checks |
|---|---|---|
| DR-01 | SKILL-CHECK-DC | All skill check DCs fall within 5-20 range per D&D 5e scale (5-9 Easy, 10-12 Easy, 13-15 Medium, 16-18 Hard, 19-20 Very Hard) |
| DR-02 | APPROVAL-RANGE | Companion approval changes within -100 to +100; recruitment typically ≥ -50 or ≥ 0 |
| DR-03 | SPELL-REFERENCE | Spell/ability references include proper notation (spell level, attunement, etc.) |
| DR-04 | MAGIC-ITEM-RARITY | Magic item rarity matches party level (Common/Uncommon 1-4, Rare 5-10, Very Rare+ 11+) |
| DR-05 | ABILITY-BALANCE | If multiple skill paths: balanced across abilities (not all Charisma) |
| DR-06 | NPC-STATBLOCK | NPC stat blocks referenced from `npc-roster.md` D&D 5e section |
| DR-07 | FACTION-REP-CUMULATIVE | Faction reputation changes tracked cumulatively (no single node exceeds ±25 per faction) |

### PR2 – Pathfinder 2e Tests (if `SESSION.ruleset = "Pathfinder 2e"`)

| ID | Name | What it checks |
|---|---|---|
| PR2-01 | SKILL-CHECK-DC | All skill check DCs fall within 10-50+ per Pathfinder 2e scale (10-11 Easy, 12-15 Medium, 16-20 Hard, 21-30 Very Hard, 31+ Extreme) |
| PR2-02 | DEGREE-OF-SUCCESS | All skill checks document degree of success outcomes (Critical Success/Success/Failure/Critical Failure) |
| PR2-03 | HERO-POINTS | Hero Point spending opportunities documented if available in node |
| PR2-04 | ANCESTRY-IMPLICATIONS | Ancestry/background implications acknowledged in narrative (not just mechanical) |
| PR2-05 | COMPANION-RECRUITMENT | Companion recruitment requires realistic approval threshold (≥ 0 approval) |
| PR2-06 | NPC-STATBLOCK | NPC stat blocks referenced from `npc-roster.md` Pathfinder 2e section |

### SR – Shadowrun 6e Tests (if `SESSION.ruleset = "Shadowrun 6e"`)

| ID | Name | What it checks |
|---|---|---|
| SR-01 | DICE-POOL-NOTATION | All dice pool checks documented with [Skill + Attribute] notation and threshold noted |
| SR-02 | ROUTING-OPTIONS | Street / Matrix / Astral routing options all genuinely available (not forced specialization) |
| SR-03 | ROUTING-BALANCE | Success/failure outcomes distinct across routing options; rewards roughly equivalent (Nuyen/Karma/info) |
| SR-04 | GLITCH-TRACKING | Glitch risk noted for critical rolls (2+ ones = glitch regardless of successes) |
| SR-05 | KARMA-ECONOMY | Karma spending tracked across node (no excessive single-node dumps; cumulative tracking valid) |
| SR-06 | CONTACT-TRACKING | Street Cred / Contact opportunities clearly documented if networking present |
| SR-07 | ROUTING-DIFFICULTY | Matrix/Street/Astral paths have equivalent difficulty and time to same outcome |

### Cross-Campaign Validation

If `SESSION.is_rpg = true` and `--unit-tests` flag set: After all nodes verified, run platform-specific validation:

**Tabletop Campaign Validation** (if `SESSION.is_rpg = "tabletop"`):

| Check | What it validates |
|---|---|
| **Ending Gate Viability** | At least 2-3 endings viable by mid-campaign, exactly 1 by final session |
| **Reputation Arc** | Each faction reputation traces realistic arc from start to ending (no 0→+100 in 1 session) |
| **Companion Recruitment** | All companions recruited in logical sequence with approval progression; timeline valid |
| **Skill Check Distribution** | Campaign uses balanced ability mix (no single ability >30% of total checks) |
| **Campaign Duration** | Nodes map correctly to session structure (~18-20 nodes per session for 2-4 hour gameplay) |
| **Encounter Scaling** | Combat encounters scale with party level (CR matches outlined progression; no CR >+3 for level) |
| **Loot Progression** | Treasure awards cumulative and appropriate (magic items match level recommendations) |
| **Companion Arc Closure** | All recruited companions reach narrative resolution before campaign end |
| **Session Pacing** | Each session averages 2-4 hours of gameplay (derived from node visit times) |

**Computer Game Campaign Validation** (if `SESSION.is_rpg = "computer"`):

| Check | What it validates |
|---|---|
| **Playstyle Route Balance** | All three playstyles (Combat/Dialogue/Exploration) reach story conclusion; time imbalance <3× |
| **Difficulty Scaling Consistency** | Easy/Normal/Hard progression consistent across all nodes (no artificial locks) |
| **Ending Gate Viability** | Ending gates remain achievable on all difficulties; choices have consequences |
| **Accessibility Completeness** | All timed challenges have accessibility variants (colorblind, audio, motor, cognitive) |
| **Companion Approval Consistency** | Approval changes sum to realistic ranges per ending (e.g., +50 for romance, -30 for betrayal) |
| **Story Convergence Points** | All playstyle routes meet at major story beats (chapters/act transitions) |
| **Difficulty Lock Absence** | Hard mode never locks story content (all story beats reachable on all difficulties) |
| **Chapter Structure** | Chapters follow consistent difficulty/progression pacing (no wild level spikes) |
| **Dialogue Tree Navigability** | Dialogue trees remain navigable (max depth 5, avg 2-3 choices per node) |

**Ruleset-Specific Cross-Campaign Validation**:

| Ruleset | Additional Checks |
|---|---|
| **D&D 5e** | Party level progression matches combat CR curve; magic item distribution by rarity; spell scaling appropriate |
| **Pathfinder 2e** | Party level and degrees of success outcomes consistent; hero point economy viable; treasure grade progression |
| **Shadowrun 6e** | Street Cred/Karma/Nuyen economies balanced; routing difficulty equivalent; contact network progression logical |

### RPG Validation Report

**Tabletop Campaign Report** (if `SESSION.is_rpg = "tabletop"`):

```
TABLETOP CAMPAIGN VERIFICATION REPORT
─────────────────────────────────────

Campaign: [CAMPAIGN_NAME] | System: [D&D 5e / Pathfinder 2e / Shadowrun 6e]
Sessions: 15 | Total Nodes: 290 | Companions: 3 | Factions: 4

SESSION STRUCTURE
✓ Session distribution: 18-22 nodes per session (average 19.3)
✓ Pacing: 2-4 hours per session maintained

ENCOUNTERS
✓ Combat CR Scaling:
  - Sessions 1-3: CR 1-2 (58 encounters) ✓
  - Sessions 4-7: CR 2-4 (76 encounters) ✓
  - Sessions 8-12: CR 3-6 (89 encounters) ✓
  - Sessions 13-15: CR 5-8 (45 encounters) ✓
⚠ [SESSION-10] One encounter CR 7 for level 9 party (±2 tolerance exceeded)

COMPANION ARCS
✓ Thorne: recruited Session 2, approval -10→+75 ✓
✓ Sister Mercy: recruited Session 5, approval +20→+85 ✓
✓ Kael: recruited Session 7, approval 0→+60 ✓

FACTION REPUTATIONS
✓ Guard Rep: 0→+95 (target +85 for Justice ending) ✓
✓ Temple Rep: 0→+78 (target +70 for Redemption) ✓
✓ Syndicate Rep: 0→-45 (target <-20 for Justice) ✓
⚠ [NODE-234] Single reputation change +30 (exceeds typical ±25 per node)

ENDING GATES
✓ Justice ending: reachable Sessions 6-14 ✓ | locked by Session 15 ✓
✓ Redemption ending: reachable Sessions 7-13 ✓ | locked by Session 14 ✓
✓ Shadow Broker ending: reachable Sessions 8-12 ✓ | locked by Session 13 ✓

SKILL CHECKS
✓ Ability distribution:
  - Charisma: 52 checks (28%)
  - Wisdom: 44 checks (24%)
  - Dexterity: 40 checks (22%)
  - Intelligence: 35 checks (19%)
  - Strength: 15 checks (8%)
  - Constitution: 12 checks (6%)
✓ BALANCED

VERIFIED: 287 nodes clean | 2 nodes with warnings | 1 node requires revision
```

**Computer Game Campaign Report** (if `SESSION.is_rpg = "computer"`):

```
COMPUTER GAME VERIFICATION REPORT
──────────────────────────────────

Campaign: [CAMPAIGN_NAME] | System: [D&D 5e / Pathfinder 2e / Shadowrun 6e]
Total Nodes: 156 | Chapters: 8 | Playstyles: 3 | Difficulty Modes: 3

PLAYSTYLE ROUTES
✓ Combat Route: 156 nodes, ~4.2 hours, all story beats reachable ✓
✓ Dialogue Route: 156 nodes, ~3.8 hours, all story beats reachable ✓
✓ Exploration Route: 156 nodes, ~4.5 hours, all story beats reachable ✓
⚠ Time imbalance: Exploration 18% longer than Dialogue (within 3× tolerance) ✓

DIFFICULTY SCALING
✓ Easy: 42 encounters (reduced NPC counts, lower AC)
✓ Normal: 42 encounters (standard NPC counts, standard AC)
✓ Hard: 42 encounters (increased NPC counts, higher AC, more loot)
✓ Story locked on Hard: NONE ✓ (all story content completable)

ENDING GATES
✓ Ending A: accessible on Easy/Normal/Hard ✓ | multiple routes to achieve ✓
✓ Ending B: accessible on Easy/Normal/Hard ✓ | multiple routes to achieve ✓
✓ Ending C: accessible on Easy/Normal/Hard ✓ | multiple routes to achieve ✓

ACCESSIBILITY COMPLIANCE
✓ 12 timed challenges: 12 with accessibility variants ✓
✓ Colorblind modes: 8/12 timed challenges ✓
✓ Audio alternatives: 6/12 timed challenges ✓
✓ Motor accessibility: 10/12 timed challenges ✓
✓ Cognitive accessibility: 7/12 timed challenges ✓
⚠ [NODE-089] Timed puzzle missing cognitive accessibility variant

COMPANION APPROVAL
✓ Companion A: -50→+95 across routes ✓
✓ Companion B: 0→+75 across routes ✓
✓ Companion C: -30→+60 across routes ✓
✓ Approval changes consistent across playstyles ✓

CHAPTER PACING
✓ Chapter 1: 18 nodes, 45 min avg ✓
✓ Chapter 2: 22 nodes, 52 min avg ✓
✓ Chapter 3: 19 nodes, 48 min avg ✓
... (Chapters 4-8)
✓ All chapters within 40-60 min target ✓

VERIFIED: 154 nodes clean | 1 node with warnings | 1 node requires revision
```

---

## Key Principles for RPG Verification

**Auto-Detection**: No flags required. Verification automatically detects platform/ruleset from `constitution.md`. RPG tests activate based on detected context.

**Layered Validation**:
1. **Structural Tests** (T-01 through T-09): Always run. Ensure nodes are syntactically valid.
2. **Platform-Specific Tests** (TR or CR): Run if RPG detected. Validate platform-specific design (session context for Tabletop, playstyle routing for Computer).
3. **Ruleset-Specific Tests** (DR/PR2/SR): Run if ruleset detected. Validate system mechanics (DC ranges, approval gates, encounter scaling).
4. **Cross-Campaign Tests**: Run only with `--unit-tests`. Validate entire campaign consistency (all endings viable, reputation arcs realistic, skill balance).

**Hard-Fail Scenarios**:
- **Any Structural Test Failure** (T-01 through T-09): Node fails verification. Self-correction loop attempts fix.
- **Tabletop TR-01 Failure** (missing session context): Node fails. GM cannot prepare.
- **Tabletop TR-03 Failure** (CR out of range by >2): Node fails. Encounter unbalanceable.
- **Computer CR-07 Failure** (difficulty locks progression): Node fails. Player stuck on Hard mode.
- **Ending Gate Unreachable** (cross-campaign): Campaign fails. Story cannot be completed.

**Self-Correction Loop** (Automatic Fixes):
- Attempts up to 3 fixes per hard error
- Applies minimal targeted changes to resolve failure
- If 3 attempts fail: Prompts user for manual intervention

**Tabletop Specifics**:
- Validates session structure (~18-20 nodes per 2-4 hour session)
- CR scaling per party level with ±2 tolerance
- Companion recruitment timeline and approval progression
- Faction reputation arcs toward ending gates
- Encounter narrative justification (combat foreshadowed, not arbitrary)

**Computer Game Specifics**:
- Validates playstyle route convergence (all routes reach story beats)
- Difficulty scaling on all modes (Hard does NOT lock story)
- Accessibility completeness (timed challenges have all variants)
- Dialogue tree navigability (depth/branching reasonable)
- Route time balance (no single playstyle 3× longer than others)

**Ruleset Validation**:
- **D&D 5e**: DC 5-20, approval/faction ±100, magic item rarity by level
- **Pathfinder 2e**: DC 10-50+, degree of success outcomes, hero point economy
- **Shadowrun 6e**: Dice pool notation, Street/Matrix/Astral routing balance, Karma/Street Cred economy

**Report Output**:
- Shows section-by-section pass/fail/warning counts
- Highlights critical issues (hard-fails) prominently
- Provides actionable suggestions for warnings
- Campaign-level report shows: ending viability, reputation arcs, companion timelines, skill balance, playstyle routes (if Computer), accessibility (if Computer)
