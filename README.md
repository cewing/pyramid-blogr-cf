# Build a Blog With Pyramid

This outline is a brief (3 hour) tutorial on developing web applications with Python.
It has been adapted from the
[Pyramid blogr](http://pyramid-blogr.readthedocs.org/en/latest/)
tutorial which in turn is an adaptation of the
[Flask Tutorial](http://flask.pocoo.org/docs/tutorial/)

This tutorial is intended for use with Python 3.

[previous](https://github.com/cewing/pyramid-blogr-cf/tree/tutorial-step-04) ::
[next](https://github.com/cewing/pyramid-blogr-cf/tree/tutorial-step-06)

## Step 5: Define the Home Page and Single Entry Views

[view the differences](https://github.com/cewing/pyramid-blogr-cf/compare/b3e0bd85...f4dadf99)

Now that we've established routes, and stub views that prove that they are wired correctly, we are ready to implement our first real views.
We'll begin with a home page which shows all blog posts in chronological order, with the most recent first.

### Service

Before we work on the view though, we'll build a `BlogRecordService` class which allows us to encapsulate all the interactions we require with a BlogRecord into a single, clear API.
The advantage of this approach is that it allows us to write our views using this API, and later, if we change our models, we need not change the view code.
The extra layer of abstraction insulates us against changes in the data model.

We'll add a `.all()` class method which will return all the blog records in our database in the correct order.
This method (and others on this service class) will make use of the [SQLAlchemy Query API](http://docs.sqlalchemy.org/en/latest/orm/query.html) to interact with the database.

Our `.by_id()` class method returns a specific blog record object, based on the ID passed as an argument.
The `.get()` query API method used here will either return us the object we seek or the Python `None` type-object if it doesn't exist.
We'll defer handling that case until in our view.

The `.get_paginator()` method uses the [paginate_sqlalchemy](https://github.com/Pylons/paginate_sqlalchemy) add-on to allow us to return a subset of `BlogRecord` objects based on a page number.
You can determine how many items you wish to display per page.

### Index Page

Once our service class is complete, we can write the code for our `index_page` view callable.
We'll return a `paginator` object which acts  as an iterable.
It will provide us with access to each entry in a given page of entries.
Having the service in place makes this view code quite compact.

Before we create a template to display the data we've returned from that view, we'll add a property
on our `BlogRecord` class which provides a `slugified` version of the title of the record.
This method makes use of another add-on, [webhelpers2](http://webhelpers2.readthedocs.io/en/latest/).
The `slug` for our record will be used to build a link to the view of each record in our index page template.

The page template for our index view comes next.
A page template allows us to render data into HTML suitable for display in a user's browser.
We'll add a template that loops through the records in our paginator object and renders each one, along with a link to the view of that one record.

We render that link using the `.route_url()` method present on the `request` object.
This process is called *reversing* URLs, and it keeps our templates decoupled from details like the specific path patterns needed for links we want to create.
Notice how we are using the `id` and `slug` of our blog records as arguments to personalize each link.
Replacement markers we have defined in our route pattern will be present as keyword arguments to this method.
The values we pass will be used in the appropriate places in the URLs that this method returns.

Also notice that the template we've created makes use of [template inheritance](http://jinja.pocoo.org/docs/dev/templates/#template-inheritance).
We'll put our template into the content slot defined by the `layout` template we were provided by our scaffold.
We could also re-write that layout to make our site look different, but we'll skip that for today.

Thanks to the [pyramid_jinja2](http://docs.pylonsproject.org/projects/pyramid_jinja2/en/latest/) add-on, we are able to use Jinja2 page templates as *renderers* for our views.
So we'll finish this work by updating the `@view_config` decorator for the `index_page` view callable to use our new template.


### Blog Page

In order to view a single blog entry, we'll need access to the ID that was sent to us in the URL path.
Remember that the values matched by replacement patterns in our routes are added to an attribute of our request called the `matchdict`.
This attribute functions like a Python `dict`, so we can use typical Python approaches to safely access the `'id'` key we expect to be present.

Once we have hold of the id, we use the `.by_id()` method of our `BlogRecordService` to get the record we want to view.
Remember that if that method is passed an ID that does not correspond to a record in our database, it will return None.
Here in the view callable, we take advantage of that detail to return a `404 Not Found` response.
The [pyramid.httpexceptions](http://docs.pylonsproject.org/projects/pyramid/en/latest/api/httpexceptions.html)
module gives us access to all sorts of exception objects that can be returned directly from views as response values.

Next, we add a page template to display our blog record.
We can build links from this page to our `blog_action` view using the same `request.route_url()` method from above.
We use the `action` replacement pattern name to indicate that we want the `edit` action.
This will allow users to click a link to edit the record they are seeing.
Thanks to predicate arguments, our `blog_update` view will be invoked when we click this link.

Notice how we are indicating *which* record we want to edit.
The `request.route_url()` method allows us to pass additional key/value pairs.
These will be appended to the generated URL as *query parameters*:

    http://my.domain.com/blog/edit?id=42
