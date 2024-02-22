#!/usr/bin/env python3


"""
User Model
"""

import logging
from sqlalchemy import *
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session


logging.disable(logging.WARNING)
Base = declarative_base()


session = Session()


class User(Base):
    """User class"""
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, autoincrement="auto")
    email = Column(String(250), nullable=False)
    hashed_password = Column(String(250), nullable=False)
    session_id = Column(String(250), nullable=True)
    reset_token = Column(String(250), nullable=True)
