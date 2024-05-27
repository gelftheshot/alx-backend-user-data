#!/usr/bin/env python3
import bcrypt
from db import DB
from user import User
from sqlalchemy.exc import NoResultFound
from uuid import uuid4

def _hash_password(password: str) -> bytes:
    """
        a method used to hash a password using
        bcrypt module
    """
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(password.encode('utf-8'), salt)

def _generate_uuid() -> str:
    """ Generates UUID
    Returns string representation of new UUID
    """
    return str(uuid4())


class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        self._db = DB()
    
    def register_user(self, email : str, password: str) -> User:
        """
                a method used to register user
        """
        try:
            user = self._db.find_user_by(email=email)
        except NoResultFound:
            hased_pwd = _hash_password(password)
            user = self._db.add_user(email, hased_pwd)
            return user
        else:
            raise ValueError(f'User {email} already exists')

    def valid_login(self, email: str, password: str) -> bool:
        """
            check if the password is correct or not
        """
        try:
            user = self._db.find_user_by(email=email)
        except NoResultFound:
            return False
        else:
            return bcrypt.checkpw(password.encode('utf-8'), user.hashed_password)