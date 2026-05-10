from pathlib import Path
import duckdb

DATABASE_PATH = Path("database/retail_warehouse.duckdb")

def create_analytics_tables() -> None:
    """
    Create cleaned staging and analytics tables.
    """

    conn = duckdb.connect(str(DATABASE_PATH))

    # ====================
    # Create staging table
    # ====================

    conn.execute("""
            CREATE OR REPLACE TABLE stg_sale AS
            SELECT
                 invoice_no,
                 CAST(invoice_data as DATE) AS invoice_date,
                 customer_id,
                 country,
                 product_code,
                 product_name,
                 CAST(quanitity AS INTEGER) AS quantity,
                 CAST(unit_price as DOUBLE) as unit_price,
                CAST(quantity AS INTEGER)
                * CAST(unit_price AS DOUBLE) AS revenue

            FROM raw_sales

            WHERE quantity > 0
            AND unit_price > 0                

    """)

        # =========================
    # Monthly sales mart
    # =========================

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

    # =========================
    # Product sales mart
    # =========================

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