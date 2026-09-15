import json
from datetime import date

from src.agent_state import build_agent_state
from src.diagnostics.opportunity_diagnostics import diagnose_opportunity


TODAY = date(2026, 9, 14)


with open("data/fixtures/opportunities.json") as file:
    opportunities = json.load(file)


def test_build_agent_state_for_stale_opportunity():
    opportunity = opportunities[1]
    diagnosis = diagnose_opportunity(opportunity, TODAY)

    state = build_agent_state(opportunity, diagnosis)

    assert state["opportunity"] == {
        "opportunity_id": "opp_002",
        "name": "Mercury Systems - New Business",
        "stage": "Discovery",
        "status": "open",
        "amount": 42000,
        "currency": "GBP",
    }

    assert state["derived_facts"] == {
        "days_to_close": -45,
        "days_since_activity": 105,
        "days_in_stage": 127,
        "close_date_passed": True,
    }

    assert state["diagnostics"] == [
        "close_date_passed",
        "inactive_opportunity",
        "prolonged_stage",
        "stale_opportunity",
    ]

    assert state["policy"] == {
        "action": "request_owner_review",
        "requires_approval": True,
        "automation_allowed": True,
    }

def test_agent_state_exposes_only_allowed_opportunity_fields():
    opportunity = opportunities[1]
    diagnosis = diagnose_opportunity(opportunity, TODAY)

    state = build_agent_state(opportunity, diagnosis)

    assert set(state["opportunity"].keys()) == {
        "opportunity_id",
        "name",
        "stage",
        "status",
        "amount",
        "currency",
    }
