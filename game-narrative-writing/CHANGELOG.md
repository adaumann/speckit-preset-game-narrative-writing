# Changelog

All notable changes to the Game Narrative Writing preset will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/), and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [1.1.0] - 2026-06-14

### Added
- **Illustration system**: `speckit.illustrate` command generates AI image prompts for scenes from outlines and character files; `speckit.background` generates environment prompts from locations and world-building; embedding of matching PNGs (`<NODE_ID>.png`) during compile via `illustrations_enabled: yes` in constitution
- **Background image system**: `speckit.background` command for environment-focused prompts (Midjourney, DALL-E 3, Firefly, Stable Diffusion)
- **Postprocessing plugin system**: `speckit.postprocessing` command generates deterministic Python scripts; `scripts/python/postprocess.py` runner discovers and executes scripts pre/post compile/export; `--postprocess-tests` in `speckit.verify` for validation (16 test cases: passage parsing, CSS/widget injection, script discovery)
- **Example postprocess scripts**: `fix_theme.py` (CSS injection), `add_headers.py` (header/footer widgets), `add_animations.py` (CSS slideIn/fadeIn)
- **CSS themes**: 6 theme templates — dark, light, and minimal for both SugarCube (`.css`) and Ink (`.html`); `speckit.theme` command for theme generation/adjustment
- **Walkthrough testing**: `--walkthrough` flag in `speckit.compile` for BFS story graph traversal; `scripts/tests/full-story-walkthrough.spec.ts` Playwright test

### Changed
- **Consolidated quality gates**: 13 overlapping commands reduced to 8 canonical commands
  - `speckit.readability` = `speckit.pacing` + `speckit.tone` (narrative flow)
  - `speckit.branching` = `speckit.complexity` + `speckit.consequences` + `speckit.agency` (branch analysis)
  - `speckit.information` = `speckit.dialogue` + `speckit.asymmetry` + `speckit.secrets` (info flow)
  - `speckit.narrative-arc` = `speckit.character` + `speckit.subplots` + `speckit.endings` (arc tracking)
  - `speckit.continuity` now includes `speckit.statemap` (state mapping)
  - `speckit.verify` now includes `speckit.checklist` (per-node quality gates)
- **Quality gates added to task phases**: `speckit.tasks.md` and `speckit.implement.md` now dispatch and schedule the 4 new consolidated commands (readability, branching, information, narrative-arc)
- **Removed leftover stubs**: Deleted 26 redirect stub files after consolidation (13 per preset)
- **Removed RAG indexing**: Stripped all `index.py`, ChromaDB, and semantic search references from constitution, plan, research, specify, and polish commands across both presets
- **Removed point-and-click engines**: Stripped all `escoria`, `ags`, and `point-and-click` references from ~80 files across both presets; deleted escoria template files
- **Cleaned preset.yml**: Fixed broken `escoria-script-template` fragment, added missing `description` fields for `research-template` and `sugarcube-character-sheet-template`
- **Updated cross-references**: `README.md`, `speckit.help.md`, `speckit.compile.md`, `speckit.revise.md`, `speckit.polish.md`, `speckit.analyze.md`, `speckit.feedback.md`, `speckit.constitution.md`, `speckit.series.md`, and all templates updated to reflect new command names

## [1.0.0] - 2026-04-25

### Added
- Initial release of the Game Narrative Writing preset
- Intermediate format: structured Markdown nodes with two-layer architecture (narrative layer + mechanics layer)
- Core commands: `speckit.specify`, `speckit.clarify`, `speckit.constitution`, `speckit.plan`, `speckit.outline`, `speckit.tasks`, `speckit.implement`, `speckit.analyze`, `speckit.status`, `speckit.checklist`, `speckit.revise`, `speckit.continuity`, `speckit.flowmap`, `speckit.export`, `speckit.brainstorm`, `speckit.feedback`, `speckit.series`, `speckit.help`
- Base templates: `constitution-template.md`, `narrative-design-doc-template.md`, `flowmap-template.md`, `node-template.md`, `node-outline-template.md`, `variables-template.md`, `mechanics-template.md`, `tasks-template.md`, `characters-template.md`, `world-building-template.md`, `endings-template.md`, `series-bible-template.md`, `glossary-template.md`, `feedback-template.md`, `agent-file-template.md`
- Tier 1 mechanic hooks: `flag`, `counter`, `visited`, `inventory`, `timer`, `trust`, `currency`, `npc_state`, `ending_condition`
- Tier 2 mechanic hook stubs: `knowledge`, `faction`, `location_state`, `object_state`, `choice_memory`, `clue`
- Export targets: Twine/Sugarcube (`.twee` Twee 3) and Ink (`.ink`)
- Hook translation layer: Tier 1 hooks → Sugarcube macros / Ink variables
- Compatibility warnings for hooks unsupported by the selected export target
- POV support: `player_perspective` field in game bible (`second-person`, `third-person`, `first-person`, `switching`); `pov` variable in variables registry for switching mode
- `speckit.continuity` POV drift check: validates prose person-agreement against declared `$pov` value per branch
- Series support: `series-bible-template.md` with carry-over variable registry, canonical import state, ending canon table, NPC survival registry
- `speckit.series` command: carry-over variable validation, ending canon consistency, import questionnaire scaffold
- `scripts/python/export.py`: Twee 3/Sugarcube emitter, Ink emitter, hook translation layer, compatibility warnings
- NPC-focused `characters-template.md`: trust state thresholds, dialogue register per state, branch behavior map, bark lines, knowledge state

### Roadmap
- v1.1: Yarn Spinner export (Unity/Godot dialogue)
- v1.2: Ren'Py export (visual novels)
- v1.3: Dialogic JSON export (Godot)
- v1.4: Ren'Py export (visual novels)
- v2.0: Tier 2 hook full export support
- Separate preset: Parser IF (Inform 7 / TADS)
