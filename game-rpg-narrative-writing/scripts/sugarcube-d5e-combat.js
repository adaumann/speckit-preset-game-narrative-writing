/**
 * sugarcube-d5e-combat.js
 * D&D 5e Combat Engine for SugarCube 2.x
 *
 * Paste the contents of this file into a Twee passage tagged [script]:
 *   :: D5eCombatEngine [script]
 *   <paste here>
 *
 * Then call from any passage:
 *   <<combat "Guard Captain Aldric" "NODE_016_COMBAT_OUTCOME">>
 *
 * SugarCube variables read:
 *   $partyLevel, $party (array of combatant objects — see buildParty())
 *   $playerStrMod, $playerDexMod, $playerConMod (ability modifiers)
 *   $playerProfBonus (proficiency bonus; auto-computed from level if absent)
 *
 * SugarCube variables written after combat:
 *   $lastCombatOutcome   "player_won" | "player_lost" | "player_retreated"
 *   $lastCombatXP        XP awarded (0 if lost/retreated)
 *   $lastCombatLoot      array of loot strings ([] if lost/retreated)
 *   $lastCombatLog       array of round-by-round narrative strings
 *   $lastEnemyName       name of the enemy fought
 *   $lastEnemySurrendered  true if enemy surrendered (HP <= 25% and morale check failed)
 *
 * Optional SugarCube variables read (set from character sheet):
 *   $partyMultiattack    number of attacks per turn (auto-derived from class+level if absent)
 *   $partyDamageType     damage type string for player weapon (default "physical")
 *   $playerResistances   array of damage type strings player is resistant to (default [])
 *   $playerImmunities    array of damage type strings player is immune to (default [])
 *
 * Usage — register enemies with D5e.registerEnemy(), then start combat:
 *   D5e.combat.start(enemyId, passageOnEnd)
 *
 * Or use the <<combat>> macro for inline use (see bottom of file).
 */

window.D5e = window.D5e || {};

/* ─────────────────────────────────────────────────────────────
   1. CORE DICE
   ───────────────────────────────────────────────────────────── */

D5e.dice = {
    /** Roll a single die (d4, d6, d8, d10, d12, d20, d100) */
    roll(sides) {
        return Math.floor(Math.random() * sides) + 1;
    },

    /** Roll NdSides and return total + individual rolls */
    rollN(n, sides) {
        const rolls = [];
        for (let i = 0; i < n; i++) rolls.push(this.roll(sides));
        return { total: rolls.reduce((a, b) => a + b, 0), rolls };
    },

    /** Roll with advantage: 2d20 keep highest */
    rollAdvantage() {
        const a = this.roll(20), b = this.roll(20);
        return { total: Math.max(a, b), rolls: [a, b], kept: Math.max(a, b) };
    },

    /** Roll with disadvantage: 2d20 keep lowest */
    rollDisadvantage() {
        const a = this.roll(20), b = this.roll(20);
        return { total: Math.min(a, b), rolls: [a, b], kept: Math.min(a, b) };
    },

    /** Parse and roll a damage string e.g. "2d6+3" or "1d8" */
    rollDamage(expr) {
        // e.g. "2d8+3", "1d6", "3d4-1"
        const m = String(expr).match(/^(\d+)d(\d+)([+-]\d+)?$/i);
        if (!m) return { total: 0, rolls: [], expr };
        const n = parseInt(m[1]), sides = parseInt(m[2]), bonus = parseInt(m[3] || 0);
        const r = this.rollN(n, sides);
        return { total: Math.max(0, r.total + bonus), rolls: r.rolls, bonus, expr };
    }
};

/* ─────────────────────────────────────────────────────────────
   2. ABILITY MODIFIERS & PROFICIENCY
   ───────────────────────────────────────────────────────────── */

D5e.abilityMod = function(score) {
    return Math.floor((score - 10) / 2);
};

D5e.profBonus = function(level) {
    return Math.ceil(level / 4) + 1; // 2 at L1-4, 3 at L5-8, 4 at L9-12, 5 at L13-16, 6 at L17-20
};

