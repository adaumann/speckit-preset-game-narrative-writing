import { test, expect } from '@playwright/test';
import {
  navigateToGame,
  getCurrentPassage,
  getCharacterHP,
  getGold,
  getPassageText,
  clickLink,
} from './helpers';

test.describe('Witchhunter Game Flow', () => {
  test('should load game and display start passage', async ({ page }) => {
    await navigateToGame(page);
    const passage = await getCurrentPassage(page);
    expect(passage).toBe('Start');
  });

  test('should display character sheet', async ({ page }) => {
    await navigateToGame(page);
    await clickLink(page, '⚔ Character');
    const passage = await getCurrentPassage(page);
    expect(passage).toBe('CharacterSheet');
    
    const text = await getPassageText(page);
    expect(text).toContain('Aldric');
    expect(text).toContain('Fighter');
  });

  test('should display quest journal', async ({ page }) => {
    await navigateToGame(page);
    await clickLink(page, '📜 Quests');
    const passage = await getCurrentPassage(page);
    expect(passage).toBe('QuestJournal');
  });

  test('should display inventory', async ({ page }) => {
    await navigateToGame(page);
    await clickLink(page, '🎒 Inventory');
    const passage = await getCurrentPassage(page);
    expect(passage).toBe('InventoryUI');
  });

  test('should display party roster', async ({ page }) => {
    await navigateToGame(page);
    await clickLink(page, '👥 Party');
    const passage = await getCurrentPassage(page);
    expect(passage).toBe('PartyRoster');
  });

  test('should display spellbook', async ({ page }) => {
    await navigateToGame(page);
    await clickLink(page, '✨ Spells');
    const passage = await getCurrentPassage(page);
    expect(passage).toBe('SpellsUI');
  });

  test('should display factions screen', async ({ page }) => {
    await navigateToGame(page);
    await clickLink(page, '⚔ Factions');
    const passage = await getCurrentPassage(page);
    expect(passage).toBe('FactionUI');
  });

  test('should display world map', async ({ page }) => {
    await navigateToGame(page);
    await clickLink(page, '🗺 World Map');
    const passage = await getCurrentPassage(page);
    expect(passage).toBe('WorldMap');
  });

  test('should have initial resources', async ({ page }) => {
    await navigateToGame(page);
    const hp = await getCharacterHP(page);
    expect(hp.current).toBe(26);
    expect(hp.max).toBe(26);
    
    const gold = await getGold(page);
    expect(gold).toBe(30);
  });

  test('should navigate to tavern', async ({ page }) => {
    await navigateToGame(page);
    await clickLink(page, '🗺 World Map');
    await clickLink(page, 'The Drunk Griffin');
    const passage = await getCurrentPassage(page);
    expect(passage).toBe('LOC-DrunkGriffin');
  });

  test('should navigate from tavern to Thorngate', async ({ page }) => {
    await navigateToGame(page);
    await clickLink(page, '🗺 World Map');
    await clickLink(page, 'The Drunk Griffin');
    const text = await getPassageText(page);
    expect(text).toContain('A two-story tavern');
  });

  test('should display intro scene correctly', async ({ page }) => {
    await navigateToGame(page);
    const text = await getPassageText(page);
    expect(text).toContain('Thorngate');
    expect(text).toContain('goblins');
  });
});
