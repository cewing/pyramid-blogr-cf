# Build a Blog With Pyramid

This outline is a brief (3 hour) tutorial on developing web applications with Python.
It has been adapted from the
[Pyramid blogr](http://pyramid-blogr.readthedocs.org/en/latest/)
tutorial which in turn is an adaptation of the
[Flask Tutorial](http://flask.pocoo.org/docs/tutorial/)

This tutorial is intended for use with Python 3.

[previous](https://github.com/cewing/pyramid-blogr-cf/tree/tutorial-step-06) ::
[next](https://github.com/cewing/pyramid-blogr-cf/tree/tutorial-step-08)

## Step 7: Add Authorization

[view the differences](https://github.com/cewing/pyramid-blogr-cf/compare/54982330...449f9513)

So far, we've built a blog application that allows a user to:

* view a list of entries
* view a single entry
* edit an existing entry
* create a new entry

This is all well and good, but at the moment *anyone* can take advantage of this functionality.
A system this open would not fare well in the rough-and-tumble world of the internet.
We must now take steps to control access to the ability to create and edit entries.

In any web application, access control rests on two concepts, *authorization* (AuthZ) and *authentication* (AuthN).
Authorization is the process of determining what rights should be granted to a user of the application.
Authentication is the process of proving the identity of a user.

These concepts are intertwined.
After all, it's no good granting special rights to specific users unless we can identify them.
Similarly, knowing who a user is holds little value unless we plan on granting them specific rights.
For these reasons, many Python web frameworks treat these two aspects with one toolkit.

Pyramid is a bit different.
The specific implementation of each of these two aspects is controlled separately.
When you build your application, if you choose to use one, you must use the other.
But you are allowed to configure each independantly.

We'll begin our work with *authorization*.

### Configuration

The first step in configuring AuthZ/AuthN for a Pyramid app is to set up a *policy* for each.
We create a new Python module called `security.py`, following the model of our *routes* and *forms* and isolating code related to this work in one file.

In this new module, we'll import the `ACLAuthorizationPolicy`, provided by `pyramid.authorization`.
This stock policy determines permissions through an *acces control list*.
More about that in a moment.
We'll also import an authentication policy, but we'll say more about that in the next step.

Our next step is to define an `includeme()` function in our new security module.
This function takes a Configurator instance as its sole argument, which provides us access to update application configuration.
We build specific instances of each of our two policy classes, and then add the policies to our configurator.

Using this pattern allows us to handle all security-related configuration in this function.
We can then execute the function (and apply the new configuration) when our app is started by *including* it in our main function.
In `__init__.py` at the root of our application package, we add the following line to the `main` function:

    config.include('.security')

### Context

When using the `ACLAuthorizationPolicy`, Pyramid will look in the current *context* for an `__acl__` attribute.
By default, Pyramid creates a *root* object for every app which uses URL dispatch.
This *root* is considered a *context*, and will be used to provide access control assertions.
This default root has no `__acl__`, so you cannot be surprised by any default permissions provided invisibly.
In practice, this means that if you require permissions for a view, by default it will be inaccessible.

We will supply our own root object using an approach called a *root factory*.
In `security.py` we add a new class with a specific interface.
The class *must* have an `.__init__()` special method that takes a request object as an argument.
It must also have an `__acl__` attribute which returns a list of access control entries (ACEs).
More on what an ACE is in a moment.

The `__acl__` attribute can be a static list, as in our example.
But it can also be a method of the class, taking no arguments.
That approach allows for setting permissions dynamically on a per-request basis.

For every request that arrives at Pyramid, the *root factory* class will be instantiated to build a *root* instance.
This instance will then be used for security assertions for any *route* that uses this factory.
In order, then, for our new root factory to be used, we have to tell Pyramid to use it.
We will use the `factory` keyword argument to the `.add_route()` method of the configurator to do so.

We update our `routes.py` module so that the route associated with creating and editing blog records will make use of this new root factory
Now, if we configure a view associated with this route to require a permission, the *root* returned by this factory will be asked for an access control list.

### ACLs and ACEs

Our root factory has an `__acl__` attribute.
The attribute is bound to a list of three-tuples we will call *access control entries*.
Each tuple will contain

* an action (Allow or Deny)
* a principal identifier
* a permission

The effect of each entry is to allow or deny the identified principal the given permission.

#### Principals

A principal is a word used to represent some identifiable entity in an authorization scheme.
It might mean a username, tied to an individual user of a system.
It might mean the name of a group of users.
It might mean the name of a role, shared with users.
The term `principal` allows us to think about identity without needing to worry about how that identity is established.

For our purposes, we can think of the `principal` as the `name` attribute of an instance of our `User` model.

Pyramid also provides some special *principals*, `Authenticated` and `Everyone`.
The former represents any user who has successfully authenticated with the application.
The latter represents any user at all, anonymous or identified.

#### Permissions

In Pyramid, permissions are arbitrary strings.
We can name them whatever we wish, but we should consider what they will be used for.
Clarity in naming will help us later to understand our code.
What permissions are we granting in our root factory's `__acl__` attribute?

In order to require a permission, we use view configuration.
The `@view_config` decorator takes an optional `permission` argument.
The value should be a string corresponding to one of the permissions our system recognizes.

Here we choose to protect both our create and edit views with the `'create'` permission.
Who will be allowed to create new entries?
Who will be able to edit them?

When a request is made for one of these views, Pyramid will construct a root using our factory.
That root will be asked to supply an access control list.
The identity of the current user will be checked against the required permission.
If there is an entry which allows the permission to that principal, the view will be executed.
If not, then Pyramid will generate a `403 Forbidden` response, indicating the user has tried something they are not allowed to do.

## Check It Out

At this point, you should be able to start your application:

    (blogr)$ pserve development.ini

Then you can visit the [home page of the app](http://localhost:6543/).

If you click on the `create entry` link, you should see a `403 Forbidden` response in your browser.
Why?
What is your identity at this point?
What principal matches you?
what permissions are you granted?

You might try

* changing the permission required for another view
* try to grant yourself permission to access that other view, while keeping the edit and create views locked
* try to grant yourself permission to access the create view, but not the edit view.
