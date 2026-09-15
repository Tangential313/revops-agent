from src.diagnostics.action_policy import determine_action


def test_no_diagnostics_returns_no_action():
    result = determine_action([])

    assert result == {
        "action": "no_action",
        "requires_approval": False,
        "automation_allowed": False,
    }


def test_stale_opportunity_requests_owner_review():
    result = determine_action(["stale_opportunity"])

    assert result == {
        "action": "request_owner_review",
        "requires_approval": True,
        "automation_allowed": True,
    }


def test_stage_status_mismatch_requests_data_correction():
    result = determine_action(["stage_status_mismatch"])

    assert result == {
        "action": "request_data_correction",
        "requires_approval": True,
        "automation_allowed": False,
    }

