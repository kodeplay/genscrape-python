API Reference
=============


GenscrapeAPI
------------

The GenscrapeAPI is the main object to be instantiated by the user by
passing the base url of the genscrape service, the api key and api
secret. Then the ``for_resource`` method can be used to obtain a new
instance of the resource manager by passing the name of the resource.

.. autoclass:: genscrapeclient.GenscrapeAPI
    :members:


Resource Managers
-----------------

A resource manager is just an container object for grouping the API
calls related to a single resource. In this case, there are 3 types of
resources - 

* scrapers
* crawls
* crawled_items

Hence the 3 resource managers are as follows,

.. autoclass:: genscrapeclient.Scrapers
    :members:

.. autoclass:: genscrapeclient.Crawls
    :members:

.. autoclass:: genscrapeclient.CrawledItems
    :members:
