Chapter 3:
===========

In this chapter we will be dealing with the creation of URLs

Creating URLs
--------------

It's time to wire up the views to specific URLs

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
        url(r'^users/(?P<pk>[0-9]+)/$', pollsapi.views.UserDetail.as_view()),

    ]

In the above lines of code we have created URLs for all the views according to our requirement.

