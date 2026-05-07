---
description: Validate variable state consistency across all branches, check POV drift, and validate series carry-over variables. For RPG campaigns (tabletop D&D/Pathfinder/Shadowrun and computer game), validates companion loyalty consistency, faction reputation persistence, session-to-session transitions, playstyle route isolation, and accessibility consistency across routes.
handoffs:
  - speckit.revise: Fix nodes with continuity failures
  - speckit.series: For series carry-over validation specifically
---

# speckit.continuity

**RPG Campaign Support**: Adapts continuity validation for tabletop (companion loyalty consistency, faction reputation persistence, session-to-session transitions, NPC roster stability) and computer game (playstyle route isolation, accessibility consistency, chapter-to-chapter variable carry-over, route-exclusive state management).

Run a full continuity analysis across all node files. Validates variable state consistency on all paths, POV drift, series carry-over variables, and NPC state transitions.

## User Input

Provide one of:
- Nothing — full continuity check across all nodes
- A specific check: `--check variables|pov|npc|dialogue|glossary|locations|relationships|series|timeline|thematic`
- A scope: `--act [N]` to scope to one act

Optional flags:
- `--check [types]` — run only specific checks (comma-separated: variables, pov, npc, dialogue, glossary, locations, relationships, series, timeline, thematic)
- `--act [N]` — scope to a single act
- `--report` — write output to `continuity-report.md`
- `--strict` — require all nodes to have `polished: [date]` before continuity check (default: optional)

## Pre-Execution Checks

**Auto-detect platform and ruleset** (for RPG campaigns):
- Load `constitution.md`
- Extract `[PLATFORM]` (tabletop/computer) and `[RULESET]` (D&D 5e/Pathfinder 2e/Shadowrun 6e)
- Set SESSION object {platform, ruleset, mechanics}
- If RPG: Load `companions.md`, `factions.md`, `mechanics-[RULESET].md`, `plan.md` (for session structure)

**Standard checks**:
1. Confirm `draft/` contains node files to analyze.
2. Load `variables.md` — authoritative variable registry.
3. Load `.specify/memory/constitution.md` — POV, craft rules, and prose profile.
4. Load `characters/` — NPC state machines, trust thresholds, dialogue registers.
5. Load `.specify/memory/craft-rules.md` — dialogue style rules per prose profile.
6. If `--strict`: verify all node files have `polished: [date]` in frontmatter; warn if not found and continue.
7. If `specs/glossary.md` exists: load for terminology consistency checks.
8. If `specs/locations.md` exists: load for location state consistency checks.
9. If `--check series` or `series-bible.md` exists: load `series-bible.md`.
10. If `specs/themes.md` exists: load it for thematic drift and motif checks.
11. If `specs/relationships.md` exists: load it for NPC dynamic consistency checks.
12. If `specs/timeline.md` exists: load it for continuity constraint checks.

## Outline

1. **Variable state consistency**
   - Simulate all reachable paths from NODE-001 through each ending
   - For each path: track variable state at each node
   - Detect: variable read before any set on that path; variable set to value outside declared range; counter exceeding declared max; flag set twice without being cleared
   - Report per-path, per-variable: "PATH [A?C?E]: $trust_mira = 130 at NODE-012 (exceeds max 100)"

2. **POV drift check**
   - Load `player_perspective` from constitution.md
   - Scan all node prose for POV violations:
     - Second-person project: flag any `he/she/they` referring to the player
     - Third-person project: flag any `you` addressing the player
     - Switching project: verify `$pov` variable is set before each POV-dependent passage
   - Report: "POV drift in NODE-[N] line [N]: '[QUOTE]'"

3. **NPC state transition validation**
   - Load `.specify/memory/craft-rules.md` for dialogue style rules per prose profile (NPC Voice & Dialogue section)
   - For each NPC: verify trust score changes are applied at the correct nodes
   - Verify that NPC dialogue register matches the trust score range at each node where the NPC speaks, and matches the dialogue style rules for the active prose profile
   - Verify that NPC state (alive/dead/hostile) is consistent — NPC dead in NODE-A cannot speak in NODE-B unless NODE-B precedes NODE-A on all paths
   - Report: "[NPC] speaks in NODE-[N] but is dead on PATH [A–B–N]"

