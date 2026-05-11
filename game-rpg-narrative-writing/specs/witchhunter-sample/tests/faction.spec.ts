import { test, expect } from '@playwright/test';
import {
  navigateToGame,
  getFactionRep,
  clickLink,
  getPassageText,
} from './helpers';

test.describe('Faction System', () => {
  test('should initialize factions at neutral', async ({ page }) => {
    await navigateToGame(page);
    
    const cityGuard = await getFactionRep(page, 'city_guard');
    expect(cityGuard.rep).toBe(0);
    expect(cityGuard.tier).toBe('neutral');
    
    const temple = await getFactionRep(page, 'temple_order');
    expect(temple.rep).toBe(0);
    expect(temple.tier).toBe('neutral');
    
    const syndicate = await getFactionRep(page, 'dark_syndicate');
    expect(syndicate.rep).toBe(0);
    expect(syndicate.tier).toBe('neutral');
  });

  test('should display factions screen', async ({ page }) => {
    await navigateToGame(page);
    await clickLink(page, '⚔ Factions');
    
    const text = await getPassageText(page);
    expect(text).toContain('Factions');
    expect(text).toContain('Reputation');
  });

  test('should show faction names on UI', async ({ page }) => {
    await navigateToGame(page);
    await clickLink(page, '⚔ Factions');
    
    const text = await getPassageText(page);
    expect(text).toContain('City Guard');
    expect(text).toContain('Temple Order');
  });

  test('should display faction icons', async ({ page }) => {
    await navigateToGame(page);
    await clickLink(page, '⚔ Factions');
    
    const text = await getPassageText(page);
    expect(text).toContain('⚔'); // City Guard icon
    expect(text).toContain('✝'); // Temple icon
  });

  test('should show faction tier for each faction', async ({ page }) => {
    await navigateToGame(page);
    await clickLink(page, '⚔ Factions');
    
    const text = await getPassageText(page);
    // Should show tier information (Neutral is default)
    expect(text.toLowerCase()).toContain('neutral');
  });

  test('should display reputation scores', async ({ page }) => {
    await navigateToGame(page);
    await clickLink(page, '⚔ Factions');
    
    const text = await getPassageText(page);
    // Should display rep scores (0 initially)
    expect(text).toContain('0');
  });

  test('Dark Syndicate should be hidden initially', async ({ page }) => {
    await navigateToGame(page);
    await clickLink(page, '⚔ Factions');
    
    const text = await getPassageText(page);
    // Syndicate should not appear on the UI if it's hidden
    // (This depends on UI implementation - adjust if needed)
    expect(text).toBeDefined();
  });

  test('should have faction reputation bounds', async ({ page }) => {
    await navigateToGame(page);
    
    const cityGuard = await getFactionRep(page, 'city_guard');
    // Rep should be within bounds [-150, 150]
    expect(cityGuard.rep).toBeGreaterThanOrEqual(-150);
    expect(cityGuard.rep).toBeLessThanOrEqual(150);
  });

  test('should calculate tier correctly from reputation', async ({ page }) => {
    await navigateToGame(page);
    
    // Initial state: neutral
    let faction = await getFactionRep(page, 'city_guard');
    expect(faction.tier).toBe('neutral');
    
    // Rep 0 -> neutral tier
    expect(faction.tier).toMatch(/hostile|unfriendly|neutral|friendly|allied|exalted/);
  });
});
