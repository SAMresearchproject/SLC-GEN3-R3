"""Compile source-bound arithmetic into current STARBREAKER native calls."""
from fractions import Fraction as F
from pathlib import Path


class Graph:
    def __init__(self):
        self.nodes = []

    def node(self, op, **fields):
        key = 'n' + str(len(self.nodes))
        self.nodes.append(dict(id=key, op=op, **fields))
        return key

    def value(self, value, source):
        return self.node('VALUE', value=str(value), source=source)

    def op(self, op, a, b):
        return self.node(op, left=a, right=b)

    def sum(self, ids):
        out = self.value(0, 'additive identity')
        for key in ids:
            out = self.op('ADD', out, key)
        return out


class Native:
    def __init__(self, session):
        self.session = session
        self.calls = []

    def evaluate(self, graph, purpose):
        before = set(self.session.directory.glob('calls/*/RECEIPT.json'))
        result = self.session.execute('GEN2_SIGNED_LOG',
            {'nodes': graph.nodes, 'representation': 'RATIONAL'}, purpose=purpose)
        if not result['complete'] or any(n['status'] != 'DEFINED' for n in result['nodes']):
            raise ValueError('Native graph is incomplete')
        receipts = set(self.session.directory.glob('calls/*/RECEIPT.json')) - before
        if len(receipts) != 1:
            raise ValueError('Native receipt custody is ambiguous')
        receipt = receipts.pop()
        self.calls.append({'purpose': purpose, 'nodes': len(graph.nodes), 'receipt': str(receipt)})
        return {n['id']: F(n['value']) for n in result['nodes']}, receipt
