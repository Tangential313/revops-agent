def find_activities_with_invalid_references(
    activities,
    accounts,
    opportunities,
    contacts,
    owners,
):
    account_ids = {
        account["account_id"]
        for account in accounts
    }

    opportunity_ids = {
        opportunity["opportunity_id"]
        for opportunity in opportunities
    }

    contact_ids = {
        contact["contact_id"]
        for contact in contacts
    }

    owner_ids = {
        owner["owner_id"]
        for owner in owners
    }

    invalid_references = []

    for activity in activities:
        activity_id = activity["activity_id"]

        if activity["account_id"] not in account_ids:
            invalid_references.append({
                "activity_id": activity_id,
                "field": "account_id",
            })

        if activity["owner_id"] not in owner_ids:
            invalid_references.append({
                "activity_id": activity_id,
                "field": "owner_id",
            })

        if (
            activity["opportunity_id"] is not None
            and activity["opportunity_id"] not in opportunity_ids
        ):
            invalid_references.append({
                "activity_id": activity_id,
                "field": "opportunity_id",
            })

        if (
            activity["contact_id"] is not None
            and activity["contact_id"] not in contact_ids
        ):
            invalid_references.append({
                "activity_id": activity_id,
                "field": "contact_id",
            })

    return invalid_references
def find_activities_with_account_mismatches(
    activities,
    opportunities,
    contacts,
):
    opportunity_accounts = {
        opportunity["opportunity_id"]: opportunity["account_id"]
        for opportunity in opportunities
    }

    contact_accounts = {
        contact["contact_id"]: contact["account_id"]
        for contact in contacts
    }

    mismatches = []

    for activity in activities:
        activity_id = activity["activity_id"]
        activity_account_id = activity["account_id"]

        opportunity_id = activity["opportunity_id"]

        if (
            opportunity_id is not None
            and opportunity_id in opportunity_accounts
            and opportunity_accounts[opportunity_id] != activity_account_id
        ):
            mismatches.append({
                "activity_id": activity_id,
                "field": "opportunity_id",
                "reason": "account_mismatch",
            })

        contact_id = activity["contact_id"]

        if (
            contact_id is not None
            and contact_id in contact_accounts
            and contact_accounts[contact_id] != activity_account_id
        ):
            mismatches.append({
                "activity_id": activity_id,
                "field": "contact_id",
                "reason": "account_mismatch",
            })

    return mismatches
