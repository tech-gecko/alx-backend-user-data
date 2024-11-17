#!/usr/bin/env python3
""" Session authentication with expiration module for the API.
    Session saved in file DB instead of in memory.
"""
from datetime import datetime, timedelta
from models.user_session import UserSession
import os
from .session_exp_auth import SessionExpAuth


class SessionDBAuth(SessionExpAuth):
    """ Session authentication class with expiration.
        Session saved in file DB instead of in memory.
    """
    def create_session(self, user_id=None):
        """ Creates a session id for the user.
            Session stored in DB.
        """
        session_id = super().create_session(user_id)
        if type(session_id) != str:
            return None

        kwargs = {
            'user_id': user_id,
            'created_at': datetime.now(),
        }
        user_session = UserSession(**kwargs)
        user_session.save()

        return session_id

    def user_id_for_session_id(self, session_id=None) -> str:
        """ Retrieves the user id of the user associated with
            a given session id.
            Retrieves user_id from DB.
        """
        try:
            sessions = UserSession.search({'session_id': session_id})
        except Exception:
            return None
        if len(sessions) <= 0:
            return None

        cur_time = datetime.now()
        time_span = timedelta(seconds=self.session_duration)
        exp_time = sessions[0].created_at + time_span
        if exp_time < cur_time:
            return None

        return sessions[0].user_id

    def destroy_session(self, request=None):
        """
            Deletes the user session from DB and logs out.
        """
        if request is None:
            return False
        session_id = self.session_cookie(request)
        try:
            sessions = UserSession.search({'session_id': session_id})
        except Exception:
            return False
        if len(sessions) <= 0:
            return False

        sessions[0].remove()

        return True
