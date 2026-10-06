# Demo Script

## Opening

We selected the Customer 360 and Next Best Action Engine problem statement because insurers and lenders often struggle with fragmented customer data across policies, loans, claims, support tickets, and call-center transcripts.

## Show Dashboard

The first screen gives a portfolio view of 10 synthetic customers: heuristic risk, open cases, supplied sentiment labels, and annual relationship value. State clearly that this is local demo mode.

## Customer Drilldown

Select C1001. The profile combines customer and account data with transcript history. The template brief gives a concise summary of recorded labels; it is not LLM-generated.

## AI Insight

Expand evidence I5001 to inspect the unresolved claim transcript. Snowflake Cortex enrichment is a proposed integration; do not present this as a live AI result.

## Next Best Action

The rules select Fast-track claim review because an unresolved claim requires a specialist. Record Accepted, then Resolved with an outcome note. Open Action Outcomes to show persistence and export. These are human-reported demo outcomes, not measured retention improvements. Use Resolution scenario to close I5001 hypothetically and show the resulting score; source data stays unchanged.

## Explainability

Open the explainability tab to show the transparent feature contributions behind the risk score. This is important for enterprise adoption because agents and managers can see why the system is recommending an action.

## Snowflake Value

The synthetic tables and Customer 360 view were verified in the Snowflake trial account using Snowsight on an X-Small warehouse. CoCo CLI demonstrated `sql-author` against the view and `data-quality` for row counts, duplicate IDs, nulls, and orphan references using read-only SQL. The audit found 10 customers, 12 accounts, 11 interactions, and no duplicate IDs, null join keys, or orphan references. The Streamlit app remains CSV-backed and is not connected to Snowflake. Cortex output, governance grants, and live app integration are not demonstrated.

## Closing

The working result is an evidence-led service decision prototype with a separately verified Snowflake data layer. A connected app and measured pilot are needed to validate AI quality, scalability, productivity, and retention benefits.