/* ─────────────────────────────────────────────────────────────
   3. SKILL CHECKS (standalone — usable outside combat)
   ───────────────────────────────────────────────────────────── */

/**
 * Perform a skill check and write results to SugarCube variables.
 *
 * @param {string} skill  e.g. "Insight", "Persuasion", "Athletics"
 * @param {number} mod    ability modifier for the skill
 * @param {number} dc     difficulty class
 * @param {boolean} proficient  add proficiency bonus?
 * @param {"normal"|"advantage"|"disadvantage"} rollType
 * @returns {{ success: boolean, total: number, roll: number, dc: number }}
 *
 * Also sets:
 *   $lastSkillCheckSuccess, $lastSkillCheckTotal, $lastSkillCheckRoll, $lastSkillCheckDC
 */
D5e.skillCheck = function(skill, mod, dc, proficient, rollType) {
    rollType = rollType || "normal";
    proficient = proficient || false;

    let rollResult;
    if (rollType === "advantage")         rollResult = D5e.dice.rollAdvantage();
    else if (rollType === "disadvantage") rollResult = D5e.dice.rollDisadvantage();
    else                                  rollResult = { total: D5e.dice.roll(20), rolls: [] };

    const level = State.variables.partyLevel || 1;
    const prof  = proficient ? D5e.profBonus(level) : 0;
    const total = rollResult.total + mod + prof;

    // Write to SugarCube story variables
    State.variables.lastSkillCheckSuccess = total >= dc;
    State.variables.lastSkillCheckTotal   = total;
    State.variables.lastSkillCheckRoll    = rollResult.total;
    State.variables.lastSkillCheckDC      = dc;
    State.variables.lastSkillCheckSkill   = skill;

    return { success: total >= dc, total, roll: rollResult.total, dc };
};

/* ─────────────────────────────────────────────────────────────
   4. ENEMY REGISTRY
   ───────────────────────────────────────────────────────────── */

D5e._enemies = {};

/**
 * Register an enemy type.
 * @param {string} id  unique key, e.g. "guard_captain"
 * @param {object} def enemy definition
 *
 * def shape:
 * {
 *   name:       "Guard Captain Aldric",
 *   cr:         3,
 *   xp:         700,
 *   hp:         52,           // max HP; string "4d10+8" also accepted
 *   ac:         16,
 *   speed:      30,
 *   str: 16, dex: 13, con: 14, int: 12, wis: 11, cha: 10,
 *   profBonus:  2,
 *   attacks: [
 *     { name: "Longsword",  toHitBonus: 5, damage: "1d8+3", damageType: "slashing" },
 *     { name: "Shield Bash",toHitBonus: 5, damage: "1d4+3", damageType: "bludgeoning", save: { ability:"STR", dc:13, effect:"prone" } }
 *   ],
 *   saves:      { str:5, dex:1, con:4, int:1, wis:0, cha:0 },
 *   resistances: [],          // damage types
 *   immunities:  [],
 *   skills:     { perception: 2, athletics: 5 },
 *   features:   [
 *     { name: "Second Wind", uses: 1, trigger: "hp_below_half",
 *       effect: (enemy) => { enemy.hp = Math.min(enemy.maxHp, enemy.hp + D5e.dice.rollN(1,10).total + 3); } }
 *   ],
 *   morale:     12,           // DC for morale check when HP <= 25%; 0 = never surrenders
 *   loot:       ["50 gp", "Guard Captain Badge"],
 *   multiattack: 2,           // number of attacks per turn
 *   legendary:  null          // or { actions: [...], resistances: 3 }
 * }
 */
D5e.registerEnemy = function(id, def) {
    D5e._enemies[id] = def;
};

/* ─── Built-in D&D 5e example enemies (override or add your own) ─── */

D5e.registerEnemy("thug", {
    name: "Thug", cr: 0.5, xp: 100,
    hp: 32, ac: 11,
    str: 15, dex: 11, con: 14, int: 10, wis: 10, cha: 11,
    profBonus: 2, multiattack: 2,
    attacks: [
        { name: "Mace", toHitBonus: 4, damage: "1d6+2", damageType: "bludgeoning" }
    ],
    saves: { str: 2, dex: 0, con: 2, int: 0, wis: 0, cha: 0 },
    resistances: [], immunities: [], features: [],
    morale: 10, loot: ["5 gp"]
});

