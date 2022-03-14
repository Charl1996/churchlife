from sqlalchemy import Column, Integer, String, ForeignKey, Table
from sqlalchemy.orm import relationship

from postgresql import Base


class OrganisationsUsers(Base):
    __tablename__ = 'organisations_users'

    id = Column(Integer, primary_key=True, index=True)
    organisation_id = Column(
        Integer,
        ForeignKey('organisations.id'),
    )

    user_id = Column(
        Integer,
        ForeignKey('users.id'),
    )


class Organisation(Base):
    __tablename__ = 'organisations'

    id = Column(Integer, primary_key=True, index=True)
    domain = Column(String, unique=True, index=True)
    name = Column(String)

    users = relationship(
        'User',
        secondary='organisations_users',
        back_populates='organisations'
    )


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String)
    last_name = Column(String)
    email = Column(String, unique=True, index=True)
    password = Column(String)
    organisation_id = Column(Integer, ForeignKey('organisations.id'))

    organisations = relationship(
        'Organisation',
        secondary='organisations_users',
        back_populates='users'
    )
