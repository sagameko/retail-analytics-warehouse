# Architecture

```text
Raw CSV
   |
   v
src/load.py
   |
   v
raw_sales table in DuckDB
   |
   v
src/transform.py
   |
   v
stg_sales table
   |
   v
mart_monthly_sales and mart_product_sales
   |
   v
Streamlit dashboard