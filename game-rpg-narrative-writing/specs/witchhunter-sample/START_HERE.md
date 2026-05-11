# 🎮 START HERE - Run Witchhunter Tests

## ⚡ Super Quick Start (< 5 minutes)

### Step 1: Install Node.js
**Download**: https://nodejs.org/ (v18 LTS)

After installing, restart your terminal and verify:
```powershell
node --version    # Should show v18.x or higher
npm --version     # Should show 9.x or higher
```

### Step 2: Run Tests
```powershell
cd game-rpg-narrative-writing/specs/witchhunter-sample
./run-tests.ps1
```

### That's It! 🎉
Tests will run automatically. You'll see results in your terminal.

---

## 📱 Windows Users - Which Command?

**PowerShell (Recommended):**
```powershell
./run-tests.ps1
```

**Command Prompt:**
```cmd
run-tests.bat
```

**Manual (All Systems):**
```powershell
npm install
npm test
```

---

## 📊 What to Expect

### Installation First Time
- npm install: 30-60 seconds
- Dependencies: ~300 MB

### Test Execution
- Total time: 45-60 seconds
- Tests: 43 total
- Browsers: Chromium, Firefox, WebKit (all run automatically)

### Success Output
```
✅ 43 passed (47.3s)
```

---

## 🎯 Tests Run For You

✅ **Game Flow** (10 tests)
- Does the game load?
- Can you access all screens?
- Do initial resources work?

✅ **Dialogue** (7 tests)
- Do conversations work?
- Can you pick dialogue choices?
- Do choices have effects?

✅ **Factions** (9 tests)
- Does reputation system work?
- Are tiers calculated correctly?
- Does UI display properly?

✅ **Spells** (8 tests)
- Does spellbook display?
- Are spell slots tracked?
- Do cantrips work?

✅ **Inventory** (9 tests)
- Does inventory work?
- Can you track quests?
- Is gold system functional?

---

## 🆘 Troubleshooting

**Problem**: "node command not found"  
**Fix**: Install Node.js from https://nodejs.org/ and restart terminal

**Problem**: "Tests timeout"  
**Fix**: Run again, usually works on retry

**Problem**: "witchhunter.html not found"  
**Fix**: Already exists ✅ in the same directory

---

## 📚 Need More Help?

| Need | Read |
|------|------|
| Quick commands | QUICKSTART.md |
| Detailed setup | TEST_SETUP.md |
| Test details | TEST_SUMMARY.md |
| All steps explained | README_TESTS.md |

---

## ✨ Most Important Commands

```powershell
# Run tests (headless - no browser window)
npm test

# Run tests with browser visible
npm run test:headed

# Debug mode (step through)
npm run test:debug

# Interactive mode
npm run test:ui

# View test report
npx playwright show-report
```

---

## 🚀 Ready? Run This Now:

```powershell
cd game-rpg-narrative-writing/specs/witchhunter-sample
./run-tests.ps1
```

**Next: All 43 tests will run automatically! ✅**
