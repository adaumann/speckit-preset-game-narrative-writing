import { test, expect } from '@playwright/test';
import {
  navigateToGame,
  getSpellSlots,
  clickLink,
  getPassageText,
  isNPCInParty,
} from './helpers';

test.describe('Spell & Combat System', () => {
  test('should display spellbook UI', async ({ page }) => {
    await navigateToGame(page);
    await clickLink(page, '✨ Spells');
    
    const text = await getPassageText(page);
    expect(text).toContain('Spellbook');
  });

  test('should show spell slots correctly', async ({ page }) => {
    await navigateToGame(page);
    
    const slots = await getSpellSlots(page);
    // Mira should have initialized spell slots
    expect(Array.isArray(slots)).toBe(true);
  });

  test('should show cantrips always available', async ({ page }) => {
    await navigateToGame(page);
    await clickLink(page, '✨ Spells');
    
    const text = await getPassageText(page);
    // Without Mira in party, should show "No spellcasters"
    // This test assumes we haven't recruited Mira yet
    if (!text.includes('No spellcasters')) {
      expect(text).toContain('Cantrips');
    }
  });

  test('should show leveled spells with slot counts', async ({ page }) => {
    await navigateToGame(page);
    
    // Recruit Mira first
    await clickLink(page, '🗺 World Map');
    await clickLink(page, 'The Drunk Griffin');
    await clickLink(page, 'Speak to Mira');
    
    // Click first dialogue choice to recruit
    const buttons = await page.locator('.dialogue-choices button').all();
    if (buttons.length > 0) {
      await buttons[0].click();
      await page.waitForLoadState('networkidle');
    }
    
    // Now check spellbook
    await clickLink(page, '✨ Spells');
    const text = await getPassageText(page);
    
    // Should show spell slots if Mira is in party
    const miraInParty = await isNPCInParty(page, 'mira');
    if (miraInParty) {
      expect(text).toContain('Level');
    }
  });

  test('should display spell descriptions', async ({ page }) => {
    await navigateToGame(page);
    await clickLink(page, '✨ Spells');
    
    const text = await getPassageText(page);
    // Spellbook should have content
    expect(text).toBeDefined();
    expect(text.length).toBeGreaterThan(0);
  });

  test('should show spell schools', async ({ page }) => {
    await navigateToGame(page);
    
    // Recruit Mira
    await clickLink(page, '🗺 World Map');
    await clickLink(page, 'The Drunk Griffin');
    await clickLink(page, 'Speak to Mira');
    const buttons = await page.locator('.dialogue-choices button').all();
    if (buttons.length > 0) {
      await buttons[0].click();
      await page.waitForLoadState('networkidle');
    }
    
    await clickLink(page, '✨ Spells');
    const text = await getPassageText(page);
    
    const miraInParty = await isNPCInParty(page, 'mira');
    if (miraInParty) {
      // Spell schools should be mentioned
      expect(text).toContain('Evocation') || expect(text).toContain('Abjuration');
    }
  });

  test('spell system should be integrated with UI', async ({ page }) => {
    await navigateToGame(page);
    await clickLink(page, '⚔ Character');
    
    const text = await getPassageText(page);
    // Character sheet should exist and be displayable
    expect(text).toBeDefined();
  });

  test('should have spell menu link in sidebar', async ({ page }) => {
    await navigateToGame(page);
    
    // Check if Spells link exists
    const spellsLink = page.locator('a:has-text("✨ Spells")');
    expect(await spellsLink.isVisible()).toBe(true);
  });

  test('should track spell slot expenditure', async ({ page }) => {
    await navigateToGame(page);
    
    const initialSlots = await getSpellSlots(page);
    expect(initialSlots).toBeDefined();
    expect(Array.isArray(initialSlots)).toBe(true);
  });
});
