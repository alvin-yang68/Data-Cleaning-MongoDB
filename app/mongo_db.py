import re
from bson.json_util import dumps, loads
from flask_pymongo import PyMongo


OPS = {'<': '$lt', '>': '$gt', '<=': '$lte', '>=': '$gte',
       '==': '$eq', '!=': '$ne', 'contains': '$regex'}


def parse_subexpr(expr):
    tokens = re.split('(' + '|'.join(OPS.keys()) + ')', expr)
    tokens = [t.strip() for t in tokens]
    return f'{{"{tokens[0]}": {{"{OPS[tokens[1]]}": {tokens[2]}}}}}'


def parse(expr):
    split_by_and = expr.split('&&', 1)
    split_by_or = expr.split('||', 1)

    if len(split_by_and) != 1:
        return f'{{"$and": [{parse_subexpr(split_by_and[0])}, {parse(split_by_and[1])}]}}'
    elif len(split_by_or) != 1:
        return f'{{"$or": [{parse_subexpr(split_by_and[0])}, {parse(split_by_and[1])}]}}'
    else:
        return parse_subexpr(expr)


class MongoDriver():
    def __init__(self, app, collection_name):
        mongo = PyMongo(app)
        self.collection = mongo.db[collection_name]
        self.expect_replacement = False

    def _find_and_jsonify(self, condition):
        docs = self.collection.find(condition)
        return dumps(docs, indent=4)

    def replace_docs(self, replacement):
        replacement = loads(replacement)
        self.collection.delete_many(self.condition)
        self.collection.insert_many(replacement)

    def execute_user_query(self, query):
        if query == '':
            self.condition = {}

        if query.startswith('length'):
            query = query[len('length'):]
            self.condition = eval(parse(query))
            return f'Length is {self.collection.count_documents(self.condition)}'
        elif query.startswith('isempty'):
            query = query[len('isempty'):]
            self.condition = eval(parse(query))
            return self.collection.count_documents(self.condition) == 0

        # print(self.condition, file=sys.stdout)
        self.condition = eval(parse(query))
        self.expect_replacement = True

        return self._find_and_jsonify(self.condition)
