#!/usr/bin/env python3
"""DB module
"""
from base import Base

from sqlalchemy import create_engine
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

    def find_user_by(self, *args: List, **kwargs: Dict) -> User:
        """
            Returns the first row found in the DB
            as filtered by 'args' or 'kwargs'.
        """
        session = self._session

        if args:
            try:
                user = session.query(User).\
                    filter(User.email == args[0]).\
                    filter(User.hashed_password == args[1]).\
                    one()
            except NoResultFound:
                raise NoResultFound
        elif kwargs:
            try:
                user = session.query(User).filter_by(**kwargs).one()
            except NoResultFound:
                raise NoResultFound
        else:
            raise InvalidRequestError

        if not user:
            raise InvalidRequestError

        return user

    def update_user(self, user_id: int, **kwargs: Dict) -> None:
        """
            Update the user's (whose ID is passed) attributes as passed in the
            method's kwargs then commit changes to the database.
        """
        session = self._session
        user = self.find_user_by(id=user_id)
        session.add(user)

        for key, value in kwargs.items():
            if key not in user.__table__.columns:
                raise ValueError

            setattr(user, key, value)

        session.commit()

        return
