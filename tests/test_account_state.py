from src.account_state import build_account_state


def test_builds_bounded_account_state():
    account = {
        "account_id": "acct_002",
        "name": "Mercury Systems",
        "lifecycle_stage": "opportunity",
        "status": "active",
    }

    contacts = [
        {
            "contact_id": "contact_003",
            "account_id": "acct_002",
        }
    ]

    opportunity_states = [
        {
            "opportunity": {
                "opportunity_id": "opp_002",
                "name": "Mercury Systems - New Business",
                "stage": "Discovery",
                "status": "open",
                "amount": 42000,
                "currency": "GBP",
            },
            "derived_facts": {
                "days_to_close": -45,
                "days_since_activity": 105,
                "days_in_stage": 127,
                "close_date_passed": True,
            },
            "diagnostics": [
                "close_date_passed",
                "inactive_opportunity",
                "prolonged_stage",
                "stale_opportunity",
            ],
            "policy": {
                "action": "request_owner_review",
                "requires_approval": True,
                "automation_allowed": True,
            },
        }
    ]

    owner = {
        "owner_id": "owner_002",
        "status": "active",
    }

    activities = [
        {
            "activity_id": "activity_003",
            "account_id": "acct_002",
            "activity_type": "call",
            "occurred_at": "2026-06-01T11:00:00",
            "notes_status": "missing",
        }
    ]

    evidence = {
        "account_id": "acct_002",
        "context_status": "unavailable",
        "available": 0,
        "missing": 1,
        "permission_denied": 0,
    }

    result = build_account_state(
        account,
        contacts,
        opportunity_states,
        owner,
        activities,
        evidence,
    )

    assert result["account"]["account_id"] == "acct_002"
    assert result["contact_coverage"] == {
        "contact_count": 1,
        "single_threaded": True,
    }
    assert result["opportunities"][0]["opportunity"]["opportunity_id"] == "opp_002"
    assert result["opportunities"][0]["diagnostics"] == [
        "close_date_passed",
        "inactive_opportunity",
        "prolonged_stage",
        "stale_opportunity",
    ]
    assert "policy" not in result["opportunities"][0]
    assert result["activity_evidence"]["activity_count"] == 1
    assert result["evidence"]["context_status"] == "unavailable"
