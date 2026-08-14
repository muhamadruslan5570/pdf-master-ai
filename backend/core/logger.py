# ==========================================================
# PDF MASTER AI
# Logger
# ==========================================================

# ----------------------------------------------------------
# IMPORT
# ----------------------------------------------------------

import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path

# ----------------------------------------------------------
# LOG DIRECTORY
# ----------------------------------------------------------

LOG_DIR = Path("logs")

LOG_DIR.mkdir(
    exist_ok=True
)

LOG_FILE = LOG_DIR / "pdf_master_ai.log"

# ----------------------------------------------------------
# LOGGER
# ----------------------------------------------------------

logger = logging.getLogger(
    "PDF_MASTER_AI"
)

logger.setLevel(
    logging.INFO
)

# ----------------------------------------------------------
# FORMAT
# ----------------------------------------------------------

formatter = logging.Formatter(

    "%(asctime)s | %(levelname)s | %(name)s | %(message)s",

    "%Y-%m-%d %H:%M:%S"

)

# ----------------------------------------------------------
# FILE HANDLER
# ----------------------------------------------------------

file_handler = RotatingFileHandler(

    LOG_FILE,

    maxBytes=5 * 1024 * 1024,

    backupCount=5,

    encoding="utf-8"

)

file_handler.setFormatter(
    formatter
)

# ----------------------------------------------------------
# CONSOLE HANDLER
# ----------------------------------------------------------

console_handler = logging.StreamHandler()

console_handler.setFormatter(
    formatter
)

# ----------------------------------------------------------
# ADD HANDLER
# ----------------------------------------------------------

if not logger.handlers:

    logger.addHandler(
        file_handler
    )

    logger.addHandler(
        console_handler
    )

# ----------------------------------------------------------
# SHORTCUT FUNCTIONS
# ----------------------------------------------------------

def info(message: str):

    logger.info(message)


def warning(message: str):

    logger.warning(message)


def error(message: str):

    logger.error(message)


def debug(message: str):

    logger.debug(message)


def critical(message: str):

    logger.critical(message)