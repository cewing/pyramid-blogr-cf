# Build a Blog With Pyramid

This outline is a brief (3 hour) tutorial on developing web applications with Python.
It has been adapted from the
[Pyramid blogr](http://pyramid-blogr.readthedocs.org/en/latest/)
tutorial which in turn is an adaptation of the
[Flask Tutorial](http://flask.pocoo.org/docs/tutorial/)

This tutorial is intended for use with Python 3.

[previous](https://github.com/cewing/pyramid-blogr-cf/tree/tutorial-step-00) ::
[next](https://github.com/cewing/pyramid-blogr-cf/tree/tutorial-step-02)

## Step 1: Get Started

[view the differences](https://github.com/cewing/pyramid-blogr-cf/compare/1cddd339...253c4d95)

We have created a new Pyramid application using a [scaffold](http://docs.pylonsproject.org/projects/pyramid/en/latest/narr/project.html).
This process provides a basic project built using best practices, and a starting point for our work.

We have also added a `.gitignore` file.
This file instructs the `git` version control system to ignore certain files that should never
be added to version control.
Starting any Python project with a [good .gitignore file](https://github.com/github/gitignore/blob/master/Python.gitignore)
really helps to keep your work clear of clutter.

Finally, we modify our `setup.py` file to add a few *dependencies*, packages that will provide
important functionality we will rely on in later steps.
Specifying the *dependencies* of your software in `setup.py` allows you to ensure that those other
packages are installed when your software is installed, preventing problems for those who use your software.

Now that we have all that settled, we can see what our scaffold has given us.

Install the application by running this command while at the root of the package (where `setup.py` is located):

    (blogr)$ pip install -e .

You'll see a number of packages downloaded and installed by pip.
All the dependencies we've listed are now available to use for use in our code.

We should be able to run the application now, by typing this command:

    (blogr)$ pserve development.ini
    Starting server in PID 29334.
    Serving on http://localhost:6543

This will inform us that the application is running and available at localhost on port 6543.
We can view the application by loading [http://localhost:6543](http://localhost:6543) in our web browser.
But notice that it tells us that we have a problem with our database.
The problem is that we have not yet created one.
We'll do that [in step two](https://github.com/cewing/pyramid-blogr-cf/tree/tutorial-step-02).