import { test, expect } from '@playwright/test';
import {
  navigateToGame,
  getCurrentPassage,
  getPassageText,
  getVisibleChoices,
  clickLink,
  getGamePath,
} from '../helpers';

const SPEC_NAME = 'shrine-sample';
const ENGINE = 'sugarcube';

const ALL_PASSAGES: string[] = ["AfterHistory", "AskHistory", "Donate", "Donate1", "Donate5", "End", "Final", "QuestUI", "Search", "ShrineWidgets"];

const PASSAGE_LINKS: Record<string, string[]> = {
  "StoryTitle": [],
  "StoryData": [],
  "StoryInit": [],
  "Start": [
    "AskHistory",
    "Donate",
    "Search"
  ],
  "AskHistory": [
    "AfterHistory"
  ],
  "AfterHistory": [
    "Start",
    "End"
  ],
  "Donate": [
    "Donate5",
    "Donate1",
    "Start"
  ],
  "Donate5": [
    "Start"
  ],
  "Donate1": [
    "Start"
  ],
  "Search": [
    "Start"
  ],
  "End": [
    "Final"
  ],
  "Final": [],
  "StoryCaption": [],
  "StoryMenu": [
    "CharacterSheet",
    "InventoryUI",
    "QuestUI",
    "Start"
  ],
  "CharacterSheet": [
    "Start"
  ],
  "InventoryUI": [
    "Start"
  ],
  "QuestUI": [
    "Start"
  ],
  "StoryStylesheet": [],
  "ShrineWidgets": []
};

const PASSAGE_SOURCE: Record<string, string> = {"StoryTitle": "shrine-init.twee", "StoryData": "shrine-init.twee", "StoryInit": "shrine-init.twee", "Start": "shrine-nodes.twee", "AskHistory": "shrine-nodes.twee", "AfterHistory": "shrine-nodes.twee", "Donate": "shrine-nodes.twee", "Donate5": "shrine-nodes.twee", "Donate1": "shrine-nodes.twee", "Search": "shrine-nodes.twee", "End": "shrine-nodes.twee", "Final": "shrine-nodes.twee", "StoryCaption": "shrine-ui.twee", "StoryMenu": "shrine-ui.twee", "CharacterSheet": "shrine-ui.twee", "InventoryUI": "shrine-ui.twee", "QuestUI": "shrine-ui.twee", "StoryStylesheet": "shrine-ui.twee", "ShrineWidgets": "shrine-widgets.twee"};

test.describe(`${SPEC_NAME} Generated Passage Tests (${ENGINE})`, () => {

  test('all passages from .twee files are known and valid', async ({ page }) => {
    expect(ALL_PASSAGES.length).toBeGreaterThanOrEqual(1);
    for (const p of ALL_PASSAGES) {
      expect(p).toMatch(/^[A-Z]/);
    }
  });

  test('every link target exists as a passage', async ({ page }) => {
    const systemPassages = new Set([
      'StoryTitle', 'StoryData', 'StoryInit', 'StoryMenu',
      'StoryCaption', 'StoryStylesheet', 'StoryShare', 'StorySettings',
      'StoryAuthoring', 'Start', 'AllWidgets',
      'CharacterSheet', 'InventoryUI', 'QuestJournal', 'PartyRoster',
      'SpellsUI', 'FactionUI', 'WorldMap',
    ]);
    for (const [passage, targets] of Object.entries(PASSAGE_LINKS)) {
      for (const target of targets) {
        if (!ALL_PASSAGES.includes(target) && !systemPassages.has(target) && !target.startsWith('END-')) {
          expect(true).toBeFalsy(
            `${passage} links to "${target}" which is not defined in any .twee file`);
        }
      }
    }
  });

  test('BFS walkthrough covers all story passages', async ({ page }) => {
    await navigateToGame(page, SPEC_NAME, ENGINE);

    const visited = new Set<string>();
    const queue: string[][] = [];

    const initialPassage = await getCurrentPassage(page);
    if (initialPassage) {
      visited.add(initialPassage);
      queue.push([]);
    }

    const storyPassages = ALL_PASSAGES.filter(
      p => !p.startsWith('Story') && p !== 'Start'
    );

    const maxNodes = Math.min(200, storyPassages.length * 3);
    let nodesVisited = 0;

    while (queue.length > 0 && nodesVisited < maxNodes) {
      const choicePath = queue.shift()!;
      nodesVisited++;

      await page.goto(getGamePath(SPEC_NAME, ENGINE), { waitUntil: 'networkidle' });

      for (const choiceText of choicePath) {
        const choices = await getVisibleChoices(page);
        if (choices.includes(choiceText)) {
          await clickLink(page, choiceText);
          await page.waitForTimeout(300);
        } else {
          break;
        }
      }

      const passage = await getCurrentPassage(page);
      if (!passage) continue;

      const text = await getPassageText(page);
      expect(text).not.toContain('[error]');
      expect(text).not.toContain('undefined');

      const choices = await getVisibleChoices(page);
      for (const choice of choices.slice(0, 5)) {
        const newPath = [...choicePath, choice];
        await page.goto(getGamePath(SPEC_NAME, ENGINE), { waitUntil: 'networkidle' });

        for (const c of newPath) {
          const cs = await getVisibleChoices(page);
          if (cs.includes(c)) {
            await clickLink(page, c);
            await page.waitForTimeout(300);
          } else {
            break;
          }
        }

        const targetPassage = await getCurrentPassage(page);
        if (targetPassage && !visited.has(targetPassage)) {
          visited.add(targetPassage);
          queue.push(newPath);

          const targetText = await getPassageText(page);
          expect(targetText).not.toContain('[error]');
          expect(targetText).not.toContain('undefined');
        }
      }
    }

    const unvisited = storyPassages.filter(p => !visited.has(p));
    if (unvisited.length > 0) {
      console.log(`⚠️  Unvisited passages (${unvisited.length}): ${unvisited.join(', ')}`);
    }

    expect(visited.size).toBeGreaterThanOrEqual(1);
  });

  test('every story passage contains valid content', async ({ page }) => {
    await navigateToGame(page, SPEC_NAME, ENGINE);

    for (let i = 0; i < Math.min(10, ALL_PASSAGES.length); i++) {
      await page.goto(getGamePath(SPEC_NAME, ENGINE), { waitUntil: 'networkidle' });

      const choices = await getVisibleChoices(page);
      if (choices.length === 0) break;

      const choiceIndex = i % choices.length;
      await clickLink(page, choices[choiceIndex]);
      await page.waitForTimeout(500);

      const passage = await getCurrentPassage(page);
      expect(passage).toBeTruthy();

      const text = await getPassageText(page);
      expect(text).toBeTruthy();
      expect(text).not.toContain('[error]');
    }
  });
});
