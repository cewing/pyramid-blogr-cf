from pyramid.view import view_config


@view_config(route_name='blog', renderer='string')
def blog_view(request):
    return 'View a Blog Record'


@view_config(route_name='blog_action', match_param='action=create',
             renderer='string')
def blog_create(request):
    return 'Create a New Blog Record'


@view_config(route_name='blog_action', match_param='action=edit',
             renderer='string')
def blog_update(request):
    return 'Edit a Blog Record'
