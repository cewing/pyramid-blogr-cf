from pyramid.httpexceptions import HTTPNotFound
from pyramid.view import view_config

from .models import (
    DBSession,
    Entry,
    )


@view_config(route_name='home', renderer='blogr:templates/index.jinja2')
def index_page(request):
    page = int(request.params.get('page', 1))
    paginator = Entry.paginator(request, page)
    return {'paginator': paginator}


@view_config(route_name='blog', renderer='blogr:templates/view_blog.jinja2')
def blog_view(request):
    id = int(request.matchdict.get('id', -1))
    entry = Entry.by_id(id)
    if not entry:
        return HTTPNotFound()
    return {'entry': entry}


@view_config(route_name='blog_action', match_param='action=create',
             renderer='blogr:templates/edit_blog.jinja2')
def blog_create(request):
    return {}


@view_config(route_name='blog_action', match_param='action=edit',
             renderer='blogr:templates/edit_blog.jinja2')
def blog_update(request):
    return {}


@view_config(route_name='auth', match_param='action=in', renderer='string',
             request_method='POST')
@view_config(route_name='auth', match_param='action=out', renderer='string')
def sign_in_out(request):
    return {}
