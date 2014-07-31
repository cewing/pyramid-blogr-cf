import datetime
from paginate import Page
import sqlalchemy as sa
from sqlalchemy import (
    Column,
    Integer,
    Text,
    Unicode,
    UnicodeText,
    DateTime,
    )
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import (
    scoped_session,
    sessionmaker,
    )
import urllib
from webhelpers2.text import urlify
from webhelpers2.date import time_ago_in_words
from zope.sqlalchemy import ZopeTransactionExtension

DBSession = scoped_session(sessionmaker(extension=ZopeTransactionExtension()))
Base = declarative_base()


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(Unicode(255), unique=True, index=True, nullable=False)
    password = Column(Unicode(255), nullable=False)
    last_logged = Column(DateTime, default=datetime.datetime.utcnow)


class Entry(Base):
    __tablename__ = 'entries'
    id = Column(Integer, primary_key=True)
    title = Column(Unicode(255), unique=True, nullable=False)
    body = Column(UnicodeText, default=u'')
    created = Column(DateTime, default=datetime.datetime.utcnow)
    edited = Column(DateTime, default=datetime.datetime.utcnow)

    @classmethod
    def all(cls):
        return DBSession.query(cls).order_by(sa.desc(cls.created)).all()

    @classmethod
    def by_id(cls, id):
        return DBSession.query(cls).filter(cls.id == id).first()

    @classmethod
    def paginator(cls, request, page=1):
        urlmaker = UrlMaker(request)
        return Page(cls.all(), page, url_maker=urlmaker, items_per_page=10)

    @property
    def slug(self):
        return urlify(self.title)

    @property
    def created_in_words(self):
        return time_ago_in_words(self.created)


class UrlMaker(object):
    """An object that can generate urls for pages in a paginator

    cribbed from webhelpers:

        https://bitbucket.org/bbangert/webhelpers/src/9ad434bec9a16c06c1cfeed38cde02f00a95685d/webhelpers/paginate.py?at=trunk
    """

    def __init__(self, request):
        self.request = request

    def __call__(self, page):
        """Generate a URL for the specified page.
        """
        params = self.request.GET.copy()
        params["page"] = page
        qs = urllib.urlencode(params, True)
        path = self.request.path
        return "%s?%s" % (path, qs)
