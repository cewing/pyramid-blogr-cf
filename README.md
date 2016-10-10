# Build a Blog With Pyramid

This outline is a brief (3 hour) tutorial on developing web applications with Python.
It has been adapted from the
[Pyramid blogr](http://pyramid-blogr.readthedocs.org/en/latest/)
tutorial which in turn is an adaptation of the
[Flask Tutorial](http://flask.pocoo.org/docs/tutorial/)

This tutorial is intended for use with Python 3.

[previous](https://github.com/cewing/pyramid-blogr-cf/tree/tutorial-step-05) ::
[next](https://github.com/cewing/pyramid-blogr-cf/tree/tutorial-step-07)

## Step 6: Define the Create and Edit Entry Views

[view the differences](https://github.com/cewing/pyramid-blogr-cf/compare/f4dadf99...54982330)

Now we turn our attention to creating new blog entries, and editing the ones we already have.

### Forms

We begin by building *forms* for each task.
In a web application, a Form class serves to transform Python data into HTML form inputs and values.
It also serves to transform data passed by request back into Python values.
There are many different form libraries available in Python.
In our blog, we will use [WTForms](https://wtforms.readthedocs.io/en/latest/).

We define two form objects in a new Python module, called `forms.py`.
The first is our `BlogCreateForm`, which has fields for the title and body text of a blog record.
Each of our fields must define the type of data it will interact with.
It may also specify other validation operations we want to use to make sure the data received is acceptable.

This first form inherits from the `Form` base class, which provides an API generalized for any form.
Our second form is the `BlogUpdateForm`, which inherits from the first.
When one Form class inherits from another, it inherits all the fields of the first.
Like any other Python class, we can also override those fields in order to change how they behave.
In this case, though, we are only adding a single new field.
Why?

### Create View

Our `blog_create` view callable comes next.

We begin by creating a new intance of our `BlogRecord` object without assigning any values.
We don't yet have to worry about valid values for our object because it is not yet connected to the database.
We then create a *bound* form instance using the `POST` attribute of our request.
On an initial request for this view, which will use a `GET` request, this dictionary will be empty.

If the current request has not been made via the `POST` HTTP method, then we move right on to rendering.
We hand back a Python `dict` containing our bound form and the action we need for building a URL to submit it.
We also update the `@view_config` decorator for this view to use a Jinja2 page template renderer.

If the current request *has* been made via `POST`, then we have some additional work to do.
We can check the form to see if it is valid.
This will invoke type checks for the fields along with any additional validation we specified.

When the form is valid, we use the data from the form to populate our new `BlogRecord` instance.
We can then add our new object to the database session, which is provided to us as an attribute of the request.
That is not a standard feature of Pyramid, which does not require that we build an app using a database.
Instead, we got it from our scaffold back in step 1.
Review `models/__init__.py` to see how that's accomplished.

Once an object is added to a database session, we can stop thinking about it.
By using the `pyramid_tm` add-on package, we have bound our database session to the Request/Response cycle of our application.
A new request will have access to a new database session, with a fresh transaction.
When the handling of the request is complete, just before a response is sent back to the client, that transaction will be committed.
If any error occurs during the handling of a request, then the transaction will be rolled back, undoing any changes that may have been broken by the error.
This transaction management allows us to focus on our application without needing to concern ourselves with data persistence.

Finally, we will use another of the exception classes from `pyramid.httpexceptions` to redirect the user back to the index view.

We also need to create a template for this view.
Because our add and edit forms are substantially similar, we can share a template between them.
Notice that we use the `action` value we passed back from our view to determine whether to render the form's `id` field.
Also notice that in a template we can treat fields as attributes of the form, and access them by name.

We could also rewrite the template to use our form as an iterator.
We could then define a single standard field layout, and repeat it for each field in our form.
Why have we not done so in this case?

### Edit View

The `blog_update` view looks quite similar to the `blog_create` view.

We've seen how we can pass extra data to a view using query parameters and the `_query` argument to `request.route_url()`.
Here in our view, we can see how that plays out.
We can retrieve the `id` passed to us from `request.params`.
This `dict-like` attribute of the request object will contain any key/value pairs set in the `GET` or `POST` dictionaries.
It's useful to get a common pool of both when you have a view that can be reached by either HTTP method.

Once we have the `id` that has been requested, we use our `BlogRecordService` to retrieve the specific record that is wanted.
Again, we take advantage of the `None` return value to send a `404 Not Found` response if it doesn't exist.

Next, we build a *bound* instance of our edit form.
This time, we use not only the `POST` data from our request, but also the entry we retrieved from the database.
On a `GET` requet, our form will be populated by the values already in the database.

On a `POST` request, if the form is valid, then we overwrite the values on the object with those that were passed to us when the form was submitted.
Notice that we **do not** add this record to the current database session.
That's because when we used the service to retrieve this record from the database, the record object was already added to the session.
Any values we updated will be marked as *dirty*,
and the SQLAlchemy ORM will take care of the rest.
It will issue a proper `UPDATE` query when the transaction is committed at the end of the Request/Response cycle.

Again, we redirect the user elsewhere after we're done editing.
But as one might expect, we send them back to the view of the entry the just updated.
That way, they will be able to see the changes they made.
Notice the use of `request.route_url` here.
In pyramid, this is always the method used to produce application urls, whether in template code or view code.

Take another look at the page template we used for the create view.
We use the same one for this view.
What adjustments do we make in the template for it's use with either view?