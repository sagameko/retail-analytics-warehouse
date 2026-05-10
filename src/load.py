from pathlib import Path
import duckdb
import pandas as pd


DATABASE_PATH = Path("database/retail_warehouse.duckdb")
RAW_DATA_PATH = Path("data/raw/online-retail-dataset.csv")

def load_raw_sales() -> None:
    """
    Load raw dataset into duck database
    """

    # check files existant
    if not RAW_DATA_PATH.exists():
        raise FileNotFoundError(f"Could not find file: {RAW_DATA_PATH}")
    
    # Read csv  files
    df = pd.read_csv(RAW_DATA_PATH)

    # Create database folder if not existed
    DATABASE_PATH.parent.mkdir(parents=True, exist_ok=True)

    # Connect to database
    conn = duckdb.connect(str(DATABASE_PATH))

    # Remove old table if there is any
    conn.execute("DROP TABLE IF EXISTS raw_sales")

    # Create raw_sawl table 
    conn.execute("CREATE TABLE raw_sales AS SELECT * FROM df")

    # Close down the conenction
    conn.close()

    print("Loaded sale data successfully!!!")

if __name__ ==  "__main__":
    load_raw_sales()