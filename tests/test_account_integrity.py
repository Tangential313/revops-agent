import json

from src.diagnostics.account_integrity import (
    find_accounts_without_opportunities,
    find_orphaned_opportunities,
)

def load_fixtures():
    with open("data/fixtures/accounts.json") as file:
        accounts = json.load(file)

    with open("data/fixtures/opportunities.json") as file:
        opportunities = json.load(file)

    return accounts, opportunities


def test_no_orphaned_opportunities_in_clean_fixtures():
    accounts, opportunities = load_fixtures()

    result = find_orphaned_opportunities(accounts, opportunities)

    assert result == []


def test_detects_orphaned_opportunity():
    accounts, opportunities = load_fixtures()

    orphaned_opportunity = {
        "opportunity_id": "opp_004",
        "account_id": "acct_999",
    }

    opportunities.append(orphaned_opportunity)

    result = find_orphaned_opportunities(accounts, opportunities)

    assert result == ["opp_004"]
def test_all_fixture_accounts_have_opportunities():
    accounts, opportunities = load_fixtures()

    result = find_accounts_without_opportunities(accounts, opportunities)

    assert result == []


def test_detects_account_without_opportunity():
    accounts, opportunities = load_fixtures()

    account_without_opportunity = {
        "account_id": "acct_004",
        "name": "Helios Industries",
    }

    accounts.append(account_without_opportunity)

    result = find_accounts_without_opportunities(accounts, opportunities)

    assert result == ["acct_004"]
