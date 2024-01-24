#!/usr/bin/env python3
"""DB module
"""
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session

from user import Base
from user import User
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.exc import InvalidRequestError


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
        """Add user"""
        user = User(email=email, hashed_password=hashed_password)
        self._session.add(user)
        self._session.commit()
        return user

    def find_user_by(self, **kwargs):
        """find the first row found in the users table as
        filtered by the method's input arguments"""
        if not kwargs:
            raise InvalidRequestError

        cols = User.__table__.columns.keys()
        for key in kwargs:
            if key not in cols:
                raise InvalidRequestError

        try:
            query = self._session.query(User).filter_by(**kwargs)
        except Exception:
            raise InvalidRequestError

        user = query.first()
        if not user:
            raise NoResultFound

        return user

    def update_user(self, user_id: id, **kwargs) -> None:
        """update user"""
        user = self.find_user_by(id=user_id)
        cols = User.__table__.columns.keys()
        for key, value in kwargs.items():
            if key not in cols:
                raise ValueError
            setattr(user, key, value)
        self._session.commit()
