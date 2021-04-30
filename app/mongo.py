import re
from enum import Enum
from bson.json_util import dumps, loads
from flask_pymongo import PyMongo


class Predicate(Enum):
    NORMAL = 1
    LENGTH = 2
    ISEMPTY = 3


OPS = {'<': '$lt', '>': '$gt', '<=': '$lte', '>=': '$gte',
       '==': '$eq', '!=': '$ne', 'contains': '$regex'}


def parse_expr(expr):
    tokens = re.split('(' + '|'.join(OPS.keys()) + ')', expr)
    tokens = tuple(map(lambda x: x.strip(), tokens))
    return f'{{"{tokens[0]}": {{"{OPS[tokens[1]]}": {tokens[2]}}}}}'


def parse_pred(expr):
    split_by_and = expr.split('&&', 1)
    split_by_or = expr.split('||', 1)

    if len(split_by_and) != 1:
        return f'{{"$and": [{parse_expr(split_by_and[0])}, {parse_pred(split_by_and[1])}]}}'
    elif len(split_by_or) != 1:
        return f'{{"$or": [{parse_expr(split_by_and[0])}, {parse_pred(split_by_and[1])}]}}'
    else:
        return parse_expr(expr)


class Collection():
    def __init__(self, app, collection_name):
        mongo = PyMongo(app)
        self.collection = mongo.db[collection_name]
        self.query_predicate = Predicate.NORMAL
        self.expect_editor = False

    def _find_and_jsonify(self):
        docs = self.collection.find(self.condition)
        return dumps(docs, indent=4)

    def replace_docs(self, replacement):
        replacement = loads(replacement)
        self.collection.delete_many(self.condition)
        self.collection.insert_many(replacement)

    def parse_query(self, query):
        if query == '':
            self.condition = {}
            return

        if query.startswith('length'):
            query = query[len('length'):]
            self.query_predicate = Predicate.LENGTH
        elif query.startswith('isempty'):
            query = query[len('isempty'):]
            self.query_predicate = Predicate.ISEMPTY

        self.condition = eval(parse_pred(query))

    def execute_query(self):
        # print(self.condition, file=sys.stdout)
        if self.query_predicate == Predicate.LENGTH:
            self.expect_editor = False
            return f'Length is {self.collection.count_documents(self.condition)}'
        elif self.query_predicate == Predicate.ISEMPTY:
            self.expect_editor = False
            return self.collection.count_documents(self.condition) == 0

        self.expect_editor = True
        return self._find_and_jsonify()
