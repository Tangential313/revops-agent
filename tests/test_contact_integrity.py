import json

from src.diagnostics.contact_integrity import find_orphaned_contacts


def load_fixtures():
    with open("data/fixtures/accounts.json") as file:
        accounts = json.load(file)

    with open("data/fixtures/contacts.json") as file:
        contacts = json.load(file)

    return accounts, contacts


def test_no_orphaned_contacts_in_clean_fixtures():
    accounts, contacts = load_fixtures()

    result = find_orphaned_contacts(accounts, contacts)

    assert result == []


def test_detects_orphaned_contact():
    accounts, contacts = load_fixtures()

    orphaned_contact = {
        "contact_id": "contact_999",
        "account_id": "acct_999",
    }

    contacts.append(orphaned_contact)

    result = find_orphaned_contacts(accounts, contacts)

    assert result == ["contact_999"]

