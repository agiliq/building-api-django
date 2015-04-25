Chapter 1
=============================

In this tutorial we will walk through a process of creating an API for a basic poll application. We will be using python 2.7, Django 1.8 and Django Rest Framework for creating API.

First things first, lets install the required modules with virtual environment created and activated.

.. code-block:: python 

    mkvirtualenv pollsapi
    pip install Django
    pip install djangorestframework 

Creating a project
--------------------

Earliest in order, to create a project we should move to the directory where we would like to store our code. For this go to command line and use cd command. Then trigger the start prject command.
    
.. code-block:: python 

    django-admin startproject django_pollsapi

The above mentioned command results us a 'django_pollsapi' directoy. 

Database setup
------------------

For ease of use we shall choose SQlite database which is already included in python. The "django_pollsapi/settings.py" file should reflect the following Database settings

.. code-block:: python 

    DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
                }
    }

Now, use the migrate command which builds the needed database tables in regard to the "django_pollsapi/settings.py" file.

.. code-block:: python

    python manage.py migrate


Creating models
---------------------

Before creating our database models, let us create our pollsapi App.

.. code-block:: python

    python manage.py startapp pollsapi

The above command resluts a 'pollsapi' directory containing different files, i.e 'admin.py', 'models.py', 'tests.py', 'views.py'.
Step in to 'models.py' file and start writing the models. For creating the polls api we are going to create a Poll model, a Choice model and a Vote model. Once we are done with designing our models, the 'models.py' file should look like this:

.. code-block:: python 

    from django.db import models
    from django.contrib.auth.models import User


    class Poll(models.Model):
        question = models.CharField(max_length=100)
        created_by = models.ForeignKey(User)
        pub_date = models.DateTimeField(auto_now=True)

        def __unicode__(self):
            return self.question


    class Choice(models.Model):
        poll = models.ForeignKey(Poll, related_name='choices')
        choice_text = models.CharField(max_length=100)

        def __unicode__(self):
            return self.choice_text


    class Vote(models.Model):
        choice = models.ForeignKey(Choice, related_name='votes')
        poll = models.ForeignKey(Poll)
        voted_by = models.ForeignKey(User)

        class Meta:
            unique_together = ("poll", "voted_by")

The above models have been designed in such a way that, it would make our API bulding a smooth process.

Activating models
----------------------

With the simple lines of code in the 'models.py' Django can create a database schema and a Python database-access API which has the capablity to access the objects of Poll, Choice, Vote. To create the database tables to our models, 'rest_framework' and 'pollsapi' app needs to be added to the "INSTALLED_APPS" in the 'django_pollsapi/settings' file. 

.. code-block:: python

    INSTALLED_APPS = (
    ...
    'rest_framework',
    'pollsapi',
    )


Now, run the makemigrations command which will notify Django that new models have been created and those changes needs to be applied to the migration.

.. code-block:: python

    python manage.py makemigrations pollsapi

Go to URls in the root folder i.e django_pollsapi and include the app urls.

.. code-block:: python

    urlpatterns = [
    url(r'^', include('pollsapi.urls')),
    ]
