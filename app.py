import streamlit as st
import pandas as pd
from sklearn.ensemble import IsolationForest

# Page settings
st.set_page_config(
    page_title="FinMatch AI",
    page_icon="💰",
    layout="wide"
)

# Load reconciliation results
results = pd.read_csv("data/reconciliation_results.csv")
# ML-based financial anomaly detection
ml_data = results.copy()

ml_data["Exception_Flag"] = (
    ml_data["Status"] != "MATCHED"
).astype(int)

ml_features = ml_data[
    ["Invoice Amount", "Financial Impact", "Exception_Flag"]
].fillna(0)

anomaly_model = IsolationForest(
    n_estimators=100,
    contamination="auto",
    random_state=42
)

anomaly_model.fit(ml_features)

results["ML_Anomaly_Score"] = -anomaly_model.decision_function(
    ml_features
)

results["ML_Anomaly"] = (
    anomaly_model.predict(ml_features) == -1
)
# Title
st.title("💰 FinMatch AI")
st.subheader("AI Finance Reconciliation Agent")

st.divider()

# ==============================
# KEY METRICS
# ==============================

total = len(results)

matched = len(
    results[results["Status"] == "MATCHED"]
)

exceptions = total - matched

match_rate = (matched / total) * 100

high_priority = len(
    results[results["Priority"] == "HIGH"]
)

medium_priority = len(
    results[results["Priority"] == "MEDIUM"]
)

exception_value = results[
    results["Status"] != "MATCHED"
]["Financial Impact"].sum()

# Four dashboard cards
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("Total Invoices", total)

with col2:
    st.metric("Matched", matched)

with col3:
    st.metric("Exceptions", exceptions)

with col4:
    st.metric("Match Rate", f"{match_rate:.1f}%")

st.divider()

# ==============================
# PRIORITY SUMMARY
# ==============================

st.subheader("⚠️ Exception Overview")

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("🔴 High Priority", high_priority)

with col2:
    st.metric("🟠 Medium Priority", medium_priority)

with col3:
    st.metric(
        "💰 Exception Value",
        f"₹{exception_value:,.0f}"
    )

st.divider()

# ==============================
# EXCEPTION TABLE
# ==============================

st.subheader("📋 Exception Details")

exceptions_df = results[
    results["Status"] != "MATCHED"
].copy()

# Filters
col1, col2, col3 = st.columns(3)

with col1:
    status_filter = st.multiselect(
        "Filter by Status",
        options=exceptions_df["Status"].unique(),
        default=exceptions_df["Status"].unique()
    )

with col2:
    priority_filter = st.multiselect(
        "Filter by Priority",
        options=exceptions_df["Priority"].unique(),
        default=exceptions_df["Priority"].unique()
    )

with col3:
    vendor_filter = st.multiselect(
        "Filter by Vendor",
        options=exceptions_df["Vendor"].unique(),
        default=exceptions_df["Vendor"].unique()
    )

# Apply filters
exceptions_df = exceptions_df[
    (exceptions_df["Status"].isin(status_filter)) &
    (exceptions_df["Priority"].isin(priority_filter)) &
    (exceptions_df["Vendor"].isin(vendor_filter))
]
# Show selected columns
display_columns = [
    "Invoice",
    "Vendor",
    "Invoice Amount",
    "Status",
    "Priority",
    "Financial Impact",
    "Explanation",
    "Recommended Action"
]

st.dataframe(
    exceptions_df[display_columns],
    width="stretch",
    hide_index=True
)
# Download filtered results
csv_data = exceptions_df[display_columns].to_csv(index=False)

st.download_button(
    label="📥 Download Filtered Exceptions",
    data=csv_data,
    file_name="finmatch_exceptions.csv",
    mime="text/csv"
)
st.divider()

# ==============================
# STATUS BREAKDOWN
# ==============================

st.subheader("📊 Reconciliation Status")

status_counts = results["Status"].value_counts()

