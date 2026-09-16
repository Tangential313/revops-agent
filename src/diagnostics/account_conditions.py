def find_accounts_without_opportunities(accounts, opportunities):
    account_ids_with_opportunities = {
        opportunity["account_id"]
        for opportunity in opportunities
    }

    accounts_without_opportunities = []

    for account in accounts:
        if account["account_id"] not in account_ids_with_opportunities:
            accounts_without_opportunities.append(account["account_id"])

    return accounts_without_opportunities

