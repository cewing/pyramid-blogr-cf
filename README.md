# Build a Blog With Pyramid

This outline is a brief (3 hour) tutorial on developing web applications with Python.
It has been adapted from the
[Pyramid blogr](http://pyramid-blogr.readthedocs.org/en/latest/)
tutorial which in turn is an adaptation of the
[Flask Tutorial](http://flask.pocoo.org/docs/tutorial/)

This tutorial is intended for use with Python 3.

## Set Up Your Environment

This tutorial requires some environmental set up.

You'll need:

* A Python 3.5 interpreter
* A virtual environment built with that interpreter
* The Pyramid framework installed
* The Git version control system.

To accomplish this, please follow [the instructions here](http://docs.pylonsproject.org/projects/pyramid/en/latest/quick_tutorial/requirements.html) to set up your environment.

Make one change, please.  Instead of creating a `quick_tutorial` directory to hold your work, call the directory `blogr_tutorial`.

    $ cd ~
    $ mkdir -p projects/blogr_tutorial
    $ cd projects/blogr_tutorial

After you've created your virtual environment and installed the Pyramid package, you'll want to clone the tutorial repository:

    $ git clone https://github.com/cewing/pyramid-blogr-cf.git
    $ cd pyramid-blogr-cf
    $ git checkout tutorial-step-00

At this point, you'll have an empty repository in the `~/projects/blogr_tutorial/pyramid-blogr-cf` directory.

For each step below, you'll check out the corresponding branch.

## Tutorial Steps

### Step 1: Get Started

    $ git checkout tutorial-step-01

In this step we will use the `pcreate` command provided by Pyramid to create a project skeleton.
We'll set up a basic project using [SQLAlchemy](http://www.sqlalchemy.org/) to store data in a
relational database and [Jinja2](http://jinja.pocoo.org/) to create templates.
We'll also add a few dependencies for our project that will come in handy later.
Finally, we'll create a `.gitignore` file to help keep our repository clean.

[view this step](https://github.com/cewing/pyramid-blogr-cf/tree/tutorial-step-01)

### Step 2: Define the Data Model

    $ git checkout tutorial-step-02

In this step, we will create our data models.
We'll add a `User` class to represent a registered user of our blog
and a `BlogRecord` class to represent an entry in the blog.

We'll also update the database initialization script that `pcreate` gave so that
it creates a default `admin` user for our blog.
We'll use the [passlib](http://pythonhosted.org/passlib/) package to ensure that our user's password
is stored securely.

Finally we will update the existing home page view so that it will work with our new data models.

[view this step](https://github.com/cewing/pyramid-blogr-cf/tree/tutorial-step-02)

### Step 3: Add Routes

    $ git checkout tutorial-step-03

In this step, we will add [routes](http://docs.pylonsproject.org/projects/pyramid/en/latest/narr/urldispatch.html)
for our blogs basic functionality.
Routes represent the available pages, or *endpoints* in our blog.
We will use route `patterns` to capture variable data in a URL for use inside our blog *views*

[view this step](https://github.com/cewing/pyramid-blogr-cf/tree/tutorial-step-03)

### Step 4: Add Stub Views

    $ git checkout tutorial-step-04

In this step, we create simple [views](http://docs.pylonsproject.org/projects/pyramid/en/latest/narr/views.html)
for each of the *routes* we have already added.
We'll see how view configuration allows us to use different criteria to connect a *route* to a *view*.
We'll also see how we can use a simple [renderer](http://docs.pylonsproject.org/projects/pyramid/en/latest/narr/renderers.html)
like `'string'` to return a basic response to a visitor viewing our blog.

[view this step](https://github.com/cewing/pyramid-blogr-cf/tree/tutorial-step-04)

### Step 5: Define the Home Page and Single Entry Views

    $ git checkout tutorial-step-05

In this step, we establish a list view and a single entry view for our blog.
We'll create a blog *service*, which provides an interface for interacting with our BlogRecord model.
We will also create a few API methods on the BlogRecord model itself.
These will allow us to get information about each BlogRecord in a way that is useful for templates and routes.

We will then use the new service to fetch all the blog entries for our list view,
or to fetch one entry for the single entry view.
We'll use the Jinja2 *renderer* provided by the [pyramid_jinja2](http://docs.pylonsproject.org/projects/pyramid_jinja2/en/latest/)
package to set up page templates to display the data returned by our new views.
We'll also see how we can use template inheritance to share common structure among many different pages in our blog.

[view this step](https://github.com/cewing/pyramid-blogr-cf/tree/tutorial-step-05)

### Step 6: Define the Create and Edit Entry Views

    $ git checkout tutorial-step-06

In this step, we'll implement the code for the views which allow us to create new entries and edit
existing entries.
We'll learn how to use the [WTForms](https://wtforms.readthedocs.io/en/latest/) package to build
form classes that can be used to render forms in page templates, to validate incoming data, and
to populate attributes of our models using that incoming data.

[view this step](https://github.com/cewing/pyramid-blogr-cf/tree/tutorial-step-06)

### Step 7: Add Authorization

    $ git checkout tutorial-step-07

In this step, we will begin to protect our blog against unwelcome intruders.
We'll learn how to configure both *authorization* and *authentication*, the two halves of Pyramid's
[security](http://docs.pylonsproject.org/projects/pyramid/en/latest/narr/security.html) system.

Then we'll implement an *authorization* system based on an [Access Control List](https://en.wikipedia.org/wiki/Access_control_list).
We'll see how we can control who can reach a give *view* by setting permissions in view configuration.
And we'll see how to use a customized `root factory` to provide a specific ACL for our blog.

[view this step](https://github.com/cewing/pyramid-blogr-cf/tree/tutorial-step-07)

### Step 8: Add Authentication

    $ git checkout tutorial-step-08

In this step, we'll implement *authentication* to go along with our *authorization*.
We'll see how Pyramid uses a shared API to delegate responsiblity for authorizing a user to
the *Authentication Policy* we configured in the previous step.
We'll make use of this API in implementing a login/logout view.

Along the way, we'll need to implement a service for users, to allow us to get a user by username.
We'll also put an API on our user that allow us to verify that a provided password matches the
hashed version stored for a user.

[view this step](https://github.com/cewing/pyramid-blogr-cf/tree/tutorial-step-08)

### Step 9: Add Registration

    $ git checkout tutorial-step-09

In this step, we'll allow new users to register with our blog.
We'll create a new form class to validate registration data, and add a new *route* and a link to it
that is visible when an anonymous user is viewing our blog home page.
We'll add an API that allows us to set an encrypted password on a user and use that in implementing
a registration view so that we never store a plain text password in our database.

[view this step](https://github.com/cewing/pyramid-blogr-cf/tree/tutorial-step-09)

### Step 10: Add Dynamic Permissions

    $ git checkout tutorial-step-10

In this step, we'll extend the data model for our blog a bit, building a relationship between
users and the blog entries that they write.
We'll take advantage of a feature of Pyramid to provide direct access to the authenticated user on
incoming requests.
Having that ability will allow us to automatically assign newly created blog entries to the user
who wrote them.

With this in place, we will update our *root factory* to dynamically assign the edit permission
only to the author of a particular post.
This means that we can allow *all* users to create new posts, while preventing them from editing
posts they did not write themselves.

[view this step](https://github.com/cewing/pyramid-blogr-cf/tree/tutorial-step-10)