from django.shortcuts import render

# Create your views here.

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
