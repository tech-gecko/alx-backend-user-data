#!/usr/bin/env python3
"""
    Module containing the 'Auth' class.
"""
import os
import re
from typing import List, TypeVar


class Auth:
    """
        Auth class containing auth functions.
    """
    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """
            Checks if a given path requires auth.
        """
        if path is None or excluded_paths is None:
            return True
        if excluded_paths == []:
            return True

        if path[-1] != '/':
            path = path + '/'

        for _path in excluded_paths:
            if _path[-1] == '*':
                pattern = _path.replace('*', '.*')
                if re.fullmatch(pattern, path):
                    return False

        if path in excluded_paths:
            return False

        return True

    def authorization_header(self, request=None) -> str:
        """
            Gets the auth header for a given request (if not None).
        """
        if request is None:
            return None

        return request.headers.get('Authorization', None)

    def current_user(self, request=None) -> TypeVar('User'):
        """
            Gets the current user from the request.
        """
        return None

    def session_cookie(self, request=None):
        """
            Returns a cookie value from a request.
        """
        if request is None:
            return None

        _my_session_id = os.getenv('SESSION_NAME')

        if _my_session_id is None:
            return None

        cookie_value = request.cookies.get(_my_session_id)

        return cookie_value
