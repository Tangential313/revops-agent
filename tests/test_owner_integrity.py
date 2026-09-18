import json

from src.diagnostics.owner_integrity import (
    find_accounts_with_missing_owners,
    find_opportunities_with_missing_owners,
)


def load_fixtures():
    with open("data/fixtures/accounts.json") as file:
        accounts = json.load(file)

    with open("data/fixtures/opportunities.json") as file:
        opportunities = json.load(file)

    with open("data/fixtures/owners.json") as file:
        owners = json.load(file)

    return accounts, opportunities, owners


def test_no_missing_owners_in_clean_fixtures():
    accounts, opportunities, owners = load_fixtures()

    assert find_accounts_with_missing_owners(accounts, owners) == []
    assert find_opportunities_with_missing_owners(opportunities, owners) == []


def test_detects_missing_account_owner():
    accounts, opportunities, owners = load_fixtures()

    accounts[0]["account_owner_id"] = "owner_999"

    result = find_accounts_with_missing_owners(accounts, owners)

    assert result == ["acct_001"]


def test_detects_missing_opportunity_owner():
    accounts, opportunities, owners = load_fixtures()

    opportunities[0]["owner_id"] = "owner_999"

    result = find_opportunities_with_missing_owners(opportunities, owners)

    assert result == ["opp_001"]
