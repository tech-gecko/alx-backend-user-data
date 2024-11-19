#!/usr/bin/env python3
"""
    Authentication module.
"""
import bcrypt
from db import DB
from sqlalchemy.orm.exc import NoResultFound
from user import User


def _hash_password(self, password: str) -> bytes:
    """
        Takes in a password string argument and returns bytes.
        The returned bytes is a salted hash of the input password.
    """
    # Convert str to bytes for use in bcrypt.hashpw
    bytes_password = password.encode("utf-8")
    hashed_password = bcrypt.hashpw(bytes_password, bcrypt.gensalt())

    return hashed_password


class Auth:
    """Auth class to interact with the authentication database.
    """
    def __init__(self):
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """
            Takes (mandatory) email and password string arguments and
            returns the User object of the new user registered.
        """
        try:
            user = self._db.find_user_by(email=email)
        except NoResultFound:
            hashed_password = _hash_password(password)
            new_user = self._db.add_user(email, hashed_password)
            return new_user
        else:
            raise ValueError(f"User {email} already exists")
