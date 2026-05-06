#!/usr/bin/env python3
"""
Validate ending gates across campaign.

Ensures:
- 2-3 endings viable at Session 8
- Exactly 1 ending viable by Session 13
- Ending lock timing respected
"""

import sys
import json
from pathlib import Path


def validate_ending_gates(campaign_data):
    """Validate ending gate progression through campaign."""
    
    errors = []
    warnings = []
    
    # Expected ending counts by gate
    session_3_min, session_3_max = 2, 4  # 2-3 endings viable
    session_8_min, session_8_max = 2, 3
    session_13_final = 1  # Exactly 1 by Session 13
    
    # Check Session 3 gate (first lock)
    session_3_viable = campaign_data.get("endings_viable_session_3", 0)
    if session_3_viable < session_3_min or session_3_viable > session_3_max:
        errors.append(
            f"Session 3: {session_3_viable} endings viable, "
            f"expected {session_3_min}-{session_3_max}"
        )
    
    # Check Session 8 gate (mid-campaign)
    session_8_viable = campaign_data.get("endings_viable_session_8", 0)
    if session_8_viable < session_8_min or session_8_viable > session_8_max:
        errors.append(
            f"Session 8: {session_8_viable} endings viable, "
            f"expected {session_8_min}-{session_8_max}"
        )
    
    # Check Session 13 gate (final lock)
    session_13_viable = campaign_data.get("endings_viable_session_13", 0)
    if session_13_viable != session_13_final:
        errors.append(
            f"Session 13: {session_13_viable} endings viable, "
            f"expected exactly {session_13_final}"
        )
    
    # Verify ending gates are achievable
    endings = campaign_data.get("endings", [])
    for ending in endings:
        requirements = ending.get("requirements", {})
        
        # Check if requirements are reachable
        if "faction_rep_minimums" in requirements:
            for faction, min_rep in requirements["faction_rep_minimums"].items():
                if min_rep > 100 or min_rep < -100:
                    errors.append(
                        f"Ending '{ending['name']}': {faction} requires {min_rep} rep "
                        f"(outside -100 to 100 range)"
                    )
        
        if "companion_requirements" in requirements:
            for companion, req in requirements["companion_requirements"].items():
                approval = req.get("approval_min")
                if approval and (approval > 100 or approval < -100):
                    errors.append(
                        f"Ending '{ending['name']}': {companion} requires {approval} approval "
                        f"(outside -100 to 100 range)"
                    )
    
    return errors, warnings


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python validate_ending_gates.py <campaign.json>")
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
    
    errors, warnings = validate_ending_gates(campaign)
    
    if errors:
        print("❌ Ending Gate Validation Failed")
        for error in errors:
            print(f"  - {error}")
        sys.exit(1)
    
    if warnings:
        print("⚠️ Warnings:")
        for warning in warnings:
            print(f"  - {warning}")
    
    print("✅ Ending gates valid!")
    sys.exit(0)
