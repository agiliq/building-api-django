Documenting API with RAML
============================

In this chapter we will see how to use raml for all the views of our API.

RAML is an acronym for "RESTful API Modeling Language". It is a YAML based language for describing the RESTful APIs. RAML contains certain sections for describing the APIs. Each section has it's purpose and we'll look into each one of these by using our polls application.


1. Root
----------------------

Root section is specifies the basic things like title, baseUri etc. These are applied through out the rest of the API

.. code-block:: python

    #%RAML 0.8
        ---
        title: django polls API
        baseUri: http://api.example.com/{version}
        version: v1
        mediaType: application/json


2. Resources
---------------------

It's important to consider how your API consumers will use your API. So we'll list out all the resources that are available in our API.

.. code-block:: python

    /polls:
    /choices:
    /votes:

Notice that these resources all begin with a slash (/). In RAML, this is how you indicate a resource. Any methods and parameters nested under these top level resources belong to and act upon that resource.

Now, since each of these resources is a collection of individual objects (specific poll, choice), we'll need to define some sub-resources to fill out the collection.

To view all the API endpoints, we need to specify them in a JSON file with the following format. You may call it pollaspi.json.

.. code-block:: python

    /polls:
        /{pollId}:

This lets the API consumer interact with the key resource and its nested resources. For example a GET request to http://api.example.com/polls/1 returns details about the one particular poll whose pollId is 1.


3. Methods
--------------

The above mentioned resources can be accessed via 4 most common HTTP methods(Verbs).

GET - Retrieve the information defined in the request URI.

PUT - Replace the addressed collection. At the object-level, create or update it.

POST - Create a new entry in the collection. This method is generally not used at the object-level.

DELETE - Delete the information defined in the request URI.

You can add as many methods as you like to each resource of your BookMobile API, at any level. However, each HTTP method can only be used once per resource.

Nest the methods to allow developers to perform these actions under your resources. Note that you must use lower-case for methods in your RAML API definition.

.. code-block:: python

    /polls:
        get:
        post:


URI Parameters
---------------

The resources that we defined are collections of smaller, relevant objects.

.. code-block:: python

    /polls:
        /{pollId}:


Query Parameters:
--------------------

Query parameters are used for filtering a collection. We already have collections-based resource types that are further defined by object-based URI parameters. We'll see how we can use query paramters for them.

.. code-block:: python

    /polls:
        get:
            description: Get list of polls
            queryParameters:
                pollId:

An API's resources and methods often have a number of associated query parameters. Each query parameter may have any number of optional attributes to further define it.

Now, we'll specify attributes for the query parameters we defined above.

.. code-block:: python

    /polls:
        get:
            description: Get list of polls
            queryParameters:
                pollId:
                    description: Specify the poll id you want to retrieve
                    type: integer
                    example: 1


Responses:
-------------

Responses MUST be a map of one or more HTTP status codes, and each response may include descriptions, examples.

.. code-block:: python

    responses:
        200:
            body:
                application/json:
                example:
                {
                    "data":
                    {
                        "Id": 1,
                        "question": "Will A be the leader next time?",
                        "created_by": "user1",
                        "pub_date": "08:02:2014"
                    },
                    "success": true,
                    "status": 200
                }
