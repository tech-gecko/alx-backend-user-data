#!/usr/bin/env python3
"""
    Module containing the 'SessionAuth' class.
"""
from .auth import Auth
import uuid


class SessionAuth(Auth):
    """
        SessionAuth class containing functions for Session authentication.
    """
    # Dictionary containing session ID as key and user ID as value.
    user_id_by_session_id = {}

    def create_session(self, user_id: str = None) -> str:
        """
            Creates a session ID for a user ID.
        """
        if user_id is None or not isinstance(user_id, str):
            return None

        session_id = str(uuid.uuid4())
        self.user_id_by_session_id[session_id] = user_id

        return session_id

    def user_id_for_session_id(self, session_id: str = None) -> str:
        """
            Returns a user ID based on a session ID.
        """
        if session_id is None or not isinstance(session_id, str):
            return None

        user_id = self.user_id_by_session_id.get(session_id, None)
        if user_id is None:
            return None

        return user_id
