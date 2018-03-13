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


Using DRF generic views to simplify code
-----------------------------------------


Let us use generic views of Django Rest Framework for creating our views which will help us in code reusablity. The generic views also aid us in building the API quickly and in mapping the database models.

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