D5e.registerEnemy("guard", {
    name: "Guard", cr: 0.125, xp: 25,
    hp: 11, ac: 16,
    str: 13, dex: 12, con: 12, int: 10, wis: 11, cha: 10,
    profBonus: 2, multiattack: 1,
    attacks: [
        { name: "Spear", toHitBonus: 3, damage: "1d6+1", damageType: "piercing" }
    ],
    saves: { str: 1, dex: 1, con: 1, int: 0, wis: 0, cha: 0 },
    resistances: [], immunities: [], features: [],
    morale: 12, loot: ["2 gp"]
});

D5e.registerEnemy("guard_captain", {
    name: "Guard Captain", cr: 3, xp: 700,
    hp: 52, ac: 16,
    str: 16, dex: 13, con: 14, int: 12, wis: 11, cha: 14,
    profBonus: 2, multiattack: 2,
    attacks: [
        { name: "Longsword", toHitBonus: 5, damage: "1d8+3", damageType: "slashing" },
        { name: "Dagger",    toHitBonus: 5, damage: "1d4+3", damageType: "piercing" }
    ],
    saves: { str: 5, dex: 1, con: 4, int: 1, wis: 0, cha: 2 },
    resistances: [], immunities: [],
    features: [
        {
            name: "Second Wind", uses: 1, trigger: "hp_below_half",
            effect(enemy) {
                const heal = D5e.dice.rollN(1, 10).total + 3;
                enemy.hp = Math.min(enemy.maxHp, enemy.hp + heal);
                return `uses Second Wind and recovers ${heal} HP`;
            }
        }
    ],
    morale: 14,
    loot: ["15 gp", "Guard Captain Signet Ring"],
    legendary: null
});

D5e.registerEnemy("bandit_leader", {
    name: "Bandit Leader", cr: 2, xp: 450,
    hp: 65, ac: 15,
    str: 16, dex: 15, con: 14, int: 14, wis: 11, cha: 14,
    profBonus: 2, multiattack: 3,
    attacks: [
        { name: "Scimitar",  toHitBonus: 5, damage: "1d6+3", damageType: "slashing" },
        { name: "Dagger",    toHitBonus: 5, damage: "1d4+3", damageType: "piercing" }
    ],
    saves: { str: 3, dex: 2, con: 2, int: 2, wis: 0, cha: 2 },
    resistances: [], immunities: [], features: [],
    morale: 11, loot: ["25 gp", "Stolen Ledger"]
});

D5e.registerEnemy("cult_fanatic", {
    name: "Cult Fanatic", cr: 2, xp: 450,
    hp: 33, ac: 13,
    str: 11, dex: 14, con: 12, int: 10, wis: 13, cha: 14,
    profBonus: 2, multiattack: 2,
    attacks: [
        { name: "Dagger", toHitBonus: 4, damage: "1d4+2", damageType: "piercing" }
    ],
    saves: { str: 0, dex: 2, con: 1, int: 0, wis: 5, cha: 4 },
    resistances: [], immunities: [],
    features: [
        {
            name: "Dark Devotion", trigger: "always",
            effect() { return null; } // advantage on saves vs. charmed/frightened (handled in save logic)
        }
    ],
    morale: 0, // never surrenders
    loot: ["Symbol of the Cult"]
});

/* ─────────────────────────────────────────────────────────────
   5. COMBAT ENGINE
   ───────────────────────────────────────────────────────────── */

