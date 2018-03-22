Testing and Using API with Postman
==========================================

In this chapter, we'll learn how to use the Postman app for testing our APIs.

Postman can be installed from `the Postman site <https://www.getpostman.com/>`_. It is a versatile tool for working with APIs.

In this books, you will be creating and using APIs. We'll see how we can make use of Postman for this.


Making HTTP request
------------------------

Postman is pretty intutive, but the image below should make the app easy to understand.

.. image:: postman.png

There are 4 key elements in making an HTTP request.

1. URL:
    This specifies to which URL we need to make a request for. In other terms where our API endpoint resides.

2. Method:
    Each API endpoint has a method which serves it's purpose. The methods for eg., can be GET for retrieving some data, POST for creating or updating, DELETE for deleting a record.

3. Headers:
    Headers provide required information about the request or the response or about the object sent in the body. Some times we use authentication headers too, in order to access the API endpoint.

4. Body:
    The request body is where we send the object. The object which may be required for the service.


Response
------------

Response is available in the bottom section, usually in a JSON format, but may also vary depending up on the API service.


Collections
--------------

We can save all the relative API endpoints to collections. In our example, we can save all our polls related endpoints as a collection or all the users related endpoints as another collection. This way all the APIs are organized.


Authentication
---------------

Postman also supports few authentication mechanisms like Basic Auth, Digest Auth and Oauth1. This allows us to use these authentication methods for the APIs.
