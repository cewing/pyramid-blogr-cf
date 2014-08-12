===============================
Intro to Python Web Development
===============================

This outline is a brief (3 hour) tutorial on developing web applications with
Python. It has been adapted from the
`pyramid blogr <http://pyramid-blogr.readthedocs.org/en/latest/>`_
tutorial which in turn is an adaptation of the
`Flask Tutorial <http://flask.pocoo.org/docs/tutorial/>`_.


Setting Up Your Environment
===========================

We will use a tool called `virtualenv` to create a Python sandbox in which to
work.

Begin by downloading and installing the package from source::

    $ curl -O https://pypi.python.org/packages/source/v/virtualenv/virtualenv-X.Y.Z.tar.gz
    $ tar xvfz virtualenv-X.X.tar.gz
    $ cd virtualenv-X.Y.Z
    $ [sudo] python setup.py install

* At the time of this writing, the most recent version of `virtualenv` is
  1.11.6, so substitute `1.11.6` for the `X.Y.Z` in the first line above.
* You may need to use `sudo` to install the virtualenv package in your system
  Python.

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

Once that is complete, you're ready to begin the tutorial
