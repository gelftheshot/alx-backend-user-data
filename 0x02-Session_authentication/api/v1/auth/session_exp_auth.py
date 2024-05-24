#!/usr/bin/env python3
""" a class used to set ex-date for sesstion
    that is onnce created
"""
from api.v1.auth.session_auth import SessionAuth
from os import getenv


class SessionAuth(SessionAuth):
    """ the main class fucntion startes here
    """
    def __init__(self):