#!/usr/bin/env python3
"""
Validate reputation arcs for factions across campaign.

Ensures:
- Each faction has realistic progression
- Reputation changes are cumulative
- Changes fit within -100 to 100 range
- Arc is narratively sensible
"""

import sys
import json
from pathlib import Path


def validate_reputation_arcs(campaign_data):
    """Validate faction reputation progression."""
    
    errors = []
    warnings = []
    
    factions = campaign_data.get("factions", [])
    plan = campaign_data.get("plan", {})
    sessions = plan.get("sessions", [])
    
    for faction in factions:
        faction_name = faction.get("name")
        starting_rep = faction.get("starting_reputation", 0)
        
        # Track cumulative reputation
        current_rep = starting_rep
        arc_changes = []
        
        for session_num, session in enumerate(sessions, 1):
            faction_changes = session.get("faction_changes", {})
            if faction_name in faction_changes:
                delta = faction_changes[faction_name]
                current_rep += delta
                arc_changes.append((session_num, delta, current_rep))
                
                # Check bounds
                if current_rep > 100 or current_rep < -100:
                    errors.append(
                        f"Session {session_num}: {faction_name} reputation {current_rep} "
                        f"outside -100 to 100 range"
                    )
        
        # Check arc is realistic (not too many large swings)
        if arc_changes:
            max_swing = max(abs(delta) for _, delta, _ in arc_changes)
            swings_over_20 = sum(1 for _, delta, _ in arc_changes if abs(delta) > 20)
            
            if swings_over_20 > len(arc_changes) / 2:
                warnings.append(
                    f"{faction_name}: More than half of changes are ±20+ "
                    f"(may be narratively jarring)"
                )
            
            # Check ending requirements are reachable
            endings = campaign_data.get("endings", [])
            for ending in endings:
                requirements = ending.get("requirements", {})
                faction_mins = requirements.get("faction_rep_minimums", {})
                
                if faction_name in faction_mins:
                    required_rep = faction_mins[faction_name]
                    final_rep = arc_changes[-1][2] if arc_changes else starting_rep
                    
                    if final_rep < required_rep and current_rep < required_rep:
                        warnings.append(
                            f"Ending '{ending['name']}': {faction_name} requires {required_rep} rep, "
                            f"current arc ends at {final_rep}"
                        )
    
    return errors, warnings


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python validate_reputation_arcs.py <campaign.json>")
        sys.exit(1)
    
    campaign_file = Path(sys.argv[1])
    if not campaign_file.exists():
        print(f"Error: {campaign_file} not found")
        sys.exit(1)
    
    try:
        with open(campaign_file) as f:
            campaign = json.load(f)
    except json.JSONDecodeError as e:
        print(f"Error: Invalid JSON in {campaign_file}: {e}")
        sys.exit(1)
    
    errors, warnings = validate_reputation_arcs(campaign)
    
    if errors:
        print("❌ Reputation Arc Validation Failed")
        for error in errors:
            print(f"  - {error}")
        sys.exit(1)
    
    if warnings:
        print("⚠️ Warnings:")
        for warning in warnings:
            print(f"  - {warning}")
    
    print("✅ Reputation arcs valid!")
    sys.exit(0)
