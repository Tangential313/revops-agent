import json

from src.diagnostics.contact_conditions import (
    find_accounts_without_contacts,
    find_single_threaded_accounts,
)

def load_fixtures():
    with open("data/fixtures/accounts.json") as file:
        accounts = json.load(file)

    with open("data/fixtures/contacts.json") as file:
        contacts = json.load(file)

    return accounts, contacts


def test_all_fixture_accounts_have_contacts():
    accounts, contacts = load_fixtures()

    result = find_accounts_without_contacts(accounts, contacts)

    assert result == []


def test_detects_account_without_contacts():
    accounts, contacts = load_fixtures()

    account_without_contacts = {
        "account_id": "acct_004",
        "name": "Helios Industries",
    }

    accounts.append(account_without_contacts)

    result = find_accounts_without_contacts(accounts, contacts)

    assert result == ["acct_004"]

def test_detects_single_threaded_accounts():
    accounts, contacts = load_fixtures()

    result = find_single_threaded_accounts(accounts, contacts)

    assert result == ["acct_002", "acct_003"]
def test_account_without_contacts_is_not_single_threaded():
    accounts, contacts = load_fixtures()

    account_without_contacts = {
        "account_id": "acct_004",
        "name": "Helios Industries",
    }

    accounts.append(account_without_contacts)

    result = find_single_threaded_accounts(accounts, contacts)

    assert "acct_004" not in result
