#!/usr/bin/env python3
""" this is function called filter_datum
    that returns the log message obfuscated
"""
import re
import logging


def filter_datum(
                fields: str, redaction: str, message: str, separator: str
                ) -> str:
    """ returns the log message obfuscated """
    for field in fields:
        message = re.sub(
            rf'{field}=(.*?){separator}',
            f'{field}={redaction}{separator}', message
        )
    return message


class RedactingFormatter(logging.Formatter):
    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: list, fmat: str = FORMAT):
        super(RedactingFormatter, self).__init__(fmat)
        self.fields = fields
        self.fmat = fmat

    def format(self, record: logging.LogRecord) -> str:
        return filter_datum(
            self.fields, self.REDACTION,
            super().format(record), self.SEPARATOR
        )