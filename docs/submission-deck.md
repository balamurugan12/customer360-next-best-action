# Submission Deck Content

Status: outline only. The current app uses CSV, rule-based decisions, template briefs,
and a SQLite outcome ledger. Synthetic Snowflake tables and a Customer 360 view
have been verified separately; the app does not query them. CoCo CLI `sql-author`
and `data-quality` read-only workflows are verified. Cortex inference is not.
No business impact has been measured.
Keep these distinctions visible in the final deck.

## Slide 1: Problem Brief

### Real business problem

Insurance and lending teams do not have one trusted customer view. Customer profile data, policies or loans, claims, support tickets, and call transcripts often sit in different systems. This slows service teams, hides churn signals, and makes next-best-action decisions inconsistent.

### Target users

- Relationship managers
- Claims operations leads
- Customer support specialists
- Retention teams
- Growth advisors
- GCC analytics and operations teams

### Current pain point

Agents spend time reading disconnected records and call notes before deciding what to do. High-risk customers can be missed until they escalate or churn. Managers also lack a governed way to see which customers need action first.

### How the solution improves it

The prototype joins synthetic customer, account, and transcript records. It creates a template brief, explains a service-risk heuristic, assigns a priority tier, and recommends a next best action with evidence, an owner, and a playbook. Agents can record decisions and outcomes. Governed Snowflake storage and Cortex enrichment are planned.

### Industry context

The solution fits insurance, lending, banking, and NBFC operations where customer experience, claim delays, billing disputes, renewal decisions, and retention actions directly affect revenue and trust.

## Slide 2: Architecture Diagram

### System design and data flow

Implemented app flow: CSV -> Pandas -> rules/template brief -> Streamlit -> SQLite ledger.
Separately verified warehouse flow: synthetic seed SQL -> Snowflake tables -> Customer 360 view.
The app is not connected to that view.

Future connected flow (Cortex and activation not executed):

```text
CRM / Policy / Loan / Claim / Call-Center Data
  -> Snowflake Tables
  -> Cortex AI Enrichment
  -> Customer 360 View
  -> Explainable Risk and Next Best Action Engine
  -> Streamlit Command Center
  -> Recommendation Monitoring
```

### CoCo CLI skills and Snowflake capabilities

- CoCo CLI demonstrated `sql-author` on the Customer 360 view and `data-quality` on the source tables; record these actual workflows. No model inference was run.
- Streamlit app pattern supports a fast interactive prototype.
- Cortex AI functions summarize transcripts and classify sentiment.
- Semantic layer pattern supports governed business questions.
- Governance SQL demonstrates masking and data classification.

### Data sources

Structured data:

- Customer profile
- Account and product holdings
- Annual relationship value
- Case status

Unstructured data:

- Call transcripts
- Email notes
- Chat interactions
- Complaint descriptions

### Modular components

- Ingestion layer: CSV demo data or enterprise source feeds
- Storage layer: Snowflake tables
- AI enrichment layer: Cortex summary, sentiment, and next-step generation
- Feature layer: Customer 360 view
- Decision layer: explainable risk scoring and next best action
- App layer: Streamlit command center
- Monitoring layer: recommendation acceptance and outcome tracking

## Slide 3: Impact Statement

### Measurable outcomes

No measured outcomes yet. Evaluate 20 or more independently labelled synthetic scenarios
for service-first routing and evidence correctness. Separately time the same tasks
with manual record review and with this app; report sample size, median times, and
errors. Use a real longitudinal pilot before making retention claims. Automated
regression-test success is not recommendation accuracy or business impact.

- Reduce agent research time by summarizing interaction history.
- Reduce unresolved case aging by prioritizing open complaints.
- Improve retention response by surfacing high-risk customers earlier.
- Increase action consistency by giving agents a clear owner, reason, and playbook.
- Track recommendation acceptance and outcomes after the action.

### Scalability potential

Scalability is untested. The local app loads CSV and calculates features per customer;
it is not a million-customer implementation. A Snowflake version would need SQL
aggregation, pagination, bounded AI processing, durable events, and measured load tests.

### Extension beyond the demo

Future versions can add:

- Snowpark ML churn and uplift model
- Cortex Search over transcripts and claims notes
- Cortex Analyst for natural-language portfolio questions
- Real-time case escalation workflows
- Recommendation A/B testing
- Outcome-based model improvement

## Suggested 5-Slide Deck Flow

1. Title: Customer 360 and Next Best Action Engine
2. Problem Brief: Fragmented customer data slows service and retention teams
3. Architecture: Snowflake-powered customer intelligence flow
4. Product Demo: Customer Copilot and explainable next best action
5. Impact: Faster service, earlier retention action, governed AI at scale

## One-Minute Pitch

We address fragmented customer intelligence for insurers and lenders. Our working
local prototype brings synthetic customer and account data together with call
transcripts, explains service-risk signals, and recommends an action grounded in
unresolved cases. An agent can inspect the evidence, accept a recommendation, and
record an outcome. We verified the same synthetic data in a Snowflake Customer 360
view; the app is not connected, and Cortex inference is not claimed. Our intended
benefit is faster, more consistent service; measured impact and production-scale
validation are still pending.