status_chart = status_counts.reset_index()
status_chart.columns = ["Status", "Count"]

st.bar_chart(
    status_chart,
    x="Status",
    y="Count",
    width="stretch"
)
st.divider()

# ==============================
# AI FINANCIAL INSIGHTS
# ==============================

st.subheader("🤖 AI Financial Insights")

total_exceptions = len(exceptions_df)
total_impact = exceptions_df["Financial Impact"].sum()

high_priority = len(
    exceptions_df[exceptions_df["Priority"] == "HIGH"]
)

medium_priority = len(
    exceptions_df[exceptions_df["Priority"] == "MEDIUM"]
)

status_counts = exceptions_df["Status"].value_counts()

missing_payments = status_counts.get("MISSING PAYMENT", 0)
duplicate_payments = status_counts.get("DUPLICATE PAYMENT", 0)
amount_mismatches = status_counts.get("AMOUNT MISMATCH", 0)

st.info(
    f"💡 **AI Insight:** {total_exceptions} invoices require attention, "
    f"representing a potential financial impact of ₹{total_impact:,.0f}. "
    f"There are {high_priority} high-priority exceptions and "
    f"{medium_priority} medium-priority exceptions."
)

st.markdown("### 🎯 Recommended Priorities")

if missing_payments > 0:
    st.write(
        f"🔴 **1. Resolve missing payments** — "
        f"{missing_payments} invoice(s) have no corresponding payment."
    )

if duplicate_payments > 0:
    st.write(
        f"🔴 **2. Investigate duplicate payments** — "
        f"{duplicate_payments} invoice(s) may have been paid more than once."
    )

if amount_mismatches > 0:
    st.write(
        f"🟠 **3. Review amount mismatches** — "
        f"{amount_mismatches} invoice(s) have differences between invoice and payment amounts."
    )

st.success(
    "📊 **Recommended Action:** Start with high-priority exceptions "
    "and investigate the largest financial impacts first."
)
st.divider()

# ==============================
# HOW FINMATCH AI WORKS
# ==============================

st.subheader("🧠 How FinMatch AI Works")

col1, col2, col3, col4, col5 = st.columns(5)

with col1:
    st.markdown("### 📄")
    st.markdown("**1. Invoice Data**")
    st.caption("Reads invoice records and amounts.")

with col2:
    st.markdown("### 💳")
    st.markdown("**2. Payment Data**")
    st.caption("Reads payment transactions.")

with col3:
    st.markdown("### 🔍")
    st.markdown("**3. Reconciliation**")
    st.caption("Matches invoices with payments.")

with col4:
    st.markdown("### 🚨")
    st.markdown("**4. Exception Detection**")
    st.caption("Detects missing, duplicate and mismatched payments.")

with col5:
    st.markdown("### 🤖")
    st.markdown("**5. AI Recommendation**")
    st.caption("Explains exceptions and recommends actions.")
    st.divider()

# ==============================
# INTERACTIVE AI INVESTIGATOR
# ==============================

st.subheader("🤖 AI Exception Investigator")

if len(exceptions_df) > 0:

    selected_invoice = st.selectbox(
        "Select an exception to investigate:",
        exceptions_df["Invoice"].tolist()
    )

    selected = exceptions_df[
        exceptions_df["Invoice"] == selected_invoice
    ].iloc[0]

    st.markdown("### 🔎 Investigation Result")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            "Invoice",
            selected["Invoice"]
        )

    with col2:
        st.metric(
            "Financial Impact",
            f"₹{selected['Financial Impact']:,.0f}"
        )

    with col3:
        st.metric(
            "Priority",
            selected["Priority"]
        )

    st.markdown("#### 🚨 Problem Detected")
    st.warning(
        f"**{selected['Status']}** — {selected['Explanation']}"
    )

    st.markdown("#### 🤖 AI Investigation")
