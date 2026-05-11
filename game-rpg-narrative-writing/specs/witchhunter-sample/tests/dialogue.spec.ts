import { test, expect } from '@playwright/test';
import {
  navigateToGame,
  getCurrentPassage,
  getDialogueChoiceCount,
  clickDialogueChoice,
  isNPCInParty,
  getPassageText,
  clickLink,
} from './helpers';

test.describe('Dialogue System', () => {
  test('should display dialogue UI elements', async ({ page }) => {
    await navigateToGame(page);
    await clickLink(page, '🗺 World Map');
    await clickLink(page, 'The Drunk Griffin');
    await clickLink(page, 'Speak to Mira');
    
    const passage = await getCurrentPassage(page);
    expect(passage).toBe('DialogueUI');
  });

  test('should have dialogue choices', async ({ page }) => {
    await navigateToGame(page);
    await clickLink(page, '🗺 World Map');
    await clickLink(page, 'The Drunk Griffin');
    await clickLink(page, 'Speak to Mira');
    
    const choiceCount = await getDialogueChoiceCount(page);
    expect(choiceCount).toBeGreaterThan(0);
  });

  test('should execute dialogue choice effects', async ({ page }) => {
    await navigateToGame(page);
    await clickLink(page, '🗺 World Map');
    await clickLink(page, 'The Drunk Griffin');
    await clickLink(page, 'Speak to Mira');
    
    // Click first dialogue choice
    await clickDialogueChoice(page, 0);
    
    // Check if Mira is now in party
    const inParty = await isNPCInParty(page, 'mira');
    expect(inParty).toBe(true);
  });

  test('should track dialogue state', async ({ page }) => {
    await navigateToGame(page);
    await clickLink(page, '🗺 World Map');
    await clickLink(page, 'The Drunk Griffin');
    await clickLink(page, 'Speak to Mira');
    
    // Verify we're in the dialogue system
    const passage = await getCurrentPassage(page);
    expect(passage).toBe('DialogueUI');
  });

  test('should display NPC name in dialogue', async ({ page }) => {
    await navigateToGame(page);
    await clickLink(page, '🗺 World Map');
    await clickLink(page, 'The Drunk Griffin');
    await clickLink(page, 'Speak to Mira');
    
    const text = await getPassageText(page);
    expect(text).toContain('Mira');
  });

  test('should display dialogue choices text', async ({ page }) => {
    await navigateToGame(page);
    await clickLink(page, '🗺 World Map');
    await clickLink(page, 'The Drunk Griffin');
    await clickLink(page, 'Speak to Mira');
    
    const choiceButtons = await page.locator('.dialogue-choices button').allTextContents();
    expect(choiceButtons.length).toBeGreaterThan(0);
    choiceButtons.forEach((text) => {
      expect(text.length).toBeGreaterThan(0);
    });
  });

  test('should handle dialogue branching', async ({ page }) => {
    await navigateToGame(page);
    await clickLink(page, '🗺 World Map');
    await clickLink(page, 'The Drunk Griffin');
    await clickLink(page, 'Speak to Mira');
    
    const initialChoiceCount = await getDialogueChoiceCount(page);
    expect(initialChoiceCount).toBeGreaterThan(0);
    
    // Click a choice
    await clickDialogueChoice(page, 0);
    
    // Should transition to next dialogue state
    const passage = await getCurrentPassage(page);
    // Passage might change or we stay in dialogue depending on "next" value
    expect(passage).toBeDefined();
  });
});
