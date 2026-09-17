def find_orphaned_contacts(accounts, contacts):
    account_ids = {
        account["account_id"]
        for account in accounts
    }

    orphaned = []

    for contact in contacts:
        if contact["account_id"] not in account_ids:
            orphaned.append(contact["contact_id"])

    return orphaned

