from pathlib import Path

import duckdb
import pandas as pd
import streamlit as st


DATABASE_PATH = Path("database/retail_warehouse.duckdb")


@st.cache_data
def load_sales_data() -> pd.DataFrame:
    conn = duckdb.connect(str(DATABASE_PATH))

    query = """
        SELECT
            f.invoice_no,
            d.full_date AS invoice_date,
            d.year,
            d.month,
            d.month_start,
            c.customer_id,
            p.product_code,
            p.product_name,
            co.country,
            f.quantity,
            f.unit_price,
            f.revenue
        FROM fact_sales f
        LEFT JOIN dim_date d
            ON f.date_key = d.date_key
        LEFT JOIN dim_customer c
            ON f.customer_key = c.customer_key
        LEFT JOIN dim_product p
            ON f.product_key = p.product_key
        LEFT JOIN dim_country co
            ON f.country_key = co.country_key
    """

    df = conn.execute(query).df()
    conn.close()

    df["invoice_date"] = pd.to_datetime(df["invoice_date"])
    df["month_start"] = pd.to_datetime(df["month_start"])

    return df


st.set_page_config(
    page_title="Retail Analytics Warehouse",
    layout="wide"
)

st.title("Retail Analytics Warehouse")
st.write(
    "A star-schema analytics dashboard built with Python, DuckDB, SQL, and Streamlit."
)

if not DATABASE_PATH.exists():
    st.error("Database not found. Please run `python main.py` first.")
    st.stop()

df = load_sales_data()

# =========================
# Sidebar filters
# =========================

st.sidebar.header("Filters")

min_date = df["invoice_date"].min().date()
max_date = df["invoice_date"].max().date()

date_range = st.sidebar.date_input(
    "Date range",
    value=(min_date, max_date),
    min_value=min_date,
    max_value=max_date
)

countries = sorted(df["country"].dropna().unique())
selected_countries = st.sidebar.multiselect(
    "Country",
    options=countries,
    default=countries
)

products = sorted(df["product_name"].dropna().unique())
selected_products = st.sidebar.multiselect(
    "Product",
    options=products,
    default=products[:20] if len(products) > 20 else products
)

filtered_df = df.copy()

if len(date_range) == 2:
    start_date, end_date = date_range
    filtered_df = filtered_df[
        (filtered_df["invoice_date"].dt.date >= start_date)
        & (filtered_df["invoice_date"].dt.date <= end_date)
    ]

filtered_df = filtered_df[
    filtered_df["country"].isin(selected_countries)
    & filtered_df["product_name"].isin(selected_products)
]

if filtered_df.empty:
    st.warning("No data available for the selected filters.")
    st.stop()

# =========================
# KPI cards
# =========================

total_revenue = filtered_df["revenue"].sum()
total_orders = filtered_df["invoice_no"].nunique()
unique_customers = filtered_df["customer_id"].nunique()
total_quantity = filtered_df["quantity"].sum()
avg_order_value = total_revenue / total_orders if total_orders else 0

col1, col2, col3, col4, col5 = st.columns(5)

col1.metric("Total Revenue", f"${total_revenue:,.2f}")
col2.metric("Total Orders", f"{total_orders:,}")
col3.metric("Unique Customers", f"{unique_customers:,}")
col4.metric("Units Sold", f"{total_quantity:,}")
col5.metric("Avg Order Value", f"${avg_order_value:,.2f}")

# =========================
# Monthly revenue
# =========================

st.subheader("Monthly Revenue")

monthly_revenue = (
    filtered_df
    .groupby("month_start", as_index=False)
    .agg(total_revenue=("revenue", "sum"))
    .sort_values("month_start")
)

st.line_chart(
    monthly_revenue,
    x="month_start",
    y="total_revenue"
)

# =========================
# Product and country analysis
# =========================

left_col, right_col = st.columns(2)

with left_col:
    st.subheader("Top Products by Revenue")

    top_products = (
        filtered_df
        .groupby("product_name", as_index=False)
        .agg(total_revenue=("revenue", "sum"))
        .sort_values("total_revenue", ascending=False)
        .head(10)
    )

    st.bar_chart(
        top_products,
        x="product_name",
        y="total_revenue"
    )

with right_col:
    st.subheader("Revenue by Country")

    country_revenue = (
        filtered_df
        .groupby("country", as_index=False)
        .agg(total_revenue=("revenue", "sum"))
        .sort_values("total_revenue", ascending=False)
        .head(10)
    )

    st.bar_chart(
        country_revenue,
        x="country",
        y="total_revenue"
    )

# =========================
# Customer analysis
# =========================

st.subheader("Top Customers")

top_customers = (
    filtered_df
    .groupby("customer_id", as_index=False)
    .agg(
        total_revenue=("revenue", "sum"),
        total_orders=("invoice_no", "nunique"),
        total_quantity=("quantity", "sum")
    )
    .sort_values("total_revenue", ascending=False)
    .head(10)
)

st.dataframe(top_customers, use_container_width=True)

# =========================
# Transaction details
# =========================

st.subheader("Transaction Details")

display_columns = [
    "invoice_no",
    "invoice_date",
    "customer_id",
    "country",
    "product_name",
    "quantity",
    "unit_price",
    "revenue"
]

st.dataframe(
    filtered_df[display_columns].sort_values("invoice_date", ascending=False),
    use_container_width=True
)