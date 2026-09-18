import json

from src.diagnostics.evidence_completeness import assess_account_evidence


def load_activities():
    with open("data/fixtures/activities.json") as file:
        return json.load(file)


def test_northstar_has_sufficient_context():
    activities = load_activities()

    result = assess_account_evidence("acct_001", activities)

    assert result == {
        "account_id": "acct_001",
        "context_status": "sufficient",
        "available": 2,
        "missing": 0,
        "permission_denied": 0,
    }


def test_mercury_has_unavailable_context():
    activities = load_activities()

    result = assess_account_evidence("acct_002", activities)

    assert result == {
        "account_id": "acct_002",
        "context_status": "unavailable",
        "available": 0,
        "missing": 1,
        "permission_denied": 0,
    }


def test_atlas_has_partial_context():
    activities = load_activities()

    result = assess_account_evidence("acct_003", activities)

    assert result == {
        "account_id": "acct_003",
        "context_status": "partial",
        "available": 1,
        "missing": 0,
        "permission_denied": 1,
    }


def test_account_with_only_not_applicable_notes_has_not_applicable_context():
    activities = [
        {
            "account_id": "acct_004",
            "notes_status": "not_applicable",
        }
    ]

    result = assess_account_evidence("acct_004", activities)

    assert result == {
        "account_id": "acct_004",
        "context_status": "not_applicable",
        "available": 0,
        "missing": 0,
        "permission_denied": 0,
    }
