---
description: Full structural analysis of all node files – branch integrity, variable coverage, endings reachability, and plan alignment. Run after node drafting phases; for per-node quality checks use speckit.checklist. For RPG campaigns (tabletop D&D/Pathfinder/Shadowrun and computer game), validates companion loyalty variables, faction reputation tracking, session structure, playstyle route isolation, and accessibility consistency.
handoffs:
  - label: Fix Flagged Nodes
    agent: speckit.revise
    prompt: Fix the structural issues flagged by the analysis report
    send: true
  - label: Run Continuity Check
    agent: speckit.continuity
    prompt: Structural issues are fixed. Run a continuity check across all nodes.
    send: true
  - label: Run Per-Node Quality Checks
    agent: speckit.checklist
    prompt: Run per-node quality checks across all drafted nodes
    send: true
---

# speckit.analyze
**RPG Campaign Support**: Adapts structural analysis for tabletop (companion loyalty variable consistency, faction reputation tracking, session node structure, campaign-guide.md synchronization) and computer game (playstyle route isolation, accessibility variant consistency, route-exclusive variable validation).
## Goal

Verify that all drafted node files are structurally sound and internally consistent. Catch dead ends, unreachable nodes, undeclared variables, unreachable endings, and plan mismatches now � not after a full playtest cycle.

Run after node drafting phases. Does not modify any files. For per-node prose and dialogue quality checks, use `speckit.checklist` instead.

## User Input

```text
$ARGUMENTS
```

You **MUST** consider the user input before proceeding (if not empty). Accepted arguments:
- *(no argument)* � analyze all nodes in `nodes/`
- `--act [N]` � scope analysis to a single act
- `--check dead-ends|unreachable|variables|endings|plan|hooks` � run only one class of check
- `--report` � write full analysis output to `analysis-report.md`

## Pre-Execution Checks

**Auto-detect platform and ruleset** (for RPG campaigns):
- Load `constitution.md`
- Extract `[PLATFORM]` (tabletop/computer) and `[RULESET]` (D&D 5e/Pathfinder 2e/Shadowrun 6e)
- Set SESSION object: `{platform: [PLATFORM], ruleset: [RULESET], mechanics: [MECHANICS]}` for downstream checks
- If no platform found: treat as generic interactive fiction (no RPG-specific logic)

**Check for extension hooks (before analysis)**:
- Check if `.specify/extensions.yml` exists in the project root.
- If it exists, read it and look for entries under the `hooks.before_analyze` key.
- Process as standard hook block (Optional/Mandatory). Skip silently if absent.

Then:
1. Confirm `nodes/` directory exists and contains at least one node file.
2. Load `specs/plan.md` – required for reachability and alignment analysis.
3. Load `specs/variables.md` – required for variable declaration check.
4. Load `specs/endings.md` – required for endings reachability check.
5. Load `.specify/memory/constitution.md` – required for hook schema compliance check.
6. If RPG: Load `companions.md`, `factions.md`, `campaign-guide.md` (if applicable), `mechanics-[RULESET].md`

## Operating Constraints

**STRICTLY READ-ONLY**: Do not modify any files. Output a structured analysis report. Offer an optional remediation plan only if the user explicitly asks for one.

**Constitution Authority**: `.specify/memory/constitution.md` is non-negotiable. If a mechanic or structural principle needs to change, that requires a `speckit.constitution` update � not reinterpretation.
**RPG Campaign Authority** (if applicable): For tabletop campaigns, `campaign-guide.md`, `companions.md`, and `factions.md` are authority documents. Node variables must align with these specs. For computer games, `mechanics-[RULESET].md` defines ruleset-specific validation rules.
## Execution Steps

1. **Setup**: Run `{SCRIPT}` from repo root and parse JSON for spec file paths.

2. **Load documents**:
   - **Required**: `nodes/` (all drafted node files), `specs/plan.md`, `specs/variables.md`, `specs/endings.md`, `.specify/memory/constitution.md`
   - **Optional**: `outlines/` (for outline-gate compliance check), `specs/spec.md`, `specs/relationships.md` (for relationship beat coverage check), `specs/timeline.md` (for continuity constraint check)
   - Abort with a clear error if any required document is missing.

