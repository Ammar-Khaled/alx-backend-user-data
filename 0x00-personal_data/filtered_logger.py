#!/usr/bin/env python3
"""Filtered logger."""
from typing import List
from re import sub
import logging
from mysql.connector.connection import MySQLConnection
from os import environ

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
    db_username = environ.get("PERSONAL_DATA_DB_USERNAME", "root")
    db_password = environ.get("PERSONAL_DATA_DB_PASSWORD", "")
    db_host = environ.get("PERSONAL_DATA_DB_HOST", "localhost")
    db_name = environ.get("PERSONAL_DATA_DB_NAME")

    connection = MySQLConnection(user=db_username, password=db_password,
                                 host=db_host, database=db_name)

    return connection


def main() -> None:
    """logs all users."""
    connection = get_db()
    cursor = connection.cursor()
    cursor.execute('SELECT * FROM users')
    rows = cursor.fetchall()
    logger = get_logger()
    for row in rows:
        msg = f'name={row[0]}; email={row[1]}; phone={row[2]}; ssn={row[2]}; '\
              f'password={row[3]}; ip={row[4]}; last_login={row[5]}; '\
              f'user_agent={row[6]};'
        logger.info(msg)


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


if __name__ == '__main__':
    main()
