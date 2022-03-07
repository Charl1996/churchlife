from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from postgresql import Base, engine


class Organisation(Base):
    __tablename__ = 'organisations'
    __table_args__ = {'extend_existing': True}

    id = Column(Integer, primary_key=True, index=True)
    domain = name = Column(String, unique=True, index=True)
    name = Column(String)


# class User(Base):
#     __tablename__ = 'users'
#     __table_args__ = {'extend_existing': True}
#
#     id = Column(Integer, primary_key=True, index=True)
#     first_name = Column(String)
#     last_name = Column(String)
#     email = Column(String, unique=True, index=True)
#     password = Column(String)
#
#     # organisation_id = Column(Integer, ForeignKey('organisations.id'))
#     organisation = relationship('Organisation', back_populates='users')
