import { Page } from '@playwright/test';
import * as path from 'path';

/**
 * Get the file:// URL for the compiled game HTML
 */
export function getGamePath(specName: string, engine: string = 'sugarcube'): string {
  const htmlPath = path.resolve(__dirname, `../../specs/${specName}/output/${engine}/story.html`);
  return `file://${htmlPath}`;
}

/**
 * Navigate to the game start
 */
export async function navigateToGame(page: Page, specName: string, engine: string = 'sugarcube'): Promise<void> {
  const gamePath = getGamePath(specName, engine);
  await page.goto(gamePath, { waitUntil: 'networkidle', timeout: 10000 });
}

/**
 * Get the current passage name in SugarCube
 */
export async function getCurrentPassage(page: Page): Promise<string> {
  return await page.evaluate(() => {
    try {
      const state = (window as any).SugarCube?.State || (window as any).State;
      return state?.passage?.name || state?.passage?.title || '';
    } catch {
      return '';
    }
  });
}

/**
 * Click a link by visible text
 */
export async function clickLink(page: Page, linkText: string): Promise<void> {
  const link = page.locator(`a:has-text("${linkText}")`).first();
  await link.waitFor({ state: 'visible', timeout: 5000 });
  await link.click();
  await page.waitForTimeout(500);
}

/**
 * Click a button by visible text
 */
export async function clickButton(page: Page, buttonText: string): Promise<void> {
  const button = page.locator(`button:has-text("${buttonText}")`).first();
  await button.waitFor({ state: 'visible', timeout: 5000 });
  await button.click();
  await page.waitForTimeout(500);
}

/**
 * Get visible passage text content
 */
export async function getPassageText(page: Page): Promise<string> {
  try {
    const text = await page.locator('.passage, [role="main"], #passages, .story-passage').first().textContent();
    return text || '';
  } catch {
    return '';
  }
}

/**
 * Get all visible links/choices on the current passage
 */
export async function getVisibleChoices(page: Page): Promise<string[]> {
  const choices: string[] = [];
  const links = await page.locator('a').all();
  for (const link of links) {
    const text = await link.textContent();
    if (text && text.trim()) {
      choices.push(text.trim());
    }
  }
  return choices;
}

/**
 * Check if there are any console errors
 */
export async function getConsoleErrors(page: Page): Promise<string[]> {
  return await page.evaluate(() => {
    try {
      const logs: string[] = [];
      const originalError = console.error;
      console.error = (...args: any[]) => {
        logs.push(args.map(String).join(' '));
      };
      return logs;
    } catch {
      return [];
    }
  });
}

/**
 * Walk a path through the story by clicking choices in sequence.
 * Returns the passages visited.
 */
export async function walkStoryPath(page: Page, choices: string[]): Promise<string[]> {
  const visited: string[] = [];
  for (const choiceText of choices) {
    const passage = await getCurrentPassage(page);
    visited.push(passage || 'unknown');
    await clickLink(page, choiceText);
  }
  const finalPassage = await getCurrentPassage(page);
  visited.push(finalPassage || 'unknown');
  return visited;
}

/**
 * Get a variable value from the game state
 */
export async function getVariable(page: Page, varName: string): Promise<any> {
  return await page.evaluate((name) => {
    try {
      const state = (window as any).SugarCube?.State || (window as any).State;
      return state?.variables?.[name];
    } catch {
      return undefined;
    }
  }, varName);
}
