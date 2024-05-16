#!/usr/bin/env python3
""" this is function called filter_datum
    that returns the log message obfuscated
"""
import re
import logging
from typing import List
import mysql.connector
from os.environ import getenv
PII_FIELDS = ('name', 'email', 'phone', 'ssn', 'password')


def filter_datum(
                fields: List[str], redaction: str, message: str, separator: str
                ) -> str:
    """ returns the log message obfuscated """
    for field in fields:
        message = re.sub(
            rf'{field}=(.*?){separator}',
            f'{field}={redaction}{separator}', message
        )
    return message


def get_logger() -> logging.Logger:
    """ a func used to get a logger """
    logger = logging.getLogger("user_data")
    s_handler = logging.StreamHandler()
    s_handler.setLevel(logging.INFO)
    logger.propagate = False
    formatter = RedactingFormatter(fields=PII_FIELDS)
    s_handler.setFormatter(formatter)
    logger.setHandler(s_handler)
    return logger

user=getenv('PERSONAL_DATA_DB_USERNAME', 'root')
password=getenv('PERSONAL_DATA_DB_PASSWORD', '')
host=getenv('PERSONAL_DATA_DB_HOST', 'localhost')
name=getenv('PERSONAL_DATA_DB_NAME')


def get_db() -> mysql.connector.connection.MySQLConnection:
    """ a fucntion that return a connction object """
    cnx = mysql.connector.connection.MySQLConnection(
            host=host,
            user=user,
            password=password,
            database=name
        )
    return cnx


class RedactingFormatter(logging.Formatter):
    """ RedactingFormatter class """
    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        """ RedactingFormatter class constructor"""
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        """ this is the format method """
        return filter_datum(
            self.fields, self.REDACTION,
            super().format(record), self.SEPARATOR
        )
