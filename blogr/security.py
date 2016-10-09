from pyramid.authentication import AuthTktAuthenticationPolicy
from pyramid.authorization import ACLAuthorizationPolicy
from pyramid.security import Allow, Everyone, Authenticated

from .services.user import UserService
from .services.blog_record import BlogRecordService


def get_user(request):
    username = request.unauthenticated_userid
    if username is not None:
        return UserService.by_name(username, request)


class BlogRecordFactory(object):

    def __acl__(self):
        acl = [(Allow, Everyone, 'view'),
               (Allow, Authenticated, 'create'), ]
        if BlogRecordService.allow_editing(self.request):
            acl.append((Allow, self.request.authenticated_userid, 'edit'))
        return acl

    def __init__(self, request):
        self.request = request


def includeme(config):
    authentication_policy = AuthTktAuthenticationPolicy('somesecret')
    authorization_policy = ACLAuthorizationPolicy()
    config.set_authentication_policy(authentication_policy)
    config.set_authorization_policy(authorization_policy)
    config.add_request_method(get_user, 'user', reify=True)
