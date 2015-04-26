Chapter 2:
==========

Django-rest-framework makes the process of building web API's simple and flexible. With its batteries included it won't be a tedious task to create an API.


Serialization and Deserialization
---------------------------------

The first part in the process of building an API is to provide a way to serialize and deserialize the instances into representations. Serialization is the process of making a streamable representation of the data which will help in the data transfer over the network. Deserialization is its reverse process. In our project of building an API we render data into JSON format. To achieve this, Django-rest-framework provides 'JSONRenderer' and 'JSONParser'. 'JSONRenderer' renders the request data into 'json' using utf-8 encoding and JSONParser parses the JSON request content.


Creating Serializers
--------------------

Lets get started with creating serializer class which will serialize and deserialize the pollsapi instances in to different representations. Create a file named "pollsapi/serializers.py". Let us make use of model serializers which will decrease replication of code by automatically determing the set of fields and by creating simple default implementations of the create() and update() methods.

.. code-block:: python

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
--------------

Let us use generic views of Django Rest Framework for creating our views which will help us in code reusablity. The generic views alos aid us in building the API quickly and in mapping the database models.

.. code-block:: python

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

- queryset: This will be used to return objects from the view.
- serializer_class: This will be used for validating and deserializing the input and for seraizling the output.
