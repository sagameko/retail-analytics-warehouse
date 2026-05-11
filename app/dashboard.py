from pathlib import Path

import duckdb
import pandas as pd
import streamlit as st


DATABASE_PATH = Path("database/retail_warehouse.duckdb")


@st.cache_data
def load_table(table_name: str) -> pd.DataFrame:
    conn = duckdb.connect(str(DATABASE_PATH))
    df = conn.execute(f"SELECT * FROM {table_name}").df()
    conn.close()
    return df


st.set_page_config(
    page_title="Retail Analytics Warehouse",
    layout="wide"
)

st.title("Retail Analytics Warehouse")
st.write("A portfolio project for data warehousing, SQL analytics, and dashboarding.")

if not DATABASE_PATH.exists():
    st.error("Database not found. Please run `python main.py` first.")
    st.stop()

monthly_sales = load_table("mart_monthly_sales")
product_sales = load_table("mart_product_sales")

total_revenue = monthly_sales["total_revenue"].sum()
total_orders = monthly_sales["total_orders"].sum()
unique_customers = monthly_sales["unique_customers"].sum()

col1, col2, col3 = st.columns(3)

col1.metric("Total Revenue", f"${total_revenue:,.2f}")
col2.metric("Total Orders", f"{total_orders:,}")
col3.metric("Unique Customers", f"{unique_customers:,}")

st.subheader("Monthly Revenue")
st.line_chart(monthly_sales, x="sales_month", y="total_revenue")

st.subheader("Top Products by Revenue")
top_products = product_sales.head(10)
st.bar_chart(top_products, x="product_name", y="total_revenue")

st.subheader("Monthly Sales Table")
st.dataframe(monthly_sales, use_container_width=True)

st.subheader("Product Sales Table")
st.dataframe(product_sales, use_container_width=True)