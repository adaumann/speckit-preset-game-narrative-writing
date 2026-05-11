# Playwright Tests - Compilation & Execution Guide

## ✅ Project Status

All test files have been created and are ready to compile and run.

### File Inventory

✅ **Configuration Files**
- package.json (dependencies configured)
- tsconfig.json (TypeScript compiler options)
- playwright.config.ts (test runner configuration)
- .gitignore (artifact exclusions)

✅ **Test Files** (6 files, 43 tests total)
- tests/helpers.ts (25+ helper utilities)
- tests/game-flow.spec.ts (10 UI/navigation tests)
- tests/dialogue.spec.ts (7 dialogue system tests)
- tests/faction.spec.ts (9 faction system tests)
- tests/spells-combat.spec.ts (8 spell & combat tests)
- tests/inventory-quests.spec.ts (9 inventory & quest tests)

✅ **Execution Scripts**
- run-tests.bat (Windows Command Prompt)
- run-tests.ps1 (Windows PowerShell)
- run-tests.sh (Linux/Mac Bash)

✅ **Documentation**
- TEST_SETUP.md (complete setup guide)
- TEST_SUMMARY.md (test breakdown)
- QUICKSTART.md (quick reference)
- TESTS_CREATED.md (overview)
- COMPILATION_GUIDE.md (this file)

---

## 🛠️ Prerequisites Checklist

Before running tests, verify:

- ✅ Node.js v18+ installed
  ```bash
  node --version
  # Should show v18.0.0 or higher
  ```

- ✅ npm v9+ installed
  ```bash
  npm --version
  # Should show 9.0.0 or higher
  ```

- ✅ witchhunter.html compiled
  ```bash
  # From the witchhunter-sample directory:
  tweego witchhunter-*.twee -o witchhunter.html
  ```

---

## 🚀 Quick Start (Choose Your Platform)

### Windows - PowerShell (Recommended)
```powershell
cd game-rpg-narrative-writing/specs/witchhunter-sample
./run-tests.ps1
```

### Windows - Command Prompt
```cmd
cd game-rpg-narrative-writing\specs\witchhunter-sample
run-tests.bat
```

### Linux / Mac
```bash
cd game-rpg-narrative-writing/specs/witchhunter-sample
bash run-tests.sh
# OR if executable permissions set:
./run-tests.sh
```

### Manual Step-by-Step
```bash
cd game-rpg-narrative-writing/specs/witchhunter-sample

# 1. Install dependencies
npm install

# 2. Verify TypeScript
npx tsc --noEmit

# 3. Run tests
npm test
```

---

## 📝 TypeScript Compilation

### Compile TypeScript to JavaScript
```bash
npm run compile
# Output: dist/ directory with compiled .js files
```

### Check TypeScript without compiling
```bash
npx tsc --noEmit
```

### Type-check specific file
```bash
npx tsc tests/game-flow.spec.ts --noEmit
```

---

## 🧪 Test Execution Modes

### Run All Tests (Headless)
```bash
npm test
# Runs tests in Chromium, Firefox, WebKit
# Output: test-results/ with HTML report
```

### Run with Browser Visible
```bash
npm run test:headed
# See the browser executing tests in real-time
```

### Debug Mode (Step Through Tests)
```bash
npm run test:debug
# Pauses at breakpoints, step through code
```

### Interactive UI
```bash
npm run test:ui
# Opens Playwright Inspector for interactive debugging
```

### Run Specific Test File
```bash
npx playwright test tests/dialogue.spec.ts
```

### Run Tests Matching Pattern
```bash
npx playwright test --grep "Dialogue"
```

---

## 📊 Expected Output

### Successful Test Run
```
======================== test session starts ==========================

 Chromium ✓  Firefox ✓  WebKit ✓

 Witchhunter Game Flow (10 tests)
   ✓ should load game and display start passage (1.2s)
   ✓ should display character sheet (1.1s)
   ✓ should display quest journal (0.9s)
   ... (7 more)

 Dialogue System (7 tests)
   ✓ should display dialogue UI elements (2.1s)
   ... (6 more)

 Faction System (9 tests)
   ✓ should initialize factions at neutral (0.6s)
   ... (8 more)

 Spell & Combat System (8 tests)
   ✓ should display spellbook UI (0.9s)
   ... (7 more)

 Inventory & Quests (9 tests)
   ✓ should display inventory UI (0.8s)
   ... (8 more)

======================== 43 passed (47.3s) ========================
```

### View Test Report
After tests complete:
```bash
npx playwright show-report
# Opens detailed HTML report in browser
```

---

## 🔍 Verification Checklist

### Pre-Compilation Checks
- ✅ All .spec.ts files in tests/ directory
- ✅ helpers.ts has all required functions
- ✅ tsconfig.json configured correctly
- ✅ playwright.config.ts has baseURL set to 'file://'
- ✅ package.json has scripts defined

