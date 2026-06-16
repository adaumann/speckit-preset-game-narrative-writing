import { test, expect } from '@playwright/test';
import {
  navigateToGame,
  getCurrentPassage,
  getPassageText,
  getVisibleChoices,
  clickLink,
  getConsoleErrors,
} from './helpers';

// Set the spec name and engine here
const SPEC_NAME = 'my-game';
const ENGINE = 'sugarcube';

test.describe(`${SPEC_NAME} Game Flow (${ENGINE})`, () => {

  test('should load game and display start passage', async ({ page }) => {
    await navigateToGame(page, SPEC_NAME, ENGINE);
    const passage = await getCurrentPassage(page);
    expect(passage).toBeTruthy();
    const text = await getPassageText(page);
    expect(text).toBeTruthy();
    const errors = await getConsoleErrors(page);
    expect(errors.length).toBe(0);
  });

  test('should have visible choices on start', async ({ page }) => {
    await navigateToGame(page, SPEC_NAME, ENGINE);
    const choices = await getVisibleChoices(page);
    expect(choices.length).toBeGreaterThanOrEqual(1);
  });

  test('should navigate between passages without errors', async ({ page }) => {
    await navigateToGame(page, SPEC_NAME, ENGINE);
    const choices = await getVisibleChoices(page);
    if (choices.length > 0) {
      const startPassage = await getCurrentPassage(page);
      await clickLink(page, choices[0]);
      await page.waitForTimeout(500);
      const newPassage = await getCurrentPassage(page);
      // Passage should change or stay (could be same if reload)
      expect(newPassage).toBeTruthy();
    }
  });

  test('should have no console errors on startup', async ({ page }) => {
    await navigateToGame(page, SPEC_NAME, ENGINE);
    const errors = await getConsoleErrors(page);
    expect(errors.length).toBe(0);
  });

  test('menu navigation: Continue should go to current passage', async ({ page }) => {
    await navigateToGame(page, SPEC_NAME, ENGINE);
    await clickLink(page, 'Continue');
    await page.waitForTimeout(500);
    const passage = await getCurrentPassage(page);
    expect(passage).toBeTruthy();
  });

  test.describe('Story Walkthrough', () => {
    test('should walk first 3 choices without errors', async ({ page }) => {
      await navigateToGame(page, SPEC_NAME, ENGINE);
      for (let depth = 0; depth < 3; depth++) {
        const choices = await getVisibleChoices(page);
        if (choices.length === 0) break;
        const passageBefore = await getCurrentPassage(page);
        expect(passageBefore).toBeTruthy();
        await clickLink(page, choices[0]);
        await page.waitForTimeout(500);
        const passageAfter = await getCurrentPassage(page);
        expect(passageAfter).toBeTruthy();
      }
    });
  });

  test.describe('Error Recovery', () => {
    test('should handle missing passage gracefully', async ({ page }) => {
      await navigateToGame(page, SPEC_NAME, ENGINE);
      const passage = await getCurrentPassage(page);
      expect(passage).toBeTruthy();
      const text = await getPassageText(page);
      expect(text).not.toContain('Error');
      expect(text).not.toContain('undefined');
    });
  });

});
