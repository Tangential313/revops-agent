# Revenue Operations Agent

An applied GTM Engineering portfolio project exploring how deterministic RevOps diagnostics and constrained AI reasoning can work together inside a governed CRM workflow.

> **Status:** Project skeleton / planned architecture. This repository documents the intended system before implementation begins.

## Problem

Revenue teams often accumulate operational problems inside the CRM that are individually small but collectively expensive to investigate and manage.

Examples include:

- stale opportunities with no recent activity
- missing or inconsistent ownership
- contradictory lifecycle stages
- incomplete or low-quality CRM records
- routing problems
- opportunities that remain in a stage far longer than expected
- high activity without corresponding pipeline progression

Many of these conditions can be detected deterministically from CRM data. The harder question is what the evidence means in context and what a revenue operator should do next.

The project asks:

**How can an AI-assisted RevOps system diagnose CRM problems, reason about appropriate interventions, and recommend or execute controlled actions without allowing the model to invent CRM truth?**

## Proposed solution

Build a small synthetic CRM environment containing accounts, contacts, opportunities and activities. Seed it with realistic data-quality and pipeline-management problems, then create a workflow that separates factual diagnosis from AI interpretation.

```text
Synthetic CRM data
        ↓
Data-quality + pipeline checks
        ↓
Deterministic diagnostics
        ↓
Structured account / opportunity state
        ↓
Constrained AI reasoning
        ↓
Recommended intervention
        ↓
Approval / policy gate
        ↓
Controlled CRM action
        ↓
Audit log
```

The system should be able to answer questions such as:

- Which opportunities require attention?
- What factual conditions triggered the diagnosis?
- What intervention is appropriate given those conditions?
- Is the proposed action safe to execute automatically?
- What happened after the recommendation or action?

## Core design principle

**The model does not determine CRM truth.**

Deterministic Python/SQL logic establishes observable states such as:

```text
opportunity_stale = true
owner_missing = false
days_since_activity = 31
days_in_stage = 94
```

The AI layer receives structured evidence and can interpret it, explain why it matters, and recommend an intervention.

For example:

> This opportunity has remained in Discovery for 94 days and has had no recorded activity for 31 days. Recommend a rep follow-up and flag it for pipeline review.

The model should not independently alter commercial facts, declare revenue lost, invent missing CRM data, or perform unrestricted writes.

## Deterministic vs AI responsibilities

### Deterministic layer

Expected responsibilities:

- schema validation
- data-quality checks
- duplicate detection
- stale opportunity detection
- lifecycle consistency checks
- ownership and routing checks
- stage-age calculations
- activity recency calculations
- policy and permission checks
- action validation
- audit logging

These decisions should be repeatable, testable and explainable.

### AI reasoning layer

Expected responsibilities:

- interpret combinations of diagnosed conditions
- prioritize issues using supplied evidence
- generate concise explanations
- recommend an appropriate intervention
- return structured outputs
- select from explicitly permitted tools/actions

The AI layer should operate downstream of validated CRM state rather than reasoning directly over uncontrolled raw data.

## Controlled actions

Potential tools exposed to the agent may include narrowly scoped operations such as:

```python
create_task(...)
write_crm_note(...)
update_review_status(...)
request_owner_review(...)
```

Higher-risk actions should require explicit approval or remain outside the agent's permissions entirely.

## Guardrails

The project will explore practical controls for AI inside operational systems:

- structured model outputs
- explicit tool schemas
- deterministic validation before execution
- allowlisted actions
- approval gates for consequential changes
- retries and fallbacks
- audit trails
- evidence attached to recommendations
- tests for business invariants
- evaluation of recommendation quality

A useful governing rule is:

**Evidence first. Reasoning second. Action last.**

## Initial data model

The first version is expected to use synthetic CRM data rather than a live production system.

Likely entities:

```text
accounts
contacts
opportunities
activities
owners
```

The dataset should be large enough to produce realistic patterns while remaining understandable and testable. An initial target may be approximately 100 accounts, 200 opportunities and 500 contacts, with intentionally seeded operational problems.

## Tools and approach

Likely implementation stack:

- **Python** for diagnostics, orchestration and business logic
- **SQL** for CRM-style querying and data modelling
- **JSON / structured schemas** for state and model outputs
- **LLM API** for constrained reasoning and tool calling
- **pytest** for business-rule and workflow tests
- **Git / GitHub** for version control and project documentation

Additional tooling may be introduced only where it serves the system rather than expanding the project for its own sake.

## Initial build stages

### 1. Model the CRM

Define the account, contact, opportunity and activity schemas. Generate a synthetic dataset with known edge cases and deliberately seeded operational problems.

### 2. Build deterministic diagnostics

Implement the factual detection layer. The output should describe CRM state without prescribing actions or using an LLM.

### 3. Define the agent contract

Create a structured input representing validated CRM state and a constrained structured output for recommendations.

### 4. Add AI reasoning

Use the model to interpret diagnosed conditions and recommend interventions. Add structured outputs, retries and fallback behaviour.

### 5. Add controlled tools

Expose a small set of safe CRM-like actions. Separate recommendation from execution and introduce approval gates where appropriate.

### 6. Evaluate and observe

Measure whether the agent selects appropriate interventions, respects its permissions, handles edge cases and produces traceable decisions.

## What this project is intended to demonstrate

This project complements a deterministic signal-intelligence pipeline by demonstrating a different part of GTM Engineering:

- CRM and RevOps systems thinking
- SQL and data modelling
- Python application logic
- AI agent architecture
- structured outputs and tool calling
- deterministic/LLM boundary design
- guardrails and human approval
- testing and evaluation
- observability and auditability

The objective is not to build a chatbot sitting on top of CRM data. It is to build a small, governed operational system in which AI is used specifically where contextual reasoning adds value.

## Non-goals for the first version

The initial version does not need to:

- connect to a real production CRM
- autonomously make high-impact pipeline changes
- reproduce an entire CRM platform
- support every possible RevOps workflow
- use an LLM for logic that is more reliably expressed as deterministic rules

Scope should remain deliberately narrow enough that the architecture, decisions and trade-offs are easy to understand.

## Current status

**Planning / architecture.**

No implementation is claimed yet. The next starting point is to define the synthetic CRM schema and decide which operational problems will be deliberately seeded into the dataset.

---

**Author:** Aanu Oduyemi-Rose
