Access Control
=================================

In this chapter, we will add access control to our APIs,
and add APIs to create and authenticate users.

Right now our APIs are completely permissive. Anyone can create, access and delete anything.
We want to add these access controls.


- A user must be authenticated to access a poll or the list of polls.
- Only an authenticated users can create a poll.
- Only an authenticated user can create a choice.
- Authenticated users can create choices only for polls they have created.
- Authenticated users can delete only polls they have created.
- Only an authenticated user can vote. Users can vote for other people's polls.

To enable the access control, we need to add two more APIs

- API to create a user, we will call this endpoint :code:`/users/`
- API to verify a user and get a token to identify them, we will call this endpoint :code:`/login/`



Creating a user
--------------------------


We will add an user serializer, which will allow creating. Add the following code to :code:`serializers.py`.

.. code-block:: python

    # ...
    from django.contrib.auth.models import User
    
    # ...
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

With Django Rest Framework, we can set up a default authentication scheme which is applied to all views using :code:`DEFAULT_AUTHENTICATION_CLASSES`. We will use the token authentication in this tutorial. In your settings.py, add this.

.. code-block:: python

    REST_FRAMEWORK = {
        'DEFAULT_AUTHENTICATION_CLASSES': (
            'rest_framework.authentication.TokenAuthentication',
            'rest_framework.authentication.SessionAuthentication',
        )
    }

You also need to enable :code:`rest_framework.authtoken` app, so update :code:`INSTALLED_APPS` in your settings.py.

.. code-block:: python

    INSTALLED_APPS = (
        ...
        'rest_framework.authtoken'
    )

Run :code:`python manage.py migrate` to create the new tables.

.. We want to ensure that, by default all apis are only allowed to authenticated users. Add this to your :code:`settings.py`.

.. code-block:: python

    REST_FRAMEWORK = {
        # ...
        'DEFAULT_PERMISSION_CLASSES': (
            'rest_framework.permissions.IsAuthenticated',
        )
    }

Also, dont forget to give exemption to :code:`UserCreate` view for authentication by overriding the global setting. The :code:`UserCreate` in :code:`polls/apiviews.py` should look as follows.

.. code-block:: python

    class UserCreate(generics.CreateAPIView):
        authentication_classes = ()
        permission_classes = ()
        serializer_class = UserSerializer

Note the :code:`authentication_classes = ()` and :code:`permission_classes = ()` to exempt :code:`UserCreate` from global authentication scheme.

We want to ensure that tokens are created when user is created in :code:`UserCreate` view, so we update the :code:`UserSerializer`. Change your :code:`serializers.py` like this

.. code-block:: python

    from rest_framework.authtoken.models import Token

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
            Token.objects.create(user=user)
            return user



The login API
-----------------------------

Since we have added :code:`rest_framework.authentication.TokenAuthentication`, we will need to set a header like this :code:`Authorization: Token c2a84953f47288ac1943a3f389a6034e395ad940` to auhenticate. We need an API where a user can give their username and password, and get a token back.

We will not be adding a serializer, because we never save a token using this API.

Add a view and connect it to urls.

.. code-block:: python

    # in apiviews.py
    # ...
    from django.contrib.auth import authenticate

    class LoginView(APIView):
        permission_classes = ()

        def post(self, request,):
            username = request.data.get("username")
            password = request.data.get("password")
            user = authenticate(username=username, password=password)
            if user:
                return Response({"token": user.auth_token.key})
            else:
                return Response({"error": "Wrong Credentials"}, status=status.HTTP_400_BAD_REQUEST)


    # in urls.py
    # ...

    from .apiviews import PollViewSet, ChoiceList, CreateVote, UserCreate, LoginView



    urlpatterns = [
        path("login/", LoginView.as_view(), name="login"),
        # ...
    ]

WARNING: You have to create a user using the :code:`/user/` endpoint before logging in using the :code:`/login/` endpoint. Using a previously existing user will result in a "User has no auth_token" error because we have not created a token for them. You can create tokens for them manually by using the django shell :code:`$ python manage.py shell`.

    >>> from django.contrib.auth.models import User
    >>> from rest_framework.authtoken.models import Token
    >>> user = User.objects.get(pk=pk_of_user_without_token)
    >>> Token.objects.create(user=user)
    <Token: e2b9fa2d4ae27fe1fdcf17b6e37711334d07e167>

Do a POST with a correct username and password, and you will get a response like this.

.. code-block:: json

    {
        "token": "c300998d0e2d1b8b4ed9215589df4497de12000c"
    }


POST with a incorrect username and password, and you will get a response like this, with a HTTP status of 400.

.. code-block:: json

    {
        "error": "Wrong Credentials"
    }

Another way to create this login endpoint is using :code:`obtain_auth_token` method provide by DRF

.. code-block:: python

    # in urls.py
    # ...
    from rest_framework.authtoken import views

    urlpatterns = [
        path("login/", views.obtain_auth_token, name="login"),
        # ...
    ]


Fine grained access control
-----------------------------

Try accessing the :code:`/polls/` API without any header. You will get an error with a http status code of :code:`HTTP 401 Unauthorized` like this.

.. code-block:: json

    {
        "detail": "Authentication credentials were not provided."
    }

Add an authorization header :code:`Authorization: Token <your token>`, and you can access the API.

From now onwards we will use a HTTP header like this, :code:`Authorization: Token <your token>` in all further requests.

We have two remaining things we need to enforce.

- Authenticated users can create choices only for polls they have created.
- Authenticated users can delete only polls they have created.

We will do that by overriding :code:`PollViewSet.destroy` and :code:`ChoiceList.post`.

.. code-block:: python

    # ...
    from rest_framework.exceptions import PermissionDenied


    class PollViewSet(viewsets.ModelViewSet):
        # ...

        def destroy(self, request, *args, **kwargs):
            poll = Poll.objects.get(pk=self.kwargs["pk"])
            if not request.user == poll.created_by:
                raise PermissionDenied("You can not delete this poll.")
            return super().destroy(request, *args, **kwargs)


    class ChoiceList(generics.ListCreateAPIView):
        # ...

        def post(self, request, *args, **kwargs):
            poll = Poll.objects.get(pk=self.kwargs["pk"])
            if not request.user == poll.created_by:
                raise PermissionDenied("You can not create choice for this poll.")
            return super().post(request, *args, **kwargs)

In both cases, we are checking :code:`request.user` against the expected user, and raising
a :code:`PermissionDenied` error if it does not match.

You can check this by doing a DELETE on someone elses :code:`Poll`. You will get an error with :code:`HTTP 403 Forbidden` and response.


.. code-block:: json

    {
        "detail": "You can not delete this poll."
    }


Similarly, trying to create choice for someone else's :code:`Poll` will get an error with :code:`HTTP 403 Forbidden` and response

.. code-block:: json

    {
        "detail": "You can not create choice for this poll."
    }


Next steps:
-----------------

In the next chapter we will look at adding tests for our API and serializers. We will also look at how to use :code:`flake8` and run our tests in a CI environment.
