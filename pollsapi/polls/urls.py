from django.urls import path

from .apiviews import PollViewSet, ChoiceList, CreateVote

from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('polls', PollViewSet, base_name='polls')


urlpatterns = [
    path("polls/<int:pk>/choices/", ChoiceList.as_view(), name="polls_list"),
    path("polls/<int:pk>/choices/<int:choice_pk>/vote/", CreateVote.as_view(), name="polls_list"),

]

urlpatterns += router.urls
