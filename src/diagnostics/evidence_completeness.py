def assess_account_evidence(account_id, activities):
    account_activities = [
        activity
        for activity in activities
        if activity["account_id"] == account_id
    ]

    relevant_statuses = [
        activity["notes_status"]
        for activity in account_activities
        if activity["notes_status"] != "not_applicable"
    ]

    available = relevant_statuses.count("available")
    missing = relevant_statuses.count("missing")
    permission_denied = relevant_statuses.count("permission_denied")

    if not relevant_statuses:
        context_status = "not_applicable"
    elif available == len(relevant_statuses):
        context_status = "sufficient"
    elif available > 0:
        context_status = "partial"
    else:
        context_status = "unavailable"

    return {
        "account_id": account_id,
        "context_status": context_status,
        "available": available,
        "missing": missing,
        "permission_denied": permission_denied,
    }

