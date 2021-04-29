from bson.json_util import dumps, loads
from flask_pymongo import PyMongo


class Collection():
    def __init__(self, app, collection_name):
        mongo = PyMongo(app)
        self.collection = mongo.db[collection_name]

    def find_and_jsonify(self, condition):
        docs = self.collection.find(filter=condition)
        return dumps(docs, indent=4)

    def replace_many(self, condition, replacement):
        replacement = loads(replacement)
        self.collection.delete_many(condition)
        self.collection.insert_many(replacement)
