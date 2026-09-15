def build_agent_state(opportunity, diagnosis):
    return {
        "opportunity": {
            "opportunity_id": opportunity["opportunity_id"],
            "name": opportunity["name"],
            "stage": opportunity["stage"],
            "status": opportunity["status"],
            "amount": opportunity["amount"],
            "currency": opportunity["currency"],
        },
        "derived_facts": {
            "days_to_close": diagnosis["days_to_close"],
            "days_since_activity": diagnosis["days_since_activity"],
            "days_in_stage": diagnosis["days_in_stage"],
            "close_date_passed": diagnosis["close_date_passed"],
        },
        "diagnostics": diagnosis["diagnostics"],
        "policy": diagnosis["recommended_action"],
    }

