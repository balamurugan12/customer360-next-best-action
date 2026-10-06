# Technical Design

Implementation status: only CSV-backed profiles, deterministic rules, template briefs,
evidence display, resolution scenarios, and SQLite action events run today. Cortex,
Snowflake governance, semantic models, and ML below are proposed capabilities.

## Product Vision

Customer 360 and Next Best Action Engine is designed as an operational AI layer for insurers and lenders. It helps service, retention, claims, and growth teams decide which customer needs attention, why they need it, and what action should happen next.

## Core Data Model

- `CUSTOMERS`: profile, segment, region, relationship value
- `ACCOUNTS`: policies, loans, cover, balances
- `INTERACTIONS`: call, email, and chat transcripts
- `INTERACTION_AI_ENRICHED`: Cortex-generated summaries and sentiment labels
- `CUSTOMER_360`: governed customer-level feature view
- `RECOMMENDATION_EVENTS`: monitoring table for recommendation outcomes

## Planned AI Capabilities

1. Transcript summarization using Cortex.
2. Sentiment classification using Cortex.
3. Complaint theme detection from interaction text.
4. Explainable churn/service-risk scoring.
5. Next best action generation.
6. Recommendation outcome monitoring.

## Enterprise Readiness Target

The following capabilities must be integrated and validated before an enterprise-ready claim:

- Governed data foundation
- Explainable recommendation logic
- Human-readable action playbooks
- Customer-level prioritization
- Monitoring for recommendation acceptance and outcomes
- Clear path to Snowpark ML and Cortex Analyst

## Snowflake Production Path

1. Load CRM, account, claims, and interaction feeds into Snowflake.
2. Use dynamic tables to refresh Customer 360 features.
3. Use Cortex AI functions to enrich unstructured transcripts.
4. Use Cortex Search to retrieve evidence from interaction history.
5. Use Cortex Analyst over semantic views for trusted business questions.
6. Deploy the app in Streamlit in Snowflake.
7. Monitor actions and outcomes through `RECOMMENDATION_EVENTS`.

## Evaluation Approach

The prototype can be evaluated with:

- Recommendation acceptance rate
- Open case aging reduction
- Claim turnaround time reduction
- Repeat contact reduction
- Churn-risk movement after intervention
- Cross-sell conversion for low-risk high-value customers

## Security And Governance

In production, the app should use:

- Role-based access control
- Masking policies for customer identity
- Row access policies by business unit or region
- Tags for sensitive data classification
- Audit history for generated recommendations
