import json

from src.diagnostics.owner_conditions import find_records_with_inactive_owners


def load_fixtures():
    with open("data/fixtures/accounts.json") as file:
        accounts = json.load(file)

    with open("data/fixtures/opportunities.json") as file:
        opportunities = json.load(file)

    with open("data/fixtures/owners.json") as file:
        owners = json.load(file)

    return accounts, opportunities, owners


def test_no_records_have_inactive_owners_in_clean_fixtures():
    accounts, opportunities, owners = load_fixtures()

    result = find_records_with_inactive_owners(
        accounts,
        opportunities,
        owners,
    )

    assert result == {
        "accounts": [],
        "opportunities": [],
    }


def test_detects_records_assigned_to_inactive_owner():
    accounts, opportunities, owners = load_fixtures()

    owners[1]["status"] = "inactive"

    result = find_records_with_inactive_owners(
        accounts,
        opportunities,
        owners,
    )

    assert result == {
        "accounts": ["acct_002"],
        "opportunities": ["opp_002"],
    }

