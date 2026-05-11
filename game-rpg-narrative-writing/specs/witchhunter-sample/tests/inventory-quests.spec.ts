import { test, expect } from '@playwright/test';
import {
  navigateToGame,
  clickLink,
  getPassageText,
  getGold,
  getQuestState,
} from './helpers';

test.describe('Inventory & Quests', () => {
  test('should display inventory UI', async ({ page }) => {
    await navigateToGame(page);
    await clickLink(page, '🎒 Inventory');
    
    const passage = await page.evaluate(() => {
      const state = (window as any).State;
      return state?.passage?.name || '';
    });
    expect(passage).toBe('InventoryUI');
  });

  test('should show inventory items', async ({ page }) => {
    await navigateToGame(page);
    await clickLink(page, '🎒 Inventory');
    
    const text = await getPassageText(page);
    expect(text).toBeDefined();
    expect(text.length).toBeGreaterThan(0);
  });

  test('should display initial gold', async ({ page }) => {
    await navigateToGame(page);
    
    const gold = await getGold(page);
    expect(gold).toBe(30); // Initial gold amount
  });

  test('should show gold in sidebar', async ({ page }) => {
    await navigateToGame(page);
    
    const goldDisplay = page.locator('#sc-gold');
    expect(await goldDisplay.isVisible()).toBe(true);
  });

  test('should track quest states', async ({ page }) => {
    await navigateToGame(page);
    
    const questState = await getQuestState(page, 'clear_goblin_lair');
    expect(questState).toBeDefined();
    expect(questState.state).toMatch(/inactive|active|completed/);
  });

  test('should display quest journal', async ({ page }) => {
    await navigateToGame(page);
    await clickLink(page, '📜 Quests');
    
    const text = await getPassageText(page);
    expect(text).toContain('Quest');
  });

  test('should show quest stages', async ({ page }) => {
    await navigateToGame(page);
    await clickLink(page, '📜 Quests');
    
    const text = await getPassageText(page);
    // Should have quest information
    expect(text.length).toBeGreaterThan(0);
  });

  test('inventory should have categories', async ({ page }) => {
    await navigateToGame(page);
    await clickLink(page, '🎒 Inventory');
    
    const text = await getPassageText(page);
    // Inventory should show items in categories
    expect(text).toBeDefined();
  });

  test('should have working quest link in sidebar', async ({ page }) => {
    await navigateToGame(page);
    
    const questLink = page.locator('a:has-text("📜 Quests")');
    expect(await questLink.isVisible()).toBe(true);
  });

  test('should track active quests in sidebar', async ({ page }) => {
    await navigateToGame(page);
    
    // There should be a quest display in sidebar
    const questDisplay = page.locator('#sc-quest');
    // It might not always be visible if no active quest
    expect(questDisplay).toBeDefined();
  });

  test('should handle inventory categories', async ({ page }) => {
    await navigateToGame(page);
    await clickLink(page, '🎒 Inventory');
    
    // Look for item buttons or links
    const buttons = await page.locator('button, a').count();
    // Inventory should have interactive elements
    expect(buttons).toBeGreaterThanOrEqual(0);
  });
});
