import os
import sys
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, deferred
from sqlalchemy import create_engine, LargeBinary, BLOB

Base = declarative_base()


class User(Base):
    """ Create User table to store user information """
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    email = Column(String(250), nullable=False)
    picture = Column(String(250))


class Catalog(Base):
    """ Create Catalog table to store catalog information """
    __tablename__ = 'catalog'

    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship(User, cascade="delete")
    description = Column(String(250))

# This serialize function is used to send JSON objects in a
# serializable format
    @property
    def serialize(self):
        return {
             'name': self.name,
             'id': self.id,
             'description': self.description
               }


class CatalogItem(Base):
    __tablename__ = 'catalog_item'

    name = Column(String(80), nullable=False)
    id = Column(Integer, primary_key=True)
    description = Column(String(250))
    catalog_id = Column(Integer, ForeignKey('catalog.id'))
    catalog = relationship(Catalog, cascade="delete")
    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship(User, cascade="delete")

    @property
    def serialize(self):
        return {
             'name': self.name,
             'description': self.description,
             'id': self.id
               }

engine = create_engine('sqlite:///catalogmenuwithusers.db')

Base.metadata.create_all(engine)
