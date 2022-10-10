# coding: utf-8
import uuid
from sqlalchemy import Column, ForeignKey, String, Integer, Text, Sequence, Boolean, DateTime, BigInteger, Time, \
    Float, REAL
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship


Base = declarative_base()


class User(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String)
    telegram_id = Column(Integer)


class Category(Base):
    __tablename__ = 'category'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String)
