import re
from enum import Enum
from neo4j import GraphDatabase, basic_auth
from bson.json_util import dumps, loads
import sys


class Entity(Enum):
    NODE = 1
    RELATIONSHIP = 2


OPS = {'<': '<', '>': '>', '<=': '<=', '>=': '>=',
       '==': '=', '!=': '<>', 'is': 'IS', 'contains': 'CONTAINS'}


def parse_subexpr(expr):
    tokens = re.split('(' + '|'.join(OPS.keys()) + ')', expr)
    tokens = [t.strip() for t in tokens]
    return f'x.{tokens[0]} {OPS[tokens[1]]} {tokens[2]}'


def parse_where_clause(expr):
    split_by_and = expr.split('&&', 1)
    split_by_or = expr.split('||', 1)

    if len(split_by_and) != 1:
        return f'{parse_subexpr(split_by_and[0])} AND {parse_where_clause(split_by_and[1])} '
    elif len(split_by_or) != 1:
        return f'{parse_subexpr(split_by_or[0])} OR {parse_where_clause(split_by_or[1])} '
    else:
        return parse_subexpr(expr)


def parse(driver, expr):
    if driver.query_entity_type == Entity.NODE:
        match_clause = f'MATCH (x:{driver.query_node_label}) '
        return_clause = 'RETURN properties(x), id(x)'
    elif driver.query_entity_type == Entity.RELATIONSHIP:
        start_node = driver.query_start_node_label
        end_node = driver.query_end_node_label
        match_clause = (
            f'MATCH '
            f'({"" if start_node == "*" else f":{start_node}"})'
            f'-[x:{driver.query_relationship_label}]->'
            f'({"" if end_node == "*" else f":{end_node}"}) '
        )
        return_clause = 'RETURN id(startNode(x)), id(endNode(x)), properties(x), id(x)'

    where_clause = 'WHERE ' + \
        parse_where_clause(expr) if expr.strip() != '' else ''

    return match_clause + where_clause + return_clause


class Neo4jDriver:
    def __init__(self, app):
        self._driver = GraphDatabase.driver(
            app.config['NEO4J_URI'],
            auth=basic_auth(app.config['NEO4J_USER'],
                            app.config['NEO4J_PASSWORD'])
        )

    def __del__(self):
        self._driver.close()

    def _read_cypher_query(self, cypher_query):
        self.ids = []
        self.query_props = []

        with self._driver.session(database="neo4j") as session:
            results = session.read_transaction(
                lambda tx: tx.run(cypher_query).data()
            )

            for x in results:
                if self.query_entity_type == Entity.NODE:
                    self.query_props.append(x['properties(x)'])
                elif self.query_entity_type == Entity.RELATIONSHIP:
                    self.query_props.append({
                        'start node ID': x['id(startNode(x))'],
                        'end node ID': x['id(endNode(x))'],
                        'relationship properties': x['properties(x)']
                    })
                self.ids.append(x['id(x)'])

        return dumps(self.query_props, indent=4)

    def _write_cypher_query(self, cypher_query):
        with self._driver.session(database="neo4j") as session:
            session.write_transaction(
                lambda tx: tx.run(cypher_query).data()
            )

    def _replace_nodes(self, new_props):
        for id, query_prop, new_prop in zip(self.ids, self.query_props, new_props):
            if query_prop == new_prop:
                continue

            self._write_cypher_query(
                f'MATCH (n:{self.query_node_label}) '
                f'WHERE id(n) = {id} '
                f'SET n = apoc.convert.fromJsonMap("{new_prop}")'
            )

    def _replace_relationships(self, new_props):
        for id, query_prop, new_prop in zip(self.ids, self.query_props, new_props):
            if query_prop == new_prop:
                continue

            start_label = f'x:{self.query_start_node_label}'
            end_label = f'y:{self.query_end_node_label}' if self.query_end_node_label != '*' else 'y'

            self._write_cypher_query(
                f'MATCH ({start_label})-[r:{self.query_relationship_label}]->({end_label}) '
                f'WHERE id(x) = {new_prop["start node ID"]} AND id(y) = {new_prop["end node ID"]} AND id(r) = {id} '
                f'SET r = apoc.convert.fromJsonMap("{new_prop["relationship properties"]}")'
            )

    def replace_subgraph(self, replacement):
        props = loads(replacement)

        if len(props) != len(self.ids):
            raise Exception('Number of nodes/relationships must NOT change.')

        if self.query_entity_type == Entity.NODE:
            self._replace_nodes(props)
        elif self.query_entity_type == Entity.RELATIONSHIP:
            self._replace_relationships(props)

    def execute_user_query(self, query):
        query = query.split(':')
        labels = [s.strip() for s in query[0].split('-')]

        if len(labels) == 1:
            self.query_entity_type = Entity.NODE
            self.query_node_label = labels[0]
        else:
            self.query_entity_type = Entity.RELATIONSHIP
            self.query_start_node_label = labels[0]
            self.query_relationship_label = labels[1]
            self.query_end_node_label = labels[2]

        try:
            cypher_query = parse(self, expr=query[1].strip())
        except IndexError:
            cypher_query = parse(self, expr='')

        return self._read_cypher_query(cypher_query)
