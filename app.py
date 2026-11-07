
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px


"""
E-Commerce Customer Retention & Revenue Intelligence Dashboard

Libraries:
- Streamlit
- Pandas
- NumPy
- Plotly

This application uses an illustrative, explainable
heuristic to identify customer retention risk.

It is a business analytics prototype, not a trained
machine-learning churn prediction model.
"""

from pathlib import Path

import numpy as np
import pandas as pd
import plotly.express as px
import streamlit as st


# ==========================================================
# 1. PAGE CONFIGURATION
# ==========================================================

st.set_page_config(
    page_title="E-Commerce Retention Intelligence",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)

APP_TITLE = "E-Commerce Customer Retention & Revenue Intelligence"

DATA_PATH = (
    Path(__file__).resolve().parent
    / "data"
    / "customer_data.csv"
)

HIGH_RISK_THRESHOLD = 3


# ==========================================================
# 2. DATA LOADING
# ==========================================================

@st.cache_data
def load_data(file_path: str) -> pd.DataFrame:
    """
    Load and validate the customer dataset.
    """

    data = pd.read_csv(file_path)

    required_columns = [
        "CustomerID",
        "Tenure",
        "MonthlySpend",
        "TotalSpend",
        "NumOrders",
        "AvgOrderValue",
        "DaysSinceLastOrder",
        "SupportTickets",
        "ContractType",
        "TechSupport",
        "Churn",
    ]

    missing_columns = [
        column
        for column in required_columns
        if column not in data.columns
    ]

    if missing_columns:
        raise ValueError(
            f"Missing required columns: {missing_columns}"
        )

    # Remove duplicate customer records
    data = data.drop_duplicates(
        subset=["CustomerID"]
    )

    # Convert numeric fields
    numeric_columns = [
        "Tenure",
        "MonthlySpend",
        "TotalSpend",
        "NumOrders",
        "AvgOrderValue",
        "DaysSinceLastOrder",
        "SupportTickets",
        "Churn",
    ]

    for column in numeric_columns:
        data[column] = pd.to_numeric(
            data[column],
            errors="coerce"
        )

    # Remove records with missing essential values
    data = data.dropna(
        subset=[
            "CustomerID",
            "Tenure",
            "MonthlySpend",
            "DaysSinceLastOrder",
            "Churn",
        ]
    )

    # Ensure churn is binary
    data = data[
        data["Churn"].isin([0, 1])
    ].copy()

    # Clean categorical values
    data["ContractType"] = (
        data["ContractType"]
        .astype(str)
        .str.strip()
    )

    data["TechSupport"] = (
        data["TechSupport"]
        .astype(str)
        .str.strip()
    )

    return data


# ==========================================================
# 3. CUSTOMER RISK SCORING
# ==========================================================

def calculate_risk_score(data: pd.DataFrame) -> pd.DataFrame:
    """
    Calculate an illustrative risk score for active customers.

    Risk indicators:
    - Month-to-month contract: +2
    - No Tech Support: +1
    - Tenure <= 12 months: +1
    - Last order more than 60 days ago: +2
    - Support tickets >= 4: +1

    Score >= 3 = High Risk
    """

    result = data.copy()

    # Create risk score using NumPy
    result["RiskScore"] = (
        2 * (
            result["ContractType"]
            == "Month-to-month"
        ).astype(int)

        + 1 * (
            result["TechSupport"]
            == "No"
        ).astype(int)

        + 1 * (
            result["Tenure"]
            <= 12
        ).astype(int)

        + 2 * (
            result["DaysSinceLastOrder"]
            > 60
        ).astype(int)

        + 1 * (
            result["SupportTickets"]
            >= 4
        ).astype(int)
    )

    # Classify risk
    result["RiskLevel"] = np.where(
        result["RiskScore"] >= HIGH_RISK_THRESHOLD,
        "High Risk",
        "Low Risk"
    )

    # Potential annualised revenue at risk
    result["AnnualRevenueAtRisk"] = np.where(
        result["RiskLevel"] == "High Risk",
        result["MonthlySpend"] * 12,
        0
    )

    return result


# ==========================================================
# 4. BUSINESS RECOMMENDATIONS
# ==========================================================

