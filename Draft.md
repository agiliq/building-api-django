Building a Polls API with Django
=============================

In this tutorial we will walk through a process of creating an API for a basic poll application. We will be using python 2.7, Django 1.8 and Django Rest Framework for creating API.

First things first, lets install the required modules with virtual environment created and activated.

    mkvirtualenv pollsapi
    pip install Django
    pip install djangorestframework 

Creating a project
--------------------

Earliest in order, to create a project we should move to the directory where we would like to store our code. For this go to command line and use cd command. Then trigger the start prject command.
    
    django-admin startproject django_pollsapi

The above mentioned command results us a 'django_pollsapi' directoy. 

Database setup
------------------

For ease of use we shall choose SQlite database which is already included in python. The "django_pollsapi/settings.py" file should reflect the following Database settings

    DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

Now, use the migrate command which builds the needed database tables in regard to the "django_pollsapi/settings.py" file.

    python manage.py migrate


Creating models
---------------------

Before creating our database models, let us create our pollsapi App.

    python manage.py startapp pollsapi

The above command resluts a 'pollsapi' directory containing different files, i.e 'admin.py', 'models.py', 'tests.py', 'views.py'.
Step in to 'models.py' file and start writing the models. For creating the polls api we are going to create a Poll model, a Choice model and a Vote model. Once we are done with designing our models, the 'models.py' file should look like this:

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

    INSTALLED_APPS = (
    ...
    'rest_framework',
    'pollsapi',
    )


Now, run the makemigrations command which will notify Django that new models have been created and those changes needs to be applied to the migration.

    python manage.py makemigrations pollsapi

Go to URls in the root folder i.e django_pollsapi and include the app urls.

    urlpatterns = [
    url(r'^', include('pollsapi.urls')),
    ]


Part 2:
========

Django-rest-framework makes the process of building web API's simple and flexible. With its batteries included it won't be a tedious task to create an API.


Serialization and Deserialization
--------------------------------------

The first part in the process of building an API is to provide a way to serialize and deserialize the instances into representations. Serialization is the process of making a streamable representation of the data which will help in the data transfer over the network. Deserialization is its reverse process. In our project of building an API we render data into JSON format. To achieve this, Django-rest-framework provides 'JSONRenderer' and 'JSONParser'. 'JSONRenderer' renders the request data into 'json' using utf-8 encoding and JSONParser parses the JSON request content.


Creating Serializers
-----------------------

Lets get started with creating serializer class which will serialize and deserialize the pollsapi instances in to different representations. Create a file named "pollsapi/serializers.py". Let us make use of model serializers which will decrease replication of code by automatically determing the set of fields and by creating simple default implementations of the create() and update() methods.


    from rest_framework import serializers

    from django.contrib.auth.models import User

    from .models import Poll, Choice, Vote



    class ChoiceSerializer(serializers.ModelSerializer):
        votes = VoteSerializer(many=True, required=False)

        class Meta:
            model = Choice


    class PollSerializer(serializers.ModelSerializer):
        choices = ChoiceSerializer(many=True, read_only=True, required=False)
        
        class Meta:
            model = Poll


    class VoteSerializer(serializers.ModelSerializer):
        class Meta:
            model = Vote


    class UserSerializer(serializers.ModelSerializer):

        class Meta:
            model = User
            fields = ('username', 'email', 'password')


In the above lines of code we created a Choice Serializer in such a way that whenever we create a choice it does need to have the votes model connected to it and if a poll is created the choices needs to be created simultaneously. We will be needing a user for dealing with the polls and voting for that we used the Django's User.

Creating Views
----------------

Let us use generic views of Django Rest Framework for creating our views which will help us in code reusablity. The generic views alos aid us in building the API quickly and in mapping the database models.


    from rest_framework import generics

    from .models import Poll, Choice
    from .serializers import PollSerializer, ChoiceSerializer,\
        VoteSerializer


    class PollList(generics.ListCreateAPIView):

        """
        List all polls, or create a new poll.
        """

        queryset = Poll.objects.all()
        serializer_class = PollSerializer


    class PollDetail(generics.RetrieveDestroyAPIView):
        """
        Create a Poll, delete a poll
        """

        queryset = Poll.objects.all()
        serializer_class = PollSerializer


    class ChoiceDetail(generics.RetrieveUpdateAPIView):
        """
        Retrieves a Choice, Updates a Choice
        """

        queryset = Choice.objects.all()
        serializer_class = ChoiceSerializer


    class CreateVote(generics.CreateAPIView):
        """
        Create a vote
        """

        serializer_class = VoteSerializer

    class UserCreate(generics.CreateAPIView):
        """
        Create an User
        """

        serializer_class = UserSerializer


    class UserDetail(generics.RetrieveAPIView):
        """
        Retrieve a User
        """

        queryset = User.objects.all()
        serializer_class = UserSerializer


When writting a generic view we will override the view and set several calss attributes.

Let us have a look in to the important parts in the code.

1. queryset: This will be used to return objects from the view. 
2. serializer_class: This will be used for validating and deserializing the input and for seraizling the output.


Part 3:
===========

Creating URLs
--------------

It's time to wire up the views to specific URLs


    from django.conf.urls import include, url
    from django.contrib import admin

    import pollsapi.views

    urlpatterns = [

        url(r'^admin/', include(admin.site.urls)),
        url(r'^polls/$', pollsapi.views.PollList.as_view()),
        url(r'polls/(?P<pk>[0-9]+)/$', pollsapi.views.PollDetail.as_view()),
        url(r'^create_user/$', pollsapi.views.UserCreate.as_view()),
        url(r'^choices/(?P<pk>[0-9]+)/$', pollsapi.views.ChoiceDetail.as_view()),
        url(r'^create_vote/$', pollsapi.views.CreateVote.as_view()),
        url(r'^users/(?P<pk>[0-9]+)/$', pollsapi.views.UserDetail.as_view()),

    ]

In the above lines of code we have created URLs for all the views according to our requirement.

