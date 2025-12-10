#!/usr/bin/env python
import sys
import networkx as nx
import itertools as it
import heapq

from math import dist, prod
from parse import parse

def part_1(rawdata, connections):
    g = nx.Graph()
    g.add_nodes_from(tuple(parse("{:d},{:d},{:d}", line)) for line in rawdata.splitlines())

    for a,b in heapq.nsmallest(connections, it.combinations(g,2), key=lambda x: dist(*x)):
        g.add_edge(a,b)

    return str(prod(len(c) for c in heapq.nlargest(3, nx.connected_components(g), key=len) ))


def part_2(rawdata):
    g = nx.Graph()
    g.add_nodes_from(tuple(parse("{:d},{:d},{:d}", line)) for line in rawdata.splitlines())

    for a,b in sorted(it.combinations(g,2), key=lambda x: dist(*x)):
        g.add_edge(a,b)

        if nx.is_connected(g):
            return str(a[0] * b[0])

    raise ValueError("uhh..")

from aocd import puzzle, submit
import pytest

@pytest.mark.parametrize("data, result",
     [(ex.input_data, ex.answer_a) for ex in puzzle.examples])
def test_part_1(data, result):
    assert part_1(data, 10) == result

@pytest.mark.parametrize("data, result",
     [(ex.input_data, ex.answer_b) for ex in puzzle.examples])
def test_part_2(data, result):
    assert part_2(data) == result

if __name__ == "__main__":
    res = pytest.main([__file__])
    if res:
        sys.exit(res.value)

    submit(part_1(puzzle.input_data, 1000), part="a", reopen=False)
    submit(part_2(puzzle.input_data), part="b", reopen=False)
