# Product Review - 6 October 2026

## Verdict

Good problem fit; improved local prototype; not yet a competitive, complete
Snowflake/CoCo submission. The prior claim that the product was ready overstated
what was implemented. UI polish cannot replace the required executable workflow.

## Portal Requirements Verified in the Registered Dashboard

The logged-in roadmap shows both submission modules open until **6 October 2026,
11:59 PM IST**. This differs from the public page, which still lists October 4.
No submission was made during this review.

Prototype/MVP form requires:

- Selected challenge: Customer 360 and Next Best Action Engine.
- Prototype/MVP brief, maximum 1,024 characters.
- Demo video link. The instructions specify a 3-5 minute screen recording of an
  end-to-end CoCo CLI workflow (input -> processing -> output), at least one fully
  working workflow, and 2-3 modular skills/capabilities demonstrated.
- Prototype deck as PDF, at most 5 MB. The form links an official slide template.

The separate GitHub/Deployed Link module requires both a public GitHub repository
URL and a deployed prototype URL, plus the selected challenge. Localhost does not
meet the deployed-link requirement.

Official template:
https://docs.google.com/presentation/d/13NuvogeWZdOF_RKe074MGKbfd9zoZVbmJmFcGYBWyxM/export/pptx

## Remaining Findings, Ordered by Severity

1. **P1: Required CoCo CLI video evidence is absent.** The official CoCo CLI is
   installed and authenticated. `sql-author` successfully queried the Customer
   360 view, and `data-quality` checked the synthetic source tables with read-only
   SQL. The required 3-5 minute video showing these skills has not been recorded.
   Non-interactive CoCo execution is unavailable on this trial account.
2. **P1: No live AI or app-to-Snowflake integration.** `app.py:load_data` reads
   CSV and `src/scoring.py:ai_brief` assembles a template. Synthetic Snowflake
   tables and the `CUSTOMER_360` view are now verified, but neither Cortex output
   nor the Snowflake view is consumed by the app. Add source-linked AI output and
   an explicit failure state only after a real model run.
3. **P1: Video and deployment remain outstanding.** The 5-slide PDF and editable
   PPTX are ready, and the source repository is public at
   https://github.com/balamurugan12/customer360-next-best-action. No screen
   recording or public deployment exists yet.
4. **P2: Scoring and impact are unvalidated.** Ten synthetic customers and eleven
   interactions cannot establish accuracy or retention lift. Hand-set weights
   count all history and can saturate. Financial value reduces the risk heuristic
   without empirical calibration. Validate weights/time windows, compare against
   a simple baseline, and keep the score distinct from churn probability.
5. **P2: Storage/governance is demo-only.** SQLite has no user authentication or
   per-team access controls. Outcomes are self-reported. SQL roles are referenced
   but not created/granted. The semantic-base view is not an Analyst semantic
   model, and summed account balances/insurance cover mix different concepts.
6. **P2: Scale and ingestion quality remain untested.** The app reads entire CSVs
   and filters interactions for every customer on each rerun. No external upload,
   schema validation, duplicate identity reconciliation, or incremental ingestion
   is implemented. Production deployment needs SQL aggregation and pagination.

## Fixes Implemented

- Updated dependency pins to match the working Streamlit/Pandas environment;
  the old Streamlit pin did not match the app's newer width API.
- Data paths now resolve relative to the app, independent of launch directory.
- Closed claim records cannot trigger active claim escalation; older unresolved
  cases remain actionable even after a newer unrelated touchpoint.
- Specialist claim/billing action takes precedence over generic retention calls.
- Open cases block growth offers; missing history does not trigger cross-sell.
- Risk explanations include baseline; the UI documents integer rounding and bounds.
- Briefs are stable across reordered history, and interpolated HTML is escaped.
- Empty filters no longer prevent subsequent tabs from rendering.
- Added transcript evidence, persistent decisions/outcomes, and JSON export.
- Added a non-mutating resolution scenario, explicitly not a causal prediction.
- Removed misleading AI/runtime-readiness claims and decorative metric trend arrows.
- Tightened headings and responsive metric layout for narrower browser panels.
- Created the synthetic Snowflake database, schema, tables, seed rows, and
  `CUSTOMER_360` view with the X-Small `COMPUTE_WH`; verified counts are 10
  customers, 12 accounts, 11 interactions, and 10 view rows.
- Changed table setup to `CREATE TABLE IF NOT EXISTS` and added a `MERGE` seed
  script to avoid replacing tables or duplicating the fixed synthetic data.
- Updated dashboard, README, submission copy, and demo narration to separate
  verified Snowflake setup from the still-CSV-backed app and unrun Cortex work.
- Verified CoCo CLI `sql-author` and `data-quality` workflows against Snowflake;
  the spot check found 10/12/11 rows, unique IDs, and no null or orphan join keys.

## Verification

`python3 -m unittest discover -s tests -v`: 10 tests pass, including all ten
customer profiles, empty filters, scenario interaction, accept/resolve UI flow,
persistence, invalid transitions, duplicate decisions, missing outcome notes,
closed claims, older unresolved cases, and explanation reconciliation.

The live browser renders the updated local app. Tests use temporary ledgers, so
test outcomes do not inflate the demo's real recorded metrics. Snowflake seed
execution was done in Snowsight; CoCo CLI queries used the verified `sql-author`
and `data-quality` skills. Cortex inference, public deployment,
model quality, and load/scale are not verified.
Visual inspection confirmed the 694px-wide in-app browser layout without page-level
horizontal overflow. The browser ignored the requested 390px override, so a true
mobile-width render has not been verified.

## Strongest Demo Story

Focus on evidence-led service recovery: an unresolved claim is identified, the
agent checks the transcript, accepts a specialist action, and records the outcome.
Show the decision trail and a labelled scenario. Add real Cortex summaries to
this workflow and demonstrate it through CoCo; avoid scattering effort across
unimplemented underwriting, chat, and autonomous outreach claims.
