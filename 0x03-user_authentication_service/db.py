#!/usr/bin/env python3
"""DB module
"""
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import InvalidRequestError
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.orm.session import Session
from user import User
from user import Base


class DB:
    """DB class
    """

    def __init__(self) -> None:
        """Initialize a new DB instance
        """
        self._engine = create_engine("sqlite:///a.db")
        Base.metadata.drop_all(self._engine)
        Base.metadata.create_all(self._engine)
        self.__session = None

    @property
    def _session(self) -> Session:
        """Memoized session object
        """
        if self.__session is None:
            DBSession = sessionmaker(bind=self._engine)
            self.__session = DBSession()
        return self.__session

    def add_user(self, email: str, hashed_password: str) -> User:
        """Add a new user to the database
        """
        user = User(email=email, hashed_password=hashed_password)
        self._session.add(user)
        self._session.commit()
        return user

    def find_user_by(self, **kwargs) -> User:
        """Returns the first row found in the users table
        """
        if not kwargs:
            raise InvalidRequestError
        found_user = self._session.query(User).filter_by(**kwargs).first()
        if found_user:
            return found_user
        else:
            raise NoResultFound

    def update_user(self, user_id: int, **kwargs) -> None:
        """Update the user
        """
        user = self.find_user_by(id=user_id)
        for key, value in kwargs.items():
            if not hasattr(user, key):
                raise ValueError
            setattr(user, key, value)
        self._session.commit()
        return None
