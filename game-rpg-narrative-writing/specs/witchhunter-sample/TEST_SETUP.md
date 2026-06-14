# Witchhunter Playwright Test Suite

## Overview

This directory contains a comprehensive Playwright test suite for the Witchhunter SugarCube interactive fiction game. The tests cover:

- **Game Flow**: Navigation, UI passages, character initialization
- **Dialogue System**: NPC conversations, choice branching, quest effects
- **Faction System**: Reputation tracking, tier calculations, reputation rewards
- **Spell & Combat System**: Spellbook UI, spell slots, spell availability
- **Inventory & Quests**: Quest tracking, item management, gold system

## Setup Instructions

### Prerequisites

1. **Install Node.js** (v18 or later)
   - Download from https://nodejs.org/
   - Verify installation: `node --version` and `npm --version`

2. **Compile the SugarCube game** to HTML
   - Ensure `witchhunter.html` exists in this directory
   - Use Tweego compiler: `tweego witchhunter-*.twee -o witchhunter.html`

### Installation Steps

```bash
# Navigate to the test directory
cd game-rpg-narrative-writing/specs/witchhunter-sample

# Install dependencies
npm install

# This will install:
# - @playwright/test (testing framework)
# - TypeScript (for type checking)
# - Node types (@types/node)
```

## Running Tests

### Run all tests
```bash
npm test
```

### Run tests in headed mode (see browser)
```bash
npm run test:headed
```

### Run specific test file
```bash
npx playwright test tests/game-flow.spec.ts
```

### Run tests in debug mode
```bash
npm run test:debug
```

### Run tests with UI mode (interactive)
```bash
npm run test:ui
```

## Test Files

### `helpers.ts`
Common utilities for all tests:
- `navigateToGame()` - Load the game HTML
- `getCurrentPassage()` - Get current SugarCube passage name
- `getCharacterHP()` - Get player HP (current/max)
- `getFactionRep()` - Get faction reputation and tier
- `isNPCInParty()` - Check if NPC is recruited
- `getQuestState()` - Get quest status and stage
- `getGold()` - Get current gold amount
- `clickLink()` - Navigate via link text
- `getDialogueChoiceCount()` - Count dialogue options
- `getSpellSlots()` - Get spell slot availability

### `game-flow.spec.ts`
**Tests core navigation and UI**
- Game loads and shows Start passage
- All menu items accessible (Character, Quests, Party, Spells, Factions, Inventory, World Map)
- Initial resources correct (26 HP, 30 gold)
- Location navigation works
- Intro scene displays correctly

### `dialogue.spec.ts`
**Tests dialogue system**
- Dialogue UI displays correctly
- Dialogue choices render and are clickable
- Choice effects execute (NPC recruitment, approval changes)
- Dialogue branching works
- NPC names display in dialogue
- Dialogue choice text is visible

### `faction.spec.ts`
**Tests faction reputation system**
- Factions initialize at neutral (rep 0, tier "neutral")
- Faction UI displays all visible factions
- Faction names, icons, and tiers show correctly
- Faction Dark Syndicate is hidden initially
- Reputation scores are bounded [-150, 150]
- Tier calculation is correct per reputation

### `spells-combat.spec.ts`
**Tests spell and combat systems**
- Spellbook UI displays correctly
- Spell slots track correctly
- Cantrips show as always available
- Leveled spells show slot counts
- Spell descriptions and schools visible
- Spell system integrated with main menu
- Spell slot expenditure tracked

### `inventory-quests.spec.ts`
**Tests inventory and quest tracking**
- Inventory UI displays
- Quest journal shows quest information
- Initial gold amount is correct (30)
- Gold displays in sidebar
- Quest states tracked correctly
- Active quests show in sidebar with stage information
- Inventory has interactive item buttons

## Expected Test Results

When all tests pass, you should see output like:

```
  Witchhunter Game Flow (10 tests)
    ✓ should load game and display start passage
    ✓ should display character sheet
    ✓ should display quest journal
    ✓ should display inventory
    ... (7 more)

  Dialogue System (7 tests)
    ✓ should display dialogue UI elements
    ✓ should have dialogue choices
    ✓ should execute dialogue choice effects
    ... (4 more)

  Faction System (9 tests)
    ✓ should initialize factions at neutral
    ✓ should display factions screen
    ... (7 more)

  Spell & Combat System (8 tests)
    ✓ should display spellbook UI
    ... (7 more)

  Inventory & Quests (9 tests)
    ✓ should display inventory UI
    ... (8 more)

======================== 43 passed ========================
```

## Troubleshooting

### Tests timeout
- Ensure `witchhunter.html` exists in the specs/witchhunter-sample/ directory
- Check that the HTML file is valid and loads properly
- Increase timeout in `playwright.config.ts` if needed

### Dialogue tests fail
- Verify dialogue system is compiled into the HTML
- Check that `$dialogue_registry` is initialized in StoryInit
- Ensure `.dialogue-choices` CSS class exists in the HTML

### Faction tests fail
- Verify faction variables are initialized in StoryInit
- Check that faction widgets are compiled into HTML
- Ensure faction helpers (`setup.factionTierFromScore`) are available

### NPC recruitment doesn't work
- Check that Mira's dialogue "meet" node has `$mira_in_party = true` effect
- Verify dialogue choice effects execute correctly
- Confirm NPC companion variables exist

## Compilation Checklist

Before running tests, ensure the `witchhunter.html` file includes:

- ✅ StoryInit with all faction/spell/quest/dialogue registries
- ✅ All widget passages (dialogue, faction, spell, combat widgets)
- ✅ All UI passages (CharacterSheet, InventoryUI, FactionUI, SpellsUI, etc.)
- ✅ All location passages (LOC-*)
- ✅ All node passages (NODE-*)
- ✅ D5e combat engine script tagged [script]
- ✅ StoryMenu with all sidebar links
- ✅ StoryCaption with faction/quest notifications

## Next Steps

1. **Install Node.js** if not already installed
2. **Compile witchhunter.html** using Tweego
3. **Run `npm install`** in this directory
4. **Run `npm test`** to execute all tests
5. **Review test results** and fix any failures
6. **Use `npm run test:ui`** for interactive debugging

## Configuration Files

- **package.json** - Dependencies and scripts
- **playwright.config.ts** - Playwright test configuration
- **tsconfig.json** - TypeScript compiler options
- **.gitignore** - Files to exclude from version control

## File Structure

```
witchhunter-sample/
├── package.json
├── tsconfig.json
├── playwright.config.ts
├── .gitignore
├── witchhunter.html          (compiled game - needed for tests)
├── tests/
│   ├── helpers.ts            (shared utilities)
│   ├── game-flow.spec.ts     (navigation, UI tests)
│   ├── dialogue.spec.ts      (dialogue system tests)
│   ├── faction.spec.ts       (faction system tests)
│   ├── spells-combat.spec.ts (spell & combat tests)
│   └── inventory-quests.spec.ts (inventory & quests tests)
└── dist/                     (compiled JavaScript - generated after npm run compile)
```

## References

- [Playwright Documentation](https://playwright.dev/)
- [Playwright Test Framework](https://playwright.dev/docs/intro)
- [Playwright Assertions](https://playwright.dev/docs/test-assertions)
- [SugarCube Documentation](https://www.motoslave.net/sugarcube/2/)
