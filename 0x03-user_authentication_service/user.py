#!/usr/bin/env python3
"""Module for Users model."""
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String

Base = declarative_base()


class User(Base):
    """User class to interact with the users table."""

    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    email = Column(String(250), nullable=False)
    hashed_password = Column(String(250), nullable=False)
    session_id = Column(String(250), nullable=True)
    reset_token = Column(String(250), nullable=True)

    def __repr__(self):
        """Method for string representation of the User object."""
        return "<User(id='%s', email='%s'>" % (
            self.id, self.email)
