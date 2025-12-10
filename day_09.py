#!/usr/bin/env python
import sys
import itertools as it

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

def part_2(rawdata, debug=False):
    red_tiles = [coord(line) for line in rawdata.splitlines()]
    midpoints = [(p1+p2)/2 for p1,p2 in it.pairwise(red_tiles + [red_tiles[0]])]

    def valid_rectangle(a,b):
        left, right = min(a.real, b.real), max(a.real, b.real)
        top, bottom = min(a.imag, b.imag), max(a.imag, b.imag)
        return not any(left < z.real < right and top < z.imag < bottom for z in red_tiles+midpoints)

    biggest = max(area(a,b) for a,b in it.combinations(red_tiles,2) if valid_rectangle(a,b))
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
    assert part_2(data, debug=True) == result

if __name__ == "__main__":
    res = pytest.main([__file__])
    if res:
        sys.exit(res.value)

    submit(part_1(puzzle.input_data), part="a", reopen=False)
    submit(part_2(puzzle.input_data), part="b", reopen=False)
