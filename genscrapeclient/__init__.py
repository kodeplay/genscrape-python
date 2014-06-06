from .rest import JSONRequests, ResourceManager, BaseAPI

from requests_oauthlib import OAuth1Session


class Scrapers(ResourceManager):
    __resourcename__ = 'scrapers'

    def get(self, scraper_id):
        """Gets the scraper from it's id

        :param int scraper_id: Identifier for the scraper
        :returns: the scraper data
        :rtype: dict

        """
        return self.client.get('/scrapers/{}'.format(scraper_id))

    def all(self):
        """Gets all the scrapers

        :returns: list of scrapers
        :rtype: list of dicts

        """
        return self.client.get('/scrapers')

    def create(self, name, config):
        """Creates a new scraper with given name and config

        :param str name: name of the scraper
        :param dict config: the scraper config or spec
        :returns: the newly created scaper
        :rtype: dict

        """
        data = {'name': name, 'config': config}
        return self.client.post('/scrapers', data)

    def delete(self, scraper_id):
        """Deletes a scraper by it's ID

        :param int scraper_id: the identifier of the scraper
        :returns: None
        :rtype: NoneType

        """
        return self.client.delete('/scrapers/{}'.format(scraper_id))

    def update(self, scraper_id, name, config):
        """Update the scraper config and name by sending PUT request.

        :param int scraper_id: id of the scraper
        :param str name: new name of the scraper to set
        :param dict config: new config to set
        :returns: the updated scraper data
        :rtype: dict

        """
        data = {'name': name, 'config': config}
        return self.client.put('/scrapers/{}'.format(scraper_id), data)


class Crawls(ResourceManager):
    __resourcename__ = 'crawls'

    def get(self, crawl_id):
        """Gets a particular crawl by crawl_id

        :param int crawl_id: Id of the crawl
        :returns: the crawl data
        :rtype: dict

        """
        return self.client.get('/crawls/{}'.format(crawl_id))

    def all(self):
        """Gets all crawls for an account

        :returns: all crawls
        :rtype: list of dicts

        """
        return self.client.get('/crawls')

    def start(self, scraper_id):
        """Create a new crawl and begins crawling of sites

        Note that it just triggers the crawling which will take some
        time to fetch all the items. In this state, the status of the
        crawl will be 'crawling' (it can be checked by calling the
        `get` method with the respective crawl_id). Once the crawling
        is complete, the status will be set to 'complete' after which
        it's ok to send request to get the items.

        :param int scraper_id: id of the scraper
        :returns: the newly created crawl
        :rtype: dict

        """
        data = {'scraper_id': scraper_id}
        return self.client.post('/crawls', data)

    def update_status(self, crawl_id, status):
        """Update the status of the crawl

        :param int crawl_id: crawl_id
        :param str status: one of {pending,crawling,complete,cancelled}
        :returns: updated crawl object
        :rtype: dict
        :raises: JSONRequestError in case of error

        """
        data = {'status': status}
        return self.client.patch('/crawls/{}'.format(crawl_id), data)


class CrawledItems(ResourceManager):
    __resourcename__ = 'crawled_items'

    def get_paginated(self, crawl_id, page, per_page):
        """Gets paginated list of crawled items

        :param int crawl_id: id of the crawl
        :param int page: the page to obtain
        :param int per_page: number of items to get per page
        :returns: list of items for the page
        :rtype: list of dicts

        """
        url = '/crawls/{}/items?page={}&per_page={}'.format(crawl_id, page, per_page)
        return self.client.get(url)

    def all(self, crawl_id):
        """Gets all the crawled items by handling pagination internally

        Note that this method will return a lazy generator object so
        it cannot be reused after it's consumed once.

        :param int crawl_id: id of the crawl
        :returns: a lazy generator that can be iterated to get items
        :rtype: generator

        """
        # Here we are dropping down to the actual underlying client
        # object (In this case the OAuth1Session instance)
        c = self.client._client
        r = c.get(self.client.url('/crawls/{}/items'.format(crawl_id)))
        assert r.status_code == 200
        for item in r.json():
            yield item
        next_page = None if 'next' not in r.links else r.links['next']['url']
        while next_page:
            r = c.get(next_page)
            assert r.status_code == 200
            for item in r.json():
                yield item
            next_page = None if 'next' not in r.links else r.links['next']['url']

    def create(self, crawl_id, data):
        """Creates a new item

        :param int crawl_id: id of the crawl
        :param dict data: the item data to store
        :returns: the stored item
        :rtype: dict

        """
        return self.client.post('/crawls/{}/items'.format(crawl_id), data)

    def delete(self, crawl_id):
        """Deletes all items for a crawl

        Irreversible!! Use with caution

        :param int crawl_id: id of the crawl
        :returns: None
        :rtype: NoneType

        """
        return self.client.delete('/crawls/{}/items'.format(crawl_id))


class GenscrapeAPI(BaseAPI):

    def __init__(self, base_url, api_key, api_secret):
        """Initialize the genscrape api object

        :param str base_url: the base url of genscrape api
        :param str api_key: your API key
        :param str api_secret: your API secret

        """
        super(GenscrapeAPI, self).__init__()
        session = OAuth1Session(api_key, api_secret, None, None)
        self.client = JSONRequests(base_url, client=session)

    def for_resource(self, resource):
        """Gets a resource manager by the resource name

        To see all resource names, use the attribute `resources` of
        the genscrape api object.

        Usage:

          >>> api = GenscrapeAPI(.., .., ..)
          >>> api.resources
          ['scrapers', 'crawls', 'crawled_items']
          >>> scrapers = api.for_resource('scrapers')
          >>> scrapers.get(9)

        :param str resource: the name of the resource
        :returns: the resource manager for the resource
        :rtype: ResourceManager

        """
        ResourceManagerCls = self.resource_factory(resource)
        return ResourceManagerCls(self.client)
