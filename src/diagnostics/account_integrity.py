def find_orphaned_opportunities(accounts, opportunities):
    account_ids = {
        account["account_id"]
        for account in accounts
    }

    orphaned = []

    for opportunity in opportunities:
        if opportunity["account_id"] not in account_ids:
            orphaned.append(opportunity["opportunity_id"])

    return orphaned
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
