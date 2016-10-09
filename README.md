# Build a Blog With Pyramid

This outline is a brief (3 hour) tutorial on developing web applications with Python.
It has been adapted from the
[Pyramid blogr](http://pyramid-blogr.readthedocs.org/en/latest/)
tutorial which in turn is an adaptation of the
[Flask Tutorial](http://flask.pocoo.org/docs/tutorial/)

This tutorial is intended for use with Python 3.

[previous](https://github.com/cewing/pyramid-blogr-cf/tree/tutorial-step-02) ::
[next](https://github.com/cewing/pyramid-blogr-cf/tree/tutorial-step-04)

## Step 3: Add Routes

[view the differences](https://github.com/cewing/pyramid-blogr-cf/compare/83daf6d1...04623c80)

For every web application, one of the first questions we face is how the request made by a visitor
will be matched to the code that will build a response.
In Pyramid, this question can be answered in a number of different ways.
Our blog app will use an approach called
[URL Dispatch](http://docs.pylonsproject.org/projects/pyramid/en/latest/narr/urldispatch.html).
In this approach, the **path** of an incoming request is matched against a series of registered *patterns*.
When a pattern matches, it is used to find the right code to run.

    |    http://my.domain.com/path/to/desired/resource     |
    | http://  | my.domain.com | /path/to/desired/resource |
    | protocol |    domain     |           path            |

In Pyramid, these patterns are registered in configuration using `routes`.
The patterns in our routes make use of [replacement markers](http://docs.pylonsproject.org/projects/pyramid/en/latest/narr/urldispatch.html#route-pattern-syntax), in the form of `{name}`.
Replacement markers match against segments of the request URL.
The values in the path segments they match will be passed on as part of the request object,
the [matchdict](http://docs.pylonsproject.org/projects/pyramid/en/latest/narr/urldispatch.html#the-matchdict)
In this way, we can handle dynamic data passed via the URL path of the request.

We will add three new routes to our blog application.

The first, named `'blog'`, contains two replacement markers, matching a numeric *id* and a *slug*.
We will use these values to find a specific blog entry to display.
The `\d+` portion of the *id* replacement marker ensures we will only match paths with one or more digits in that part of the path.
An incoming request with a path like

    /blog/24/a-post-about-a-cheese-shop

would match this route.
The value `'24'` would become the *id* and the value `'a-post-about-a-cheese-shop'` would become the *slug*

The second, named `'blog_action'`, contains only one replacement marker, *action*.
This value will determine what action we want to take for our blog.
We might use this to match a request with a path like

    '/blog/create'

or

    '/blog/edit'


The third, named `'auth'` also contains an *action* replacement marker.
In this case, the value matched will determine which authentication action should be taken.
This pattern would match requests like

    '/sign/in'

or

    '/sign/out'

If none of the routes in our application are matched by an incoming request, then Pyramid will automatically generate a `404 Not Found` response.

The purpose of routes in Pyramid is to match incoming requests and find the right code to generate a response.
[In the next step](https://github.com/cewing/pyramid-blogr-cf/tree/tutorial-step-04),
we'll see how this connection is handled.