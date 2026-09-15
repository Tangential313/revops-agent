ALLOWED_INTERVENTIONS = {
    "no_intervention",
    "review_opportunity",
    "investigate_data_quality",
}


def validate_agent_response(response):
    required_fields = {
        "summary",
        "reasoning",
        "recommended_intervention",
        "evidence",
        "confidence",
    }

    if set(response.keys()) != required_fields:
        return False

    if response["recommended_intervention"] not in ALLOWED_INTERVENTIONS:
        return False

    if not isinstance(response["evidence"], list):
        return False

    if not isinstance(response["confidence"], float):
        return False

    if not 0.0 <= response["confidence"] <= 1.0:
        return False

    return True

    if response["recommended_intervention"] not in ALLOWED_INTERVENTIONS:
        return False

    if not isinstance(response["evidence"], list):
        return False

    if not isinstance(response["confidence"], float):
        return False

    if not 0.0 <= response["confidence"] <= 1.0:
        return False

    return True
