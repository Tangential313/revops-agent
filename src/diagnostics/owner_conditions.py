def find_records_with_inactive_owners(accounts, opportunities, owners):
    inactive_owner_ids = {
        owner["owner_id"]
        for owner in owners
        if owner["status"] == "inactive"
    }

    affected_accounts = []
    affected_opportunities = []

    for account in accounts:
        if account["account_owner_id"] in inactive_owner_ids:
            affected_accounts.append(account["account_id"])

    for opportunity in opportunities:
        if opportunity["owner_id"] in inactive_owner_ids:
            affected_opportunities.append(opportunity["opportunity_id"])

    return {
        "accounts": affected_accounts,
        "opportunities": affected_opportunities,
    }

