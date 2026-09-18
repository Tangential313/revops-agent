import json
from datetime import date

from src.account_state import build_account_state
from src.agent_state import build_agent_state
from src.diagnostics.evidence_completeness import assess_account_evidence
from src.diagnostics.opportunity_diagnostics import diagnose_opportunity
from src.openai_model import OpenAIModelClient


TODAY = date(2026, 9, 14)


def load_json(path):
    with open(path) as file:
        return json.load(file)


def main():
    accounts = load_json("data/fixtures/accounts.json")
    contacts = load_json("data/fixtures/contacts.json")
    opportunities = load_json("data/fixtures/opportunities.json")
    owners = load_json("data/fixtures/owners.json")
    activities = load_json("data/fixtures/activities.json")

    account = next(
        account
        for account in accounts
        if account["account_id"] == "acct_002"
    )

    owner = next(
        owner
        for owner in owners
        if owner["owner_id"] == account["account_owner_id"]
    )

    account_opportunities = [
        opportunity
        for opportunity in opportunities
        if opportunity["account_id"] == account["account_id"]
    ]

    opportunity_states = []

    for opportunity in account_opportunities:
        diagnosis = diagnose_opportunity(opportunity, TODAY)
        opportunity_states.append(
            build_agent_state(opportunity, diagnosis)
        )

    evidence = assess_account_evidence(
        account["account_id"],
        activities,
    )

    account_state = build_account_state(
        account,
        contacts,
        opportunity_states,
        owner,
        activities,
        evidence,
    )

    print("Account state:")
    print(json.dumps(account_state, indent=2))

    print("\nCalling model exactly once...")

    model_client = OpenAIModelClient()
    response = model_client.generate(account_state)

    print("\nModel response:")
    print(json.dumps(response, indent=2))


if __name__ == "__main__":
    main()
