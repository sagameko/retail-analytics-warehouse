import logging

def set_up_logger() -> logging.Logger:

    logging.basicConfig(
        level= logging.INFO,
        format= "%(asctime)s | %(levelname)s | %(message)s",
        force= True
    )

    return logging.getLogger(__name__)