Views and Generic Views
============================

In this chapter, we will create views using :code:`APIVIew`, and :code:`generics.ListCreateAPIView` and family.

Creating Views with :code:`APIView`
-----------------------------------------


To start with, we will use the :code:`APIView` to build the polls list and poll detail API we built in the chapter, doc:apis-without-drf:.

Add this to a new file :code:`polls/apiviews.py`

.. code-block:: python

    class PollList(APIView):
        def get(self, request):
            polls = Poll.objects.all()[:20]
            data = PollSerializer(polls, many=True).data
            return Response(data)



    class PollDetail(APIView):
        def get(self, request, pk):
            poll = get_object_or_404(Poll, pk=pk)
            data = PollSerializer(poll).data
            return Response(data)


And change your :code:`urls.py` to

.. code-block:: python

    from django.urls import path

    from .apiviews import PollList, PollDetail

    urlpatterns = [
        path("polls/", PollList.as_view(), name="polls_list"),
        path("polls/<int:pk>/", PollDetail.as_view(), name="polls_detail")
    ]

DRF comes with a browsable api, so you can directly open :code:`http://localhost:8000/polls/` in the browser. It looks like this


.. image:: browsable-api-poll-details.png


You can now do an :code:`options` request to `/polls/`, which gives

.. code-block:: json


    {
        "name": "Poll List",
        "description": "",
        "renders": [
            "application/json",
            "text/html"
        ],
        "parses": [
            "application/json",
            "application/x-www-form-urlencoded",
            "multipart/form-data"
        ]
    }


This is how it looks like in postman.

.. image:: postman-poll-detail-options.png

Using DRF generic views to simplify code
-----------------------------------------


The :code:`PollList` and :code:`PollDetail` get the work done, but there are bunch of common operations, we can abstract away.

The generic views of Django Rest Framework help us in code reusablity. They infer the response format and allowed methods from the serilizer class and base class.

Change your :code:`apiviews.py` to the below code, and leave urls.py as is.

.. code-block:: python

    from rest_framework import generics

    from .models import Poll, Choice
    from .serializers import PollSerializer, ChoiceSerializer,\
        VoteSerializer


    class PollList(generics.ListCreateAPIView):
        queryset = Poll.objects.all()
        serializer_class = PollSerializer


    class PollDetail(generics.RetrieveDestroyAPIView):
        queryset = Poll.objects.all()
        serializer_class = PollSerializer

With this change, GET requests to :code:`/polls/` and :code:`/polls/<pk>/`, continue to work as was, but we have a more data available with OPTIONS.

Do an OPTIONs request to :code:`/polls/`, and you will get a response like this.

.. code-block:: javascript

    {
        "name": "Poll List",
        "description": "",
        "renders": [
            "application/json",
            "text/html"
        ],
        "parses": [
            "application/json",
            "application/x-www-form-urlencoded",
            "multipart/form-data"
        ],
        "actions": {
            "POST": {
                "id": {
                    "type": "integer",
                    "required": false,
                    "read_only": true,
                    "label": "ID"
                },
                // ...
                },
                "question": {
                    "type": "string",
                    "required": true,
                    "read_only": false,
                    "label": "Question",
                    "max_length": 100
                },
                "pub_date": {
                    "type": "datetime",
                    "required": false,
                    "read_only": true,
                    "label": "Pub date"
                },
                "created_by": {
                    "type": "field",
                    "required": true,
                    "read_only": false,
                    "label": "Created by"
                }
            }
        }
    }

This tells us

* Our API now accepts POST
* The required data fields
* The type of each data field.

Pretty nifty! This is what it looks like in Postman.


.. image:: postman-options-2.png

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


When writting a generic view we will override the view and set several calss attributes.

Let us have a look in to the important parts in the code.

- queryset: This will be used to return objects from the view.
- serializer_class: This will be used for validating and deserializing the input and for seraizling the output.
