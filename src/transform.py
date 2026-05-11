from pathlib import Path
import duckdb


DATABASE_PATH = Path("database/retail_warehouse.duckdb")


def create_analytics_tables() -> None:
    conn = duckdb.connect(str(DATABASE_PATH))

    conn.execute("""
        CREATE OR REPLACE TABLE stg_sales AS
        SELECT
            InvoiceNo AS invoice_no,
            CAST(STRPTIME(InvoiceDate, '%m/%d/%Y %H:%M') AS DATE) AS invoice_date,

            COALESCE(CAST(CustomerID AS VARCHAR), 'UNKNOWN') AS customer_id,
            Country AS country,

            StockCode AS product_code,
            Description AS product_name,

            CAST(Quantity AS INTEGER) AS quantity,
            CAST(UnitPrice AS DOUBLE) AS unit_price,

            CAST(Quantity AS INTEGER) * CAST(UnitPrice AS DOUBLE) AS revenue

        FROM raw_sales

        WHERE Quantity > 0
        AND UnitPrice > 0
    """)

    conn.execute("""
        CREATE OR REPLACE TABLE mart_monthly_sales AS
        SELECT
            DATE_TRUNC('month', invoice_date) AS sales_month,
            SUM(revenue) AS total_revenue,
            SUM(quantity) AS total_quantity,
            COUNT(DISTINCT invoice_no) AS total_orders,
            COUNT(DISTINCT customer_id) AS unique_customers
        FROM stg_sales
        GROUP BY 1
        ORDER BY 1
    """)

    conn.execute("""
        CREATE OR REPLACE TABLE mart_product_sales AS
        SELECT
            product_code,
            product_name,
            SUM(quantity) AS total_quantity,
            SUM(revenue) AS total_revenue,
            COUNT(DISTINCT invoice_no) AS total_orders
        FROM stg_sales
        GROUP BY 1, 2
        ORDER BY total_revenue DESC
    """)

    conn.close()
    print("Analytics tables created successfully.")


if __name__ == "__main__":
    create_analytics_tables()