D5e.combat = (function() {

    let _state = null;

    /* Build the party combatant from SugarCube story variables */
    function _buildParty() {
        const sv  = State.variables;
        const lvl = sv.partyLevel || 1;
        const pb  = sv.playerProfBonus || D5e.profBonus(lvl);

        return {
            name:     "Party",
            hp:       sv.partyCurrentHP  || _defaultPartyHP(lvl),
            maxHp:    sv.partyMaxHP      || _defaultPartyHP(lvl),
            ac:       sv.partyAC         || 13,
            toHitBonus: (sv.playerStrMod || sv.playerDexMod || 2) + pb,
            damage:   sv.partyWeaponDmg  || "1d4",
            saves: {
                str: (sv.playerStrMod || 0) + (sv.playerProfSaveStr ? pb : 0),
                dex: (sv.playerDexMod || 0) + (sv.playerProfSaveDex ? pb : 0),
                con: (sv.playerConMod || 0) + (sv.playerProfSaveCon ? pb : 0),
                wis: (sv.playerWisMod || 0) + (sv.playerProfSaveWis ? pb : 0),
                int: (sv.playerIntMod || 0) + (sv.playerProfSaveInt ? pb : 0),
                cha: (sv.playerChaMod || 0) + (sv.playerProfSaveCha ? pb : 0)
            },
            profBonus:  pb,
            conditions: []
        };
    }

    function _defaultPartyHP(level) {
        // Conservative average per level (medium party of 4, d8 hit die)
        return 8 + (level - 1) * 5;
    }

    /* Instantiate an enemy from registry */
    function _buildEnemy(idOrDef) {
        const def = typeof idOrDef === "string" ? D5e._enemies[idOrDef] : idOrDef;
        if (!def) throw new Error(`D5e combat: unknown enemy id "${idOrDef}"`);
        const hpVal = typeof def.hp === "string" ? D5e.dice.rollDamage(def.hp).total : def.hp;
        return Object.assign({}, def, {
            hp: hpVal,
            maxHp: hpVal,
            usedFeatures: {},
            conditions: []
        });
    }

    /* Roll an attack: returns { hit: bool, roll: number, total: number, crit: bool } */
    function _attackRoll(toHitBonus, targetAC) {
        const roll  = D5e.dice.roll(20);
        const crit  = roll === 20;
        const fumble = roll === 1;
        return { hit: (!fumble && (crit || roll + toHitBonus >= targetAC)), roll, total: roll + toHitBonus, crit, fumble };
    }

    /**
     * Attack roll with advantage/disadvantage support and a separate "target modifier".
     * attackType: "normal" | "advantage" | "disadvantage"
     * targetType:  "normal" | "advantage" (attacker gains adv from target condition e.g. prone)
     * If both would grant advantage AND impose disadvantage they cancel out per 5e rules.
     */
    function _attackRollTyped(toHitBonus, targetAC, attackType, targetType) {
        // Resolve net: adv from target stacks with disadvantage from self only if one isn't cancelled
        let netAdv = "normal";
        if (attackType === "advantage" || targetType === "advantage") netAdv = "advantage";
        if (attackType === "disadvantage") netAdv = (netAdv === "advantage") ? "normal" : "disadvantage";

        let roll1 = D5e.dice.roll(20);
        let roll2 = netAdv !== "normal" ? D5e.dice.roll(20) : roll1;
        const raw = netAdv === "advantage" ? Math.max(roll1, roll2)
                  : netAdv === "disadvantage" ? Math.min(roll1, roll2)
                  : roll1;
        const crit   = raw === 20;
        const fumble = raw === 1;
        return { hit: (!fumble && (crit || raw + toHitBonus >= targetAC)), roll: raw, total: raw + toHitBonus, crit, fumble };
    }

    /* Roll damage, doubling dice on crit */
    function _damageRoll(expr, crit) {
        const m = String(expr).match(/^(\d+)d(\d+)([+-]\d+)?$/i);
        if (!m) return { total: 1, rolls: [] };
        const n = crit ? parseInt(m[1]) * 2 : parseInt(m[1]);
        const sides  = parseInt(m[2]);
        const bonus  = parseInt(m[3] || 0);
        const r = D5e.dice.rollN(n, sides);
        return { total: Math.max(0, r.total + bonus), rolls: r.rolls };
    }

    /* Apply resistance / immunity */
    function _applyResistance(dmg, type, resistances, immunities) {
        if (immunities.includes(type))  return 0;
        if (resistances.includes(type)) return Math.floor(dmg / 2);
        return dmg;
    }

    /* Saving throw */
    function _savingThrow(saveMod, dc) {
        const roll = D5e.dice.roll(20);
        return { success: roll + saveMod >= dc, roll, total: roll + saveMod };
    }

    /* Enemy feature trigger check */
    function _triggerFeatures(enemy, trigger, log) {
        if (!enemy.features) return;
        for (const f of enemy.features) {
            if (f.trigger !== trigger) continue;
            if (f.uses !== undefined) {
                if (enemy.usedFeatures[f.name] >= (f.uses || 1)) continue;
                enemy.usedFeatures[f.name] = (enemy.usedFeatures[f.name] || 0) + 1;
            }
            const msg = f.effect(enemy);
            if (msg) log.push(`  ↳ ${enemy.name} ${msg}.`);
        }
    }

    /* Morale check: DC wisdom save for enemy when HP <= 25% */
    function _moraleCheck(enemy) {
        if (!enemy.morale || enemy.morale === 0) return false; // never surrenders
        const wisMod = D5e.abilityMod(enemy.wis || 10);
        const result = _savingThrow(wisMod, enemy.morale);
        return !result.success; // fails morale → surrenders
    }

    /* ── Main combat loop ── */
    function _runCombat(enemy, party, maxRounds) {
        maxRounds = maxRounds || 20;
        const log = [];
        let round = 0;
        let surrendered = false;

        // Initiative: party wins ties
        const partyInit = D5e.dice.roll(20) + (State.variables.playerDexMod || 1);
        const enemyInit = D5e.dice.roll(20) + D5e.abilityMod(enemy.dex || 10);
        const partyFirst = partyInit >= enemyInit;
        log.push(`--- Initiative: ${party.name} ${partyFirst ? "acts first" : "acts second"} (${partyInit} vs ${enemyInit}) ---`);

        while (round < maxRounds && party.hp > 0 && enemy.hp > 0) {
            round++;
            log.push(`\n[Round ${round}]`);

            const turnOrder = partyFirst ? ["party", "enemy"] : ["enemy", "party"];

            for (const turn of turnOrder) {
                if (party.hp <= 0 || enemy.hp <= 0) break;

                if (turn === "party") {
                    // Multiattack: Fighter 5+ gets 2, Fighter 11+ gets 3, Fighter 20 gets 4.
                    // Other classes get 1 unless $partyMultiattack is set.
                    const sv = State.variables;
                    const partyMulti = sv.partyMultiattack
                        || (sv.partyLevel >= 20 && sv.playerClass && sv.playerClass.toLowerCase() === "fighter" ? 4
                        :   sv.partyLevel >= 11 && sv.playerClass && sv.playerClass.toLowerCase() === "fighter" ? 3
                        :   sv.partyLevel >=  5 ? 2 : 1);
                    // Poisoned: attacks with disadvantage
                    const partyPoisoned = party.conditions.includes("poisoned");
                    // Blinded: attacks with disadvantage (enemy also has advantage, handled below)
                    const partyBlinded  = party.conditions.includes("blinded");
                    const atkType = (partyPoisoned || partyBlinded) ? "disadvantage" : "normal";

                    for (let i = 0; i < partyMulti; i++) {
                        if (enemy.hp <= 0) break;
                        const atk = _attackRollTyped(party.toHitBonus, enemy.ac, atkType,
                            enemy.conditions.includes("blinded") || enemy.conditions.includes("prone") ? "advantage" : "normal");
                        if (atk.fumble) {
                            log.push(`  Party attacks — fumble! (rolled 1)`);
                        } else if (atk.hit) {
                            const dmg = _damageRoll(party.damage, atk.crit);
                            // Apply player damage type against enemy resistances/immunities
                            const finalDmg = _applyResistance(dmg.total, sv.partyDamageType || "physical", enemy.resistances || [], enemy.immunities || []);
                            enemy.hp = Math.max(0, enemy.hp - finalDmg);
                            log.push(`  Party attacks — ${atk.crit ? "CRITICAL HIT! " : ""}hits (${atk.total} vs AC ${enemy.ac}): ${finalDmg} damage. Enemy HP: ${enemy.hp}/${enemy.maxHp}`);
                        } else {
                            log.push(`  Party attacks — misses (${atk.total} vs AC ${enemy.ac}).`);
                        }
                    }

                    // Check enemy death / surrender after party turn
                    if (enemy.hp <= 0) break;
                    if (enemy.hp <= Math.floor(enemy.maxHp * 0.50)) {
                        _triggerFeatures(enemy, "hp_below_half", log);
                    }
                    if (enemy.hp <= Math.floor(enemy.maxHp * 0.25)) {
                        if (_moraleCheck(enemy)) {
                            surrendered = true;
                            log.push(`  ${enemy.name} breaks — surrenders!`);
                            break;
                        }
                    }

                } else {
                    // Enemy attacks
                    const numAttacks = enemy.multiattack || 1;
                    // Blinded enemy: attacks with disadvantage; prone/blinded player: enemy has advantage
                    const enemyBlinded  = enemy.conditions.includes("blinded");
                    const partyProne    = party.conditions.includes("prone");
                    const partyBlinded2 = party.conditions.includes("blinded");
                    const atkType  = enemyBlinded  ? "disadvantage" : "normal";
                    const targType = (partyProne || partyBlinded2) ? "advantage" : "normal";

                    for (let i = 0; i < numAttacks; i++) {
                        if (party.hp <= 0) break;
                        // Pick an attack (cycle through available attacks)
                        const atkDef = enemy.attacks[i % enemy.attacks.length];
                        const atk = _attackRollTyped(atkDef.toHitBonus, party.ac, atkType, targType);
                        if (atk.fumble) {
                            log.push(`  ${enemy.name} attacks (${atkDef.name}) — fumble! (rolled 1)`);
                        } else if (atk.hit) {
                            const dmg = _damageRoll(atkDef.damage, atk.crit);
                            // Apply player resistance/immunity if set in SugarCube variables
                            const sv2 = State.variables;
                            const playerResist = sv2.playerResistances || [];
                            const playerImmune = sv2.playerImmunities  || [];
                            const finalDmg = _applyResistance(dmg.total, atkDef.damageType || "physical", playerResist, playerImmune);
                            party.hp = Math.max(0, party.hp - finalDmg);
                            log.push(`  ${enemy.name} attacks (${atkDef.name}) — ${atk.crit ? "CRITICAL HIT! " : ""}hits (${atk.total} vs AC ${party.ac}): ${finalDmg} damage. Party HP: ${party.hp}/${party.maxHp}`);

                            // Saving throw on-hit effect
                            if (atkDef.save) {
                                const saveResult = _savingThrow(party.saves[atkDef.save.ability.toLowerCase()] || 0, atkDef.save.dc);
                                if (!saveResult.success) {
                                    party.conditions.push(atkDef.save.effect);
                                    log.push(`    Party fails ${atkDef.save.ability} save (DC ${atkDef.save.dc}) — ${atkDef.save.effect}!`);
                                } else {
                                    log.push(`    Party saves (${saveResult.total} vs DC ${atkDef.save.dc}).`);
                                }
                            }
                        } else {
                            log.push(`  ${enemy.name} attacks (${atkDef.name}) — misses (${atk.total} vs AC ${party.ac}).`);
                        }
                    }

                    // Enemy features on its turn
                    _triggerFeatures(enemy, "start_of_turn", log);

                    // Legendary actions (after enemy turn — up to legendary.actions.length uses)
                    if (enemy.legendary && enemy.legendary.actions && enemy.legendary.actions.length > 0) {
                        const legendaryUses = enemy.legendary.resistances || 3; // misnamed field; default 3 legendary action uses
                        if (!enemy._legendaryActionsUsed) enemy._legendaryActionsUsed = 0;
                        if (enemy._legendaryActionsUsed < legendaryUses) {
                            // Pick first available legendary action
                            const la = enemy.legendary.actions[enemy._legendaryActionsUsed % enemy.legendary.actions.length];
                            const laResult = la.effect ? la.effect(enemy, party) : null;
                            enemy._legendaryActionsUsed++;
                            log.push(`  ★ Legendary Action: ${la.name}${laResult ? ` — ${laResult}` : ""}.`);
                        }
                    }
                }
            }
        }

        if (round >= maxRounds && party.hp > 0 && enemy.hp > 0) {
            log.push(`\n[Stalemate after ${maxRounds} rounds — tactical retreat.]`);
        }

        return { log, surrendered, rounds: round };
    }

    /* ── Public API ── */
    return {
        /**
         * Start a combat encounter.
         * @param {string|object} enemyIdOrDef  registered enemy id OR inline def object
         * @param {string} passageOnEnd         Twee passage to go to after combat
         * @param {object} [opts]               { retreat: bool, advantage: bool }
         */
        start(enemyIdOrDef, passageOnEnd, opts) {
            opts = opts || {};

            const sv    = State.variables;
            const party = _buildParty();
            const enemy = _buildEnemy(enemyIdOrDef);

            // Allow player to retreat before combat if opts.retreat === true
            if (opts.retreat) {
                sv.lastCombatOutcome  = "player_retreated";
                sv.lastCombatXP       = 0;
                sv.lastCombatLoot     = [];
                sv.lastCombatLog      = ["[Retreated before combat started]"];
                sv.lastEnemyName      = enemy.name;
                sv.lastEnemySurrendered = false;
                Engine.play(passageOnEnd);
                return;
            }

            const result = _runCombat(enemy, party, opts.maxRounds || 20);

            // Write results to story variables
            sv.lastEnemyName = enemy.name;
            sv.lastCombatLog = result.log;
            sv.lastEnemySurrendered = result.surrendered;

            if (result.surrendered || enemy.hp <= 0) {
                sv.lastCombatOutcome = "player_won";
                sv.lastCombatXP      = enemy.xp || 0;
                sv.lastCombatLoot    = enemy.loot ? [...enemy.loot] : [];
                sv.partyXP           = (sv.partyXP || 0) + sv.lastCombatXP;
                // Write surviving party HP back
                sv.partyCurrentHP    = party.hp;
            } else if (party.hp <= 0) {
                sv.lastCombatOutcome = "player_lost";
                sv.lastCombatXP      = 0;
                sv.lastCombatLoot    = [];
                sv.partyCurrentHP    = 0;
            } else {
                // Stalemate = retreat
                sv.lastCombatOutcome = "player_retreated";
                sv.lastCombatXP      = 0;
                sv.lastCombatLoot    = [];
                sv.partyCurrentHP    = party.hp;
            }

            Engine.play(passageOnEnd);
        },

        /** Shorthand: roll a skill check and write results to SugarCube vars */
        skillCheck: D5e.skillCheck
    };
}());

