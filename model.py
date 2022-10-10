# coding: utf-8
from sqlalchemy import Column, ForeignKey, String, Integer, DateTime
from sqlalchemy.ext.declarative import declarative_base


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
    slug = Column(String)
    pattern = Column(String)


class Cost(Base):
    __tablename__ = 'cost'

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('user.id'))
    category_id = Column(Integer, ForeignKey('category.id'))
    sum_rub = Column(Integer)
    sum_tng = Column(Integer)
    date = Column(DateTime)


class Answer(Base):
    __tablename__ = 'answer'

    id = Column(Integer, primary_key=True, autoincrement=True)
    type = Column(String)
    text = Column(String)