3. **Run analysis across these dimensions**:

   **A. Branch Integrity** (dead ends & unreachable nodes) � severity: CRITICAL if blocking
   - Find all non-terminal nodes with 0 outgoing choices
   - Find all nodes where all choice targets are referenced but no corresponding file exists
   - Build the full node?choice?node graph from all node files
   - Identify nodes with no incoming links (orphaned)
   - Cross-reference with `plan.md`: flag plan nodes with no drafted file; flag drafted nodes not in `plan.md`

   **B. Variable Coverage**
   - Scan all `variables_read` and `variables_set` frontmatter fields across all node files
   - Check every variable against `specs/variables.md` � flag undeclared variables as CRITICAL
   - Check for read-before-set: a variable read in a node that has no upstream node setting it on any path to that node � flag as CRITICAL
   - Flag any variable declared in `specs/variables.md` that is never read or set in any node � WARNING

   **C. Endings Reachability**
   - For each ending in `specs/endings.md`, trace whether its required variable conditions can be satisfied on at least one complete path from the opening node to the ending node
   - Flag any ending with no satisfiable path as CRITICAL
   - Flag any ending node referenced in `specs/endings.md` with no drafted node file as CRITICAL

   **D. Flowmap ? Node Alignment**
   - List flowmap nodes that have no drafted file in `nodes/` � WARNING (or CRITICAL if gating an ending)
   - List drafted node files not registered in `plan.md` � WARNING
   - Verify act assignments in node frontmatter match the act assignments in `plan.md` � flag mismatches as WARNING

   **E. Outline Gate Compliance**
   - For each drafted node, check whether a corresponding `outlines/[NODE_ID].md` exists with `status: APPROVED`
   - Flag any node drafted without an APPROVED outline as WARNING (outline gating was bypassed)

   **F. Hook Schema Compliance**
   - For each `variables_set` entry across all nodes, verify the hook type matches the valid hook types defined in `.specify/memory/constitution.md` mechanic schemas
   - Flag invalid or unrecognised hook types as WARNING
   - Flag any NPC trust or state variable that exceeds its declared range in `specs/variables.md` as WARNING

   **G. Relationship Beat Coverage** *(skip if `specs/relationships.md` is absent)*
   - For each REL-NNN in `specs/relationships.md`: verify that all five key beats have a mapped node ID (not `[NEEDS NODE]`) � flag any unmapped beat as WARNING
   - Verify the mapped node exists in `specs/plan.md` � flag missing nodes as CRITICAL if the beat gates an ending

   **H. Timeline Constraint Check** *(skip if `specs/timeline.md` is absent)*
   - For each TC-NNN in `specs/timeline.md`: verify no drafted node with a variable value that satisfies the "before" condition precedes the required fabula event � flag violations as CRITICAL
   **I. RPG Campaign Variable Consistency** (if [PLATFORM] detected)
   
   *For Tabletop*:
   - **Companion Loyalty Tracking**: For each companion in `companions.md`, verify `loyalty(companion_name)` variable is declared in `specs/variables.md` with proper range (typically -5 to +5 or -10 to +10)
   - Flag any companion without a loyalty variable as CRITICAL (companion state cannot persist)
   - Check that all loyalty changes in nodes match the declared range; flag out-of-range changes as WARNING
   - Verify companion loyalty variables are read and set across multiple sessions (not just one session) – flag single-session-only companions as WARNING
   - **Faction Reputation Tracking**: For each faction in `factions.md`, verify `faction_reputation(faction_name)` is declared in `specs/variables.md` with proper range
   - Flag any faction without a reputation variable as CRITICAL
   - Check that faction reputation changes carry forward across modules (reputation set in Session 3 should be readable in Session 5) – flag reputation that reconverges as WARNING
   - **Campaign Prep Doc Sync**: Verify `campaign-guide.md` companion roster matches `companions.md` definitions
   - Flag any companion in campaign-guide.md not defined in companions.md as WARNING
   - Flag any "joined in Session N" marker without a corresponding node setting `companion_joined` variable as WARNING
   - **Session Structure**: Verify all nodes are assigned to correct session (SESSION-N) in frontmatter
   - Flag nodes not assigned to any session as WARNING
   - Flag nodes in SESSION-N that reference SESSION-M events without corresponding nodes as CRITICAL
   
   *For Computer Game*:
   - **Route Isolation**: Check that route-exclusive variables (e.g., `$stealth_mode`, `$combat_stance`) are not readable from other route paths
   - Flag any route-exclusive variable accessible in another route as CRITICAL (route leakage)
   - **Playstyle Commitment**: Verify `$player_playstyle` variable is set once (route commitment) and never changed
   - Flag any node that changes `$player_playstyle` after initial commitment as CRITICAL
   - **Accessibility Consistency**: For each accessibility variant (colorblind, audio, motor), check that variant-specific variables exist for all route nodes
   - Flag any route missing accessibility variant variables as WARNING
   - Verify accessibility variables are consistent across all chapters (if colorblind variant exists in Chapter 2, must exist in Chapters 3-4) – flag missing variants as CRITICAL
   - **Route Balance Validation**: Calculate content point totals per route (encounters, puzzles, bosses weighted)
   - Flag any route with >3× imbalance vs. others as WARNING (e.g., Stealth 100 points, Combat 25 points)
   - **Variable Naming**: Verify route-exclusive variables use route-prefixed naming (e.g., `$stealth_discovered_tunnel` not `$discovered_tunnel`)
   - Flag unprefixed route-exclusive variables as WARNING (risk of accidental cross-route access)
