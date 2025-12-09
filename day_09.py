#!/usr/bin/env python
import sys
import itertools as it
from collections import defaultdict
import portion as P

def coord(data):
    a,b = data.split(",")
    return complex(int(a), int(b))

def area(a,b):
    dx = abs(a.real-b.real)+1
    dy = abs(a.imag-b.imag)+1
    return int(dx*dy)

def part_1(rawdata):
    coords = [coord(line) for line in rawdata.splitlines()]

    biggest = max(area(a,b) for a,b in it.combinations(coords,2) )
    return str(biggest)

def part_2(rawdata):
    red_tiles = [coord(line) for line in rawdata.splitlines()]
    perimeter = set(red_tiles)

    for a,b in it.pairwise(red_tiles):
        if a.real == b.real:
            lo_y = int(min(a.imag,b.imag))
            hi_y = int(max(a.imag,b.imag))
            perimeter |= {complex(a.real,y) for y in range(lo_y,hi_y)}
        elif a.imag == b.imag:
            lo_x = int(min(a.real,b.real))
            hi_x = int(max(a.real,b.real))
            perimeter |= {complex(x,a.imag) for x in range(lo_x,hi_x)}

    edge_groups = defaultdict(list)
    for x, cs in it.groupby(perimeter, lambda c: c.real):
        edge_groups[int(x)].extend(int(c.imag) for c in cs)

    all_tiles = {x: P.empty() for x in edge_groups}
    for x, col in edge_groups.items():
        col.sort()
        for lo_y, hi_y in it.pairwise(col):
            all_tiles[x] |= P.closed(lo_y,hi_y)

    # hope like all get out that this shape is convex
    biggest = max(area(a,b) for a,b in it.combinations(red_tiles,2) 
                if b.imag in all_tiles[a.real] and a.imag in all_tiles[b.real] )
    return str(biggest)
        

from aocd import puzzle, submit
import pytest

@pytest.mark.parametrize("data, result",
     [(ex.input_data, ex.answer_a) for ex in puzzle.examples])
def test_part_1(data, result):
    result = "50" # aoce parsing error
    assert part_1(data) == result

@pytest.mark.parametrize("data, result",
     [(ex.input_data, ex.answer_b) for ex in puzzle.examples])
def test_part_2(data, result):
    result = "24" # more aoce parsing error
    assert part_2(data) == result

if __name__ == "__main__":
    res = pytest.main([__file__])
    if res:
        sys.exit(res.value)

    submit(part_1(puzzle.input_data), part="a", reopen=False)
    submit(part_2(puzzle.input_data), part="b", reopen=False)
