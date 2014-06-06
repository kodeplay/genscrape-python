Quickstart
==========

Genscrape Client is the API Client library for Genscrape. To use the
Genscrape API, you will need to have an account there and a valid API
key and secret. To create an account, send an email to
`genscrape@kodeplay.com <genscrape@kodeplay.com>`_.


Dependencies
------------

The only dependency is `requests-oauthlib
<https://pypi.python.org/pypi/requests-oauthlib/0.4.0>`_.


Installation
------------

This library is yet to be packaged and published to PyPI. Till then,
just clone the git repository and run, ::

    $ python setup.py install


Preferably install inside a virtualenv.


Usage and Examples
------------------

GenscapeAPI object
~~~~~~~~~~~~~~~~~~

The user only needs to instantiate the ``GenscrapeAPI`` instance and
then call it's ``for_resource`` method with a resource name to get a
resource manager instance. The resource manager has methods that can
then be called to send requests to the API. ::

    >>> api = GenscrapeAPI(base_url, api_key, api_secret)
    >>> api.resources
    ['scrapers', 'crawls', 'crawled_items']
    >>> scrapers = api.for_resource('scrapers')
    >>> scrapers.get(9)
    ...
    ...
    ...
    >>> crawls = api.for_resource('crawls')
    >>> crawls.start(9)
    ...
    ...
    ...
    >>> items = api.for_resource('crawled_items')
    >>> for item in items.all():
    ...     print(item)
