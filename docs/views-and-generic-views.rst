Views and Generic Views
============================


Creating Views
----------------

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


When writting a generic view we will override the view and set several calss attributes.

Let us have a look in to the important parts in the code.

- queryset: This will be used to return objects from the view.
- serializer_class: This will be used for validating and deserializing the input and for seraizling the output.
