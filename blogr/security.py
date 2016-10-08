from pyramid.authentication import AuthTktAuthenticationPolicy
from pyramid.authorization import ACLAuthorizationPolicy
from pyramid.security import Allow, Everyone, Authenticated

from .services.user import UserService


def get_user(request):
    username = request.unauthenticated_userid
    if username is not None:
        return UserService.by_name(username, request)


class BlogRecordFactory(object):
    __acl__ = [(Allow, Everyone, 'view'),
               (Allow, Authenticated, 'create'),
               (Allow, Authenticated, 'edit'), ]

    def __init__(self, request):
        pass


def includeme(config):
    authentication_policy = AuthTktAuthenticationPolicy('somesecret')
    authorization_policy = ACLAuthorizationPolicy()
    config.set_authentication_policy(authentication_policy)
    config.set_authorization_policy(authorization_policy)
    config.add_request_method(get_user, 'user', reify=True)
