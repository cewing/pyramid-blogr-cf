import datetime

from blogr.models.meta import Base

from sqlalchemy import (
    Column,
    Integer,
    Unicode,
    DateTime,
)


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    name = Column(Unicode(255), unique=True, nullable=False)
    password = Column(Unicode(255), nullable=False)
    last_logged = Column(DateTime, default=datetime.datetime.utcnow)
