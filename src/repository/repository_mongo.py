from pymongo import MongoClient

# MongoDB Implementation of Repository.
class RepositoryMongo(object):
    def __init__(self, mongo_url, db_selector, collection_selector):
        self.collection = MongoClient(mongo_url)[db_selector][collection_selector]
    
    def create(self, value):
        return self.collection.insert_one(value)
    
    def read(self, selector):
        return self.collection.find_one(selector)
    
    def update(self, selector, value):
        return self.collection.update(selector, value, upsert=True).modified_count
    
    def delete(self, selector):
        return self.collection.delete_one(selector).deleted_count