#!/usr/bin/env python3
""" a class used for authentication purpose """
from flask import request
from typing import List
from typing import TypeVar


class Auth():
    """the main authentication class
    """
    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """ return ture if path is not in
            excluded_path and aggs none
        """
        if path is None:
            return True
        if excluded_paths is None or len(excluded_paths) == 0:
            return True
        path = path + '/' if not path.endswith('/') else path
        excluded_paths = [
            p + '/' if not p.endswith('/') else p
            for p in excluded_paths]
        if path in excluded_paths:
            return False
        return True

    def authorization_header(self, request: request = None) -> str:
        """ return the header from atuorzation or none
        """
        if request is None:
            return None
        return request.headers.get("Authorization", None)

    def current_user(self, request=None) -> TypeVar('User'):
        """ return none for now it wiil be
        """
        return None