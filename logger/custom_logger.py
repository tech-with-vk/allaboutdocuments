import logging
import os
from datetime import datetime
import structlog


class CustomLogger:
    """A singleton custom logger that prevents duplicate handlers and repeated log file creation."""

    _logger_initialized = False
    _log_file_path = None

    def __init__(self, logs_directory="logs"):
        if not CustomLogger._logger_initialized:
            # Set up log folder
            self.logs_directory = os.path.join(os.getcwd(), logs_directory)
            os.makedirs(self.logs_directory, exist_ok=True)

            # Create only one log file path for the entire app run
            CustomLogger._log_file_path = os.path.join(
                self.logs_directory,
                f"{datetime.now().strftime('%m_%d_%Y_%H_%M_%S')}.log",
            )

            # Setup base logging handlers
            self._configure_logging()

            CustomLogger._logger_initialized = True

    def _configure_logging(self):
        # File Handler
        file_handler = logging.FileHandler(CustomLogger._log_file_path)
        file_handler.setLevel(logging.INFO)
        file_handler.setFormatter(logging.Formatter("%(message)s"))

        # Console Handler
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)
        console_handler.setFormatter(logging.Formatter("%(message)s"))

        # Attach handlers only once
        root_logger = logging.getLogger()
        if not root_logger.handlers:
            logging.basicConfig(
                level=logging.INFO,
                handlers=[file_handler, console_handler],
            )

        # Structlog configuration
        structlog.configure(
            processors=[
                structlog.processors.EventRenamer(to="event"),
                structlog.processors.TimeStamper(fmt="iso", utc=True, key="timestamp"),
                structlog.processors.add_log_level,
                structlog.processors.JSONRenderer(),
            ],
            logger_factory=structlog.stdlib.LoggerFactory(),
            cache_logger_on_first_use=True,
        )

    def get_logger(self, name=__file__):
        logger_name = os.path.splitext(os.path.basename(name))[0]
        return structlog.get_logger(logger_name)
