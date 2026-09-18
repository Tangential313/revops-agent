def build_account_state(
    account,
    contacts,
    opportunity_states,
    owner,
    activities,
    evidence,
):
    account_contacts = [
        contact
        for contact in contacts
        if contact["account_id"] == account["account_id"]
    ]

    account_activities = [
        activity
        for activity in activities
        if activity["account_id"] == account["account_id"]
    ]

    return {
        "account": {
            "account_id": account["account_id"],
            "name": account["name"],
            "lifecycle_stage": account["lifecycle_stage"],
            "status": account["status"],
        },
        "owner": {
            "owner_id": owner["owner_id"],
            "status": owner["status"],
        },
        "contact_coverage": {
            "contact_count": len(account_contacts),
            "single_threaded": len(account_contacts) == 1,
        },
"opportunities": [
    {
        "opportunity": opportunity_state["opportunity"],
        "derived_facts": opportunity_state["derived_facts"],
        "diagnostics": opportunity_state["diagnostics"],
    }
    for opportunity_state in opportunity_states
],        "activity_evidence": {
            "activity_count": len(account_activities),
            "activities": [
                {
                    "activity_id": activity["activity_id"],
                    "activity_type": activity["activity_type"],
                    "occurred_at": activity["occurred_at"],
                    "notes_status": activity["notes_status"],
                }
                for activity in account_activities
            ],
        },
        "evidence": evidence,
    }
