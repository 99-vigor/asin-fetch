import scrapy

# Scrapy serialization of fetched product information
class ProductInfoItem(scrapy.Item):
    asin = scrapy.Field()
    category = scrapy.Field()
    rank = scrapy.Field()
    dimensions = scrapy.Field()