4. **Series carry-over validation** (if `series-bible.md` exists or `--check series`)
   - Verify all carry-over variables in `series-bible.md` are declared in `variables.md`
   - Verify each ending's variable state snapshot is achievable on at least one path
   - Report any carry-over variable that is never set before the ending node

5. **Update continuity logs**
   - Append issues to `world-building.md` continuity log and `glossary.md` consistency log
   - Mark resolved issues from previous runs

6. **Thematic drift check** *(skip if `specs/themes.md` is absent)*
   - For each registered motif (MO-NNN): verify it appears in at least 3 drafted nodes; flag < 3 occurrences as WARNING
   - For each act: verify at least one node carries thematic work (node outline "Thematic work" field or prose evidence); two consecutive acts with no thematic work ? CRITICAL
   - For each symbol in the Symbol & Object Registry: verify physical state is consistent across nodes (object cannot be in two locations simultaneously); flag inconsistency as CRITICAL
   - Append issues to `specs/themes.md` Thematic Drift Log

7. **NPC relationship consistency check** *(skip if `specs/relationships.md` is absent)*
   - For each REL-NNN: verify the NPC states implied by each key beat are consistent with the variable values set in the corresponding node
   - Verify no node references an NPC as friendly/ally when the active dynamic at that branch point should make them hostile
   - Append issues to `specs/relationships.md` Relationship Drift Log

8. **Timeline constraint check** *(skip if `specs/timeline.md` is absent)*
   - For each TC-NNN constraint: verify no drafted node violates the stated before/after rule
   - Flag any NPC dialogue that reveals information before the fabula event that creates it — CRITICAL

9. **Dialogue continuity check** *(skip if no `Dialogue Tree` fields found in outlines)*
   - For each node with a `Dialogue Tree` (from `outlines/[NODE_ID].md`):
     - Verify each NPC's dialogue response uses the correct register from `specs/characters/[NPC_ID].md` Section VIII (Dialogue Register by Trust State)
     - Pull the NPC's current trust state from `variables_read` in the outline; verify the dialogue prose in the drafted node matches that register
     - Verify all NPCs present in the dialogue tree are actually present in the node (no dangling NPC responses)
     - For multi-party dialogues: verify NPC-A and NPC-B responses are consistent with their relationship state (from `specs/relationships.md` if present)
   - Report: "[NPC] dialogue in NODE-[N] uses high-register prose but trust state is 'hostile' (expected low-register)"
   - Report: "[NPC-A] and [NPC-B] dialogue in NODE-[N] contradicts their relationship arc"

10. **Glossary validation check** *(skip if `specs/glossary.md` is absent)*
   - Scan all drafted node prose for terminology that appears in `specs/glossary.md` Section I (Term Registry)
   - For each found term: verify it is spelled correctly and used with a meaning consistent with the glossary definition
   - Flag capitalization errors: term registered as `Sanctuary` but used as `sanctuary` in node
   - Flag usage variance: term has a "Rejected variant" in glossary (e.g., "Temporal Flux" vs. rejected "Time Flux") — flag if rejected variant used
   - Flag contradictory definitions: same term used with two different meanings across different nodes
   - Append issues to `specs/glossary.md` Consistency Log

11. **Location state consistency check** *(skip if `specs/locations.md` is absent)*
   - For each location appearing in multiple nodes: extract sensory details and location state from the node prose
   - Verify sensory descriptions are consistent across nodes (e.g., "sterile white walls" in NODE-005 should not become "organic vine-covered walls" in NODE-010 unless explicitly changed)
   - Track location state changes (e.g., if NODE-005 describes the door as "sealed", verify NODE-010 shows the door still sealed unless a node between them opened it)
   - Flag contradictions: "Sanctuary Station described as 'sterile white' in NODE-005 but 'overgrown with moss' in NODE-012 — timeline unclear"
   - Append issues to `specs/locations.md` State Change Log

12. **Multi-party dialogue consistency check** *(skip if fewer than 2 NPCs in project)*
   - For each pair of NPCs (NPC-A, NPC-B) that interact in multiple nodes:
     - Verify their dialogue and interaction patterns are consistent with their relationship arc (from `specs/relationships.md` if present or inferred from trust state delta)
     - If NPC-A's trust toward player is increasing but NPC-B's is decreasing, verify their dialogue reflects this (NPC-A increasingly friendly, NPC-B increasingly distant)
     - Verify neither NPC contradicts information the other has stated in earlier nodes
   - Report: "NODE-005: Corvus trusts you enough to reveal the vault key. NODE-012: Corvus claims he never knew about it. Contradiction." (if trust path supports first statement)

