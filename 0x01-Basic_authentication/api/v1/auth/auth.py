#!/usr/bin/env python3
"""
    Module containing the 'Auth' class.
"""
from flask import request
from typing import List, TypeVar


class Auth:
    """
        Auth class containing auth functions.
    """
    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """
            Checks if a given path requires auth.
        """
        return False

    def authorization_header(self, request=None) -> str:
        """
            Gets the auth header for a given request (if not None).
        """
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """
            Gets the current user from the request.
        """
        return None
