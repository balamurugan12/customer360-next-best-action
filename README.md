# Customer 360 and Next Best Action Engine

Hackathon submission for Snowflake CoCo CLI Hackathon 2026 - GCC Edition.

## Verified Status (6 October 2026)

This is a local prototype, not a production-ready Snowflake application. It uses
10 synthetic customers, 12 accounts, and 11 interactions. Sentiment/issue labels
are supplied in the dataset, briefs are templates, and service-risk scores and
recommendations are deterministic rules. Scores are not churn probabilities.
On 6 October 2026, the synthetic data was also loaded into the
`CUSTOMER360_HACKATHON.APP` Snowflake schema and the `CUSTOMER_360` view was
verified (10 rows) using Snowsight and the X-Small `COMPUTE_WH`. The Streamlit
app still reads local CSV files; it is not connected to Snowflake. CoCo CLI
demonstrated the bundled `sql-author` and `data-quality` skills with read-only
queries. The audit found 10/12/11 rows, unique IDs, and no null or orphan customer
keys. No Cortex model inference was run.

Working features include evidence references, service-first recommendations,
decision/outcome recording, JSON ledger export, and resolution scenarios. The local
SQLite ledger lives in `runtime/` (excluded from Git), is shared by app users, and
has no authentication. Use only synthetic demo data. Ephemeral hosting can lose
the ledger on redeploy. Reported outcomes do not change source case records.

No business impact has been measured. The five-slide PDF deck and editable PPTX
are ready. The source repository is public at
https://github.com/balamurugan12/customer360-next-best-action. A screen-recorded
demo, public deployment, and submission remain pending.
See `docs/product-review.md` for the full review.

## Problem Statement

Insurers and lenders want a unified customer view to drive personalization, smarter underwriting, and churn reduction.

This prototype combines customer profiles, account holdings, and transcript records. It calculates rule-based service signals and recommends an operational action. Separate transaction and claims datasets are not included.

## Solution Overview

The app provides:

- Unified Customer 360 profile
- Heuristic service-risk scoring
- Template briefs and original transcripts
- Supplied sentiment and complaint labels
- Next Best Action recommendations
- Explainable risk drivers
- Service priority tiers
- Action playbooks for human teams
- Persistent local recommendation decisions and outcomes
- Portfolio-level executive dashboard
- Snowflake SQL scripts for table creation and Cortex AI enrichment

## Why This Matters

Customer-facing teams often work across CRM, policy, loan, transaction, support, and call-center systems. This creates fragmented decision-making. The solution gives agents and managers a single trusted view of each customer and recommends an action based on governed data signals.

## Architecture

Running app flow: CSV -> Pandas -> rules and template briefs -> Streamlit -> SQLite ledger.
Separately verified Snowflake flow: synthetic seed SQL -> Snowflake tables -> Customer 360 view.

Proposed Snowflake integration, not currently running:

```text
Synthetic Data
  -> Snowflake Tables -> Customer 360 View (verified)
  -> Cortex AI Enrichment (proposed; not run)
  -> Streamlit App (currently local CSV-backed)
  -> Next Best Action Dashboard
```

## Tech Stack

- Python
- Streamlit
- Pandas
- Snowflake SQL
- Snowflake Cortex AI functions
- Snowflake CoCo CLI `sql-author` and `data-quality` skills (read-only workflows verified)

## Repository Structure

```text
customer360-next-best-action/
  app.py
  requirements.txt
  data/
    customers.csv
    accounts.csv
    interactions.csv
    recommendations.csv
  sql/
    01_create_tables.sql
    02_cortex_enrichment.sql
    03_customer_360_view.sql
    04_governance_and_semantic_layer.sql
    05_recommendation_monitoring.sql
    06_seed_synthetic_data.sql
  src/
    scoring.py
  docs/
    submission.md
    submission-deck.md
    demo-script.md
    architecture.md
    technical-design.md
```

## Local Setup

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
streamlit run app.py
```

Verified environment: Python 3.9, Streamlit 1.50.0, Pandas 2.3.3.

Run regression and Streamlit workflow checks:

```bash
python -m unittest discover -s tests -v
```

## Snowflake Setup

Verified in the registered trial account on 6 October 2026 using the existing
X-Small `COMPUTE_WH`: database/schema creation, synthetic seed data, and the
Customer 360 view. `sql/01_create_tables.sql` is non-destructive and
`sql/06_seed_synthetic_data.sql` uses `MERGE` so rerunning it does not duplicate
the seed rows. These scripts do not create a new warehouse. The live Streamlit
app is still CSV-backed; do not describe this as a deployed integration.

The CoCo CLI OAuth connection is valid, and interactive read-only execution was
verified with `sql-author` and `data-quality`. The CLI's non-interactive mode is
not available on this trial. Cortex enrichment, model availability, governance
grants, and Snowflake-to-app connectivity are not implemented. Cortex model
calls may consume additional trial credits and have not been run.

1. Create a database and schema for the project.
2. Run `sql/01_create_tables.sql`.
3. Run `sql/06_seed_synthetic_data.sql`.
4. Run `sql/03_customer_360_view.sql`.
5. Verify row counts and view output before connecting an application.

## Demo Flow

1. Open the dashboard and show portfolio metrics.
2. Filter to high-risk customers.
3. Select a customer profile.
4. Show structured profile, source transcripts, template brief, and service-risk signals.
5. Show the recommended next best action and explain why it was selected.
6. Explain how Snowflake enables governed analytics and AI enrichment.

## Judging Alignment

### Real-World Relevance

The solution addresses a common problem in banking, insurance, and lending GCCs: fragmented customer data and inconsistent service actions.

### Technical Execution

The app includes data modeling, explainable scoring, AI-ready transcript processing, governance patterns, semantic-layer design, recommendation monitoring, Snowflake SQL, and an interactive dashboard.

### Solution Completeness

The repository includes working code, sample data, setup instructions, architecture notes, and a demo script.

## Notes

All included data is synthetic and safe for demo use.

## Winning Demo Angle

Current verified story:

1. Structured customer data and unstructured transcripts come together.
2. Snowflake materializes a unified customer view (verified on 10 synthetic rows).
3. The local app explains rule-based service risk and prioritizes human action.
4. Human decisions and outcomes are recorded in a local SQLite ledger.

Cortex summaries, production-scale impact, and a hosted Snowflake-connected app
remain future work, not demo claims.
