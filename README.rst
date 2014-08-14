===============================
Intro to Python Web Development
===============================

This outline is a brief (3 hour) tutorial on developing web applications with
Python. It has been adapted from the
`pyramid blogr <http://pyramid-blogr.readthedocs.org/en/latest/>`_
tutorial which in turn is an adaptation of the
`Flask Tutorial <http://flask.pocoo.org/docs/tutorial/>`_.

This tutorial is compatible with Python versions 2.7 and later.

.. contents:: :local:

Set Up Your Environment
===========================

Get Python
--------------

To follow along with this tutorial you will need a computer with Python
installed. In most cases, this will automatically be true.  You can check by
running the following command in a command-line terminal::

    $ which python
    /usr/bin/python

If the `which` shell command returns a path, then you have Python on your
computer.  If no value is printed, then you do not.  You will need to install
python either using one of the installers from
`the python website <https://www.python.org>`_, or using your system's package
manager (`apt-get`, `yum`, `rpm`, etc.).

There are several versions of Python available.  You will need to have either
version 2.7.x (the latest in the Python 2 series) or version 3.3 or later (in
the Python 3 series). You can check which version of Python you have with this
command::

    $ python -V
    Python 2.7.5

Make sure that your version is appropriate.

Get a Python Package Installer
----------------------------------

In order to install new Python libraries and packages into your system, you
must have a package installer.  The most popular of these is `pip
<http://pip.readthedocs.org/en/latest/installing.html>`_. You can check if your
Python installation already has pip by running the following command at your
command-line::

    $ which pip
    /usr/local/bin/pip

If you already have a version of `pip` installed, please **skip to the next
section**.

If you do not have `pip` installed, you can install it by running the pip
bootstrap script::

    $ cd
    $ mkdir installers
    $ cd installers
    $ curl -O https://bootstrap.pypa.io/get-pip.py
    $ sudo python get-pip.py

That will install `pip` after which you should be able to use it to install and
upgrade Python add-ons.  Begin by upgrading pip itself::

    $ sudo pip install -U pip

The most recent version when this documentation was written is 1.5.6

Create A Sandbox
------------------

We will use a tool called `virtualenv <http://virtualenv.readthedocs.org>`_ to
create a Python sandbox in which to work.

Begin by installing the package using `pip`::

    $ sudo pip install virtualenv

* You will likely need to use `sudo` to install the virtualenv package in your
  system Python.

After `virtualenv` is installed, you'll want to create a project folder in
which to work::

    $ cd </path/to-your/projects/directory>
    $ mkdir python-tutorial
    $ cd python-tutorial

* It's not important where you create this directory, only that you have it in
  a place where you can find it again.

Next, you'll create a new Python sandbox in your project folder::

    $ virtualenv blogr
    New python executable in blogr/bin/python
    Installing setuptools, pip...done.

At this point, you will have a new folder called `blogr`::

    $ ls
    blogr

You can activate this sandbox using the `activate` script it contains::

    $ source blogr/bin/activate
    (blogr)$ which python
    /path/to/python-tutorial/blogr/bin/python

* Notice that when activated, virtualenv enhances your terminal prompt, letting
  you know that it's working.
* Notice also that when activated, virtualenv redirects the `python` command so
  that you are using the Python inside the sandbox.

When you are done working, you can deactivate the sandbox with the `deactivate`
command::

    (blogr)$ deactivate
    $ which python
    /usr/bin/python

Get the Tutorial Code
-------------------------

Your final step in preparing your environment for this tutorial is to clone
this project repository from github::

    $ pwd
    /path/to/python-tutorial
    $ git clone https://github.com/cewing/pyramid-blogr-cf.git
    ...
    Checking connectivity... done.
    $ ls
    blogr
    pyramid-blogr-cf

This tutorial is formatted as a set of commits on the `tutorial_walkthrough`
branch of this repository. Each commit makes a few changes that add
functionality to the application. To follow along with the tutorial, you'll
begin by checking out the `tutorial_walkthrough` branch::

    $ cd /path/to/python-tutorial/pyramid-blogr-cf
    $ git branch -a
    * master
      remotes/origin/HEAD -> origin/master
      remotes/origin/master
      remotes/origin/tutorial_walkthrough
     git checkout tutorial_walkthrough
    Branch tutorial_walkthrough set up to track remote branch tutorial_walkthrough from origin.
    Switched to a new branch 'tutorial_walkthrough'
    $ git branch
      master
    * tutorial_walkthrough

The commit log will show you the steps in the tutorial (and the commit hashes
are listed below). For each step, you'll checkout a successive commit and we'll
discuss the code changes made: the purpose of the changes, how the code works,
and what Python features are demonstrated.

