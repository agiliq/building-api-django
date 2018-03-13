from django.urls import path

from .apiviews import PollList, PollDetail, ChoiceList, CreateVote

urlpatterns = [
    path("polls/", PollList.as_view(), name="polls_list"),
    path("polls/<int:pk>/", PollDetail.as_view(), name="polls_detail"),
    path("choices/", ChoiceList.as_view(), name="polls_list"),
    path("vote/", CreateVote.as_view(), name="polls_list"),

]
