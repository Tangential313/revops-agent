from typing import Literal
import json

from openai import OpenAI
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


SYSTEM_INSTRUCTIONS = """
You are a Revenue Operations reasoning component.

Reason only from the supplied CRM account state.

The supplied state may contain:
- account facts
- contact coverage
- opportunity facts and deterministic diagnostics
- recorded activity evidence
- evidence completeness information

You may:
- summarize the operational issue
- explain your reasoning
- recommend one permitted intervention
- cite supplied evidence
- express confidence in your reasoning

You must not:
- invent CRM facts
- invent reasons for missing or unavailable context
- treat missing evidence as evidence that an event did not occur
- infer customer intent, sentiment, or deal outcome without supplied evidence
- change opportunity stage or status
- decide that an opportunity is won or lost
- grant yourself automation permission
- infer facts that are not present in the supplied state

When context_status is "unavailable", explicitly acknowledge that the
available evidence is insufficient to determine why the observed CRM
condition exists.
"""


class OpenAIModelClient:
    def __init__(self, client=None, model="gpt-5-nano"):
        self.client = client or OpenAI()
        self.model = model

    def generate(self, agent_state):
        response = self.client.responses.parse(
            model=self.model,
            instructions=SYSTEM_INSTRUCTIONS,
            input=json.dumps(agent_state),
            text_format=AgentResponse,
            reasoning={"effort": "minimal"},
            max_output_tokens=1000,
        )

        if response.output_parsed is None:
            raise RuntimeError(
                "Model returned no parsed output. "
                f"status={response.status!r}, "
                f"incomplete_details={response.incomplete_details!r}, "
                f"output={response.output!r}"
            )

        return response.output_parsed.model_dump()
