---
description: Generate or update a Mermaid flowchart of the node graph with mechanic trigger annotations, ending markers, and act boundary labels. For RPG campaigns (tabletop D&D/Pathfinder/Shadowrun and computer game), visualizes session structure, companion/faction branching, playstyle routes, and accessibility variant logic.
handoffs:
  - label: Update Plan
    agent: speckit.plan
    prompt: The plan.md source needs updating based on the diagram
    send: false
  - label: Analyze Unreachable Nodes
    agent: speckit.analyze
    prompt: Check for unreachable nodes visible in the diagram
    send: true
---

# speckit.flowmap

**RPG Campaign Support**: Adapts flowmaps for tabletop (session structure with SESSION-1 through SESSION-N, companion recruitment/loyalty branching, faction reputation decision trees) and computer game (chapter structure with CHAPTER-1 through CHAPTER-N, playstyle route commitment and divergence, accessibility variant logic).

Generate a Mermaid flowchart of the full node graph. Annotates mechanic triggers, ending nodes, and act boundaries.

## User Input

Provide one of:
- Nothing — generate full flowchart from all node files and `plan.md`
- `--act [N]` — diagram one act only
- `--endings` — highlight ending nodes only
- `--hooks` — annotate mechanic trigger types on edges

Optional flags:
- `--act [N]` — scope to one act
- `--endings` — bold or colour-code ending nodes
- `--hooks` — add edge labels for mechanic triggers (trust, flag, inventory check)
- `--output [filename]` — write to a named file instead of printing

## Pre-Execution Checks

**Auto-detect platform and ruleset** (for RPG campaigns):
- Load `constitution.md`
- Extract `[PLATFORM]` (tabletop/computer) and `[RULESET]` (D&D 5e/Pathfinder 2e/Shadowrun 6e)
- Set SESSION object {platform, ruleset, mechanics}
- If RPG: Load `plan.md` for session/chapter structure, `companions.md`, `factions.md`, `mechanics-[RULESET].md`

**Standard checks**:
1. Load `specs/plan.md` — authoritative node graph source.
2. Load all node files in `nodes/` to extract actual choice targets.
3. If node files exist: prefer actual node file links over plan.md estimates.

## Outline

1. **Build graph model** (with RPG enhancements if [PLATFORM] detected):

**For Tabletop RPG**:
   - Session structure: GROUP nodes by SESSION-N boundary (add `%% SESSION-1 %%` comment dividers)
   - Companion recruitment: Branch nodes labeled `NODE-XXX[Recruit: Theron]`, edges showing recruitment outcomes (joined/rejected)
   - Companion loyalty: Edges labeled `[+loyalty(theron), -loyalty(sera)]` showing loyalty changes
   - Faction reputation: Edges labeled `[+faction_rep(Temple), -faction_rep(Thieves)]` showing reputation shifts
   - Campaign-level state: Highlight key decision nodes that affect multiple sessions (e.g., alliance choices)

**For Computer Game**:
   - Chapter structure: GROUP nodes by CHAPTER-N boundary (add `%% CHAPTER-1 %%` comment dividers)
   - Route commitment node: Highlight CHAPTER-2 route choice node with special styling (e.g., `NODE_ROUTE_CHOICE[🎯 Commit to Route]`)
   - Route branching: Color-code or label route-specific nodes:
     - STEALTH nodes: `NODE_S_XXX{Stealth}` or styled with `::: stealth-route`
     - COMBAT nodes: `NODE_C_XXX{Combat}` or styled with `::: combat-route`
     - DIPLOMACY nodes: `NODE_D_XXX{Diplomacy}` or styled with `::: diplomacy-route`
   - Accessibility variant nodes: If accessibility branching exists, mark nodes with `[accessibility variant]` label
   - Convergence points: Highlight nodes where routes reconverge with `:::convergence` styling

**Standard elements** (all platforms):
   - Every node becomes a Mermaid node (`NODE_001[Opening]`)
   - Every choice becomes a directed edge (`NODE_001 -->|choice label| NODE_002`)
   - Gated choices: annotate the condition on the edge label (e.g. `-->|"Trust ≥ 75: Tell me"| NODE_005`)
   - Terminal/ending nodes: marked with double-bracket shape `NODE_END_A[[Ending A]]`
   - Act boundaries: add comment dividers `%% ACT 1 %%`
   - **Hub nodes**: if a node is tagged `hub` in `plan.md`, render it with a stadium shape `NODE_HUB([Hub Label])` and annotate topic sub-nodes as `:::hub-topic`; add a `%% DIALOGUE HUB %%` comment above the hub node group