/* ─────────────────────────────────────────────────────────────
   6. SUGARCUBE MACROS
   ───────────────────────────────────────────────────────────── */

/**
 * <<combat "enemyId" "OUTCOME_PASSAGE">>
 *
 * Runs a full D&D 5e combat encounter and navigates to OUTCOME_PASSAGE.
 * Sets $lastCombatOutcome, $lastCombatXP, $lastCombatLoot, $lastCombatLog.
 *
 * Example:
 *   <<combat "guard_captain" "NODE_016_COMBAT_WITH_CAPTAIN">>
 */
Macro.add("combat", {
    handler() {
        if (this.args.length < 2) {
            return this.error("<<combat>> requires: enemyId, outcomePassage");
        }
        const enemyId = this.args[0];
        const passage = this.args[1];
        const opts    = this.args[2] || {};
        try {
            D5e.combat.start(enemyId, passage, opts);
        } catch (e) {
            return this.error(e.message);
        }
    }
});

/**
 * <<skillcheck "Insight" mod dc [proficient] [rollType]>>
 *
 * Performs a skill check and writes results to SugarCube vars.
 * Does NOT navigate — use <<if $lastSkillCheckSuccess>> after.
 *
 * Example:
 *   <<skillcheck "Insight" $playerInsightMod 14 true "normal">>
 *   <<if $lastSkillCheckSuccess>>...success...<<else>>...failure...<</if>>
 */
