#!/usr/bin/env python3
"""
    Module containing the 'BasicAuth' class.
"""
from .auth import Auth
import base64
import binascii
from models.user import User
import re
from typing import TypeVar


class BasicAuth(Auth):
    """
        BasicAuth class containing functions for 'Basic' authentication.
    """
    def extract_base64_authorization_header(
            self, authorization_header: str) -> str:
        """
            Extracts the base64-encoded header from the
            header of the request using Basic Authentication.
        """
        if (
            authorization_header is None or
            not isinstance(authorization_header, str) or
            not re.match(r"^Basic\s.*", authorization_header)
        ):
            return None

        return authorization_header[6:]

    def decode_base64_authorization_header(
            self, base64_authorization_header: str) -> str:
        """
            Decodes the base64-encoded string gotten from the method above.
        """
        if (
            base64_authorization_header is None or
            not isinstance(base64_authorization_header, str)
        ):
            return None

        try:
            decoded_bytes = base64.b64decode(
                base64_authorization_header,
                validate=True
            )
            decoded_str = decoded_bytes.decode('utf-8')

            return decoded_str
        except binascii.Error:
            return None

    def extract_user_credentials(
            self, decoded_base64_authorization_header: str) -> (str, str):
        """
            Extracts the email and password from the decoded string.
        """
        if (
            decoded_base64_authorization_header is None or
            not isinstance(decoded_base64_authorization_header, str) or
            ":" not in decoded_base64_authorization_header
        ):
            return None, None

        email = decoded_base64_authorization_header.split(':')[0]
        password = decoded_base64_authorization_header.split(':')[1]

        return email, password

    def user_object_from_credentials(
            self, user_email: str, user_pwd: str) -> TypeVar('User'):
        """
            Returns the 'User' onject based on his email and password.
        """
        if (
            user_email is None or
            user_pwd is None or
            not isinstance(user_email, str) or
            not isinstance(user_pwd, str)
        ):
            return None

        try:
            users = User.search({'email': user_email})
        except Exception:
            return None
        if not users:
            return None
        user = users[0]
        if user.is_valid_password(user_pwd):
            return user

        return None
