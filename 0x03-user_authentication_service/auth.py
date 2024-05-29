#!/usr/bin/env python3
import bcrypt
from db import DB
from sqlalchemy.orm.exc import NoResultFound
from user import User
from uuid import uuid4
from typing import Union


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
    """
        Auth class to interact with the authentication database.
    """

    def __init__(self):
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """
            Creates a new user if the email does not exist
        """
        try:
            user = self._db.find_user_by(email=email)
        except NoResultFound:
            return self._db.add_user(email, _hash_password(password))
        else:
            raise ValueError("User %s already exists" % email)

    def valid_login(self, email: str, password: str) -> bool:
        """
            check if the password is correct or not
        """
        try:
            user = self._db.find_user_by(email=email)
        except NoResultFound:
            return False
        return bcrypt.checkpw(password.encode('utf-8'), user.hashed_password)

    def create_session(self, email: str) -> str:
        """
            create the session for one user with given
            emial address
        """
        try:
            user = self._db.find_user_by(email=email)
            ses_id = _generate_uuid()
            setattr(user, "session_id", ses_id)
            self._db._session.commit()
            return ses_id
        except NoResultFound:
            return None

    def get_user_from_session_id(self, session_id: str) -> Union[User, None]:
        """
            used to get user for a given session id
        """
        try:
            user = self._db.find_user_by(session_id=session_id)
            return user
        except NoResultFound:
            return None

    def destroy_session(self, user_id: str) -> None:
        """
            update a users session id to None
        """
        user = self._db.find_user_by(id=user_id)
        setattr(user, "session_id", None)
        return None

    def get_reset_password_token(self, email: str) -> str:
        """
            return the token of password from the user
        """
        try:
            user = self._db.find_user_by(email=email)
            token = _generate_uuid()
            setattr(user, 'reset_token', token)
            return token
        except NoResultFound:
            raise ValueError
