from src.agent_response import validate_agent_response


def reason_about_opportunity(agent_state, model_client):
    response = None

    for attempt in range(2):
        try:
            response = model_client.generate(agent_state)
            break
        except Exception:
            if attempt == 1:
                return {
                    "status": "model_error",
                    "response": None,
                }

    if not validate_agent_response(response):
        return {
            "status": "validation_failed",
            "response": None,
        }

    return {
        "status": "success",
        "response": response,
    }
