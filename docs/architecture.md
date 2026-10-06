# Architecture

## Data Layer

The prototype uses synthetic CSV data that can be loaded into Snowflake tables:

- `CUSTOMERS`
- `ACCOUNTS`
- `INTERACTIONS`

## AI Enrichment Layer

The `INTERACTIONS` table contains unstructured call and chat transcripts. Snowflake Cortex can summarize transcripts, classify sentiment, and recommend operational follow-ups.

## Customer 360 Layer

The `CUSTOMER_360` view joins customer attributes, account holdings, interaction counts, open cases, and negative sentiment signals.

## Application Layer

The Streamlit app reads the sample data locally for demo convenience. In production, the same app can connect to Snowflake and read from `CUSTOMER_360` plus the enriched interaction tables.

## Governance

All data in this repository is synthetic. In a production deployment, role-based access control, masking policies, and row access policies can be applied in Snowflake.