2. **Mechanic annotations** (if `--hooks`):
   - Trust shift: append `[±N trust]` to edge label
   - Companion loyalty shift: append `[loyalty(companion)±N]` to edge label (for tabletop RPG)
   - Faction reputation shift: append `[faction_rep(faction)±N]` to edge label (for tabletop RPG)
   - Flag set: append `[flag_name=true]` to edge label
   - Inventory change: append `[+item / -item]` to edge label
   - Ending condition trigger: append `[end_A_progress+1]`

3. **Unreachable nodes** (cross-reference with speckit.analyze):
   - Shade or mark nodes with no incoming edges as `:::orphan`

4. **RPG Campaign Flowmap Notes** (if [PLATFORM] detected):

**For Tabletop RPG**:
   - Session grouping: Visually separate SESSION-1 through SESSION-N with section comments
   - Companion branches: Show companion recruitment in SESSION-2, then track loyalty changes through SESSION-3-N
   - Faction decision trees: Map faction reputation changes and their effects on available quests/NPCs
   - Campaign convergence: Identify nodes where multiple session branches meet (e.g., all paths reconverge for final boss)
   
**For Computer Game**:
   - Chapter grouping: Visually separate CHAPTER-1 through CHAPTER-N with section comments
   - Route commitment: Clearly mark CHAPTER-2 route choice as decision point; show route divergence from that point forward
   - Route-specific nodes: Group STEALTH/COMBAT/DIPLOMACY nodes together to show route structure
   - Accessibility variants: If accessibility mode affects branching, show variant logic
   - Convergence strategy: Identify if/when routes reconverge before ending

5. **Output**:
   ```mermaid
   flowchart TD
   %% SESSION-1 or CHAPTER-1 %%
   NODE_001[Opening]
   NODE_001 -->|"A: Ask for help"| NODE_002A
   NODE_001 -->|"B: Walk away"| NODE_002B
   ...
   NODE_END_A[[Ending A — Redemption]]
   NODE_END_B[[Ending B — Exile]]
   ```
   - Write to `flowmap-diagram.md` or specified `--output` file
   - Report: "Diagram generated: [N] nodes, [N] edges, [N] ending nodes."
   - If RPG campaign: Add "Sessions: [N]" (tabletop) or "Chapters: [N], Routes: [N]" (computer) to report

---

## RPG Campaign Flowmap Notes

### Tabletop Campaign Flowmap Structure

**Session-Based Grouping**:
- Divide flowmap into SESSION-1 through SESSION-N sections (each session is a bounded play session)
- Use comment dividers: `%% SESSION-1: The Beginning %%` (optionally include session name/focus)
- All nodes in SESSION-N section are connected to nodes in SESSION-(N+1) section via decision branches
- Example:
  ```
  %% SESSION-1: Refugees Arrive %%
  NODE_S1_001[Opening: Refugees at Gate]
  NODE_S1_001 -->|"Welcome them"| NODE_S1_002A
  NODE_S1_001 -->|"Turn them away"| NODE_S1_002B
  NODE_S1_002A & NODE_S1_002B -->|"[End SESSION-1]"| NODE_S2_001
  
  %% SESSION-2: Investigate Refugees %%
  NODE_S2_001[Refugees Settle]
  ...
  ```

**Companion Recruitment Branching**:
- Companion recruitment typically happens in SESSION-2 or SESSION-3
- Show companion recruitment as decision node: `NODE_S2_RECRUIT[Recruit Companion?]`
- Each companion option becomes a branch: `-->|"Recruit Theron"| NODE_S2_THERON_YES`
- Loyalty tracking: Show loyalty changes on edges in subsequent sessions
- Example:
  ```
  NODE_S2_RECRUIT[Recruit Companion?]
  NODE_S2_RECRUIT -->|"Recruit Theron [loyalty(theron)=0]"| NODE_S3_THERON
  NODE_S2_RECRUIT -->|"Recruit Sera [loyalty(sera)=0]"| NODE_S3_SERA
  NODE_S2_RECRUIT -->|"Solo campaign"| NODE_S3_SOLO
  
  NODE_S3_THERON -->|"Defend Temple [+loyalty(theron)]"| NODE_S4_A
  NODE_S3_THERON -->|"Help Thieves [−loyalty(theron)]"| NODE_S4_B
  ```

**Faction Reputation Decision Trees**:
- Map faction reputation branches alongside companion branches
- Show faction_reputation changes on edges
- Example:
  ```
  NODE_S3_CHOICE[Choose Side]
  NODE_S3_CHOICE -->|"Support Temple [+faction_rep(Temple)]"| NODE_S4_TEMPLE
  NODE_S3_CHOICE -->|"Support Thieves [+faction_rep(Thieves)]"| NODE_S4_THIEVES
  NODE_S3_CHOICE -->|"Stay neutral"| NODE_S4_NEUTRAL
  ```

