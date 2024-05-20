#!/usr/bin/env python3
"""
    a calss the inherit from auth
"""
from api.v1.auth.auth import Auth


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
