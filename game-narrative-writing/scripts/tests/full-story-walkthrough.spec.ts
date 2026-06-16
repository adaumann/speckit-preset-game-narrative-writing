import { test, expect } from '@playwright/test';
import {
  navigateToGame,
  getCurrentPassage,
  getPassageText,
  getVisibleChoices,
  clickLink,
  walkStoryPath,
  getGamePath,
} from './helpers';

const SPEC_NAME = 'my-game';
const ENGINE = 'sugarcube';

test.describe(`${SPEC_NAME} Full Story Walkthrough (${ENGINE})`, () => {

  test('complete first-choice path through entire story', async ({ page }) => {
    await navigateToGame(page, SPEC_NAME, ENGINE);

    const visitedPassages: string[] = [];

    for (let depth = 0; depth < 20; depth++) {
      const currentPassage = await getCurrentPassage(page);
      visitedPassages.push(currentPassage || 'unknown');

      const choices = await getVisibleChoices(page);

      // If no choices or we hit an ending, stop
      if (choices.length === 0) break;

      const text = await getPassageText(page);

      // Check for error states
      expect(text).not.toContain('[error]');
      expect(text).not.toContain('undefined');

      // Take the first available choice
      await clickLink(page, choices[0]);
      await page.waitForTimeout(300);
    }

    expect(visitedPassages.length).toBeGreaterThanOrEqual(2);
  });

  test('explore all branches at depth 1', async ({ page }) => {
    await navigateToGame(page, SPEC_NAME, ENGINE);

    const firstChoices = await getVisibleChoices(page);
    expect(firstChoices.length).toBeGreaterThanOrEqual(1);

    for (const choice of firstChoices.slice(0, 5)) {
      // Navigate back to start
      await page.goto(getGamePath(SPEC_NAME, ENGINE), { waitUntil: 'networkidle' });

      await clickLink(page, choice);
      await page.waitForTimeout(500);

      const passage = await getCurrentPassage(page);
      expect(passage).toBeTruthy();

      const text = await getPassageText(page);
      expect(text).toBeTruthy();
      expect(text).not.toContain('[error]');
    }
  });

  test('every choice leads to a valid passage', async ({ page }) => {
    await navigateToGame(page, SPEC_NAME, ENGINE);

    const visited = new Set<string>();
    const queue: { passage: string; choicePath: string[] }[] = [];

    const initialPassage = await getCurrentPassage(page);
    queue.push({ passage: initialPassage || 'start', choicePath: [] });
    visited.add(initialPassage || 'start');

    // BFS traversal limited to prevent infinite loops
    const maxNodes = 50;
    let nodesVisited = 0;

    while (queue.length > 0 && nodesVisited < maxNodes) {
      const current = queue.shift()!;
      nodesVisited++;

      // Navigate to this node by replaying the choice path
      await page.goto(getGamePath(SPEC_NAME, ENGINE), { waitUntil: 'networkidle' });
      for (const choice of current.choicePath) {
        const choices = await getVisibleChoices(page);
        if (choices.includes(choice)) {
          await clickLink(page, choice);
          await page.waitForTimeout(300);
        } else {
          break;
        }
      }

      const currentPassage = await getCurrentPassage(page);
      if (!currentPassage) continue;

      const choices = await getVisibleChoices(page);
      for (const choice of choices.slice(0, 3)) {
        const newPath = [...current.choicePath, choice];
        await page.goto(getGamePath(SPEC_NAME, ENGINE), { waitUntil: 'networkidle' });
        for (const c of newPath) {
          const cs = await getVisibleChoices(page);
          if (cs.includes(c)) {
            await clickLink(page, c);
            await page.waitForTimeout(300);
          }
        }

        const targetPassage = await getCurrentPassage(page);
        if (targetPassage && !visited.has(targetPassage)) {
          visited.add(targetPassage);
          queue.push({ passage: targetPassage, choicePath: newPath });

          const text = await getPassageText(page);
          expect(text).not.toContain('[error]');
          expect(text).not.toContain('undefined');
        }
      }
    }

    expect(visited.size).toBeGreaterThanOrEqual(2);
  });

});
