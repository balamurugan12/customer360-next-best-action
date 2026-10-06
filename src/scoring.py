def risk_band(score: int) -> str:
    if score >= 70:
        return "High"
    if score >= 45:
        return "Medium"
    return "Low"


def customer_signals(customer_row, interactions):
    complaint_count = int((interactions["issue_type"] == "Complaint").sum())
    claim_delay_count = int((interactions["issue_type"] == "Claim Delay").sum())
    billing_count = int((interactions["issue_type"] == "Billing").sum())
    negative_count = int((interactions["sentiment"] == "Negative").sum())
    open_cases = int((interactions["status"] == "Open").sum())
    product_count = int(customer_row["product_count"])
    tenure_years = float(customer_row["tenure_years"])
    annual_value = float(customer_row["annual_value"])
    interaction_count = int(len(interactions))

    return {
        "complaint_count": complaint_count,
        "claim_delay_count": claim_delay_count,
        "billing_count": billing_count,
        "negative_count": negative_count,
        "open_cases": open_cases,
        "product_count": product_count,
        "tenure_years": tenure_years,
        "annual_value": annual_value,
        "interaction_count": interaction_count,
    }


def explain_risk(customer_row, interactions):
    signals = customer_signals(customer_row, interactions)
    contributions = [
        {"signal": "Baseline", "value": 1, "impact": 35},
        {
            "signal": "Negative interactions",
            "value": signals["negative_count"],
            "impact": signals["negative_count"] * 15,
        },
        {
            "signal": "Open service cases",
            "value": signals["open_cases"],
            "impact": signals["open_cases"] * 15,
        },
        {
            "signal": "Formal complaints",
            "value": signals["complaint_count"],
            "impact": signals["complaint_count"] * 20,
        },
        {
            "signal": "Claim delay mentions",
            "value": signals["claim_delay_count"],
            "impact": signals["claim_delay_count"] * 18,
        },
        {
            "signal": "Billing issue mentions",
            "value": signals["billing_count"],
            "impact": signals["billing_count"] * 12,
        },
        {
            "signal": "Product relationship depth",
            "value": signals["product_count"],
            "impact": -min(signals["product_count"] * 2, 10),
        },
        {
            "signal": "Tenure stability",
            "value": round(signals["tenure_years"], 1),
            "impact": -min(signals["tenure_years"], 8),
        },
        {
            "signal": "High value relationship",
            "value": int(signals["annual_value"]),
            "impact": -3 if signals["annual_value"] >= 150000 else 0,
        },
    ]
    return contributions


def score_customer(customer_row, interactions):
    contributions = explain_risk(customer_row, interactions)

    score = sum(item["impact"] for item in contributions)

    return max(0, min(100, int(score)))


def service_priority(customer_row, interactions, risk_score):
    annual_value = float(customer_row["annual_value"])
    open_cases = int((interactions["status"] == "Open").sum()) if len(interactions) else 0
    priority = risk_score + (annual_value / 25000) + (open_cases * 6)
    if priority >= 90:
        return "P0 - executive escalation"
    if priority >= 65:
        return "P1 - same day action"
    if priority >= 45:
        return "P2 - proactive follow-up"
    return "P3 - nurture"


def ai_brief(customer_row, interactions, action):
    if interactions.empty:
        return "No recent interaction history is available. Continue standard engagement."

    interactions = interactions.sort_values(["interaction_date", "interaction_id"], ascending=[False, True])
    latest = interactions.iloc[0]
    themes = interactions["issue_type"].value_counts().head(2).index.tolist()
    theme_text = ", ".join(themes).lower()
    sentiment_mix = interactions["sentiment"].value_counts().to_dict()
    negative_count = int(sentiment_mix.get("Negative", 0))

    if negative_count:
        tone = f"{negative_count} negative signal(s)"
    else:
        tone = "no major negative signal"

    return (
        f"{customer_row['name']} is a {customer_row['segment'].lower()} customer with "
        f"recent themes around {theme_text}. The latest touchpoint is a "
        f"{latest['issue_type'].lower()} case over {latest['channel'].lower()}, with "
        f"{tone}. Recommended action: {action['action']} because {action['reason'].lower()}"
    )


def next_best_action(customer_row, interactions, risk_score):
    open_interactions = interactions[interactions["status"] == "Open"].sort_values(
        "interaction_date", ascending=False
    )
    open_issues = set(open_interactions["issue_type"])
    has_open_case = not open_interactions.empty
    product_count = int(customer_row["product_count"])
    annual_value = float(customer_row["annual_value"])

    if "Claim Delay" in open_issues:
        return {
            "action": "Fast-track claim review",
            "owner": "Claims operations lead",
            "reason": "An unresolved claim delay requires a claims specialist.",
            "playbook": "Validate documents, publish decision timeline, and trigger claim operations escalation.",
        }

    if "Billing" in open_issues:
        return {
            "action": "Resolve billing dispute",
            "owner": "Support specialist",
            "reason": "An unresolved billing issue requires reconciliation before outreach.",
            "playbook": "Reconcile debit history, reverse duplicate charge if valid, and confirm closure.",
        }

    if risk_score >= 70 and has_open_case:
        return {
            "action": "Priority retention call",
            "owner": "Senior relationship manager",
            "reason": "High service-risk score with an unresolved customer issue.",
            "playbook": "Acknowledge friction, commit an SLA, offer a named owner, and schedule a follow-up.",
        }

    if has_open_case:
        return {
            "action": "Resolve open service case",
            "owner": "Support specialist",
            "reason": "An unresolved service issue takes priority over growth outreach.",
            "playbook": "Assign a case owner, confirm the outstanding request, and agree a follow-up date.",
        }

    if not interactions.empty and risk_score <= 35 and product_count <= 2 and annual_value >= 90000:
        return {
            "action": "Personalized cross-sell offer",
            "owner": "Growth advisor",
            "reason": "Low-risk, high-value customer with room for portfolio expansion.",
            "playbook": "Recommend one relevant product using current holdings and next likely need.",
        }

    if risk_score >= 45:
        return {
            "action": "Proactive service check-in",
            "owner": "Relationship manager",
            "reason": "Moderate risk signals suggest intervention before escalation.",
            "playbook": "Call within 48 hours, confirm service experience, and prevent repeat contact.",
        }

    return {
        "action": "Maintain and nurture",
        "owner": "Customer success team",
        "reason": "Customer appears stable; continue regular engagement.",
        "playbook": "Keep regular engagement cadence and monitor for new negative signals.",
    }
