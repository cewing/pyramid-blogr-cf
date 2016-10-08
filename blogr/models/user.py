import datetime

from blogr import context
from blogr.models.meta import Base

from sqlalchemy import (
    Column,
    Integer,
    Unicode,
    DateTime,
)
from sqlalchemy.orm import relationship


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    name = Column(Unicode(255), unique=True, nullable=False)
    password = Column(Unicode(255), nullable=False)
    last_logged = Column(DateTime, default=datetime.datetime.utcnow)

    posts = relationship("BlogRecord", back_populates="author")

    def verify_password(self, password):
        return context.verify(password, self.password)

    def set_password(self, password):
        hashed = context.encrypt(password)
        self.password = hashed
