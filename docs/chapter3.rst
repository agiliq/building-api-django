Chapter 3:
===========

In this chapter we will be dealing with the creation of URLs and authentication.

Creating URLs
--------------

It's time to wire up the views to their respective specific URLs. We shall do it in the following manner.

.. code-block:: python

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
    ]

In the above lines of code we have created URLs for all the views according to our requirement.

Authentication of the API
--------------------------

Right now any one can create a poll or vote for a choice, and our endpoints are openly accessable to the world. Let us restrict the access by adding the authenitcation.
The following are the on we are going to deal with:

- A user has to login to access a poll.
- Only an authenicated users can create a poll.
- Only an authenticated user can vote.
- Only an authenticated user can create a choice.


Initially we should need representaions for User and for that let us create one in the serializers.py. Add the following code snippet to our serializers file.

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

In the above lines of code we used the ModelSerializer method's 'create()' to save the 'User' instances. 

Let us also add views to the User Serializer for creating and retrieving the user.

.. code-block:: python

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

Let us create a URL for accessing the detail info about the user. For that access the urls.py file and wire up the following User URL.

.. code-block:: python

    url(r'^users/(?P<pk>[0-9]+)/$', pollsapi.views.UserDetail.as_view()),

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

Exceptional handling
---------------------

Now, let us deal with exception handling which will make our code to work perfect at all situations. Take an instance of a user trying to select a choice that is not availble in choice list and our application should not get freezed or turn buggy. At this point we can make use of 'ValidationError' class which can be used for serializer and field validations.

The model Serializer class in Django Rest Framework has the default implementations of '.create()' and '.update()'. We can make use fo the '.create()' here. Let us do it right away in the pollsapi/serializers.py.

.. code-block:: python

    class VoteSerializer(serializers.ModelSerializer):
        class Meta:
            model = Vote
            validators=[
                UniqueTogetherValidator(
                    queryset=Vote.objects.all(),
                    fields=('poll', 'voted_by'),
                    message="User already voted for this poll"
                )
            ]

        def create(self, validated_data):
            poll = validated_data["poll"]
            choice = validated_data["choice"]
            if not choice in poll.choices.all():
                raise serializers.ValidationError('Choice must be valid.')
            vote = super(VoteSerializer, self).create(validated_data)
            return vote

In the above lines of code in the 'create()' we were checking whether the selected choice is a valid one or not. And if turns to be false a validation error will be raised.

We have got another place where we need to handle an exception. If the user forgot to create the choices while starting a new poll an exception needs to be raised that the choices needs to be created as well. For that, make the below changes in the PollSerializer method in the pollsapi/serializers.py

.. code-block:: python

    class PollSerializer(serializers.ModelSerializer):
        choices = ChoiceSerializer(many=True, read_only=True, required=False)
    
        class Meta:
            model = Poll
    
        def create(self, validated_data):
            choice_strings = self.context.get("request").data.get("choice_strings")
            if not choice_strings:
                raise serializers.ValidationError('choice_strings needed.')
            poll = super(PollSerializer, self).create(validated_data)
            for choice in choice_strings:
                Choice.objects.create(poll=poll, choice_text=choice)
            return poll

So the above fixes makes sure that no bugs comes to light and turns the code to run smooth.

