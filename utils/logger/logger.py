import os
import logging
from datetime import datetime
import colorlog  # For colored logging


class Logger:
    def __init__(self, log_dir="logs", log_level=logging.DEBUG):
        self.log_dir = log_dir
        self.log_level = log_level
        self.logger = self.setup_logger()

    def setup_logger(self):
        if not os.path.exists(self.log_dir):
            os.makedirs(self.log_dir)

        today_date = datetime.now().strftime("%Y-%m-%d")
        log_file = f"{self.log_dir}/application_{today_date}.log"

        # Set up the logger
        logger = logging.getLogger(__name__)
        logger.setLevel(self.log_level)

        # Avoid adding duplicate handlers
        if not logger.handlers:
            # Create file handler for writing logs to file
            file_handler = logging.FileHandler(log_file)
            file_handler.setFormatter(
                logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
            )

            # Create console handler for colored logs
            console_handler = colorlog.StreamHandler()
            console_handler.setFormatter(
                colorlog.ColoredFormatter(
                    "%(log_color)s%(asctime)s - %(levelname)s - %(message)s",
                    log_colors={
                        "DEBUG": "cyan",
                        "INFO": "green",
                        "WARNING": "yellow",
                        "ERROR": "red",
                        "CRITICAL": "magenta",
                    },
                )
            )

            # Add handlers to the logger
            logger.addHandler(file_handler)
            logger.addHandler(console_handler)

        return logger

    def get_logger(self):
        return self.logger

    def log_info(self, message):
        self.logger.info(message)

    def log_error(self, message):
        self.logger.error(message)

    def log_debug(self, message):
        self.logger.debug(message)

    def log_warning(self, message):
        self.logger.warning(message)

    def log_critical(self, message):
        self.logger.critical(message)
