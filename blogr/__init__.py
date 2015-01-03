import os
from pyramid.authentication import AuthTktAuthenticationPolicy
from pyramid.authorization import ACLAuthorizationPolicy
from pyramid.config import Configurator
from sqlalchemy import engine_from_config
from .models import (
    DBSession,
    Base,
    )
from .security import EntryFactory


def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    if 'DATABASE_URL' in os.environ:
        settings['sqlalchemy.url'] = os.environ['DATABASE_URL']
    engine = engine_from_config(settings, 'sqlalchemy.')
    DBSession.configure(bind=engine)
    authentication_policy = AuthTktAuthenticationPolicy('somesecret')
    authorization_policy = ACLAuthorizationPolicy()
    config = Configurator(
        settings=settings,
        authentication_policy=authentication_policy,
        authorization_policy=authorization_policy
    )
    config.include('pyramid_jinja2')
    config.add_static_view('static', 'static', cache_max_age=3600)
    config.add_route('home', '/')
    config.add_route('blog', '/blog/{id:\d+}/{slug}')
    config.add_route(
        'blog_action',
        '/blog/{action}',
        factory='blogr.security.EntryFactory'
    )
    config.add_route('auth', '/sign/{action}')
    config.scan()
    return config.make_wsgi_app()
