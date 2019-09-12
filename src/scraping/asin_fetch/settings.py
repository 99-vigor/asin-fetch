# Configurations for the scrapy pipeline.
# More information available at https://doc.scrapy.org/en/latest/topics/settings.html

BOT_NAME = 'asin_fetch'

SPIDER_MODULES = ['asin_fetch.spiders']
NEWSPIDER_MODULE = 'asin_fetch.spiders'

# Heed robots.txt when scraping, ignoring pages designated by author not to index
ROBOTSTXT_OBEY = True

# Pipelines stored in (pipelineName, priority) entries. In this case,
# we operate our ASIN fetch operation with a single pipeline.
ITEM_PIPELINES = {
    'asin_fetch.pipelines.ASINFetchPipeline': 1,
}