def generate_recommendations(
    risk_level: str,
    contract_type: str,
    tech_support: str,
    days_since_last_order: int,
    support_tickets: int,
) -> list[str]:

    recommendations = []

    if risk_level == "High Risk":

        recommendations.append(
            "Prioritise customer outreach within "
            "the next 1-2 business days."
        )

        if days_since_last_order > 60:

            recommendations.append(
                "Launch a personalised re-engagement "
                "campaign with a relevant product offer."
            )

        if contract_type == "Month-to-month":

            recommendations.append(
                "Explore a suitable annual contract "
                "or loyalty incentive."
            )

        if tech_support == "No":

            recommendations.append(
                "Introduce the benefits of Tech Support "
                "and assess customer service needs."
            )

        if support_tickets >= 4:

            recommendations.append(
                "Review unresolved support issues and "
                "assign an appropriate service owner."
            )

        recommendations.append(
            "Track the outcome of the retention action "
            "and schedule a follow-up."
        )

    else:

        recommendations.append(
            "Maintain the current service experience "
            "and monitor customer engagement."
        )

        recommendations.append(
            "Reinforce the value of the subscription "
            "through relevant customer communication."
        )

        recommendations.append(
            "Continue periodic customer satisfaction "
            "and retention reviews."
        )

    return recommendations


# ==========================================================
# 5. LOAD DATA
# ==========================================================

st.title(APP_TITLE)

st.markdown(
    """
    **Manager's view:** Understand customer retention,
    identify high-risk customers, and evaluate revenue
    exposure using interactive business analytics.
    """
)

st.divider()

if not DATA_PATH.exists():

    st.error(
        "Dataset not found. Please place customer_data.csv "
        "inside the project's data folder."
    )

    st.code(
        "Ecommerce-Retention-Analytics/"
        "\n├── app.py"
        "\n├── requirements.txt"
        "\n├── README.md"
        "\n└── data/"
        "\n    └── customer_data.csv"
    )

    st.stop()


try:

    df = load_data(str(DATA_PATH))

except (ValueError, OSError, pd.errors.ParserError) as error:

    st.error(f"Unable to load the dataset: {error}")

    st.stop()


# ==========================================================
# 6. CUSTOMER RISK ASSESSMENT
# ==========================================================

# Churned customers are excluded from active retention risk.
active_customers = df[
    df["Churn"] == 0
].copy()

active_customers = calculate_risk_score(
    active_customers
)


# ==========================================================
# 7. SIDEBAR FILTERS
# ==========================================================

st.sidebar.header("Dashboard Filters")

st.sidebar.caption(
    "Use these filters to analyse customer segments."
)

contract_options = sorted(
    df["ContractType"].dropna().unique().tolist()
)

selected_contracts = st.sidebar.multiselect(
    "Contract Type",
    options=contract_options,
    default=contract_options,
)

support_options = sorted(
    df["TechSupport"].dropna().unique().tolist()
)

selected_support = st.sidebar.multiselect(
    "Tech Support",
    options=support_options,
    default=support_options,
)

tenure_range = st.sidebar.slider(
    "Customer Tenure (months)",
    min_value=int(df["Tenure"].min()),
    max_value=int(df["Tenure"].max()),
    value=(
        int(df["Tenure"].min()),
        int(df["Tenure"].max()),
    ),
)

risk_filter = st.sidebar.selectbox(
    "Retention Risk",
    options=[
        "All",
        "High Risk",
        "Low Risk",
    ],
)

st.sidebar.divider()

st.sidebar.caption(
    "Risk scoring is based on predefined business rules."
)


# ==========================================================
# 8. APPLY FILTERS
# ==========================================================

filtered_df = df[
    df["ContractType"].isin(selected_contracts)
    & df["TechSupport"].isin(selected_support)
    & df["Tenure"].between(
        tenure_range[0],
        tenure_range[1],
    )
].copy()

filtered_active = active_customers[
    active_customers["ContractType"].isin(
        selected_contracts
    )
    & active_customers["TechSupport"].isin(
        selected_support
    )
    & active_customers["Tenure"].between(
        tenure_range[0],
        tenure_range[1],
    )
].copy()

