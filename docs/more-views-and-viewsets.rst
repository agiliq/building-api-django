More views and viewsets
======================================

A better URL structure
-----------------------------

We have three API endpoints

- :code:`/polls/` and :code:`/polls/<pk>/`
- :code:`/choices/`
- :code:`/vote/`

They get the work done, but we can make our API more intuitive by nesting them correctly. Our redesigned urls look like this:

- :code:`/polls/` and :code:`/polls/<pk>`
- :code:`/polls/<pk>/choices/` to GET the choices for a specific poll, and to create choices for a specific poll. (Idenitfied by the :code:`<pk>`)
- :code:`/polls/<pk>/choices/<choice_pk>/vote/` - To vote for the choice identified by :code:`<choice_pk>` under poll with :code:`<pk>`.

Changing the views
-----------------------------

We will make changes to :code:`ChoiceList` and :code:`CreateVote`, because the :code:`/polls/` and :code:`/polls/<pk>` have not changed.

.. code-block:: python

    from rest_framework import generics
    from rest_framework.views import APIView
    from rest_framework import status
    from rest_framework.response import Response

    from .models import Poll, Choice
    from .serializers import PollSerializer, ChoiceSerializer, VoteSerializer

    # ...
    # PollList and PollDetail views

    class ChoiceList(generics.ListCreateAPIView):
        def get_queryset(self):
            queryset = Choice.objects.filter(poll_id=self.kwargs["pk"])
            return queryset
        serializer_class = ChoiceSerializer


    class CreateVote(APIView):
        serializer_class = VoteSerializer
        
        def post(self, request, pk, choice_pk):
            voted_by = request.data.get("voted_by")
            data = {'choice': choice_pk, 'poll': pk, 'voted_by': voted_by}
            serializer = VoteSerializer(data=data)
            if serializer.is_valid():
                vote = serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

And change your urls.py to a nested structure.

.. code-block:: python

    #...
    urlpatterns = [
        path("polls/<int:pk>/choices/", ChoiceList.as_view(), name="choice_list"),
        path("polls/<int:pk>/choices/<int:choice_pk>/vote/", CreateVote.as_view(), name="create_vote"),

    ]


You can see the changes by doing a GET to :code:`http://localhost:8000/polls/1/choices/`, which should give you.

.. code-block:: json

    [
        {
            "id": 1,
            "votes": [],
            "choice_text": "Flask",
            "poll": 1
        },
        {
            "id": 2,
            "votes": [
            ],
            "choice_text": "Django",
            "poll": 1
        }
    ]

You can vote for choices 2, of poll 1 by doing a POST to :code:`http://localhost:8000/polls/1/choices/2/vote/` with data :code:`{"voted_by": 1}`.

.. code-block:: json

    {
        "id": 2,
        "choice": 2,
        "poll": 1,
        "voted_by": 1
    }

Lets get back to :code:`ChoiceList`.

.. code-block:: python

    # urls.py
    #...
    urlpatterns = [
        # ...
        path("polls/<int:pk>/choices/", ChoiceList.as_view(), name="choice_list"),
    ]

    # apiviews.py
    # ...

    class ChoiceList(generics.ListCreateAPIView):
        def get_queryset(self):
            queryset = Choice.objects.filter(poll_id=self.kwargs["pk"])
            return queryset
        serializer_class = ChoiceSerializer

From the urls, we pass on :code:`pk` to :code:`ChoiceList`. We override the :code:`get_queryset` method, to filter on choices with this :code:`poll_id`, and let DRF handle the rest.


And for :code:`CreateVote`,

.. code-block:: python

    # urls.py
    #...
    urlpatterns = [
        # ...
        path("polls/<int:pk>/choices/<int:choice_pk>/vote/", CreateVote.as_view(), name="create_vote"),
    ]

    # apiviews.py
    # ...

    class CreateVote(APIView):

        def post(self, request, pk, choice_pk):
            voted_by = request.data.get("voted_by")
            data = {'choice': choice_pk, 'poll': pk, 'voted_by': voted_by}
            serializer = VoteSerializer(data=data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

We pass on poll id and choice id. We subclass this from :code:`APIView`, rather than a generic view, because we competely customize the behaviour. This is similar to our earlier :code:`APIView`, where in we are passing the data to a serializer, and saving or returning an error depending on whether the serializer is valid.

Introducing Viewsets and Routers
-----------------------------------

Our urls are looking good, and we have a views with very little code duplication, but we can do better.

The :code:`/polls/` and :code:`/polls/<pk>/` urls require two view classes, with the same serializer and base queryset. We can group them into a viewset, and connect them to the urls using a router.

This is what it will look like:

.. code-block:: python

    # urls.py
    # ...
    from rest_framework.routers import DefaultRouter
    from .apiviews import PollViewSet


    router = DefaultRouter()
    router.register('polls', PollViewSet, base_name='polls')


    urlpatterns = [
        # ...
    ]

    urlpatterns += router.urls

    # apiviews.py
    # ...
    from rest_framework import viewsets

    from .models import Poll, Choice
    from .serializers import PollSerializer, ChoiceSerializer, VoteSerializer


    class PollViewSet(viewsets.ModelViewSet):
        queryset = Poll.objects.all()
        serializer_class = PollSerializer

There is no change at all to the urls or to the responses. You can verify this by doing a GET to
:code:`/polls/` and :code:`/polls/<pk>/`.


Choosing the base class to use
-----------------------------------

We have seen 4 ways to build API views until now

- Pure Django views
- :code:`APIView` subclasses
- :code:`generics.*` subclasses
- :code:`viewsets.ModelViewSet`

So which one should you use when? My rule of thumb is,

- Use :code:`viewsets.ModelViewSet` when you are going to allow all or most of CRUD operations on a model.
- Use :code:`generics.*` when you only want to allow some operations on a model
- Use :code:`APIView` when you want to completely customize the behaviour.

Next steps
-----------------

In the next chapter, we will look at adding access control to our apis.
