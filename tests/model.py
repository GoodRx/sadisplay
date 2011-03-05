# -*- coding: utf-8 -*-
from sqlalchemy import Column, Integer, Unicode, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relation


BASE = declarative_base()


class User(BASE):
    __tablename__ = 'user_table'

    id = Column(Integer, primary_key=True)
    name = Column(Unicode(50))

    def login(self):
        pass

    def __repr__(self):
        pass

class Admin(User):
    __tablename__ = 'admin_table'
    __mapper_args__ = {'polymorphic_identity': 'user_table'}

    id = Column(Integer, ForeignKey('user_table.id'), primary_key=True)
    phone = Column(Unicode(50))

    def permissions(self):
        pass

    def __unicode__(self):
        pass

class Address(BASE):
    __tablename__ = 'address_table'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('user_table.id'))
    user = relation(User, backref="address")
