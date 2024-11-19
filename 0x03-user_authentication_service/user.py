#!/usr/bin/env python3
"""
    user module.
    A module containing a SQLAlchemy model for a database table named 'users'.
"""
from base import Base
from sqlalchemy import Column, Integer, String


class User(Base):
    """
        'User' class.
        A SQLAlchemy model for a database table named 'users'.
    """
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, autoincrement=True)
    email = Column(String(250), nullable=False)
    hashed_password = Column(String(250), nullable=False)
    session_id = Column(String(250), nullable=True)
    reset_token = Column(String(250), nullable=True)
