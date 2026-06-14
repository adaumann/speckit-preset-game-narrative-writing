import { Page } from '@playwright/test';
import * as path from 'path';

/**
 * Get the file:// URL for the witchhunter game HTML
 */
export function getGamePath(): string {
  const htmlPath = path.resolve(__dirname, '../witchhunter.html');
  return `file://${htmlPath}`;
}

/**
 * Navigate to the game start
 */
export async function navigateToGame(page: Page): Promise<void> {
  const gamePath = getGamePath();
  await page.goto(gamePath, { waitUntil: 'networkidle' });
}

/**
 * Get the current passage name
 */
export async function getCurrentPassage(page: Page): Promise<string> {
  return await page.evaluate(() => {
    const state = (window as any).State;
    return state?.passage?.name || '';
  });
}

/**
 * Click a link by text
 */
export async function clickLink(page: Page, linkText: string): Promise<void> {
  await page.click(`a:has-text("${linkText}")`);
  await page.waitForLoadState('networkidle');
}

/**
 * Get character HP
 */
export async function getCharacterHP(page: Page): Promise<{ current: number; max: number }> {
  return await page.evaluate(() => {
    const state = (window as any).State.variables;
    return {
      current: state.$partyCurrentHP,
      max: state.$partyMaxHP,
    };
  });
}

/**
 * Get faction reputation
 */
export async function getFactionRep(page: Page, factionId: string): Promise<{ rep: number; tier: string }> {
  return await page.evaluate((fId) => {
    const state = (window as any).State.variables;
    const rep = state[`$faction_${fId}_rep`] || 0;
    const tier = state[`$faction_${fId}_tier`] || 'neutral';
    return { rep, tier };
  }, factionId);
}

/**
 * Check if NPC is in party
 */
export async function isNPCInParty(page: Page, npcId: string): Promise<boolean> {
  return await page.evaluate((id) => {
    const state = (window as any).State.variables;
    return state[`$${id}_in_party`] || false;
  }, npcId);
}

/**
 * Get quest state
 */
export async function getQuestState(page: Page, questId: string): Promise<{ state: string; stage: number }> {
  return await page.evaluate((qId) => {
    const state = (window as any).State.variables;
    return {
      state: state[`$quest_${qId}_state`] || 'inactive',
      stage: state[`$quest_${qId}_stage`] || 0,
    };
  }, questId);
}

/**
 * Get current gold amount
 */
export async function getGold(page: Page): Promise<number> {
  return await page.evaluate(() => {
    const state = (window as any).State.variables;
    return state.$gold || 0;
  });
}

/**
 * Get dialogue choice count
 */
export async function getDialogueChoiceCount(page: Page): Promise<number> {
  return await page.locator('.dialogue-choices button').count();
}

/**
 * Click dialogue choice by index
 */
export async function clickDialogueChoice(page: Page, index: number): Promise<void> {
  const buttons = await page.locator('.dialogue-choices button').all();
  if (index < buttons.length) {
    await buttons[index].click();
    await page.waitForLoadState('networkidle');
  }
}

/**
 * Get visible passage text content
 */
export async function getPassageText(page: Page): Promise<string> {
  return await page.locator('[role="main"]').textContent() || '';
}

/**
 * Check if tactical combat is active
 */
export async function isCombatActive(page: Page): Promise<boolean> {
  const passageName = await getCurrentPassage(page);
  return passageName.includes('Combat') || passageName === 'CombatUI';
}

/**
 * Perform a tactical combat round
 */
export async function performCombatAction(page: Page, actionText: string): Promise<void> {
  await page.click(`button:has-text("${actionText}")`);
  await page.waitForLoadState('networkidle');
}

/**
 * Get spell slot status
 */
export async function getSpellSlots(page: Page): Promise<{ level: number; current: number; max: number }[]> {
  return await page.evaluate(() => {
    const state = (window as any).State.variables;
    const slots = state.$mira_spell_slots || {};
    return Object.entries(slots).map(([level, data]: [string, any]) => ({
      level: parseInt(level),
      current: data.current,
      max: data.max,
    }));
  });
}
