import logging
import sys


def init_logger() -> None:
    """Starts basic logger"""
    logging.basicConfig(
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        stream=sys.stdout,
        level=logging.INFO
    )
    return