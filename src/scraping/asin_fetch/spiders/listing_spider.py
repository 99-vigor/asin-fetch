from scrapy import Spider
from ..items import ProductInfoItem
import re

class ListingSpider(Spider):
    KEY_ASIN = "asin"
    KEY_DIMENSIONS = "dimensions"
    KEY_CATEGORY = "category"
    KEY_RANK = "rank"
    
    name = "listing_spider"
    allowed_domains = [ "amazon.com" ]

    def __init__(self, *args, **kwargs): 
      super(ListingSpider, self).__init__(*args, **kwargs)
      self.start_urls = [ "https://www.amazon.com/dp/" + kwargs.get('asin') ] 

    def extract_asin(self, url):
        maybe_asin = re.match(r'^.*/dp/([A-Z0-9]{10}).*$', url)
        if not maybe_asin:
            return None
        else:
            return maybe_asin.group(1)

    def extract_categories(self, selector):
        category_nodes = selector.xpath('//div[@id="wayfinding-breadcrumbs_feature_div"]/ul/li/span[@class="a-list-item"]/a/text()')
        if not category_nodes:
            return []
        else:
            return list(map(lambda node: node.get().strip(), category_nodes))

    def extract_dimensions_tableform(self, selector):
        result = selector.xpath('//tr[@class="size-weight"]/td[text()="Product Dimensions"]/../td[@class="value"]/text()')
        if not result:
            return None
        else:
            return result.get().strip()

    def extract_rank_tableform(self, selector):
        raw_rank = selector.xpath('//tr[@id="SalesRank"]/td[@class="value"]/ul[@class="zg_hrsr"]/li[1]/span[@class="zg_hrsr_rank"]/text()') # In form '#{number}'
        if not raw_rank:
            return None
        else:
            return int(raw_rank.get().strip()[1:])

    def extract_dimensions_listform(self, selector):
        result = selector.xpath('//tr/th[contains(@class, "prodDetSectionEntry") and contains(text(), "Product Dimensions")]/../td/text()')
        if not result:
            return None
        else:
            return result.get().strip()

    def extract_rank_listform(self, selector):
        raw_rank = selector.xpath('//tr/th[contains(text(), "Best Sellers Rank")]/../td/span/span[2]/text()') # In form '#{number} in'
        if not raw_rank:
            return None
        else:
            regex_results = re.match('^#([0-9]+) in', raw_rank.get().strip())
            if not regex_results:
                return None
            else:
                return int(regex_results.group(1))

    def process(self, response):
        product_item = ProductInfoItem()
        # Parse ASIN
        product_item['asin'] = self.extract_asin(response.request.url)
        # Parse Category
        product_item['category'] = self.extract_categories(response.selector)
        # Parse Rank and Dimensions
        list_element_selectors = response.selector.xpath('//table[@id="productDetails_detailBullets_sections1"]')
        if(len(list_element_selectors) > 0):
            # List-style Product Details Case
            product_item['dimensions'] = self.extract_dimensions_listform(response.selector)
            product_item['rank'] = self.extract_rank_listform(response.selector)
        else:
            # Table-style Product Details Case
            table_element_selector = response.selector.xpath('//div[@id="prodDetails"]')
            product_item['dimensions'] = self.extract_dimensions_tableform(table_element_selector)
            product_item['rank'] = self.extract_rank_tableform(response.selector)
        return product_item

    def parse(self, response):
        return self.process(response)