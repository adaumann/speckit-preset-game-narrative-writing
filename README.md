# Spec Kit Game Narrative Writing Preset

A [Spec Kit](https://github.com/github/spec-kit) preset for game narrative design and interactive storytelling.

It adapts the Spec-Driven Development workflow for game narratives: features become story mechanics, specs become narrative briefs, plans become story maps, and tasks become dialogue and scene-writing tasks. Supports branching narratives, player agency systems, state machines, and interactive dialogue trees.

---

## Contents

```
speckit-preset-game-narrative-writing/
└── game-narrative-writing/          ← Game narrative design
    └── For choice-based stories, interactive fiction, branching narratives
```

**Full documentation:** [game-narrative-writing/README.md](game-narrative-writing/README.md)

---

## Installation

Requires [Spec Kit](https://github.com/github/spec-kit) >= 0.5.0.

### Install for Narrative Writing

```bash
specify preset add --from https://github.com/adaumann/speckit-preset-game-narrative-writing/archive/refs/tags/v1.1.0/V1.1.0-import.zip

```

Or for local development:

```bash
specify preset add --dev /path/to/speckit-preset-game-narrative-writing/game-narrative-writing
```

---

## License

MIT — see [game-narrative-writing/LICENSE](game-narrative-writing/LICENSE).
