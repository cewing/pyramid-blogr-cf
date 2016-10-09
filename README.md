# Build a Blog With Pyramid

This outline is a brief (3 hour) tutorial on developing web applications with Python.
It has been adapted from the
[Pyramid blogr](http://pyramid-blogr.readthedocs.org/en/latest/)
tutorial which in turn is an adaptation of the
[Flask Tutorial](http://flask.pocoo.org/docs/tutorial/)

This tutorial is intended for use with Python 3.

[previous](https://github.com/cewing/pyramid-blogr-cf/tree/tutorial-step-01) ::
[next](https://github.com/cewing/pyramid-blogr-cf/tree/tutorial-step-03)

## Step 2: Define the Data Model

[view the differences](https://github.com/cewing/pyramid-blogr-cf/compare/253c4d95...83daf6d1)

First, we delete the sample model created by our starter scaffold.

Then we set up our User and BlogRecord models, using the
[declarative](http://docs.sqlalchemy.org/en/latest/orm/extensions/declarative/) style of the
[SQLAlchemy ORM](http://docs.sqlalchemy.org/en/latest/orm/tutorial.html)

We'll also need to update the script used to initialize our database.
We can set it up now to create an initial `admin` user for our blog.
We also update the code in the default home from our scaffold so that it will work with our new database.

Notice that from the start we initialize the admin user with a password that is encrypted.
We use the [passlib](http://pythonhosted.org/passlib/) package we added as a dependency to create a password context.
This unique object will control encrypting user passwords, and verifying that passwords supplied at login match
the encrypted values we store for our user.
We must never use plain-text passwords in a web application.

We can now initialize a database by running the script:

    (blogr)$ initialize_blogr_db development.ini

That will create a sqlite3 database, so we need to update our `.gitignore` file to prevent adding it
to our repostiory.

Once that is done, we can start the blog running, using the `pserve` command:

    (blogr)$ pserve development.ini

And we can visit the homepage of our new blog by loading [http://localhost:6543](http://localhost:6543) in our web browser.

That's great, but a blog should have more than just a home page.
And even our home page should do something a bit more interesting.
We'll begin working on this problem [in step three](https://github.com/cewing/pyramid-blogr-cf/tree/tutorial-step-03)