if risk_filter != "All":

    filtered_active = filtered_active[
        filtered_active["RiskLevel"]
        == risk_filter
    ]


# ==========================================================
# 9. EXECUTIVE KPI CARDS
# ==========================================================

total_customers = len(filtered_df)

churned_customers = int(
    filtered_df["Churn"].sum()
)

churn_rate = (
    churned_customers / total_customers * 100
    if total_customers > 0
    else 0
)

total_revenue = filtered_df[
    "MonthlySpend"
].sum() * 12

high_risk_customers = int(
    (
        filtered_active["RiskLevel"]
        == "High Risk"
    ).sum()
)

revenue_at_risk = filtered_active[
    "AnnualRevenueAtRisk"
].sum()


st.subheader("Executive Summary")

kpi1, kpi2, kpi3, kpi4, kpi5 = st.columns(5)

kpi1.metric(
    "Total Customers",
    f"{total_customers:,}",
)

kpi2.metric(
    "Churned Customers",
    f"{churned_customers:,}",
)

kpi3.metric(
    "Churn Rate",
    f"{churn_rate:.2f}%",
)

kpi4.metric(
    "High-Risk Customers",
    f"{high_risk_customers:,}",
)

kpi5.metric(
    "Annualised Revenue at Risk",
    f"${revenue_at_risk:,.0f}",
)

st.caption(
    "Annualised revenue at risk is an illustrative estimate "
    "based on monthly spend multiplied by 12 for high-risk "
    "active customers. It is not a forecast of actual losses."
)


# ==========================================================
# 10. REVENUE AND CHURN ANALYSIS
# ==========================================================

st.divider()

st.subheader("Revenue & Churn Analytics")

chart1, chart2 = st.columns(2)

# ----------------------------------------------------------
# Churn by Contract Type
# ----------------------------------------------------------

with chart1:

    contract_analysis = (
        filtered_df.groupby("ContractType")
        .agg(
            TotalCustomers=("CustomerID", "count"),
            ChurnedCustomers=("Churn", "sum"),
        )
        .reset_index()
    )

    contract_analysis["ChurnRate"] = (
        contract_analysis["ChurnedCustomers"]
        / contract_analysis["TotalCustomers"]
        * 100
    )

    fig_contract = px.bar(
        contract_analysis,
        x="ContractType",
        y="ChurnRate",
        color="ContractType",
        text="ChurnRate",
        title="Churn Rate by Contract Type",
        labels={
            "ContractType": "Contract Type",
            "ChurnRate": "Churn Rate (%)",
        },
    )

    fig_contract.update_traces(
        texttemplate="%{text:.1f}%",
        textposition="outside",
    )

    fig_contract.update_layout(
        showlegend=False,
        yaxis_title="Churn Rate (%)",
    )

    st.plotly_chart(
        fig_contract,
        use_container_width=True,
    )


# ----------------------------------------------------------
# Revenue by Contract Type
# ----------------------------------------------------------

with chart2:

    revenue_analysis = (
        filtered_df.groupby("ContractType")
        .agg(
            AnnualisedRevenue=(
                "MonthlySpend",
                lambda x: x.sum() * 12
            )
        )
        .reset_index()
    )

    fig_revenue = px.bar(
        revenue_analysis,
        x="ContractType",
        y="AnnualisedRevenue",
        color="ContractType",
        title="Annualised Revenue by Contract Type",
        labels={
            "ContractType": "Contract Type",
            "AnnualisedRevenue": "Annualised Revenue ($)",
        },
    )

    fig_revenue.update_layout(
        showlegend=False,
        yaxis_title="Annualised Revenue ($)",
    )

    st.plotly_chart(
        fig_revenue,
        use_container_width=True,
    )


# ==========================================================
# 11. CUSTOMER SEGMENTATION
# ==========================================================

st.divider()

st.subheader("Customer Segmentation")

segment_data = filtered_df.copy()

segment_data["CustomerSegment"] = np.select(
    [
        segment_data["Tenure"] <= 12,
        segment_data["Tenure"] <= 36,
    ],
    [
        "New Customers",
        "Growing Customers",
    ],
    default="Loyal Customers",
)

