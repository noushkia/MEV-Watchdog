import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path

from hexbytes._utils import hexstr_to_bytes


def hex_to_int(value: str) -> int:
    return int.from_bytes(hexstr_to_bytes(value), byteorder="big")


def equal_within_percent(
        first_value: int, second_value: int, threshold_percent: float
) -> bool:
    difference = abs(
        (first_value - second_value) / (0.5 * (first_value + second_value))
    )
    return difference < threshold_percent


def get_handler(log_path: Path, formatter: logging.Formatter, rotate: bool = False) -> logging.Handler:
    """Setup logger with file handler."""
    if rotate:
        file_handler = RotatingFileHandler(log_path, maxBytes=2300000, backupCount=5)
    else:
        file_handler = logging.FileHandler(log_path)
    file_handler.setLevel(logging.INFO)
    file_handler.setFormatter(formatter)

    return file_handler