As we pass through each step, feel free to make edits and see how you can
change the application. If you do change files, you can always revert your
changes with `git` (you'll have to do so before moving to the next step in the
tutorial)::

    $ git status
    ...
      modified:   README.rst

    $ git checkout -- README.rst


Tutorial Outline
================

Let's step through the process of creating a simple but featureful blog
application using the Pyramid web framework.

Step 1: Project Creation
------------------------

**To Reach This Step**::

    $ git checkout a656bc23

We are using the `pyramid web framework <http://docs.pylonsproject.org/en/latest/docs/pyramid.html>`_
for this tutorial. The framework comes with a code templating tool called
`pcreate`. This tool uses *scaffolds* to generate basic project skeletons we
can use to get started.

The code in this step is the result of using the `sqlalchemy` scaffold to
generate a project that will use an **RDBMS** to persist data and **url
dispatch** to connect client requests to the programs that will generate
responses.

We can see our application in action already by *installing* it and then
*running* the server::

    $ cd /path/to/python-tutorial/pyramid-blogr-cf
    $ source ../blogr/bin/activate
    (blogr)$ python setup.py develop
    ...
    (blogr)$ initialize_blogr_db development.ini
    ...
    (blogr)$ pserve development.ini --reload
    Starting subprocess with file monitor
    Starting server in PID 29653.
    serving on http://0.0.0.0:6543


**Topics**

* Pyramid Project Layout
* RDBMS Persistence
* URL Dispatch
* Application installation and operations

Step 2: Dependencies and Configuration
--------------------------------------

**To Reach This Step**::

    $ git checkout 192c1150

In this step we begin by adding a `.gitignore` file to our project. Every code
project should have one, and you can find excellent examples for various
languages `on github <https://github.com/github/gitignore>`_.

In addition, we update the `setup.py` file in our project to list additional
`Python packages <https://pypi.python.org>`_ that our code will depend on.
Having a `setup.py` file means that your code can be *installed* into a Python
environment. When it is installed, all the *dependencies* we have listed will
also be installed, ensuring that the code we require is available.

Finally, we make a small change to the `configuration <http://docs.pylonsproject.org/projects/pyramid/en/latest/narr/configuration.html>`_
for our application. Pyramid uses configuration to control how an application
behaves.  In this case, we have changed the templating engine we will use from
`chameleon <https://chameleon.readthedocs.org>`_ to `jinja2 <http://jinja.pocoo.org>`_.
Pyramid supports many different templating engines and it is simple to change
which you will use.

**Topics**

* Git management
* Python packages
* Pyramid application configuration

Step 3: Models and DB Initialization
------------------------------------

**To Reach This Step**::

    $ git checkout 30c5a781

We must begin by delete code related to the sample model created by our
*scaffold*. This code occurs both in the `models.py` file and in the `views.py`
file.

Once all traces of that code are removed, we can move on to adding *models* of
our own. A *model* is a Python class that can be persisted via an *ORM* to a
database. We have two such models, an `Entry` and a `User`.

We must also update the script that is used to initialize our database. This
script will create the database tables needed to store our entries and users.
It must also create an initial user. This script is registered as a *console
script* in our application `setup.py` file so that when the application is
installed, it is available at the command line.

Notice that we create our initial user with an encrypted password.  You must
*never* store plain-text passwords on a server.

Now that we have different models for our database, we will need to delete and
re-initialize our database::

    (blogr)$ rm blogr.sqlite
    (blogr)$ initialize_blogr_db development.ini
    ...
    (blogr)$

**Topics**

* Data Models and ORMs
* Python console scripts
* Password encryption

Step 4: Routes
--------------

**To Reach This Step**::

    $ git checkout 0daa4e79

We update our application configuration to add the *routes* that will be
available to clients. Each *route* represents one or more *endpoint* that will
be served by our application's *views*.

Defining the *routes* for an application is really the same as defining the
*API* that your application will provide.  It determines the functionality your
application will have and how users will access that functionality.

Pyramid routes have many configuration options, but here we are simply
providing a *name* for the route (which must be unique across our application)
and a
`pattern <http://docs.pylonsproject.org/projects/pyramid/en/latest/narr/urldispatch.html#route-pattern-syntax>`_
which will be used to match the incoming request to appropriate view code.

**Topics**

* URL Matching
* Regular Expressions
* API

Step 5: Stub Views
------------------

**To Reach This Step**::

    $ git checkout 2905b7fb

In this step we define stub views that will serve as *endpoints* for the
*routes* we have already added. Each view in a Pyramid application is written
as a function or class method that must take `request` as the first argument.
Pyramid views must return a Python `dictionary` which serves as a mapping of
names to values that will be used to render a template.

