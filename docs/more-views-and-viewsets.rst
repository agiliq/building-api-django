More views and viewsets
======================================

A better URL structure
-----------------------------

We have three API endpoints

- :code:`/polls/` and :code:`/polls/<pk>/`
- :code:`/choices/`
- :code:`/vote/`

They get the work done, but we can make our API more intutive by nesting them correctly. Our redesigned urls look like this:

- :code:`/polls/` and :code:`/polls/<pk>`
- :code:`/polls/<pk>/choices/` to GET the choices for a specfifc poll, and to create choices for a specific poll. (Idenitfied by the :code:`<pk>`)
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
        path("polls/<int:pk>/choices/", ChoiceList.as_view(), name="polls_list"),
        path("polls/<int:pk>/choices/<int:choice_pk>/vote/", CreateVote.as_view(), name="polls_list"),

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
        path("polls/<int:pk>/choices/", ChoiceList.as_view(), name="polls_list"),
    ]

    # views.py
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
        path("polls/<int:pk>/choices/<int:choice_pk>/vote/", CreateVote.as_view(), name="polls_list"),
    ]

    # views.py
    # ...

    class CreateVote(APIView):

        def post(self, request, pk, choice_pk):
            voted_by = request.data.get("voted_by")
            data = {'choice': choice_pk, 'poll': pk, 'voted_by': voted_by}
            serializer = VoteSerializer(data=data)
            if serializer.is_valid():
                vote = serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

We pass on poll id and choice id. We subclss this from :code:`APIView`, rather than a generic view, because we competely customize the behaviour.
