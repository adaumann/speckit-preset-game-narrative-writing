# Changelog

All notable changes to the Game Narrative Writing preset will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/), and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

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
- v1.4: AGS `.asc` export (adventure games)
- v1.5: Escoria export (SCUMM-style Godot adventures)
- v2.0: Tier 2 hook full export support
- Separate preset: Parser IF (Inform 7 / TADS)