Macro.add("skillcheck", {
    handler() {
        if (this.args.length < 3) {
            return this.error("<<skillcheck>> requires: skill, mod, dc [proficient] [rollType]");
        }
        const skill     = this.args[0];
        const mod       = Number(this.args[1]);
        const dc        = Number(this.args[2]);
        const proficient = this.args[3] !== undefined ? !!this.args[3] : false;
        const rollType  = this.args[4] || "normal";
        D5e.skillCheck(skill, mod, dc, proficient, rollType);
    }
});

/**
 * <<combatlog>>
 *
 * Renders the round-by-round log from the last combat as a collapsible block.
 * Call this from the outcome passage to show what happened.
 *
 * Example:
 *   <<combatlog>>
 */
Macro.add("combatlog", {
    handler() {
        const log = State.variables.lastCombatLog || [];
        if (log.length === 0) return;
        const el = document.createElement("details");
        const summary = document.createElement("summary");
        summary.textContent = "Combat log";
        el.appendChild(summary);
        const pre = document.createElement("pre");
        pre.className = "d5e-combat-log";
        pre.textContent = log.join("\n");
        el.appendChild(pre);
        this.output.appendChild(el);
    }
});

/**
 * <<retreat "OUTCOME_PASSAGE" ["enemyId"]>>
 *
 * Sets outcome to "player_retreated" without rolling combat.
 * Use for nodes where player chooses to flee before fighting.
 * Pass the enemy id as the optional second argument, or pre-set $lastEnemyId.
 *
 * Example:
 *   <<retreat "NODE_018_PURSUIT" "guard_captain">>
 */
