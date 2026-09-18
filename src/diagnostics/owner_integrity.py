def find_accounts_with_missing_owners(accounts, owners):
    owner_ids = {
        owner["owner_id"]
        for owner in owners
    }

    invalid_accounts = []

    for account in accounts:
        if account["account_owner_id"] not in owner_ids:
            invalid_accounts.append(account["account_id"])

    return invalid_accounts


def find_opportunities_with_missing_owners(opportunities, owners):
    owner_ids = {
        owner["owner_id"]
        for owner in owners
    }

    invalid_opportunities = []

    for opportunity in opportunities:
        if opportunity["owner_id"] not in owner_ids:
            invalid_opportunities.append(opportunity["opportunity_id"])

    return invalid_opportunities
