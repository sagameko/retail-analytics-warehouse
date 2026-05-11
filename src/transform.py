from pathlib import Path

import duckdb

from src.logger import set_up_logger


logger = set_up_logger()

DATABASE_PATH = Path("database/retail_warehouse.duckdb")


def create_analytics_tables() -> None:

    conn = duckdb.connect(str(DATABASE_PATH))

    # =========================
    # Drop existing objects
    # Prevent dbt view/table conflicts
    # =========================

    objects_to_drop = [
        "stg_sales",
        "dim_customer",
        "dim_product",
        "dim_country",
        "dim_date",
        "fact_sales",
        "mart_monthly_sales",
        "mart_product_sales"
    ]

    for obj in objects_to_drop:

        try:
            conn.execute(f"DROP VIEW IF EXISTS {obj}")
        except Exception:
            pass

        try:
            conn.execute(f"DROP TABLE IF EXISTS {obj}")
        except Exception:
            pass

    # =========================
    # Create staging table
    # =========================

    conn.execute("""
        CREATE OR REPLACE TABLE stg_sales AS

        SELECT
            InvoiceNo AS invoice_no,

            CAST(
                STRPTIME(InvoiceDate, '%m/%d/%Y %H:%M')
                AS DATE
            ) AS invoice_date,

            COALESCE(
                CAST(CustomerID AS VARCHAR),
                'UNKNOWN'
            ) AS customer_id,

            Country AS country,

            StockCode AS product_code,
            Description AS product_name,

            CAST(Quantity AS INTEGER) AS quantity,
            CAST(UnitPrice AS DOUBLE) AS unit_price,

            CAST(Quantity AS INTEGER)
            * CAST(UnitPrice AS DOUBLE) AS revenue

        FROM raw_sales

        WHERE Quantity > 0
          AND UnitPrice > 0
    """)

    # =========================
    # Dimension: Customer
    # =========================

    conn.execute("""
        CREATE OR REPLACE TABLE dim_customer AS

        SELECT
            ROW_NUMBER() OVER (
                ORDER BY customer_id
            ) AS customer_key,

            customer_id

        FROM (
            SELECT DISTINCT customer_id
            FROM stg_sales
        )
    """)

    # =========================
    # Dimension: Product
    # =========================

    conn.execute("""
        CREATE OR REPLACE TABLE dim_product AS

        SELECT
            ROW_NUMBER() OVER (
                ORDER BY product_code, product_name
            ) AS product_key,

            product_code,
            product_name

        FROM (
            SELECT DISTINCT
                product_code,
                product_name
            FROM stg_sales
        )
    """)

    # =========================
    # Dimension: Country
    # =========================

    conn.execute("""
        CREATE OR REPLACE TABLE dim_country AS

        SELECT
            ROW_NUMBER() OVER (
                ORDER BY country
            ) AS country_key,

            country

        FROM (
            SELECT DISTINCT country
            FROM stg_sales
        )
    """)

    # =========================
    # Dimension: Date
    # =========================

    conn.execute("""
        CREATE OR REPLACE TABLE dim_date AS

        SELECT
            ROW_NUMBER() OVER (
                ORDER BY invoice_date
            ) AS date_key,

            invoice_date AS full_date,

            EXTRACT(year FROM invoice_date) AS year,
            EXTRACT(month FROM invoice_date) AS month,
            EXTRACT(day FROM invoice_date) AS day,

            DATE_TRUNC(
                'month',
                invoice_date
            ) AS month_start

        FROM (
            SELECT DISTINCT invoice_date
            FROM stg_sales
        )
    """)

    # =========================
    # Fact Table: Sales
    # =========================

    conn.execute("""
        CREATE OR REPLACE TABLE fact_sales AS

        SELECT
            s.invoice_no,

            d.date_key,
            c.customer_key,
            p.product_key,
            co.country_key,

            s.quantity,
            s.unit_price,
            s.revenue

        FROM stg_sales s

        LEFT JOIN dim_date d
            ON s.invoice_date = d.full_date

        LEFT JOIN dim_customer c
            ON s.customer_id = c.customer_id

        LEFT JOIN dim_product p
            ON s.product_code = p.product_code
           AND s.product_name = p.product_name

        LEFT JOIN dim_country co
            ON s.country = co.country
    """)

    # =========================
    # Monthly Sales Mart
    # =========================

    conn.execute("""
        CREATE OR REPLACE TABLE mart_monthly_sales AS

        SELECT
            d.month_start AS sales_month,

            SUM(f.revenue) AS total_revenue,
            SUM(f.quantity) AS total_quantity,

            COUNT(DISTINCT f.invoice_no) AS total_orders,

            COUNT(DISTINCT f.customer_key)
                AS unique_customers

        FROM fact_sales f

        LEFT JOIN dim_date d
            ON f.date_key = d.date_key

        GROUP BY 1

        ORDER BY 1
    """)

    # =========================
    # Product Sales Mart
    # =========================

    conn.execute("""
        CREATE OR REPLACE TABLE mart_product_sales AS

        SELECT
            p.product_code,
            p.product_name,

            SUM(f.quantity) AS total_quantity,
            SUM(f.revenue) AS total_revenue,

            COUNT(DISTINCT f.invoice_no)
                AS total_orders

        FROM fact_sales f

        LEFT JOIN dim_product p
            ON f.product_key = p.product_key

        GROUP BY 1, 2

        ORDER BY total_revenue DESC
    """)

    conn.close()

    logger.info(
        "Analytics tables created successfully."
    )


if __name__ == "__main__":
    create_analytics_tables()