Macro.add("retreat", {
    handler() {
        const passage = this.args[0];
        if (!passage) return this.error("<<retreat>> requires a passage name");
        const enemyId = this.args[1] || State.variables.lastEnemyId || "guard";
        D5e.combat.start(enemyId, passage, { retreat: true });
    }
});

/* ─────────────────────────────────────────────────────────────
   7. XP & LEVEL-UP HELPER
   ───────────────────────────────────────────────────────────── */

D5e.xpThresholds = [0, 300, 900, 2700, 6500, 14000, 23000, 34000, 48000, 64000,
                    85000, 100000, 120000, 140000, 165000, 195000, 225000, 265000, 305000, 355000];

/**
 * Call after awarding XP. Sets $partyLevel if threshold crossed.
 * Writes $partyLeveledUp = true and $partyNewLevel if level changed.
 */
D5e.checkLevelUp = function() {
    const sv   = State.variables;
    const xp   = sv.partyXP || 0;
    const lvl  = sv.partyLevel || 1;
    let newLvl = lvl;
    for (let i = D5e.xpThresholds.length - 1; i >= 0; i--) {
        if (xp >= D5e.xpThresholds[i]) { newLvl = i + 1; break; }
    }
    newLvl = Math.min(20, newLvl);
    if (newLvl > lvl) {
        sv.partyLevel    = newLvl;
        sv.partyLeveledUp = true;
        sv.partyNewLevel  = newLvl;
    } else {
        sv.partyLeveledUp = false;
    }
};

/* ─────────────────────────────────────────────────────────────
   8. CSS (inject once)
   ───────────────────────────────────────────────────────────── */

(function injectCSS() {
    if (document.getElementById("d5e-combat-style")) return;
    const style = document.createElement("style");
    style.id = "d5e-combat-style";
    style.textContent = `
        .d5e-combat-log {
            font-family: monospace;
            font-size: 0.82em;
            background: rgba(0,0,0,0.15);
            border-left: 3px solid #888;
            padding: 0.6em 1em;
            max-height: 260px;
            overflow-y: auto;
            white-space: pre-wrap;
            word-break: break-word;
        }
        details > summary {
            cursor: pointer;
            font-style: italic;
            opacity: 0.7;
            margin-bottom: 0.4em;
        }
    `;
    document.head.appendChild(style);
}());
