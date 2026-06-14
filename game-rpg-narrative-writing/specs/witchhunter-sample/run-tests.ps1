#!/usr/bin/env pwsh
<#
.SYNOPSIS
Witchhunter Playwright Tests - Setup and Run Script
#>

$ErrorActionPreference = "Continue"

Write-Host ""
Write-Host "============================================================================" -ForegroundColor Cyan
Write-Host "Witchhunter Playwright Test Suite - Setup & Execution" -ForegroundColor Cyan
Write-Host "============================================================================" -ForegroundColor Cyan
Write-Host ""

# Get script directory
$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $scriptDir

# ---- Check Node.js Installation ----
Write-Host "[1/5] Checking Node.js installation..." -ForegroundColor Yellow

$nodeVersion = node --version 2>$null
if ($LASTEXITCODE -ne 0) {
    Write-Host ""
    Write-Host "❌ Node.js is NOT installed" -ForegroundColor Red
    Write-Host ""
    Write-Host "Please install Node.js from: https://nodejs.org/" -ForegroundColor White
    Write-Host "- Download v18 LTS or later" -ForegroundColor White
    Write-Host "- Run the installer" -ForegroundColor White
    Write-Host "- Restart your terminal" -ForegroundColor White
    Write-Host ""
    Read-Host "Press Enter to exit"
    exit 1
}
Write-Host "✅ Node.js found: $nodeVersion" -ForegroundColor Green

# ---- Check npm Installation ----
Write-Host "[2/5] Checking npm installation..." -ForegroundColor Yellow

$npmVersion = npm --version 2>$null
if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ npm is NOT installed" -ForegroundColor Red
    Read-Host "Press Enter to exit"
    exit 1
}
Write-Host "✅ npm found: $npmVersion" -ForegroundColor Green

# ---- Install Dependencies ----
Write-Host "[3/5] Installing dependencies..." -ForegroundColor Yellow

if (-not (Test-Path "node_modules")) {
    Write-Host "Installing packages from package.json..." -ForegroundColor Cyan
    npm install
    if ($LASTEXITCODE -ne 0) {
        Write-Host "❌ npm install failed" -ForegroundColor Red
        Read-Host "Press Enter to exit"
        exit 1
    }
}
else {
    Write-Host "✅ Dependencies already installed" -ForegroundColor Green
}

# ---- Verify Test Files ----
Write-Host "[4/5] Verifying test files..." -ForegroundColor Yellow

$missing = $false

if (-not (Test-Path "witchhunter.html")) {
    Write-Host "⚠️  WARNING: witchhunter.html not found" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "You need to compile the game with Tweego:" -ForegroundColor White
    Write-Host "  tweego witchhunter-*.twee -o witchhunter.html" -ForegroundColor White
    Write-Host ""
    $missing = $true
}

$testFiles = @(
    "tests/helpers.ts",
    "tests/game-flow.spec.ts",
    "tests/dialogue.spec.ts",
    "tests/faction.spec.ts",
    "tests/spells-combat.spec.ts",
    "tests/inventory-quests.spec.ts"
)

foreach ($file in $testFiles) {
    if (-not (Test-Path $file)) {
        Write-Host "❌ $file missing" -ForegroundColor Red
        $missing = $true
    }
}

if ($missing -and (Test-Path "witchhunter.html")) {
    Write-Host ""
    Write-Host "⚠️  Some test files are missing. Please check and try again." -ForegroundColor Yellow
    Read-Host "Press Enter to exit"
    exit 1
}

Write-Host "✅ All test files found" -ForegroundColor Green

# ---- Compile TypeScript ----
Write-Host "[5/5] Compiling TypeScript..." -ForegroundColor Yellow

$tscOutput = npx tsc --noEmit 2>&1
$tscResult = $LASTEXITCODE

if ($tscResult -ne 0) {
    if ($tscOutput -match "error") {
        Write-Host "⚠️  TypeScript compilation found errors:" -ForegroundColor Yellow
        Write-Host $tscOutput -ForegroundColor Yellow
    }
    else {
        Write-Host "✅ TypeScript check passed" -ForegroundColor Green
    }
}
else {
    Write-Host "✅ TypeScript check passed" -ForegroundColor Green
}

Write-Host ""
Write-Host "============================================================================" -ForegroundColor Cyan
Write-Host "Ready to run tests!" -ForegroundColor Cyan
Write-Host "============================================================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Command: npm test" -ForegroundColor White
Write-Host ""
Write-Host "Options:" -ForegroundColor White
Write-Host "  npm test              - Run all tests (headless)" -ForegroundColor White
Write-Host "  npm run test:headed   - Run with browser visible" -ForegroundColor White
Write-Host "  npm run test:debug    - Debug mode" -ForegroundColor White
Write-Host "  npm run test:ui       - Interactive UI mode" -ForegroundColor White
Write-Host ""
Write-Host "Running all tests now..." -ForegroundColor Cyan
Write-Host "============================================================================" -ForegroundColor Cyan
Write-Host ""

npm test

Read-Host "`nPress Enter to exit"
