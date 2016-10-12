# Build a Blog With Pyramid

This outline is a brief (3 hour) tutorial on developing web applications with Python.
It has been adapted from the
[Pyramid blogr](http://pyramid-blogr.readthedocs.org/en/latest/)
tutorial which in turn is an adaptation of the
[Flask Tutorial](http://flask.pocoo.org/docs/tutorial/)

This tutorial is intended for use with Python 3.

[previous](https://github.com/cewing/pyramid-blogr-cf/tree/tutorial-step-08) ::
[next](https://github.com/cewing/pyramid-blogr-cf/tree/tutorial-step-10)

## Step 9: Add Registration

[view the differences](https://github.com/cewing/pyramid-blogr-cf/compare/b0c0553e...c75b3031)

We can allow users to log in to our app now, and create and edit entries,
but we only have the one user.
Let's add the ability to register for an account.

We'll start by making a form for registration.
This lets us use the `PasswordField` which will mask the users input when typing a password.
We'll also build a template to render this form.

Next, we'll add an API to our user allowing us to hash a password value when setting it.
It again uses the `passlib` password ecryption context, to ensure that all passwords are treated the same.
This will help us avoid forgetting to encrypt a value when creating a new user.

With this all in place, we can focus on the view itself.
We bind an instance of our `RegistrationForm` to the `POST` data from our request.
If the request was a `POST` request and the form validates, we'll move on.
We create a new user with the provided username.
Then we use our `.set_password()` API to encrypt the password that came in on the form.
We need to `.add()` this new `User` instance to our database session and then redirect back to the home page.
The transaction management of `pyramid_tm` will ensure that this new user is inserted to the database when a response is returned.

For any `GET` requests, or if the form fails to validate, we'll hand back the bound form for rendering by the template.

Our final step is to add a new *route* for this view.
We can then add a link to the register view in our index page, just near the login form.

## Check It Out

Start your application:

    (blogr)$ pserve development.ini

Visit [the home page](http://localhost:6543/) and make sure you log out as "admin".

Click on the "register" link and sign up as a different user.

Then log in as this user and verify that you, too, can add and edit posts.

You might wish to:

* Add a `password_duplicate` field to the `RegistrationForm` to help make sure the user has typed their password correctly.
  Make sure that you verify the two password values match.
* Update your `initialize_blogr_db` script to use the new `User.set_password` API.