Each of our *views* is preceded by the `view_config` Python *decorator*. This
is used to configure how the view is paired with the *routes* we configured
earlier. The `route_name` argument determines which route is paired with this
view. The `renderer` argument determines how the data mapping returned by the
view will be rendered for return to the client. Further arguments to
`view_config` are called *predicates*. These can help to control which specific
*view* will be used as the endpoint for a matched *route*.

In order for our view code to work, we must provide templates that match the
names of our *renderer* arguments. We add three such templates in this step.
For now, we'll keep them simple so we can test the application.

Finally, we remove the template generated by our scaffold. It will not be used
by our application and is therefore not needed.

Now we can test our routes and views in a browser.  Start your application::

    (blogr)$ pserve development.ini --reload
    Starting subprocess with file monitor
    Starting server in PID 30051.
    serving on http://0.0.0.0:6543

You should be able to view:

* the homepage at http://localhost:6543/
* an entry at http://localhost:6543/blog/1/foo
* an edit page at http://localhost:6543/blog/edit
* a create page at http://localhost:6543/blog/create

**Topics**

* The Pyramid view contract
* View configuration
* Python decorators
* View predicates
* Renderers

Step 6: Entry Model Methods
---------------------------

**To Reach This Step**::

    $ git checkout aef7e1ed

We add methods to the `Entry` model class we created earlier that are related
to accessing and viewing entries.

Some of our methods are decorated with `classmethod`, a decorator that means
these methods can be called on the `Entry` class object without needing an
instance of that class.

Others are decorated as `properties`. This allows us to address them as simple
object *attributes* rather than needing to call them as methods. It also allows
us to make them *read only*, which we do in this case.

One of our `Entry` class methods is responsible for creating a *paginator* for
`Entry` objects. This paginator will manage all aspects of having many entries,
from minimizing database calls to providing data about the previous and next
pages and the total count of entries. Building a paginator requires a
*callable* Python object that can be used to create a URL for pages of entries.
We create such an object.

Together, these methods form the *API* of our `Entry` model.

**Topics**

* Python OO Techniques
* Python decorators
* Pagination and DB Management

Step 7: List and Item Views
---------------------------

**To Reach This Step**::

    $ git checkout 2f64b75e

We update our application's `index_page` view to provide a paginated list of
`Entry` instances. Notice that this view still follows the contract of
accepting the *request* as an argument and returning a Python `dictionary`
mapping as a return value.

Similarly, we update the `blog_view` view to return a single entry in its
mapping. We find the correct entry by inspecing the `matchdict` created when
the incoming request was matched with the `blog` *route*. Notice that if the
specified entry cannot be found, we return an `HTTPNotFound`.  This will
trigger sending a `404 Not Found` response to the client.

Finally, we create the `jinja2` templates we will need to show the results from
these two views. We start by creating a *main template* we call
`layout.jinja2`. This allows us to have shared structure common to all pages in
our site. Our `index.jinja2` and `view_blog.jinja2` templates then *extend*
this main template, filling in the details that are different.

View the changes you've made by starting your application again::

    (blogr)$ pserve development.ini --reload
    Starting subprocess with file monitor
    Starting server in PID 30051.
    serving on http://0.0.0.0:6543

