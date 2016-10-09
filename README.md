# Build a Blog With Pyramid

This outline is a brief (3 hour) tutorial on developing web applications with Python.
It has been adapted from the
[Pyramid blogr](http://pyramid-blogr.readthedocs.org/en/latest/)
tutorial which in turn is an adaptation of the
[Flask Tutorial](http://flask.pocoo.org/docs/tutorial/)

This tutorial is intended for use with Python 3.

[previous](https://github.com/cewing/pyramid-blogr-cf/tree/tutorial-step-03) ::
[next](https://github.com/cewing/pyramid-blogr-cf/tree/tutorial-step-05)

## Step 4: Add Stub Views

[view the differences](https://github.com/cewing/pyramid-blogr-cf/compare/04623c80...b3e0bd85)

Now that we've established *routes* as a way of matching incoming requests, we need to build
[views](http://docs.pylonsproject.org/projects/pyramid/en/latest/narr/views.html) to build responses.
Views in Pyramid are *callable objects* (functions, class methods, or callable classes) which must take `request` as a positional argument.
They can return responses directly, or more commonly they will return a Python `dict` which is passed to a
[renderer](http://docs.pylonsproject.org/projects/pyramid/en/latest/narr/renderers.html).
The *renderer* is then responsible for building a response using the data provided by the view callable.

But before we concern ourselves with building specific views we should check to make sure that everything is configured correctly.
To that end, we'll begin by putting a *stub view* in place for each real view we will eventually create.
This will allow us to focus configuring the connections from routes to views without worrying about exactly what the view will do yet.

[View configuration](http://docs.pylonsproject.org/projects/pyramid/en/latest/narr/viewconfig.html) in Pyramid
can be handled either imperatively, in our application configuration, or declaratively, using the
[@view_config decorator](http://docs.pylonsproject.org/projects/pyramid/en/latest/narr/viewconfig.html#mapping-views-using-a-decorator-section).
We'll choose this latter approach.

We'll begin by removing the view that was created for us by the *alchemy* scaffold.
We'll replace that with an `index_view` which returns a simple string describing what the view is.

Notice that the `route_name` argument to the `@view_config` decorator.
This argument is used to associate one or more view callables with the routes we registred in the previous step.
It is an error to use a `route_name` that has not been registered.

A second argument to this virst view configuration is the `renderer`.
We will configure this view to use the `'string'` renderer, which comes built in to Pyramid.
This will take the string returned by our stub view and convert it to a Python `str` object.
That string will be returned as the body of an HTTP response with the content type `text/plain`.

We'll also create a new view function called `sign_in_out`.
Notice that there are *two* `@view_config` decorators on this function.
Each makes use of a new argument to the decorator, `match_param`.
The value of this argument must be a string which contains a "key=value" pair.
The key must be a replacement marker used in the named route.
The value will be used as a test.
If the value of that specific replacement marker in an incoming request path matches the configured value, then this view callable will be used.
If it does not, then some other view callable might be matched (or non at all, which results in `404 Not Found`).

This `match_param` argument is an example of a
[predicate argument](http://docs.pylonsproject.org/projects/pyramid/en/latest/narr/viewconfig.html#predicate-arguments) to the `@view_config` decorator.
Predicates allow Pyramid to choose the *correct* view callable from a number of callables that might be associated with a given route.

Another predicate argument `request_method` is used for one of the two decorators for this view callable.
This ensures that requests to `/sign/in` will only be matched if the request uses the `POST` HTTP method.

Once we've configured these views, we should be able to visit any of these endpoints to see the results.
Start up your Pyramid server to try this out:

    (blogr)$ pserve development.ini

Once it is running, you should be able click any of the following links and see the expected results:

* [http://localhost:6543/](http://localhost:6543/) => "Index Page"
* [http://localhost:6543/blog/1/some-slug](http://localhost:6543/blog/1/some-slug) => "View a Blog Record"
* [http://localhost:6543/blog/create](http://localhost:6543/blog/create) => "Create a New Blog Record"
* [http://localhost:6543/blog/edit](http://localhost:6543/blog/edit) => "Edit a Blog Record"
* [http://localhost:6543/sign/in](http://localhost:6543/sign/in) => "Sign In or Out"

Here are some things you might experiment with at this stage:

* Try to update the `blog_view` to return a string that tells a visitor *which* blog record is being viewed
* Try to update the `sign_in_out` view to return a string that says which action was passed in the URL
* Investigate other attributes of the [Pyramid request](http://docs.pylonsproject.org/projects/pyramid/en/latest/api/request.html),
  come up with a way of telling the `blog_update` view which entry should be updated,
  can you make this appear in the string returned by the view callable?

[In step 5](https://github.com/cewing/pyramid-blogr-cf/tree/tutorial-step-05) we'll start implementing some of these views.
