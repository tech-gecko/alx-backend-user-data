#!/usr/bin/env python3
"""
    Module containing the 'SessionExpAuth' class.
"""
from api.v1.auth.session_auth import SessionAuth
from datetime import datetime, timedelta
from os import getenv


class SessionExpAuth(SessionAuth):
    """
        SessionExpAuth class containing functions for
        session authentication with support for session expiry.
    """
    def __init__(self):
        try:
            self.session_duration = int(getenv('SESSION_DURATION', '0'))
        except Exception:
            self.session_duration = 0

    def create_session(self, user_id=None) -> str:
        """
            Creates a session ID for a user ID.
            Adds support to know the time the session was created.
        """
        try:
            session_id = super().create_session(user_id)

            self.session_dict = {}
            self.session_dict['user_id'] = user_id
            self.session_dict['created_at'] = datetime.now()

            self.user_id_by_session_id[session_id] = self.session_dict

            return session_id
        except Exception:
            return None

    def user_id_for_session_id(self, session_id=None) -> str:
        """
            Returns a user ID based on a session ID.
            Returns None if session has expired.
        """
        if session_id is None:
            return None

        if session_id not in self.user_id_by_session_id:
            return None

        if self.session_duration <= 0:
            return self.session_dict['user_id']

        if 'created_at' not in self.session_dict:
            return None

        if (
            self.session_dict['created_at'] + timedelta(self.session_duration)
            < datetime.now
        ):
            return None

        return self.session_dict['user_id']
