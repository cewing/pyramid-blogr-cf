# Build a Blog With Pyramid

This outline is a brief (3 hour) tutorial on developing web applications with Python.
It has been adapted from the
[Pyramid blogr](http://pyramid-blogr.readthedocs.org/en/latest/)
tutorial which in turn is an adaptation of the
[Flask Tutorial](http://flask.pocoo.org/docs/tutorial/)

This tutorial is intended for use with Python 3.

[previous](https://github.com/cewing/pyramid-blogr-cf/tree/tutorial-step-07) ::
[next](https://github.com/cewing/pyramid-blogr-cf/tree/tutorial-step-09)

## Step 8: Add Authentication

[view the differences](https://github.com/cewing/pyramid-blogr-cf/compare/449f9513...b0c0553e)

We've now locked access to the views that let us create and edit blog records.
This is good, but it means we need to allow a user to log in.
That way, someone will be able to use our application to record their deepest musings on life.

It's time to deal with authentication.

### The Flow

Authentication is the process of proving the identity of a user.
In general, it works by requiring the user to provide credentials.
In many web applications these credentials are a *username* and *password*.
The application accepts a request containing these values.
Then it checks to see if there is a user defined who matches the provided username.
If there is, then it will verify the provided password against the value stored for that user.
If everything goes right, then the user will be considered identified.
The application will then take steps to ensure that the this fact is persisted from one request to another.
That way, the user does not need to provide the credentials

Pyramid will handle that last part on our behalf (and we'll see how shortly).
But the rest is up to us.

#### Finding a User

The first step is to find a user.
Like with our `BlogRecord` class, we'd prefer to delegate interaction with our model to a service.
So we will begin by creating a new service at `services/user.py`.
This service will provide a standard api for retrieving a `User` model instance based on `'name'`.

#### Verifying a Password

Our user has been set up so that it stores an encrypted version of the password.
That encryption is one-way.
We cannot recover the original password.
So we need to add an API to our user that allows us to verify that the plain-text password we get from the request results in the same hash we have stored.
We'll add this to the `User` model itself.
The data is stored there, so it's a logical place for the functionality to be located.

We'll add a method to our `User` model to accomplish this.
It will make use of the `.verify()` method of our password encryption context.
This method applies the same encryption method to the provided plain-text password as was applied to the stored hashed value.
If the result matches the stored value, then the original must be a match for the value provided.
The `context` object is responsible for keeping track of what algorithm was used.


#### Persisting State

Pyramid provides us with a uniform API for handling authenticated state.
We interact with the `remember` and `forget` methods from `pyramid.security`.
These methods are responsible for returning headers for a response suitable for remembering that we are authenticated,
or for forgetting that we were.
But what exactly does that mean?

We don't really need to know.
These methods both delegate to a corresponding method on the *authentication policy* we've configured.
The *policy* is responsible for handling this job.
We can write our own policies, if we need, or we can use one that comes provided by Pyramid.
In our case, we are using the `AuthTktAuthenticationPolicy`, which makes use of a standardized cookie format to securely store authentication data on a users machine.

### Our View

Now that we have the tools we need, we'll write our view.
We'll begin by trying to get a `'username'` from the `POST` data of our request.
If we don't find a value there, then either the form was not properly submitted,
or we arrived in this view via a `GET` request.
Either way, we'll choose to forget any existing authentication.

If a value *is* found, we'll use our new `UserService` to retrieve a `User` object using this name.
If a user is found, *and* that user's password matches the one we find in the `POST` data,
then we will use the `remember` function to build headers that will persist the fact that we've proven our identity.

If any of those conditions fail, we again will forget any existing authentication information.

Finally, we'll redirect the user back to the home page, using the headers that will appropriately update the state of authentication.

### Our Form

We'll avoid requiring a renderer for this view by placing the form for login directly into the index page template.
This gives us a chance to make use of `request.authenticated_userid`.

This attribute is always present on the request object.
If no user has been authenticated, then it will return False.
If a user has been authenticated it will be bound to the user name we `remember`ed.

We can make use of this behavior to make tests in our template.
If a user *is* authenticated, then we will omit the login form.
Instead we them by name and offer a logout button.
If no user is authenticated, we'll show the form.

## Check It Out

You should be able now to start your application:

    (blogr)$ pserve development.ini

Load [the home page](http://localhost:6543/) and attempt to login as the default user created by our `initialize_blogr_db` script.
If login succeeds, you'll see the form disappear, and you'll be able to create new records and edit existing ones.

Play around a bit here:

* See if you can hide the `create entry` link if the user is not logged in.
* Observe what happens if you provide incorrect login values. What might you want to happen instead?
