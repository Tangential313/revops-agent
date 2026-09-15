from src.agent_response import validate_agent_response


def test_valid_agent_response_is_accepted():
    response = {
        "summary": "Opportunity appears commercially stale.",
        "reasoning": (
            "The opportunity has had no recent activity, "
            "has remained in its current stage for an extended period, "
            "and its expected close date has passed."
        ),
        "recommended_intervention": "review_opportunity",
        "evidence": [
            "days_since_activity=105",
            "days_in_stage=127",
            "close_date_passed=True",
        ],
        "confidence": 0.92,
    }

    assert validate_agent_response(response) is True


def test_unapproved_intervention_is_rejected():
    response = {
        "summary": "This deal is dead.",
        "reasoning": "It has been inactive for too long.",
        "recommended_intervention": "close_lost",
        "evidence": [
            "days_since_activity=105",
        ],
        "confidence": 0.99,
    }

    assert validate_agent_response(response) is False


def test_extra_field_is_rejected():
    response = {
        "summary": "Opportunity requires review.",
        "reasoning": "The expected close date has passed.",
        "recommended_intervention": "review_opportunity",
        "evidence": [
            "close_date_passed=True",
        ],
        "confidence": 0.85,
        "new_stage": "Closed Lost",
    }

    assert validate_agent_response(response) is False


def test_invalid_confidence_is_rejected():
    response = {
        "summary": "Opportunity requires review.",
        "reasoning": "Activity is stale.",
        "recommended_intervention": "review_opportunity",
        "evidence": [
            "days_since_activity=105",
        ],
        "confidence": 1.4,
    }

    assert validate_agent_response(response) is False
