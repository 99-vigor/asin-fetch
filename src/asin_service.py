from repository.repository import Repository
from scraping.product_lookup_service import ProductLookupService
import re

class ASINService(object):

    def __init__(self, repo, lookupService):
        self.repo = repo
        self.lookupService = lookupService
        self.asin_regex = re.compile("^[A-Z0-9]{10}$")

    def get_product_info(self, asin):
        # Validate ASIN
        if(re.match(self.asin_regex, asin) == None):
            raise Exception('"{}" is not a valid ASIN.'.format(asin))
        raw_result = self.repo.read({ "asin" : asin })
        if(raw_result == None):
            self.lookupService.updateInfo(asin)
            raw_result = self.repo.read({ "asin" : asin })
        return raw_result
