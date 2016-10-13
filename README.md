# Build a Blog With Pyramid

This outline is a brief (3 hour) tutorial on developing web applications with Python.
It has been adapted from the
[Pyramid blogr](http://pyramid-blogr.readthedocs.org/en/latest/)
tutorial which in turn is an adaptation of the
[Flask Tutorial](http://flask.pocoo.org/docs/tutorial/)

This tutorial is intended for use with Python 3.

[previous](https://github.com/cewing/pyramid-blogr-cf/tree/tutorial-step-09)

## Step 10: Add Dynamic Permissions

[view the differences](https://github.com/cewing/pyramid-blogr-cf/compare/c75b3031...df03e277)

Now that new users can register, we might notice a wee problem with how things work now.
Both the original default user and the newly registered user can create blog records.
They can edit the records they've created too.
But perhaps you've noticed that each can also edit the other's posts.
This seems like something we'd like to fix.

### Ownership

In order to prevent one user from editing another users records, we first have to be able to answer one question.
Which user does this record *belong* to.
We need a way of asserting the ownership of an individual record in the database.

SQL allows us to model this type of scenario using a `ForeignKey`.
We'll add a foreign key to our `BlogRecord` model.
It refers to the `id` field of the `users` table.
This means that any one `BlogRecord` will be associated with a `User`.
Conversely any `User` may be associated with any number of `BlogRecords`.
This is called a `ManyToOne` relationship.

This will accomplish what we need.
But SQLAlchemy offers us a bit more.
We can make use of the [relationship](http://docs.sqlalchemy.org/en/latest/orm/extensions/declarative/relationships.html) construct in the SQLAlchemy ORM
to add attributes to our Python model classes that refer directly to the objects on the other end of that foreign key.
Instead of referencing the `id` of the related object and then using that to look that object up,
we can refer to the name of the relationship (`author`) as an attribute of a `BlogRecord` and the value will be that specific `User` object.

A nice feature of this `relationship` is that we can add an attribute to the `User` that will give us all the `BlogRecords` that user owns.
The `back_populates` argument to the `relationship` constructor tells SQLAlchemy that we wish the path to be reciprocal.
We can get to `BlogRecords` from `Users` using the attribute `posts`.
And we can get to `Users` from `BlogRecords` using the attribute `author`.

### Changing The Database

We've made a change to our data models.
This means that the way our tables are built is no longer in sync with the Python models we have.

In a production scenario, we would definitely want to face this problem by using a *data migration*.
The [alembic](http://alembic.zzzcomputing.com/en/latest/index.html) package provides the ability to create Python code that will progressively alter a database to keep it in sync with a Python model.
But we aren't in a production scenario, so let's take a different approach.

Delete your database:

    (blogr)$ rm blogr.sqlite3

Then, re-initialize the database with the new models:

    (blogr)$ initialize_blogr_db development.ini

Now, our tables match our models and we can proceed.

### Who's There?

Our next step is to ensure that when a `BlogRecord` is created, it has the current authenticated user set as its author.
In order to accomplish this, we need to be able to access the current authenticated user.

Pyramid provides a mechanism to do this.
We can add methods to the request using `config.add_request_method()` that will give us access to various run-time values.
In `security.py`, we'll add a method attaches the `User` instance for the authenticated user to the request.
And in the `includeme` we will wire that up.
Then, in our view code we can refer to `request.user` and have direct access to that object.

### Update the View

Now that we have that set up, we should be able to add a single line of code to our `blog_create` view.
We'll set the `author` of our new record to the currently authenticated user.
When the object is saved, the id of that user will be saved as the `author_id` value in the entries table.
And we'll be able to reconstruct this relationship in Python easily.

And now all the pieces are in place for us to reach our goal.

### That's My Record!

Remember that in Pyramid a *root* is responsible for determining the ACL for a request.
At the moment, our ACL is static.
But the *root factory* has access to the current request.
And the request has access to the current user.
We can use this to determine if the current user should have access to the blog record being requested (if any).

We'll update our `BlogRecordService` to provide a method that indicates if the current user should be allowed the `edit` permission.
It will look for a blog `id` value, either in the `request.matchdict` or in `request.params`.
If such an 'id' exists, and there is a currently authenticated user,
it checks the database to find a record with that `id`, owned by this user.
If such a record exists, then we should return True.
Otherwise, we return False

### Let Me At It

We can now update our root factory to make our `__acl__` dynamic.
We begin by storing a reference to the request on the root instance.
Then we convert `__acl__` from an attribute to a method.
We set up a basic ACL that grants 'view' to `Everyone` and 'create' to the `Authenticated` principal.
Then, we check to see if our current user should be granted the 'edit' permission using our new service API.
If the answer is yes, we add a new ACE to our ACL, allowing `self.request.authenticated_userid` the permission.
Finally, we return our ACL.

Now, if the current user is interacting with a record they have created, they will be allowed the 'edit' permission.
But if they are not interacting with a record, or the record belongs to another user, they will not.

When we update our `blog_edit` view configuration to require the `edit` permission, we are almost there.

### Prevent Leakage

One remaining problem is that when we are viewing an idividual post, we still see the 'edit' button,
even if the post is not ours.
The problem is that we are not checking permissions when deciding to show that link.

The Pyramid request offers a `.has_permission()` method that allows us to check if the authenticated user has a give permission in the current context.
We can add a check for the 'edit' permission in our page template around the "edit" link.
But now, when we check our running app, nobody sees that button.

That's because the view that *shows* us a record does not use our custom *root factory*.
Remember that Pyramid by default uses an empty ACL, so if you require a permission for something,
it will fail unless you specifically grant that permission.
Pyramid is secure by default.

To solve our problem then, we need to use our custom factory *both* for the blog action route, but also for the blog view route.
Updating this causes the edit link to appear for blog owners, and disappear for other authenticated users.


### Check It Out

Start your application running:

    (blogr)$ pserve development.ini

You can now [visit your homepage](http://locahost:6543/) and register yourself as a user.
Create a few entries and observe that you are allowed to edit them.

Next, log out and register as a different user.
Log in as that user and then create a few entries with that identity.
Notice that you can edit your own entries, but you are not allowed to edit those you created as the other user.
You can try entering the urls directly, and it won't make a difference.
We have not just hidden the link for editing, we've forbidden users from editing posts they do not own.

