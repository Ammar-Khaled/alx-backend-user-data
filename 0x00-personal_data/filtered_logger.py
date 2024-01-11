#!/usr/bin/env python3
"""Filtered logger."""
from typing import List
from re import sub
import logging
from mysql.connector.connection import MySQLConnection
from os import getenv

PII_FIELDS = ('name', 'email', 'phone', 'ssn', 'password')


def filter_datum(fields: List[str], redaction: str, message: str,
                 separator: str) -> str:
    """Return the log message obfuscated."""
    for field in fields:
        message = sub(field + "=.*?" + separator,
                      field + "=" + redaction + separator, message)
    return message


def get_logger() -> logging.Logger:
    """Create a Logger."""
    formatter = RedactingFormatter(PII_FIELDS)

    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(formatter)

    logger = logging.getLogger("user_data")
    logger.propagate = False
    logger.setLevel(logging.INFO)
    logger.addHandler(stream_handler)

    return logger


def get_db() -> MySQLConnection:
    """Connect to MySQL db."""
    db_username = getenv('PERSONAL_DATA_DB_USERNAME') or 'root'
    db_password = getenv('PERSONAL_DATA_DB_PASSWORD') or ''
    db_host = getenv('PERSONAL_DATA_DB_HOST') or 'localhost'
    db_name = getenv('PERSONAL_DATA_DB_NAME')

    connection = MySQLConnection(user=db_username, password=db_password,
                         host=db_host, database=db_name)

    return connection


class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter class
        """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        """Init method."""
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        """Filter values in incoming log records."""
        return filter_datum(self.fields, self.REDACTION,
                            super().format(record), self.SEPARATOR)
