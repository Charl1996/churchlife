from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from postgresql import Base


class Organisation(Base):
    __tablename__ = 'organisations'

    id = Column(Integer, primary_key=True, index=True)
    domain = name = Column(String, unique=True, index=True)
    name = Column(String)

    users = relationship('User', back_populates='organisation')


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String)
    last_name = Column(String)
    email = Column(String, unique=True, index=True)
    password = Column(String)
    organisation_id = Column(Integer, ForeignKey('organisations.id'))

    organisation = relationship('Organisation', back_populates='users')
