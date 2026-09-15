from src.agent import reason_about_opportunity


class ValidFakeModel:
    def generate(self, agent_state):
        return {
            "summary": "Opportunity appears commercially stale.",
            "reasoning": (
                "The opportunity has remained in its current stage "
                "without recent activity."
            ),
            "recommended_intervention": "review_opportunity",
            "evidence": [
                "days_since_activity=105",
                "days_in_stage=127",
            ],
            "confidence": 0.92,
        }


class RogueFakeModel:
    def generate(self, agent_state):
        return {
            "summary": "I have taken matters into my own hands.",
            "reasoning": "Trust me.",
            "recommended_intervention": "close_lost",
            "evidence": [],
            "confidence": 0.99,
        }


def test_valid_model_response_succeeds():
    result = reason_about_opportunity(
        {"example": "state"},
        ValidFakeModel(),
    )

    assert result["status"] == "success"
    assert result["response"]["recommended_intervention"] == (
        "review_opportunity"
    )


def test_invalid_model_response_is_rejected():
    result = reason_about_opportunity(
        {"example": "state"},
        RogueFakeModel(),
    )

    assert result == {
        "status": "validation_failed",
        "response": None,
    }
class ExplodingFakeModel:
    def generate(self, agent_state):
        raise RuntimeError("Model provider unavailable")

def test_model_failure_is_handled():
    result = reason_about_opportunity(
        {"example": "state"},
        ExplodingFakeModel(),
    )

    assert result == {
        "status": "model_error",
        "response": None,
    }
class FlakyFakeModel:
    def __init__(self):
        self.calls = 0

    def generate(self, agent_state):
        self.calls += 1

        if self.calls == 1:
            raise RuntimeError("Temporary provider failure")

        return {
            "summary": "Opportunity requires review.",
            "reasoning": "The opportunity shows stale pipeline signals.",
            "recommended_intervention": "review_opportunity",
            "evidence": [
                "days_since_activity=105",
            ],
            "confidence": 0.90,
        }


def test_model_failure_retries_once():
    model = FlakyFakeModel()

    result = reason_about_opportunity(
        {"example": "state"},
        model,
    )

    assert result["status"] == "success"
    assert model.calls == 2
