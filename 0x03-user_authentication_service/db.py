#!/usr/bin/env python3
"""DB module
"""
from base import Base

from sqlalchemy import create_engine, tuple_
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.exc import InvalidRequestError
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session

from typing import List, Dict
from user import User


class DB:
    """DB class
    """
    def __init__(self) -> None:
        """Initialize a new DB instance.
        """
        self._engine = create_engine("sqlite:///a.db", echo=False)
        Base.metadata.drop_all(self._engine)
        Base.metadata.create_all(self._engine)
        self.__session = None

    @property
    def _session(self) -> Session:
        """Memoized session object.
        """
        if self.__session is None:
            DBSession = sessionmaker(bind=self._engine)
            self.__session = DBSession()
        return self.__session

    def add_user(self, email: str, hashed_password: str) -> User:
        """
            Adds a new user to the database.
            Returns an instance of the new user.
        """
        session = self._session
        new_user = User(email=email, hashed_password=hashed_password)
        session.add(new_user)
        session.commit()

        return new_user

    def find_user_by(self, **kwargs: Dict) -> User:
        """
            Returns the first row found in the DB
            as filtered by 'args' or 'kwargs'.
        """
        session = self._session
        fields, values = [], []

        for key, value in kwargs.items():
            if hasattr(User, key):
                fields.append(getattr(User, key))
                values.append(value)
            else:
                raise InvalidRequestError()

        result = session.query(User).filter(
            tuple_(*fields).in_([tuple(values)])
        ).first()
        if result is None:
            raise NoResultFound()

        return result

    def update_user(self, user_id: int, **kwargs: Dict) -> None:
        """
            Update the user's (whose ID is passed) attributes as passed in the
            method's kwargs then commit changes to the database.
        """
        session = self._session
        user = self.find_user_by(id=user_id)
        if user is None:
            return

        updater = {}
        for key, value in kwargs.items():
            if not hasattr(User, key):
                raise ValueError
            else:
                updater[getattr(User, key)] = value

        session.query(User).filter(id == user_id).update(
            updater, synchronize_session=False
        )

        session.commit()
