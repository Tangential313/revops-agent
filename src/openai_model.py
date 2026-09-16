from typing import Literal

from pydantic import BaseModel


class AgentResponse(BaseModel):
    summary: str
    reasoning: str
    recommended_intervention: Literal[
        "no_intervention",
        "review_opportunity",
        "investigate_data_quality",
    ]
    evidence: list[str]
    confidence: float

import json

from openai import OpenAI


SYSTEM_INSTRUCTIONS = """
You are a Revenue Operations reasoning component.

Reason only from the supplied opportunity state.

You may:
- summarize the operational issue
- explain your reasoning
- recommend one permitted intervention
- cite supplied evidence
- express confidence in your reasoning

You must not:
- invent CRM facts
- change opportunity stage or status
- decide that an opportunity is won or lost
- grant yourself automation permission
- infer facts that are not present in the supplied state
"""


class OpenAIModelClient:
    def __init__(self, client=None, model=None):
        self.client = client or OpenAI()
        self.model = model

    def generate(self, agent_state):
        response = self.client.responses.parse(
            model=self.model,
            instructions=SYSTEM_INSTRUCTIONS,
            input=json.dumps(agent_state),
            text_format=AgentResponse,
        )

        return response.output_parsed.model_dump()
