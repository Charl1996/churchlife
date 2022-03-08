from sqlalchemy import Column, Integer, String, ForeignKey, Table
from sqlalchemy.orm import relationship

from postgresql import Base


organisation_user_table = Table(
    'organisations_users',
    Base.metadata,
    Column('users_id', ForeignKey('users.id')),
    Column('organisations_id', ForeignKey('organisations.id')),
)


class Organisation(Base):
    __tablename__ = 'organisations'

    id = Column(Integer, primary_key=True, index=True)
    domain = name = Column(String, unique=True, index=True)
    name = Column(String)

    users = relationship(
        'User',
        secondary=organisation_user_table,
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
        secondary=organisation_user_table,
        back_populates='users'
    )
