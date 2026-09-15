import json
from datetime import date

from src.diagnostics.opportunity_diagnostics import diagnose_opportunity


TODAY = date(2026, 9, 14)


with open("data/fixtures/opportunities.json") as file:
    opportunities = json.load(file)


def test_healthy_opportunity():
    result = diagnose_opportunity(opportunities[0], TODAY)

    assert result["stale_opportunity"] is False
    assert result["stage_status_mismatch"] is False
    assert result["inactive_opportunity"] is False
    assert result["prolonged_stage"] is False
    assert result["diagnostics"] == []
    assert result["recommended_action"] == {
        "action": "no_action",
        "requires_approval": False,
        "automation_allowed": False,
    }


def test_stale_opportunity():
    result = diagnose_opportunity(opportunities[1], TODAY)

    assert result["stale_opportunity"] is True
    assert result["close_date_passed"] is True
    assert result["inactive_opportunity"] is True
    assert result["prolonged_stage"] is True
    assert result["diagnostics"] == [
        "close_date_passed",
        "inactive_opportunity",
        "prolonged_stage",
        "stale_opportunity",
    ]
    assert result["recommended_action"] == {
        "action": "request_owner_review",
        "requires_approval": True,
	"automation_allowed": True,
    }

def test_stage_status_mismatch():
    result = diagnose_opportunity(opportunities[2], TODAY)

    assert result["stale_opportunity"] is False
    assert result["stage_status_mismatch"] is True 	
    assert result["diagnostics"] == [
        "close_date_passed",
        "stage_status_mismatch",
    ]
    assert result["recommended_action"] == {
        "action": "request_data_correction",
        "requires_approval": True,
        "automation_allowed": False,
    }
