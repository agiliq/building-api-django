Testing and Continuous Integeration
==========================================


In this chapater we will add test to our API.

DRF provides a few important classes which makes testing APIs simpler. We will be using these classes later in the chapter in our tests.

- :code:`APIRequestFactory`: This is similar to Django's :code:`RequestFactory`. It allows you to create requests with any http method, which you can then pass on to any view method and compare responses.
- :code:`APIClient`: similar to Django's :code:`Client`. You can GET or POST a URL, and test responses.
- :code:`APITestCase`: similar to Django's :code:`TestCase`. Most of your tests will subclass this.

Now lets us write test cases to our polls application.

Creating Test Requests
------------------------
Django's 'Requestfactory' has the capability to create request instances which allow us in testing view functions induvidually. Django Rest Framework has a class called 'APIRequestFactory' which extends the standard Django's  'Requestfactory'. This class contains almost all the http verbs like .get(), .post(), .put(), .patch() et all.

Syntax for Post request:

.. code-block:: python

    factory = APIRequestFactory()
    request = factory.post(uri, post data)

Lets add a test for the polls list.

.. code-block:: python

    from rest_framework.test import APITestCase
    from rest_framework.test import APIRequestFactory

    from polls import apiviews


    class TestPoll(APITestCase):
        def setUp(self):
            self.factory = APIRequestFactory()
            self.view = apiviews.PollViewSet.as_view({'get': 'list'})
            self.uri = '/polls/'

        def test_list(self):
            request = self.factory.get(self.uri)
            response = self.view(request)
            self.assertEqual(response.status_code, 200,
                             'Expected Response Code 200, received {0} instead.'
                             .format(response.status_code))



In the above lines of code, we are trying to access the PollList view. We are asserting that the HTTP response code is 200.

Now run the test command.

.. code-block:: python

    python manage.py test

And it will display the below message.

.. code-block:: bash

    Creating test database for alias 'default'...
    System check identified no issues (0 silenced).
    F
    ======================================================================
    FAIL: test_list (polls.tests.TestPoll)
    ----------------------------------------------------------------------
    Traceback (most recent call last):
      File "/Users/shabda/repos/building-api-django/pollsapi/polls/tests.py", line 19, in test_list
        .format(response.status_code))
    AssertionError: 401 != 200 : Expected Response Code 200, received 401 instead.

    ----------------------------------------------------------------------
    Ran 1 test in 0.002s

    FAILED (failures=1)
    Destroying test database for alias 'default'...

Ouch! Our test failed. This happened because the view is not accessable without authentication. So we need to create a user and test the view after getting authenticated.


Testing APIs with authentication
------------------------------------

To test apis with authentication, a test user needs to be created so that we can make requests in context of that user. Let's create a test user. Change your tests to

.. code-block:: python

    from django.contrib.auth import get_user_model
    # ...

    class TestPoll(APITestCase):
        def setUp(self):
            # ...
            self.user = self.setup_user()

        @staticmethod
        def setup_user():
            User = get_user_model()
            return User.objects.create_user(
                'test',
                email='testuser@test.com',
                password='test'
            )

        def test_list(self):
            request = self.factory.get(self.uri)
            request.user = self.user
            response = self.view(request)
            self.assertEqual(response.status_code, 200,
                             'Expected Response Code 200, received {0} instead.'
                             .format(response.status_code))


Now run the test command.

.. code-block:: python

    python manage.py test

You should get this response

.. code-block:: bash

    Creating test database for alias 'default'...
    System check identified no issues (0 silenced).
    .
    ----------------------------------------------------------------------
    Ran 1 test in 0.119s

    OK
    Destroying test database for alias 'default'...

Let us use the .force_authenticate method and force all requests by the test client every time it access the view. This makes the test user automatically treated as authenticated. This becomes handy while testing API and if we dont want to create a valid authentication credentials everytime we make a request. We shall use the same get() but with authentication added to it. The whole part looks as follows.

