#!/usr/bin/env python3
"""
    Authentication module.
"""
import bcrypt
from db import DB
from sqlalchemy.orm.exc import NoResultFound
from user import User
import uuid


def _hash_password(password: str) -> bytes:
    """
        Takes in a password string argument and returns bytes.
        The returned bytes is a salted hash of the input password.
    """
    # Convert str to bytes for use in bcrypt.hashpw
    bytes_password = password.encode("utf-8")
    hashed_password = bcrypt.hashpw(bytes_password, bcrypt.gensalt())

    return hashed_password


def _generate_uuid() -> str:
    """
        Returns a string representation of a new UUID.
    """
    return str(uuid.uuid4())


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

    def valid_login(self, email: str, password: str) -> bool:
        """
            Returns True if email and password are valid. Else, returns False.
        """
        try:
            user = self._db.find_user_by(email=email)
        except Exception:
            return False

        if user:
            # Checks if passed pw matches the one in DB.
            if bcrypt.checkpw(
                password.encode('utf-8'), getattr(user, 'hashed_password')
            ):
                return True

        return False

    def create_session(self, email: str) -> str:
        """
            Takes an email string arg and returns the session ID as a string.
        """
        try:
            user = self._db.find_user_by(email=email)
        except Exception:
            return None

        if not user:
            return None

        new_session_id = _generate_uuid()
        setattr(user, 'session_id', new_session_id)

        return new_session_id

    def get_user_from_session_id(self, session_id: str) -> User:
        """
            Takes a single session_id string argument and
            returns the corresponding User or None.
        """
        if session_id is None:
            return None

        try:
            user = self._db.find_user_by(session_id=session_id)
        except Exception:
            return None

        if not user:
            return None

        return user

    def destroy_session(self, user_id: int) -> None:
        """
            Destroys a session associated with a given user.
        """
        if user_id is None:
            return

        self._db.update_user(user_id, session_id=None)

    def get_reset_password_token(self, email: str) -> str:
        """
            Generates a reset password token, updates the user's reset_token DB
            field and returns the token.
        """
        try:
            user = self._db.find_user_by(email=email)
        except Exception:
            raise ValueError

        reset_token = _generate_uuid()
        self._db.update_user(user.id, reset_token=reset_token)

        return reset_token

    def update_password(self, reset_token: str, password: str) -> None:
        """
            Updates the password of the user (if there's a user corresponding
            to the passed reset token) in the DB.
        """
        try:
            user = self._db.find_user_by(reset_token=reset_token)
        except Exception:
            raise ValueError

        hashed_password = _hash_password(password)
        self._db.update_user(
            user.id, hashed_password=hashed_password, reset_token=None
        )
