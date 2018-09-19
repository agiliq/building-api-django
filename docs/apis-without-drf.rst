A simple API with pure Django
========================================

In this chapter, we will build an API with pure Django. We will not use Django Rest Framework (Or any other library).
To start add some :code:`Poll` using the admin.

The endpoints and the URLS
+++++++++++++++++++++++++++++++

Our API will have two endpoints returning data in JSON format.

* :code:`/polls/` GETs list of :code:`Poll`
* :code:`/polls/<id>/` GETs data of a specific :code:`Poll`

Connecting urls to the views
++++++++++++++++++++++++++++++

Write two place holder view functions and connect them in your :code:`urls.py`. We will finish :code:`polls_list` and :code:`polls_detail` shortly.

.. code-block:: python

    # In views.py
    def polls_list(request):
        pass

    def polls_detail(request, pk):
        pass


    # in urls.py
    from django.urls import path
    from .views import polls_list, polls_detail

    urlpatterns = [
        path("polls/", polls_list, name="polls_list"),
        path("polls/<int:pk>/", polls_detail, name="polls_detail")
    ]


Writing the views
++++++++++++++++++++++++

We will now write the :code:`polls_list` and :code:`polls_detail`

.. code-block:: python

    from django.shortcuts import render, get_object_or_404
    from django.http import JsonResponse

    from .models import Poll

    def polls_list(request):
        MAX_OBJECTS = 20
        polls = Poll.objects.all()[:MAX_OBJECTS]
        data = {"results": list(polls.values("question", "created_by__username", "pub_date"))}
        return JsonResponse(data)


    def polls_detail(request, pk):
        poll = get_object_or_404(Poll, pk=pk)
        data = {"results": {
            "question": poll.question,
            "created_by": poll.created_by.username,
            "pub_date": poll.pub_date
        }}
        return JsonResponse(data)

This should be standard Django for you. :code:`polls = Poll.objects.all()[:20]` gets us upto 20 :code:`Poll` objects.
We get a list of dictionaries using :code:`{"results": list(polls.values("question", "created_by__username", "pub_date"))}` and return it with a :code:`JsonResponse`. A :code:`JsonResponse` is a like :code:`HttpResponse` with :code:`content-type=application/json`.

Similarly, `polls_detail` gets a specific Poll using :code:`get_object_or_404(Poll, pk=pk)`, and returns it wrapped in :code:`JsonResponse`.


Using the API
++++++++++++++++++++++++

You can now access the API using curl, wget, postman, browser or any other API consuming tools. Here us the response with curl.

.. code-block:: bash

    $ curl http://localhost:8000/polls/

    {"results": [{"pk": 1, "question": "What is the weight of an unladen swallow?", "created_by__username": "shabda", "pub_date": "2018-03-12T10:14:19.002Z"}, {"pk": 2, "question": "What do you prefer, Flask or Django?", "created_by__username": "shabda", "pub_date": "2018-03-12T10:15:55.949Z"}, {"pk": 3, "question": "What is your favorite vacation spot?", "created_by__username": "shabda", "pub_date": "2018-03-12T10:16:11.998Z"}]}

You should consider using postman or a similar tool. This is how your API looks in Postman.

.. image:: postman_polls_detail.png


Why do we need DRF?
++++++++++++++++++++++++

**(DRF = Django Rest Framework)**

We were able to build the API with just Django, without using DRF, so why do we need DRF?
Almost always, you will need common tasks with your APIs, such as access control, serialization, rate limiting and more.

DRF provides a well thought out set of base components and convenient hook points for building APIs. We will be using DRF in the rest of the chapters.
