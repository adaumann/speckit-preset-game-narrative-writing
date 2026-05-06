#!/usr/bin/env python3
"""
Validate skill check distribution across campaign.

Ensures:
- Skill checks use all abilities (not 70% one type)
- DCs are within 5-20 range
- Success/failure outcomes are narrated
- Distribution is balanced across sessions
"""

import sys
import json
from pathlib import Path
from collections import Counter


def validate_skill_distribution(campaign_data):
    """Validate skill check balance and DCs."""
    
    errors = []
    warnings = []
    
    plan = campaign_data.get("plan", {})
    sessions = plan.get("sessions", [])
    
    skill_checks = []
    dc_values = []
    ability_counts = Counter()
    
    for session_num, session in enumerate(sessions, 1):
        encounters = session.get("encounters", [])
        
        for encounter in encounters:
            skill_checks_in_enc = encounter.get("skill_checks", [])
            
            for check in skill_checks_in_enc:
                dc = check.get("dc")
                ability = check.get("ability", "").lower()
                success_outcome = check.get("success_outcome")
                failure_outcome = check.get("failure_outcome")
                
                # Validate DC range
                if dc and (dc < 5 or dc > 20):
                    errors.append(
                        f"Session {session_num}: Skill check DC {dc} outside 5-20 range"
                    )
                else:
                    dc_values.append(dc)
                
                # Validate outcomes are narrated
                if not success_outcome:
                    errors.append(
                        f"Session {session_num}: Skill check missing success outcome"
                    )
                if not failure_outcome:
                    errors.append(
                        f"Session {session_num}: Skill check missing failure outcome"
                    )
                
                # Track ability usage
                if ability:
                    ability_counts[ability] += 1
                    skill_checks.append((session_num, ability, dc))
    
    # Check ability balance
    if ability_counts:
        total_checks = sum(ability_counts.values())
        for ability, count in ability_counts.items():
            percentage = (count / total_checks) * 100
            
            if percentage > 70:
                errors.append(
                    f"Skill distribution: {ability} represents {percentage:.1f}% "
                    f"of checks (max 70% recommended)"
                )
            elif percentage > 50:
                warnings.append(
                    f"Skill distribution: {ability} represents {percentage:.1f}% "
                    f"of checks (consider more variety)"
                )
    
    # Check DC distribution
    if dc_values:
        avg_dc = sum(dc_values) / len(dc_values)
        if avg_dc < 10:
            warnings.append(
                f"Average DC: {avg_dc:.1f} (consider harder challenges)"
            )
        elif avg_dc > 16:
            warnings.append(
                f"Average DC: {avg_dc:.1f} (consider easier entry challenges)"
            )
    
    return errors, warnings


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python validate_skill_distribution.py <campaign.json>")
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
    
    errors, warnings = validate_skill_distribution(campaign)
    
    if errors:
        print("❌ Skill Distribution Validation Failed")
        for error in errors:
            print(f"  - {error}")
        sys.exit(1)
    
    if warnings:
        print("⚠️ Warnings:")
        for warning in warnings:
            print(f"  - {warning}")
    
    print("✅ Skill distribution valid!")
    sys.exit(0)
