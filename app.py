import pandas as pd
import streamlit as st
from html import escape
from pathlib import Path

from src.workflow import STATUSES, read_events, record_event

from src.scoring import (
    ai_brief,
    explain_risk,
    next_best_action,
    risk_band,
    score_customer,
    service_priority,
)


st.set_page_config(
    page_title="Customer 360 Next Best Action",
    page_icon=":bar_chart:",
    layout="wide",
)


@st.cache_data
def load_data():
    data_dir = Path(__file__).resolve().parent / "data"
    customers = pd.read_csv(data_dir / "customers.csv")
    accounts = pd.read_csv(data_dir / "accounts.csv")
    interactions = pd.read_csv(data_dir / "interactions.csv", parse_dates=["interaction_date"])
    return customers, accounts, interactions


def prepare_customers(customers, interactions):
    enriched = customers.copy()
    scores = []
    actions = []
    priorities = []
    briefs = []

    for _, customer in enriched.iterrows():
        customer_interactions = interactions[
            interactions["customer_id"] == customer["customer_id"]
        ].sort_values("interaction_date", ascending=False)
        score = score_customer(customer, customer_interactions)
        action = next_best_action(customer, customer_interactions, score)

        scores.append(score)
        actions.append(action)
        priorities.append(service_priority(customer, customer_interactions, score))
        briefs.append(ai_brief(customer, customer_interactions, action))

    enriched["risk_score"] = scores
    enriched["risk_band"] = enriched["risk_score"].apply(risk_band)
    enriched["next_action"] = [item["action"] for item in actions]
    enriched["action_owner"] = [item["owner"] for item in actions]
    enriched["action_reason"] = [item["reason"] for item in actions]
    enriched["action_playbook"] = [item["playbook"] for item in actions]
    enriched["service_priority"] = priorities
    enriched["ai_brief"] = briefs
    return enriched


customers_raw, accounts, interactions = load_data()
customers = prepare_customers(customers_raw, interactions)

