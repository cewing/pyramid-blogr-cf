from pyramid.view import view_config


@view_config(route_name='home', renderer='string')
def index_page(request):
    return 'Index Page'


@view_config(route_name='auth', match_param='action=in', renderer='string',
             request_method='POST')
@view_config(route_name='auth', match_param='action=out', renderer='string')
def sign_in_out(request):
    return 'Sign In or Out'
