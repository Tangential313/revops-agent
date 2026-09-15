def determine_action(diagnostics):
    if "stage_status_mismatch" in diagnostics:
        return {
            "action": "request_data_correction",
            "requires_approval": True,
            "automation_allowed": False,
        }

    if "stale_opportunity" in diagnostics:
        return {
            "action": "request_owner_review",
            "requires_approval": True,
            "automation_allowed": True,
        }

    return {
        "action": "no_action",
        "requires_approval": False,
        "automation_allowed": False,
    }