**Campaign-Level State Convergence**:
- Identify nodes where multiple session branches meet (convergence points)
- Example: SESSION-8 might have only 1-2 nodes despite 5-6 path variations from SESSION-2-7 (all paths funnel to final boss)
- Mark convergence nodes: `NODE_S8_FINAL[Final Confrontation]` with incoming edges from multiple routes
- This shows visual simplification: many decisions lead to same final choice

**Session Interdependency Visualization**:
- Show how SESSION-N decisions affect SESSION-(N+1) options
- Example: If faction_reputation(Temple) < -2, Temple quest unavailable in SESSION-4 (show edge with conditional label)

### Computer Game Flowmap Structure

**Chapter-Based Grouping**:
- Divide flowmap into CHAPTER-1 through CHAPTER-N sections
- Use comment dividers: `%% CHAPTER-1: Escape the Prison %%`
- All nodes in CHAPTER-N section are connected to nodes in CHAPTER-(N+1) section via decision branches
- Example:
  ```
  %% CHAPTER-1: Awakening %%
  NODE_C1_001[Prison Cell]
  NODE_C1_001 -->|"Escape through door"| NODE_C1_002
  
  %% CHAPTER-2: Choose Your Path %%
  NODE_C1_END -->|"[End CHAPTER-1]"| NODE_C2_ROUTE_CHOICE
  NODE_C2_ROUTE_CHOICE[🎯 Commit to Playstyle]
  NODE_C2_ROUTE_CHOICE -->|"Stealth: Avoid detection"| NODE_C3_STEALTH_001
  NODE_C2_ROUTE_CHOICE -->|"Combat: Fight through"| NODE_C3_COMBAT_001
  NODE_C2_ROUTE_CHOICE -->|"Diplomacy: Talk your way"| NODE_C3_DIPLOMACY_001
  ```

**Route Commitment and Divergence**:
- CHAPTER-2 route choice creates the primary branch point for entire game
- After route choice: group nodes by route
- Show route-specific nodes with distinct styling/color:
  ```
  %% CHAPTER-3: Stealth Route %%
  NODE_C3_STEALTH_001[Infiltrate Compound]
  NODE_C3_STEALTH_001 -->|"Use side entrance"| NODE_C3_STEALTH_002
  NODE_C3_STEALTH_001 -->|"Climb to roof"| NODE_C3_STEALTH_003
  
  %% CHAPTER-3: Combat Route %%
  NODE_C3_COMBAT_001[Assault Compound]
  NODE_C3_COMBAT_001 -->|"Front gate attack"| NODE_C3_COMBAT_002
  NODE_C3_COMBAT_001 -->|"Side ambush"| NODE_C3_COMBAT_003
  ```

**Route Convergence Points**:
- Identify nodes where routes reconverge (typically in final chapter)
- Example: CHAPTER-4 final boss scene might have all three routes converging
- Show with converging edges: both STEALTH and COMBAT and DIPLOMACY nodes pointing to same final node
- Helps visualize: "Routes diverge at CHAPTER-2, reconverge at CHAPTER-4 final boss"

**Accessibility Variant Logic**:
- If accessibility modes affect branching logic, show variant nodes
- Example: Colorblind mode might use button shapes instead of colors, but follows same story path
- Show as parallel nodes: `NODE_C2_VISUAL[CHAPTER-2: Scene (Standard)]` and `NODE_C2_VISUAL_CB[CHAPTER-2: Scene (Colorblind)]`
- Both paths lead to same story outcomes (accessibility shouldn't create story variants, just adapt presentation)

### Flowmap Visualization Best Practices

**For Tabletop RPG Flowmaps**:
- Keep each session section compact: ideal ~8-12 nodes per session on diagram
- If session has >15 nodes, consider splitting visualization into "Session Overview" (convergence points only) and "Session Detail" (all nodes)
- Use hub nodes for complex decisions: instead of showing all sub-choices inline, create a `%% SESSION-3 DIALOGUE HUB %%` section
- Color or style key decision nodes (companion recruitment, faction choice, quest completion) differently

**For Computer Game Flowmaps**:
- CHAPTER-1-2: Show linear/simple structure (few branches)
- CHAPTER-2 route choice: Make this node visually prominent (larger, special styling, centered)
- CHAPTER-3-4: Show route-specific sections clearly separated
- Final chapter: Show convergence of all routes
- Use consistent color coding for routes (red=Combat, blue=Stealth, green=Diplomacy recommended)

**General Flowmap Clarity**:
- Avoid massive single diagrams: if >80 nodes total, break into multiple diagrams (per-session or per-route)
- Use node IDs that reflect structure: `NODE_S2_RECRUIT` is clearer than `NODE_047`
- Label high-branching nodes: if a node has 5+ outgoing edges, consider annotating with `[5-way choice]`
- Keep edge labels short: instead of full choice text, use abbreviated labels and reference external legend if needed
