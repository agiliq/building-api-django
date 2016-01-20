Chapter 5
==============

In this chapater we will see how to use swagger for all the views of our API.

Swagger is a tool used to understand the capabilities of the service without access to source code, documentation, or through network traffic inspection. In simple terms, with swagger you can see what all API end points are available for a web application. You can use swagger for testing the requests and responses of the API endpoints.

Now lets us use swagger to our polls application.

Hosting Swagger UI
----------------------

Firstly we need to host the swagger UI in order to view all the API endpoints. so we'll first clone the swagger UI from github.

.. code-block:: python

    git clone

As swagger UI is a simple web application, you can host it using any of the hosting methods (apache, nginx, python's simple http server ) which you are familiar with.

For simplicity purposes we'll use python's SimpleHTTPServer. Change the working directory to the above cloned folder i.e., swagger-ui and run the following command to start simple http server.

.. code-block:: python

    cd swagger-ui
    python -m SimpleHTTPServer 8000

Now that we have the swagger UI running and you can see this by going to url http://localhost:8000/ in your browser.


JSON representation of the API
---------------------------------

To view all the API endpoints, we need to specify them in a JSON file with the following format. You may call it pollaspi.json.

.. code-block:: python

    {
        "swagger": "2.0",
        "info": {
            "description": "This is a sample server for polls api.",
            "version": "1.0.0",
            "title": "Polls API",
            "termsOfService": "http://example.com/terms/",
            "contact": {"email": "apiteam@example.com"},
            "license": {"name": "Apache 2.0", "url": "http://www.apache.org/licenses/LICENSE-2.0.html"}
        },
        "host": "polls.example.com",
        "basePath": "/v2",
        "tags": [
            {
                "name": "polls",
                "description": "Everything about your Polls",
                "externalDocs": {"description": "Find out more","url":"http://example.com"}
            },
            {
                "name": "choices",
                "description": "Access to choices for the polls"
            },
            {
                "name": "user",
                "description": "Operations about user",
                "externalDocs": {"description": "Find out more about our store","url":"http://example.com"}
            }
        ],
        "schemes": ["http"],
        "paths": {
            "/polls": {
                "get": {
                    "tags": ["poll"],
                    "summary": "Get all the polls",
                    "description": "",
                    "operationId": "pollList",
                    "consumes": ["application/json","application/xml"],
                    "produces": ["application/xml","application/json"],
                    "parameters": [{
                        "in": "query",
                        "name": "body",
                        "description": "Get all the polls.",
                        "required": false,
                        "schema":{"$ref":"#/pollsapi/Poll"}
                    }],
                    "responses": {"200":{"description":"Successfull operation"}},
                },
                "post":{
                    "tags": ["poll"],
                    "summary": "Create a new poll",
                    "description": "Creates a new poll.",
                    "operationId": "createPoll",
                    "consumes":["application/json","application/xml"],
                    "produces":["application/xml","application/json"],
                    "parameters":[{
                        "in":"query",
                        "name":"body",
                        "description": "Poll object that needs to be added.",
                        "required": true,
                        "schema": {"$ref":"#/pollsapi/Poll"}
                    }],
                    "responses": {
                        "200": {"description":"Poll created successfully"}
                    }
                }
            },
            "/choices": {
                "get": {
                    "tags": ["choice"],
                    "summary": "Get all the choices",
                    "description": "",
                    "operationId": "choiceList",
                    "consumes": ["application/json","application/xml"],
                    "produces": ["application/xml","application/json"],
                    "parameters": [{
                        "in": "query",
                        "name": "body",
                        "description": "Get all the choices.",
                        "required": false,
                        "schema":{"$ref":"#/pollsapi/Choice"}
                    }],
                    "responses": {"200":{"description":"Successfull operation"}},
                },
                "post":{
                    "tags": ["choice"],
                    "summary": "Create a new choice",
                    "description": "Creates a new choice.",
                    "operationId": "createChoice",
                    "consumes":["application/json","application/xml"],
                    "produces":["application/xml","application/json"],
                    "parameters":[{
                        "in":"query",
                        "name":"body",
                        "description": "Choice object that needs to be added.",
                        "required": true,
                        "schema": {"$ref":"#/pollsapi/Poll"}
                    }],
                    "responses": {
                        "200": {"description":"Poll created successfully"}
                    }
                }
            }
        }
    }


This JSON file should also be available/hosted somewhere in order to access from swagger UI.

Lets use the same python's SimpleHTTPServer for hosting this JSON file but on a different port. In your terminal cd to the directory where the JSON file is located and run the following command.

.. code-block:: python

    python -m SimpleHTTPServer 8001


Now open the swagger UI in your browser from http://localhost:8000/ and enter http://localhost:8000/pollsapi.json in the url textbox and click explore to view all the API endpoints of the service.


Note
--------

You may get errors while running both swagger and the JSON file with SimpleHTTPServer locally saying "It may not have the appropriate access-control-origin settings." That's because the server running swagger doesn't have access over the other server. In order to resolve this, we need give the access control. We can do this by writing a custom class and running the server using this. We'll write the custom class in a seperate file called simple-cors-http-server.py.


.. code-block:: python

    #! /usr/bin/env python2
    from SimpleHTTPServer import SimpleHTTPRequestHandler
    import BaseHTTPServer

    class CORSRequestHandler (SimpleHTTPRequestHandler):
        def end_headers (self):
            self.send_header('Access-Control-Allow-Origin', '*')
            SimpleHTTPRequestHandler.end_headers(self)

    if __name__ == '__main__':
        BaseHTTPServer.test(CORSRequestHandler, BaseHTTPServer.HTTPServer)

Now we may run this (simple-cors-http-server.py) file to serve the JSON file, which will allow swagger UI to access this file.
