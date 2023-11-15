import logging
import sys

APP_LOGGER_NAME = "synthema"


class CustomFormatter(logging.Formatter):
    grey = "\x1b[38;21m"
    green = "\x1b[32;21m"
    yellow = "\x1b[33;21m"
    red = "\x1b[31;21m"
    bold_red = "\x1b[31;1m"
    reset = "\x1b[0m"
    format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"  # type: ignore

    FORMATS = {
        logging.DEBUG: grey + format + reset,  # type: ignore
        logging.INFO: green + format + reset,  # type: ignore
        logging.WARNING: yellow + format + reset,  # type: ignore
        logging.ERROR: red + format + reset,  # type: ignore
        logging.CRITICAL: bold_red + format + reset  # type: ignore
    }

    def format(self, record):
        log_fmt = self.FORMATS.get(record.levelno)
        formatter = logging.Formatter(log_fmt)
        return formatter.format(record)


def setup_applevel_logger(logger_name=APP_LOGGER_NAME, file_name=None):
    logger = logging.getLogger(logger_name)
    logger.setLevel(logging.DEBUG)
    formatter = CustomFormatter()

    sh = logging.StreamHandler(sys.stderr)
    sh.setFormatter(formatter)

    logger.handlers.clear()
    logger.addHandler(sh)

    if file_name:
        fh = logging.FileHandler(file_name)
        fh.setFormatter(formatter)
        logger.addHandler(fh)

    return logger


def get_logger(module_name):
    return logging.getLogger(APP_LOGGER_NAME).getChild(module_name)
