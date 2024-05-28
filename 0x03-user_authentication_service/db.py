#!/usr/bin/env python3
"""DB module
"""
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session
from sqlalchemy.exc import InvalidRequestError, NoResultFound
import bcrypt
from user import Base
from user import User

class DB:
    """DB class
    """

    def __init__(self) -> None:
        """Initialize a new DB instance
        """
        self._engine = create_engine("sqlite:///a.db", echo=False)
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
        """
            a method used to add the user
        """
        new_user = User(email = email, hashed_password = hashed_password)
        self._session.add(new_user)
        self._session.commit()
        return new_user
 

    def find_user_by(self, **kwargs):
        """
            This method takes in arbitrary keyword arguments
            and returns the first row found in the users table
            as filtered by the method’s input arguments
        """
        try:
            user = self._session.query(User).filter_by(**kwargs).one()
            return user
        except NoResultFound as e:
            raise e
        except InvalidRequestError as e :
            raise e
        
    def update_user(self, user_id, **kwargs) -> None:
        """
            The method will use find_user_by to locate the user 
            to update, then will update the user’s attributes as
            passed in the method’s arguments then commit changes
            to the database.

            If an argument that does not correspond to a user attribute
            is passed, raise a ValueError
        """
        user = self.find_user_by(id=user_id)
        
        if user:
            for key, value in kwargs.items():
                if hasattr(user, key):
                    setattr(user, key, value)
                else:
                    raise ValueError
            self._session.commit()
