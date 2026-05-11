# Quick Start Guide — Witchhunter Playwright Tests

## 🚀 TL;DR — Get Running in 5 Steps

### 1. Install Node.js
Download from https://nodejs.org/ (v18 or later)

### 2. Verify Game HTML Exists
```bash
# Ensure this file exists:
game-rpg-narrative-writing/specs/witchhunter-sample/witchhunter.html
```
If not, compile using Tweego:
```bash
tweego witchhunter-*.twee -o witchhunter.html
```

### 3. Install Dependencies
```bash
cd game-rpg-narrative-writing/specs/witchhunter-sample
npm install
```

### 4. Run Tests
```bash
npm test
```

### 5. View Results
- Test output in terminal
- Detailed report: `npx playwright show-report`

---

## 📋 Checklist Before Running Tests

Before executing `npm test`, verify:

- ✅ Node.js installed (`node --version` returns v18+)
- ✅ npm installed (`npm --version` returns 9+)
- ✅ `witchhunter.html` exists in specs/witchhunter-sample/
- ✅ HTML file is valid and loads in browser
- ✅ All Twee files compiled into HTML (use Tweego)
- ✅ package.json exists with test scripts
- ✅ playwright.config.ts configured
- ✅ tests/ directory has .spec.ts files
- ✅ tsconfig.json configured

---

## 🔧 Common Commands

```bash
# Navigate to test directory
cd game-rpg-narrative-writing/specs/witchhunter-sample

# Install dependencies
npm install

# Run ALL tests
npm test

# Run tests in browser (watch mode)
npm run test:headed

# Debug a specific test
npx playwright test tests/dialogue.spec.ts --debug

# Interactive test UI
npm run test:ui

# Show test report
npx playwright show-report

# Check TypeScript syntax
npm run compile

# Run only tests matching pattern
npx playwright test --grep "dialogue"
```

---

## 📊 Expected Output

When tests pass:

```
======================== test session starts =========================

 Chromium ✓  Firefox ✓  WebKit ✓

 Witchhunter Game Flow
   ✓ should load game and display start passage (1.2s)
   ✓ should display character sheet (1.1s)
   ✓ should display quest journal (0.9s)
   ✓ should display inventory (0.8s)
   ... (10 total)

 Dialogue System
   ✓ should display dialogue UI elements (2.1s)
   ✓ should have dialogue choices (0.7s)
   ... (7 total)

 Faction System
   ✓ should initialize factions at neutral (0.6s)
   ... (9 total)

 Spell & Combat System
   ✓ should display spellbook UI (0.9s)
   ... (8 total)

 Inventory & Quests
   ✓ should display inventory UI (0.8s)
   ... (9 total)

===================== 43 passed (45.2s) =====================
```

---

## 🐛 Troubleshooting

### Problem: "npm command not found"
**Solution**: Install Node.js from https://nodejs.org/

### Problem: "witchhunter.html not found"
**Solution**: 
1. Ensure you're in the correct directory
2. Compile with Tweego: `tweego witchhunter-*.twee -o witchhunter.html`
3. Verify file exists: `ls -la witchhunter.html`

### Problem: Tests timeout
**Solution**:
1. Increase timeout in playwright.config.ts
2. Ensure HTML loads: Open in browser manually
3. Check HTML file size (should be >100KB)

### Problem: Dialogue tests fail
**Solution**:
1. Verify dialogue registry exists in StoryInit
2. Check that `.dialogue-choices` CSS class is defined
3. Ensure dialogue widgets compiled into HTML

### Problem: Faction tests fail
**Solution**:
1. Check StoryInit has faction registry
2. Verify faction widgets exist
3. Ensure helper functions in HTML

### Problem: "Port already in use"
**Solution**: Tests use file:// protocol (no port needed)

---

## 📁 File Structure

```
witchhunter-sample/
├── package.json                    ← Dependencies
├── tsconfig.json                   ← TypeScript config
├── playwright.config.ts            ← Test framework config
├── witchhunter.html               ← Compiled game (REQUIRED)
├── tests/
│   ├── helpers.ts                 ← Shared utilities
│   ├── game-flow.spec.ts          ← 10 UI tests
│   ├── dialogue.spec.ts           ← 7 dialogue tests
│   ├── faction.spec.ts            ← 9 faction tests
│   ├── spells-combat.spec.ts      ← 8 spell tests
│   └── inventory-quests.spec.ts   ← 9 inventory tests
├── dist/                          ← Compiled JS (auto-generated)
└── test-results/                  ← Test artifacts (auto-generated)
```

---

## 🎯 Test Coverage

| System | Tests | Status |
|--------|-------|--------|
| Game Flow | 10 | ✅ Navigation, UI, resources |
| Dialogue | 7 | ✅ NPC conversations, choices |
| Factions | 9 | ✅ Reputation, tiers, rewards |
| Spells | 8 | ✅ Spellbook, slots, UI |
| Inventory | 9 | ✅ Items, quests, gold |
| **TOTAL** | **43** | **All systems** |

---

## 🔗 Key Links

- [Playwright Docs](https://playwright.dev/)
- [Test Framework Guide](https://playwright.dev/docs/intro)
- [Assertions Reference](https://playwright.dev/docs/test-assertions)
- [SugarCube Docs](https://www.motoslave.net/sugarcube/2/)

---

## 💡 Tips & Tricks

### Debugging a Failed Test
```bash
# Run with browser visible
npx playwright test tests/dialogue.spec.ts --headed

# Debug mode (step through)
npx playwright test tests/dialogue.spec.ts --debug

# Show trace of what happened
npx playwright test tests/dialogue.spec.ts --trace on
npx playwright show-trace trace.zip
```

### Run Specific Test Pattern
```bash
# Only dialogue tests
npx playwright test --grep "Dialogue"

# Only faction tests starting with "should initialize"
npx playwright test --grep "should initialize"
```

### Parallel vs Sequential
```bash
# Run in parallel (default)
npm test

# Run one at a time
npx playwright test --workers 1
```

### Generate HTML Report
```bash
npm test
npx playwright show-report
```

---

## ✨ Next Steps After Tests Pass

1. **Review Coverage**: Check TEST_SUMMARY.md for all tested scenarios
2. **Fix Failures**: Use test results to debug game logic
3. **Expand Tests**: Add tests for new features
4. **CI Integration**: Add `npm test` to your build pipeline
5. **Performance**: Track test runtime and optimize

---

## 📝 Creating New Tests

### Template
```typescript
import { test, expect } from '@playwright/test';
import { navigateToGame, getCurrentPassage } from './helpers';

test.describe('Feature Name', () => {
  test('should verify behavior', async ({ page }) => {
    await navigateToGame(page);
    // Your test here
    expect(something).toBe(expected);
  });
});
```

### Add Custom Helper
```typescript
// In helpers.ts
export async function myHelper(page: Page): Promise<string> {
  return await page.evaluate(() => {
    const state = (window as any).State.variables;
    return state.$myVariable || '';
  });
}
```

---

## 🎓 Learning Resources

- **Playwright Test Tutorial**: https://playwright.dev/docs/writing-tests
- **SugarCube State Access**: `(window).State.variables`
- **Passage Manipulation**: `(window).State.passage.name`
- **DOM Selection**: Playwright uses CSS selectors

---

**Ready to test? Run `npm install && npm test` 🚀**
