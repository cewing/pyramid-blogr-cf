from pyramid.httpexceptions import (
    HTTPNotFound,
    HTTPFound,
    )
from pyramid.view import view_config

from .forms import (
    BlogCreateForm,
    BlogUpdateForm,
    )
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
             renderer='blogr:templates/edit_blog.jinja2',
             permission='create')
def blog_create(request):
    entry = Entry()
    form = BlogCreateForm(request.POST)
    if request.method == 'POST' and form.validate():
        form.populate_obj(entry)
        DBSession.add(entry)
        return HTTPFound(location=request.route_url('home'))
    return {'form': form, 'action': request.matchdict.get('action')}


@view_config(route_name='blog_action', match_param='action=edit',
             renderer='blogr:templates/edit_blog.jinja2',
             permission='edit')
def blog_update(request):
    id = int(request.params.get('id', -1))
    entry = Entry.by_id(id)
    if not entry:
        return HTTPNotFound()
    form = BlogUpdateForm(request.POST, entry)
    if request.method == 'POST' and form.validate():
        form.populate_obj(entry)
        return HTTPFound(
            location=request.route_url('blog', id=entry.id, slug=entry.slug)
        )
    return {'form': form, 'action': request.matchdict.get('action')}


@view_config(route_name='auth', match_param='action=in', renderer='string',
             request_method='POST')
@view_config(route_name='auth', match_param='action=out', renderer='string')
def sign_in_out(request):
    return {}