4. **Output structured report**:

   ```
   ## Structural Analysis Report

   **Platform**: [Generic / Tabletop-D&D5e / Tabletop-Pathfinder2e / Tabletop-Shadowrun6e / Computer-Game]

   ### CRITICAL Issues (blocking – fix before QA or export)
   - [issue] – [node or file] – [remediation suggestion]
   - [For RPG] [missing companion loyalty var] – companions.md – Add loyalty(NAME) to specs/variables.md
   - [For RPG] [route variable leakage] – NODE-XXX – Rename $var to $route_var to prevent cross-route access
   - [For RPG] [campaign guide sync] – campaign-guide.md – Update roster to match actual companion state in nodes

   ### WARNINGS (quality risks, addressable before export)
   - [issue] – [node or file] – [suggestion]
   - [For RPG] [single-session companion] – Companion: Theron – Add scenes in later sessions to demonstrate persistence
   - [For RPG] [faction reputation reconverges] – Faction: Temple – Reputation set in Session 3, but Session 5 has no reputation check
   - [For RPG] [route imbalance >3×] – Routes – Stealth: 100 points, Combat: 25 points – Rebalance content distribution
   - [For RPG] [unprefixed route variable] – NODE-015 – Rename $discovered_secret to $stealth_discovered_secret

   ### PASS (dimensions with no issues)
   - [dimension]: OK

   ### Summary
   CRITICAL: N | WARNINGS: N | PASS: N
   Nodes analyzed: N | Flowmap nodes: N | Endings checked: N | Variables checked: N | Relationships checked: N | Timeline constraints: [N checked / skipped]
   **[For RPG]** Companions: [N companions with loyalty tracking] | Factions: [N factions with reputation tracking] | Sessions: [Session range] | Routes: [N routes, imbalance ratio]
   Recommended action: [clear to QA / fix criticals first / run speckit.revise on flagged nodes]
   ```

   If `--report` is set, write the full details to `analysis-report.md`.

5. **Check for extension hooks (after analysis)**:
   - Look for `hooks.after_analyze` in `.specify/extensions.yml`. Process as standard hook block. Skip silently if absent.

6. **Optional remediation plan**: Only if the user explicitly requests it, list the specific file edits needed to resolve CRITICAL issues. The user must approve before any editing commands are invoked.

---

## RPG Campaign Analysis Notes

**Tabletop Campaign Variable Structure**:
- Every companion must have `loyalty(companion_name)` variable that persists across all sessions
- Loyalty changes should be meaningful: +/- 1 for normal choices, +/- 2-3 for major decisions
- Verify loyalty state is readable in later sessions to determine NPC behavior/availability
- Faction reputation variables must follow same logic: persist across modules, affect quest availability

**Tabletop Campaign Prep Synchronization**:
- `campaign-guide.md` is the player contract: what's documented there is ground truth
- Any node setting companion state should update campaign-guide.md implications (e.g., "if Theron left party, remove from active companion list")
- Session node assignments must match `plan.md` session structure (no SESSION-5 nodes if campaign only has 4 sessions)
- Campaign-level decisions (companion recruitment, faction alignment) must be tracked in campaign-guide.md updates

**Computer Game Route Structure**:
- Route commitment is one-way: once player chooses Stealth in CHAPTER-2, all subsequent route-exclusive nodes are Stealth-only
- Route-exclusive variables MUST be prefixed (e.g., `$stealth_*`, `$combat_*`, `$diplomacy_*`) to prevent accidental cross-route data leakage
- Accessibility variants are orthogonal to routes: a colorblind player can play Stealth route with colorblind-enabled UI
- Route imbalance >3× is a quality warning: if routes have different content volumes, ensure player doesn't feel Stealth route is "less satisfying"
- All route-exclusive nodes must exist in every route for fair playstyle comparison

**Ruleset-Specific Validation**:
- Load `mechanics-[RULESET].md` to verify variable ranges, DC values, etc. match ruleset conventions
- D&D 5e: Check DCs are in 8-20 range; Pathfinder 2e: Check roll values use 1-20 + modifiers; Shadowrun 6e: Check karma/edge values match convention
- Flag any variable that violates ruleset-specific constraints as WARNING (may confuse players familiar with ruleset)

