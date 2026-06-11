import streamlit as st
import pandas as pd
import sqlite3
import plotly.express as px

# -----------------------------
# Page Configuration
# -----------------------------
st.set_page_config(
    page_title="Profitability & Margin Analytics Dashboard",
    page_icon="📊",
    layout="wide"
)

st.title("📊 Profitability & Margin Analytics Dashboard")
st.markdown("Analyze revenue, contribution margin, and customer performance.")

# -----------------------------
# Load Data
# -----------------------------
@st.cache_data
def load_data():
    conn = sqlite3.connect("sales.db")
    df = pd.read_sql("SELECT * FROM sales_orders", conn)
    conn.close()

    df["margin"] = df["sales"] - df["cost"]
    df["month"] = pd.to_datetime(df["order_date"]).dt.strftime("%Y-%m")

    return df

df = load_data()

# -----------------------------
# Sidebar Filters
# -----------------------------
st.sidebar.header("Filters")

regions = ["All"] + sorted(df["region"].unique().tolist())
categories = ["All"] + sorted(df["category"].unique().tolist())

selected_region = st.sidebar.selectbox("Region", regions)
selected_category = st.sidebar.selectbox("Category", categories)

filtered_df = df.copy()

if selected_region != "All":
    filtered_df = filtered_df[
        filtered_df["region"] == selected_region
    ]

if selected_category != "All":
    filtered_df = filtered_df[
        filtered_df["category"] == selected_category
    ]

# -----------------------------
# Empty Data Handling
# -----------------------------
if filtered_df.empty:
    st.warning("No data available for the selected filters.")
    st.stop()

# -----------------------------
# KPIs
# -----------------------------
total_revenue = filtered_df["sales"].sum()
total_margin = filtered_df["margin"].sum()
margin_pct = (total_margin / total_revenue) * 100
customer_count = filtered_df["customer_id"].nunique()

col1, col2, col3 = st.columns(3)

col1.metric(
    "💰 Total Revenue",
    f"${total_revenue:,.2f}"
)

col2.metric(
    "📈 Margin %",
    f"{margin_pct:.2f}%"
)

col3.metric(
    "👥 Customers",
    customer_count
)

st.divider()

# -----------------------------
# Revenue Trend
# -----------------------------
monthly = (
    filtered_df
    .groupby("month")["sales"]
    .sum()
    .reset_index()
)

fig1 = px.line(
    monthly,
    x="month",
    y="sales",
    title="Monthly Revenue Trend",
    markers=True
)

st.plotly_chart(fig1, use_container_width=True)

# -----------------------------
# Top Customers
# -----------------------------
top_customers = (
    filtered_df
    .groupby("customer_id")["sales"]
    .sum()
    .sort_values(ascending=False)
    .head(10)
    .reset_index()
)

fig2 = px.bar(
    top_customers,
    x="customer_id",
    y="sales",
    title="Top 10 Customers by Revenue"
)

st.plotly_chart(fig2, use_container_width=True)

# -----------------------------
# Margin by Category
# -----------------------------
margin_category = (
    filtered_df
    .groupby("category")["margin"]
    .sum()
    .reset_index()
)

fig3 = px.bar(
    margin_category,
    x="category",
    y="margin",
    title="Contribution Margin by Category"
)

st.plotly_chart(fig3, use_container_width=True)

# -----------------------------
# Insight Callout
# -----------------------------
customer_revenue = (
    filtered_df
    .groupby("customer_id")["sales"]
    .sum()
    .sort_values(ascending=False)
)

top5_share = (
    customer_revenue.head(5).sum()
    / customer_revenue.sum()
) * 100

st.info(
    f"""
### 📌 Insight

The top 5 customers contribute **{top5_share:.2f}%**
of total revenue. This indicates that revenue is
concentrated among a small group of customers,
which may create dependency risk.
"""
)