.. code-block:: python

    from rest_framework.test import APITestCase
    from rest_framework.test import APIRequestFactory, APIClient, force_authenticate
    from pollsapi.tests.user_setup import setup_user

    from pollsapi import views


    class TestPoll(APITestCase):
        def setUp(self):
            self.factory = APIRequestFactory()
            self.client = APIClient()
            self.user = setup_user()
            self.view = views.PollList.as_view()
            self.uri = '/polls/'

        def test_get(self):
            request = self.factory.get(self.uri)
            force_authenticate(request, self.user)
            response = self.view(request)
            self.assertEqual(response.status_code, 200,
                             'Expected Response Code 200, received {0} instead.'
                             .format(response.status_code))

Let us test it now.

.. code-block:: python

    python manage.py test


    Creating test database for alias 'default'...
    .....
    ----------------------------------------------------------------------
    Ran 1 tests in 0.001s

    OK
    Destroying test database for alias 'default'...

Voilà! The test passed successfully

On the way we shall test the post request in the same manner. We can use the the APIRequestFactory() with post method this time. The syntax looks like this:

.. code-block:: python

    factory = APIRequestFactory()
    factory.post(uri, params)

Let us try creating a new poll by sending the 'question', 'choice_strings' and 'created_by' parameters which needs the Post method. The function looks as follows.

.. code-block:: python

    def test_post_uri(self):
            params = {
                "question": "How are you man?",
                "choice_strings": ["Yo Man", "Not Fine"],
                "created_by": 1
                }
            request = self.factory.post(self.uri, params)
            force_authenticate(request, user=self.user)
            response = self.view(request)
            self.assertEqual(response.status_code, 201,
                             'Expected Response Code 201, received {0} instead.'
                             .format(response.status_code))

And the above function should result us the http code 201 if the test passes succesfully. And we are all done with the stuff. Time to celebrate with the API :)


Continuous integration with CircleCI
---------------------------------------

Maintaining a solid rapport with the ongoing software development process always turns out to be a walk on air. Ensuring a software build integrity and quality in every single commit makes it much more exciting.

If the current software bulid is constantly available for testing, demo or release isn't it a developer's paradise on earth?
Giving a cold shoulder to "Integration hell" the 'Continuous integration' process stands out to deliver all the above assets.

Let us use circle CI software for our App.

We can configure our application to use Circle CI  by adding a file named circle.yml which is a YAML(a human-readable data serialization format) text file. It automatically detects when a commit has been made and pushed to a GitHub repository that is using Circle CI, and each time this happens, it will try to build the project and runs tests. It also builds and once it is completed it notifies the developer in the way it is configured.

Steps to use Circle CI:

- Sign-in: To get started with Circle CI we can sign-in with our github account on circleci.com.
- Activate Github webhook: Once the Signup process gets completed we need to enable the service hook in the github profile page.
- Add circle.yml: We should add the yml file to the project.

Writing circle.yml file
------------------------
In order for circle CI to build our project we need to tell the system a little bit about it. we will be needed to add a file named circle.yml to the root of our repository. The basic options in the circle.yml should contain are language key which tells which language environment to select for our project and other options include the version of the language and command to run the tests, etc.

Below are the keywords that are used in writting circle.yml file.

- machine: adjusting the VM to your preferences and requirements
- checkout: checking out and cloning your git repo
- dependencies: setting up your project's language-specific dependencies
- database: preparing the databases for your tests
- test: running your tests
- deployment: deploying your code to your web servers


- pre: commands run before CircleCI's inferred commands
- override: commands run instead of CircleCI's inferred commands
- post: commands run after CircleCI's inferred commands


Example for circle.yml for python project:

.. code-block:: python

    ## Customize the test machine
    machine:

      timezone:
        Asia/Kolkata # Set the timezone

      # Version of python to use
      python:
        version: 2.7.5

    dependencies:
      pre:
        - pip install -r requirements.txt

    test:
      override:
        - python manage.py test

From now onwards whenever we push our code to our repository a new build will be created for it and the running of the test cases will be taken place. It gives us the potential to check how good our development process is taking place with out hitting a failed test case.