13. **RPG Campaign Continuity Validation** (if [PLATFORM] detected)

**For Tabletop RPG**:
- Companion loyalty consistency: Verify loyalty(companion_name) state changes are justified by dialogue/events; loyalty never decreases without event; all companions start with loyalty(0) or specified initial value
- Faction reputation persistence: Verify faction_reputation(faction_name) values carry across sessions; reputation changes match faction reactions; final reputation values are achievable by at least one path
- Session-to-session roster: Verify companions present in SESSION-N match their alive/dead/joined status from previous sessions; no companion appears after death without resurrection; NPC roster in SESSION-briefing matches campaign-guide.md
- Campaign-level variable carry-over: Verify all SESSION-N references to SESSION-(N-1) variables are declared; no dangling references; quest completion flags persist across sessions unless explicitly cleared
- NPC progression consistency: Verify NPC relationship states are consistent with their appearances across sessions; NPC dialogue reflects campaign progress (knows about previous sessions' events)

**For Computer Game**:
- Route isolation: Verify $stealth_*, $combat_*, $diplomacy_* variables never leak between routes; no variable from one route referenced in another route's nodes
- Route commitment lock: Verify playthrough_route variable is set once in CHAPTER-2 and never changed; all post-CHAPTER-2 nodes verify current route before branching
- Accessibility consistency: Verify accessibility mode variables (colorblind_mode, audio_mode, motor_mode) are available in ALL chapters; no chapter missing accessibility support; accessibility state persists across chapters
- Chapter-to-chapter carry-over: Verify all CHAPTER-N references to CHAPTER-(N-1) outcomes are valid; choices made in CHAPTER-2 affect CHAPTER-3-4 logic; no orphaned outcome states
- Cross-route variable conflicts: Verify no route-generic variable (not prefixed $stealth_/etc.) is set differently by different routes; route-exclusive logic isolated to route-specific prefixed variables

14. **Polish stage gate** (if `--strict` flag set)
   - For each node file in `draft/` or SESSION-N files: verify the frontmatter includes `polished: [YYYY-MM-DD]`
   - Emit a report: "Nodes awaiting polish: [count] (required for --strict mode)"
   - If all nodes have been polished: proceed with full continuity check
   - If some nodes not polished: halt and report which nodes need polish before continuity can be validated in strict mode

15. **Output**
   - Report summary: "Variable errors: [N] | POV drift: [N] | NPC errors: [N] | Dialogue continuity: [N] | Glossary errors: [N] | Location state errors: [N] | Multi-party dialogue: [N] | Series errors: [N] | Thematic drift: [N] | Relationship errors: [N] | Timeline violations: [N]"
   - If RPG campaign: Add to summary: "Companion loyalty: [N] | Faction reputation: [N] | Route isolation: [N] | Accessibility consistency: [N] | Session carry-over: [N]"
   - If `--report`: write full details to `continuity-report.md` with sections per check type
   - Suggest: "Run `speckit.revise NODE-NNN` to fix flagged nodes. Run `speckit.polish NODE-NNN` to complete polish stage gate."
   - If `--strict` and polish gate failed: "Cannot complete continuity check in strict mode. Run `speckit.polish [UNPOLISHED_NODES]` first."

---

## RPG Campaign Continuity Notes

### Tabletop Campaign Continuity Considerations

**Companion Loyalty Consistency**:
- Each companion loyalty state must be justified by dialogue or events
- Loyalty changes should reflect NPC reactions to player choices
- Example: Sir Theron's loyalty(theron) increases from 1 to 2 in SESSION-4 when party chooses to defend Temple (his faction). This choice was presented in SESSION-3, loyalty increase justified.
- Red flags:
  - Loyalty changes without corresponding event/dialogue
  - Loyalty decreases without negative player choice
  - Companion appears in SESSION-5 with loyalty state different from SESSION-4 without explanation
- Testing approach: For each companion, trace loyalty value across all sessions; verify each change is explained

**Faction Reputation Persistence**:
- Faction reputation values must carry from SESSION-N to SESSION-(N+1)
- Reputation changes in SESSION-N must affect available quests in SESSION-(N+1)
- Example: In SESSION-3, party reduces Temple reputation from 2 to -1 by choosing to protect Thieves Guild. In SESSION-4, Temple should not offer quests (only hostile NPCs available)
- Red flags:
  - Faction reputation resets between sessions without explanation
  - SESSION-N decision affects faction reputation but SESSION-(N+1) shows no consequence
  - Faction reputation value outside declared range (-5 to +5 typical)
- Testing approach: For each faction, verify reputation changes persist and create logical consequences

**Session-to-Session NPC Roster**:
- Companions present in SESSION-N must match their alive/dead/joined status from SESSION-(N-1)
- Dead companions cannot appear in later sessions (unless resurrected with explicit mechanic)
- Joined companions should appear in subsequent sessions unless they leave (with explanation)
- Example: Sir Theron joined in SESSION-2. He should appear in SESSION-3 through SESSION-9 unless:
  - He dies (verify death event exists in SESSION-2-8)
  - He leaves party (verify departure dialogue in specific session)
  - He's optional (verify optional roster system documents this)
- Red flags:
  - Companion appears in SESSION-5 but never joined/dead status tracked
  - Companion dies in SESSION-6 but appears in SESSION-8
  - SESSION-N-BRIEFING.md shows different roster than campaign-guide.md
- Testing approach: Cross-check each SESSION-N-BRIEFING.md against campaign-guide.md for roster consistency

**Campaign-Level Variable Carry-Over**:
- Quest completion flags must persist across sessions
- Major story state variables (dragon_slain, temple_sealed) must be accessible in later sessions
- Example: In SESSION-4, party defeats the dragon. Set `$dragon_slain = true`. In SESSION-8, final boss dialogue should read `$dragon_slain` to provide context
- Red flags:
  - SESSION-5 code references `$quest_completed` but variable never set in SESSION-3-4
  - SESSION-8 dialogue mentions past event but relevant quest flag doesn't exist
  - Quest completion flags are local (SESSION-N only) instead of campaign-global
- Testing approach: For each campaign variable, trace when it's set and when it's read; verify all reads have preceding sets

**NPC Progression Consistency**:
- NPCs should remember previous sessions' interactions
- NPC dialogue should reference past events the player participated in
- Example: In SESSION-4, party learns Marcus is secretly working for the Thieves Guild. In SESSION-7, Marcus's dialogue should reference this knowledge (or denial if player never confronted him)
- Red flags:
  - NPC greets party in SESSION-7 as if they've never met (SESSION-2 introductions should establish relationship)
  - NPC forgets past sessions' events ("I hear you defeated the dragon" in SESSION-8 if that happened in SESSION-5)
  - NPC relationship arc is inconsistent (SESSION-3 friendly, SESSION-4 hostile, SESSION-5 friendly again without reason)
- Testing approach: For each major NPC, verify their dialogue arc is consistent across sessions

### Computer Game Continuity Considerations

**Route Isolation Enforcement**:
- Variables from Stealth route ($stealth_*) must never be read in Combat or Diplomacy routes
- Each route should have self-contained variable namespace
- Example: `$stealth_alarm_triggered` is set and read only within Stealth nodes (CHAPTER-3 stealth infiltration, CHAPTER-4 stealth boss). Combat nodes never reference this variable.
- Red flags:
  - CHAPTER-3 Combat node reads `$stealth_alarm_triggered` (wrong route)
  - Variable missing route prefix (`$alarm_triggered` instead of `$stealth_alarm_triggered`)
  - Route-specific variable used in non-route-specific node
- Testing approach: Search for route-prefixed variables ($stealth_*, $combat_*, $diplomacy_*) and verify they only appear in their respective route nodes

**Route Commitment Lock**:
- `playthrough_route` variable must be set exactly once in CHAPTER-2
- After CHAPTER-2, all nodes must read `playthrough_route` before branching
- Example: CHAPTER-2 node allows player to choose Stealth, Combat, or Diplomacy. Set `$playthrough_route = "stealth"`. CHAPTER-3 nodes include logic: if ($playthrough_route == "stealth") branch to Stealth infiltration; else skip.
- Red flags:
  - `$playthrough_route` set in multiple chapters
  - `$playthrough_route` modified after CHAPTER-2
  - CHAPTER-3-4 nodes don't check `$playthrough_route` before routing
- Testing approach: Verify `$playthrough_route` is set exactly once; search for modifications after CHAPTER-2; verify all post-CHAPTER-2 nodes check this variable

**Accessibility Consistency Across Routes**:
- Accessibility mode variables (colorblind_mode, audio_mode, motor_mode) must be available in ALL chapters
- Each route must support each accessibility type equally
- Example: CHAPTER-3 Stealth route includes colorblind UI overlay if colorblind_mode == true. CHAPTER-3 Combat route includes same overlay. CHAPTER-3 Diplomacy route includes same overlay.
- Red flags:
  - Accessibility mode set in CHAPTER-1 but not checked in CHAPTER-3-4
  - CHAPTER-3 Stealth nodes support colorblind mode but CHAPTER-3 Combat doesn't
  - Accessibility mode variables are route-specific instead of global
- Testing approach: Verify accessibility mode variables are global (not route-prefixed); verify all chapters read accessibility modes; verify visual/audio adjustments apply uniformly across all routes

**Chapter-to-Chapter Carry-Over**:
- Decisions made in CHAPTER-2 must logically affect CHAPTER-3-4
- Story-critical information revealed in CHAPTER-2 must be available (via variables) in CHAPTER-3-4
- Example: In CHAPTER-2, player learns the "true name" of the enemy. Dialogue in CHAPTER-4 boss fight should reference this name (via `$enemy_true_name` variable)
- Red flags:
  - CHAPTER-3 node references decision from CHAPTER-1 that was never set (variable doesn't exist)
  - CHAPTER-4 dialogue mentions knowledge player never acquired
  - CHAPTER-2 variables aren't accessible in CHAPTER-3-4 (scope issue)
- Testing approach: For each chapter, verify CHAPTER-(N+1) references to CHAPTER-N outcomes are valid

**Cross-Route Variable Conflicts**:
- Generic variables (not route-prefixed) must have consistent meaning across all routes
- Route-exclusive variables must use route prefix to avoid conflicts
- Example: `$enemy_defeated` is WRONG (generic, ambiguous which enemy). Correct: `$stealth_boss_defeated`, `$combat_boss_defeated`, `$diplomacy_boss_defeated` (each route's specific outcome)
- Red flags:
  - Generic variable name used by multiple routes with different meanings
  - Route-exclusive variable set to different values by different routes (ambiguous)
  - Variables like `$route_choice` or `$boss_defeated` (ambiguous which route/boss)
- Testing approach: Audit variable naming; ensure generic variables are truly generic (used same way everywhere); ensure route-specific variables use route prefixes

### Ruleset-Specific Continuity Checks

**D&D 5e**:
- Ability check DCs must be consistent (DC 8-20 range)
- Advantage/disadvantage states must be tracked through outcomes (e.g., if player gained advantage on Perception in CHAPTER-2, is this advantage still active in CHAPTER-3 or cleared?)
- Spell durations and conditions must be tracked (e.g., "blessed for 1 hour" set in CHAPTER-2 must expire by specific CHAPTER-3 node if "1 hour" has passed)
- Example: `$blessed_until = SESSION-4_MORNING`. If current SESSION is SESSION-5_AFTERNOON, bless is expired; remove `$blessed` flag

**Pathfinder 2e**:
- Critical success/failure outcomes must be consistent (degrees of success matter)
- Multiple critical successes on same check must compound meaningfully
- Conditions must track (frightened 1/2/3 levels, or cleared)
- Example: Two critical successes on Deception checks should provide better outcome than one success; track via `$deception_critical_count` variable

**Shadowrun 6e**:
- Karma pool and Edge pool must be tracked (decline throughout campaign)
- Matrix vs Physical separation must be maintained (hacker actions don't affect physical team and vice versa)
- Hit margin calculations must carry over (net hits from previous session may affect current session's continuation of mission)
- Example: `$karma_remaining = 15` at SESSION-3 start; players spend 3 karma; SESSION-4 start shows `$karma_remaining = 12`
