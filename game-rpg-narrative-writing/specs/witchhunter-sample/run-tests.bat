@echo off
REM ============================================================================
REM Witchhunter Playwright Tests - Setup and Run Script
REM ============================================================================

setlocal enabledelayedexpansion

cd /d "%~dp0"

echo.
echo ============================================================================
echo Witchhunter Playwright Test Suite - Setup & Execution
echo ============================================================================
echo.

REM ---- Check Node.js Installation ----
echo [1/5] Checking Node.js installation...
node --version >nul 2>&1
if errorlevel 1 (
    echo.
    echo ❌ Node.js is NOT installed
    echo.
    echo Please install Node.js from: https://nodejs.org/
    echo - Download v18 LTS or later
    echo - Run the installer
    echo - Restart this terminal
    echo.
    echo After installing Node.js, run this script again.
    pause
    exit /b 1
)

for /f "tokens=*" %%i in ('node --version') do set NODE_VERSION=%%i
echo ✅ Node.js found: %NODE_VERSION%

REM ---- Check npm Installation ----
echo [2/5] Checking npm installation...
npm --version >nul 2>&1
if errorlevel 1 (
    echo ❌ npm is NOT installed
    pause
    exit /b 1
)

for /f "tokens=*" %%i in ('npm --version') do set NPM_VERSION=%%i
echo ✅ npm found: %NPM_VERSION%

REM ---- Install Dependencies ----
echo [3/5] Installing dependencies...
if not exist "node_modules\" (
    echo Installing packages from package.json...
    call npm install
    if errorlevel 1 (
        echo ❌ npm install failed
        pause
        exit /b 1
    )
) else (
    echo ✅ Dependencies already installed
)

REM ---- Verify Test Files ----
echo [4/5] Verifying test files...
set MISSING=0

if not exist "witchhunter.html" (
    echo ⚠️  WARNING: witchhunter.html not found
    echo.
    echo You need to compile the game with Tweego:
    echo   tweego witchhunter-*.twee -o witchhunter.html
    echo.
    set MISSING=1
)

if not exist "tests\helpers.ts" (
    echo ❌ tests\helpers.ts missing
    set MISSING=1
)
if not exist "tests\game-flow.spec.ts" (
    echo ❌ tests\game-flow.spec.ts missing
    set MISSING=1
)
if not exist "tests\dialogue.spec.ts" (
    echo ❌ tests\dialogue.spec.ts missing
    set MISSING=1
)
if not exist "tests\faction.spec.ts" (
    echo ❌ tests\faction.spec.ts missing
    set MISSING=1
)
if not exist "tests\spells-combat.spec.ts" (
    echo ❌ tests\spells-combat.spec.ts missing
    set MISSING=1
)
if not exist "tests\inventory-quests.spec.ts" (
    echo ❌ tests\inventory-quests.spec.ts missing
    set MISSING=1
)

if %MISSING%==1 (
    echo.
    echo ⚠️  Some required files are missing. Please check and try again.
    pause
    exit /b 1
)

echo ✅ All test files found

REM ---- Compile TypeScript ----
echo [5/5] Compiling TypeScript...
call npx tsc --noEmit
if errorlevel 1 (
    echo ⚠️  TypeScript compilation found errors (non-fatal)
    echo Attempting to run tests anyway...
)

echo.
echo ============================================================================
echo Ready to run tests!
echo ============================================================================
echo.
echo Command: npm test
echo.
echo Options:
echo   npm test              - Run all tests (headless)
echo   npm run test:headed   - Run with browser visible
echo   npm run test:debug    - Debug mode
echo   npm run test:ui       - Interactive UI mode
echo.
echo Running all tests now...
echo ============================================================================
echo.

call npm test

pause
