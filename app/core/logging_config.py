import logging
import sys


def setup_logging():
    # Define format
    log_format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"

    # Configure root logger
    logging.basicConfig(
        level=logging.INFO,
        format=log_format,
        handlers=[
            logging.StreamHandler(sys.stdout),
            # Optional: logging.FileHandler("app.log")
        ],
    )

    # Return a logger instance for this module (optional)
    return logging.getLogger("travel_planner")


logger = setup_logging()
