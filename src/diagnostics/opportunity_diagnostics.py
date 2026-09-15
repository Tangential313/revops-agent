from datetime import date
from src.diagnostics.action_policy import determine_action

def diagnose_opportunity(opportunity, today):
    close_date = date.fromisoformat(opportunity["close_date"])

    last_activity_at = date.fromisoformat(
        opportunity["last_activity_at"]
    )

    stage_entered_at = date.fromisoformat(
        opportunity["stage_entered_at"]
    )

    days_to_close = (close_date - today).days
    days_since_activity = (today - last_activity_at).days
    days_in_stage = (today - stage_entered_at).days

    close_date_passed = (
        opportunity["status"] == "open"
        and close_date < today
    ) 

    inactive_opportunity = (
        opportunity["status"] == "open"
        and days_since_activity > 30
    )

    prolonged_stage = (
        opportunity["status"] == "open"
        and days_in_stage > 60
    )

    stale_opportunity = (
        inactive_opportunity
        and prolonged_stage
    )

    stage_status_mismatch = (
        opportunity["stage"] == "Closed Won"
        and opportunity["status"] != "closed_won"
    )
    diagnostics = []

    if close_date_passed:
        diagnostics.append("close_date_passed")

    if inactive_opportunity:
        diagnostics.append("inactive_opportunity")

    if prolonged_stage:
        diagnostics.append("prolonged_stage")

    if stale_opportunity:
        diagnostics.append("stale_opportunity")

    if stage_status_mismatch:
        diagnostics.append("stage_status_mismatch")

    recommended_action = determine_action(diagnostics)

    return {
        "opportunity_id": opportunity["opportunity_id"],
        "days_to_close": days_to_close,
        "days_since_activity": days_since_activity,
        "days_in_stage": days_in_stage,
        "close_date_passed": close_date_passed,
        "stale_opportunity": stale_opportunity,
        "stage_status_mismatch": stage_status_mismatch,
        "prolonged_stage": prolonged_stage,
        "inactive_opportunity": inactive_opportunity,
        "diagnostics": diagnostics,
        "recommended_action": recommended_action,
    }
