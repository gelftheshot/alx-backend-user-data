#!/usr/bin/env python3
"""
    a calss the inherit from auth
"""
from api.v1.auth.auth import Auth
import base64
from models.user import User
from typing import TypeVar

class BasicAuth(Auth):
    """ empty class for now
        but will be modifed later
    """

    def extract_base64_authorization_header(
            self, authorization_header: str) -> str:
        """ return the the base64 part of
            header for basic authentication
        """
        if authorization_header is None:
            return None
        elif not isinstance(authorization_header, str):
            return None
        elif not (authorization_header[0:6] == "Basic "):
            return None
        return authorization_header[6:]
    import base64

    def decode_base64_authorization_header(
            self, base64_authorization_header: str) -> str:
        """
            returns the decoded base64 string
        """
        if base64_authorization_header is None:
            return None
        if not isinstance(base64_authorization_header, str):
            return None
        try:
            base64_bytes = base64_authorization_header.encode('utf-8')
            message_bytes = base64.b64decode(base64_bytes)
            message = message_bytes.decode('utf-8')
            return message
        except BaseException:
            return None

    def extract_user_credentials(
            self, decoded_base64_authorization_header: str) -> (str, str):
        """ extract email and password from it
        """
        if decoded_base64_authorization_header is None:
            return (None, None)
        if not isinstance(decoded_base64_authorization_header, str):
            return (None, None)
        if ':' not in decoded_base64_authorization_header:
            return (None, None)
        email_and_pass = decoded_base64_authorization_header.split(':', 1)

        return email_and_pass[0], email_and_pass[1]

    def user_object_from_credentials(
            self, user_email: str, user_pwd: str) -> TypeVar('User'):
        """return user data based on user name
            and password
        """
        if user_email is None:
            return None
        if user_pwd is None:
            return None
        if not isinstance(user_email, str):
            return None

        if not isinstance(user_pwd, str):
            return None

        try:
            found_users = User.search({'email': user_email})
        except Exception:
            return None

        for user in found_users:
            if user.is_valid_password(user_pwd):
                return user

        return None
