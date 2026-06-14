# Spec Kit Game Narrative Writing Preset

A [Spec Kit](https://github.com/github/spec-kit) preset for game narrative design and interactive storytelling.

It adapts the Spec-Driven Development workflow for game narratives: features become story mechanics, specs become narrative briefs, plans become story maps, and tasks become dialogue and scene-writing tasks. Supports branching narratives, player agency systems, state machines, and interactive dialogue trees.

---

## Contents

This package includes **two separate presets** for different use cases:

```
speckit-preset-game-narrative-writing/
├── game-narrative-writing/          ← Generic narrative design
│   └── For choice-based stories, interactive fiction, branching narratives
│
└── game-rpg-narrative-writing/      ← RPG campaign design (NEW)
    └── For tabletop RPGs with mechanics (D&D 5e, PBTA, FATE, Blades)
```

---

### 1. Generic Narrative Writing Preset

**For:** Choice-based storytelling, interactive fiction, branching narratives, point-and-click adventures

**Contains:**
- Story structure templates (spec, plan, outline, variables, endings)
- Dialogue and character design templates
- Mechanics for branching, state management, dialogue trees
- Generic validation and compilation

**See:** [game-narrative-writing/README.md](game-narrative-writing/README.md)

---

### 2. RPG Campaign Writing Preset

**For:** Tabletop RPG campaigns with mechanics-driven narrative

**Contains:**
- D&D 5e campaign templates (15-session structure, 290+ nodes)
- Companion system with approval tracking
- Faction system with reputation mechanics
- Skill check system with DC scaling
- Seven ending paths with lock timing
- RPG-specific validation tools
- Support for multiple systems (D&D 5e, PBTA, FATE, Blades in the Dark)

**See:** [game-rpg-narrative-writing/README.md](game-rpg-narrative-writing/README.md)

---

## Installation

Requires [Spec Kit](https://github.com/github/spec-kit) >= 0.5.0.

### Install for Narrative Writing

```bash
specify preset add --from https://github.com/adaumann/speckit-preset-game-narrative-writing/archive/refs/tags/v1.0.0.zip game-narrative-writing
```

Or for local development:

```bash
specify preset add --dev /path/to/speckit-preset-game-narrative-writing/game-narrative-writing
```

### Install for RPG Campaign Design

```bash
specify preset add --from https://github.com/adaumann/speckit-preset-game-narrative-writing/archive/refs/tags/v1.0.0.zip game-rpg-narrative-writing
```

Or for local development:

```bash
specify preset add --dev /path/to/speckit-preset-game-narrative-writing/game-rpg-narrative-writing
```

### Install Both Presets

```bash
specify preset add --from https://github.com/adaumann/speckit-preset-game-narrative-writing/archive/refs/tags/v1.0.0.zip
```

This installs both presets, allowing you to choose the right one for each project.

---

## License

MIT — see [game-narrative-writing/LICENSE](game-narrative-writing/LICENSE).
