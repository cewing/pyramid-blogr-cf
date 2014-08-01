from jinja2 import Markup
import markdown

from pyramid.httpexceptions import HTTPNotFound, HTTPFound
from pyramid.view import view_config
from pyramid.security import (
    authenticated_userid,
    forget,
    remember,
    )

from .forms import (
    BlogCreateForm,
    BlogUpdateForm,
    LoginForm,
    )
from .models import (
    DBSession,
    User,
    Entry,
    )


@view_config(route_name='home', renderer='blogr:templates/index.jinja2')
def index_page(request):
    page = int(request.params.get('page', 1))
    paginator = Entry.paginator(request, page)
    form = None
    if not authenticated_userid(request):
        form = LoginForm()
    return {'paginator': paginator, 'login_form': form}


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
    import pdb; pdb.set_trace()
    login_form = None
    if request.method == 'POST':
        login_form = LoginForm(request.POST)

    if login_form and login_form.validate():
        user = User.by_name(login_form.username.data)
        if user and user.verify_password(login_form.password.data):
            headers = remember(request, user.name)
        else:
            headers = forget(request)
    else:
        headers = forget(request)
    return HTTPFound(location=request.route_url('home'),
                     headers=headers)


# Jinja2 markdown filter
def render_markdown(content, linenums=False, pygments_style='default'):
    ext = "codehilite(linenums={linenums}, pygments_style={pygments_style})"
    import pdb; pdb.set_trace()
    output = Markup(
        markdown.markdown(
            content,
            extensions=[ext.format(**locals()), 'fenced_code'])
    )
    return output