# ML-based risk assessment for the selected exception
ml_record = results[results["Invoice"] == selected["Invoice"]]

if not ml_record.empty:
    ml_row = ml_record.iloc[0]
    ml_score = float(ml_row["ML_Anomaly_Score"])
    ml_anomaly = bool(ml_row["ML_Anomaly"])

    if ml_anomaly:
        st.error("🔴 ML Risk Signal: Anomalous financial pattern detected")
    else:
        st.success("🟢 ML Risk Signal: No unusual financial pattern detected")

    st.caption(
        f"ML anomaly score: {ml_score:.3f} | "
        f"Model considers invoice amount, financial impact, and exception status."
    )

    if selected["Status"] == "MISSING PAYMENT":

        st.info(
            "No corresponding payment was found. "
            "Verify whether the payment was processed under a "
            "different transaction reference, date, or account."
        )

        st.markdown(
            "**Recommended Next Action:** "
            "Contact the payment team and verify the payment status."
        )

    elif selected["Status"] == "DUPLICATE PAYMENT":

        st.info(
            "Multiple payments were detected for the same invoice. "
            "This may indicate a duplicate transaction or repeated payment."
        )

        st.markdown(
            "**Recommended Next Action:** "
            "Review the duplicate transactions and determine whether "
            "a refund or accounting adjustment is required."
        )

    elif selected["Status"] == "AMOUNT MISMATCH":

        st.info(
            "The invoice amount does not match the payment received. "
            "The difference should be verified against the payment records."
        )

        st.markdown(
            "**Recommended Next Action:** "
            "Confirm whether the difference represents an authorized "
            "partial payment, adjustment, tax, or other valid difference."
        )

    st.markdown("#### 📋 Original Recommendation")

    st.success(
        selected["Recommended Action"]
    )

else:

    st.success("🎉 No exceptions require investigation.")
    st.divider()

# ==============================
# TOP FINANCIAL RISKS
# ==============================

st.subheader("🔴 Top Financial Risks")

if len(exceptions_df) > 0:

    top_risks = exceptions_df.sort_values(
        by="Financial Impact",
        ascending=False
    ).head(5)

    st.markdown(
        "The following exceptions have the highest potential financial impact "
        "and should be investigated first."
    )

    for rank, (_, risk) in enumerate(top_risks.iterrows(), start=1):

        st.markdown(
            f"### {rank}. {risk['Invoice']} — {risk['Status']}"
        )

        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric(
                "Financial Impact",
                f"₹{risk['Financial Impact']:,.0f}"
            )

        with col2:
            st.metric(
                "Priority",
                risk["Priority"]
            )

        with col3:
            st.metric(
                "Vendor",
                risk["Vendor"]
            )

        st.caption(
            f"💡 {risk['Explanation']}"
        )

        st.divider()

else:

    st.success("🎉 No financial risks detected.")
    st.divider()

# ==============================
# VENDOR RISK ANALYSIS
# ==============================

st.subheader("📊 Vendor Risk Analysis")

if len(exceptions_df) > 0:

    vendor_risk = (
        exceptions_df
        .groupby("Vendor")
        .agg(
            Exceptions=("Invoice", "count"),
            Financial_Impact=("Financial Impact", "sum")
        )
        .sort_values(
            by="Financial_Impact",
            ascending=False
        )
        .reset_index()
    )

    st.markdown(
        "Vendors are ranked by total financial impact from reconciliation exceptions."
    )

    st.dataframe(
        vendor_risk,
        width="stretch",
        hide_index=True
    )

    st.markdown("### 🏆 Highest Risk Vendor")

    top_vendor = vendor_risk.iloc[0]

    st.warning(
        f"**{top_vendor['Vendor']}** has the highest exception impact: "
        f"₹{top_vendor['Financial_Impact']:,.0f} "
        f"across {top_vendor['Exceptions']} exception(s)."
    )

else:

    st.success("🎉 No vendor risks detected.")
    