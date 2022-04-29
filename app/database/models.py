from sqlalchemy import (
    Column,
    Integer,
    String,
    ForeignKey,
    DateTime,
    Time,
    Boolean,
    JSON,
)
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

SET_NULL = "SET NULL"  # will this delete the row instance or only set the key to null?


class OrganisationsUsers(Base):
    __tablename__ = 'organisations_users'
    __table_args__ = {'extend_existing': True}

    id = Column(Integer, primary_key=True, index=True)
    status = Column(String)
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
    platforms = relationship(
        'Platform',
        back_populates='organisation'
    )
    notifications = relationship(
        'Notification',
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


class ScheduleTrigger(Base):
    __tablename__ = 'schedule_triggers'
    __table_args__ = {'extend_existing': True}

    id = Column(Integer, primary_key=True, index=True)
    execute_date = Column(DateTime, nullable=False)

    actions = relationship(
        'Action',
        back_populates='schedule_trigger'
    )


class Action(Base):
    __tablename__ = 'actions'
    __table_args__ = {'extend_existing': True}

    id = Column(Integer, primary_key=True, index=True)
    model_name = Column(String)
    model_id = Column(Integer)
    model_method = Column(String)
    model_method_kwargs = Column(JSON)  # will contain the kwargs to the action_method
    schedule_trigger_id = Column(Integer, ForeignKey('schedule_triggers.id', ondelete=SET_NULL), index=True)

    schedule_trigger = relationship(
        'ScheduleTrigger',
        back_populates='actions'
    )


class Platform(Base):
    __tablename__ = 'platform'
    __table_args__ = {'extend_existing': True}

    id = Column(Integer, primary_key=True, index=True)
    api_key = Column(String, nullable=True)
    subdomain = Column(String, nullable=True)
    slug = Column(String, nullable=False, index=True)
    type = Column(String, nullable=False, index=True)

    organisation_id = Column(Integer, ForeignKey('organisations.id', ondelete=SET_NULL), index=True)

    organisation = relationship(
        'Organisation',
        back_populates='platforms'
    )


class Notification(Base):
    __tablename__ = 'notification'
    __table_args__ = {'extend_existing': True}

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)

    organisation_id = Column(Integer, ForeignKey('organisations.id', ondelete=SET_NULL), index=True)

    notification_items = relationship(
        'NotificationItem',
        back_populates='notification'
    )
    organisation = relationship(
        'Organisation',
        back_populates='notifications'
    )


class NotificationItem(Base):
    __tablename__ = 'notification_item'
    __table_args__ = {'extend_existing': True}

    id = Column(Integer, primary_key=True, index=True)
    type = Column(String, nullable=False)
    data = Column(JSON, nullable=False)

    notification_id = Column(Integer, ForeignKey('notification.id', ondelete=SET_NULL), index=True)

    notification = relationship(
        'Notification',
        back_populates='notification_items'
    )

