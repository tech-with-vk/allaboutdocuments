import logging
import os
from datetime import datetime
import structlog

class CustomLogger:
    """This is a custom logger class that accepts creates a log in the location from where it is being called."""

    def __init__(self, logs_directory="logs"):
        # building the log path
        self.where_are_the_logs = os.path.join(os.getcwd(), logs_directory)

        # creating logs folder
        os.makedirs(self.where_are_the_logs, exist_ok=True)

        # create log file name using system timestamp
        log_file_name = f"{datetime.now().strftime('%m_%d_%Y_%H_%M_%S')}.log"

        # create log file
        self.log_file_path = os.path.join(self.where_are_the_logs, log_file_name)

    def get_logger(self, name=__file__):
        # logger_name = os.path.basename(name)
        logger_name = os.path.splitext(os.path.basename(__file__))[0]

        # configure logging for log file
        file_log_handler = logging.FileHandler(self.log_file_path)
        file_log_handler.setLevel(logging.INFO)
        file_log_handler.setFormatter(logging.Formatter("%(message)s"))  # JSON

        # configure logging for console
        console_log_handler = logging.StreamHandler()
        console_log_handler.setLevel(logging.INFO)
        console_log_handler.setFormatter(logging.Formatter("%(message)s"))

        # set up logging configuration
        logging.basicConfig(
            level=logging.INFO,
            format="%(message)s",
            handlers=[file_log_handler, console_log_handler],
        )

        # Configure structlog for JSON structured logging
        structlog.configure(
            processors=[
                structlog.processors.TimeStamper(fmt="iso", utc=True, key="timestamp"),
                structlog.processors.add_log_level,
                structlog.processors.EventRenamer(to="event"),
                structlog.processors.JSONRenderer(),
            ],
            logger_factory=structlog.stdlib.LoggerFactory(),
            cache_logger_on_first_use=True,
        )

        return structlog.get_logger(logger_name)


if __name__ == "__main__":
    # create an instance of the logger
    logger = CustomLogger()

    # get the calling file's name
    logger = logger.get_logger(__file__)
    # logger.info("This log is from All About Documents Logger")

    # Testing logs with sample values
    logger.info("User uploaded a file", user_id="testUser", filename="sample.pdf")
    logger.error("Failed to process PDF", error="File not found", user_id="testUser")