Notice that the home page now offers us a chance to create a new entry.  What
happens when you click on that link? What happens if you attempt to load an
entry now (http://localhost:6543/blog/1/foo)?

**Topics**

* Passing entries to templates
* Receiving data from the client via the request
* Simple jinja2 template structure and template inheritance

Step 8: Create and Edit Entries
------------------------------------

**To Reach This Step**::

    $ git checkout dce363b0

We use a Python packaged called `WTForms <http://wtforms.readthedocs.org/>`_ to
create two `Form` subclasses that will serve for creating new entries and
editing existing ones. *Forms* will handle rendering *html inputs* in our
templates as well as binding data from `Entry` objects retrieved from the
database or data from *inputs* received via request from the client. Forms can
also *validate* received data, ensuring it is correct before you attempt to use
it.

We can incorporate our new `Form` subclasses into the views intended for
creating and editing entries. Notice that in these views, we instantiate a form
*instance* by passing the data from `POST`. This ensures that information the
client entered into html inputs is properly translated into Python values.
Notice also that we only make changes to our database when the request is
received via the `POST` method. This is best practice.

Finally, we update our template for creating and editing to render the form we
pass back from the views. We can iterate over the fields in the form so that we
need not render them one at a time.

At last, we can create our first entry.  Start up the application again and
play for a while::

    (blogr)$ pserve development.ini --reload
    Starting subprocess with file monitor
    Starting server in PID 30051.
    serving on http://0.0.0.0:6543

**Topics**

* Forms
* Data translation
* Creating and editing model instances
* Python iterators

Step 9: Authorization
---------------------

**To Reach This Step**::

    $ git checkout 9d0a9de7

Anyone can add or edit an entry in our blog. To close this security hole we
must implement an authorization scheme.  Authorization is the process of
determining what a given user is allowed to do within an application. Our
scheme will be simple. Anyone can view entries, but only a person who is logged
in can add or edit them.

Pyramid has `several possible methods <http://docs.pylonsproject.org/projects/pyramid/en/latest/narr/security.html>`_
for handling authorization.  We'll be using the ACL policy, which makes use of
`Access Control Lists <http://en.wikipedia.org/wiki/Access_control_list>`_. We
create a new factory object that has an `__acl__` special attribute. This
attribute is our access control list. It consists of a series of Access Control
Entries (ACEs), which consist of a rule (Allow or Deny), a *principal* (an
identity within our system) and a *permission*. Ours is simple and static, but
you can create ones that are quite complex and dynamic.

Once we have this ACL factory, we add configuration to our application to use
it. We instruct the application to use the `ACLAuthorizationPolicy` and to
combine it with the `AuthTktAuthenticationPolicy` (more about that soon).
Finally, we add our factory as predicate argument to the *route* connect with
creating and editing entries.  This ensures that every request matched to this
route will check with our ACL factory before allowing access.

Last, we add `permission` predicate arguments to our `view_config` decorators
for the two *views* that handle creating and editing entries. When the ACL
factory is checked, it will verify that the current *principal* has been
*Allowed* the *permission* required by the view to which the request is
dispatched.

**Topics**

* Authorization
* Access control lists
* Principals and permissions
* Separation of concerns

Step 10: Authentication
-----------------------

**To Reach This Step**::

    $ git checkout a6ca539b

Now only logged in users can add or edit posts, but no-one can log in. To solve
this, we must implement an authentication scheme. Authentication is the process
of verifying that a given user is who they say they are. Once a user is
authenticated, then the `Authenticated` *principal* is available for our ACL
factory.

We start by creating a login form.  Like the edit and create forms from
earlier, this will enable simple rendering of the login fields when required as
well as handling validation of login data.

Where the form can validate data, the User model class should be responsible
for verifying a user's password.  We add a method to our User model to do so.
And we want a controller method that will fetch a user given a name so that we
can find the user who is trying to log in.

With all that in place, We create the view for logging in to the application.
The view binds data submitted by the user to our login form, then uses that
form to find a user and verify the submitted password. When work is done, it
redirects the client to the home page using the `HTTPFound` response.

In addition, we modify the index page view so that if we are *not* logged in,
we will have a login form to render. We also update the blog index page
template so that it will show the login form if present.  If the form is not
present, we must be logged in, and we can show the "create" button.

We also update the edit view to provide information to the template about
whether or not a user is logged in.  This will allow showing/hiding the "edit"
button in the template. The single blog entry view template is then updated to
show the *edit* button only if we are logged in.

Now we can log in and create another entry::

    (blogr)$ pserve development.ini --reload
    Starting subprocess with file monitor
    Starting server in PID 30051.
    serving on http://0.0.0.0:6543

**Topics**

* Authentication
* Encryption
* Handling login and logout
* Conditional rendering in templates

Step 11: Style Forms
----------------------

**To Reach This Step**::

    $ git checkout 6319927e

One flaw in our application is that the forms look a bit out of place. The rest
of the page is reasonably styled using a simple `bootstrap` theme. Let's fix
this by rendering our forms in a more bootstrap-compliant fashion.

We begin by creating a set of `macros <http://jinja.pocoo.org/docs/templates/#macros>`_,
a really nice feature of the Jinja2 templating language. Macros allow us to
create re-usable blocks of HTML with placeholders that can be filled in with
provided arguments when the macro is called. Our macros will render fields and
a form using bootstrap-style markup.

Once the macros exist, using them in our templates is just a matter of
importing the macros and then calling them in context. This allows us to
eliminate nearly all of the template code we wrote to handle form rendering.
Nice!

Now we can see our nifty new forms in action::

    (blogr)$ pserve development.ini --reload
    Starting subprocess with file monitor
    Starting server in PID 30051.
    serving on http://0.0.0.0:6543

**Topics**

* Jinja2 template macros
* Bootstrap form markup
* Advanced form rendering

Step 12: Simple Entry Formatting with Markdown
----------------------------------------------

**To Reach This Step**::

    $ git checkout 85faa53f


