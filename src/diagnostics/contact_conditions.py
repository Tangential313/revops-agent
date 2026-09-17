def find_accounts_without_contacts(accounts, contacts):
    account_ids_with_contacts = {
        contact["account_id"]
        for contact in contacts
    }

    accounts_without_contacts = []

    for account in accounts:
        if account["account_id"] not in account_ids_with_contacts:
            accounts_without_contacts.append(account["account_id"])

    return accounts_without_contacts
def find_single_threaded_accounts(accounts, contacts):
    contact_counts = {}

    for contact in contacts:
        account_id = contact["account_id"]
        contact_counts[account_id] = contact_counts.get(account_id, 0) + 1

    single_threaded = []

    for account in accounts:
        if contact_counts.get(account["account_id"], 0) == 1:
            single_threaded.append(account["account_id"])

    return single_threaded
