import json

from src.diagnostics.activity_integrity import (
    find_activities_with_invalid_references,
    find_activities_with_account_mismatches,
)

def load_fixtures():
    with open("data/fixtures/activities.json") as file:
        activities = json.load(file)

    with open("data/fixtures/accounts.json") as file:
        accounts = json.load(file)

    with open("data/fixtures/opportunities.json") as file:
        opportunities = json.load(file)

    with open("data/fixtures/contacts.json") as file:
        contacts = json.load(file)

    with open("data/fixtures/owners.json") as file:
        owners = json.load(file)

    return activities, accounts, opportunities, contacts, owners


def test_clean_activity_references_are_valid():
    activities, accounts, opportunities, contacts, owners = load_fixtures()

    result = find_activities_with_invalid_references(
        activities,
        accounts,
        opportunities,
        contacts,
        owners,
    )

    assert result == []


def test_detects_invalid_required_references():
    activities, accounts, opportunities, contacts, owners = load_fixtures()

    activities[0]["account_id"] = "acct_999"
    activities[1]["owner_id"] = "owner_999"

    result = find_activities_with_invalid_references(
        activities,
        accounts,
        opportunities,
        contacts,
        owners,
    )

    assert result == [
        {
            "activity_id": "activity_001",
            "field": "account_id",
        },
        {
            "activity_id": "activity_002",
            "field": "owner_id",
        },
    ]


def test_null_optional_references_are_valid():
    activities, accounts, opportunities, contacts, owners = load_fixtures()

    result = find_activities_with_invalid_references(
        activities,
        accounts,
        opportunities,
        contacts,
        owners,
    )

    flagged_activity_ids = {
        item["activity_id"]
        for item in result
    }

    assert "activity_005" not in flagged_activity_ids
    assert "activity_006" not in flagged_activity_ids


def test_detects_invalid_optional_references():
    activities, accounts, opportunities, contacts, owners = load_fixtures()

    activities[0]["opportunity_id"] = "opp_999"
    activities[1]["contact_id"] = "contact_999"

    result = find_activities_with_invalid_references(
        activities,
        accounts,
        opportunities,
        contacts,
        owners,
    )

    assert result == [
        {
            "activity_id": "activity_001",
            "field": "opportunity_id",
        },
        {
            "activity_id": "activity_002",
            "field": "contact_id",
        },
    ]
def test_clean_activity_account_relationships_are_consistent():
    activities, accounts, opportunities, contacts, owners = load_fixtures()

    result = find_activities_with_account_mismatches(
        activities,
        opportunities,
        contacts,
    )

    assert result == []


def test_detects_activity_account_mismatches():
    activities, accounts, opportunities, contacts, owners = load_fixtures()

    activities[0]["contact_id"] = "contact_003"
    activities[1]["opportunity_id"] = "opp_002"

    result = find_activities_with_account_mismatches(
        activities,
        opportunities,
        contacts,
    )

    assert result == [
        {
            "activity_id": "activity_001",
            "field": "contact_id",
            "reason": "account_mismatch",
        },
        {
            "activity_id": "activity_002",
            "field": "opportunity_id",
            "reason": "account_mismatch",
        },
    ]
