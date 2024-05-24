#!/usr/bin/env python3
""" a class used to set ex-date for sesstion
    that is onnce created
"""
from api.v1.auth.session_auth import SessionAuth
from os
from datetime import datetime


class SessionExpAuth(SessionAuth):
    """ the main class fucntion startes here
    """
    def __init__(self):
        """ constructor fucntion for session
            authentication expiredate
        """"
        session_duration = int(os.environ.get('SESSION_DURATION', 0))
    
    def create_session(self, user_id=None):
        """ over riding the create session class
            from the parent class
        """
        ses_id = super().create_session(user_id)
        if ses_id is None:
            return None
        user_id = self.user_id_for_session_id(ses_id)
        created_at = datetime.now()
        session_dict = {"user_id": user_id, "created_at": created_at}
        self.user_id_by_session_id[ses_id] = session_dict
        return ses_id
        