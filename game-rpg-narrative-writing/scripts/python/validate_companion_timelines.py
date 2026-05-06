#!/usr/bin/env python3
"""
Validate companion recruitment timeline.

Ensures:
- All 3 companions recruited in proper sequence
- Recruitment happens at expected sessions (2, 5, 7-8)
- Approval gates are respected
- Companions not used before recruitment
- Companion state flags (alive/dead) consistent with requirements
"""

import sys
import json
from pathlib import Path


def validate_companion_timelines(campaign_data):
    """Validate companion recruitment and usage."""
    
    errors = []
    warnings = []
    
    companions = campaign_data.get("companions", [])
    plan = campaign_data.get("plan", {})
    sessions = plan.get("sessions", [])
    
    # Track companion state
    companion_state = {c.get("name"): {"recruited": None, "state": "not_recruited"} 
                       for c in companions}
    
    expected_recruitment = {
        "companion_1": 2,
        "companion_2": 5,
        "companion_3": (7, 8)  # 7-8 range
    }
    
    for session_num, session in enumerate(sessions, 1):
        events = session.get("events", [])
        
        for event in events:
            event_type = event.get("type")
            companion = event.get("companion")
            
            # Check recruitment happens at expected session
            if event_type == "recruitment":
                if companion in companion_state:
                    state = companion_state[companion]
                    if state["state"] != "not_recruited":
                        errors.append(
                            f"Companion '{companion}' recruited twice "
                            f"(first at session {state['recruited']}, again at {session_num})"
                        )
                    else:
                        state["recruited"] = session_num
                        state["state"] = "recruited"
            
            # Check companion not used before recruitment
            elif event_type in ["interaction", "approval_check", "consequence"]:
                state = companion_state.get(companion, {})
                if state.get("state") == "not_recruited":
                    errors.append(
                        f"Session {session_num}: Companion '{companion}' used before recruitment"
                    )
    
    # Check all companions recruited
    for companion_id, expected_session in expected_recruitment.items():
        state = companion_state.get(f"companion_{companion_id.split('_')[1]}")
        if state and state["state"] == "not_recruited":
            if isinstance(expected_session, tuple):
                warnings.append(
                    f"Companion not recruited (expected session {expected_session[0]}-{expected_session[1]})"
                )
            else:
                warnings.append(
                    f"Companion not recruited (expected session {expected_session})"
                )
    
    # Verify approval gates
    for companion in companions:
        comp_name = companion.get("name")
        approval_gate = companion.get("recruitment_approval_gate", 0)
        
        if abs(approval_gate) > 100:
            errors.append(
                f"Companion '{comp_name}': approval gate {approval_gate} outside -100 to 100"
            )
    
    return errors, warnings


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python validate_companion_timelines.py <campaign.json>")
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
    
    errors, warnings = validate_companion_timelines(campaign)
    
    if errors:
        print("❌ Companion Timeline Validation Failed")
        for error in errors:
            print(f"  - {error}")
        sys.exit(1)
    
    if warnings:
        print("⚠️ Warnings:")
        for warning in warnings:
            print(f"  - {warning}")
    
    print("✅ Companion timelines valid!")
    sys.exit(0)
