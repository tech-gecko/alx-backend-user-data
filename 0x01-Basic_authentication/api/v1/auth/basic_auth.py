#!/usr/bin/env python3
"""
    Module containing the 'BasicAuth' class.
"""
from .auth import Auth
from flask import request
from typing import List, TypeVar


class BasicAuth(Auth):
    """
        BasicAuth class containing functions for 'Basic' authentication.
    """
    pass
