#!/usr/bin/env python3
""" a class used for authentication purpose """
from flask import request
from typing import List
from typing import TypeVar

class Auth():
    """the main authentication class
    """
    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """ retun just fals for now
        """
        return False
    

    def authorization_header(self, request : request = None) -> str:
        """ return none for now it will be
        """
        return None

    
    def current_user(self, request=None) -> TypeVar('User'):
        """ return none for now it wiil be
        """
        return None

