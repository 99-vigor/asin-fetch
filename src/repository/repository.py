# Abstracting layer for Repository classes. Rather than directly interface with
# a database, all operations interact with this class' CRUD API methods which
# themselves interact with some database connector implementation.
class Repository(object):
    def __init__(self, connector):
        self.connector = connector
    
    def create(self, value):
        return self.connector.create(value)

    def read(self, selector):
        return self.connector.read(selector)

    def update(self, selector, value):
        return self.connector.update(selector, value)

    def delete(self, selector):
        return self.connector.delete(selector)