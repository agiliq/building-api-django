Access Control
=================================

In this chapter, we will add access control to our APIs,
and add APIs to create and authenticate users.

Right now our APIs are completely permissive. Anyone can create, access and delete anything.
We want to add these access controls.


- A user must be authenticated to access a poll or the list of polls.
- Only an authenicated users can create a poll.
- Only an authenticated user can create a choice.
- Authenticated users can create choices only for polls they have created.
- Authenticated users can delete only polls they have created.
- Only an authenticated user can vote. Users can vote for other people's polls.

To enable thi access control, we need to add two more APIs

- API to create a user, we will call this endpoint :code:`/users/`
- API to verify a user and get a token to identify them, we will call this endpoint :code:`/login/`



Creating a user
--------------------------


We will add an user serializer, which will allow creating. Add the following code to :code:`serializers.py`.

.. code-block:: python

    class UserSerializer(serializers.ModelSerializer):

        class Meta:
            model = User
            fields = ('username', 'email', 'password')
            extra_kwargs = {'password': {'write_only': True}}

        def create(self, validated_data):
            user = User(
                email=validated_data['email'],
                username=validated_data['username']
            )
            user.set_password(validated_data['password'])
            user.save()
            return user

We have overriden the ModelSerializer method's :code:`create()` to save the :code:`User` instances. We ensure that we set the password correctly using :code:`user.set_password`, rather than setting the raw password as the hash. We also don't want to get back the password in response which we ensure using :code:`extra_kwargs = {'password': {'write_only': True}}`.

Let us also add views to the User Serializer for creating the user and connect it to the urls.py

.. code-block:: python

    # in apiviews.py
    # ...
    from .serializers import PollSerializer, ChoiceSerializer, VoteSerializer, UserSerializer

    # ...
    class UserCreate(generics.CreateAPIView):
        serializer_class = UserSerializer

    # in urls.py
    # ...
    from .apiviews import PollViewSet, ChoiceList, CreateVote, UserCreate


    urlpatterns = [
        # ...
        path("users/", UserCreate.as_view(), name="user_create"),
    ]

We can test this api by posting to :code:`/users/` with this json.

.. code-block:: json

    {
        "username": "nate.silver",
        "email": "nate.silver@example.com",
        "password": "FiveThirtyEight"
    }

Which give back this response.

.. code-block:: json

    {
        "username": "nate.silver",
        "email": "nate.silver@example.com"
    }

Try posting the same json, and you will get a error response (HTTP status code 400)

.. code-block:: json

    {
        "username": [
            "A user with that username already exists."
        ]
    }


Authentication scheme setup
-----------------------------

With Django Rest Framework we can set up a default authentication scheme which works globally with the help of setting called 'DEFAULT_AUTHENTICATION_CLASSES'. We shall use the Basic authentication scheme in this tutorial. For achieving it we should set it in our settings.py file.

.. code-block:: python

    REST_FRAMEWORK = {
        'DEFAULT_AUTHENTICATION_CLASSES': (
            'rest_framework.authentication.BasicAuthentication',
            'rest_framework.authentication.SessionAuthentication',
        )
    }


If we add the above lines in our settings.py file, we do require basic authentication to access the views. But, we do need the access to create a user. So we shall override the global setting in a single view level. Move to the app's view.py file and add the below line to the 'UserCreate' view.

.. code-block:: python

    authentication_classes = ()


Now we should make sure that the bullet points we mentioned in the beginning of authentication needs to be achieved. Whether to create or access a poll the user needs to be a registered one. For that we can add the default permission policy globally using the DEFAULT_PERMISSION_CLASSES setting. Add the below setting to the settings.py file.

.. code-block:: python

    REST_FRAMEWORK = {
        'DEFAULT_PERMISSION_CLASSES': (
            'rest_framework.permissions.IsAuthenticated',
        )
    }

Also, dont forget to give excemption to UserCreate view by overriding the global setting. Just to make sure the UserCreate should look as follows.

.. code-block:: python

    class UserCreate(generics.CreateAPIView):
        """
        Create an User
        """

        authentication_classes = ()
        permission_classes = ()
        serializer_class = UserSerializer

All done, so from now the user needs to be an 'authenticated user' to access our poll and the poll data.
