#!/usr/bin/env python3
"""
This module defines the SessionExpAuth class, which extends the SessionAuth
class to add session expiration functionality. The session duration is
determined by the 'SESSION_DURATION' environment variable.
"""

from api.v1.auth.session_auth import SessionAuth
from os import environ
from datetime import datetime, timedelta


class SessionExpAuth(SessionAuth):
    """
    A class used to manage sessions with an expiration date.

    Attributes:
        session_duration: The duration of the session in seconds. This is
            determined by the 'SESSION_DURATION' environment variable, with
            a default of 0 if the variable is not set.
    """

    def __init__(self):
        """
        Initializes a new SessionExpAuth instance and sets the session duration.
        """
        self.session_duration = int(environ.get('SESSION_DURATION', 0))

    def create_session(self, user_id=None):
        """
        Creates a new session and stores the user ID and creation time.

        Args:
            user_id: The ID of the user for the session.

        Returns:
            The ID of the created session, or None if the session could not be
            created.
        """
        ses_id = super().create_session(user_id)
        if ses_id is None:
            return None
        user_id = self.user_id_for_session_id(ses_id)
        created_at = datetime.now()
         SessionExpAuth.user_id_by_session_id[ses_id] = {
            'user_id': user_id,
            'created_at': datetime.now()
        }
        return ses_id

    def user_id_for_session_id(self, session_id=None):
        """
        Retrieves the user ID associated with a session ID.

        This method also checks if the session has expired based on the creation
        time and the session duration.

        Args:
            session_id: The ID of the session.

        Returns:
            The ID of the user for the session, or None if the session ID is not
            provided, the session does not exist, or the session has expired.
        """
        if session_id is None:
            return None

        session_dict = self.user_id_by_session_id.get(session_id, None)
        if session_dict is None:
            return None
        if 'created_at' not in session_dict:
            return None

        if self.session_duration <= 0:
            return session_dict.get('user_id')

        creation_time = session_dict.get('created_at')
        session_length = timedelta(seconds=self.session_duration)
        expiry_time = creation_time + session_length

        if expiry_time < datetime.now():
            return None
        return session_dict.get('user_id')