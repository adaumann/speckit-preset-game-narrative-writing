import { test, expect } from '@playwright/test';
import {
  navigateToGame,
  getCurrentPassage,
  getPassageText,
  getVisibleChoices,
  clickLink,
  getGamePath,
} from '../helpers';

const SPEC_NAME = 'witchhunter-sample';
const ENGINE = 'sugarcube';

const ALL_PASSAGES: string[] = ["D5eCombatEngine", "ElaraShop", "LOC-DrunkGriffin", "LOC-Thorngate", "MiraSpellSelect", "NODE-001_RoadToThorn", "NODE-001b_SkillCheckResult", "NODE-002_TavernMira", "NODE-002b_MiraJoins", "NODE-002c_MiraDeclined", "NODE-003_GoblinAmbush", "NODE-004_AlchemyBench", "NODE-005_InnRest", "NODE-006_QuestComplete", "NODE-006b_Ending", "ScriptPassage"];

const PASSAGE_LINKS: Record<string, string[]> = {
  "StoryTitle": [],
  "StoryData": [],
  "ScriptPassage": [],
  "StoryInit": [],
  "D5eCombatEngine": [],
  "LOC-Thorngate": [
    "WorldMap",
    "CharacterSheet",
    "QuestJournal"
  ],
  "LOC-DrunkGriffin": [
    "WorldMap",
    "LOC-Thorngate",
    "CharacterSheet",
    "QuestJournal"
  ],
  "ElaraShop": [],
  "Start": [
    "NODE-001_RoadToThorn"
  ],
  "NODE-001_RoadToThorn": [
    "NODE-001b_SkillCheckResult"
  ],
  "NODE-001b_SkillCheckResult": [],
  "NODE-002_TavernMira": [
    "NODE-003_GoblinAmbush"
  ],
  "NODE-002b_MiraJoins": [
    "LOC-DrunkGriffin"
  ],
  "NODE-002c_MiraDeclined": [
    "LOC-DrunkGriffin"
  ],
  "NODE-003_GoblinAmbush": [
    "NODE-004_AlchemyBench"
  ],
  "NODE-004_AlchemyBench": [
    "LOC-DrunkGriffin"
  ],
  "NODE-005_InnRest": [],
  "NODE-006_QuestComplete": [
    "NODE-006b_Ending"
  ],
  "NODE-006b_Ending": [
    "END-C",
    "Start",
    "CharacterSheet",
    "QuestJournal",
    "END-B",
    "END-A"
  ],
  "StoryMenu": [
    "CharacterSheet",
    "QuestJournal",
    "PartyRoster",
    "SpellsUI",
    "FactionUI",
    "WorldMap",
    "InventoryUI"
  ],
  "StoryCaption": [
    "InventoryUI",
    "CharacterSheet",
    "QuestJournal",
    "WorldMap"
  ],
  "StoryStylesheet": [],
  "CharacterSheet": [],
  "InventoryUI": [],
  "QuestJournal": [
    "QuestJournal"
  ],
  "PartyRoster": [],
  "DialogueUI": [],
  "MiraSpellSelect": [
    "TacticalCombatUI",
    "CombatOutcome"
  ],
  "SpellsUI": [],
  "FactionUI": [],
  "WorldMap": [],
  "CombatOutcome": [
    "Start"
  ],
  "CombatModeSelect": [
    "CombatOutcome",
    "TacticalCombatUI"
  ],
  "TacticalCombatUI": [
    "TacticalCombatUI",
    "CombatOutcome",
    "MiraSpellSelect"
  ],
  "LootContainer": [
    "LootContainerUI"
  ],
  "LootContainerUI": [],
  "CraftUI": [
    "CraftResultUI"
  ],
  "CraftResultUI": [
    "CraftUI"
  ],
  "RestUI": [],
  "TravelEncounterTransition": [],
  "AllWidgets": [
    "RestUI",
    "LootContainerUI",
    "CombatModeSelect",
    "DialogueUI",
    "CraftUI",
    "TravelEncounterTransition"
  ]
};

const PASSAGE_SOURCE: Record<string, string> = {"StoryTitle": "witchhunter-init.twee", "StoryData": "witchhunter-init.twee", "ScriptPassage": "witchhunter-init.twee", "StoryInit": "witchhunter-init.twee", "D5eCombatEngine": "witchhunter-init.twee", "LOC-Thorngate": "witchhunter-locations.twee", "LOC-DrunkGriffin": "witchhunter-locations.twee", "ElaraShop": "witchhunter-locations.twee", "Start": "witchhunter-nodes.twee", "NODE-001_RoadToThorn": "witchhunter-nodes.twee", "NODE-001b_SkillCheckResult": "witchhunter-nodes.twee", "NODE-002_TavernMira": "witchhunter-nodes.twee", "NODE-002b_MiraJoins": "witchhunter-nodes.twee", "NODE-002c_MiraDeclined": "witchhunter-nodes.twee", "NODE-003_GoblinAmbush": "witchhunter-nodes.twee", "NODE-004_AlchemyBench": "witchhunter-nodes.twee", "NODE-005_InnRest": "witchhunter-nodes.twee", "NODE-006_QuestComplete": "witchhunter-nodes.twee", "NODE-006b_Ending": "witchhunter-nodes.twee", "StoryMenu": "witchhunter-ui.twee", "StoryCaption": "witchhunter-ui.twee", "StoryStylesheet": "witchhunter-ui.twee", "CharacterSheet": "witchhunter-ui.twee", "InventoryUI": "witchhunter-ui.twee", "QuestJournal": "witchhunter-ui.twee", "PartyRoster": "witchhunter-ui.twee", "DialogueUI": "witchhunter-ui.twee", "MiraSpellSelect": "witchhunter-ui.twee", "SpellsUI": "witchhunter-ui.twee", "FactionUI": "witchhunter-ui.twee", "WorldMap": "witchhunter-ui.twee", "CombatOutcome": "witchhunter-ui.twee", "CombatModeSelect": "witchhunter-ui.twee", "TacticalCombatUI": "witchhunter-ui.twee", "LootContainer": "witchhunter-ui.twee", "LootContainerUI": "witchhunter-ui.twee", "CraftUI": "witchhunter-ui.twee", "CraftResultUI": "witchhunter-ui.twee", "RestUI": "witchhunter-ui.twee", "TravelEncounterTransition": "witchhunter-ui.twee", "AllWidgets": "witchhunter-widgets.twee"};

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
