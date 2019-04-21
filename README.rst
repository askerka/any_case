.. highlight:: python

any_case
========

When developing a web application, you often have to choose the format (snake_case/camelCase)
will be used for the input and the output json data. If the backend is written in python,
the easiest option is to choose snake_case. On the one hand, this is good, because we have
an obvious consistency, but on the other hand, the main consumers of the API (mobile and browser)
prefer to use camelCase.

If we care about our consumers, we will change the case to camelCase. And it's good if we think
about it in advance, before publishing API. But if this happens in an existing application,
it becomes much more difficult to do so because there are consumers using the existing API.
We have two options here:

  - introduce a new version of the api
  - send data in two cases at once

The second option increases the size of the data, and the first option forces us to support two
versions of the API without serious need. These options complicate the support and development of API.

Things get a little more complicated when we have consumers who natively use snake_case,
and using camelCase for them is not an option at all.

As you can see, the use of one notation does not improve, but may worsen the situation.

But why do we have to choose for the customer which version of the notation they use?
Why customers do not send and not receive data in the format, which would be more convenient to them?


That's what this library is for. Consumers choose in what case they expect the data.
If they specified an incorrect case or made a request without specifying a case,
the data will be given as is.

This approach allows existing consumers to work without changes with existing API, and for those
consumers who want to use a single format, allows granular rewriting of the application.

Installation
============
::

    pip install any_case

Usage
=====
For converting dict or list use `converts_keys` function::

    >>> from any_case import converts_keys
    >>> data = {'camelCaseKey': 'value'}
    >>> converts_keys(data, case='snake')
    {'camel_case_key': 'value'}
    >>> data = {'snake_case': 'camelCase'}
    >>> converts_keys(data, case='camel')
    {'snakeCase': 'camelCase'}
    >>>
For converting `any_case` uses compiled regex and stack for objects traversal.

To convert text, use `to_snake_case` or `to_camel_case`::

    >>> from any_case import to_snake_case, to_camel_case
    >>> to_snake_case('snakeCase')
    'snake_case'
    >>> to_camel_case('snake_case')
    'snakeCase'

Integrations
============

Django
------

For integration with the Django framework, you need to add any_case middleware::

    MIDDLEWARE = [
        'django.contrib.sessions.middleware.SessionMiddleware',
        ...
        'any_case.contrib.django.middleware.KeysConverterMiddleware'
    ]


When the input data is converted, it is saved in the `json` field of request object.
That is, you can access to the converted data in the view as follows::

    def view(request):
        data = request.json
        ...

rest_framework
--------------

For integration with rest_framework, replace default json parser and renderer::

    REST_FRAMEWORK = {
        'DEFAULT_RENDERER_CLASSES': (
            'any_case.contrib.rest_framework.AnyCaseJSONParser',
            ...
        ),
        'DEFAULT_PARSER_CLASSES': (
            'any_case.contrib.rest_framework.AnyCaseJSONRenderer',
            ...
        )
    }


Settings
--------
`any_case` has the next default settings::

    ANY_CASE = {
        'HEADER_KEY': 'Accept-Json-Case',
        'QUERY_KEY': None,
        'BODY_KEY': None,
        'CONVERT_INPUT_JSON': True
    }

`any_case` can be used for converting input json data to snake_case and for converting
output json to snake_case or camelCase. Or only one of the above independently.

You can specify the format in the header, in the query parameters, or in the json body.
The preferred way is the header, because specifying in the query or in the body
is not always possible. Specifying case format in the body also forces to parse json data that
may not be needed at all.


Disable converting output data
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
 ::

    ANY_CASE = {
        'HEADER_KEY': None,
        'QUERY_KEY': None,
        'BODY_KEY': None,
    }

Disable converting input data
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

 ::

    ANY_CASE = {
        'CONVERT_INPUT_JSON': False
    }
