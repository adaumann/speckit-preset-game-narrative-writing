# Spec Kit Game Narrative Writing Preset

A [Spec Kit](https://github.com/github/spec-kit) preset for game narrative design and interactive storytelling.

It adapts the Spec-Driven Development workflow for game narratives: features become story mechanics, specs become narrative briefs, plans become story maps, and tasks become dialogue and scene-writing tasks. Supports branching narratives, player agency systems, state machines, and interactive dialogue trees.

---

## Contents

```
game-narrative-writing/   ← The installable preset
```

The preset directory contains:

- `preset.yml` — manifest consumed by `specify preset add`
- `commands/` — AI slash commands for narrative design, dialogue writing, and story structure
- `templates/` — Story document templates for characters, world-building, mechanics, dialogue, and more
- `scripts/` — Validation and compilation scripts for story outputs

---

## Full Documentation

See **[game-narrative-writing/README.md](game-narrative-writing/README.md)** for:

- Quick Start guide
- Complete commands reference
- Templates reference
- Tutorials (narrative design, dialogue writing, state machines, dialogue trees)
- Branching narrative support
- Player agency and consequence systems

---

## Installation

Requires [Spec Kit](https://github.com/github/spec-kit) >= 0.5.0.

```bash
specify preset add --from https://github.com/adaumann/speckit-preset-game-narrative-writing/archive/refs/tags/v1.0.0.zip
```

Or for local development:

```bash
specify preset add --dev /path/to/speckit-preset-game-narrative-writing/game-narrative-writing
```

---

## License

MIT — see [game-narrative-writing/LICENSE](game-narrative-writing/LICENSE).
