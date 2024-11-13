#!/usr/bin/env python3
"""
    Module containing the 'BasicAuth' class.
"""
from .auth import Auth
from flask import request
import re


class BasicAuth(Auth):
    """
        BasicAuth class containing functions for 'Basic' authentication.
    """
    def extract_base64_authorization_header(
            self, authorization_header: str) -> str:
        """
            Method that extracts the base64 encoded header from the
            header of the request using Basic Authentication.
        """
        if (
            authorization_header is None or
            not isinstance(authorization_header, str) or
            not re.match(r"^Basic\s.*", authorization_header)
        ):
            return None

        return authorization_header[6:]
