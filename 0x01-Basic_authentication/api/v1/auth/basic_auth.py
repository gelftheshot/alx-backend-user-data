#!/usr/bin/env python3
"""
    a calss the inherit from auth
"""
from api.v1.auth.auth import Auth
import base64


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