st.markdown(
    """
    <style>
    .block-container { padding-top: 1.4rem; }
    [data-testid="stMetric"] {
        background: #ffffff;
        border: 1px solid #e5e7eb;
        border-radius: 8px;
        padding: 14px 16px;
        color: #17241f;
    }
    [data-testid="stMetricValue"] { font-size: 1.35rem; }
    [data-testid="stMetricValue"] > div,
    [data-testid="stMetricLabel"] p {
        white-space: normal;
        overflow-wrap: anywhere;
        text-overflow: clip;
    }
    h3 { font-size: 1.2rem !important; }
    .insight { color: #17241f; }
    @media (max-width: 900px) {
        [data-testid="stHorizontalBlock"] { flex-wrap: wrap; }
        [data-testid="stColumn"] { min-width: min(100%, 220px); flex: 1 1 220px; }
    }
    .hero {
        border-bottom: 2px solid #16836b;
        padding: 12px 0 20px;
        margin-bottom: 18px;
    }
    .hero h1 {
        margin: 0;
        font-size: 1.8rem;
        line-height: 1.15;
    }
    .hero p {
        margin: 10px 0 0 0;
        max-width: 980px;
        font-size: 1rem;
    }
    .pill {
        display: inline-block;
        border: 1px solid #bae6fd;
        border-radius: 999px;
        padding: 4px 10px;
        margin: 0 8px 8px 0;
        color: #e0f2fe;
        font-size: 0.85rem;
    }
    .insight {
        border-left: 4px solid #2563eb;
        background: #eff6ff;
        padding: 14px 16px;
        border-radius: 6px;
        margin: 8px 0 14px 0;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

st.markdown(
    """
    <div class="hero">
      <h1>Customer 360 and Next Best Action Engine</h1>
    </div>
    """,
    unsafe_allow_html=True,
)
st.caption("Synthetic data | Local CSV-backed demo | Rules-based recommendations | Snowflake warehouse setup verified separately")

total_value = customers["annual_value"].sum()
high_risk = customers[customers["risk_band"] == "High"]
open_cases = interactions[interactions["status"] == "Open"]
negative_interactions = interactions[interactions["sentiment"] == "Negative"]

metric_cols = st.columns(5)
metric_cols[0].metric("Customers", f"{len(customers):,}")
metric_cols[1].metric("High Risk", f"{len(high_risk):,}")
metric_cols[2].metric("Open Cases", f"{len(open_cases):,}")
metric_cols[3].metric("Negative Signals", f"{len(negative_interactions):,}")
metric_cols[4].metric("Annual Value (INR)", f"{total_value / 100000:.1f}L")

executive_tab, copilot_tab, outcomes_tab, architecture_tab, submission_tab = st.tabs(
    ["Portfolio", "Customer Workbench", "Action Outcomes", "Architecture", "Submission Readiness"]
)

with executive_tab:
    st.subheader("Portfolio Intelligence")
    left, right = st.columns([1, 1])

    with left:
        st.write("**Risk Distribution**")
        risk_counts = (
            customers.groupby("risk_band", as_index=False)
            .size()
            .rename(columns={"size": "customers"})
        )
        risk_lookup = dict(zip(risk_counts["risk_band"], risk_counts["customers"]))
        for band in ["High", "Medium", "Low"]:
            count = int(risk_lookup.get(band, 0))
            percent = count / max(len(customers), 1)
            st.markdown(f"**{band}** - {count} customers")
            st.progress(percent, text=f"{percent:.0%} of portfolio")

    with right:
        st.write("**Action Queue**")
        action_counts = (
            customers.groupby("next_action", as_index=False)
            .size()
            .rename(columns={"size": "customers"})
            .sort_values("customers", ascending=False)
        )
        max_actions = max(int(action_counts["customers"].max()), 1)
        for _, row in action_counts.iterrows():
            count = int(row["customers"])
            st.markdown(f"**{row['next_action']}** - {count} customers")
            st.progress(count / max_actions, text=f"{count} recommended")

    st.write("**Top Priority Customers**")
    top_customers = customers.sort_values(
        ["service_priority", "risk_score", "annual_value"], ascending=[True, False, False]
    )
    st.dataframe(
        top_customers[
            [
                "customer_id",
                "name",
                "segment",
                "city",
                "risk_score",
                "risk_band",
                "service_priority",
                "next_action",
                "action_owner",
            ]
        ],
        width="stretch",
        hide_index=True,
    )

with copilot_tab:
    filters, profile = st.columns([0.9, 2.2])

    with filters:
        st.subheader("Customer Queue")
        selected_band = st.multiselect(
            "Risk band",
            ["High", "Medium", "Low"],
            default=["High", "Medium", "Low"],
        )
        selected_segment = st.multiselect(
            "Segment",
            sorted(customers["segment"].unique()),
            default=sorted(customers["segment"].unique()),
        )

        filtered = customers[
            customers["risk_band"].isin(selected_band)
            & customers["segment"].isin(selected_segment)
        ].sort_values("risk_score", ascending=False)

        if filtered.empty:
            st.warning("No matching customers. Showing the full queue until filters match.")
            filtered = customers.sort_values("risk_score", ascending=False)

        selected_customer_id = st.radio(
            "Select customer",
            filtered["customer_id"].tolist(),
            format_func=lambda cid: (
                f"{customers.loc[customers['customer_id'] == cid, 'name'].iloc[0]} "
                f"({cid})"
            ),
        )

    selected_customer = customers[customers["customer_id"] == selected_customer_id].iloc[0]
    selected_accounts = accounts[accounts["customer_id"] == selected_customer_id]
    selected_interactions = interactions[
        interactions["customer_id"] == selected_customer_id
    ].sort_values("interaction_date", ascending=False)
    selected_action = next_best_action(
        selected_customer,
        selected_interactions,
        int(selected_customer["risk_score"]),
    )
    explanation = pd.DataFrame(explain_risk(selected_customer, selected_interactions))

    with profile:
        top = st.columns([1.4, 0.8, 0.8, 1])
        top[0].subheader(f"{selected_customer['name']} - {selected_customer_id}")
        top[1].metric("Risk Score", int(selected_customer["risk_score"]))
        top[2].metric("Risk Band", selected_customer["risk_band"])
        top[3].metric("Priority", selected_customer["service_priority"])

        st.markdown(
            f"""
            <div class="insight">
              <strong>Customer Brief (template):</strong><br/>
              {escape(selected_customer['ai_brief'])}
            </div>
            """,
            unsafe_allow_html=True,
        )

        detail_cols = st.columns(4)
        detail_cols[0].metric("Segment", selected_customer["segment"])
        detail_cols[1].metric("City", selected_customer["city"])
        detail_cols[2].metric("Products", int(selected_customer["product_count"]))
        detail_cols[3].metric("Annual Value", f"INR {selected_customer['annual_value']:,.0f}")

        action_cols = st.columns([1.2, 1])
        with action_cols[0]:
            st.subheader("Recommended Next Best Action")
            st.info(
                f"**{selected_action['action']}**\n\n"
                f"Owner: {selected_action['owner']}\n\n"
                f"Reason: {selected_action['reason']}"
            )
        with action_cols[1]:
            st.subheader("Action Playbook")
            st.success(selected_action["playbook"])

        evidence = selected_interactions[selected_interactions["status"] == "Open"]
        st.write("**Open-case evidence**")
        if evidence.empty:
            st.caption("No unresolved interaction records. Recommendation uses profile and recorded history.")
        else:
            for _, item in evidence.iterrows():
                with st.expander(f"{item['interaction_id']} | {item['issue_type']} | {item['interaction_date']:%d %b %Y}"):
                    st.write(item["transcript"])
                    st.caption(f"Recorded sentiment: {item['sentiment']} | Status: {item['status']}")

        with st.form(f"decision_{selected_customer_id}"):
            st.write("**Action decision**")
            decision = st.selectbox("Decision or outcome", STATUSES)
            notes = st.text_area("Decision / outcome notes", max_chars=2000)
            submitted = st.form_submit_button("Record decision", icon=":material/save:")
            if submitted:
                try:
                    record_event(selected_customer_id, selected_action,
                                 selected_customer["risk_score"], decision, notes,
                                 selected_interactions["interaction_id"].tolist())
                    st.success("Decision saved to the local action ledger. No customer message was sent.")
                except ValueError as error:
                    st.warning(str(error))

        with st.expander("Resolution scenario"):
            close_ids = st.multiselect("Cases to mark closed in simulation", evidence["interaction_id"].tolist())
            scenario = selected_interactions.copy()
            scenario.loc[scenario["interaction_id"].isin(close_ids), "status"] = "Closed"
            scenario_score = score_customer(selected_customer, scenario)
            scenario_action = next_best_action(selected_customer, scenario, scenario_score)
            st.metric("Simulated risk score", scenario_score,
                      delta=scenario_score - int(selected_customer["risk_score"]), delta_color="inverse")
            st.write(f"Scenario recommendation: **{scenario_action['action']}**")
            st.caption("Rules-based scenario, not a prediction of churn reduction. Historical sentiment remains unchanged. Source records are not modified.")

        tab_ai, tab_explain, tab_interactions, tab_accounts = st.tabs(
            ["Latest Interaction", "Explainability", "Interaction History", "Accounts"]
        )

        with tab_ai:
            if selected_interactions.empty:
                st.write("No recent interactions.")
            else:
                latest = selected_interactions.iloc[0]
                st.write("**Latest transcript**")
                st.write(latest["transcript"])
                st.caption(f"Source: {latest['interaction_id']} | Labels supplied in synthetic dataset")
                st.success(
                    f"{latest['issue_type']} interaction with {latest['sentiment'].lower()} "
                    f"sentiment. Status is {latest['status'].lower()}. Recommended focus: "
                    f"{selected_action['action'].lower()}."
                )

        with tab_explain:
            st.write("**Transparent risk score features**")
            explanation["impact"] = explanation["impact"].round(1)
            st.dataframe(explanation, width="stretch", hide_index=True)
            st.caption(
                "Score = sum of contributions, truncated to an integer and bounded to 0-100. "
                "This is a service-risk heuristic, not a calibrated churn probability. All supplied history is included."
            )

        with tab_interactions:
            st.dataframe(
                selected_interactions[
                    [
                        "interaction_date",
                        "channel",
                        "issue_type",
                        "sentiment",
                        "status",
                        "transcript",
                    ]
                ],
                width="stretch",
                hide_index=True,
            )

        with tab_accounts:
            st.dataframe(selected_accounts, width="stretch", hide_index=True)

with outcomes_tab:
    st.subheader("Action Outcomes")
    events = pd.DataFrame(read_events())
    st.caption("Local demo ledger | Human-reported outcomes | Shared by users of this app instance")
    if events.empty:
        st.info("No decisions recorded yet.")
    else:
        latest_decisions = events.drop_duplicates(["customer_id", "action"])
        metrics = st.columns(3)
        metrics[0].metric("Recommendations reviewed", len(latest_decisions))
        metrics[1].metric("Awaiting outcome", int((latest_decisions["status"] == "Accepted").sum()))
        metrics[2].metric("Reported resolved", int((latest_decisions["status"] == "Resolved").sum()))
        st.dataframe(events, hide_index=True, width="stretch")
        st.download_button("Export action ledger", events.to_json(orient="records", indent=2),
                           file_name="action-ledger.json", mime="application/json", icon=":material/download:")

with architecture_tab:
    st.subheader("Deep Technical Design")
    st.warning("The running app uses CSV data and a local SQLite action ledger. Synthetic tables and the Customer 360 view were verified separately in Snowflake; this app does not query them. Cortex enrichment and production governance are proposed, not active.")
    layer_cols = st.columns(4)
    layer_cols[0].markdown("**1. Ingest**\n\nVerified: synthetic customer, account, and interaction records are in Snowflake. Enterprise source feeds are future work.")
    layer_cols[1].markdown("**2. Govern**\n\nFuture work: least-privilege roles, masking, row-access policies, and semantic definitions.")
    layer_cols[2].markdown("**3. Enrich**\n\nFuture work: Cortex summaries and classifications. No model inference has been run.")
    layer_cols[3].markdown("**4. Activate**\n\nCurrent app is local and CSV-backed. Connecting it to the Snowflake view is future work.")

    st.code(
        """
        -- Example only; Cortex enrichment has not been executed in this demo.
        CREATE TABLE IF NOT EXISTS INTERACTION_AI_ENRICHED AS
SELECT
  interaction_id,
  customer_id,
  SNOWFLAKE.CORTEX.SUMMARIZE(transcript) AS ai_summary,
  SNOWFLAKE.CORTEX.CLASSIFY_TEXT(transcript, ['Positive','Neutral','Negative']) AS ai_sentiment,
  SNOWFLAKE.CORTEX.COMPLETE(
    'claude-3-5-sonnet',
    'Recommend one operational next step: ' || transcript
  ) AS ai_recommended_step
FROM interactions;
        """.strip(),
        language="sql",
    )

    st.write("**Production extensions**")
    st.markdown(
        """
        - Dynamic tables for incremental Customer 360 refreshes
        - Cortex Search over call transcripts, emails, and claims notes
        - Cortex Analyst semantic view for trusted natural-language questions
        - Snowpark ML model for churn propensity and uplift scoring
        - Streamlit in Snowflake for governed app access
        - Evaluation table to monitor recommendation acceptance and customer outcome
        """
    )

with submission_tab:
    st.subheader("Submission Evidence")
    st.markdown(
        """
        **Real-world relevance:** GCC teams in insurance, lending, and banking already manage
        fragmented customer records and manual service prioritization.

        **Technical execution:** The local demo includes explainable rules, evidence references,
        action decisions, outcome history, and resolution scenarios. AI and governance SQL are proposed integrations.

        **Completeness:** The repo includes app code, sample data, Snowflake SQL scripts,
        architecture notes, submission text, and a demo script.
        """
    )

    st.write("**Submission checklist**")
    checklist = pd.DataFrame(
        [
            ["GitHub repository", "Local repository only; remote not verified"],
            ["Working local demo", "Ready"],
            ["Synthetic dataset", "Ready"],
            ["Snowflake tables and Customer 360 view", "Verified in trial account; 10 customers, 12 accounts, 11 interactions"],
            ["CoCo CLI skills", "Verified read-only sql-author query and data-quality audit"],
            ["Live Cortex integration", "Not run; no model inference claimed"],
            ["Measured business impact", "Pending pilot"],
            ["Submission deck", "5-slide PDF and editable PPTX prepared"],
            ["Architecture explanation", "Ready"],
            ["Demo script", "Ready"],
            ["Deployment link", "Pending after GitHub push"],
            ["Demo video", "Pending recording"],
        ],
        columns=["Item", "Status"],
    )
    st.dataframe(checklist, width="stretch", hide_index=True)
