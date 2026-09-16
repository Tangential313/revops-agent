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
