from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Time, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

SET_NULL = "SET NULL"


class OrganisationsUsers(Base):
    __tablename__ = 'organisations_users'
    __table_args__ = {'extend_existing': True}

    id = Column(Integer, primary_key=True, index=True)
    organisation_id = Column(
        Integer,
        ForeignKey('organisations.id', ondelete=SET_NULL),
    )

    user_id = Column(
        Integer,
        ForeignKey('users.id', ondelete=SET_NULL),
    )


class Organisation(Base):
    __tablename__ = 'organisations'
    __table_args__ = {'extend_existing': True}

    id = Column(Integer, primary_key=True, index=True)
    domain = Column(String, unique=True, index=True)
    name = Column(String)

    users = relationship(
        'User',
        secondary='organisations_users',
        back_populates='organisations'
    )
    events = relationship(
        'Event',
        back_populates='organisation'
    )


class User(Base):
    __tablename__ = 'users'
    __table_args__ = {'extend_existing': True}

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


class Event(Base):
    __tablename__ = 'events'
    __table_args__ = {'extend_existing': True}

    id = Column(Integer, primary_key=True, index=True)
    from_date = Column(DateTime)
    to_date = Column(DateTime, nullable=True)
    start_time = Column(Time, nullable=False)
    end_time = Column(Time, nullable=True)
    interval = Column(String, nullable=True)
    organisation_id = Column(Integer, ForeignKey('organisations.id', ondelete=SET_NULL))

    organisation = relationship(
        'Organisation',
        back_populates='events'
    )
    event_sessions = relationship(
        'EventSession',
        back_populates='event'
    )


class EventSession(Base):
    __tablename__ = 'event_sessions'
    __table_args__ = {'extend_existing': True}

    id = Column(Integer, primary_key=True, index=True)
    active = Column(Boolean, default=False)
    event_id = Column(Integer, ForeignKey('events.id', ondelete=SET_NULL))

    event = relationship(
        'Event',
        back_populates='event_sessions'
    )
