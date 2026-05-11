from src.load import load_raw_sales
from src.transform import create_analytics_tables
from src.logger import set_up_logger


logger = set_up_logger()


def main() -> None:

    logger.info("Starting retail analytics warehouse pipeline.")

    load_raw_sales()

    create_analytics_tables()

    logger.info("Pipeline completed successfully.")


if __name__ == "__main__":
    main()