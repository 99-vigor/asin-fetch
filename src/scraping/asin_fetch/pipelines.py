from pymongo import MongoClient

# Pipeline object for the pipeline workflow prescribed by Scrapy.
# As spider scraping operations access websites concurrently,
# the items yielded by each spider are processed.
class ASINFetchPipeline(object):
    
    mongo_collection = 'product_info'

    def __init__(self, mongo_url, mongo_db):
        self.mongo_url = mongo_url
        self.mongo_db = mongo_db

    # Overrides command line invocation; allows user to pass additional
    # arguments to __init__. Inject database dependencies in the constructor
    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            mongo_url = crawler.settings.get('MONGO_URL'),
            mongo_db = crawler.settings.get('MONGO_DB')
        )

    def open_spider(self, spider):
        self.client = MongoClient(self.mongo_url.strip())
        self.db = self.client[self.mongo_db]

    def close_spider(self, spider):
        self.client.close()

    def process_item(self, item, spider):
        # Upsert this ASIN product info entry into the database
        self.db[self.mongo_collection].replace_one(
            { "asin": item['asin'] }, 
            dict(item),
            upsert=True
        )
        return item
