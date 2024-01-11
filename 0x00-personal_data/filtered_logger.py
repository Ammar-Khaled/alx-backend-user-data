#!/usr/bin/env python3
"""Filtered logger."""
from typing import List
from re import sub


def filter_datum(fields: List[str], redaction: str, message: str,
                 separator: str) -> str:
    """Return the log message obfuscated."""
    for field in fields:
        message = sub(field + "=.*?" + separator,
                      field + "=" + redaction + separator, message)
    return message