segment_summary = (
    segment_data.groupby("CustomerSegment")
    .agg(
        CustomerCount=("CustomerID", "count"),
        AverageMonthlySpend=("MonthlySpend", "mean"),
        TotalMonthlyRevenue=("MonthlySpend", "sum"),
        ChurnRate=("Churn", "mean"),
    )
    .reset_index()
)

segment_summary["ChurnRate"] *= 100

segment_summary["AnnualisedRevenue"] = (
    segment_summary["TotalMonthlyRevenue"] * 12
)

segment_chart = px.bar(
    segment_summary,
    x="CustomerSegment",
    y="CustomerCount",
    color="CustomerSegment",
    title="Customer Distribution by Segment",
    labels={
        "CustomerSegment": "Customer Segment",
        "CustomerCount": "Number of Customers",
    },
)

segment_chart.update_layout(
    showlegend=False,
)

st.plotly_chart(
    segment_chart,
    use_container_width=True,
)

st.dataframe(
    segment_summary,
    use_container_width=True,
    hide_index=True,
)


# ==========================================================
# 12. HIGH-RISK CUSTOMER ANALYSIS
# ==========================================================

st.divider()

st.subheader("High-Risk Customer Retention List")

high_risk_df = pd.DataFrame()

if filtered_active.empty:

    st.info(
        "No active customers match the selected filters."
    )

else:

    high_risk_df = filtered_active[
        filtered_active["RiskLevel"] == "High Risk"
    ].copy()

    if high_risk_df.empty:

        st.success(
            "No high-risk customers were identified "
            "within the selected active customer segment."
        )

    else:

        high_risk_df = high_risk_df.sort_values(
            by=[
                "RiskScore",
                "DaysSinceLastOrder",
                "MonthlySpend",
            ],
            ascending=[
                False,
                False,
                False,
            ],
        )

        st.write(
            f"Number of high-risk customers: "
            f"{len(high_risk_df):,}"
        )

        display_columns = [
            "CustomerID",
            "Tenure",
            "MonthlySpend",
            "DaysSinceLastOrder",
            "SupportTickets",
            "ContractType",
            "TechSupport",
            "RiskScore",
            "RiskLevel",
            "AnnualRevenueAtRisk",
        ]

        st.dataframe(
            high_risk_df[display_columns],
            use_container_width=True,
            hide_index=True,
        )

        csv_data = high_risk_df[
            display_columns
        ].to_csv(index=False).encode("utf-8")

        st.download_button(
            label="Download High-Risk Customers CSV",
            data=csv_data,
            file_name="high_risk_customers.csv",
            mime="text/csv",
        )


# ==========================================================
# 13. CUSTOMER RETENTION RECOMMENDATIONS
# ==========================================================

st.divider()

st.subheader("Manager's Recommended Actions")

if not high_risk_df.empty:

    example_customer = high_risk_df.iloc[0]

    recommendations = generate_recommendations(
        risk_level=example_customer["RiskLevel"],
        contract_type=example_customer["ContractType"],
        tech_support=example_customer["TechSupport"],
        days_since_last_order=int(
            example_customer["DaysSinceLastOrder"]
        ),
        support_tickets=int(
            example_customer["SupportTickets"]
        ),
    )

    st.write(
        "Recommended actions for the highest-priority "
        "customer in the filtered segment:"
    )

    for recommendation in recommendations:

        st.markdown(
            f"- {recommendation}"
        )

else:

    st.success(
        "No high-risk customers are currently "
        "identified in the filtered segment."
    )


# ==========================================================
# 14. DATASET PREVIEW
# ==========================================================

st.divider()

with st.expander("View Filtered Dataset"):

    st.dataframe(
        filtered_df,
        use_container_width=True,
        hide_index=True,
    )

    csv_data = filtered_df.to_csv(
        index=False
    ).encode("utf-8")

    st.download_button(
        label="Download Filtered Customer Dataset",
        data=csv_data,
        file_name="filtered_customer_data.csv",
        mime="text/csv",
    )


# ==========================================================
# 15. FOOTER
# ==========================================================

st.divider()

st.caption(
    "E-Commerce Customer Retention & Revenue Intelligence | "
    "Business Analytics Prototype | "
    "Risk scores are illustrative heuristic estimates."
)
