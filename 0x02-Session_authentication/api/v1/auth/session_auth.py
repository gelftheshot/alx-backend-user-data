#!/usr/bin/env python3
"""
    session authenticatim mechanizems
"""
from api.v1.auth.auth import Auth
from uuid import uuid4


class SessionAuth(Auth):
    """ empty for know i don't knw what to do
    """
    user_id_by_session_id = {}

    def create_session(self, user_id: str = None) -> str:
        """ a method that will creat a sesstion id for
            user id
        """
        if user_id is None:
            return None
        if not isinstance(user_id, str):
            return None
        ses_id = str(uuid4())
        self.user_id_by_session_id[ses_id] = user_id
        return ses_id

    def user_id_for_session_id(self, session_id: str = None) -> str:
        """ a method that will retuen a session id based on user id
        """
        if session_id is None:
            return None
        if not isinstance(session_id, str):
            return None
        return self.user_id_by_session_id.get(session_id)