#!/usr/bin/env python3

""" a class user -- it is a table --- and it is
    connected with sqlalchemy moduel to create
    the table and update and quary user
"""
from sqlalchemy import create_engine, String, Integer, Column
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# engine = create_engine('')

# session = sessionmaker(bind=engine)
# session = session()

Base = declarative_base()


class User(Base):
    """
        the user module used to create the table used
        to store the info about the user
    """
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    email = Column(String(250), nullable=False)
    hashed_password = Column(String(250), nullable=False)
    session_id = Column(String(250),)
    reset_token = Column(String(250))
