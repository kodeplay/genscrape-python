from .rest import JSONRequests, ResourceManager, BaseAPI


class Scrapers(ResourceManager):
    __resourcename__ = 'scrapers'

    def get(self, scraper_id):
        return self.client.get('/scrapers/{}'.format(scraper_id))

    def all(self):
        return self.client.get('/scrapers')

    def create(self, name, config):
        data = {'name': name, 'config': config}
        return self.client.post('/scrapers', data)

    def delete(self, scraper_id):
        return self.client.delete('/scrapers/{}'.format(scraper_id))

    def update(self, scraper_id, name, config):
        data = {'name': name, 'config': config}
        return self.client.put('/scrapers/{}'.format(scraper_id), data)


class Crawls(ResourceManager):
    __resourcename__ = 'crawls'

    def get(self, crawl_id):
        return self.client.get('/crawls/{}'.format(crawl_id))

    def all(self):
        return self.client.get('/crawls')

    def start(self, scraper_id):
        data = {'scraper_id': scraper_id}
        return self.client.post('/crawls', data)


class CrawledItems(ResourceManager):
    __resourcename__ = 'crawled_items'

    def get_paginated(self, crawl_id, page, per_page):
        url = '/crawls/{}/items?page={}&per_page={}'.format(crawl_id, page, per_page)
        return self.client.get(url)

    def all(self, crawl_id):
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
        return self.client.post('/crawls/{}/items'.format(crawl_id), data)

    def delete(self, crawl_id):
        return self.client.delete('/crawls/{}/items'.format(crawl_id))


class GenscrapeAPI(BaseAPI):

    def __init__(self, base_url):
        super(GenscrapeAPI, self).__init__()
        self.client = JSONRequests(base_url)

    def for_resource(self, resource):
        ResourceManagerCls = self.resource_factory(resource)
        return ResourceManagerCls(self.client)