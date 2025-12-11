#!/usr/bin/env python
import sys
import networkx as nx
from collections import Counter

def dag_path_count(G, source, target):
    # nx has all_simple_paths which is close to what we want,except:
    #  - it has to calculate all paths explicitly
    #  - it does extra housekeeping to avoid cycles
    # We can do better
    # Our input turns out to be acyclic, and we don't care about the paths, just the count
    # So we visit each node in topological order and count the edges pointing out -
    #   if we have the number of paths from `start` to `here`, times the edges from `here` to `there`,
    #   that gives us all the paths from `start` to `there` via `here`
    #   the sum of those across all nodes before `there` in topological order is necessarily ALL
    #   the paths from `start` to `there`
    # assert nx.is_directed_acyclic_graph(G)
    npaths = Counter([source])
    for here in nx.topological_sort(G):
        # theoretically we should start at source rather than "whatever is first topologically"
        # but it doesnt seem to matter
        for there in G.successors(here):
            npaths[there] += npaths[here]
        if here == target:
            return npaths[target]

def part_1(rawdata):
    G = nx.DiGraph()
    G.add_edges_from([(source.removesuffix(":"), target) for source, *targets in (l.split() for l in rawdata.splitlines()) for target in targets])
    # return mit.ilen(nx.all_simple_paths(G, "you", "out"))
    return str(dag_path_count(G,"you", "out"))

def part_2(rawdata):
    G = nx.DiGraph()
    G.add_edges_from([(source.removesuffix(":"), target) for source, *targets in (l.split() for l in rawdata.splitlines()) for target in targets])

    fft_first = dag_path_count(G, "svr", "fft") * dag_path_count(G, "fft", "dac") * dag_path_count(G, "dac", "out")
    dac_first = dag_path_count(G, "svr", "dac") * dag_path_count(G, "dac", "fft") * dag_path_count(G, "fft", "out")
    # breakpoint()
    return str(fft_first+dac_first)


from aocd import puzzle, submit
import pytest

@pytest.mark.parametrize("data, result",
     [(ex.input_data, ex.answer_a) for ex in puzzle.examples])
def test_part_1(data, result):
    if result == "out":
        result = "5" #aoce parsing error
    assert part_1(data) == result

# aoce fails to notce part 2 has different objects to part 1
@pytest.mark.parametrize("data, result",
[("""svr: aaa bbb
aaa: fft
fft: ccc
bbb: tty
tty: ccc
ccc: ddd eee
ddd: hub
hub: fff
eee: dac
dac: fff
fff: ggg hhh
ggg: out
hhh: out""", "2")] )
def test_part_2(data, result):
    assert part_2(data) == result

if __name__ == "__main__":
    res = pytest.main([__file__])
    if res:
        sys.exit(res.value)

    submit(part_1(puzzle.input_data), part="a", reopen=False)
    submit(part_2(puzzle.input_data), part="b", reopen=False)
