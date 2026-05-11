import duckdb


DATABASE_PATH = "database/retail_warehouse.duckdb"


def run_data_quality_checks() -> None:

    conn = duckdb.connect(DATABASE_PATH)

    print("=" * 50)
    print("RUNNING DATA QUALITY CHECKS")
    print("=" * 50)

    # =========================
    # Check required tables
    # =========================

    required_tables = [
        "raw_sales",
        "stg_sales",
        "fact_sales",
        "dim_customer",
        "dim_product",
        "dim_country",
        "dim_date"
    ]

    existing_tables = [
        row[0]
        for row in conn.execute("SHOW TABLES").fetchall()
    ]

    for table in required_tables:
        assert table in existing_tables, f"Missing table: {table}"

    print("Required tables check passed.")

    # =========================
    # Negative quantity check
    # =========================

    negative_quantity = conn.execute("""
        SELECT COUNT(*)
        FROM stg_sales
        WHERE quantity < 0
    """).fetchone()[0]

    assert negative_quantity == 0, "Negative quantity values found."

    print("Negative quantity check passed.")

    # =========================
    # Negative price check
    # =========================

    negative_price = conn.execute("""
        SELECT COUNT(*)
        FROM stg_sales
        WHERE unit_price < 0
    """).fetchone()[0]

    assert negative_price == 0, "Negative prices found."

    print("Negative price check passed.")

    # =========================
    # Null revenue check
    # =========================

    null_revenue = conn.execute("""
        SELECT COUNT(*)
        FROM fact_sales
        WHERE revenue IS NULL
    """).fetchone()[0]

    assert null_revenue == 0, "Null revenue values found."

    print("Null revenue check passed.")

    # =========================
    # Fact row count check
    # =========================

    stg_count = conn.execute("""
        SELECT COUNT(*)
        FROM stg_sales
    """).fetchone()[0]

    fact_count = conn.execute("""
        SELECT COUNT(*)
        FROM fact_sales
    """).fetchone()[0]

    assert stg_count == fact_count, (
        "Fact table row count mismatch."
    )

    print("Fact table row count check passed.")

    # =========================
    # Null dimension key checks
    # =========================

    null_customer_keys = conn.execute("""
        SELECT COUNT(*)
        FROM fact_sales
        WHERE customer_key IS NULL
    """).fetchone()[0]

    assert null_customer_keys == 0, (
        "Null customer keys found."
    )

    print("Customer key check passed.")

    null_product_keys = conn.execute("""
        SELECT COUNT(*)
        FROM fact_sales
        WHERE product_key IS NULL
    """).fetchone()[0]

    assert null_product_keys == 0, (
        "Null product keys found."
    )

    print("Product key check passed.")

    null_date_keys = conn.execute("""
        SELECT COUNT(*)
        FROM fact_sales
        WHERE date_key IS NULL
    """).fetchone()[0]

    assert null_date_keys == 0, (
        "Null date keys found."
    )

    print("Date key check passed.")

    conn.close()

    print("=" * 50)
    print("ALL DATA QUALITY CHECKS PASSED")
    print("=" * 50)


if __name__ == "__main__":
    run_data_quality_checks()