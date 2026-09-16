import json
from datetime import date

from src.agent import reason_about_opportunity
from src.agent_state import build_agent_state
from src.diagnostics.opportunity_diagnostics import diagnose_opportunity
from src.openai_model import OpenAIModelClient


TODAY = date(2026, 9, 14)


with open("data/fixtures/opportunities.json") as file:
    opportunities = json.load(file)


opportunity = next(
    opportunity
    for opportunity in opportunities
    if opportunity["opportunity_id"] == "opp_002"
)


diagnosis = diagnose_opportunity(opportunity, TODAY)
agent_state = build_agent_state(opportunity, diagnosis)


print("Agent state:")
print(json.dumps(agent_state, indent=2))

print("\nNo API call made yet.")
