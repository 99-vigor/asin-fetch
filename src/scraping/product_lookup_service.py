import subprocess
from subprocess import call
import os
import sys
import shlex
from app_config import MONGO_URL, DB_NAME

class ProductLookupService(object):
    def updateInfo(self, asin):
        # Trigger the listing_spider pipeline from within the scraping module
        # We need execution within the scraping module for scrapy-related settings in that scope
        command = shlex.split('scrapy crawl listing_spider -a asin="{}" -s MONGO_URL={} -s MONGO_DB={}'.format(asin, MONGO_URL, DB_NAME))
        call(command, cwd=os.path.join(os.path.dirname(sys.argv[0]), "scraping"))
        