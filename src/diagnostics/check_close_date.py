import json
from datetime import date
from pathlib import Path


TODAY = date(2026, 9, 14)

DATA_PATH = Path("data/fixtures/opportunities.json")


with DATA_PATH.open() as file:
    opportunities = json.load(file)


for opportunity in opportunities:
    close_date = date.fromisoformat(opportunity["close_date"])

    last_activity_at = date.fromisoformat(
        opportunity["last_activity_at"]
    )

    stage_entered_at = date.fromisoformat(
        opportunity["stage_entered_at"]
    )

    days_to_close = (close_date - TODAY).days
    days_since_activity = (TODAY - last_activity_at).days
    days_in_stage = (TODAY - stage_entered_at).days

    close_date_passed = (
        opportunity["status"] == "open"
        and close_date < TODAY
    )

    stale_opportunity = (
        opportunity["status"] == "open"
        and days_since_activity > 30
        and days_in_stage > 60
    )
    stage_status_mismatch = (
        opportunity["stage"] == "Closed Won"
        and opportunity["status"] != "closed_won"
    )
 
    print(
        opportunity["opportunity_id"],
        "days_to_close=",
        days_to_close,
        "days_since_activity=",
        days_since_activity,
        "days_in_stage=",
        days_in_stage,
        "close_date_passed=",
        close_date_passed,
        "stale_opportunity=",
        stale_opportunity,
	"stage_status_mismatch=",
        stage_status_mismatch,
    )