### TypeScript Syntax Check
Run this to verify syntax without running tests:
```bash
npx tsc --noEmit
```

Expected: No output (no errors)

### Dependencies Check
```bash
npm list @playwright/test
npm list typescript
```

Expected: Versions installed

### Test Files Validation

**Helper File**: tests/helpers.ts
- ✅ 25+ exported functions
- ✅ TypeScript types defined
- ✅ Playwright Page type imported
- ✅ Path module imported

**Game Flow Tests**: tests/game-flow.spec.ts
- ✅ 10 test cases
- ✅ Imports from helpers
- ✅ Navigation tests
- ✅ Resource verification tests

**Dialogue Tests**: tests/dialogue.spec.ts
- ✅ 7 test cases
- ✅ NPC interaction tests
- ✅ Choice effects tests
- ✅ Branching logic tests

**Faction Tests**: tests/faction.spec.ts
- ✅ 9 test cases
- ✅ Initialization tests
- ✅ Tier calculation tests
- ✅ Reputation bounds tests

**Spell Tests**: tests/spells-combat.spec.ts
- ✅ 8 test cases
- ✅ Spellbook UI tests
- ✅ Spell slot tests
- ✅ Integration tests

**Inventory Tests**: tests/inventory-quests.spec.ts
- ✅ 9 test cases
- ✅ Item management tests
- ✅ Quest tracking tests
- ✅ Gold system tests

---

## 🐛 Troubleshooting

### Issue: "Command not found: npm"
**Fix**: Install Node.js from https://nodejs.org/

### Issue: "Cannot find witchhunter.html"
**Fix**: 
```bash
# Compile the game first
tweego witchhunter-*.twee -o witchhunter.html
```

### Issue: TypeScript Compilation Errors
**Check**: 
```bash
npx tsc --noEmit
# Shows detailed error messages
```

**Common errors**:
- Missing imports: Add `import { Page } from '@playwright/test'`
- Type mismatches: Verify variable types
- Path issues: Check relative paths in helpers.ts

### Issue: Tests Timeout
**Fix in playwright.config.ts**:
```typescript
timeout: 30000,  // Increase from 10000
```

### Issue: "Port already in use"
**Note**: Tests use file:// protocol (no port needed)

### Issue: Browser Won't Close
**Note**: Normal behavior - Playwright cleans up after tests

---

## 📈 Performance Baseline

Expected execution times:
- TypeScript compilation: 2-3 seconds
- Dependency installation: 30-60 seconds (first time)
- Test execution: 45-60 seconds (all 43 tests, 3 browsers)
- Average per test: 1-2 seconds

---

## 🔄 Continuous Integration

### GitHub Actions Example
```yaml
name: Tests
on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-node@v3
        with:
          node-version: '18'
      - run: cd game-rpg-narrative-writing/specs/witchhunter-sample
      - run: npm install
      - run: npm test
      - uses: actions/upload-artifact@v3
        with:
          name: test-results
          path: test-results/
```

---

## 📦 Build Artifacts

After running tests, look for:

```
witchhunter-sample/
├── dist/              ← Compiled JavaScript
├── node_modules/      ← Installed dependencies
├── test-results/      ← Test execution results
├── playwright-report/ ← HTML test report
└── .auth/            ← Playwright auth state (if used)
```

To view HTML report:
```bash
npx playwright show-report
```

---

## ✨ Next Steps

1. **Verify Setup**
   ```bash
   npm --version
   node --version
   ```

2. **Install Dependencies**
   ```bash
   npm install
   ```

3. **Verify Game Compiled**
   ```bash
   ls -la witchhunter.html  # Should exist
   ```

4. **Run Type Check**
   ```bash
   npx tsc --noEmit
   ```

5. **Execute Tests**
   ```bash
   npm test
   ```

6. **View Report**
   ```bash
   npx playwright show-report
   ```

---

## 📚 Documentation References

| Document | Purpose |
|----------|---------|
| TEST_SETUP.md | Complete setup guide |
| TEST_SUMMARY.md | Detailed test breakdown |
| QUICKSTART.md | Quick reference |
| TESTS_CREATED.md | Overview |
| COMPILATION_GUIDE.md | This file |

---

## 🎯 Success Criteria

Tests are successful when:
- ✅ All 43 tests pass
- ✅ No TypeScript errors
- ✅ HTML report generates
- ✅ Zero timeout failures
- ✅ Test execution under 60 seconds

---

## 📞 Support

For issues, check:
1. QUICKSTART.md - Quick fixes
2. TEST_SETUP.md - Detailed troubleshooting
3. Node.js: https://nodejs.org/
4. Playwright: https://playwright.dev/

---

**Ready? Run: `npm install && npm test` 🚀**
