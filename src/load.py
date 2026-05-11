from pathlib import Path
import duckdb
import pandas as pd


DATABASE_PATH = Path("database/retail_warehouse.duckdb")
RAW_DATA_PATH = Path("data/raw/online-retail-dataset.csv")

from pathlib import Path

import duckdb
import pandas as pd

from src.logger import set_up_logger


logger = set_up_logger()

DATABASE_PATH = Path("database/retail_warehouse.duckdb")
RAW_DATA_PATH = Path("data/raw/online-retail-dataset.csv")


def load_raw_sales() -> None:

    logger.info("Starting raw sales load process.")

    if not RAW_DATA_PATH.exists():
        logger.error(f"Missing file: {RAW_DATA_PATH}")
        raise FileNotFoundError(f"Could not find file: {RAW_DATA_PATH}")

    df = pd.read_csv(RAW_DATA_PATH)

    logger.info(f"Loaded CSV with {len(df):,} rows.")

    DATABASE_PATH.parent.mkdir(parents=True, exist_ok=True)

    conn = duckdb.connect(str(DATABASE_PATH))

    conn.execute("DROP TABLE IF EXISTS raw_sales")

    conn.execute("""
        CREATE TABLE raw_sales AS
        SELECT *
        FROM df
    """)

    conn.close()

    logger.info("Raw sales table created successfully.")

if __name__ ==  "__main__":
    load_raw_sales()