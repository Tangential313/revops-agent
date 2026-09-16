import json
import pytest
from pydantic import ValidationError

from src.openai_model import (
    AgentResponse,
    OpenAIModelClient,
    SYSTEM_INSTRUCTIONS,
)

def test_agent_response_accepts_valid_output():
    response = AgentResponse(
        summary="Opportunity needs review.",
        reasoning="The opportunity has been inactive for 105 days.",
        recommended_intervention="review_opportunity",
        evidence=["inactive_opportunity", "stale_opportunity"],
        confidence=0.92,
    )

    assert response.recommended_intervention == "review_opportunity"


def test_agent_response_rejects_unapproved_intervention():
    with pytest.raises(ValidationError):
        AgentResponse(
            summary="Close the opportunity.",
            reasoning="The deal appears stale.",
            recommended_intervention="close_lost",
            evidence=["stale_opportunity"],
            confidence=0.95,
        )


class FakeParsedResponse:
    def __init__(self):
        self.output_parsed = AgentResponse(
            summary="Opportunity needs review.",
            reasoning="The opportunity is stale.",
            recommended_intervention="review_opportunity",
            evidence=["stale_opportunity"],
            confidence=0.91,
        )


class FakeResponses:
    def __init__(self):
        self.parse_kwargs = None

    def parse(self, **kwargs):
        self.parse_kwargs = kwargs
        return FakeParsedResponse()

def test_openai_model_client_sends_controlled_request():
    fake_client = FakeOpenAIClient()

    client = OpenAIModelClient(
        client=fake_client,
        model="test-model",
    )

    agent_state = {
        "diagnostics": ["stale_opportunity"],
        "policy": {
            "action": "request_owner_review",
            "requires_approval": True,
            "automation_allowed": True,
        },
    }

    client.generate(agent_state)

    request = fake_client.responses.parse_kwargs

    assert request["model"] == "test-model"
    assert request["text_format"] is AgentResponse
    assert request["instructions"] == SYSTEM_INSTRUCTIONS
    assert json.loads(request["input"]) == agent_state

class FakeOpenAIClient:
    def __init__(self):
        self.responses = FakeResponses()


def test_openai_model_client_returns_valid_dict():
    client = OpenAIModelClient(
        client=FakeOpenAIClient(),
        model="test-model",
    )

    result = client.generate({"diagnostics": ["stale_opportunity"]})

    assert result == {
        "summary": "Opportunity needs review.",
        "reasoning": "The opportunity is stale.",
        "recommended_intervention": "review_opportunity",
        "evidence": ["stale_opportunity"],
        "confidence": 0.91,
    }
def test_openai_model_client_uses_cheap_default_model():
    client = OpenAIModelClient(client=FakeOpenAIClient())

    assert client.model == "gpt-5-nano"
