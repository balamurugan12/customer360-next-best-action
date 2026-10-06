# Hackathon Submission Content

## Project Title

Customer 360 and Next Best Action Engine

## Selected Problem Statement

Customer 360 and Next Best Action Engine

## Short Description

A local Customer 360 prototype that unifies synthetic customer, account, and interaction data, explains service-risk rules, and recommends operational actions with evidence, ownership, and a saved decision history. Its synthetic tables and Customer 360 view have been verified in Snowflake; the app remains local and CSV-backed.

## Long Description

The solution addresses fragmented customer intelligence in insurance and lending organizations. Customer-facing teams often lack a single trusted view of customers because profile data, policy or loan data, transactions, support cases, and call transcripts live in separate systems.

The prototype combines structured synthetic customer and account data with interaction transcripts. A Snowflake `CUSTOMER_360` view was verified over 10 synthetic customers, and the interactive Streamlit app currently runs separately against local CSV files. It applies transparent rules to identify service risk and recommends an action with evidence, owner, priority tier, and playbook. These rules are not a churn model. Cortex enrichment is proposed and has not been run.

## Key Features

- Customer 360 profile
- Portfolio-level risk dashboard
- High-risk customer filtering
- Interaction history with original transcripts and evidence IDs
- Sentiment and complaint signals
- Next Best Action recommendation
- Template-generated customer brief
- Explainable risk drivers
- Operational action playbooks
- Local decision and outcome ledger with JSON export
- Resolution scenario simulation
- Snowflake SQL scripts for data modeling and AI enrichment

## Business Impact

These are intended benefits, not measured results. No churn reduction, accuracy improvement, or time saving has been demonstrated yet.

- Reduces customer churn through early intervention
- Improves agent productivity by summarizing interaction history
- Increases consistency of service and retention actions
- Creates a governed data layer for analytics and AI
- Helps insurers and lenders personalize customer engagement

## How Snowflake Is Used

The running app uses local CSV and SQLite. Snowflake table creation, synthetic seed data, and the `CUSTOMER_360` view were verified separately in Snowsight. CoCo CLI demonstrated `sql-author` and `data-quality` with read-only SQL. No live Cortex result or app-to-Snowflake connection is claimed.

- Snowflake tables store customer, account, and interaction data.
- Snowflake currently stores the synthetic demo tables and exposes a Customer 360 view.
- Snowflake Cortex summarization and classification remain future work.
- Governance SQL demonstrates masking and data-classification patterns.
- Recommendation monitoring captures acceptance and business outcomes.
- The app can be connected to Snowflake for live governed analytics.
- Snowflake CoCo CLI can accelerate SQL, app, and deployment workflows.

## GitHub Repository

https://github.com/balamurugan12/customer360-next-best-action

## Deployment Link

Add your Streamlit, Snowflake, or other deployment link here after publishing the app.

## Demo Video Link

Add your demo video link here after recording.
