from src.load import load_raw_sales
from src.transform import create_analytics_tables


def main() -> None:

    print("Starting retail analytics warehouse pipeline...")

    load_raw_sales()

    create_analytics_tables()

    print("Pipeline completed successfully.")


if __name__ == "__main__":
    main()